#!/usr/bin/env python3
"""Generate publications.html and publicationsCN.html from data/publications.json.

Run this after editing data/publications.json (e.g. adding a new paper):

    python tools/build_pubs.py

Output pages are fully static: system fonts, one local stylesheet, zero
JavaScript and zero external CDNs.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data" / "publications.json"

PAGES = {
    "publications.html": {
        "lang": "en",
        "title": "Publications — Yi Gao",
        "desc": "Publications of Yi Gao: journal papers, book chapters, open-science "
                "contributions, and refereed conference papers.",
        "brand": "Yi Gao",
        "brand_sub": "Medical AI × Clinical Translation",
        "nav": [("index.html", "Home"), ("research.html", "Research"),
                ("software.html", "Open Science"), ("publications.html", "Publications")],
        "lang_link": ("publicationsCN.html", "中文版"),
        "page_eyebrow": "138 publications · 2004 – 2026",
        "page_title": "Publications",
        "page_sub": "Author names in <b>bold</b> are mine; <b>bold&nbsp;*</b> marks the corresponding author.",
        "scholar_label": "Complete citation data on",
        "footer_org": "Yi Gao · Shenzhen University",
        "footer_links": ("research.html", "Research", "software.html", "Open Science"),
        "other_label": "Other formats",
    },
    "publicationsCN.html": {
        "lang": "zh-CN",
        "title": "文章列表 — 高毅",
        "desc": "高毅的论文列表：期刊论文与书籍章节、开放科学贡献、同行评审会议论文。",
        "brand": "高毅",
        "brand_sub": "医学人工智能 × 临床转化",
        "nav": [("indexCN.html", "主页"), ("researchCN.html", "研究"),
                ("softwareCN.html", "开源与软件"), ("publicationsCN.html", "文章列表")],
        "lang_link": ("publications.html", "English"),
        "page_eyebrow": "138 篇论文 · 2004 – 2026",
        "page_title": "文章列表",
        "page_sub": "<b>加粗</b>为本人生效作者名，<b>加粗&nbsp;*</b>表示通讯作者。",
        "scholar_label": "完整引用数据见",
        "footer_org": "高毅 · 深圳大学",
        "footer_links": ("researchCN.html", "研究", "softwareCN.html", "开源与软件"),
        "other_label": "其他入口",
    },
}

SCHOLAR_URL = "https://scholar.google.com/citations?user=wnl1lfcAAAAJ"

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#06101b">
  <link rel="icon" type="image/svg+xml" href="images/favicon.svg">
  <link rel="stylesheet" href="assets/css/main.css">
</head>
<body>

<header class="site-header">
  <div class="inner">
    <span class="brand">
      <a href="{home}">{brand}</a>
      <span class="brand-sub">{brand_sub}</span>
    </span>
    <nav class="site-nav">
{nav_html}
      <a class="lang" href="{lang_href}">{lang_label}</a>
    </nav>
  </div>
</header>

<main>
  <section class="page-hero">
    <div class="inner">
      <p class="eyebrow">{page_eyebrow}</p>
      <h1 class="page-title">{page_title}</h1>
      <p class="page-sub">{page_sub}</p>
    </div>
  </section>

  <section class="band">
    <div class="inner">
      <nav class="pub-nav">
        <span>{scholar_label} <a href="{scholar_url}">Google Scholar</a></span>
{section_nav}
      </nav>

{sections_html}
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="inner">
    <span>{footer_org}</span>
    <span><a href="{fl1_href}">{fl1_label}</a> · <a href="{fl2_href}">{fl2_label}</a> · gaoyi@gatech.edu</span>
  </div>
</footer>

</body>
</html>
"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_section(sec: dict, title_key: str, nav: bool) -> str:
    n = len(sec["items"])
    heading = f'<h2><a id="{sec["id"]}" href="#{sec["id"]}">{esc(sec[title_key])}</a>' \
              f'<span class="count">{n}</span></h2>'
    tag = "ol" if sec.get("ordered") else "ul"
    lis = "\n".join(f"      <li>{item}</li>" for item in sec["items"])
    return f'  <section class="pub-section">\n    {heading}\n    <{tag} class="pub-list">\n{lis}\n    </{tag}>\n  </section>'


def build_page(cfg: dict, data: dict) -> str:
    # build nav with active state on the page being generated
    page_href = "publications.html" if cfg["lang"] == "en" else "publicationsCN.html"
    nav_html = "\n".join(
        f'      <a class="active" href="{href}">{label}</a>' if href == page_href
        else f'      <a href="{href}">{label}</a>'
        for href, label in cfg["nav"]
    )
    home = cfg["nav"][0][0]

    section_nav = "\n".join(
        f'    <a href="#{sec["id"]}">{esc(sec["title_" + ("en" if cfg["lang"] == "en" else "cn")])}</a>'
        for sec in data["sections"]
    )

    title_key = "title_" + ("en" if cfg["lang"] == "en" else "cn")
    sections_html = "\n\n".join(render_section(sec, title_key, True) for sec in data["sections"])

    fl_href, fl_label, fl2_href, fl2_label = cfg["footer_links"]
    return TEMPLATE.format(
        lang=cfg["lang"], title=cfg["title"], desc=esc(cfg["desc"]),
        brand=cfg["brand"], brand_sub=cfg["brand_sub"], home=home, nav_html=nav_html,
        lang_href=cfg["lang_link"][0], lang_label=cfg["lang_link"][1],
        page_eyebrow=cfg["page_eyebrow"],
        page_title=cfg["page_title"], page_sub=cfg["page_sub"],
        scholar_label=cfg["scholar_label"], scholar_url=SCHOLAR_URL,
        section_nav=section_nav, sections_html=sections_html,
        footer_org=cfg["footer_org"],
        fl1_href=fl_href, fl1_label=fl_label, fl2_href=fl2_href, fl2_label=fl2_label,
    )


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    for filename, cfg in PAGES.items():
        html = build_page(cfg, data)
        out = ROOT / filename
        out.write_text(html, encoding="utf-8")
        n = sum(len(s["items"]) for s in data["sections"])
        print(f"Wrote {out.name}: {n} entries")


if __name__ == "__main__":
    main()
