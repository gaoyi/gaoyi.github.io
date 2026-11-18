# -*- coding: utf-8 -*-
"""Render first page of published PDFs to jpg for website publication cards."""
import os, sys, glob, subprocess, tempfile
from PIL import Image

BASE = r"D:/usr/01_work/06_gth818nWrite/manuscript/40_published"
SITE = r"D:/usr/01_work/01_project/gaoyi.github.io"
AREAS = os.path.join(SITE, "images", "areas")

J = os.path.join(BASE, "j")
C = os.path.join(BASE, "c")
BR = os.path.join(J, "breastRelated")

def find(folder, pattern):
    hits = glob.glob(os.path.join(folder, pattern))
    if not hits:
        raise FileNotFoundError(pattern + " in " + folder)
    return hits[0]

# card-id -> absolute pdf path
M = {
    # breast
    "cmj-2025":    find(BR, "2025-*中华医学杂志*.pdf"),
    "ajr-2024":    find(J, "2024 党晓智 AJR*.pdf"),
    "jiim-2026":   find(J, "2026-黄增安-有损压缩.pdf"),
    "i2i-2024":    find(BR, "2024-HuangZengan-Explainable*.pdf"),
    "jbc-2022":    find(J, "2022-Dang-abus-nac.pdf"),
    "zhzl-2024":   find(J, "2024 党晓智 基于自动乳腺超声远程阅片*.pdf"),
    "jmri-2018":   find(BR, "2018 Ding JMRI*.pdf"),
    "jmri-2019":   find(J, "2019 Liu Preoperative*.pdf"),
    # brain
    "nicl-2024":   find(J, "2024 yang-2911 subjects.pdf"),
    "fnins-2023":  find(J, "2023 Fine scale hippocampus*.pdf"),
    "cerebellum-2022": find(J, "2022 Zheng_cerebellum.pdf"),
    "neuroimage-2017": find(J, "2017 ratner-glymphatics.pdf"),
    "bmcp-2025":   find(J, "2025 黄焜 胆红素*.pdf"),
    "cns-2025":    find(J, "2025 杨钦铸*.pdf"),
    "hbm-2018":    find(J, "2018 HBM_bumps.pdf"),
    # others
    "bioinf-2023": find(J, "2022 HuangKaibin-Bioinformatics-Scintigraphy.pdf"),
    "atm-2021":    find(J, "2021 Huang Development and validation*.pdf"),
    "ent-2023":    find(J, "2023 王路*.pdf"),
    "cc-2020":     find(J, "2020 COVID-19 targets the right lung.pdf"),
    "vciba-2022":  find(J, "2022 virtual pancreatoscopy.pdf"),
    # pathology
    "access-2021": find(J, "2021 Yu-slicerscope.pdf"),
    "srep-2025-path": find(J, "2025 GTEX 13种组织.pdf"),
    "intonc-2025": find(J, "2025 HuangQinqin*.pdf"),
    "spie-2017":   find(C, "2016 Zhou SPIE Evaluation of nucleus segmentation*.pdf"),
    "mbec-2023":   find(J, "2022 LiXue PNI.pdf"),
    "cvpr-2016":   find(C, "2016 CVPR Hou_Patch-Based_Convolutional_Neural.pdf"),
    "fonc-2022":   find(J, "2022 Frontier oncology*.pdf"),
    # radiomics
    "cancerimg-2024": find(J, "2024 Deng-Cancer_Imaging*.pdf"),
    "tc-2023":     find(J, "2023 钦铸*.pdf"),
    "jitc-2023":   find(J, "2023 Xia Assessing*.pdf"),
    "ejro-2025":   find(J, "2025 汕大*.pdf"),
    "phenomics-2026": find(J, "2026-牟天-PET和谐化.pdf"),
    # registration
    "ijist-2024":  find(J, "2024 HuangZengan - Enhanced Deformation*.pdf"),
    "tip-2012":    find(J, "2012 polyaffine.pdf"),
    "siamsims-2015": find(J, "2015 kalmanAtlas.pdf"),
    # segmentation
    "media-2012-seg": find(J, "2012 rss.pdf"),
    "jvcir-2025":  find(J, "2025 田木 AttenScribble.pdf"),
    "cbm-2022":    find(J, "2022 zhangsai- deep equilibrium model.pdf"),
    "bspc-2026":   find(J, "2026 黄增安 A multi-task*.pdf"),
    "imic-2014":   find(C, "zhu-miccai2014*.pdf"),
    # shape
    "hbm-2014":    find(J, "2015 hbm22525.pdf"),
    "mediasc-2015": find(J, "2015 hong_depthShapeAnalysis.pdf"),
    "siamsims-2014": find(J, "2014 Tammy SIAM*.pdf"),
    # synthesis
    "ijist-2025":  find(J, "2024 黄增安 Synthesizing*.pdf"),
    "spie-2017-syn": find(C, "2016 Zhou SPIE Evaluation of nucleus segmentation*.pdf"),
    # spine
    "isbi-2024":   find(C, "2024-ISBI-Combing_3D*.pdf"),
    "umb-2024":    find(J, "2024-HeWeizhen-3D US.pdf"),
}

ok, fail = [], []
for cid, pdf in sorted(M.items()):
    out_jpg = os.path.join(AREAS, cid + ".jpg")
    try:
        with tempfile.TemporaryDirectory() as td:
            prefix = os.path.join(td, "p")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120",
                 "-f", "1", "-l", "1", "-singlefile", pdf, prefix],
                check=True, capture_output=True)
            png = prefix + ".png"
            if not (os.path.exists(png) and os.path.getsize(png) > 10000):
                fail.append((cid, "png missing or tiny"))
                continue
            im = Image.open(png)
            if im.mode in ("RGBA", "P", "LA"):
                im = im.convert("RGB")
            im.save(out_jpg, "JPEG", quality=85, optimize=True)
        sz = os.path.getsize(out_jpg)
        if sz > 10000:
            ok.append((cid, sz))
        else:
            fail.append((cid, "jpg too small"))
    except Exception as e:
        fail.append((cid, str(e)[:120]))

print("OK (%d):" % len(ok))
for cid, sz in ok:
    print("  %s  %.0f KB" % (cid, sz / 1024))
print("FAIL (%d):" % len(fail))
for cid, err in fail:
    print("  %s  %s" % (cid, err))
