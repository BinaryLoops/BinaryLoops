"""BINARYLOOPS // ENGINEERING OPERATING SYSTEM — shared design system.

Every panel is drawn with the same chrome so the README reads as one continuous
surface rather than a stack of cards. No renderer is available in this
environment, so all layout is computed arithmetically and checked with the
guards at the bottom of this file.

Static artwork only: no <style>, no animation, no SMIL anywhere.
"""
import json, os

W = 900                    # every panel is authored at this width

INK    = "#05070e"
PANEL  = "#0a101c"
PANEL2 = "#0e1626"
RULE   = "#17223a"
RULE2  = "#232f4d"
BONE   = "#e6ecf7"
TEXT   = "#b9c7dd"
STEEL  = "#5b6d8a"
DEEP   = "#2b3b5c"

TEAL   = "#46e0c8"
VIOLET = "#9b7dff"
AMBER  = "#ffae3d"
MINT   = "#5ee39b"

REGION_COLOR = {"AI": VIOLET, "WEB": TEAL, "DATA": AMBER, "SYSTEMS": MINT}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"

LANG = {"TypeScript": "#3178c6", "Python": "#3572A5",
        "Dart": "#00B4AB", "JavaScript": "#f1e05a"}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")


# ───────────────────────────────────────────── data access
def load():
    with open(os.path.join(ROOT, "data", "repositories.json")) as f:
        return json.load(f)

DB = load()
OWNER = DB["owner"]
REPOS = DB["repositories"]
PROJECTS = [r for r in REPOS if r["kind"] == "project"]
FEATURED = [r for r in REPOS if r.get("featured")]
CODED = [r for r in REPOS if r["lang"]]


def lang_counts():
    c = {}
    for r in REPOS:
        if r["lang"]:
            c[r["lang"]] = c.get(r["lang"], 0) + 1
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


# ───────────────────────────────────────────── text metrics
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def tw(text, size, spacing=0.0):
    """Advance width of monospace text: 0.6em per glyph plus letter-spacing."""
    return len(str(text)) * (size * 0.6 + spacing)


def fits(text, size, box_w, spacing=0.0, label=""):
    w = tw(text, size, spacing)
    assert w <= box_w, f"[{label}] {text!r} needs {w:.0f}px, box is {box_w:.0f}px"
    return w


def no_overlap(boxes, label=""):
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            n1, x1, y1, w1, h1 = boxes[i]
            n2, x2, y2, w2, h2 = boxes[j]
            if x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1:
                raise AssertionError(f"[{label}] {n1} overlaps {n2}")


def inside(boxes, w, h, label=""):
    for n, x, y, bw, bh in boxes:
        assert -1 <= x and x + bw <= w + 1 and -1 <= y and y + bh <= h + 1, \
            f"[{label}] {n} escapes canvas: ({x:.0f},{y:.0f},{bw:.0f},{bh:.0f}) in {w}x{h}"


# ───────────────────────────────────────────── primitives
def T(x, y, text, size=10, fill=None, anchor="start", spacing=1.6,
      weight=400, op=None, family=None):
    a = f' opacity="{op}"' if op is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family or MONO}" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" '
            f'fill="{fill or STEEL}" text-anchor="{anchor}"{a}>{esc(text)}</text>\n')


def outline_T(x, y, text, size, stroke, anchor="start", spacing=0, sw=1.2, op="1",
              crop=False):
    """crop=True marks type that is deliberately bled off the canvas edge, so the
    verification gate treats it as intentional rather than as a layout escape."""
    c = ' data-crop="1"' if crop else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="700" letter-spacing="{spacing}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" text-anchor="{anchor}" opacity="{op}"{c}>'
            f'{esc(text)}</text>\n')


def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
            f'<title>{esc(title)}</title>\n')


def close():
    return "</svg>\n"


def tech_grid(w, h, step=30, op=".5"):
    """Background measurement grid — the substrate every panel shares."""
    v = "".join(f'<path d="M{x} 0V{h}"/>' for x in range(step, w, step))
    hz = "".join(f'<path d="M0 {y}H{w}"/>' for y in range(step, h, step))
    return f'<g stroke="{RULE}" stroke-width=".5" opacity="{op}">{v}{hz}</g>\n'


def registration(w, h, col=None):
    """Corner registration marks — the recurring identity mark of the system."""
    c = col or DEEP
    a, b = 18, 30
    return (f'<g stroke="{c}" stroke-width="1.2" fill="none">'
            f'<path d="M{a} {a+12} V{a} H{a+12}"/><path d="M{w-a-12} {a} H{w-a} V{a+12}"/>'
            f'<path d="M{a} {h-a-12} V{h-a} H{a+12}"/>'
            f'<path d="M{w-a-12} {h-a} H{w-a} V{h-a-12}"/></g>\n')


def ruler(x, y, length, step=15, major=4, col=None):
    """Hairline measurement ruler with tick marks."""
    c = col or RULE2
    parts = [f'<path d="M{x} {y} H{x+length}" stroke="{c}" stroke-width="1"/>']
    n = int(length // step)
    for i in range(n + 1):
        tx = x + i * step
        tall = 6 if i % major == 0 else 3
        parts.append(f'<path d="M{tx} {y} V{y - tall}" stroke="{c}" stroke-width="1"/>')
    return "<g>" + "".join(parts) + "</g>\n"


def chrome(w, h, num, section, right_note, ghost=True):
    """Shared panel chrome: substrate, registration, section header, ghost numeral,
    and the bottom status strip. This is what makes the sections one system."""
    s = f'<rect width="{w}" height="{h}" fill="{INK}"/>\n'
    s += tech_grid(w, h)
    s += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{RULE2}"/>\n'
    s += registration(w, h)

    if ghost:
        # oversized cropped numeral in the background layer
        s += outline_T(w - 26, h + 46, num, 210, RULE2, anchor="end", spacing=-6,
                       sw=1.6, op=".55", crop=True)

    # header
    s += T(40, 44, "BINARYLOOPS", 11, BONE, spacing=3.4, weight=700)
    s += T(40 + tw("BINARYLOOPS", 11, 3.4) + 10, 44, "//", 11, DEEP, spacing=2)
    hx = 40 + tw("BINARYLOOPS", 11, 3.4) + 10 + tw("//", 11, 2) + 10
    s += T(hx, 44, f"{num} {section}", 11, TEAL, spacing=3.4, weight=700)
    assert hx + tw(f"{num} {section}", 11, 3.4) < w - tw(right_note, 9, 1.6) - 60, \
        f"[chrome/{num}] header and right note collide"
    s += T(w - 40, 44, right_note, 9, STEEL, anchor="end", spacing=1.6)
    s += ruler(40, 58, w - 80)

    # bottom strip
    s += f'<path d="M40 {h-40} H{w-40}" stroke="{RULE2}" stroke-width="1"/>\n'
    return s


def status(w, h, left, right=""):
    s = T(40, h - 22, left, 8.5, DEEP, spacing=1.8)
    if right:
        s += T(w - 40, h - 22, right, 8.5, DEEP, anchor="end", spacing=1.8)
    return s


def write(name, body):
    path = os.path.join(ASSETS, name)
    with open(path, "w") as f:
        f.write(body + close())
    import xml.etree.ElementTree as ET
    ET.parse(path)
    assert "<style" not in body and "animate" not in body, \
        f"[{name}] contains animation — assets must be static"
    return path
