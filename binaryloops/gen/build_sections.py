import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system import *


# ═══════════════════════════════════════════ 01 · TERMINAL
def terminal():
    w, h = W, 330
    counts = lang_counts()
    reserved = len([r for r in REPOS if r["kind"] == "placeholder"])

    lines = [
        ("whoami",  f"{OWNER['name'].lower()} — {OWNER['login'].lower()}"),
        ("system",  f"{OWNER['public_repos']} repositories · "
                    f"{len(DB['regions'])} regions · {len(counts)} languages"),
        ("status",  f"{len(CODED)} with code · {reserved} reserved · 1 profile surface"),
        ("build",   " · ".join(f"{k.lower()} x{v}" for k, v in counts.items())),
    ]

    s = head(w, h, "BinaryLoops — system readout")
    s += chrome(w, h, "01", "READOUT", "LIVE FROM repositories.json")

    # ── terminal block
    tx, ty, tw_, th = 40, 84, 520, 196
    s += f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" fill="{PANEL}" stroke="{RULE2}"/>\n'
    s += f'<path d="M{tx} {ty+24} H{tx+tw_}" stroke="{RULE2}" stroke-width="1"/>\n'
    for i, c in enumerate((TEAL, VIOLET, AMBER)):
        s += f'<circle cx="{tx+16+i*13}" cy="{ty+12}" r="3.2" fill="{c}" opacity=".8"/>\n'
    s += T(tx + 62, ty + 16, "binaryloops // core", 9, STEEL, spacing=1.4)

    y = ty + 48
    for cmd, out in lines:
        s += T(tx + 18, y, "$", 11, TEAL, spacing=0, weight=700)
        fits(cmd, 11, 180, 1.4, "term/cmd")
        s += T(tx + 34, y, cmd, 11, BONE, spacing=1.4, weight=700)
        fits(out, 9.5, tw_ - 56, 0.4, "term/out")
        s += T(tx + 34, y + 18, out, 9.5, TEXT, spacing=0.4)
        s += f'<path d="M{tx+18} {y+24} H{tx+26}" stroke="{DEEP}" stroke-width="1"/>\n'
        y += 34
    s += T(tx + 18, y, "$", 11, TEAL, spacing=0, weight=700)
    s += f'<rect x="{tx+34}" y="{y-9}" width="8" height="12" fill="{TEAL}" opacity=".8"/>\n'
    assert y + 6 < ty + th, "[terminal] output overruns the block"

    # ── region map, right
    rx, ry = 594, 84
    s += T(rx, ry + 12, "REGIONS", 9.5, DEEP, spacing=2.6, weight=700)
    yy = ry + 34
    boxes = []
    for reg, col in REGION_COLOR.items():
        mem = [r for r in REPOS if r["region"] == reg]
        boxes.append((reg, rx, yy - 12, 266, 40))
        s += f'<path d="M{rx} {yy+18} H{rx+266}" stroke="{RULE}" stroke-width="1"/>\n'
        s += f'<rect x="{rx}" y="{yy-10}" width="3" height="20" fill="{col}"/>\n'
        s += T(rx + 14, yy + 4, reg, 10, col, spacing=2.2, weight=700)
        # one dot per repository in the region
        dx = rx + 266
        for j, repo in enumerate(mem):
            cxx = dx - j * 15
            r = 5 if repo["featured"] else 3.2
            fill = col if repo["kind"] == "project" else "none"
            s += (f'<circle cx="{cxx}" cy="{yy}" r="{r}" fill="{fill}" stroke="{col}" '
                  f'stroke-width="1" opacity="{".95" if repo["kind"]=="project" else ".5"}"/>\n')
        assert dx - (len(mem) - 1) * 15 > rx + 90, f"[terminal] {reg} dots reach the label"
        yy += 42
    no_overlap(boxes, "terminal/regions")
    s += T(rx, yy + 4, "hollow = profile or reserved", 8.5, DEEP, spacing=1.2)

    s += status(w, h, "SECTION 01 / 09  ▸  READOUT", "NO INFERRED STATISTICS")
    return write("01-readout.svg", s)


# ═══════════════════════════════════════════ 02 · STACK MATRIX
def matrix():
    counts = lang_counts()
    langs = list(counts.keys())
    cols = CODED
    cell, gap = 52, 10
    grid_w = len(cols) * cell + (len(cols) - 1) * gap
    left = 196
    head_h = 214
    grid_h = len(langs) * cell + (len(langs) - 1) * gap
    w, h = W, head_h + grid_h + 76
    assert left + grid_w + 130 <= w - 20, "matrix grid too wide"

    s = head(w, h, "BinaryLoops — language stack matrix")
    s += chrome(w, h, "02", "STACK MATRIX", "PRIMARY LANGUAGE PER REPOSITORY")

    for c, repo in enumerate(cols):
        x = left + c * (cell + gap) + cell * 0.62
        fs = 8.5
        length = tw(repo["name"], fs, 0.3)
        assert length * math.sin(math.radians(60)) < head_h - 78, \
            f"[matrix] header {repo['name']} too tall"
        s += (f'<g transform="translate({x:.1f},{head_h-12}) rotate(-60)">'
              f'<text x="0" y="0" font-family="{MONO}" font-size="{fs}" letter-spacing=".3" '
              f'fill="{BONE if repo["featured"] else STEEL}" '
              f'font-weight="{700 if repo["featured"] else 400}">'
              f'{esc(repo["name"])}</text></g>\n')
        if repo["featured"]:
            s += (f'<path d="M{left + c*(cell+gap)} {head_h-6} h{cell}" '
                  f'stroke="{TEAL}" stroke-width="1.5"/>\n')

    for r, lang in enumerate(langs):
        y = head_h + r * (cell + gap)
        col = LANG.get(lang, TEAL)
        fits(lang, 10.5, left - 70, 0.8, "matrix/row")
        s += T(left - 30, y + cell / 2 + 4, lang, 10.5, BONE, anchor="end", spacing=0.8)
        s += f'<rect x="{left-20}" y="{y+cell/2-5}" width="10" height="10" fill="{col}"/>\n'

        for c, repo in enumerate(cols):
            x = left + c * (cell + gap)
            on = repo["lang"] == lang
            s += (f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                  f'fill="{col if on else PANEL}" fill-opacity="{".9" if on else "1"}" '
                  f'stroke="{col if on else RULE2}"/>\n')
            if on:
                s += (f'<path d="M{x+16} {y+cell/2+1} l7 8 l13 -17" fill="none" '
                      f'stroke="{INK}" stroke-width="2.6" stroke-linecap="round" '
                      f'stroke-linejoin="round"/>\n')
            else:
                s += (f'<circle cx="{x+cell/2}" cy="{y+cell/2}" r="1.6" fill="{RULE2}"/>\n')

        tx = left + grid_w + 26
        n = counts[lang]
        bar = n / max(counts.values()) * 74
        s += (f'<rect x="{tx}" y="{y+cell/2-6}" width="{bar:.1f}" height="12" '
              f'fill="{col}" opacity=".75"/>\n')
        s += T(tx + 86, y + cell / 2 + 5, f"{n}", 13, BONE, spacing=0, weight=700)
        assert tx + 96 <= w - 40, "[matrix] totals overflow"

    s += T(left, h - 58, f"{len(cols)} repositories carry committed code · "
           f"{len(langs)} primary languages", 9, STEEL, spacing=1.2)
    s += status(w, h, "SECTION 02 / 09  ▸  STACK MATRIX",
                "LANGUAGE AS REPORTED BY GITHUB")
    return write("02-stack-matrix.svg", s)


# ═══════════════════════════════════════════ 03 · ARCHITECTURE
def architecture():
    w, h = W, 430
    layers = [
        ("INTERFACE", "WEB",     TEAL,   "operator consoles"),
        ("INTELLIGENCE", "AI",   VIOLET, "extraction and scoring"),
        ("PERSISTENCE", "DATA",  AMBER,  "schemas and records"),
        ("RUNTIME", "SYSTEMS",   MINT,   "structures and monitoring"),
    ]
    s = head(w, h, "BinaryLoops — system layers")
    s += chrome(w, h, "03", "LAYERS", "EVERY REPOSITORY PLACED ON ITS LAYER")

    top, lh, gap, skew = 88, 66, 14, 30
    base_x, base_w = 60, 700
    boxes = []
    for i, (name, region, col, note) in enumerate(layers):
        y = top + i * (lh + gap)
        x = base_x + (len(layers) - 1 - i) * skew
        boxes.append((name, x, y, base_w, lh))

        # depth: a shadow plate offset behind each slab
        s += (f'<rect x="{x-8}" y="{y+8}" width="{base_w}" height="{lh}" '
              f'fill="{PANEL}" opacity=".55"/>\n')
        s += (f'<rect x="{x}" y="{y}" width="{base_w}" height="{lh}" fill="{PANEL2}" '
              f'stroke="{RULE2}"/>\n')
        s += f'<rect x="{x}" y="{y}" width="4" height="{lh}" fill="{col}"/>\n'

        fits(name, 12, 190, 2.6, "arch/name")
        s += T(x + 20, y + 28, name, 12, col, spacing=2.6, weight=700)
        s += T(x + 20, y + 46, note, 8.5, DEEP, spacing=1.2)

        # repositories that live on this layer
        mem = [r for r in REPOS if r["region"] == region]
        chip_x = x + base_w - 18
        chips = []
        for repo in reversed(mem):
            fs = 9
            cw = tw(repo["name"], fs, 0.4) + 24
            cxx = chip_x - cw
            chips.append((repo["name"], cxx, y + 20, cw, 26))
            solid = repo["kind"] == "project"
            s += (f'<rect x="{cxx:.1f}" y="{y+20}" width="{cw:.1f}" height="26" '
                  f'fill="{PANEL}" stroke="{col}" stroke-opacity="{".7" if solid else ".3"}" '
                  f'stroke-dasharray="{"none" if solid else "3 3"}"/>\n')
            if repo["featured"]:
                s += f'<rect x="{cxx:.1f}" y="{y+20}" width="3" height="26" fill="{col}"/>\n'
            s += T(cxx + 12, y + 37, repo["name"], fs,
                   BONE if solid else DEEP, spacing=0.4)
            chip_x = cxx - 10
        no_overlap(chips, f"arch/chips/{name}")
        assert chip_x > x + 230, f"[arch/{name}] chips collide with the layer label"

        # signal path down to the next layer
        if i < len(layers) - 1:
            nx = x - skew
            s += (f'<path d="M{x+140} {y+lh} L{x+140} {y+lh+gap/2} '
                  f'L{nx+140} {y+lh+gap/2} L{nx+140} {y+lh+gap}" fill="none" '
                  f'stroke="{col}" stroke-width="1.2" opacity=".7"/>\n')
            s += f'<circle cx="{nx+140}" cy="{y+lh+gap}" r="2.6" fill="{col}"/>\n'
    no_overlap(boxes, "arch/layers")
    inside(boxes, w, h, "arch/layers")

    s += T(60, h - 58, "signal descends interface → intelligence → persistence → runtime",
           9, STEEL, spacing=1.2)
    s += status(w, h, "SECTION 03 / 09  ▸  LAYERS",
                "LAYER ASSIGNMENT FROM repositories.json")
    return write("03-layers.svg", s)


# ═══════════════════════════════════════════ 09 · FOOTER
def footer():
    w, h = W, 210
    s = head(w, h, "BinaryLoops — end of transmission")
    s += f'<rect width="{w}" height="{h}" fill="{INK}"/>\n'
    s += tech_grid(w, h)
    s += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{RULE2}"/>\n'
    s += registration(w, h)

    # cropped wordmark bleeding off the bottom edge
    s += outline_T(-120, h + 34, "BINARYLOOPS", 172, RULE2, spacing=-3, sw=1.3,
                   op=".75", crop=True)

    s += ruler(40, 58, w - 80)
    s += T(40, 44, "BINARYLOOPS", 11, BONE, spacing=3.4, weight=700)
    s += T(40 + tw("BINARYLOOPS", 11, 3.4) + 10, 44, "// 09 END OF TRANSMISSION",
           11, TEAL, spacing=3.4, weight=700)
    s += T(w - 40, 44, "github.com/BinaryLoops", 9, STEEL, anchor="end", spacing=1.6)

    s += T(40, 96, "BUILDING SYSTEMS THAT THINK.", 15, BONE, spacing=6, weight=700)
    s += T(40, 122, "artwork generated from repositories.json — no figure on this "
           "page is estimated", 9, STEEL, spacing=1.0)
    s += f'<path d="M40 {h-40} H{w-40}" stroke="{RULE2}" stroke-width="1"/>\n'
    s += status(w, h, "SECTION 09 / 09  ▸  END", "STATIC SVG · NO ANIMATION")
    return write("09-footer.svg", s)


if __name__ == "__main__":
    for fn in (terminal, matrix, architecture, footer):
        print("built", fn())
