"""Generate two 1000x1000 avatar SVGs matching the profile header (pixel padlock, and a '> HT_' monogram)."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
S = 1000
BG_IN, BG_OUT = "#1b2230", "#0d1117"
BLUE, GREEN, WHITE, DIM = "#79c0ff", "#7ee787", "#e6edf3", "#30363d"

LOCK = [
    "....########....",
    "...##########...",
    "..###......###..",
    "..##........##..",
    "..##........##..",
    "..##........##..",
    "..##........##..",
    "################",
    "################",
    "################",
    "######....######",
    "######....######",
    "#######..#######",
    "#######..#######",
    "#######..#######",
    "################",
    "################",
    "################",
]

FONT = {
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    " ": ["....."] * 7,
}


def frame(inner):
    # faint dot grid inside the circle area, for a terminal feel
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{DIM}"/>'
                   for x in range(40, S, 40) for y in range(40, S, 40)
                   if (x - S / 2) ** 2 + (y - S / 2) ** 2 < 470 ** 2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
<defs>
<radialGradient id="bg" cx="50%" cy="45%" r="65%"><stop offset="0" stop-color="{BG_IN}"/><stop offset="1" stop-color="{BG_OUT}"/></radialGradient>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{S}" height="{S}" fill="url(#bg)"/>
{dots}
{inner}
</svg>'''


def pixels(grid, x0, y0, px, color_fn, gap=4, rx=4):
    out = []
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == "#":
                out.append(f'<rect x="{x0 + j * px}" y="{y0 + i * px}" width="{px - gap}" height="{px - gap}" rx="{rx}" fill="{color_fn(i, j)}"/>')
    return "".join(out)


# A: padlock
px = 34
w, h = 16 * px, 18 * px
lock = pixels(LOCK, (S - w) // 2, (S - h) // 2 + 6, px, lambda i, j: BLUE if i < 7 else GREEN)
(OUT / "avatar-lock.svg").write_text(frame(f'<g filter="url(#glow)">{lock}</g>'), encoding="utf-8")

# B: "> HT_" monogram
text = "> HT_"
px = 30
cols = len(text) * 5 + (len(text) - 1) * 1
x0, y0 = (S - cols * px) // 2, (S - 7 * px) // 2
parts = []
for k, ch in enumerate(text):
    col = GREEN if ch in ">_" else WHITE
    parts.append(pixels(FONT[ch], x0 + k * 6 * px, y0, px, lambda i, j, c=col: c, gap=3, rx=3))
(OUT / "avatar-ht.svg").write_text(frame(f'<g filter="url(#glow)">{"".join(parts)}</g>'), encoding="utf-8")
print("ok")
