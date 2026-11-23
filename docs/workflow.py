#!/usr/bin/env python3
"""Generates docs/workflow.svg, the workflow flowchart shown in the README.

Run from the repo root:  python3 docs/workflow.py
No dependencies. Edit the layout below, never the SVG.
"""
from pathlib import Path

W, H = 1280, 840
VIOLET, CYAN, PINK, GREEN, AMBER = "#a78bfa", "#22d3ee", "#fb7185", "#34d399", "#fbbf24"
TEXT, MUTED = "#f8fafc", "#a5b0cf"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

out = []
add = out.append


def text(x, y, s, size=13, fill=TEXT, weight=400, anchor="start", font=SANS, spacing=0):
    add(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{s}</text>')


def line(points, color, dashed=False, arrow=True):
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    end = f' marker-end="url(#arrow-{color[1:]})"' if arrow else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"{dash}{end}/>')


def start(cx, y, label, color):
    """A starting point: where the developer is right now."""
    w, h = 320, 52
    text(cx, y - 14, "START HERE", 11, color, 700, "middle", spacing=2)
    add(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{color}" '
        f'fill-opacity="0.16" stroke="{color}" stroke-width="1.5" filter="url(#glow)"/>')
    text(cx, y + 32, label, 16, TEXT, 600, "middle")


def skill(x, y, w, h, name, lines, color, note=None, badge=None):
    """A skill card: name, what it does, and an optional hint to another skill."""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#141a33" stroke="{color}" '
        f'stroke-width="1.5" filter="url(#glow)"/>')
    add(f'<rect x="{x}" y="{y + 14}" width="4" height="{h - 28}" rx="2" fill="{color}"/>')
    tx = x + 18
    if badge:
        add(f'<circle cx="{x + 30}" cy="{y + 27}" r="12" fill="{color}"/>')
        text(x + 30, y + 32, badge, 13, "#0b1020", 800, "middle")
        tx = x + 52
    text(tx, y + 32, name, 15, color, 700, font=MONO)
    for i, s in enumerate(lines):
        text(x + 18, y + 58 + i * 19, s, 13, TEXT)
    if note:
        text(x + 18, y + h - 14, note, 12, MUTED)


add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
    f'aria-label="Workflow: three starting points that all lead into the implement skill and end in a pull request">')
add("<defs>")
add('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/>'
    '<stop offset="1" stop-color="#151235"/></linearGradient>')
add(f'<radialGradient id="g1" cx="0.12" cy="0.1" r="0.5"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.28"/>'
    f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')
add(f'<radialGradient id="g2" cx="0.9" cy="0.95" r="0.55"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.22"/>'
    f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>')
add(f'<linearGradient id="band" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/>'
    f'<stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
add(f'<linearGradient id="title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/>'
    f'<stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>')
add(f'<linearGradient id="rail" gradientUnits="userSpaceOnUse" x1="135" y1="0" x2="1045" y2="0">'
    f'<stop offset="0" stop-color="{VIOLET}"/><stop offset="0.5" stop-color="{CYAN}"/>'
    f'<stop offset="1" stop-color="{PINK}"/></linearGradient>')
add('<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
    '<circle cx="2" cy="2" r="1" fill="#ffffff" fill-opacity="0.06"/></pattern>')
add('<filter id="glow" x="-20%" y="-30%" width="140%" height="160%">'
    '<feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.45"/></filter>')
for c in (VIOLET, CYAN, PINK, GREEN, AMBER):
    add(f'<marker id="arrow-{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
add("</defs>")

for fill in ("url(#bg)", "url(#g1)", "url(#g2)", "url(#dots)"):
    add(f'<rect width="{W}" height="{H}" rx="24" fill="{fill}"/>')

# Title
text(40, 58, "From idea to pull request", 30, "url(#title)", 800)
text(40, 84, "Start wherever you are. Every path leads into implement.", 15, MUTED)

# Three starting points
A, B, C = 235, 640, 1045   # lane centers
RAIL, BAND_Y = 400, 432    # where the lanes join, and the top of the implement band
start(A, 136, "An idea, no ticket yet", VIOLET)
start(B, 136, "A ticket, task or known bug", CYAN)
start(C, 136, "A problem, cause unknown", PINK)

# Lane A: write tickets first
line([(A - 60, 188), (135, 236)], VIOLET)
line([(A + 60, 188), (335, 236)], VIOLET)
text(92, 218, "one ticket", 12, MUTED, anchor="middle")
text(382, 218, "several", 12, MUTED, anchor="middle")
skill(35, 240, 200, 116, "ticket-creator", ["One ticket, approved", "before it is created."], VIOLET)
skill(245, 240, 200, 116, "ticket-orchestrator", ["Many tickets, sliced", "and linked as a set."], VIOLET)
line([(135, 356), (135, RAIL)], VIOLET, arrow=False)
line([(335, 356), (335, RAIL)], VIOLET, arrow=False)
text(A, 384, "pick up a ticket", 12, MUTED, anchor="middle")

# Lane B: straight in
line([(B, 188), (B, RAIL)], CYAN, arrow=False)
add(f'<rect x="{B - 150}" y="262" width="300" height="60" rx="14" fill="#0b1020" stroke="{CYAN}" '
    f'stroke-opacity="0.5" stroke-dasharray="4 5"/>')
text(B, 288, "No detour needed.", 14, TEXT, 600, "middle")
text(B, 308, "Just ask for the implementation.", 13, MUTED, anchor="middle")

# Lane C: find the cause first
line([(C, 188), (C, 236)], PINK)
skill(C - 170, 240, 340, 116, "investigate",
      ["Evidence first, one hypothesis at a time.", "Proves the cause. Fixes nothing."], PINK,
      note="no ticket yet?  &#8594;  ticket-creator drafts one")
line([(C, 356), (C, RAIL)], PINK, arrow=False)
text(C + 14, 384, "cause proven", 12, MUTED)

# The lanes join and enter implement at refine
ENTRY = 205
add(f'<path d="M135,{RAIL} L{C},{RAIL}" stroke="url(#rail)" stroke-width="2" fill="none"/>')
line([(ENTRY, RAIL), (ENTRY, BAND_Y - 2)], CYAN)

# implement band with its four phases
add(f'<rect x="35" y="{BAND_Y}" width="1210" height="262" rx="20" fill="#0e1430" fill-opacity="0.85" '
    f'stroke="url(#band)" stroke-width="2" filter="url(#glow)"/>')
text(60, BAND_Y + 36, "implement", 20, "url(#band)", 800, font=MONO)
text(182, BAND_Y + 36, "runs four phases in order. Each one ends with your approval, and each skill also works on its own.",
     13, MUTED)

CY, CW, CH, GAP = BAND_Y + 56, 262, 126, 34
xs = [60 + i * (CW + GAP) for i in range(4)]
skill(xs[0], CY, CW, CH, "refine", ["Asks what changes the outcome.", "Writes spec.md, updates glossary."], CYAN, badge="1")
skill(xs[1], CY, CW, CH, "strategic-design", ["Refactor first, or not?", "Writes plan.md, does the refactor."],
      "#60a5fa", badge="2")
skill(xs[2], CY, CW, CH, "build", ["One fresh subagent per plan step.", "Test-driven; bugs reproduce first."], "#818cf8",
      note="won't reproduce?  &#8594;  investigate", badge="3")
skill(xs[3], CY, CW, CH, "deliver", ["Fresh subagent checks the diff", "against the spec."], VIOLET, badge="4")
for i in range(3):
    line([(xs[i] + CW + 4, CY + CH / 2), (xs[i + 1] - 4, CY + CH / 2)], CYAN)

# deliver sends the work back to build when a criterion is not met
bx, dx, ly = xs[2] + CW / 2, xs[3] + CW / 2 - 60, CY + CH + 34
add(f'<path d="M{dx},{CY + CH + 2} L{dx},{ly - 10} Q{dx},{ly} {dx - 10},{ly} L{bx + 10},{ly} Q{bx},{ly} {bx},{ly - 10} '
    f'L{bx},{CY + CH + 6}" fill="none" stroke="{AMBER}" stroke-width="2" stroke-dasharray="6 6" '
    f'marker-end="url(#arrow-{AMBER[1:]})"/>')
text((bx + dx) / 2, ly + 20, "criterion not met: fix it, then a new check", 12, AMBER, anchor="middle")

# Outcome
px = xs[3] + CW / 2 + 60
line([(px, CY + CH + 2), (px, 742)], GREEN)
text(px - 14, 726, "all criteria met, you approve", 12, MUTED, anchor="end")
add(f'<rect x="945" y="746" width="300" height="56" rx="28" fill="{GREEN}" fill-opacity="0.18" '
    f'stroke="{GREEN}" stroke-width="1.5" filter="url(#glow)"/>')
text(1095, 780, "Pull request, linked on the ticket", 15, TEXT, 600, "middle")

# home-repo, the optional base for all of it
add(f'<rect x="35" y="746" width="760" height="56" rx="14" fill="#141a33" stroke="{MUTED}" '
    f'stroke-opacity="0.5" stroke-dasharray="4 5"/>')
text(55, 780, "home-repo", 15, AMBER, 700, font=MONO)
text(158, 780, "Optional, set up once. Work across many repos from one place; specs and plans live there.",
     13, MUTED)

add("</svg>")
Path(__file__).with_name("workflow.svg").write_text("\n".join(out) + "\n")
