#!/usr/bin/env python3
"""Generate the cyberpunk SVG asset set for the profile README.

Edit the constants or the CARDS table below and re-run; it rewrites assets/.

    python3 .github/scripts/gen_assets.py [output_dir]

Why the assets look the way they do — GitHub's README rules, all verified:

  - Inline <svg> in a README is stripped entirely, and so are <style>, class=
    and style=. The only way to control the look is committed SVG files
    referenced with relative paths (assets/x.svg), which GitHub rewrites to a
    same-origin /raw/ URL. Those are NOT camo-proxied (only external images
    are), so there is no year-long camo cache to fight — worst case is the
    5-minute max-age on raw.
  - Every asset paints its own opaque dark background. An SVG loaded via <img>
    cannot see GitHub's theme toggle (an internal prefers-color-scheme query
    reads the OS setting, not the site's), so baking the background is what
    keeps these readable in both light and dark mode without a second file set.
  - No external fonts: SVG in <img> runs in "secure animated mode", which
    forbids external references. System monospace stack only.
  - SMIL animation does run in that mode, but scripting never does. Each
    composition is designed to read correctly frozen, with motion as a layer
    on top.
  - Root <svg> needs viewBox AND numeric width/height. A percentage width on
    the root leaves no intrinsic size and the art collapses.
"""
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else \
    pathlib.Path(__file__).resolve().parents[2] / "assets"
OUT.mkdir(parents=True, exist_ok=True)

BG      = "#0A0E14"
PANEL   = "#0D1117"
CYAN    = "#00F0FF"
MAGENTA = "#FF2E97"
PURPLE  = "#A78BFA"
TEXT    = "#C9D1D9"
DIM     = "#6E7681"
# GitHub's own Primer stack — tuned for the platforms that view READMEs.
# Single quotes are safe inside the double-quoted XML attribute.
MONO    = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def defs_common(uid):
    """Grid pattern, scanlines and a neon glow filter, namespaced per-file."""
    return f"""
  <defs>
    <pattern id="grid{uid}" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{CYAN}" stroke-width="0.5" opacity="0.07"/>
    </pattern>
    <pattern id="scan{uid}" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="{CYAN}" opacity="0.045"/>
    </pattern>
    <filter id="glow{uid}" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft{uid}" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="1.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>"""


def brackets(x, y, w, h, size=14, color=CYAN, sw=1.6, op=0.9):
    """HUD corner brackets."""
    return f"""
  <g stroke="{color}" stroke-width="{sw}" fill="none" opacity="{op}">
    <path d="M{x} {y+size}V{y}H{x+size}"/>
    <path d="M{x+w-size} {y}H{x+w}V{y+size}"/>
    <path d="M{x+w} {y+h-size}V{y+h}H{x+w-size}"/>
    <path d="M{x+size} {y+h}H{x}V{y+h-size}"/>
  </g>"""


# ─────────────────────────────────────────────────────────── header
def header():
    W, H, uid = 1000, 250, "h"
    title, ty = "MIHIR JANI", 118
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Mihir Jani — Computer Vision Data Engineer at Glimpse">
{defs_common(uid)}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid{uid})"/>

  <!-- horizon glow -->
  <ellipse cx="{W/2}" cy="{H}" rx="460" ry="90" fill="{CYAN}" opacity="0.06"/>
  <ellipse cx="{W/2}" cy="{H}" rx="240" ry="55" fill="{MAGENTA}" opacity="0.05"/>

{brackets(22, 20, W-44, H-40)}

  <!-- chromatic-aberration title: magenta and cyan ghosts under a white core -->
  <g font-family="{MONO}" font-size="66" font-weight="700" text-anchor="middle" letter-spacing="10">
    <text x="{W/2-3}" y="{ty}" fill="{MAGENTA}" opacity="0.85" filter="url(#soft{uid})">{title}
      <animate attributeName="dx" values="0;-4;1;0;3;0" dur="4s" repeatCount="indefinite"/>
    </text>
    <text x="{W/2+3}" y="{ty}" fill="{CYAN}" opacity="0.85" filter="url(#soft{uid})">{title}
      <animate attributeName="dx" values="0;4;-1;0;-3;0" dur="4s" repeatCount="indefinite"/>
    </text>
    <text x="{W/2}" y="{ty}" fill="#F0F6FC">{title}</text>
  </g>

  <!-- underline -->
  <g>
    <rect x="{W/2-230}" y="140" width="460" height="1.5" fill="{CYAN}" opacity="0.55"/>
    <rect x="{W/2-230}" y="140" width="90" height="1.5" fill="{MAGENTA}">
      <animate attributeName="x" values="{W/2-230};{W/2+140};{W/2-230}" dur="6s" repeatCount="indefinite"/>
    </rect>
  </g>

  <text x="{W/2}" y="177" font-family="{MONO}" font-size="19" fill="{CYAN}" text-anchor="middle" letter-spacing="4.2" filter="url(#soft{uid})">COMPUTER VISION DATA ENGINEER @ GLIMPSE</text>
  <text x="{W/2}" y="207" font-family="{MONO}" font-size="14" fill="{DIM}" text-anchor="middle" letter-spacing="2.4">DATA SCIENCE + COMPUTATIONAL MATH @ UMASS AMHERST — CLASS OF 2028</text>

  <!-- status pips -->
  <g font-family="{MONO}" font-size="11" letter-spacing="1.6">
    <circle cx="46" cy="42" r="3.5" fill="{MAGENTA}">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <text x="58" y="46" fill="{DIM}">SYS.ONLINE</text>
    <text x="{W-46}" y="46" fill="{DIM}" text-anchor="end">BUILDING // SHIPPING</text>
  </g>

  <rect width="{W}" height="{H}" fill="url(#scan{uid})"/>
  <!-- sweep -->
  <rect x="0" y="0" width="{W}" height="2" fill="{CYAN}" opacity="0.16">
    <animate attributeName="y" values="0;{H};0" dur="9s" repeatCount="indefinite"/>
  </rect>
</svg>"""


# ─────────────────────────────────────────────────────────── project card
def card(name, desc, chips, accent=CYAN, tag=None):
    W, H, uid = 560, 158, "c"
    pad = 30
    chip_txt = "  ·  ".join(chips)
    tag_svg = ""
    if tag:
        tw = len(tag) * 7.4 + 18
        tag_svg = f"""
  <g>
    <rect x="{W-pad-tw}" y="30" width="{tw}" height="20" rx="2" fill="{MAGENTA}" opacity="0.16"/>
    <rect x="{W-pad-tw}" y="30" width="{tw}" height="20" rx="2" fill="none" stroke="{MAGENTA}" stroke-width="1" opacity="0.7"/>
    <text x="{W-pad-tw/2}" y="44" font-family="{MONO}" font-size="10.5" fill="{MAGENTA}" text-anchor="middle" letter-spacing="1.4">{tag}</text>
    <animate attributeName="opacity" values="1;0.55;1" dur="2.6s" repeatCount="indefinite"/>
  </g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{name} — {desc}">
{defs_common(uid)}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid{uid})"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="3" fill="{PANEL}" fill-opacity="0.55" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.45"/>

  <!-- left accent spine -->
  <rect x="1" y="1" width="3.5" height="{H-2}" fill="{accent}" opacity="0.9"/>
  <rect x="1" y="1" width="3.5" height="42" fill="{accent}">
    <animate attributeName="y" values="1;{H-45};1" dur="7s" repeatCount="indefinite"/>
  </rect>

{brackets(12, 12, W-24, H-24, size=11, color=accent, sw=1.2, op=0.5)}
{tag_svg}

  <text x="{pad}" y="52" font-family="{MONO}" font-size="25" font-weight="700" fill="{accent}" letter-spacing="1.5" filter="url(#soft{uid})">{name}</text>
  <text x="{pad}" y="88" font-family="{MONO}" font-size="13" fill="{TEXT}" letter-spacing="0.2">{desc}</text>

  <rect x="{pad}" y="107" width="{W-2*pad}" height="1" fill="{accent}" opacity="0.2"/>
  <text x="{pad}" y="130" font-family="{MONO}" font-size="11.5" fill="{DIM}" letter-spacing="0.8">{chip_txt}</text>
  <text x="{W-pad}" y="130" font-family="{MONO}" font-size="13" fill="{accent}" text-anchor="end" opacity="0.75">&#8599;</text>

  <rect width="{W}" height="{H}" fill="url(#scan{uid})"/>
</svg>"""


# ─────────────────────────────────────────────────────────── stack strip
def stack():
    W, uid = 1000, "s"
    rows = [
        ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "C", "R", "SQL"]),
        ("ML  /  AI", ["PyTorch-free sklearn", "NumPy", "Pandas", "OpenCV", "Claude API", "Gemini", "RAG", "FAISS"]),
        ("BACKEND  /  DATA", ["FastAPI", "Next.js", "React", "Node", "PostgreSQL", "Prisma", "MongoDB", "Supabase"]),
        ("TOOLS", ["Git", "Docker", "Linux", "Vercel", "Railway", "Jupyter"]),
    ]
    rows[1] = ("ML  /  AI", ["scikit-learn", "NumPy", "Pandas", "OpenCV", "Claude API", "Gemini", "RAG", "FAISS"])

    row_h, top, label_w = 62, 54, 190
    H = top + row_h * len(rows) + 22
    body = ""
    for i, (label, items) in enumerate(rows):
        y = top + i * row_h
        accent = [CYAN, MAGENTA, PURPLE, CYAN][i]
        body += f"""
  <text x="34" y="{y+22}" font-family="{MONO}" font-size="11.5" fill="{accent}" letter-spacing="2.2" opacity="0.9">{label}</text>
  <rect x="34" y="{y+31}" width="{label_w-46}" height="1" fill="{accent}" opacity="0.25"/>"""
        x = label_w
        for it in items:
            w = len(it) * 7.5 + 24
            body += f"""
  <g>
    <rect x="{x}" y="{y+2}" width="{w:.0f}" height="27" rx="2" fill="{accent}" opacity="0.09"/>
    <rect x="{x}" y="{y+2}" width="{w:.0f}" height="27" rx="2" fill="none" stroke="{accent}" stroke-width="1" opacity="0.35"/>
    <text x="{x+w/2:.0f}" y="{y+20}" font-family="{MONO}" font-size="12" fill="{TEXT}" text-anchor="middle">{it}</text>
  </g>"""
            x += w + 9
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tech stack">
{defs_common(uid)}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid{uid})"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="3" fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.3"/>
{brackets(14, 14, W-28, H-28, size=12, color=CYAN, sw=1.2, op=0.45)}
  <text x="34" y="36" font-family="{MONO}" font-size="13" fill="{CYAN}" letter-spacing="3.4" filter="url(#soft{uid})">// STACK</text>
{body}
  <rect width="{W}" height="{H}" fill="url(#scan{uid})"/>
</svg>"""


# ─────────────────────────────────────────────────────────── divider
def divider():
    W, H, uid = 1000, 26, "d"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="">
{defs_common(uid)}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect x="0" y="{H/2-0.5}" width="{W}" height="1" fill="{CYAN}" opacity="0.45"/>
  <g fill="{CYAN}" opacity="0.9">
    <rect x="0" y="{H/2-3.5}" width="7" height="7"/>
    <rect x="{W-7}" y="{H/2-3.5}" width="7" height="7"/>
  </g>
  <g fill="{CYAN}" opacity="0.35">
    <rect x="{W/2-70}" y="{H/2-1.5}" width="30" height="3"/>
    <rect x="{W/2-26}" y="{H/2-1.5}" width="52" height="3"/>
    <rect x="{W/2+40}" y="{H/2-1.5}" width="30" height="3"/>
  </g>
  <rect x="0" y="{H/2-1}" width="150" height="2" fill="{MAGENTA}" opacity="0.85">
    <animate attributeName="x" values="-150;{W};-150" dur="8s" repeatCount="indefinite"/>
  </rect>
</svg>"""


# ─────────────────────────────────────────────────────────── footer
def footer():
    W, H, uid = 1000, 96, "f"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Building things that matter, one commit at a time">
{defs_common(uid)}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid{uid})"/>
  <ellipse cx="{W/2}" cy="0" rx="420" ry="60" fill="{MAGENTA}" opacity="0.07"/>
  <rect x="0" y="0" width="{W}" height="1.5" fill="{CYAN}" opacity="0.5"/>
  <rect x="0" y="0" width="120" height="1.5" fill="{MAGENTA}">
    <animate attributeName="x" values="-120;{W};-120" dur="7s" repeatCount="indefinite"/>
  </rect>
  <text x="{W/2}" y="46" font-family="{MONO}" font-size="14.5" fill="{TEXT}" text-anchor="middle" letter-spacing="2.4">Building things that matter, one commit at a time.</text>
  <text x="{W/2}" y="72" font-family="{MONO}" font-size="11" fill="{DIM}" text-anchor="middle" letter-spacing="2.8">EOF &#183; mihirzx</text>
  <rect width="{W}" height="{H}" fill="url(#scan{uid})"/>
</svg>"""


CARDS = [
    ("card-rxbuddy.svg",     "RxBuddy",     "AI pharmacy consult over 10k+ FDA drug questions",
     ["TF-IDF + KNN", "OpenFDA", "RxNorm"], MAGENTA, "LIVE"),
    ("card-buddy.svg",       "Buddy",       "Catches medication errors on camera, intervenes by voice",
     ["Viam", "Gemini", "ElevenLabs"], CYAN, None),
    ("card-studiea.svg",     "Studiea",     "Four AI agents running the classroom loop end to end",
     ["Gemini 2.0", "MongoDB", "Express"], CYAN, None),
    ("card-crewlytics.svg",  "Crewlytics",  "Flags overloaded teams, suggests skill-aware reassignment",
     ["Next.js", "Prisma", "scikit-learn"], PURPLE, None),
    ("card-evilhangman.svg", "EvilHangMan", "Hangman that cheats — always keeps the largest word family",
     ["C", "BST", "Makefile"], PURPLE, None),
    ("card-neetcode.svg",    "NeetCode 150","Running solution log for fall recruiting prep",
     ["Python", "DSA"], CYAN, None),
]

written = []
for fn, name, desc, chips, accent, tag in CARDS:
    (OUT / fn).write_text(card(name, desc, chips, accent, tag))
    written.append(fn)

for fn, fx in [("header.svg", header), ("stack.svg", stack),
               ("divider.svg", divider), ("footer.svg", footer)]:
    (OUT / fn).write_text(fx())
    written.append(fn)

for fn in sorted(written):
    print(f"  {fn:26} {(OUT/fn).stat().st_size:>6,} bytes")
print(f"\n{len(written)} assets -> {OUT}")
