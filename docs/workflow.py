#!/usr/bin/env python3
"""Generates docs/workflow.svg, the workflow flowchart shown in the README.

Run from the repo root:  python3 docs/workflow.py
No dependencies. Edit the layout below, never the SVG.
"""
from pathlib import Path

W, H = 1280, 1096
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
    f'aria-label="Workflow: three starting points that lead into the implement skill, with quick-fix as the short path '
    f'for a small change, and end in a pull request. After that, revise handles review comments and failing checks, '
    f'and once it is merged retro turns what was found into lessons and cleanup removes the worktrees">')
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
text(40, 84, "Start wherever you are. Every path ends in a checked pull request.", 15, MUTED)

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

# Lane B: straight in, or the short path when the change is small
IN = 540                    # the straight-in line
QX, QW = 632, 250           # the quick-fix card
QC, QD = QX + QW / 2, 1000  # its center, and where its path drops into deliver
line([(B - 60, 188), (IN, 236), (IN, RAIL)], CYAN, arrow=False)
line([(B + 60, 188), (QC, 236)], CYAN)
text(IN - 8, 218, "anything else", 12, MUTED, anchor="end")
text(QC + 2, 218, "small and local", 12, MUTED)
add(f'<rect x="{IN - 78}" y="262" width="156" height="60" rx="14" fill="#0b1020" stroke="{CYAN}" '
    f'stroke-opacity="0.5" stroke-dasharray="4 5"/>')
text(IN, 288, "No detour needed.", 14, TEXT, 600, "middle")
text(IN, 308, "Just ask to implement it.", 13, MUTED, anchor="middle")
skill(QX, 240, QW, 116, "quick-fix",
      ["Small, local, nothing to decide.", "Short spec, one approval, test first."], CYAN,
      note="not quick?  &#8594;  implement or investigate")

# Lane C: find the cause first
line([(C, 188), (C, 236)], PINK)
skill(C - 150, 240, 300, 116, "investigate",
      ["Evidence first, one hypothesis at a time.", "Proves the cause. Fixes nothing."], PINK,
      note="no ticket yet?  &#8594;  ticket-creator drafts one")
line([(C, 356), (C, RAIL)], PINK, arrow=False)
text(C + 14, 384, "cause proven", 12, MUTED)

# The lanes join and enter implement at refine. The rail has a gap where the quick-fix path crosses it.
ENTRY = 205
add(f'<path d="M135,{RAIL} L{QD - 8},{RAIL} M{QD + 8},{RAIL} L{C},{RAIL}" stroke="url(#rail)" stroke-width="2" '
    f'fill="none"/>')
line([(ENTRY, RAIL), (ENTRY, BAND_Y - 2)], CYAN)

# implement band with its four phases
add(f'<rect x="35" y="{BAND_Y}" width="1210" height="262" rx="20" fill="#0e1430" fill-opacity="0.85" '
    f'stroke="url(#band)" stroke-width="2" filter="url(#glow)"/>')
text(60, BAND_Y + 36, "implement", 20, "url(#band)", 800, font=MONO)
text(182, BAND_Y + 36, "runs four phases in order. Each one ends with your approval, and each skill also works on its own.",
     13, MUTED)

CY, CW, CH, GAP = BAND_Y + 56, 262, 126, 34
xs = [60 + i * (CW + GAP) for i in range(4)]

# quick-fix skips phases 1 to 3 and goes straight to the check in deliver
line([(QC, 356), (QC, 378), (QD, 378), (QD, CY - 4)], CYAN)
text(QD + 12, BAND_Y + 36, "quick-fix joins here", 12, MUTED)

skill(xs[0], CY, CW, CH, "refine", ["Asks until you are aligned.", "Writes spec.md, agrees on the terms."], CYAN, badge="1")
skill(xs[1], CY, CW, CH, "strategic-design", ["Refactor first, or not?", "Writes plan.md, does the refactor."],
      "#60a5fa", note="decision made?  &#8594;  adr records it", badge="2")
skill(xs[2], CY, CW, CH, "build", ["One fresh subagent per plan step.", "Test-driven; bugs reproduce first."], "#818cf8",
      note="won't reproduce?  &#8594;  investigate", badge="3")
skill(xs[3], CY, CW, CH, "deliver", ["Two fresh subagents: spec check", "and code review. You approve."], VIOLET,
      note="what they find  &#8594;  findings.md", badge="4")
for i in range(3):
    line([(xs[i] + CW + 4, CY + CH / 2), (xs[i + 1] - 4, CY + CH / 2)], CYAN)

# deliver sends the work back to build when a criterion is not met or the review finds a bug
bx, dx, ly = xs[2] + CW / 2, xs[3] + CW / 2 - 60, CY + CH + 34
add(f'<path d="M{dx},{CY + CH + 2} L{dx},{ly - 10} Q{dx},{ly} {dx - 10},{ly} L{bx + 10},{ly} Q{bx},{ly} {bx},{ly - 10} '
    f'L{bx},{CY + CH + 6}" fill="none" stroke="{AMBER}" stroke-width="2" stroke-dasharray="6 6" '
    f'marker-end="url(#arrow-{AMBER[1:]})"/>')
text((bx + dx) / 2, ly + 20, "not met, or a bug found: fix it, then new checks", 12, AMBER, anchor="middle")

# Outcome
px = xs[3] + CW / 2 + 60
line([(px, CY + CH + 2), (px, 742)], GREEN)
text(px - 14, 726, "checks pass, you approve the code", 12, MUTED, anchor="end")
add(f'<rect x="945" y="746" width="300" height="56" rx="28" fill="{GREEN}" fill-opacity="0.18" '
    f'stroke="{GREEN}" stroke-width="1.5" filter="url(#glow)"/>')
text(1095, 780, "Pull request, linked on the ticket", 15, TEXT, 600, "middle")

# After the pull request: revise for review comments and failing checks, retro and cleanup once it is merged
AY, AH = 852, 116           # the row below the pull request
skill(945, AY, 300, AH, "revise", ["Review comments and failing checks.", "Same rules, then deliver checks again."],
      AMBER, note="cause unknown?  &#8594;  investigate")
line([(1045, 804), (1045, AY - 4)], AMBER, dashed=True)
line([(1145, AY - 2), (1145, 808)], GREEN)
text(1037, 832, "comments, red checks", 12, MUTED, anchor="end")
text(1153, 832, "fixed, checked", 12, MUTED)

RX, KX = 585, 215           # the retro card and the cleanup card
RC, KC = RX + 150, KX + 150  # their centers
skill(RX, AY, 300, AH, "retro", ["Reads findings.md, proposes lessons.", "You approve each one."], GREEN,
      note="a rule a machine can check?  &#8594;  ticket")
skill(KX, AY, 300, AH, "cleanup", ["Removes the worktrees and branches.", "Checks first; you approve the list."],
      GREEN, note="spec, plan and findings stay")
line([(943, 774), (835, 774), (835, AY - 4)], GREEN)
line([(835, 824), (KC, 824), (KC, AY - 4)], GREEN)
text(889, 764, "merged", 12, MUTED, anchor="middle")

# What retro leaves behind
LY = AY + AH + 44
line([(RC, AY + AH + 2), (RC, LY - 4)], GREEN)
add(f'<rect x="{RC - 240}" y="{LY}" width="480" height="56" rx="28" fill="{GREEN}" fill-opacity="0.18" '
    f'stroke="{GREEN}" stroke-width="1.5" filter="url(#glow)"/>')
text(RC, LY + 34, "Lessons in the standards, glossary and ADRs", 15, TEXT, 600, "middle")

# home-repo, the optional base for all of it
add(f'<rect x="35" y="746" width="760" height="56" rx="14" fill="#141a33" stroke="{MUTED}" '
    f'stroke-opacity="0.5" stroke-dasharray="4 5"/>')
text(55, 780, "home-repo", 15, AMBER, 700, font=MONO)
text(158, 780, "Optional, set up once. Work across many repos from one place; specs and plans live there.",
     13, MUTED)

add("</svg>")
Path(__file__).with_name("workflow.svg").write_text("\n".join(out) + "\n")
