import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system import *


def topology():
    w, h = W, 580
    s = head(w, h, "BinaryLoops — repository topology")
    s += chrome(w, h, "08", "TOPOLOGY", "10 REPOSITORIES · 4 REGIONS · 4 LANGUAGES")

    # ── region plates: left column faces the spine from the right,
    #    right column faces it from the left.
    plates = {
        "AI":      dict(x=40,  y=92,  w=380, h=196, side=-1),
        "DATA":    dict(x=480, y=92,  w=380, h=196, side=1),
        "WEB":     dict(x=40,  y=322, w=380, h=154, side=-1),
        "SYSTEMS": dict(x=480, y=322, w=380, h=196, side=1),
    }
    assert max(p["y"] + p["h"] for p in plates.values()) <= h - 60, "plates overrun"

    node_pos = {}
    plate_boxes = []
    body = []

    for region, p in plates.items():
        col = REGION_COLOR[region]
        px, py, pw, ph, side = p["x"], p["y"], p["w"], p["h"], p["side"]
        plate_boxes.append((region, px, py, pw, ph))

        # depth: recessed plate with an offset ground shadow
        body.append(f'<rect x="{px+7}" y="{py+7}" width="{pw}" height="{ph}" '
                    f'fill="{PANEL}" opacity=".5"/>')
        body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{PANEL2}" '
                    f'stroke="{RULE2}"/>')
        body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="22" fill="{col}" '
                    f'opacity=".13"/>')
        # region corner tick facing the spine
        ex = px + pw if side < 0 else px
        body.append(f'<rect x="{ex - (4 if side<0 else 0)}" y="{py}" width="4" '
                    f'height="{ph}" fill="{col}" opacity=".55"/>')

        fits(region, 10, 160, 2.6, "topo/region")
        body.append(T(px + 16, py + 15, region, 10, col, spacing=2.6, weight=700))
        body.append(T(px + pw - 16, py + 15, DB["regions"][region].lower(), 8.5,
                      DEEP, anchor="end", spacing=1.0))

        mem = sorted([r for r in REPOS if r["region"] == region],
                     key=lambda r: (not r["featured"], r["kind"] != "project", r["name"]))

        # nodes hug the spine-facing edge; labels always read outward
        nx = px + pw - 42 if side < 0 else px + 42
        label_x = nx - 26 if side < 0 else nx + 26
        anchor = "end" if side < 0 else "start"
        avail = (label_x - (px + 16)) if side < 0 else (px + pw - 16 - label_x)

        yy = py + 54
        for repo in mem:
            feat = repo["featured"]
            r = 15 if feat else 8
            live = repo["kind"] == "project"
            lc = LANG.get(repo["lang"], DEEP)

            body.append(f'<circle cx="{nx}" cy="{yy}" r="{r}" fill="{INK}" '
                        f'stroke="{col}" stroke-width="{2 if feat else 1.2}" '
                        f'opacity="{1 if live else .55}"/>')
            if live:
                body.append(f'<circle cx="{nx}" cy="{yy}" r="{r-5 if feat else 3.4}" '
                            f'fill="{lc}"/>')
            else:
                body.append(f'<path d="M{nx-4} {yy} H{nx+4}" stroke="{col}" '
                            f'stroke-width="1.4" opacity=".7"/>')

            fits(repo["name"], 11 if feat else 9.5, avail, 0.4, f"topo/{repo['name']}")
            body.append(T(label_x, yy + (0 if feat else 3.5), repo["name"],
                          11 if feat else 9.5, BONE if live else DEEP,
                          anchor=anchor, spacing=0.4, weight=700 if feat else 400))
            if feat:
                sub = f'{repo["title"]} · {repo["lang"]}'
                fits(sub, 8, avail, 1.2, "topo/sub")
                body.append(T(label_x, yy + 15, sub, 8, col, anchor=anchor, spacing=1.2))
            elif repo["lang"]:
                pass

            node_pos[repo["name"]] = (nx, yy, side)
            yy += 50 if feat else 38
        assert yy - 38 <= py + ph - 12, f"[topo/{region}] nodes overrun the plate"

    no_overlap(plate_boxes, "topo/plates")
    inside(plate_boxes, w, h, "topo/plates")

    # ── language buses in the central gutter: the meaningful connections
    counts = lang_counts()
    shared = [l for l, n in counts.items() if n > 1]
    bus_x = {l: 438 + i * 16 for i, l in enumerate(shared)}
    edges = []
    for lang in shared:
        bx = bus_x[lang]
        members = [r for r in REPOS if r["lang"] == lang]
        ys = [node_pos[r["name"]][1] for r in members]
        col = LANG[lang]
        edges.append(f'<path d="M{bx} {min(ys)-18} V{max(ys)}" stroke="{col}" '
                     f'stroke-width="1.4" opacity=".85"/>')
        for r in members:
            nxp, nyp, side = node_pos[r["name"]]
            edge_x = nxp + (15 if r["featured"] else 8) * (1 if side < 0 else -1)
            edges.append(f'<path d="M{edge_x} {nyp} H{bx}" stroke="{col}" '
                         f'stroke-width="1.1" opacity=".55"/>')
            edges.append(f'<circle cx="{bx}" cy="{nyp}" r="2.6" fill="{col}"/>')
        # bus tag, set vertically in the gutter below the bus
        tag_len = tw(lang, 8, 1.4)
        tag_y = max(ys) + 18 + tag_len
        edges.append(f'<g transform="translate({bx-4},{tag_y:.0f}) rotate(-90)">'
                     f'<text x="0" y="0" font-family="{MONO}" font-size="8" '
                     f'letter-spacing="1.4" fill="{col}">{esc(lang.upper())}</text></g>')
        assert tag_y < h - 58, f"[topo] {lang} bus tag overruns the footer"
    assert max(bus_x.values()) < 480, "[topo] buses stray out of the gutter"

    s += "".join(body) + "".join(edges) + "\n"

    # ── annotations
    s += T(40, h - 62, "vertical buses connect repositories that share a primary "
           "language · hollow node = profile or reserved", 8.5, STEEL, spacing=1.0)
    lx = 40
    for lang in shared:
        s += f'<rect x="{lx}" y="{h-86}" width="10" height="10" fill="{LANG[lang]}"/>'
        s += T(lx + 16, h - 77, f"{lang} x{counts[lang]}", 8.5, DEEP, spacing=1.0)
        lx += tw(f"{lang} x{counts[lang]}", 8.5, 1.0) + 40
    assert lx < w - 260, "[topo] legend runs into the right margin"
    s += T(w - 40, h - 77, "large node = featured system", 8.5, DEEP,
           anchor="end", spacing=1.0)

    s += status(w, h, "SECTION 08 / 09  ▸  TOPOLOGY", "THE ARCHITECTURE OF THE WORK")
    return write("08-topology.svg", s)


if __name__ == "__main__":
    print("built", topology())
