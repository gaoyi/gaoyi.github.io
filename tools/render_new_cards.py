import subprocess, tempfile, os, glob
from PIL import Image, ImageChops

J = r"D:/usr/01_work/06_gth818nWrite/manuscript/40_published/j"
C = r"D:/usr/01_work/06_gth818nWrite/manuscript/40_published/c"
OUT = r"D:/usr/01_work/01_project/gaoyi.github.io/images/areas"

def find(patterns, root):
    for pat in patterns:
        hits = glob.glob(os.path.join(root, pat))
        if hits:
            return hits[0]
    return None

jobs = {
    "isci-2026": [find(["2026-SunWanyi-bundled AI.pdf"], J)],
    "nbd-2026": [find(["2026*OSA*.pdf"], J)],
    "tlcr-2026": [find(["2026*PET CT radiomics.pdf"], J)],
    "miccai-2026": [find(["2026 GanShushen MICCAI.pdf"], C)],
}

for cid, pdfs in jobs.items():
    pdf = pdfs[0]
    if not pdf:
        print(cid, "NO PDF")
        continue
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "p")
        subprocess.run(["pdftoppm", "-png", "-r", "120", "-f", "1", "-l", "1", "-singlefile", pdf, p],
                       check=True, capture_output=True)
        im = Image.open(p + ".png").convert("RGB")
    g = im.convert("L"); bg = Image.new("L", g.size, 255)
    bb = ImageChops.difference(g, bg).point(lambda v: 255 if v > 18 else 0).getbbox()
    pad = 10
    l = max(0, bb[0]-pad); t = max(0, bb[1]-pad)
    r = min(im.width, bb[2]+pad); b = min(im.height, bb[3]+pad)
    out = os.path.join(OUT, cid + ".jpg")
    im.crop((l, t, r, b)).save(out, "JPEG", quality=86, optimize=True)
    print(cid, os.path.basename(pdf), im.size, "->", (r-l, b-t), os.path.getsize(out)//1024, "KB")
