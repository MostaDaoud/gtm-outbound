#!/usr/bin/env python3
"""Render the chart SVGs to PNG at 3x via headless Chrome.

Google Docs cannot insert SVG, so the PNGs are the deliverable; the SVGs are kept
as the editable source. 3x device scale keeps the type crisp when Docs scales the
image down to the text column.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
SCALE = 3
CHROME = next(
    (
        p
        for p in (
            Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        )
        if p.exists()
    ),
    None,
)
if CHROME is None:
    sys.exit("No Chrome or Edge found.")


def dimensions(svg: str) -> tuple[int, int]:
    w = re.search(r'\bwidth="(\d+)"', svg)
    h = re.search(r'\bheight="(\d+)"', svg)
    if not (w and h):
        raise ValueError("SVG needs literal width and height attributes")
    return int(w.group(1)), int(h.group(1))


for svg_path in sorted(HERE.glob("*.svg")):
    svg = svg_path.read_text(encoding="utf-8")
    width, height = dimensions(svg)
    png = svg_path.with_suffix(".png")

    # Chrome screenshots the viewport, so the page must be exactly the SVG box with
    # no margin, no scrollbars, and nothing else in flow.
    html = (
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;overflow:hidden;background:#fff}"
        "svg{display:block}</style>" + svg
    )
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html, encoding="utf-8")
        out = Path(tmp) / "shot.png"
        subprocess.run(
            [
                str(CHROME),
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--default-background-color=FFFFFFFF",
                f"--force-device-scale-factor={SCALE}",
                f"--window-size={width},{height}",
                f"--screenshot={out}",
                page.as_uri(),
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        if not out.exists():
            sys.exit(f"Chrome produced no output for {svg_path.name}")
        shutil.copyfile(out, png)

    kb = png.stat().st_size / 1024
    print(f"{png.name:<32}{width * SCALE} x {height * SCALE} px   {kb:,.0f} KB")
