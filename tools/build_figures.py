#!/usr/bin/env python3
"""Generate the ABUS detection-rate comparison figure (CN + EN) as standalone SVG.

Zero dependencies: plain SVG, system fonts, no JS.
Output: images/fig-abus-cdr-cn.svg, images/fig-abus-cdr-en.svg

To add a study (e.g. the iScience paper), append to ROWS below and rerun.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images"

W, H = 1200, 840
LABEL_W = 430
BAR_X = 452
MAX_VAL = 4.5
BAR_MAX = 640
ROW_TOP = 208
ROW_H = 60
BAR_H = 26

# Our studies deliberately use a warm amber palette — the complement of the
# navy/cyan site theme — so they read as a separate colour family, not just a
# brighter shade of the benchmark bars.
OURS = "#ffb35c"
OURS_GLOW = "#ffd9a0"
OURS_EDGE = "#ffe6c2"
OURS_LABEL = "#fff2e2"
OURS_SUB = "#d8ae86"
FOREIGN = "#3f7f9e"
BASELINE = "#4d5f6d"

ROWS = [
    # label, sub, value, display, group, ref
    ("深圳福田 · 手持超声", "n=21,405 · 2024", 0.47, "0.47", "base", 2),
    ("中国农村两癌筛查 · 超声优化流程", "n=1,501,753 · 2015", 0.85, "0.85", "base", 1),
    ("深圳福田 · AI-ABUS", "n=14,766 · 2024", 1.69, "1.69", "ours", 2),
    ("韩国全国筛查", "2016", 2.69, "2.69", "foreign", 3),
    ("我们 · 深圳组织性筛查 ABUS", "n=11,703 · 2026 · iScience", 3.08, "3.08", "ours", 7),
    ("日本 J-START · 乳腺X线组", "2016", 3.30, "3.30", "foreign", 4),
    ("我们 · 多中心远程阅片", "n=10,344 · 2024", 3.70, "3.70", "ours", 5),
    ("我们 · 46 社区中心远程阅片", "n=5,978 · 2024", 4.00, "4.00", "ours", 6),
]

ROWS_EN = [
    ("Shenzhen Futian · handheld US", "n=21,405 · 2024", 0.47, "0.47", "base", 2),
    ("Rural China program · optimized US", "n=1,501,753 · 2015", 0.85, "0.85", "base", 1),
    ("Shenzhen Futian · AI-ABUS", "n=14,766 · 2024", 1.69, "1.69", "ours", 2),
    ("Korea · national screening", "2016", 2.69, "2.69", "foreign", 3),
    ("Ours · Shenzhen organized screening", "n=11,703 · 2026 · iScience", 3.08, "3.08", "ours", 7),
    ("Japan J-START · mammography arm", "2016", 3.30, "3.30", "foreign", 4),
    ("Ours · multicentre remote reading", "n=10,344 · 2024", 3.70, "3.70", "ours", 5),
    ("Ours · 46 centres, remote reading", "n=5,978 · 2024", 4.00, "4.00", "ours", 6),
]

TEXT = {
    "cn": {
        "title": "乳腺癌检出率：我们的模式与国内外基准",
        "sub": "每千名筛查女性检出的乳腺癌例数（‰）",
        "sub_tag": "　·　橙色为我们的研究",
        "unit_ticks": ["0", "1", "2", "3", "4"],
        "foot": [
            "数据来源：[1] 马兰等，中华肿瘤杂志 2021;43(4) · [2] 中华医学杂志 2025;105(32) · [3] 韩国乳腺癌筛查联盟 2016",
            "[4] Ohuchi et al., Lancet 2016（J-START）· [5] 中华肿瘤杂志 2024;46(11) · [6] Dang et al., AJR 2024",
            "[7] Sun W, et al. iScience 2026;29:118186 — AI-ABUS 3.08‰ vs 手持超声 1.22‰（n=11,703 / 11,435）",
            "检出率受年龄结构、首筛比例与随访完整性影响，跨研究比较仅供参考。橙色行 = 本研究组数据。",
        ],
        "legend": [("我们的研究（高亮）", OURS), ("日韩 / 外部 AI 基准", FOREIGN), ("中国既往筛查基准", BASELINE)],
    },
    "en": {
        "title": "Breast cancer detection rate: our model vs benchmarks",
        "sub": "Cancers detected per 1,000 women screened (‰)",
        "sub_tag": "  ·  amber = our studies",
        "unit_ticks": ["0", "1", "2", "3", "4"],
        "foot": [
            "Sources: [1] Ma et al., Chin J Oncol 2021 · [2] Natl Med J China 2025;105(32) · [3] Korean Breast Cancer Screening Alliance 2016",
            "[4] Ohuchi et al., Lancet 2016 (J-START) · [5] Chin J Oncol 2024;46(11) · [6] Dang et al., AJR 2024",
            "[7] Sun W, et al. iScience 2026;29:118186 — AI-ABUS 3.08 vs handheld US 1.22 per 1,000 (n=11,703 / 11,435)",
            "Detection rates depend on age structure, first-round proportion and follow-up completeness. Amber rows = our studies.",
        ],
        "legend": [("Our studies (highlighted)", OURS), ("Japan/Korea & external AI benchmarks", FOREIGN), ("Chinese prior benchmarks", BASELINE)],
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def scale(v: float) -> float:
    return v / MAX_VAL * BAR_MAX


def build(lang: str) -> str:
    T = TEXT[lang]
    rows = ROWS if lang == "cn" else ROWS_EN
    serif = "Georgia, 'Times New Roman', 'Songti SC', SimSun, serif"
    sans = "'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img">',
        f'<title>{esc(T["title"])}</title>',
        f'<desc>{esc(T["sub"])}</desc>',
        f'<rect width="{W}" height="{H}" fill="#0b1d2e"/>',
    ]

    # faint node-grid backdrop: evokes a multi-site screening network without any map boundaries
    parts.append('<g fill="#3a5a70" opacity="0.45">')
    for gx in range(60, W, 96):
        for gy in range(48, H - 40, 92):
            parts.append(f'<circle cx="{gx}" cy="{gy}" r="1.4" opacity="0.28"/>')
    parts.append("</g>")

    # title
    parts.append(f'<text x="48" y="66" font-family="{serif}" font-size="38" fill="#ffffff">{esc(T["title"])}</text>')
    parts.append(f'<text x="48" y="104" font-family="{sans}" font-size="21" fill="#a9b8c2">{esc(T["sub"])}<tspan fill="{OURS}">{esc(T["sub_tag"])}</tspan></text>')

    # scale ticks + guide lines
    for i, t in enumerate(T["unit_ticks"]):
        x = BAR_X + i * scale(1)
        parts.append(f'<line x1="{x}" y1="{ROW_TOP - 16}" x2="{x}" y2="{ROW_TOP + len(rows) * ROW_H - 18}" stroke="#1b3247" stroke-width="1"/>')
        parts.append(f'<text x="{x}" y="{ROW_TOP - 26}" font-family="{sans}" font-size="17" fill="#5f7c8e" text-anchor="middle">{t}</text>')

    # bars
    for i, (label, sub, val, disp, group, ref) in enumerate(rows):
        y = ROW_TOP + i * ROW_H
        ours = group == "ours"
        color = {"ours": OURS, "foreign": FOREIGN, "base": BASELINE}[group]
        bw = max(scale(val), 4)

        # highlighted row band + left rail for our own studies
        if ours:
            parts.append(f'<rect x="32" y="{y - 6}" width="{W - 64}" height="{ROW_H - 6}" rx="8" fill="{OURS}" opacity="0.09"/>')
            parts.append(f'<rect x="32" y="{y - 6}" width="4" height="{ROW_H - 6}" rx="2" fill="{OURS}"/>')

        label_fill = OURS_LABEL if ours else "#e8eef2"
        label_weight = "600" if ours else "400"
        sub_fill = OURS_SUB if ours else "#7f93a1"
        parts.append(f'<text x="48" y="{y + 16}" font-family="{sans}" font-size="21" fill="{label_fill}" font-weight="{label_weight}">{esc(label)}</text>')
        parts.append(f'<text x="48" y="{y + 38}" font-family="{sans}" font-size="15" fill="{sub_fill}">{esc(sub)} · [{ref}]</text>')

        if ours:
            parts.append(f'<rect x="{BAR_X - 3}" y="{y + 1}" width="{bw + 6:.1f}" height="{BAR_H + 6}" rx="8" fill="{OURS}" opacity="0.22"/>')
        stroke = f' stroke="{OURS_EDGE}" stroke-width="1"' if ours else ""
        parts.append(f'<rect x="{BAR_X}" y="{y + 4}" width="{bw:.1f}" height="{BAR_H}" rx="5" fill="{color}"{stroke}/>')
        num_fill = OURS_GLOW if ours else color
        num_size = 27 if ours else 24
        parts.append(f'<text x="{BAR_X + bw + 12:.1f}" y="{y + 25}" font-family="{sans}" font-size="{num_size}" fill="{num_fill}" font-weight="700">{disp}</text>')

    # legend
    ly = ROW_TOP + len(rows) * ROW_H + 14
    lx = 48
    for text, color in T["legend"]:
        parts.append(f'<rect x="{lx}" y="{ly}" width="16" height="16" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{lx + 24}" y="{ly + 14}" font-family="{sans}" font-size="17" fill="#a9b8c2">{esc(text)}</text>')
        lx += 40 + len(text) * (16 if lang == "cn" else 9)

    # footnotes
    fy = ly + 44
    for line in T["foot"]:
        parts.append(f'<text x="48" y="{fy}" font-family="{sans}" font-size="14" fill="#6f8493">{esc(line)}</text>')
        fy += 22

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    for lang, name in (("cn", "fig-abus-cdr-cn.svg"), ("en", "fig-abus-cdr-en.svg")):
        (OUT / name).write_text(build(lang), encoding="utf-8")
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
