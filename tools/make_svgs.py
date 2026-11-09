"""Generate the profile README SVGs (terminal header + build-rule pipeline), dark and light."""
import sys
from html import escape
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", dim="#8b949e",
                 key="#79c0ff", accent="#7ee787", red="#ff7b72", amber="#e3b341", purple="#d2a8ff"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", dim="#656d76",
                  key="#0550ae", accent="#1a7f37", red="#cf222e", amber="#9a6700", purple="#8250df"),
}
FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# ---------------------------------------------------------------- terminal header
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
    "######....######",
    "######....######",
    "#######..#######",
    "#######..#######",
    "#######..#######",
    "################",
    "################",
    "################",
]

# (key, [(text, color-name), ...])
INFO = [
    ("Role",    [("Founding engineer · Indian credit fintech", "text")]),
    ("Focus",   [("Agent identity · delegated authz · MCP security", "text")]),
    ("Specs",   [("OAuth 2.1 · RFC 8693 · RFC 9728 · WIMSE · ID-JAG", "text")]),
    ("Now",     [("Tamarin model of MCP authorization", "text"), (" (IETF 127)", "dim")]),
    ("Model 01", [("bug variant ", "text"), ("✗ attack found", "red"), (" · fix ", "text"), ("✓ proven", "accent")]),
    ("Agents",  [("LangGraph · CrewAI · Vertex AI · GAIA L1 ", "text"), ("90%", "accent"), (" @ $0", "dim")]),
    ("Stack",   [("Python · TypeScript · FastAPI · Postgres · GCP", "text")]),
    ("Infra",   [("Terraform · Docker · Cloud Run · keyless CI", "text")]),
    ("Rule",    [("model recommends → code decides → human signs", "amber")]),
]

W, CH, LH = 860, 8.43, 23  # width, approx char width at 14px, line height


def terminal(t):
    c = THEMES[t]
    rows = []
    top = 70
    # ASCII lock
    px, lx, ly = 11, 44, top - 4
    for i, line in enumerate(LOCK):
        col = c["key"] if i < 7 else c["accent"]
        rects = "".join(f'<rect x="{lx + j * px}" y="{ly + i * px}" width="{px - 1}" height="{px - 1}" rx="1.5"/>'
                        for j, ch in enumerate(line) if ch == "#")
        rows.append(f'<g fill="{col}" class="l" style="animation-delay:{i * 0.035:.2f}s">{rects}</g>')
    x0 = 268
    rows.append(f'<text x="{x0}" y="{top}" class="l" style="animation-delay:.1s"><tspan fill="{c["accent"]}" font-weight="700">harsh</tspan><tspan fill="{c["dim"]}">@</tspan><tspan fill="{c["key"]}" font-weight="700">thumar</tspan></text>')
    rows.append(f'<text x="{x0}" y="{top + LH}" class="l dim" style="animation-delay:.2s">{"─" * 64}</text>')
    for i, (k, parts) in enumerate(INFO):
        y = top + LH * (i + 2)
        dots = "." * (11 - len(k))
        spans = "".join(f'<tspan fill="{c[col]}">{escape(txt)}</tspan>' for txt, col in parts)
        rows.append(
            f'<text x="{x0}" y="{y}" class="l" style="animation-delay:{0.3 + i * 0.12:.2f}s">'
            f'<tspan fill="{c["key"]}">{escape(k)}</tspan><tspan fill="{c["dim"]}"> {dots} </tspan>{spans}</text>')
    y = top + LH * (len(INFO) + 3)
    rows.append(f'<text x="{x0}" y="{y}" class="l" style="animation-delay:{0.3 + len(INFO) * 0.12:.2f}s">'
                f'<tspan fill="{c["accent"]}">$</tspan><tspan fill="{c["text"]}"> ./verify --model mcp-auth</tspan></text>')
    cur_x = x0 + CH * 26
    rows.append(f'<rect x="{cur_x:.0f}" y="{y - 14}" width="9" height="17" fill="{c["accent"]}" class="cursor"/>')
    H = y + 34
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Harsh Thumar: founding engineer working on agent identity, delegated authorization and MCP security">
<style>
text{{font-family:{FONT};font-size:14px;fill:{c["text"]};white-space:pre}}
.dim{{fill:{c["dim"]}}}
.art{{fill:{c["accent"]};font-size:15px}}
.l{{animation:in .45s ease-out both}}
.cursor{{animation:blink 1.1s steps(1) infinite}}
@keyframes in{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.l,.cursor{{animation:none}}}}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>
<path d="M.5 12.5a12 12 0 0 1 12-12h{W - 25}a12 12 0 0 1 12 12v24h-{W - 1}z" fill="{c["panel"]}"/>
<line x1="0" y1="36.5" x2="{W}" y2="36.5" stroke="{c["border"]}"/>
<circle cx="22" cy="18.5" r="6" fill="#ff5f57"/><circle cx="42" cy="18.5" r="6" fill="#febc2e"/><circle cx="62" cy="18.5" r="6" fill="#28c840"/>
<text x="{W / 2}" y="23" text-anchor="middle" class="dim" style="font-size:12.5px">harsh@thumar: ~ — whoami</text>
{chr(10).join(rows)}
</svg>
'''


# ---------------------------------------------------------------- pipeline diagram
STEPS = [
    ("01", "MODEL", "proposes", "LLM / agent drafts the", "answer or action", "purple"),
    ("02", "GUARD", "decides", "rules, allow-lists,", "read-only DB roles", "key"),
    ("03", "HUMAN", "signs off", "anything that moves", "money or credit", "amber"),
    ("04", "LOG", "remembers", "append-only, hash-", "chained audit trail", "accent"),
]


def pipeline(t):
    c = THEMES[t]
    Wp, H = 860, 150
    bw, gap, x = 178, 40, 12
    parts = []
    for i, (n, title, verb, l1, l2, col) in enumerate(STEPS):
        bx = x + i * (bw + gap)
        parts.append(f'''<g class="b" style="animation-delay:{i * 0.25:.2f}s">
<rect x="{bx}" y="14" width="{bw}" height="120" rx="10" fill="{c["panel"]}" stroke="{c["border"]}"/>
<rect x="{bx}" y="14" width="4" height="120" rx="2" fill="{c[col]}"/>
<text x="{bx + 18}" y="40" class="n" fill="{c["dim"]}">{n}</text>
<text x="{bx + 44}" y="40" class="h" fill="{c[col]}">{title}</text>
<text x="{bx + 18}" y="66" class="v" fill="{c["text"]}">{verb}</text>
<text x="{bx + 18}" y="96" class="s" fill="{c["dim"]}">{escape(l1)}</text>
<text x="{bx + 18}" y="115" class="s" fill="{c["dim"]}">{escape(l2)}</text>
</g>''')
        if i < len(STEPS) - 1:
            ax = bx + bw + 6
            parts.append(f'<line x1="{ax}" y1="74" x2="{ax + gap - 14}" y2="74" stroke="{c["dim"]}" stroke-width="2" class="flow"/>'
                         f'<path d="M{ax + gap - 16} 68 l8 6 -8 6" fill="none" stroke="{c["dim"]}" stroke-width="2"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wp}" height="{H}" viewBox="0 0 {Wp} {H}" role="img" aria-label="How I build AI near money: the model proposes, deterministic code decides, a human signs off, and everything is logged">
<style>
text{{font-family:{FONT}}}
.n{{font-size:12px}} .h{{font-size:14px;font-weight:700;letter-spacing:1.5px}}
.v{{font-size:18px;font-weight:600}} .s{{font-size:12.5px}}
.b{{animation:in .5s ease-out both}}
.flow{{stroke-dasharray:4 5;animation:dash 1.2s linear infinite}}
@keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
@keyframes dash{{to{{stroke-dashoffset:-18}}}}
@media (prefers-reduced-motion:reduce){{.b,.flow{{animation:none}}}}
</style>
{chr(10).join(parts)}
</svg>
'''


for t in THEMES:
    (OUT / f"header-{t}.svg").write_text(terminal(t), encoding="utf-8")
    (OUT / f"rule-{t}.svg").write_text(pipeline(t), encoding="utf-8")
print("ok", sorted(p.name for p in OUT.iterdir()))
