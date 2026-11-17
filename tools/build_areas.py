#!/usr/bin/env python3
"""Generate research area sub-pages (research/<id>.html and research/<id>CN.html)
from data/areas.json, mimicking the Open Science page layout:
overview card with pill navigation on top, one card per paper below.

Images: if a paper entry has an explicit "img" (root-relative path), it is used
as-is. Otherwise the script looks for images/areas/<id>.png|jpg|jpeg|webp|svg.
If none exists, a styled SVG placeholder is generated at images/areas/<id>.svg.
To upgrade a placeholder to a real figure later, drop a file named
images/areas/<id>.png (or .jpg/.webp) and rerun this script.

Usage:
    python tools/build_areas.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data" / "areas.json"
OUT_DIR = ROOT / "research"
IMG_DIR = ROOT / "images" / "areas"

LANGS = {
    "en": {
        "file_suffix": ".html", "lang": "en",
        "brand": "Yi Gao", "brand_sub": "Medical AI × Clinical Translation",
        "nav": [("index.html", "Home"), ("research.html", "Research"),
                ("software.html", "Open Science"), ("publications.html", "Publications")],
        "lang_switch": ("CN", "{id}CN.html"),
        "back_label": "← All research areas",
        "overview_title": "Overview",
        "papers_title": "Selected work",
        "papers_sub": "Each card: figure on top, key points below.",
        "venue_label": "Venue", "paper_link": "Paper ↗", "ongoing": "Ongoing",
    },
    "zh": {
        "file_suffix": "CN.html", "lang": "zh-CN",
        "brand": "高毅", "brand_sub": "医学人工智能 × 临床转化",
        "nav": [("index.html", "主页"), ("research.html", "研究"),
                ("software.html", "开源与软件"), ("publications.html", "文章列表")],
        "lang_switch": ("EN", "{id}.html"),
        "back_label": "← 返回研究总览",
        "overview_title": "综述",
        "papers_title": "代表工作",
        "papers_sub": "每张卡片：上方配图，下方要点。",
        "venue_label": "发表", "paper_link": "论文 ↗", "ongoing": "进行中",
    },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {brand}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#06101b">
  <link rel="icon" type="image/svg+xml" href="../images/favicon.svg">
  <link rel="stylesheet" href="../assets/css/main.css">
</head>
<body>

<header class="site-header">
  <div class="inner">
    <span class="brand">
      <a href="../index.html">{brand}</a>
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
      <p class="eyebrow">{kind} · {num}</p>
      <h1 class="page-title">{title}</h1>
      <p class="page-sub">{intro}</p>
      <p style="margin:18px 0 0;"><a class="text-link" href="../research.html">{back_label}</a></p>
    </div>
  </section>

  <section class="band">
    <div class="inner">
      <section class="card" style="margin-bottom:22px">
        <h3>{overview_title}</h3>
        <p>{intro}</p>
        <ul>
{highlights}
        </ul>
        <div class="sw-links">
{pills}
        </div>
      </section>

      <p class="eyebrow">{papers_eyebrow}</p>
      <h2 class="section-title">{papers_title}</h2>
      <p class="section-sub">{papers_sub}</p>
      <div class="grid-2">
{paper_cards}
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="inner">
    <span>{footer_org}</span>
    <span><a href="../publications.html">{fl_pubs}</a> · <a href="../software.html">{fl_soft}</a> · gaoyi@gatech.edu</span>
  </div>
</footer>

</body>
</html>
"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def xml_esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def placeholder_svg(paper: dict) -> str:
    label = f"{paper['venue']} · {paper['year']}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 300">
  <rect width="640" height="300" fill="#0b1d2e"/>
  <path d="M0 75h640M0 150h640M0 225h640M160 0v300M320 0v300M480 0v300" stroke="#1b3247" stroke-width="1" fill="none"/>
  <circle cx="320" cy="128" r="30" fill="none" stroke="#2b9dc8" stroke-width="2"/>
  <path d="M290 128h60M320 98v60" stroke="#2b9dc8" stroke-width="1" stroke-opacity="0.5"/>
  <text x="320" y="196" font-family="Georgia, 'Times New Roman', serif" font-size="19" fill="#80d6ef" text-anchor="middle">{xml_esc(label)}</text>
  <text x="320" y="224" font-family="'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" fill="#a9b8c2" text-anchor="middle">Figure to come · 配图待补</text>
</svg>
'''


def resolve_img(paper: dict) -> str:
    """Return image path relative to the research/ sub-pages ('../images/...')."""
    pid = paper["id"]
    if paper.get("img"):
        p = ROOT / paper["img"]
        if p.exists():
            return "../" + paper["img"].replace("images/", "images/", 1)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        if (IMG_DIR / (pid + ext)).exists():
            return f"../images/areas/{pid}{ext}"
    svg = IMG_DIR / (pid + ".svg")
    if not svg.exists():
        svg.write_text(placeholder_svg(paper), encoding="utf-8")
    return f"../images/areas/{pid}.svg"


def render_card(paper: dict, idx: int, L: dict) -> str:
    lang_key = "en" if L["lang"] == "en" else "cn"
    bullets = paper[f"bullets_{lang_key}"]
    img = resolve_img(paper)
    lis = "\n".join(f"          <li>{b}</li>" for b in bullets)
    if paper.get("doi"):
        title_html = f'<a href="https://doi.org/{esc(paper["doi"])}">{esc(paper["title"])}</a>'
        link_badge = f'<a class="badge" href="https://doi.org/{esc(paper["doi"])}">{L["paper_link"]}</a>'
    else:
        title_html = esc(paper["title"])
        link_badge = ""
    if paper.get("type") == "project":
        status = f'<span class="badge ghost">{L["ongoing"]}</span>'
        link_badge = status
    return f'''        <div class="card proj-card card-numbered" id="{paper["id"]}">
      <div class="card-num">{idx:02d}</div>
      <div class="card-img"><img src="{img}" alt="{esc(paper["title"][:80])}"></div>
      <h3>{title_html}</h3>
      <p class="muted">{esc(paper["venue"])} · {paper["year"]}</p>
      <ul>
{lis}
      </ul>
      <div class="sw-links">{link_badge}</div>
    </div>'''


def build_page(area: dict, lang: str) -> str:
    L = LANGS[lang]
    lang_key = "en" if lang == "en" else "cn"
    title = area[f"title_{lang_key}"]
    intro = area[f"intro_{lang_key}"]
    kind = area[f"kind_{lang_key}"]

    nav_html = "\n".join(
        f'      <a class="active" href="../{href}">{label}</a>' if label in ("Research", "研究")
        else f'      <a href="../{href}">{label}</a>'
        for href, label in L["nav"]
    )

    highlights = "\n".join(f"          <li>{h}</li>" for h in area[f"highlights_{lang_key}"])
    pills = "\n".join(
        f'        <a class="badge" href="#{p["id"]}">{esc(p["pill"])}</a>'
        for p in area["papers"]
    )
    paper_cards = "\n\n".join(render_card(p, i + 1, L) for i, p in enumerate(area["papers"]))

    fl_pubs = "Publications" if lang == "en" else "文章列表"
    fl_soft = "Open Science" if lang == "en" else "开源与软件"
    footer_org = "Yi Gao · Shenzhen University" if lang == "en" else "高毅 · 深圳大学"
    papers_eyebrow = f'{len(area["papers"]):02d} · {L["papers_title"]}'

    lang_href = L["lang_switch"][1].format(id=area["id"])

    return TEMPLATE.format(
        lang=L["lang"], title=esc(title), brand=L["brand"], brand_sub=L["brand_sub"],
        desc=esc(intro[:150]), nav_html=nav_html,
        lang_href=lang_href, lang_label=L["lang_switch"][0],
        kind=esc(kind), num=area["num"], intro=intro, back_label=L["back_label"],
        overview_title=L["overview_title"], highlights=highlights, pills=pills,
        papers_eyebrow=papers_eyebrow, papers_title=L["papers_title"],
        papers_sub=L["papers_sub"], paper_cards=paper_cards,
        footer_org=footer_org, fl_pubs=fl_pubs, fl_soft=fl_soft,
    )


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(exist_ok=True)
    for area in data["areas"]:
        for lang in ("en", "zh"):
            html = build_page(area, lang)
            out = OUT_DIR / (area["id"] + LANGS[lang]["file_suffix"])
            out.write_text(html, encoding="utf-8")
        print(f"  {area['id']}: {len(area['papers'])} cards")
    print(f"Done: {len(data['areas'])} areas x 2 languages -> {OUT_DIR}")


if __name__ == "__main__":
    main()
