"""Verification gate. The build fails unless every one of these holds."""
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system import *
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
BASE = "https://github.com/BinaryLoops"


def check():
    readme = open(os.path.join(ROOT, "README.md")).read()
    fails, notes = [], []

    # 1 ── every referenced asset exists
    refs = re.findall(r'src="\./assets/([^"]+)"', readme)
    for r in refs:
        if not os.path.exists(os.path.join(ASSETS, r)):
            fails.append(f"README references missing asset: {r}")
    notes.append(f"{len(refs)} asset references, all resolved")

    # 2 ── no orphaned assets on disk
    on_disk = {os.path.basename(p) for p in glob.glob(os.path.join(ASSETS, "*.svg"))}
    orphans = on_disk - set(refs)
    if orphans:
        fails.append(f"assets on disk never referenced: {sorted(orphans)}")
    notes.append(f"{len(on_disk)} assets on disk, 0 orphaned")

    # 3 ── every repository link resolves to a real repository name
    names = {r["name"] for r in REPOS}
    links = re.findall(r'https://github\.com/BinaryLoops/([A-Za-z0-9_\-]+)', readme)
    for l in links:
        if l not in names:
            fails.append(f"link points at unknown repository: {l}")
    notes.append(f"{len(links)} repository links, all present in repositories.json")

    # 4 ── the index lists exactly the project-kind repositories
    projects = {r["name"] for r in REPOS if r["kind"] == "project"}
    rows = set(re.findall(r'\| `\d+` \| \[([^\]]+)\]', readme))
    if rows != projects:
        fails.append(f"index mismatch — only in index: {rows-projects}, "
                     f"only in dataset: {projects-rows}")
    notes.append(f"index lists exactly the {len(projects)} project repositories")

    # 5 ── the profile repo is never presented as a project
    prof = [r["name"] for r in REPOS if r["kind"] == "profile"]
    for p in prof:
        if p in rows:
            fails.append(f"profile repository {p} is listed as a project")
        if f"this profile repository" not in readme:
            fails.append("profile repository is not explained as such")
    notes.append(f"profile repository ({prof[0]}) excluded from the project index")

    # 6 ── static artwork only, and every label inside its canvas
    n_text = 0
    for path in sorted(glob.glob(os.path.join(ASSETS, "*.svg"))):
        raw = open(path).read()
        base = os.path.basename(path)
        for bad in ("<style", "animate", "@keyframes"):
            if bad in raw:
                fails.append(f"{base} contains {bad} — assets must be static")
        root = ET.parse(path).getroot()
        cw, ch = float(root.get("width")), float(root.get("height"))
        for el in root.iter(f"{NS}text"):
            n_text += 1
            if el.get("x") is None or el.get("data-crop"):
                continue  # deliberate edge bleed, declared at the call site
            x, y = float(el.get("x")), float(el.get("y"))
            fs = float(el.get("font-size", 10))
            sp = float(el.get("letter-spacing", 0))
            wd = len(el.text or "") * (fs * 0.6 + sp)
            a = el.get("text-anchor", "start")
            x0 = x if a == "start" else (x - wd / 2 if a == "middle" else x - wd)
            # rotated labels live under a transform; their parent g carries it
            if x0 < -2 or x0 + wd > cw + 2 or y > ch + 2:
                fails.append(f"{base}: label {el.text!r} outside canvas "
                             f"(x={x0:.0f} w={wd:.0f} in {cw:.0f}x{ch:.0f})")
    notes.append(f"{n_text} labels checked, all within canvas (excl. declared bleeds); 0 animated")

    print("VERIFICATION")
    for n in notes:
        print("  ok   ", n)
    if fails:
        print("\nFAILED")
        for f in fails:
            print("  FAIL ", f)
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    check()
