"""Draw the hexagon badges of the README: school projects and roadmap modules.

    python3 assets/badges/draw.py

Two sets, one silhouette: 150 by 150, a pointy top, a coloured frame.

- **The 2026 school projects.** The README shows the 42 projects with the
  badges collected in ayogun/42-project-badges. That collection predates the
  2026 common core, so nine of its projects have no badge there. They are drawn
  here with the same teal frame, so the school table reads as one set, and the
  README says they are home-made. They are written next to this file.
- **The roadmap's own modules.** One badge per module of the added layer and
  of the proofs, written to `roadmap/`. The frame says the layer: violet for
  the added layer, gold for a deliverable or a proof. Each is drawn twice,
  `<id>.svg` and `<id>-locked.svg`, the second in grey. `carte_phases.py`
  picks one from the graders and refuses a module that has no badge here.

Each glyph is plain vector, so nothing depends on the viewer's fonts except the
name band and a few glyphs made of letters. The output is deterministic: a
second run rewrites the same bytes. Standard library only.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROADMAP = OUT / 'roadmap'
FRAMES = {'school': '#5ecfd0', 'added': '#8b9cf7', 'proof': '#e3b341'}
SANS = 'Helvetica, Arial, sans-serif'


def hexagon(r, cx=75, cy=75):
    """The six corners of a pointy-top hexagon of radius r, as SVG points."""
    pts = [(cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)))
           for a in range(0, 360, 60)]
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)


def badge(label, frame, glyph, locked=False):
    """One badge as SVG text. A locked badge is the same drawing, greyed."""
    size = 11 if len(label) <= 12 else 9 if len(label) <= 14 else 8
    grey = ('\n    <filter id="grey"><feColorMatrix type="saturate" values="0"/></filter>'
            if locked else '')
    body = f'''
  <polygon points="{hexagon(72)}" fill="{FRAMES[frame]}"/>
  <polygon points="{hexagon(66)}" fill="#0d1117"/>
  <polygon points="{hexagon(62)}" fill="url(#sky)"/>
  <g clip-path="url(#in)" fill="#fff" opacity=".7">
    <circle cx="40" cy="45" r="1"/><circle cx="112" cy="40" r="1.2"/><circle cx="104" cy="98" r="1"/>
    <circle cx="35" cy="88" r="1.1"/><circle cx="60" cy="28" r="0.9"/><circle cx="92" cy="26" r="1"/>
  </g>
  <g clip-path="url(#in)">{glyph}
  </g>
  <g clip-path="url(#in)"><rect x="0" y="96" width="150" height="19" fill="#0d1117"/></g>
  <text x="75" y="109.5" text-anchor="middle" font-family="{SANS}" font-size="{size}"
        font-weight="700" letter-spacing=".5" fill="#ffffff">{label}</text>'''
    if locked:
        body = f'\n  <g filter="url(#grey)" opacity=".45">{body}\n  </g>'
    aria = f'{label}, not yet earned' if locked else label
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150" role="img" aria-label="{aria}">
  <defs>
    <radialGradient id="sky" cx="50%" cy="35%" r="70%">
      <stop offset="0" stop-color="#2b3a67"/><stop offset="1" stop-color="#0b1026"/>
    </radialGradient>
    <clipPath id="in"><polygon points="{hexagon(62)}"/></clipPath>{grey}
  </defs>{body}
</svg>
'''

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


# Colours shared by the roadmap glyphs.
T = '#7ee0e0'   # cyan accent
Y = '#ffd43b'   # yellow
O = '#f0883e'   # orange
G = '#3fb950'   # green
S = '#c9d1d9'   # light grey
M = '#5a6b8c'   # muted blue-grey
D = '#0d1117'   # near black


def big(text, size=40, colour=T, y=80):
    """A glyph made of letters, centred in the badge."""
    return (f'<text x="75" y="{y}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="{size}" font-weight="700" fill="{colour}">{text}</text>')


# The roadmap's modules, by curriculum id: (label, frame, glyph). The frame is
# "added" for the added layer and "proof" for a deliverable or a proof.
MODULES = {
    'py-socle': ('PYTHON SOCLE', 'added', f'''
      <rect x="42" y="36" width="66" height="50" rx="6" fill="{S}"/>
      <rect x="42" y="36" width="66" height="11" rx="6" fill="{M}"/>
      <circle cx="50" cy="41.5" r="2.2" fill="{O}"/><circle cx="57" cy="41.5" r="2.2" fill="{Y}"/>
      <path d="M52 58 l9 7 l-9 7" fill="none" stroke="{D}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M66 74 h18" stroke="#3776ab" stroke-width="4" stroke-linecap="round"/>'''),
    'ms-maths': ('MATHS', 'added', f'''
      <path d="M40 86 H112 M44 90 V34" stroke="{M}" stroke-width="2.5"/>
      <path d="M46 84 C60 84 62 40 76 40 C90 40 92 84 108 84" fill="none" stroke="{T}" stroke-width="4"/>
      <path d="M76 40 V86" stroke="{Y}" stroke-width="2" stroke-dasharray="3 3"/>'''),
    'rte-route-l1': ('ROUTE TO L1', 'added', f'''
      <path d="M42 86 C54 70 60 80 70 66 S88 52 96 42" fill="none" stroke="{S}" stroke-width="3" stroke-dasharray="5 5"/>
      <circle cx="42" cy="86" r="5" fill="{T}"/><circle cx="70" cy="66" r="5" fill="{T}"/>
      <path d="M96 30 V56" stroke="{S}" stroke-width="3"/><path d="M96 30 L114 36 L96 42 Z" fill="{O}"/>'''),
    'l1-livrable': ('L1 · A GPT', 'proof', big('L1', 46, '#e3b341', 82)),
    'mes-performance': ('MEASUREMENT', 'added', f'''
      <circle cx="75" cy="64" r="24" fill="none" stroke="{S}" stroke-width="5"/>
      <rect x="69" y="30" width="12" height="7" rx="2" fill="{S}"/>
      <path d="M75 64 L88 52" stroke="{O}" stroke-width="4" stroke-linecap="round"/>
      <circle cx="75" cy="64" r="3.5" fill="{O}"/>
      <path d="M75 44 v4 M95 64 h-4 M75 84 v-4 M55 64 h4" stroke="{M}" stroke-width="2.5"/>'''),
    'inf-mesure': ('INFERENCE', 'added', f'''
      <path d="M42 88 H110 M44 90 V34" stroke="{M}" stroke-width="2.5"/>
      <path d="M46 84 L62 80 L76 72 L88 58 L96 40" fill="none" stroke="{T}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M88 58 V88" stroke="{O}" stroke-width="2" stroke-dasharray="3 3"/>
      <circle cx="88" cy="58" r="4.5" fill="{O}"/>'''),
    'l2-livrable': ('L2 · THE CURVE', 'proof', big('L2', 46, '#e3b341', 82)),
    'go-bases': ('GO', 'added', big('Go', 44, '#00add8', 80)),
    'ops-exploitation': ('KUBERNETES', 'added', f'''
      <circle cx="75" cy="62" r="25" fill="#326ce5"/>
      <circle cx="75" cy="62" r="11" fill="none" stroke="#fff" stroke-width="3.5"/>
      <g stroke="#fff" stroke-width="3.5" stroke-linecap="round">
        <path d="M75 51 V40"/><path d="M83.6 55.1 L92.2 48.3"/><path d="M85.7 64.4 L96.4 66.9"/>
        <path d="M79.8 71.9 L84.5 81.8"/><path d="M70.2 71.9 L65.5 81.8"/><path d="M64.3 64.4 L53.6 66.9"/>
        <path d="M66.4 55.1 L57.8 48.3"/></g>'''),
    'ops-controle': ('CONTROL LAYER', 'added', f'''
      <path d="M44 80 A31 31 0 0 1 106 80" fill="none" stroke="{M}" stroke-width="7"/>
      <path d="M44 80 A31 31 0 0 1 90 54" fill="none" stroke="{T}" stroke-width="7"/>
      <path d="M75 80 L94 58" stroke="{O}" stroke-width="4" stroke-linecap="round"/>
      <circle cx="75" cy="80" r="5" fill="{O}"/>'''),
    'inf-speculatif': ('SPECULATIVE', 'added', f'''
      <path d="M40 62 H60 M60 62 L80 44 H108 M60 62 L80 80 H108" fill="none" stroke="{S}" stroke-width="4" stroke-linejoin="round"/>
      <g fill="{T}"><circle cx="88" cy="44" r="4"/><circle cx="100" cy="44" r="4"/></g>
      <g fill="{M}"><circle cx="88" cy="80" r="4"/><circle cx="100" cy="80" r="4"/></g>
      <path d="M106 36 l6 8 l-6 8" fill="none" stroke="{G}" stroke-width="3"/>'''),
    'inf-memoire': ('MEMORY', 'added', f'''
      <g fill="{M}"><rect x="40" y="36" width="20" height="14" rx="2"/><rect x="65" y="36" width="20" height="14" rx="2"/>
      <rect x="90" y="36" width="20" height="14" rx="2"/><rect x="40" y="56" width="20" height="14" rx="2"/>
      <rect x="90" y="56" width="20" height="14" rx="2"/><rect x="65" y="76" width="20" height="14" rx="2"/></g>
      <g fill="{T}"><rect x="65" y="56" width="20" height="14" rx="2"/><rect x="40" y="76" width="20" height="14" rx="2"/>
      <rect x="90" y="76" width="20" height="14" rx="2"/></g>'''),
    'inf-vllm': ('VLLM', 'added', f'''
      <path d="M44 38 L66 88 H84 L106 38 H90 L75 72 L60 38 Z" fill="{Y}"/>
      <path d="M60 38 L75 72 L66 88 L44 38 Z" fill="#30a2ff"/>'''),
    'l3-livrable': ('L3 · CONTRIB', 'proof', big('L3', 46, '#e3b341', 82)),
    'pro-entretiens': ('INTERVIEWS', 'proof', f'''
      <path d="M38 40 h44 a6 6 0 0 1 6 6 v20 a6 6 0 0 1 -6 6 h-28 l-10 9 v-9 h-6 a6 6 0 0 1 -6 -6 v-20 a6 6 0 0 1 6 -6 z" fill="{S}"/>
      <path d="M112 56 h-30 a6 6 0 0 0 -6 6 v16 a6 6 0 0 0 6 6 h18 l9 8 v-8 h3 a6 6 0 0 0 6 -6 v-16 a6 6 0 0 0 -6 -6 z" fill="{T}"/>
      <g fill="{M}"><circle cx="50" cy="56" r="3"/><circle cx="60" cy="56" r="3"/><circle cx="70" cy="56" r="3"/></g>'''),
    'go-controleur': ('GO CONTROLLER', 'added', f'''
      <path d="M100 52 A26 26 0 1 0 101 74" fill="none" stroke="#00add8" stroke-width="6" stroke-linecap="round"/>
      <path d="M92 44 L103 51 L94 61" fill="none" stroke="#00add8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="75" cy="62" r="9" fill="{Y}"/>'''),
    'pro-stage-1': ('INTERNSHIP', 'proof', f'''
      <rect x="40" y="46" width="70" height="42" rx="6" fill="{O}"/>
      <path d="M62 46 v-8 a4 4 0 0 1 4 -4 h18 a4 4 0 0 1 4 4 v8" fill="none" stroke="{S}" stroke-width="4"/>
      <path d="M40 64 H110" stroke="{D}" stroke-width="3"/><rect x="69" y="59" width="12" height="10" rx="2" fill="{Y}"/>'''),
    'c-moteur-inference': ('C ENGINE', 'added', f'''
      <g transform="translate(75 62)">
        <g fill="{S}">{''.join(f'<rect x="-5" y="-31" width="10" height="12" rx="2" transform="rotate({a})"/>' for a in range(0, 360, 45))}</g>
        <circle r="22" fill="{S}"/><circle r="14" fill="{D}"/>
      </g>{big('C', 22, T, 70)}'''),
    'c-concurrence': ('CONCURRENCY', 'added', f'''
      <g fill="none" stroke-width="4" stroke-linecap="round">
        <path d="M40 44 H110" stroke="{T}"/><path d="M40 62 H110" stroke="{Y}"/><path d="M40 80 H110" stroke="{O}"/></g>
      <rect x="66" y="36" width="18" height="52" rx="4" fill="none" stroke="{S}" stroke-width="3" stroke-dasharray="4 3"/>'''),
    'cs149-parallelisme': ('CS149', 'added', f'''
      <g fill="{M}">{''.join(f'<rect x="{42 + 17 * (i % 4)}" y="{32 + 15 * (i // 4)}" width="14" height="12" rx="2"/>' for i in range(16))}</g>
      <g fill="{T}">{''.join(f'<rect x="{42 + 17 * (i % 4)}" y="{32 + 15 * (i // 4)}" width="14" height="12" rx="2"/>' for i in (0, 1, 2, 3, 5, 6, 10))}</g>'''),
    'par-profilage': ('PROFILING', 'added', f'''
      <rect x="38" y="78" width="74" height="10" rx="2" fill="{O}"/>
      <rect x="38" y="66" width="46" height="10" rx="2" fill="{Y}"/><rect x="86" y="66" width="22" height="10" rx="2" fill="{Y}"/>
      <rect x="38" y="54" width="30" height="10" rx="2" fill="{T}"/><rect x="70" y="54" width="12" height="10" rx="2" fill="{T}"/>
      <rect x="38" y="42" width="18" height="10" rx="2" fill="{S}"/>'''),
    'l4-livrable': ('L4 · PROFILE', 'proof', big('L4', 46, '#e3b341', 82)),
    'gpu-competition': ('GPU MODE', 'added', f'''
      <path d="M56 36 H94 V54 a19 19 0 0 1 -38 0 Z" fill="{Y}"/>
      <path d="M56 42 h-8 a8 8 0 0 0 8 14 M94 42 h8 a8 8 0 0 1 -8 14" fill="none" stroke="{Y}" stroke-width="4"/>
      <rect x="70" y="72" width="10" height="8" fill="{Y}"/><rect x="60" y="80" width="30" height="8" rx="2" fill="{O}"/>'''),
    'cu-cuda': ('CUDA', 'added', f'''
      <rect x="44" y="38" width="62" height="48" rx="5" fill="#76b900"/>
      <rect x="54" y="47" width="42" height="30" rx="3" fill="{D}"/>
      <g fill="#76b900">{''.join(f'<rect x="{58 + 9 * (i % 4)}" y="{51 + 8 * (i // 4)}" width="6" height="5"/>' for i in range(12))}</g>
      <g stroke="#76b900" stroke-width="3">{''.join(f'<path d="M{52 + 10 * i} 38 v-6 M{52 + 10 * i} 86 v6"/>' for i in range(5))}</g>'''),
    'tri-triton': ('TRITON', 'added', f'''
      <path d="M75 92 V44" stroke="{S}" stroke-width="5"/>
      <path d="M55 30 V50 a20 20 0 0 0 40 0 V30" fill="none" stroke="{T}" stroke-width="5"/>
      <path d="M75 28 V50" stroke="{T}" stroke-width="5"/>
      <g fill="{T}"><path d="M55 22 l-6 10 h12 z"/><path d="M75 20 l-6 10 h12 z"/><path d="M95 22 l-6 10 h12 z"/></g>'''),
    'l5-livrable': ('L5 · KERNEL', 'proof', big('L5', 46, '#e3b341', 82)),
    'num-precision': ('PRECISION', 'added', f'''
      <rect x="36" y="52" width="8" height="20" fill="{O}"/>
      <g fill="{Y}">{''.join(f'<rect x="{46 + 9 * i}" y="52" width="7" height="20"/>' for i in range(4))}</g>
      <g fill="{T}">{''.join(f'<rect x="{84 + 9 * i}" y="52" width="7" height="20"/>' for i in range(4))}</g>
      <path d="M36 80 H114" stroke="{M}" stroke-width="2"/>'''),
    'dist-multigpu': ('MULTI-GPU', 'added', f'''
      <g stroke="{S}" stroke-width="3"><path d="M56 46 H94 M56 78 H94 M56 46 V78 M94 46 V78 M56 46 L94 78"/></g>
      <g fill="#76b900"><rect x="44" y="35" width="24" height="22" rx="3"/><rect x="82" y="35" width="24" height="22" rx="3"/>
      <rect x="44" y="67" width="24" height="22" rx="3"/><rect x="82" y="67" width="24" height="22" rx="3"/></g>'''),
    'cpp-moderne': ('MODERN C++', 'added', big('C++', 34, '#659ad2', 76)),
    'qua-evaluation': ('EVALUATION', 'added', f'''
      <circle cx="75" cy="62" r="28" fill="{S}"/><circle cx="75" cy="62" r="19" fill="{O}"/>
      <circle cx="75" cy="62" r="10" fill="{S}"/><circle cx="75" cy="62" r="4" fill="{O}"/>
      <path d="M75 62 L106 34" stroke="{D}" stroke-width="3"/><path d="M106 34 l-2 8 l8 -2 z" fill="{D}"/>'''),
    'pro-alternance': ('WORK-STUDY', 'proof', f'''
      <path d="M75 34 L114 52 L75 70 L36 52 Z" fill="{S}"/>
      <path d="M54 62 V80 q21 12 42 0 V62 L75 72 Z" fill="{M}"/>
      <path d="M108 55 V78" stroke="{Y}" stroke-width="3"/><circle cx="108" cy="80" r="4" fill="{Y}"/>'''),
}


if __name__ == '__main__':
    for name, (label, glyph) in GLYPHS.items():
        (OUT / f'{name}.svg').write_text(badge(label, 'school', glyph), encoding='utf-8')
    ROADMAP.mkdir(exist_ok=True)
    for name, (label, frame, glyph) in MODULES.items():
        (ROADMAP / f'{name}.svg').write_text(badge(label, frame, glyph), encoding='utf-8')
        (ROADMAP / f'{name}-locked.svg').write_text(badge(label, frame, glyph, True),
                                                    encoding='utf-8')
    print(f'{len(GLYPHS)} school badges and {len(MODULES)} module badges, '
          f'each module twice, written to {OUT}')
