import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system import *


def rot_pt(rx, ry, ang, rot, cx, cy):
    x, y = rx * math.cos(ang), ry * math.sin(ang)
    c, s = math.cos(rot), math.sin(rot)
    return cx + x * c - y * s, cy + x * s + y * c


def hero():
    w, h = W, 520
    cx, cy = 620, 200
    rot = math.radians(-16)

    s = head(w, h, "BINARYLOOPS — building systems that think")
    s += f'<defs><clipPath id="corefield">' \
         f'<rect x="20" y="66" width="860" height="216"/></clipPath></defs>\n'

    s += chrome(w, h, "00", "CORE", "AYUSH · BUILDING SYSTEMS THAT THINK", ghost=False)

    # ── background layer: cropped ghost wordmark
    s += outline_T(-150, 150, "BINARYLOOPS", 186, RULE2, spacing=-4, sw=1.4, op=".5",
                   crop=True)

    # ── background layer: perspective spokes radiating from the core
    spokes = []
    for i in range(36):
        a = math.radians(i * 10)
        x2, y2 = cx + 430 * math.cos(a), cy + 430 * math.sin(a)
        spokes.append(f'<path d="M{cx + 120*math.cos(a):.1f} {cy + 120*math.sin(a):.1f} '
                      f'L{x2:.1f} {y2:.1f}"/>')
    s += (f'<g clip-path="url(#corefield)" stroke="{RULE2}" stroke-width=".7" '
          f'opacity=".55">{"".join(spokes)}</g>\n')
    s += (f'<g clip-path="url(#corefield)" fill="none" stroke="{RULE2}" opacity=".7">'
          f'<circle cx="{cx}" cy="{cy}" r="172" stroke-width=".7"/>'
          f'<circle cx="{cx}" cy="{cy}" r="240" stroke-width=".7"/></g>\n')

    # ── midground: orbital geometry
    orbits = [(214, 63), (163, 48), (114, 34)]
    for rx, ry in orbits:
        s += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
              f'stroke="{RULE2}" stroke-width="1.1" '
              f'transform="rotate(-16 {cx} {cy})"/>\n')

    # repositories with code, distributed across the three orbits
    rings = [CODED[0:3], CODED[3:6], CODED[6:8]]
    nodes = []
    for (rx, ry), members, phase in zip(orbits, rings, (0.25, 1.15, 2.4)):
        for k, repo in enumerate(members):
            a = phase + 2 * math.pi * k / max(len(members), 1)
            nx, ny = rot_pt(rx, ry, a, rot, cx, cy)
            col = REGION_COLOR[repo["region"]]
            r = 7 if repo["featured"] else 4.2
            nodes.append((nx, ny, r, col, repo))
    for nx, ny, r, col, repo in nodes:
        s += f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{r}" fill="{col}"/>\n'
        if repo["featured"]:
            s += (f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{r+6}" fill="none" '
                  f'stroke="{col}" stroke-width="1" opacity=".55"/>\n')

    # dial ticks around the core
    ticks = []
    for i in range(48):
        a = math.radians(i * 7.5)
        r1 = 78 if i % 4 else 72
        ticks.append(f'<path d="M{cx + r1*math.cos(a):.1f} {cy + r1*math.sin(a):.1f} '
                     f'L{cx + 86*math.cos(a):.1f} {cy + 86*math.sin(a):.1f}"/>')
    s += f'<g stroke="{DEEP}" stroke-width="1">{"".join(ticks)}</g>\n'

    # ── foreground: the core itself
    s += (f'<circle cx="{cx}" cy="{cy}" r="62" fill="{PANEL2}" stroke="{RULE2}"/>\n'
          f'<circle cx="{cx}" cy="{cy}" r="42" fill="none" stroke="{TEAL}" '
          f'stroke-width="1.3" opacity=".9"/>\n'
          f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{TEAL}" '
          f'stroke-width=".9" opacity=".5"/>\n'
          f'<circle cx="{cx}" cy="{cy}" r="11" fill="{TEAL}"/>\n')
    s += (f'<g stroke="{TEAL}" stroke-width=".9" opacity=".45">'
          f'<path d="M{cx-92} {cy} H{cx-70}"/><path d="M{cx+70} {cy} H{cx+92}"/>'
          f'<path d="M{cx} {cy-92} V{cy-70}"/>'
          f'<path d="M{cx} {cy+70} V{cy+92}"/></g>\n')

    # ── spec block, top right
    specs = [("OPERATOR", OWNER["name"]),
             ("REPOSITORIES", str(OWNER["public_repos"])),
             ("LANGUAGES", str(len(lang_counts())))]
    sy = 92
    for k, v in specs:
        line = f"{k}  {v}"
        fits(line, 9.5, 220, 1.6, "hero/spec")
        s += T(w - 40, sy, k, 9.5, DEEP, anchor="end", spacing=1.6)
        s += T(w - 40 - tw(k, 9.5, 1.6) - 14, sy, v, 9.5, TEXT, anchor="end", spacing=1.6)
        sy += 18

    # ── region bus
    by = 284
    s += f'<path d="M40 {by} H820" stroke="{RULE2}" stroke-width="1.2"/>\n'
    s += f'<path d="M{cx} {cy+62} V{by}" stroke="{TEAL}" stroke-width="1.2" opacity=".6"/>\n'
    s += f'<circle cx="{cx}" cy="{by}" r="3.5" fill="{TEAL}"/>\n'

    counts = {}
    for r in REPOS:
        counts[r["region"]] = counts.get(r["region"], 0) + 1
    boxes = []
    bw, bh = 150, 36
    for i, (reg, col) in enumerate(REGION_COLOR.items()):
        bx = 40 + i * 210
        boxes.append((reg, bx, 292, bw, bh))
        s += f'<path d="M{bx+bw/2} {by} V292" stroke="{RULE2}" stroke-width="1"/>\n'
        s += (f'<rect x="{bx}" y="292" width="{bw}" height="{bh}" fill="{PANEL}" '
              f'stroke="{RULE2}"/>\n')
        s += f'<rect x="{bx}" y="292" width="3" height="{bh}" fill="{col}"/>\n'
        fits(reg, 10, 92, 2.2, "hero/region")
        s += T(bx + 14, 315, reg, 10, col, spacing=2.2, weight=700)
        s += T(bx + bw - 12, 315, str(counts[reg]), 13, TEXT,
               anchor="end", spacing=0, weight=700)
    no_overlap(boxes, "hero/regions")
    inside(boxes, w, h, "hero/regions")

    # ── foreground: the wordmark
    mark, msize, msp = "BINARYLOOPS", 112, -1.5
    mwidth = fits(mark, msize, w - 90, msp, "hero/wordmark")
    base = 415
    assert base - msize * 0.74 > 292 + bh, "[hero] wordmark collides with the region bus"
    s += outline_T(40 + 5, base + 5, mark, msize, TEAL, spacing=msp, sw=1.1, op=".38")
    s += T(40, base, mark, msize, BONE, spacing=msp, weight=700)

    tag = "BUILDING SYSTEMS THAT THINK."
    fits(tag, 19, w - 90, 8, "hero/tagline")
    s += T(42, 450, tag, 19, TEAL, spacing=8, weight=400)
    s += f'<path d="M40 {base+18} H{40+mwidth:.0f}" stroke="{RULE2}" stroke-width="1"/>\n'

    s += status(w, h, "SECTION 00 / 09  ▸  CORE",
                f"{len(CODED)} REPOSITORIES WITH CODE  ·  {OWNER['public_repos']} PUBLIC")
    return write("00-hero.svg", s)


if __name__ == "__main__":
    print("built", hero())
