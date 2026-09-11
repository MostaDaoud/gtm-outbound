#!/usr/bin/env python3
"""Build a provenance-aware Obsidian vault from Copy Lab artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


INVALID_FILENAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
FRONTMATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
RESERVED = {
    "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

THEME_LABELS = {
    "frameworks": "Frameworks",
    "psychology": "Psychology",
    "headlines": "Headlines",
    "sales_pages": "Sales Pages",
    "emails": "Emails",
    "offers": "Offers",
    "voice": "Voice",
    "ai_workflow": "AI Workflow",
    "examples": "Examples and Swipes",
    "client_work": "Client Work",
    "positioning": "Positioning",
    "research": "Research",
}

THEME_REFERENCES = {
    "frameworks": ["frameworks.md", "classic-direct-response.md"],
    "psychology": ["psychology.md"],
    "headlines": ["headlines.md", "harry-dry-copywriting.md"],
    "sales_pages": ["sales-pages.md", "classic-direct-response.md"],
    "emails": ["emails.md", "lead-and-email-playbooks.md"],
    "offers": ["offers.md"],
    "voice": ["voice.md", "anti-generic-copy.md"],
    "ai_workflow": ["ai-workflow.md", "anti-generic-copy.md"],
    "examples": ["swipe-file.md", "fascination-bullets.md"],
    "client_work": ["client-work.md"],
    "positioning": ["positioning.md"],
    "research": ["research.md"],
}

COURSE_REFERENCES = {
    "Bart Schutz – Master of Online Persuasion": ["psychology.md", "offers.md"],
    "Branding & Brand Strategy": ["positioning.md", "voice.md"],
    "Digital Psychology & Persuasion": ["psychology.md", "research.md"],
    "Drop Dead Copy – AI Copywriting Secrets (Volume 1)": ["ai-workflow.md", "voice.md"],
    "Jason C Fox - Magnetic Content": ["client-work.md", "emails.md", "offers.md"],
    "Kathryn Morrison – Words Are Wands": ["voice.md", "sales-pages.md", "positioning.md"],
    "Kevin Meng - Next-Level AI Content": ["ai-workflow.md", "voice.md"],
    "Maria Wendt – Words Into Money": ["headlines.md", "sales-pages.md", "offers.md"],
    "Neville Medhora – Copywriting Course": ["frameworks.md", "headlines.md", "emails.md", "client-work.md"],
    "Product Marketing": ["positioning.md", "research.md"],
    "Rohan - Copy Launchpad": ["client-work.md", "research.md", "emails.md"],
    "Martin Lindstrom - Buyology": ["psychology.md", "research.md", "positioning.md"],
}


def load_json(path: Path, *, required: bool = True) -> dict[str, Any]:
    if not path.is_file():
        if required:
            raise FileNotFoundError(path)
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_tree_recursive(root: Path) -> str:
    """Hash relevant text paths and contents so a later tree change is visible."""
    digest = hashlib.sha256()
    paths = (
        path for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".txt"}
        and not path.name.startswith("_")
        and path.name.casefold() != "document.md"
    )
    for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix().casefold()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def safe_name(value: str) -> str:
    name = INVALID_FILENAME.sub("-", value).strip().rstrip(".")
    name = re.sub(r"\s+", " ", name) or "Untitled"
    if name.upper() in RESERVED:
        name = f"{name}-note"
    return name[:140].rstrip()


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def frontmatter(
    title: str,
    note_type: str,
    tags: list[str],
    extra: dict[str, str | int | float] | None = None,
) -> str:
    lines = ["---", f"title: {yaml_string(title)}", f"type: {note_type}", "generated: true"]
    lines.append("tags: [" + ", ".join(tags) + "]")
    for key, value in (extra or {}).items():
        rendered = yaml_string(value) if isinstance(value, str) else str(value)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def read_reference(path: Path) -> tuple[str, str]:
    body = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    body = FRONTMATTER.sub("", body)
    match = H1.search(body)
    title = match.group(1).strip() if match else path.stem.replace("-", " ").title()
    if match:
        body = body[: match.start()] + body[match.end() :]
    return title, body.lstrip("\n")


def table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


class VaultWriter:
    def __init__(self, root: Path):
        self.root = root
        self.generated: dict[str, str] = {}

    def generated_file(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = text.rstrip() + "\n"
        path.write_text(data, encoding="utf-8", newline="\n")
        self.generated[Path(relative).as_posix()] = sha256_bytes(data.encode("utf-8"))

    def generated_json(self, relative: str, payload: object) -> None:
        self.generated_file(relative, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

    def seed_file(self, relative: str, text: str) -> None:
        path = self.root / relative
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")

    def seed_json(self, relative: str, payload: object) -> None:
        self.seed_file(relative, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def topic_notes(writer: VaultWriter, references: Path, library: dict[str, Any]) -> dict[str, str]:
    links: dict[str, str] = {}
    used: set[str] = set()
    manifest_refs = library.get("references", {})
    for source in sorted(references.glob("*.md"), key=lambda p: p.name.casefold()):
        title, body = read_reference(source)
        filename = safe_name(title)
        if filename.casefold() in used:
            filename = safe_name(f"{title} - {source.stem}")
        used.add(filename.casefold())
        relative = f"_generated/Topics/{filename}.md"
        record = manifest_refs.get(source.name, {}) if isinstance(manifest_refs, dict) else {}
        actual_hash = sha256_file(source)
        recorded_hash = str(record.get("sha256", ""))
        if recorded_hash and recorded_hash != actual_hash:
            raise ValueError(
                f"reference drift: {source.name} does not match library_manifest.json"
            )
        note = frontmatter(
            title,
            "copy-lab-topic",
            ["copy-lab/topic"],
            {
                "source_file": source.name,
                "source_sha256": actual_hash,
                "citations": int(record.get("citations", 0)),
            },
        )
        note += f"# {title}\n\n"
        note += "> [!info] Rebuildable Copy Lab reference\n"
        note += "> This note mirrors the distilled reference library. Put personal annotations in `Source Notes/`.\n\n"
        note += "[[Copy Lab Dashboard|Dashboard]] · [[Topic Library]]\n\n---\n\n" + body
        writer.generated_file(relative, note)
        links[source.name] = f"_generated/Topics/{filename}"
    return links


def course_notes(writer: VaultWriter, corpus: dict[str, Any], topics: dict[str, str]) -> list[str]:
    links: list[str] = []
    for course in corpus.get("courses", []):
        if not isinstance(course, dict):
            continue
        name = str(course.get("name", "Untitled course"))
        filename = safe_name(name)
        relative = f"_generated/Courses/{filename}.md"
        links.append(f"_generated/Courses/{filename}")
        note = frontmatter(
            name,
            "copy-lab-course",
            ["copy-lab/course"],
            {
                "lessons": int(course.get("lessons", 0)),
                "words": int(course.get("words", 0)),
                "hours": float(course.get("hours", 0)),
            },
        )
        note += f"# {name}\n\n[[Copy Lab Dashboard|Dashboard]] · [[Course Library]]\n\n"
        note += "## Coverage\n\n"
        note += f"- **Lessons:** {int(course.get('lessons', 0)):,}\n"
        note += f"- **Words:** {int(course.get('words', 0)):,}\n"
        note += f"- **Runtime:** {float(course.get('hours', 0)):.2f} hours\n"
        sections = course.get("sections", [])
        if sections:
            note += "\n## Sections\n\n" + "\n".join(f"- {item}" for item in sections) + "\n"
        related = [topics[item] for item in COURSE_REFERENCES.get(name, []) if item in topics]
        if related:
            note += "\n## Best distilled entry points\n\n" + "\n".join(f"- [[{item}]]" for item in related) + "\n"
        note += "\n## Search this course\n\n"
        note += f"```powershell\npython <copy-lab>/scripts/copy_lab.py search \"QUERY\" --course {json.dumps(name, ensure_ascii=False)} --limit 15\n```\n"
        note += "\n> [!note]\n> Use Copy Lab search for quotations and timestamps; this note is a map, not the transcript.\n"
        writer.generated_file(relative, note)
    return links


def source_notes(
    writer: VaultWriter,
    catalog: dict[str, Any],
    source_manifest: dict[str, Any],
) -> list[str]:
    status_by_id = {
        str(item.get("id")): item
        for item in source_manifest.get("sources", [])
        if isinstance(item, dict)
    }
    links: list[str] = []
    for item in catalog.get("sources", []):
        if not isinstance(item, dict):
            continue
        source_id = str(item.get("id", "unknown-source"))
        title = str(item.get("title", source_id))
        author = str(item.get("author", "Unknown"))
        status = status_by_id.get(source_id, {})
        filename = safe_name(f"{author} - {title}")
        relative = f"_generated/Sources/{filename}.md"
        links.append(f"_generated/Sources/{filename}")
        note = frontmatter(
            title,
            "copy-lab-source",
            ["copy-lab/source"],
            {
                "source_id": source_id,
                "author": author,
                "index_status": str(status.get("status", "not-indexed")),
                "records": int(status.get("records", 0)),
            },
        )
        note += f"# {title}\n\n**Author:** {author}  \n"
        note += f"**Format:** {item.get('format', 'unknown')}  \n"
        note += f"**Index status:** {status.get('status', 'not indexed')}  \n"
        note += f"**Citable records:** {int(status.get('records', 0)):,}  \n"
        note += f"**Locator:** {status.get('locator_type', 'unavailable')}\n\n"
        if item.get("source_url"):
            note += f"**Public URL:** {item['source_url']}\n\n"
        note += "## Local provenance\n\n"
        note += f"- Original: `{item.get('source_path', 'not configured')}`\n"
        if item.get("text_path"):
            note += f"- Extracted text: `{item['text_path']}`\n"
        if item.get("ocr_manifest_path"):
            note += f"- OCR manifest: `{item['ocr_manifest_path']}`\n"
        if item.get("transcript_manifest_path"):
            note += f"- Transcript manifest: `{item['transcript_manifest_path']}`\n"
        note += "\n## Retrieve passages\n\n"
        note += f"```powershell\npython <copy-lab>/scripts/copy_lab.py search \"QUERY\" --source books --course {json.dumps(author, ensure_ascii=False)} --limit 15\n```\n"
        note += "\n> [!warning]\n> Indexed means retrievable with provenance. It does not mean every claim in the source has been independently verified.\n"
        writer.generated_file(relative, note)
    return links


def theme_notes(writer: VaultWriter, mining: dict[str, Any], topics: dict[str, str]) -> list[str]:
    links: list[str] = []
    for key, stats in sorted(mining.get("themes", {}).items()):
        if not isinstance(stats, dict):
            continue
        title = THEME_LABELS.get(key, key.replace("_", " ").title())
        filename = safe_name(title)
        relative = f"_generated/Themes/{filename}.md"
        links.append(f"_generated/Themes/{filename}")
        note = frontmatter(
            title,
            "copy-lab-theme",
            ["copy-lab/theme"],
            {"passage_pool": int(stats.get("pool", 0)), "selected": int(stats.get("selected", 0))},
        )
        note += f"# {title}\n\n**Candidate passages:** {int(stats.get('pool', 0)):,}  \n"
        note += f"**Selected for digest:** {int(stats.get('selected', 0)):,}\n\n"
        related = [topics[item] for item in THEME_REFERENCES.get(key, []) if item in topics]
        if related:
            note += "## Distilled references\n\n" + "\n".join(f"- [[{item}]]" for item in related) + "\n\n"
        note += "## Search the underlying library\n\n"
        note += "```powershell\npython <copy-lab>/scripts/copy_lab.py search \"QUERY\" --source all --limit 15\n```\n"
        writer.generated_file(relative, note)
    return links


def index_note(title: str, note_type: str, rows: list[list[object]], headers: list[str]) -> str:
    note = frontmatter(title, note_type, ["copy-lab/dashboard"])
    note += f"# {title}\n\n[[Copy Lab Dashboard|Dashboard]]\n\n"
    note += "| " + " | ".join(headers) + " |\n"
    note += "|" + "|".join("---" for _ in headers) + "|\n"
    for row in rows:
        note += "| " + " | ".join(table_cell(value) for value in row) + " |\n"
    return note


def build_dashboards(
    writer: VaultWriter,
    corpus: dict[str, Any],
    mining: dict[str, Any],
    topics: dict[str, str],
    course_links: list[str],
    source_links: list[str],
    theme_links: list[str],
    source_catalog_available: bool,
) -> None:
    totals = corpus.get("totals", {})
    dashboard = frontmatter("Copy Lab Dashboard", "copy-lab-dashboard", ["copy-lab/dashboard"])
    dashboard += "# Copy Lab Dashboard\n\n"
    dashboard += "> [!abstract] Copy Lab at a glance\n"
    dashboard += f"> **{int(totals.get('lessons', 0)):,} lessons** · **{int(totals.get('words', 0)):,} words** · **{float(totals.get('hours', 0)):.2f} hours** · **{len(topics)} distilled topics**\n\n"
    dashboard += "## Start a job\n\n"
    dashboard += "- [[Workflows/Write Copy|Write copy]]\n- [[Workflows/Critique Copy|Critique copy]]\n"
    dashboard += "- [[Workflows/Swipe Research|Research the library]]\n- [[Workflows/Humanize Copy|Remove generic patterns]]\n"
    dashboard += "- [[Workflows/Refresh Library and Vault|Refresh the library and vault]]\n\n"
    dashboard += "## Library\n\n"
    dashboard += "- [[Topic Library]] — distilled frameworks and playbooks\n"
    dashboard += f"- [[Course Library]] — the {len(course_links)}-course corpus map\n"
    dashboard += "- [[Source Library]] — books, PDFs, letters, and videos\n"
    dashboard += "- [[Theme Coverage]] — mined passage coverage\n"
    dashboard += "- [[Library Health]] — build provenance and current counts\n"
    dashboard += "- [[Copy Lab Workflow.canvas|Workflow canvas]]\n\n"
    dashboard += "## Working space\n\n- [[Inbox/Inbox|Inbox]]\n- [[Projects/Projects|Projects]]\n- [[Source Notes/Source Notes|Source notes]]\n- [[Templates/Templates|Templates]]\n\n"
    if not source_catalog_available:
        dashboard += "> [!warning] Local source catalog unavailable\n> The course and topic library built successfully, but external books and videos were not mapped.\n"
    writer.generated_file("Copy Lab Dashboard.md", dashboard)

    course_rows = []
    by_name = {str(item.get("name")): item for item in corpus.get("courses", []) if isinstance(item, dict)}
    for link in course_links:
        filename = Path(link).name
        item = next((value for name, value in by_name.items() if safe_name(name) == filename), {})
        course_rows.append([
            f"[[{link}|{item.get('name', filename)}]]",
            f"{int(item.get('lessons', 0)):,}",
            f"{int(item.get('words', 0)):,}",
            f"{float(item.get('hours', 0)):.2f}",
        ])
    writer.generated_file("Dashboards/Course Library.md", index_note("Course Library", "copy-lab-course-index", course_rows, ["Course", "Lessons", "Words", "Hours"]))

    topic_rows = [[f"[[{link}|{Path(link).name}]]", source] for source, link in sorted(topics.items())]
    writer.generated_file("Dashboards/Topic Library.md", index_note("Topic Library", "copy-lab-topic-index", topic_rows, ["Topic", "Reference file"]))

    source_rows = [[f"[[{link}|{Path(link).name}]]"] for link in source_links] or [["Local source catalog not available"]]
    writer.generated_file("Dashboards/Source Library.md", index_note("Source Library", "copy-lab-source-index", source_rows, ["Indexed source"]))

    theme_rows = [[f"[[{link}|{Path(link).name}]]"] for link in theme_links]
    writer.generated_file("Dashboards/Theme Coverage.md", index_note("Theme Coverage", "copy-lab-theme-index", theme_rows, ["Mining theme"]))

    health = frontmatter("Library Health", "copy-lab-health", ["copy-lab/dashboard"])
    health += "# Library Health\n\n"
    health += f"- **Courses:** {int(totals.get('courses', len(course_links))):,}\n"
    health += f"- **Lessons:** {int(totals.get('lessons', 0)):,}\n"
    health += f"- **Words:** {int(totals.get('words', 0)):,}\n"
    health += f"- **Runtime:** {float(totals.get('hours', 0)):.2f} hours\n"
    health += f"- **Mined passages kept:** {int(mining.get('passages_kept', 0)):,}\n"
    health += f"- **Unique mined passages:** {int(mining.get('passages_unique', 0)):,}\n"
    health += f"- **Distilled topics:** {len(topics):,}\n"
    health += f"- **Indexed local sources:** {len(source_links):,}\n"
    health += f"- **Mining themes:** {len(theme_links):,}\n\n"
    health += "> [!info]\n> Run the vault validator after every Copy Lab re-mine. These totals describe indexed material, not independent factual verification.\n"
    writer.generated_file("Dashboards/Library Health.md", health)

    canvas = {
        "nodes": [
            {"id": "brief", "type": "text", "text": "Brief\nReader, action, offer, proof", "x": 0, "y": 80, "width": 260, "height": 120},
            {"id": "research", "type": "text", "text": "Research\nSources + swipe search", "x": 340, "y": 0, "width": 260, "height": 120},
            {"id": "strategy", "type": "text", "text": "Strategy\nPositioning + offer", "x": 340, "y": 180, "width": 260, "height": 120},
            {"id": "draft", "type": "text", "text": "Draft\nFramework + format", "x": 680, "y": 80, "width": 260, "height": 120},
            {"id": "critique", "type": "text", "text": "Critique\n100-point rubric", "x": 1020, "y": 80, "width": 260, "height": 120},
            {"id": "final", "type": "text", "text": "Final copy\nProof checked, action clear", "x": 1360, "y": 80, "width": 280, "height": 120},
        ],
        "edges": [
            {"id": "e1", "fromNode": "brief", "fromSide": "right", "toNode": "research", "toSide": "left"},
            {"id": "e2", "fromNode": "brief", "fromSide": "right", "toNode": "strategy", "toSide": "left"},
            {"id": "e3", "fromNode": "research", "fromSide": "right", "toNode": "draft", "toSide": "left"},
            {"id": "e4", "fromNode": "strategy", "fromSide": "right", "toNode": "draft", "toSide": "left"},
            {"id": "e5", "fromNode": "draft", "fromSide": "right", "toNode": "critique", "toSide": "left"},
            {"id": "e6", "fromNode": "critique", "fromSide": "right", "toNode": "final", "toSide": "left"},
        ],
    }
    writer.generated_json("Dashboards/Copy Lab Workflow.canvas", canvas)


def seed_editable(writer: VaultWriter) -> None:
    seeds = {
        "Start Here.md": """# Start Here

Open [[Copy Lab Dashboard]] first.

This vault has two kinds of material:

- `_generated/` and `Dashboards/` are rebuilt from Copy Lab indexes and references.
- `Projects/`, `Inbox/`, `Source Notes/`, `Templates/`, and `Workflows/` belong to you.

Use the core Templates plugin to create a brief or project note. Use Copy Lab's CLI when you need a source passage, timestamp, page, or chapter; Obsidian is the operating surface, while Copy Lab search remains the retrieval authority.
""",
        "Projects/Projects.md": """# Projects

Create one folder per client or product. Start with [[Templates/Copy Project]] and keep the brief, research, drafts, critique, approvals, and final copy together.

## Active

- Add active projects here.

## Archive

- Move completed project links here.
""",
        "Inbox/Inbox.md": "# Inbox\n\nCapture uncategorized ideas, requests, swipe fragments, and follow-ups here. Process them into a project or source note.\n",
        "Source Notes/Source Notes.md": "# Source Notes\n\nKeep your annotations and applied lessons here. Generated source summaries are in [[Source Library]].\n",
        "Templates/Templates.md": "# Templates\n\n- [[Templates/Copy Brief]]\n- [[Templates/Copy Project]]\n- [[Templates/Critique Note]]\n- [[Templates/Swipe Note]]\n- [[Templates/Source Note]]\n- [[Templates/Voice Guide]]\n",
        "Workflows/Write Copy.md": """# Write Copy

1. Create a [[Templates/Copy Brief|Copy Brief]].
2. Confirm reader, awareness, one action, offer, proof, traffic source, sequence position, and voice.
3. Check the offer before polishing language.
4. Choose a framework from [[_generated/Topics/Frameworks|Frameworks]] and the matching format note.
5. Search the corpus for missing evidence or examples with `copy_lab.py search`.
6. Draft, then run the voice and proof checks.
7. Send the draft through [[Workflows/Critique Copy|Critique Copy]].
""",
        "Workflows/Critique Copy.md": """# Critique Copy

1. State the segment, action, traffic source, offer, and available proof.
2. Use [[Critique Rubric]].
3. Score audience psychology, structure, evidence, voice, and offer once each.
4. Quote every failing line.
5. Rank findings by impact and supply a specific fix.
6. Preserve at least two things already working.
""",
        "Workflows/Swipe Research.md": """# Swipe Research

1. Start with [[Topic Library]].
2. Run `python <copy-lab>/scripts/copy_lab.py search \"QUERY\" --source all --limit 15`.
3. Pull surrounding context for load-bearing hits.
4. Save only brief excerpts in a [[Templates/Swipe Note]].
5. Record course and timestamp, or author and page/chapter.
6. Report disagreements and missing coverage honestly.
""",
        "Workflows/Humanize Copy.md": """# Humanize Copy

1. Protect facts, message, action, format, and distinctive lines.
2. Use [[Anti-generic copy pass]] to find clustered patterns, not isolated words.
3. Replace abstraction with verified specifics or explicit placeholders.
4. Match the supplied voice instead of applying a universal casual style.
5. Recheck proof, offer, and action after the voice pass.

Never infer authorship or promise detector results.
""",
        "Workflows/Refresh Library and Vault.md": """# Refresh Library and Vault

1. Run `copy_lab.py doctor`.
2. If courses changed, run `copy_lab.py index` and `copy_lab.py mine`.
3. If local sources changed, run `copy_lab.py ingest`.
4. Validate and update distilled references in a staged Copy Lab package.
5. Run the `copy-lab-vault` builder.
6. Run `validate_vault.py` and inspect [[Library Health]].

Generated notes may be replaced. Personal work in Projects, Inbox, Source Notes, Templates, and Workflows is preserved.
""",
    }
    for path, text in seeds.items():
        writer.seed_file(path, text)

    templates = {
        "Templates/Copy Brief.md": """---
type: copy-brief
status: draft
created: {{date}}
tags: [copy-lab/project]
---
# Copy Brief — 

## One action

## Reader and awareness

## Offer

## Proof available

## Traffic source

## Sequence position

## Voice sample

## Constraints and approvals
""",
        "Templates/Copy Project.md": """---
type: copy-project
status: active
created: {{date}}
tags: [copy-lab/project]
---
# Project — 

## Brief

## Research

## Copy platform

## Drafts

## Critique

## Decisions

## Final
""",
        "Templates/Critique Note.md": """---
type: critique
created: {{date}}
tags: [copy-lab/critique]
---
# Critique — 

**Segment:**  
**Action:**  
**Context confidence:**  

## Score

## Critical findings

## High-impact fixes

## What is already working

## Recommended rewrite order
""",
        "Templates/Swipe Note.md": """---
type: swipe-note
created: {{date}}
tags: [copy-lab/swipe]
---
# Swipe — 

## Passage

## Source and locator

## Principle

## Where I would use it

## Caveat or disagreement
""",
        "Templates/Source Note.md": """---
type: source-note
created: {{date}}
tags: [copy-lab/source-note]
---
# Source Note — 

## Source

## Claim or lesson

## Evidence

## Application

## Limits
""",
        "Templates/Voice Guide.md": """---
type: voice-guide
created: {{date}}
tags: [copy-lab/voice]
---
# Voice Guide — 

## Sounds like

## Does not sound like

## Sentence rhythm

## Vocabulary

## Attitude and humor

## Approved examples

## Lines to preserve
""",
    }
    for path, text in templates.items():
        writer.seed_file(path, text)


def seed_obsidian(writer: VaultWriter) -> None:
    writer.seed_json(".obsidian/app.json", {"alwaysUpdateLinks": True, "showLineNumber": True, "strictLineBreaks": False})
    writer.seed_json(".obsidian/appearance.json", {"baseFontSize": 16, "enabledCssSnippets": ["copy-lab"]})
    writer.seed_json(
        ".obsidian/core-plugins.json",
        ["file-explorer", "global-search", "switcher", "graph", "backlink", "outgoing-link", "tag-pane", "page-preview", "templates", "outline", "word-count", "canvas"],
    )
    writer.seed_json(".obsidian/templates.json", {"folder": "Templates", "dateFormat": "YYYY-MM-DD", "timeFormat": "HH:mm"})
    writer.seed_json(
        ".obsidian/graph.json",
        {
            "collapse-filter": False,
            "search": "-path:_meta",
            "showTags": True,
            "showAttachments": False,
            "hideUnresolved": True,
            "showOrphans": False,
            "colorGroups": [
                {"query": "tag:#copy-lab/course", "color": {"a": 1, "rgb": 3447003}},
                {"query": "tag:#copy-lab/topic", "color": {"a": 1, "rgb": 16750848}},
                {"query": "tag:#copy-lab/source", "color": {"a": 1, "rgb": 10181046}},
                {"query": "tag:#copy-lab/project", "color": {"a": 1, "rgb": 15158332}},
            ],
        },
    )
    writer.seed_file(
        ".obsidian/snippets/copy-lab.css",
        """body { --copy-lab-accent: #f28c28; }
.theme-dark { --copy-lab-accent: #ffad55; }
.markdown-rendered h1 { letter-spacing: -0.025em; }
.markdown-rendered a.internal-link { text-decoration-thickness: 1px; }
.callout[data-callout="abstract"] { --callout-color: 242, 140, 40; }
.tag[href="#copy-lab/project"] { background: color-mix(in srgb, var(--copy-lab-accent) 24%, transparent); }
""",
    )


def clean_stale(root: Path, prior: dict[str, Any], current: set[str]) -> list[str]:
    removed: list[str] = []
    prior_files = prior.get("generated_files", {})
    if not isinstance(prior_files, dict):
        return removed
    allowed_prefixes = ("_generated/", "Dashboards/", "Copy Lab Dashboard.md")
    for relative in sorted(set(prior_files) - current):
        normalized = Path(relative).as_posix()
        if not normalized.startswith(allowed_prefixes):
            continue
        target = (root / normalized).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            continue
        if target.is_file():
            target.unlink()
            removed.append(normalized)
    return removed


def build(copy_lab: Path, data_dir: Path, vault: Path) -> dict[str, Any]:
    assets = copy_lab / "assets"
    references = copy_lab / "references"
    required = [
        assets / "corpus_index.json",
        assets / "library_manifest.json",
        assets / "mining" / "mining_report.json",
        references,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing required Copy Lab input(s): " + ", ".join(missing))

    corpus_path = assets / "corpus_index.json"
    library_path = assets / "library_manifest.json"
    mining_path = assets / "mining" / "mining_report.json"
    catalog_path = data_dir / "sources" / "catalog.json"
    source_manifest_path = data_dir / "sources" / "manifest.json"
    corpus = load_json(corpus_path)
    library = load_json(library_path)
    mining = load_json(mining_path)
    catalog = load_json(catalog_path, required=False)
    source_manifest = load_json(source_manifest_path, required=False)

    vault.mkdir(parents=True, exist_ok=True)
    prior_path = vault / "_meta" / "build-manifest.json"
    prior = load_json(prior_path, required=False)
    writer = VaultWriter(vault)
    seed_obsidian(writer)
    seed_editable(writer)
    topics = topic_notes(writer, references, library)
    courses = course_notes(writer, corpus, topics)
    sources = source_notes(writer, catalog, source_manifest)
    themes = theme_notes(writer, mining, topics)
    build_dashboards(writer, corpus, mining, topics, courses, sources, themes, bool(catalog))

    stale_removed = clean_stale(vault, prior, set(writer.generated))
    inputs = {
        "corpus_index": {"path": str(corpus_path.resolve()), "sha256": sha256_file(corpus_path)},
        "library_manifest": {"path": str(library_path.resolve()), "sha256": sha256_file(library_path)},
        "mining_report": {"path": str(mining_path.resolve()), "sha256": sha256_file(mining_path)},
        "reference_library": {
            "path": str(references.resolve()),
            "sha256": sha256_tree_recursive(references),
        },
    }
    if catalog_path.is_file():
        inputs["source_catalog"] = {"path": str(catalog_path.resolve()), "sha256": sha256_file(catalog_path)}
    if source_manifest_path.is_file():
        inputs["source_manifest"] = {"path": str(source_manifest_path.resolve()), "sha256": sha256_file(source_manifest_path)}
    transcript_root = data_dir.parent / "_transcripts"
    if transcript_root.is_dir():
        inputs["live_transcript_corpus"] = {
            "path": str(transcript_root.resolve()),
            "sha256": sha256_tree_recursive(transcript_root),
        }
    build_id = sha256_bytes(json.dumps(inputs, sort_keys=True).encode("utf-8"))[:16]
    totals = corpus.get("totals", {})
    manifest = {
        "schema_version": 1,
        "build_id": build_id,
        "copy_lab_dir": str(copy_lab.resolve()),
        "data_dir": str(data_dir.resolve()),
        "vault": str(vault.resolve()),
        "inputs": inputs,
        "counts": {
            "topics": len(topics),
            "courses": len(courses),
            "sources": len(sources),
            "themes": len(themes),
            "lessons": int(totals.get("lessons", 0)),
            "words": int(totals.get("words", 0)),
            "hours": float(totals.get("hours", 0)),
        },
        "generated_files": dict(sorted(writer.generated.items())),
        "stale_files_removed": stale_removed,
        "optional_inputs": {
            "source_catalog": catalog_path.is_file(),
            "source_manifest": source_manifest_path.is_file(),
            "live_transcript_corpus": transcript_root.is_dir(),
        },
    }
    prior_path.parent.mkdir(parents=True, exist_ok=True)
    prior_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    config = {"copy_lab_dir": str(copy_lab.resolve()), "data_dir": str(data_dir.resolve()), "vault": str(vault.resolve())}
    (vault / "_meta" / "vault-config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return manifest


def default_paths() -> tuple[Path, Path, Path]:
    skill = Path(__file__).resolve().parent.parent
    workspace = skill.parents[2]
    return skill.parent / "copy-lab", workspace / ".copy-lab-data", workspace / "Copy Lab Vault"


def main(argv: list[str] | None = None) -> int:
    default_copy_lab, default_data, default_vault = default_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy-lab-dir", type=Path, default=default_copy_lab)
    parser.add_argument("--data-dir", type=Path, default=default_data)
    parser.add_argument("--vault", type=Path, default=default_vault)
    args = parser.parse_args(argv)
    try:
        result = build(args.copy_lab_dir, args.data_dir, args.vault)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"build error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "built", **result}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
