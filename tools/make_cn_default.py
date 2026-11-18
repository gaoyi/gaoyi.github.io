# -*- coding: utf-8 -*-
"""Make Chinese the default landing page; fix all CN pages to link CN targets."""
import os, re, glob

SITE = r"D:/usr/01_work/01_project/gaoyi.github.io"

def read(p): return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)

report = []

# ---- Step 1: index.html becomes Chinese; English home moves to indexEN.html ----
cn = read(os.path.join(SITE, "indexCN.html"))
en = read(os.path.join(SITE, "index.html"))

# new Chinese index.html
c = cn
c = c.replace('href="indexCN.html"', 'href="index.html"')                     # brand + nav
c = c.replace('<a class="lang" href="index.html">English</a>',
              '<a class="lang" href="indexEN.html">English</a>')
for a in ["breast", "brain", "spine", "pathology"]:
    c = c.replace('href="research/%s.html"' % a, 'href="research/%sCN.html"' % a)
c = c.replace('href="research.html#methods"', 'href="researchCN.html#methods"')
write(os.path.join(SITE, "index.html"), c)
report.append("index.html  <- Chinese landing")

# English home at indexEN.html
e = en
e = e.replace('href="index.html"', 'href="indexEN.html"')                      # brand + Home
e = e.replace('<a class="lang" href="indexCN.html">中文版</a>',
              '<a class="lang" href="index.html">中文版</a>')
write(os.path.join(SITE, "indexEN.html"), e)
report.append("indexEN.html <- English home")

os.remove(os.path.join(SITE, "indexCN.html"))
report.append("indexCN.html removed")

# ---- Step 2: EN top pages: Home/brand -> indexEN.html ----
for p in ["research.html", "software.html", "publications.html"]:
    fp = os.path.join(SITE, p); s = read(fp)
    s2 = s.replace('href="index.html"', 'href="indexEN.html"')
    if s2 != s: write(fp, s2); report.append(p + ": home -> indexEN.html")

# ---- Step 3: CN top pages: home -> index.html ----
for p in ["researchCN.html", "softwareCN.html", "publicationsCN.html"]:
    fp = os.path.join(SITE, p); s = read(fp)
    s2 = s.replace('href="indexCN.html"', 'href="index.html"')
    if s2 != s: write(fp, s2); report.append(p + ": home -> index.html")

# ---- Step 4: researchCN.html subpage cards -> CN subpages ----
fp = os.path.join(SITE, "researchCN.html"); s = read(fp)
n = 0
for a in ["breast", "brain", "spine", "pathology", "others",
          "seg", "reg", "syn", "shape", "radiomics"]:
    old = 'href="research/%s.html"' % a; new = 'href="research/%sCN.html"' % a
    n += s.count(old); s = s.replace(old, new)
write(fp, s); report.append("researchCN.html: %d subpage links -> CN" % n)

# ---- Step 5: EN research subpages: home -> ../indexEN.html ----
for fp in glob.glob(os.path.join(SITE, "research", "*.html")):
    b = os.path.basename(fp); s = read(fp)
    if b.endswith("CN.html"): continue
    s2 = s.replace('href="../index.html"', 'href="../indexEN.html"')
    if s2 != s: write(fp, s2); report.append("research/" + b + ": home -> indexEN")

# ---- Step 6: CN research subpages: nav/footer top links -> CN ----
for fp in glob.glob(os.path.join(SITE, "research", "*CN.html")):
    b = os.path.basename(fp); s = read(fp); n = 0
    for t in ["research", "software", "publications"]:
        old = 'href="../%s.html"' % t; new = 'href="../%sCN.html"' % t
        n += s.count(old); s = s.replace(old, new)
    if n: write(fp, s); report.append("research/" + b + ": %d top links -> CN" % n)

print("\n".join(report))

# ---- Audit: any remaining cross-language leaks ----
print("\n--- audit ---")
problems = 0
for fp in glob.glob(os.path.join(SITE, "*.html")) + glob.glob(os.path.join(SITE, "research", "*.html")):
    rel = os.path.relpath(fp, SITE); s = read(fp)
    for m in re.findall(r'href="([^"#]+)"', s):
        if m.startswith("http") or m.endswith(".css") or m.endswith(".svg"): continue
        target = os.path.normpath(os.path.join(os.path.dirname(rel), m))
        if not os.path.exists(os.path.join(SITE, target)):
            print("DEAD LINK: %s -> %s" % (rel, m)); problems += 1
    if "indexCN.html" in s:
        print("STALE indexCN ref: %s" % rel); problems += 1
print("problems:", problems)
