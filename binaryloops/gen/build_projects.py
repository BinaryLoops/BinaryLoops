import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system import *

H = 340
PW, PH = 530, 192
PY = 88


def repo(name):
    return next(r for r in REPOS if r["name"] == name)


def wrap(text, size, box_w):
    per = max(int(box_w // (size * 0.6 + 0.4)), 12)
    out, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if len(t) <= per:
            cur = t
        else:
            out.append(cur); cur = wd
    if cur:
        out.append(cur)
    return out


def spec(x, r, col, width=260):
    """Identification column. Same information every time, so the eye always
    knows where to look — the artwork beside it is what changes."""
    s = T(x, PY + 14, r["title"], 9.5, col, spacing=2.4, weight=700)
    fits(r["title"], 9.5, width, 2.4, "spec/title")
    size = 26 if tw(r["name"], 26, 0.5) <= width else 20
    fits(r["name"], size, width, 0.5, "spec/name")
    s += T(x, PY + 52, r["name"], size, BONE, spacing=0.5, weight=700)
    s += f'<path d="M{x} {PY+64} H{x+52}" stroke="{col}" stroke-width="2.5"/>\n'

    y = PY + 90
    for line in wrap(r["role"], 9.5, width):
        s += T(x, y, line, 9.5, TEXT, spacing=0.4)
        y += 16
    assert y < PY + 150, "[spec] role text runs into the language chip"

    lc = LANG.get(r["lang"], col)
    cw = tw(r["lang"], 9.5, 0.6) + 34
    s += (f'<rect x="{x}" y="{PY+156}" width="{cw:.1f}" height="26" fill="{PANEL}" '
          f'stroke="{RULE2}"/>\n')
    s += f'<rect x="{x}" y="{PY+156}" width="10" height="26" fill="{lc}"/>\n'
    s += T(x + 22, PY + 173, r["lang"], 9.5, BONE, spacing=0.6)
    return s


def pane(x, label_):
    s = (f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" fill="{PANEL}" '
         f'stroke="{RULE2}"/>\n')
    s += T(x + 14, PY + PH + 18, label_, 8.5, DEEP, spacing=1.8)
    return s


# ═════════════════════════════════════ 04 · SmartChennai
def smartchennai():
    r, col = repo("SmartChennai"), REGION_COLOR["WEB"]
    w = W
    s = head(w, H, "SmartChennai — urban operating system")
    s += chrome(w, H, "04", "SMARTCHENNAI", "FEATURED SYSTEM · 01 OF 04")
    px = 330
    s += f'<defs><clipPath id="city"><rect x="{px}" y="{PY}" width="{PW}" height="{PH}"/>' \
         f'</clipPath></defs>\n'
    s += spec(40, r, col)
    s += pane(px, "plan view · zones, arterials and sensor points")

    g = []
    # ground plane in perspective: verticals converge, bands compress upward
    vpx, vpy = px + PW * 0.5, PY - 150
    for i in range(-6, 19):
        gx = px + i * 46
        g.append(f'<path d="M{gx} {PY+PH} L{vpx + (gx-vpx)*0.30:.1f} {PY}"/>')
    yy, stepy = float(PY + PH), 46.0
    for _ in range(14):
        if yy <= PY:
            break
        g.append(f'<path d="M{px} {yy:.1f} H{px+PW}"/>')
        yy -= stepy
        stepy *= 0.82
    s += (f'<g clip-path="url(#city)" stroke="{RULE2}" stroke-width=".7" '
          f'opacity=".8">{"".join(g)}</g>\n')

    # extruded zone blocks: two rows, back row smaller for depth
    def block(bx, by, bw, bh, d, fill, stroke, op=1):
        top = f'{bx},{by} {bx+d},{by-d*0.55:.1f} {bx+bw+d},{by-d*0.55:.1f} {bx+bw},{by}'
        side = (f'{bx+bw},{by} {bx+bw+d},{by-d*0.55:.1f} '
                f'{bx+bw+d},{by+bh-d*0.55:.1f} {bx+bw},{by+bh}')
        return (f'<g opacity="{op}">'
                f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="1"/>'
                f'<polygon points="{top}" fill="{PANEL2}" stroke="{stroke}" stroke-width="1"/>'
                f'<polygon points="{side}" fill="{INK}" stroke="{stroke}" stroke-width="1"/>'
                f'</g>')

    back = [(px + 62, 26, 34), (px + 134, 22, 46), (px + 214, 30, 30),
            (px + 288, 20, 40), (px + 360, 28, 36), (px + 432, 24, 32)]
    for bx, bh, bw in back:
        s += block(bx, PY + 96 - bh, bw, bh, 7, PANEL2, DEEP, .85)
    front = [(px + 40, 52, 46, False), (px + 118, 74, 40, True),
             (px + 196, 44, 52, False), (px + 282, 88, 44, True),
             (px + 364, 58, 38, False), (px + 430, 70, 48, True)]
    for bx, bh, bw, lit in front:
        s += block(bx, PY + 168 - bh, bw, bh, 11,
                   PANEL if not lit else "#0d1a24", col if lit else RULE2)
        if lit:
            s += (f'<rect x="{bx+8}" y="{PY+168-bh+10}" width="{bw-16}" height="3" '
                  f'fill="{col}" opacity=".85"/>\n')
    assert px + 430 + 48 + 11 < px + PW, "[smartchennai] blocks overflow the pane"

    # arterial route threaded between the two rows
    d = (f"M{px} {PY+120} H{px+96} L{px+150} {PY+108} H{px+262} "
         f"L{px+310} {PY+122} H{px+PW}")
    s += (f'<g clip-path="url(#city)"><path d="{d}" fill="none" stroke="{AMBER}" '
          f'stroke-width="2" opacity=".9"/></g>\n')
    for sx, sy in [(px + 96, PY + 120), (px + 262, PY + 108), (px + 310, PY + 122)]:
        s += (f'<polygon points="{sx},{sy-6} {sx+6},{sy} {sx},{sy+6} {sx-6},{sy}" '
              f'fill="{INK}" stroke="{AMBER}" stroke-width="1.4"/>\n')

    # sensor points
    for sx, sy in [(px + 74, PY + 52), (px + 206, PY + 44), (px + 330, PY + 60),
                   (px + 452, PY + 48), (px + 152, PY + 70)]:
        s += (f'<circle cx="{sx}" cy="{sy}" r="3" fill="{col}"/>'
              f'<circle cx="{sx}" cy="{sy}" r="8" fill="none" stroke="{col}" '
              f'stroke-width=".9" opacity=".45"/>\n')

    s += status(w, H, "SECTION 04 / 09  ▸  SMARTCHENNAI",
                "github.com/BinaryLoops/SmartChennai")
    return write("04-smartchennai.svg", s)


# ═════════════════════════════════════ 05 · Document-AI
def documind():
    r, col = repo("Document-AI"), REGION_COLOR["AI"]
    w = W
    s = head(w, H, "Document-AI — document intelligence")
    s += chrome(w, H, "05", "DOCUMENT-AI", "FEATURED SYSTEM · 02 OF 04")
    px = 40                                   # pane flips to the left
    s += pane(px, "unstructured page in · structured entities out")
    s += spec(610, r, col, width=250)

    # page stack, receding
    for i, (ox, oy, op) in enumerate([(22, 16, ".35"), (11, 8, ".6"), (0, 0, "1")]):
        s += (f'<rect x="{px+40+ox}" y="{PY+26+oy}" width="118" height="146" '
              f'fill="{PANEL2}" stroke="{RULE2}" opacity="{op}"/>\n')
    fx, fy = px + 40, PY + 26
    # text lines with detection boxes over two of them
    for i in range(9):
        ly = fy + 18 + i * 14
        lw = 92 - (30 if i in (2, 6, 8) else 0)
        s += (f'<rect x="{fx+13}" y="{ly}" width="{lw}" height="4" fill="{STEEL}" '
              f'opacity=".45"/>\n')
    for i in (2, 5):
        ly = fy + 12 + i * 14
        s += (f'<rect x="{fx+9}" y="{ly}" width="100" height="16" fill="none" '
              f'stroke="{col}" stroke-width="1.2" stroke-dasharray="4 3"/>\n')
        s += f'<rect x="{fx+9}" y="{ly}" width="4" height="16" fill="{col}"/>\n'

    # entity graph
    nodes = [(px + 330, PY + 44), (px + 430, PY + 70), (px + 352, PY + 106),
             (px + 452, PY + 136), (px + 300, PY + 150)]
    for a, b in [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4)]:
        s += (f'<path d="M{nodes[a][0]} {nodes[a][1]} L{nodes[b][0]} {nodes[b][1]}" '
              f'stroke="{col}" stroke-width="1" opacity=".5"/>\n')
    for i, (nx, ny) in enumerate(nodes):
        rr = 11 if i == 0 else 7.5
        s += (f'<circle cx="{nx}" cy="{ny}" r="{rr}" fill="{INK}" stroke="{col}" '
              f'stroke-width="1.6"/>\n')
        s += f'<circle cx="{nx}" cy="{ny}" r="{rr-4.5}" fill="{col}" opacity=".85"/>\n'

    # extraction rays from the detection boxes into the graph
    for i, (tx2, ty2) in enumerate([(nodes[0][0] - 12, nodes[0][1]),
                                    (nodes[4][0] - 10, nodes[4][1])]):
        sy = fy + 20 + (2 if i == 0 else 5) * 14
        s += (f'<path d="M{fx+112} {sy} C{fx+190} {sy} {tx2-70} {ty2} {tx2} {ty2}" '
              f'fill="none" stroke="{col}" stroke-width="1.2" opacity=".75"/>\n')
        s += f'<polygon points="{tx2},{ty2} {tx2-7},{ty2-4} {tx2-7},{ty2+4}" fill="{col}"/>\n'

    s += T(fx + 178, PY + 100, "extract", 8.5, DEEP, spacing=2.0)
    s += T(px + 296, PY + 178, "entities and relations", 8.5, DEEP, spacing=1.4)
    s += status(w, H, "SECTION 05 / 09  ▸  DOCUMENT-AI",
                "github.com/BinaryLoops/Document-AI")
    return write("05-document-ai.svg", s)


# ═════════════════════════════════════ 06 · PocketMate
def pocketmate():
    r, col = repo("PocketMate"), REGION_COLOR["DATA"]
    w = W
    s = head(w, H, "PocketMate — financial data system")
    s += chrome(w, H, "06", "POCKETMATE", "FEATURED SYSTEM · 03 OF 04")
    px = 330
    s += spec(40, r, col)
    s += pane(px, "relational core on the left, derived series on the right")

    # schema tables
    tables = [("accounts", px + 22, PY + 24), ("entries", px + 22, PY + 112),
              ("categories", px + 150, PY + 68)]
    tw_, rows = 104, 3
    for name, tx, ty in tables:
        th = 20 + rows * 13
        s += f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" fill="{PANEL2}" stroke="{RULE2}"/>\n'
        s += f'<rect x="{tx}" y="{ty}" width="{tw_}" height="16" fill="{col}" opacity=".22"/>\n'
        fits(name, 8.5, tw_ - 12, 0.4, "pocket/table")
        s += T(tx + 7, ty + 11, name, 8.5, BONE, spacing=0.4, weight=700)
        for i in range(rows):
            ry = ty + 22 + i * 13
            s += (f'<rect x="{tx+7}" y="{ry}" width="{tw_-40}" height="3.5" '
                  f'fill="{STEEL}" opacity=".5"/>\n')
            s += f'<circle cx="{tx+tw_-12}" cy="{ry+2}" r="2" fill="{col}" opacity=".7"/>\n'
    # foreign-key links
    s += (f'<path d="M{px+74} {PY+83} V{PY+112}" stroke="{col}" stroke-width="1.2" '
          f'opacity=".8"/>\n')
    s += (f'<path d="M{px+126} {PY+136} H{px+140} V{PY+96} H{px+150}" fill="none" '
          f'stroke="{col}" stroke-width="1.2" opacity=".8"/>\n')

    # derived series
    gx, gy, gw, gh = px + 286, PY + 30, 216, 132
    s += f'<path d="M{gx} {gy+gh} H{gx+gw}" stroke="{RULE2}" stroke-width="1"/>\n'
    s += f'<path d="M{gx} {gy} V{gy+gh}" stroke="{RULE2}" stroke-width="1"/>\n'
    for i in range(1, 4):
        yy = gy + gh * i / 4
        s += f'<path d="M{gx} {yy:.1f} H{gx+gw}" stroke="{RULE}" stroke-dasharray="3 5"/>\n'
    vals = [34, 58, 44, 86, 66, 104, 58, 78]
    bw2 = 16
    step = (gw - 20) / len(vals)
    for i, v in enumerate(vals):
        bx = gx + 12 + i * step
        s += (f'<rect x="{bx:.1f}" y="{gy+gh-v}" width="{bw2}" height="{v}" '
              f'fill="{col}" opacity=".40"/>\n')
        s += (f'<rect x="{bx:.1f}" y="{gy+gh-v}" width="{bw2}" height="2.5" fill="{col}"/>\n')
    assert gx + 12 + (len(vals) - 1) * step + bw2 < gx + gw, "[pocketmate] bars overflow"
    pts = " ".join(f"{gx+12+i*step+bw2/2:.1f},{gy+gh-v-16:.1f}" for i, v in enumerate(vals))
    s += f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="1.6"/>\n'
    for i, v in enumerate(vals):
        s += (f'<circle cx="{gx+12+i*step+bw2/2:.1f}" cy="{gy+gh-v-16:.1f}" r="2.4" '
              f'fill="{TEAL}"/>\n')
    s += T(gx, gy - 8, "entries per period, with running balance above",
           8.5, DEEP, spacing=1.0)
    s += status(w, H, "SECTION 06 / 09  ▸  POCKETMATE",
                "github.com/BinaryLoops/PocketMate")
    return write("06-pocketmate.svg", s)


# ═════════════════════════════════════ 07 · GroceryAppDSA
def grocery():
    r, col = repo("GroceryAppDSA"), REGION_COLOR["SYSTEMS"]
    w = W
    s = head(w, H, "GroceryAppDSA — algorithmic engine")
    s += chrome(w, H, "07", "GROCERYAPPDSA", "FEATURED SYSTEM · 04 OF 04")
    px = 40
    s += pane(px, "search tree above, backing array below")
    s += spec(610, r, col, width=250)

    # balanced tree, levels 1-2-4
    levels = [1, 2, 4]
    pos, idx = {}, 0
    top, vgap = PY + 30, 40
    for li, n in enumerate(levels):
        for k in range(n):
            pos[idx] = (px + 40 + (PW - 130) * (k + 0.5) / n, top + li * vgap)
            idx += 1
    links = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    path = [(0, 2), (2, 5)]
    for a, b in links:
        x1, y1 = pos[a]; x2, y2 = pos[b]
        hot = (a, b) in path
        s += (f'<path d="M{x1:.1f} {y1+11:.1f} C{x1:.1f} {y1+26:.1f} {x2:.1f} {y2-26:.1f} '
              f'{x2:.1f} {y2-11:.1f}" fill="none" stroke="{col if hot else RULE2}" '
              f'stroke-width="{2 if hot else 1.1}" opacity="{1 if hot else .9}"/>\n')
    hot_nodes = {0, 2, 5}
    for i, (nx, ny) in pos.items():
        on = i in hot_nodes
        s += (f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="11" fill="{INK}" '
              f'stroke="{col if on else RULE2}" stroke-width="{2 if on else 1.2}"/>\n')
        if on:
            s += f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="4.5" fill="{col}"/>\n'

    # backing array
    cells, cw2 = 11, 38
    ax = px + 32
    ay = PY + 142
    assert ax + cells * cw2 < px + PW - 10, "[grocery] array overflows the pane"
    for i in range(cells):
        x = ax + i * cw2
        on = i in (5,)
        s += (f'<rect x="{x}" y="{ay}" width="{cw2}" height="30" fill="{PANEL2}" '
              f'stroke="{col if on else RULE2}" stroke-width="{1.6 if on else 1}"/>\n')
        s += T(x + cw2 / 2, ay + 44, str(i), 8, DEEP, anchor="middle", spacing=0)
        if on:
            s += f'<rect x="{x+6}" y="{ay+6}" width="{cw2-12}" height="18" fill="{col}" opacity=".8"/>\n'
    # pointer from the resolved leaf into the array slot
    lx, ly = pos[5]
    s += (f'<path d="M{lx:.1f} {ly+11:.1f} V{ay-10}" stroke="{col}" stroke-width="1.4" '
          f'stroke-dasharray="4 3"/>\n')
    s += f'<polygon points="{lx:.1f},{ay-2} {lx-5:.1f},{ay-11} {lx+5:.1f},{ay-11}" fill="{col}"/>\n'
    s += T(px + 32, PY + 30, "descend", 8.5, DEEP, spacing=1.8)
    s += T(px + PW - 14, ay - 16, "resolve to index", 8.5, DEEP, anchor="end", spacing=1.4)
    s += status(w, H, "SECTION 07 / 09  ▸  GROCERYAPPDSA",
                "github.com/BinaryLoops/GroceryAppDSA")
    return write("07-groceryappdsa.svg", s)


if __name__ == "__main__":
    for fn in (smartchennai, documind, pocketmate, grocery):
        print("built", fn())
