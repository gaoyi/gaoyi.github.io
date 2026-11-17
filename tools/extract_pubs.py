#!/usr/bin/env python3
"""Extract publication entries from the legacy publications.html into data/publications.json.

One-time migration tool. Source: the v1 backup of the old site.

Usage:
    python tools/extract_pubs.py [source_html]

The source file defaults to ../gaoyi.github.io-v1-backup/publications.html
(relative to this script). Output: data/publications.json
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SECTIONS = [
    {"id": "journals", "title_en": "Journal Publications and Book Chapters",
     "title_cn": "期刊论文和书籍章节", "ordered": True},
    {"id": "open-science", "title_en": "Contributions to the Open Science",
     "title_cn": "开放科学贡献", "ordered": True},
    {"id": "conferences", "title_en": "Refereed Conference Publications",
     "title_cn": "同行评审会议论文", "ordered": True},
    {"id": "others", "title_en": "Abstracts, Workshops, and Other Publications",
     "title_cn": "摘要、研讨会及其他出版物", "ordered": True},
]


def clean_item(html: str) -> str:
    """Strip trailing list markup and outer whitespace from a raw <li> chunk."""
    html = html.strip()
    html = re.sub(r"</li>\s*$", "", html).strip()
    # remove stray closing </p> left over from legacy markup
    html = html.replace("</p></li>", "").replace("</p>", "")
    # collapse runs of blank lines
    html = re.sub(r"\n\s*\n+", "\n", html)
    return html.strip()


def extract(source: Path) -> dict:
    text = source.read_text(encoding="utf-8")
    # drop HTML comments (legacy page has commented-out <ol> blocks)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    ols = re.findall(r"<ol>(.*?)</ol>", text, flags=re.S | re.I)
    if len(ols) != len(SECTIONS):
        sys.exit(f"Expected {len(SECTIONS)} <ol> sections, found {len(ols)}")

    sections = []
    for meta, block in zip(SECTIONS, ols):
        # split on opening <li> tags only: tolerant of nested/broken legacy markup
        parts = re.split(r"<li>", block, flags=re.I)[1:]
        items = [clean_item(p) for p in parts]
        items = [i for i in items if i]
        meta = dict(meta)
        meta["items"] = items
        sections.append(meta)
        print(f"  {meta['id']}: {len(items)} items")
    return {"sections": sections}


def main() -> None:
    default_src = ROOT.parent / "gaoyi.github.io-v1-backup" / "publications.html"
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else default_src
    if not source.exists():
        sys.exit(f"Source not found: {source}")

    print(f"Extracting from {source}")
    data = extract(source)

    out = ROOT / "data" / "publications.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(s["items"]) for s in data["sections"])
    print(f"Wrote {out} ({total} items total)")


if __name__ == "__main__":
    main()
