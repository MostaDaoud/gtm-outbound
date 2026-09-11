"""Build a provenance-aware local index for books and other source documents.

Only generated passages and hashes are stored in ``.copy-lab-data``. Original
documents stay at their user-owned paths and are never copied into the skill.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Iterable
from xml.etree import ElementTree

from copy_lab_config import (
    resolve_source_catalog,
    resolve_source_dir,
    resolve_source_manifest,
    resolve_source_store,
)

PAGE_CLOCK = re.compile(r"^\[(\d{1,3}):(\d{2})\]\s*(.*)$")
PAGE_TAG = re.compile(r"^\[p(\d+)\]\s*(.*)$", re.IGNORECASE)
VTT_TIMING = re.compile(
    r"^(?P<start>(?:\d{2}:)?\d{2}:\d{2}\.\d{3})\s+-->\s+"
    r"(?P<end>(?:\d{2}:)?\d{2}:\d{2}\.\d{3})"
)
VTT_TAG = re.compile(r"<[^>]+>")
TOKEN_KEY = re.compile(r"[^\w']+", re.UNICODE)
SPACE = re.compile(r"\s+")
MEDIA_FORMATS = {"m4a", "m4b", "mp3", "mp4", "wav"}
SUPPORTED_FORMATS = {"epub", "pdf", "md", "txt", "vtt", *MEDIA_FORMATS}


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


class _VisibleText(HTMLParser):
    """Small dependency-free HTML text and heading extractor."""

    BLOCKS = {
        "address", "article", "aside", "blockquote", "br", "div", "figcaption",
        "footer", "h1", "h2", "h3", "h4", "header", "li", "main", "p",
        "section", "table", "td", "th", "title", "tr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.heading_parts: list[str] = []
        self._skip = 0
        self._heading = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg"}:
            self._skip += 1
        if tag in {"h1", "h2", "h3", "title"} and not self.heading_parts:
            self._heading += 1
        if tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg"} and self._skip:
            self._skip -= 1
        if tag in {"h1", "h2", "h3", "title"} and self._heading:
            self._heading -= 1
        if tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        cleaned = SPACE.sub(" ", data).strip()
        if cleaned:
            self.parts.append(cleaned)
            if self._heading:
                self.heading_parts.append(cleaned)

    @property
    def text(self) -> str:
        lines = [SPACE.sub(" ", line).strip() for line in " ".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line)

    @property
    def heading(self) -> str:
        return SPACE.sub(" ", " ".join(self.heading_parts)).strip()


def chunk_text(text: str, *, target_words: int = 220, overlap_words: int = 35) -> list[str]:
    """Split text into stable, overlapping search passages."""
    words = SPACE.sub(" ", text).strip().split()
    if not words:
        return []
    chunks: list[str] = []
    step = max(1, target_words - overlap_words)
    for start in range(0, len(words), step):
        chunk = words[start : start + target_words]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        if start + target_words >= len(words):
            break
    return chunks


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _epub_documents(archive: zipfile.ZipFile) -> list[str]:
    names = set(archive.namelist())
    try:
        container = ElementTree.fromstring(archive.read("META-INF/container.xml"))
        rootfile = next(
            node.attrib["full-path"]
            for node in container.iter()
            if _local_name(node.tag) == "rootfile" and node.attrib.get("full-path")
        )
        package = ElementTree.fromstring(archive.read(rootfile))
        manifest = {
            node.attrib.get("id", ""): node.attrib
            for node in package.iter()
            if _local_name(node.tag) == "item"
        }
        base = PurePosixPath(rootfile).parent
        ordered: list[str] = []
        for node in package.iter():
            if _local_name(node.tag) != "itemref":
                continue
            item = manifest.get(node.attrib.get("idref", ""), {})
            href = item.get("href")
            if href:
                candidate = str(base / href)
                if candidate in names:
                    ordered.append(candidate)
        if ordered:
            return ordered
    except (KeyError, StopIteration, ElementTree.ParseError, zipfile.BadZipFile):
        pass
    return sorted(
        name for name in names if Path(name).suffix.lower() in {".html", ".htm", ".xhtml"}
    )


def extract_epub(path: Path) -> tuple[list[dict], str, list[str]]:
    chapters: list[dict] = []
    with zipfile.ZipFile(path) as archive:
        for index, name in enumerate(_epub_documents(archive), start=1):
            try:
                raw = archive.read(name).decode("utf-8", errors="replace")
            except (KeyError, OSError):
                continue
            parser = _VisibleText()
            parser.feed(raw)
            if not parser.text:
                continue
            heading = parser.heading or PurePosixPath(name).stem.replace("_", " ")
            chapters.append({"chapter": heading, "chapter_index": index, "text": parser.text})
    return chapters, "epub-stdlib", []


def extract_page_document(path: Path) -> tuple[list[dict], str, list[str]]:
    """Translate imported ``[HH:MM]`` clocks or ``[pN]`` tags into pages."""
    page_parts: dict[int, list[str]] = {}
    saw_page_tag = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = PAGE_CLOCK.match(line.strip())
        if match:
            page = int(match.group(1)) * 60 + int(match.group(2))
            text = SPACE.sub(" ", match.group(3)).strip()
        else:
            tagged = PAGE_TAG.match(line.strip())
            if not tagged:
                continue
            saw_page_tag = True
            page = int(tagged.group(1))
            text = SPACE.sub(" ", tagged.group(2)).strip()
        if text:
            page_parts.setdefault(page, []).append(text)
    pages = [
        {"page": page, "text": " ".join(parts)}
        for page, parts in page_parts.items()
    ]
    method = "page-tag-markdown" if saw_page_tag else "page-clock-markdown"
    return pages, method, []


def _vtt_seconds(value: str) -> float:
    parts = value.split(":")
    if len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    else:
        hours, minutes, seconds = parts
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def _clock(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _token_key(value: str) -> str:
    return TOKEN_KEY.sub("", value.casefold())


def extract_vtt(path: Path, *, window_seconds: int = 30) -> tuple[list[dict], str, list[str]]:
    """Extract a deduplicated, timestamped transcript from rolling WebVTT cues.

    YouTube auto-captions repeatedly carry earlier words into later cues. The
    longest prefix/suffix overlap keeps the visible wording while emitting each
    word only once. Passages are grouped into short clock windows so retrieval
    can cite the point in the video where the passage begins.
    """
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    blocks = re.split(r"\r?\n\s*\r?\n", raw)
    emitted: list[str] = []
    timed_words: list[tuple[float, list[str]]] = []
    cues = 0
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next(
            (index for index, line in enumerate(lines) if VTT_TIMING.match(line)),
            None,
        )
        if timing_index is None:
            continue
        match = VTT_TIMING.match(lines[timing_index])
        if not match:
            continue
        cleaned = html.unescape(
            VTT_TAG.sub("", " ".join(lines[timing_index + 1 :]))
        )
        words = SPACE.sub(" ", cleaned).strip().split()
        if not words:
            continue
        cues += 1
        comparable = [_token_key(word) for word in words]
        previous = [_token_key(word) for word in emitted[-len(words) :]]
        overlap = 0
        maximum = min(len(previous), len(comparable))
        for size in range(maximum, 0, -1):
            if previous[-size:] == comparable[:size]:
                overlap = size
                break
        additions = words[overlap:]
        if additions:
            emitted.extend(additions)
            timed_words.append((_vtt_seconds(match.group("start")), additions))

    windows: dict[int, list[str]] = {}
    for seconds, words in timed_words:
        start = int(seconds) // window_seconds * window_seconds
        windows.setdefault(start, []).extend(words)
    units = [
        {"timestamp": _clock(start), "seconds": start, "text": " ".join(words)}
        for start, words in sorted(windows.items())
        if words
    ]
    warnings = [] if cues else ["WebVTT contained no timed caption cues"]
    return units, "webvtt-overlap-dedupe", warnings


def _extract_pdf_text(path: Path) -> tuple[list[dict], str, list[str]]:
    warnings: list[str] = []
    try:
        from pypdf import PdfReader  # type: ignore

        pages = []
        for number, page in enumerate(PdfReader(str(path)).pages, start=1):
            text = SPACE.sub(" ", page.extract_text() or "").strip()
            if text:
                pages.append({"page": number, "text": text})
        return pages, "pypdf", warnings
    except (ImportError, OSError, ValueError) as exc:
        warnings.append(f"pypdf unavailable or failed: {exc}")

    try:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "pages.txt"
            subprocess.run(
                ["pdftotext", "-layout", str(path), str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            text = output.read_text(encoding="utf-8", errors="replace")
        pages = [
            {"page": number, "text": SPACE.sub(" ", page).strip()}
            for number, page in enumerate(text.split("\f"), start=1)
            if SPACE.sub(" ", page).strip()
        ]
        return pages, "pdftotext", warnings
    except (FileNotFoundError, OSError, subprocess.SubprocessError) as exc:
        warnings.append(f"pdftotext unavailable or failed: {exc}")
        return [], "unavailable", warnings


def _record_base(source: dict, source_path: Path) -> dict:
    return {
        "source_type": source.get("source_type", "book"),
        "source_id": source["id"],
        "title": source["title"],
        "author": source.get("author", ""),
        "format": source.get("format", source_path.suffix.lstrip(".").lower()),
        "course": source["title"],
        "section": source.get("author", ""),
        "path": str(source_path),
        "url": source.get("source_url", ""),
        "score": 0,
    }


def extract_source(source: dict) -> tuple[list[dict], dict]:
    """Extract one catalog entry into normalized, citable passage records."""
    source_path = Path(source["source_path"]).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"source does not exist: {source_path}")
    source_format = str(source.get("format") or source_path.suffix.lstrip(".")).lower()
    if source_format not in SUPPORTED_FORMATS:
        raise ValueError(f"unsupported source format: {source_format}")

    text_path_value = source.get("text_path")
    text_path = Path(text_path_value).expanduser().resolve() if text_path_value else None
    if text_path and not text_path.is_file():
        raise FileNotFoundError(f"text_path does not exist: {text_path}")
    ocr_manifest_value = source.get("ocr_manifest_path")
    ocr_manifest_path = (
        Path(ocr_manifest_value).expanduser().resolve() if ocr_manifest_value else None
    )
    ocr_data: dict = {}
    if ocr_manifest_path:
        if not ocr_manifest_path.is_file():
            raise FileNotFoundError(f"ocr_manifest_path does not exist: {ocr_manifest_path}")
        try:
            ocr_data = json.loads(ocr_manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"invalid OCR manifest: {ocr_manifest_path}: {exc}") from exc
        if ocr_data.get("status") != "complete":
            raise ValueError(f"OCR manifest is not complete: {ocr_manifest_path}")
        if ocr_data.get("source_sha256") != file_hash(source_path):
            raise ValueError("OCR manifest source hash does not match the catalog source")

    transcript_manifest_value = source.get("transcript_manifest_path")
    transcript_manifest_path = (
        Path(transcript_manifest_value).expanduser().resolve()
        if transcript_manifest_value
        else None
    )
    transcript_data: dict = {}
    if transcript_manifest_path:
        if not transcript_manifest_path.is_file():
            raise FileNotFoundError(
                f"transcript_manifest_path does not exist: {transcript_manifest_path}"
            )
        try:
            transcript_data = json.loads(
                transcript_manifest_path.read_text(encoding="utf-8")
            )
        except (OSError, ValueError) as exc:
            raise ValueError(
                f"invalid transcript manifest: {transcript_manifest_path}: {exc}"
            ) from exc
        if transcript_data.get("status") != "complete":
            raise ValueError(f"transcript manifest is not complete: {transcript_manifest_path}")
        if transcript_data.get("source_sha256") != file_hash(source_path):
            raise ValueError("transcript manifest source hash does not match the catalog source")
        if text_path and transcript_data.get("transcript_sha256") != file_hash(text_path):
            raise ValueError("transcript manifest text hash does not match text_path")

    if text_path:
        if text_path.suffix.lower() == ".vtt":
            units, method, warnings = extract_vtt(text_path)
            locator_type = "timestamp"
            if transcript_manifest_path:
                method = "faster-whisper-webvtt"
        else:
            units, method, warnings = extract_page_document(text_path)
            locator_type = "page"
        if units and ocr_manifest_path:
            method = "tesseract-page-clock-markdown"
        elif not units and ocr_manifest_path:
            raise ValueError(f"OCR text contains no page markers: {text_path}")
        elif not units and source_format == "epub":
            units, method, fallback_warnings = extract_epub(source_path)
            locator_type = "chapter"
            warnings.extend(fallback_warnings)
            warnings.append("text_path contained no page markers; used EPUB chapters")
        elif not units and source_format == "pdf":
            units, method, fallback_warnings = _extract_pdf_text(source_path)
            warnings.extend(fallback_warnings)
            warnings.append("text_path contained no page markers; used embedded PDF text")
        elif not units and source_format in MEDIA_FORMATS:
            raise ValueError(f"media transcript contains no timed cues: {text_path}")
    elif source_format == "epub":
        units, method, warnings = extract_epub(source_path)
        locator_type = "chapter"
    elif source_format == "pdf":
        units, method, warnings = _extract_pdf_text(source_path)
        locator_type = "page"
    elif source_format == "vtt":
        units, method, warnings = extract_vtt(source_path)
        locator_type = "timestamp"
    elif source_format in MEDIA_FORMATS:
        raise ValueError(f"media source requires a WebVTT text_path: {source_path}")
    else:
        raw = source_path.read_text(encoding="utf-8", errors="replace")
        units, method, warnings = ([{"chapter": source["title"], "text": raw}], "plain-text", [])
        locator_type = "chapter"

    base = _record_base(source, source_path)
    records: list[dict] = []
    for unit in units:
        if locator_type == "page":
            locator = f"page {unit['page']}"
            locator_fields = {"page": unit["page"]}
        elif locator_type == "timestamp":
            locator = f"@ {unit['timestamp']}"
            locator_fields = {
                "timestamp": unit["timestamp"],
                "seconds": unit["seconds"],
            }
        else:
            locator = f"chapter {unit['chapter']}"
            locator_fields = {
                "chapter": unit["chapter"],
                "chapter_index": unit.get("chapter_index"),
            }
        for part, text in enumerate(chunk_text(unit["text"]), start=1):
            records.append(
                {
                    **base,
                    **locator_fields,
                    "locator_type": locator_type,
                    "locator": locator,
                    "lesson": locator,
                    "timestamp": unit["timestamp"] if locator_type == "timestamp" else "",
                    "part": part,
                    "citation": f"{source.get('author', '')} — {source['title']}, {locator}".strip(" —"),
                    "text": text,
                }
            )

    status = "indexed" if records else ("needs_ocr" if source_format == "pdf" else "empty")
    manifest = {
        "id": source["id"],
        "title": source["title"],
        "author": source.get("author", ""),
        "format": source_format,
        "source_path": str(source_path),
        "source_sha256": file_hash(source_path),
        "text_path": str(text_path) if text_path else "",
        "text_sha256": file_hash(text_path) if text_path else "",
        "ocr_manifest_path": str(ocr_manifest_path) if ocr_manifest_path else "",
        "ocr_manifest_sha256": file_hash(ocr_manifest_path) if ocr_manifest_path else "",
        "ocr_mean_confidence": ocr_data.get("mean_confidence"),
        "ocr_low_quality_pages": ocr_data.get("low_quality_pages", []),
        "transcript_manifest_path": str(transcript_manifest_path) if transcript_manifest_path else "",
        "transcript_manifest_sha256": file_hash(transcript_manifest_path) if transcript_manifest_path else "",
        "transcription_model": transcript_data.get("model", ""),
        "locator_type": locator_type,
        "extraction_method": method,
        "status": status,
        "records": len(records),
        "words": sum(len(record["text"].split()) for record in records),
        "warnings": warnings,
    }
    return records, manifest


def load_catalog(path: Path | None = None) -> tuple[Path, list[dict]]:
    catalog_path = resolve_source_catalog(path)
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    sources = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(sources, list):
        raise ValueError("catalog must contain a 'sources' list")
    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("every catalog source must be an object")
        for key in ("id", "title", "source_path"):
            if not source.get(key):
                raise ValueError(f"catalog source is missing '{key}'")
        if source["id"] in seen:
            raise ValueError(f"duplicate source id: {source['id']}")
        seen.add(source["id"])
    return catalog_path, sources


def build_source_index(
    catalog: Path | None = None,
    out_dir: Path | None = None,
) -> dict:
    catalog_path, sources = load_catalog(catalog)
    target = resolve_source_dir(out_dir, for_write=True)
    store_path = target / "passages.jsonl" if out_dir else resolve_source_store()
    manifest_path = target / "manifest.json" if out_dir else resolve_source_manifest()

    records: list[dict] = []
    source_manifests: list[dict] = []
    for source in sorted(sources, key=lambda item: item["id"]):
        extracted, source_manifest = extract_source(source)
        records.extend(extracted)
        source_manifests.append(source_manifest)
    records.sort(
        key=lambda item: (
            item["source_id"],
            item.get("chapter_index") or item.get("page") or item.get("seconds") or 0,
            item["part"],
        )
    )
    payload = "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)
    atomic_text(store_path, payload)
    manifest = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "catalog_path": str(catalog_path.resolve()),
        "catalog_sha256": file_hash(catalog_path),
        "store_path": str(store_path.resolve()),
        "store_sha256": file_hash(store_path),
        "records": len(records),
        "sources": source_manifests,
    }
    atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return manifest


def validate_source_index(
    manifest_path: Path | None = None,
    store_path: Path | None = None,
) -> tuple[list[dict], dict]:
    """Validate external source provenance without requiring an index to exist."""
    manifest_target = resolve_source_manifest(manifest_path)
    store_target = resolve_source_store(store_path)
    if not manifest_target.is_file() and not store_target.is_file():
        return [], {"status": "not_configured", "sources": 0, "records": 0}
    findings: list[dict] = []
    if not manifest_target.is_file():
        return ([{"severity": "High", "file": str(manifest_target), "issue": "Missing source manifest"}],
                {"status": "invalid", "sources": 0, "records": 0})
    try:
        manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ([{"severity": "Critical", "file": str(manifest_target), "issue": f"Invalid source manifest: {exc}"}],
                {"status": "invalid", "sources": 0, "records": 0})
    if not store_target.is_file():
        findings.append({"severity": "High", "file": str(store_target), "issue": "Missing source passage store"})
    elif file_hash(store_target) != manifest.get("store_sha256"):
        findings.append({"severity": "High", "file": str(store_target), "issue": "Source passage store hash changed"})

    catalog_value = manifest.get("catalog_path")
    if catalog_value:
        catalog_path = Path(catalog_value)
        if not catalog_path.is_file():
            findings.append({"severity": "High", "file": str(catalog_path), "issue": "Source catalog is missing"})
        elif file_hash(catalog_path) != manifest.get("catalog_sha256"):
            findings.append({"severity": "High", "file": str(catalog_path), "issue": "Source catalog changed; re-ingest"})

    for source in manifest.get("sources", []):
        path = Path(source.get("source_path", ""))
        if not path.is_file():
            findings.append({"severity": "High", "file": str(path), "issue": "Source file is missing"})
        elif file_hash(path) != source.get("source_sha256"):
            findings.append({"severity": "High", "file": str(path), "issue": "Source file changed; re-ingest"})
        text_value = source.get("text_path")
        if text_value:
            text_path = Path(text_value)
            if not text_path.is_file():
                findings.append({"severity": "High", "file": str(text_path), "issue": "Extracted text file is missing"})
            elif file_hash(text_path) != source.get("text_sha256"):
                findings.append({"severity": "High", "file": str(text_path), "issue": "Extracted text changed; re-ingest"})
        ocr_value = source.get("ocr_manifest_path")
        if ocr_value:
            ocr_path = Path(ocr_value)
            if not ocr_path.is_file():
                findings.append({"severity": "High", "file": str(ocr_path), "issue": "OCR manifest is missing"})
            elif file_hash(ocr_path) != source.get("ocr_manifest_sha256"):
                findings.append({"severity": "High", "file": str(ocr_path), "issue": "OCR manifest changed; re-ingest"})
        transcript_value = source.get("transcript_manifest_path")
        if transcript_value:
            transcript_path = Path(transcript_value)
            if not transcript_path.is_file():
                findings.append({"severity": "High", "file": str(transcript_path), "issue": "Transcript manifest is missing"})
            elif file_hash(transcript_path) != source.get("transcript_manifest_sha256"):
                findings.append({"severity": "High", "file": str(transcript_path), "issue": "Transcript manifest changed; re-ingest"})
        if not source.get("records") and source.get("status") != "needs_ocr":
            findings.append({"severity": "Medium", "file": source.get("title", "source"), "issue": "Source produced no passages"})
    summary = {
        "status": "valid" if not findings else "drifted",
        "sources": len(manifest.get("sources", [])),
        "records": manifest.get("records", 0),
    }
    return findings, summary
