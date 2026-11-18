# -*- coding: utf-8 -*-
"""Swap publication-card placeholder SVGs for rendered paper first-page screenshots."""
import os, glob, re

SITE = r"D:/usr/01_work/01_project/gaoyi.github.io"
AREAS = os.path.join(SITE, "images", "areas")

ids = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(AREAS, "*.jpg")))
print("ids:", len(ids))

changed = {}
for page in sorted(glob.glob(os.path.join(SITE, "research", "*.html"))):
    s = open(page, encoding="utf-8").read()
    orig = s
    hits = []
    for cid in ids:
        old = 'src="../images/areas/%s.svg"' % cid
        new = 'class="paper" src="../images/areas/%s.jpg"' % cid
        if old in s:
            hits.append(cid)
            s = s.replace(old, new)
    if s != orig:
        open(page, "w", encoding="utf-8", newline="").write(s)
        changed[os.path.basename(page)] = hits

for k, v in changed.items():
    print(k, len(v), ",".join(v))

# report placeholders still left
left = {}
for page in sorted(glob.glob(os.path.join(SITE, "research", "*.html"))):
    s = open(page, encoding="utf-8").read()
    for m in re.findall(r'areas/([a-zA-Z0-9_-]+)\.svg', s):
        left.setdefault(m, set()).add(os.path.basename(page))
print("\nremaining svg placeholders:")
for k in sorted(left):
    print("  %s -> %s" % (k, ",".join(sorted(left[k]))))
