import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system import *

BASE = "https://github.com/BinaryLoops"

PANELS = [
    ("00-hero.svg", "BINARYLOOPS — building systems that think"),
    ("01-readout.svg", "System readout"),
    ("02-stack-matrix.svg", "Language stack matrix"),
    ("03-layers.svg", "System layers"),
]
FEATURED_PANELS = [
    ("SmartChennai", "04-smartchennai.svg"),
    ("Document-AI", "05-document-ai.svg"),
    ("PocketMate", "06-pocketmate.svg"),
    ("GroceryAppDSA", "07-groceryappdsa.svg"),
]


def img(src, alt, link=None):
    tag = f'  <img src="./assets/{src}" width="900" alt="{alt}"/>'
    if link:
        return f'<div align="center">\n  <a href="{link}">\n  {tag}\n  </a>\n</div>'
    return f'<div align="center">\n{tag}\n</div>'


def build():
    counts = lang_counts()
    projects = [r for r in REPOS if r["kind"] == "project"]
    placeholder = [r for r in REPOS if r["kind"] == "placeholder"]
    profile = [r for r in REPOS if r["kind"] == "profile"]

    out = []
    out.append("<!-- BINARYLOOPS // ENGINEERING OPERATING SYSTEM\n"
               "     This file is generated. Edit data/repositories.json, then run\n"
               "     python3 gen/build_all.py — it rebuilds every panel and this README\n"
               "     from the same source and fails if anything is inconsistent. -->\n")

    for src, alt in PANELS[:1]:
        out.append(img(src, alt))
    out.append("")
    out.append(img(PANELS[1][0], PANELS[1][1]))
    out.append("")
    out.append(img(PANELS[2][0], PANELS[2][1]))
    out.append("")
    out.append(img(PANELS[3][0], PANELS[3][1]))
    out.append("")

    for name, src in FEATURED_PANELS:
        r = next(x for x in REPOS if x["name"] == name)
        out.append(img(src, f'{r["name"]} — {r["title"].lower()}', f"{BASE}/{name}"))
        out.append("")

    out.append(img("08-topology.svg", "Repository topology"))
    out.append("")

    # ── index, generated straight from the dataset
    out.append("<!-- index generated from data/repositories.json -->")
    out.append("")
    out.append("| # | Repository | Region | Language | System |")
    out.append("| --- | --- | --- | --- | --- |")
    for i, r in enumerate(projects, 1):
        star = " ●" if r["featured"] else ""
        out.append(f'| `{i:02d}` | [{r["name"]}]({BASE}/{r["name"]}){star} | '
                   f'{r["region"]} | {r["lang"]} | {r["desc"]} |')
    out.append("")
    out.append("`●` marks the four featured systems above.")
    out.append("")

    notes = []
    for r in placeholder:
        notes.append(f'[`{r["name"]}`]({BASE}/{r["name"]}) is a reserved namespace with '
                     f'no code committed, so it is not listed as a project.')
    for r in profile:
        notes.append(f'[`{r["name"]}`]({BASE}/{r["name"]}) is this profile repository — '
                     f'it holds the README and the generated artwork, not a project.')
    out.append("  \n".join(notes))
    out.append("")

    out.append("<details>")
    out.append("<summary><strong>How this page is built</strong></summary>")
    out.append("")
    out.append(f"Every figure comes from `data/repositories.json`: "
               f"{OWNER['public_repos']} public repositories, {len(CODED)} carrying "
               f"committed code, across {len(counts)} primary languages "
               f"({', '.join(f'{k} ×{v}' for k, v in counts.items())}). "
               f"Nothing is estimated, inferred or padded — where a repository has no "
               f"content, the artwork draws it hollow rather than dressing it up.")
    out.append("")
    out.append("```bash")
    out.append("python3 gen/build_all.py     # rebuild every panel and this README")
    out.append("```")
    out.append("")
    out.append("`build_all.py` runs a verification gate that fails the build if an asset "
               "referenced here is missing, if an asset on disk is orphaned, if a "
               "repository link points at a name absent from the dataset, if the index "
               "disagrees with the dataset, or if any label has drifted outside its "
               "canvas. The panels are static SVG — no animation, so they render "
               "identically everywhere GitHub serves them.")
    out.append("")
    out.append("</details>")
    out.append("")
    out.append(img("09-footer.svg", "End of transmission"))
    out.append("")

    path = os.path.join(ROOT, "README.md")
    with open(path, "w") as f:
        f.write("\n".join(out))
    return path


if __name__ == "__main__":
    print("built", build())
