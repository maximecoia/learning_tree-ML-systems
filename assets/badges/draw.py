"""Draw the badges of the 2026 common-core projects that have none yet.

    python3 assets/badges/draw.py

The README shows the 42 projects with the badges collected in
ayogun/42-project-badges. That collection predates the 2026 common core, so
nine of its projects have no badge there. These are drawn here instead, in the
same silhouette and size, 150 by 150 with a pointy top and a teal frame, so the
table reads as one set. They are home-made and the README says so.

Each glyph is plain vector, so nothing depends on the viewer's fonts except the
name band and the "42" of The Answer Protocol. The output is deterministic: a
second run rewrites the same bytes. Standard library only.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent

def hexagon(r, cx=75, cy=75):
    """The six corners of a pointy-top hexagon of radius r, as SVG points."""
    pts = [(cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)))
           for a in range(0, 360, 60)]
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)

# One glyph per project: what the subject is about, in a few shapes.
GLYPHS = {
    'python_piscine': ('PYTHON PISCINE', '''
      <rect x="52" y="40" width="30" height="30" rx="8" fill="#3776ab"/>
      <rect x="68" y="56" width="30" height="30" rx="8" fill="#ffd43b"/>
      <circle cx="60" cy="47" r="3" fill="#fff"/><circle cx="90" cy="79" r="3" fill="#1b1f24"/>'''),
    'a_maze_ing': ('A-MAZE-ING', '''
      <g fill="none" stroke="#7ee0e0" stroke-width="4" stroke-linecap="square">
        <path d="M48 38 H102 V96 H58"/><path d="M48 38 V96"/>
        <path d="M58 48 H92 V86 H68 V58 H82 V76"/>
      </g><circle cx="76" cy="67" r="4" fill="#ffd43b"/>'''),
    'pac_man': ('PAC MAN', '''
      <path d="M70 67 L94 53 A28 28 0 1 0 94 81 Z" fill="#ffd43b"/>
      <circle cx="68" cy="53" r="3.5" fill="#1b1f24"/>
      <circle cx="104" cy="67" r="3.5" fill="#fff"/><circle cx="116" cy="67" r="3.5" fill="#fff"/>'''),
    'call_me_maybe': ('CALL ME MAYBE', '''
      <g fill="#5a6b8c"><rect x="46" y="72" width="9" height="20"/><rect x="60" y="62" width="9" height="30"/>
      <rect x="88" y="66" width="9" height="26"/><rect x="102" y="78" width="9" height="14"/></g>
      <rect x="74" y="40" width="9" height="52" fill="#7ee0e0"/>
      <path d="M78.5 30 l-6 8 h12 z" fill="#7ee0e0"/>'''),
    'rag_against_the_machine': ('RAG', '''
      <g fill="#c9d1d9"><rect x="44" y="40" width="44" height="54" rx="3"/></g>
      <g stroke="#5a6b8c" stroke-width="3"><path d="M51 52 H81 M51 61 H81 M51 70 H72 M51 79 H77"/></g>
      <circle cx="90" cy="76" r="14" fill="none" stroke="#7ee0e0" stroke-width="5"/>
      <path d="M100 86 L112 98" stroke="#7ee0e0" stroke-width="7" stroke-linecap="round"/>'''),
    'codexion': ('CODEXION', '''
      <g fill="#5a6b8c"><rect x="42" y="42" width="52" height="11" rx="2"/>
      <rect x="42" y="58" width="40" height="11" rx="2"/><rect x="42" y="74" width="60" height="11" rx="2"/></g>
      <rect x="42" y="74" width="22" height="11" rx="2" fill="#f0883e"/>
      <circle cx="102" cy="52" r="12" fill="none" stroke="#7ee0e0" stroke-width="4"/>
      <path d="M102 45 V52 H108" stroke="#7ee0e0" stroke-width="3" fill="none"/>'''),
    'fly_in': ('FLY-IN', '''
      <path d="M40 74 L110 42 L84 98 L74 78 Z" fill="#c9d1d9"/>
      <path d="M74 78 L110 42 L64 72 Z" fill="#7ee0e0"/>
      <path d="M44 96 q12 -6 22 -2" stroke="#5a6b8c" stroke-width="3" fill="none" stroke-dasharray="4 4"/>'''),
    'agent_smith': ('AGENT SMITH', '''
      <path d="M40 58 H110" stroke="#c9d1d9" stroke-width="4"/>
      <path d="M44 58 h26 q0 18 -13 18 q-13 0 -13 -18 z" fill="#0d1117" stroke="#c9d1d9" stroke-width="3"/>
      <path d="M80 58 h26 q0 18 -13 18 q-13 0 -13 -18 z" fill="#0d1117" stroke="#c9d1d9" stroke-width="3"/>
      <path d="M50 62 l6 6" stroke="#3fb950" stroke-width="2"/><path d="M86 62 l6 6" stroke="#3fb950" stroke-width="2"/>'''),
    'the_answer_protocol': ('ANSWER PROTOCOL', '''
      <text x="75" y="84" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
            font-size="44" font-weight="700" fill="#7ee0e0">42</text>
      <path d="M44 92 H106" stroke="#5a6b8c" stroke-width="3" stroke-dasharray="6 4"/>'''),
}

for name, (label, glyph) in GLYPHS.items():
    size = 11 if len(label) <= 12 else 9 if len(label) <= 14 else 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150" role="img" aria-label="{label}">
  <defs>
    <radialGradient id="sky" cx="50%" cy="35%" r="70%">
      <stop offset="0" stop-color="#2b3a67"/><stop offset="1" stop-color="#0b1026"/>
    </radialGradient>
    <clipPath id="in"><polygon points="{hexagon(62)}"/></clipPath>
  </defs>
  <polygon points="{hexagon(72)}" fill="#5ecfd0"/>
  <polygon points="{hexagon(66)}" fill="#0d1117"/>
  <polygon points="{hexagon(62)}" fill="url(#sky)"/>
  <g clip-path="url(#in)" fill="#fff" opacity=".7">
    <circle cx="40" cy="45" r="1"/><circle cx="112" cy="40" r="1.2"/><circle cx="104" cy="98" r="1"/>
    <circle cx="35" cy="88" r="1.1"/><circle cx="60" cy="28" r="0.9"/><circle cx="92" cy="26" r="1"/>
  </g>
  <g clip-path="url(#in)">{glyph}
  </g>
  <g clip-path="url(#in)"><rect x="0" y="96" width="150" height="19" fill="#0d1117"/></g>
  <text x="75" y="109.5" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{size}"
        font-weight="700" letter-spacing=".5" fill="#ffffff">{label}</text>
</svg>
'''
    (OUT / f'{name}.svg').write_text(svg, encoding='utf-8')
print(f'{len(GLYPHS)} badges written to {OUT}')
