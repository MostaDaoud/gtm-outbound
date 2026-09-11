"""OCR an image-only PDF into resumable, page-cited external text.

The original PDF is read-only. Each completed page is checkpointed separately,
so interrupted runs resume without reprocessing successful pages.

Usage:
    python ocr_pdf.py SOURCE.pdf --out-dir .linkedin-lab-data/ocr/source-id
    python ocr_pdf.py SOURCE.pdf --out-dir OUTPUT --pages 1,25,100-105
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def find_tool(name: str, explicit: Path | None = None) -> Path:
    """Find an OCR dependency, including Codex's bundled Poppler runtime."""
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit.expanduser())
    if name == "tesseract":
        for variable in ("ProgramFiles", "ProgramFiles(x86)"):
            root = os.environ.get(variable)
            if root:
                candidates.append(Path(root) / "Tesseract-OCR" / "tesseract.exe")
    if name == "pdftoppm":
        candidates.append(
            Path.home()
            / ".cache"
            / "codex-runtimes"
            / "codex-primary-runtime"
            / "dependencies"
            / "native"
            / "poppler"
            / "Library"
            / "bin"
            / "pdftoppm.exe"
        )
    if name == "pdfinfo":
        candidates.append(
            Path.home()
            / ".cache"
            / "codex-runtimes"
            / "codex-primary-runtime"
            / "dependencies"
            / "native"
            / "poppler"
            / "Library"
            / "bin"
            / "pdfinfo.exe"
        )
    located = shutil.which(name)
    if located:
        candidates.append(Path(located))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(
        f"Could not find {name}. Pass --{name.replace('_', '-')} or install it first."
    )


def pdf_page_count(pdf: Path, pdfinfo: Path) -> int:
    result = subprocess.run(
        [str(pdfinfo), str(pdf)], check=True, capture_output=True, text=True
    )
    match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", result.stdout)
    if not match:
        raise ValueError("pdfinfo did not report a page count")
    return int(match.group(1))


def parse_pages(spec: str, page_count: int) -> list[int]:
    """Parse ``1,4,10-15`` page selections and validate their bounds."""
    selected: set[int] = set()
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if "-" in item:
            start_text, end_text = item.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start > end:
                raise ValueError(f"invalid descending page range: {item}")
            selected.update(range(start, end + 1))
        else:
            selected.add(int(item))
    if not selected:
        raise ValueError("page selection is empty")
    invalid = sorted(page for page in selected if page < 1 or page > page_count)
    if invalid:
        raise ValueError(f"pages outside 1-{page_count}: {invalid[:10]}")
    return sorted(selected)


def page_clock(page: int) -> str:
    """Encode a 1-based page number in LinkedIn Lab's reversible clock form."""
    return f"[{page // 60:02d}:{page % 60:02d}]"


def clean_ocr_text(text: str) -> str:
    lines: list[str] = []
    blank = False
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw.rstrip()
        if not line:
            if lines and not blank:
                lines.append("")
            blank = True
            continue
        lines.append(line)
        blank = False
    return "\n".join(lines).strip()


def tsv_confidence(path: Path) -> tuple[float, int]:
    confidences: list[float] = []
    words = 0
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            text = (row.get("text") or "").strip()
            try:
                confidence = float(row.get("conf") or -1)
            except ValueError:
                confidence = -1
            if text:
                words += 1
                if confidence >= 0:
                    confidences.append(confidence)
    mean = sum(confidences) / len(confidences) if confidences else 0.0
    return round(mean, 2), words


def _page_paths(pages_dir: Path, page: int) -> tuple[Path, Path]:
    stem = f"page-{page:04d}"
    return pages_dir / f"{stem}.txt", pages_dir / f"{stem}.json"


def load_page_result(pages_dir: Path, page: int) -> dict | None:
    text_path, metadata_path = _page_paths(pages_dir, page)
    if not text_path.is_file() or not metadata_path.is_file() or text_path.stat().st_size == 0:
        return None
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return {**metadata, "text": text_path.read_text(encoding="utf-8", errors="replace")}


def ocr_page(
    pdf: Path,
    page: int,
    work_dir: Path,
    pdftoppm: Path,
    tesseract: Path,
    dpi: int,
    language: str,
    psm: int,
) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"page-{page:04d}-", dir=work_dir) as temporary:
        temporary_path = Path(temporary)
        image_prefix = temporary_path / "render"
        subprocess.run(
            [
                str(pdftoppm), "-f", str(page), "-l", str(page), "-singlefile",
                "-gray", "-r", str(dpi), "-png", str(pdf), str(image_prefix),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        image_path = image_prefix.with_suffix(".png")
        output_base = temporary_path / "ocr"
        result = subprocess.run(
            [
                str(tesseract), str(image_path), str(output_base), "-l", language,
                "--oem", "1", "--psm", str(psm), "txt", "tsv",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        text = clean_ocr_text(output_base.with_suffix(".txt").read_text(
            encoding="utf-8", errors="replace"
        ))
        confidence, words = tsv_confidence(output_base.with_suffix(".tsv"))
        return {
            "page": page,
            "confidence": confidence,
            "words": words,
            "characters": len(text),
            "text": text,
            "warning": result.stderr.strip(),
        }


def write_page_result(pages_dir: Path, result: dict) -> None:
    text_path, metadata_path = _page_paths(pages_dir, result["page"])
    text = result["text"].strip()
    atomic_text(text_path, text + "\n")
    metadata = {key: value for key, value in result.items() if key != "text"}
    atomic_text(metadata_path, json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")


def compose_document(pages_dir: Path, pages: list[int], destination: Path) -> None:
    lines = ["## Transcript", ""]
    for page in pages:
        result = load_page_result(pages_dir, page)
        if not result:
            continue
        marker = page_clock(page)
        for line in result["text"].splitlines():
            cleaned = line.strip()
            if cleaned:
                lines.append(f"{marker} {cleaned}")
    atomic_text(destination, "\n".join(lines).rstrip() + "\n")


def build_manifest(
    source: Path,
    source_sha256: str,
    page_count: int,
    pages_dir: Path,
    settings: dict,
) -> dict:
    completed: list[dict] = []
    for page in range(1, page_count + 1):
        result = load_page_result(pages_dir, page)
        if result:
            completed.append({key: value for key, value in result.items() if key != "text"})
    low_quality = [
        result["page"]
        for result in completed
        if result.get("confidence", 0) < settings["min_confidence"]
        or result.get("words", 0) < settings["min_words"]
    ]
    mean_confidence = (
        round(sum(result.get("confidence", 0) for result in completed) / len(completed), 2)
        if completed else 0.0
    )
    return {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_path": str(source),
        "source_sha256": source_sha256,
        "page_count": page_count,
        "completed_pages": len(completed),
        "status": "complete" if len(completed) == page_count else "partial",
        "words": sum(result.get("words", 0) for result in completed),
        "mean_confidence": mean_confidence,
        "low_quality_pages": low_quality,
        "settings": settings,
        "pages": completed,
    }


def run_ocr(args: argparse.Namespace) -> dict:
    source = args.source.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"PDF does not exist: {source}")
    out_dir = args.out_dir.expanduser().resolve()
    pages_dir = out_dir / "pages"
    work_dir = out_dir / "work"
    pages_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    tesseract = find_tool("tesseract", args.tesseract)
    pdftoppm = find_tool("pdftoppm", args.pdftoppm)
    pdfinfo = find_tool("pdfinfo", args.pdfinfo)
    page_count = pdf_page_count(source, pdfinfo)
    source_sha256 = file_hash(source)
    manifest_path = out_dir / "ocr_manifest.json"
    if manifest_path.is_file() and not args.force:
        try:
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            previous = {}
        if previous.get("source_sha256") not in (None, source_sha256):
            raise ValueError("source PDF changed; use a new output directory or --force")

    if args.pages:
        selected = parse_pages(args.pages, page_count)
    else:
        start = max(1, args.start_page)
        end = min(page_count, args.end_page or page_count)
        selected = list(range(start, end + 1))
    if args.force:
        for page in selected:
            for path in _page_paths(pages_dir, page):
                if path.is_file():
                    path.unlink()
    pending = [page for page in selected if not load_page_result(pages_dir, page)]

    settings = {
        "dpi": args.dpi,
        "language": args.language,
        "psm": args.psm,
        "jobs": args.jobs,
        "min_confidence": args.min_confidence,
        "min_words": args.min_words,
        "tesseract": str(tesseract),
        "pdftoppm": str(pdftoppm),
        "pdfinfo": str(pdfinfo),
    }
    print(
        f"OCR source: {source}\nPages: {page_count}; selected: {len(selected)}; "
        f"already complete: {len(selected) - len(pending)}; pending: {len(pending)}",
        flush=True,
    )
    failures: list[dict] = []
    completed_now = 0
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as executor:
        futures = {
            executor.submit(
                ocr_page, source, page, work_dir, pdftoppm, tesseract,
                args.dpi, args.language, args.psm,
            ): page
            for page in pending
        }
        for future in as_completed(futures):
            page = futures[future]
            try:
                result = future.result()
                write_page_result(pages_dir, result)
                completed_now += 1
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                failures.append({"page": page, "error": str(exc)})
            processed = completed_now + len(failures)
            if processed % args.report_every == 0 or processed == len(pending):
                manifest = build_manifest(source, source_sha256, page_count, pages_dir, settings)
                manifest["failures"] = failures
                atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
                print(
                    f"Progress: {processed}/{len(pending)} pending pages handled; "
                    f"{manifest['completed_pages']}/{page_count} total complete",
                    flush=True,
                )

    manifest = build_manifest(source, source_sha256, page_count, pages_dir, settings)
    manifest["failures"] = failures
    atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    destination = out_dir / (
        "document.md" if manifest["status"] == "complete" else "document.partial.md"
    )
    compose_document(pages_dir, list(range(1, page_count + 1)), destination)
    manifest["document_path"] = str(destination)
    manifest["document_sha256"] = file_hash(destination)
    atomic_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="Image-only source PDF")
    parser.add_argument("--out-dir", type=Path, required=True, help="External OCR output directory")
    parser.add_argument("--pages", help="Specific pages/ranges, e.g. 1,25,100-105")
    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--end-page", type=int)
    parser.add_argument("--dpi", type=int, default=240)
    parser.add_argument("--language", default="eng")
    parser.add_argument("--psm", type=int, default=3)
    parser.add_argument("--jobs", type=int, default=max(1, min(4, os.cpu_count() or 1)))
    parser.add_argument("--report-every", type=int, default=25)
    parser.add_argument("--min-confidence", type=float, default=75.0)
    parser.add_argument("--min-words", type=int, default=20)
    parser.add_argument("--force", action="store_true", help="Reprocess selected pages")
    parser.add_argument("--tesseract", type=Path)
    parser.add_argument("--pdftoppm", type=Path)
    parser.add_argument("--pdfinfo", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.dpi < 100 or args.dpi > 600:
        parser.error("--dpi must be between 100 and 600")
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")
    try:
        manifest = run_ocr(args)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print(
            f"OCR {manifest['status']}: {manifest['completed_pages']}/{manifest['page_count']} "
            f"pages, {manifest['words']} words, mean confidence "
            f"{manifest['mean_confidence']:.2f}.\nDocument: {manifest['document_path']}"
        )
    return 0 if not manifest.get("failures") else 1


if __name__ == "__main__":
    raise SystemExit(main())
