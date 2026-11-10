#!/usr/bin/env python3
"""Static destination scenes (no animation), 1000x1250 SVG, named by destination code (fr.svg, af-21.svg ...).

Reuses the drawing helpers from destination_art.py (sky, sun, clouds, hills, trees). This file adds the landmark motifs
and the per-destination scene functions. Names / scene types come from destination-art/scene-plan.xlsx.

Usage: python tools/make_scenes.py --out destination-art/samples [--plan destination-art/scene-plan.xlsx] [codes...]
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import destination_art as da  # noqa: E402
from destination_art import W, H, svg, vgrad, glow_def, sun, clouds, hills, acacia, palm  # noqa: E402

da.ANIMATE = False  # static artwork


def g(x, y, s, body, flip=1):
    return f'<g transform="translate({x} {y}) scale({s * flip} {s})">{body}</g>'


def stars(n, seed, y_max=600, color='#fff'):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.randint(10, 990)}" cy="{r.randint(20, y_max)}" r="{r.choice((1, 1.3, 1.8, 2.4))}" '
                   f'fill="{color}" opacity="{r.choice((.5, .7, .9))}"/>' for _ in range(n))


def pine(x, y, s, c='#1F4D3A'):
    t = ''.join(f'<path d="M{-46 + i * 7} {-i * 44}L0 {-i * 44 - 80}L{46 - i * 7} {-i * 44}Z"/>' for i in range(3))
    return g(x, y, s, f'<g fill="{c}">{t}<rect x="-6" y="0" width="12" height="20"/></g>')


def reflect(body, y, op=.28):
    """Mirror `body` (drawn above the waterline y) below it."""
    return f'<g transform="translate(0 {2 * y}) scale(1 -1)" opacity="{op}">{body}</g>'


# ----------------------------------------------------------------------------------------------------------------
# Landmark motifs: origin = centre of the base, y grows downward (so the structure is drawn with negative y)
# ----------------------------------------------------------------------------------------------------------------
def eiffel(c='#3A2A28', c2='#5A4440'):
    return (f'<path fill="{c}" d="M0 -540L10 -470L20 -380C32 -280 56 -180 112 0L72 0C64 -40 40 -88 0 -88C-40 -88 -64 -40 -72 0'
            f'L-112 0C-56 -180 -32 -280 -20 -380L-10 -470Z"/>'
            f'<rect x="-66" y="-176" width="132" height="12" fill="{c2}"/><rect x="-38" y="-338" width="76" height="9" fill="{c2}"/>'
            f'<rect x="-14" y="-468" width="28" height="7" fill="{c2}"/>')


def taj(c='#FBF3E4', shade='#D9C7B0', c2='#EADCC6'):
    mina = ''.join(
        f'<g transform="translate({sx * 215} 0)"><rect x="-17" y="-30" width="34" height="30" fill="{c2}"/>'
        f'<rect x="-10" y="-250" width="20" height="220" fill="{c}"/><rect x="-14" y="-140" width="28" height="7" fill="{c2}"/>'
        f'<rect x="-14" y="-196" width="28" height="7" fill="{c2}"/><path d="M-14 -250C-14 -284 14 -284 14 -250Z" fill="{c}"/>'
        f'<rect x="-1.5" y="-296" width="3" height="16" fill="{c2}"/></g>' for sx in (-1, 1))
    return (f'<rect x="-300" y="0" width="600" height="36" fill="{c2}"/><rect x="-250" y="-34" width="500" height="34" fill="{c}"/>'
            + mina +
            f'<rect x="-112" y="-170" width="224" height="140" fill="{c}"/>'
            f'<path d="M-36 -30V-98Q-36 -128 0 -140Q36 -128 36 -98V-30Z" fill="{shade}"/>'
            f'<path d="M-92 -30V-88Q-92 -108 -76 -112Q-60 -108 -60 -88V-30Z" fill="{shade}" opacity=".7"/>'
            f'<path d="M92 -30V-88Q92 -108 76 -112Q60 -108 60 -88V-30Z" fill="{shade}" opacity=".7"/>'
            f'<rect x="-64" y="-196" width="128" height="30" fill="{c}"/>'
            f'<path d="M-70 -196C-96 -330 96 -330 70 -196Z" fill="{c}"/><rect x="-2" y="-340" width="4" height="30" fill="{c2}"/>'
            f'<circle cx="0" cy="-346" r="5" fill="{c2}"/>'
            f'<path d="M-104 -170C-108 -216 -66 -216 -70 -170Z" fill="{c}"/><path d="M104 -170C108 -216 66 -216 70 -170Z" fill="{c}"/>')


def opera(c='#FBF4E8', c2='#E4D8C4', base='#C9BBA5'):
    sail = 'M0 0C0 -80 70 -190 200 -225C170 -150 120 -70 104 0Z'
    shade = 'M0 0C0 -80 70 -190 200 -225C120 -120 70 -50 60 0Z'
    parts = ''
    for i, (dx, sc) in enumerate(((0, 1.0), (70, .86), (136, .72), (190, .58))):
        parts += (f'<g transform="translate({dx} 0) scale({sc})"><path d="{sail}" fill="{c}"/><path d="{shade}" fill="{c2}" opacity=".65"/></g>')
    right = ''.join(f'<g transform="translate({300 + dx} 0) scale({-sc} {sc})"><path d="{sail}" fill="{c}"/><path d="{shade}" fill="{c2}" opacity=".65"/></g>'
                    for dx, sc in ((0, .78), (60, .62), (110, .48)))
    return f'<rect x="-30" y="-4" width="420" height="44" fill="{base}"/>' + parts + right


def matterhorn(light='#B9C7E0', dark='#6F81A3', snow='#FFFFFF'):
    return (f'<path d="M-380 0L-120 -250L-60 -300L-40 -420L0 -540L30 -470L70 -360L120 -300L200 -170L380 0Z" fill="{light}"/>'
            f'<path d="M0 -540L30 -470L70 -360L120 -300L200 -170L380 0L60 0L40 -200L18 -380Z" fill="{dark}"/>'
            f'<path d="M-40 -420L0 -540L30 -470L10 -440L-6 -470L-22 -430Z" fill="{snow}"/>'
            f'<path d="M-120 -250L-60 -300L-40 -330L-70 -290L-92 -300Z" fill="{snow}" opacity=".9"/>'
            f'<path d="M70 -360L120 -300L96 -296L84 -330Z" fill="{snow}" opacity=".8"/>')


def windmill(body='#8A5A44', cap='#2E2424', sail='#F1E6D2', arm='#3A2C2C'):
    blades = ''
    for a in (40, 130, 220, 310):
        blades += (f'<g transform="rotate({a})"><rect x="-6" y="-230" width="12" height="230" fill="{arm}"/>'
                   f'<rect x="6" y="-226" width="46" height="130" fill="{sail}" stroke="{arm}" stroke-width="3"/></g>')
    return (f'<path d="M-46 0L-30 -240L30 -240L46 0Z" fill="{body}"/><rect x="-54" y="-26" width="108" height="26" fill="{cap}"/>'
            f'<path d="M-34 -240C-34 -290 34 -290 34 -240Z" fill="{cap}"/>'
            f'<rect x="-9" y="-170" width="18" height="30" fill="{cap}" opacity=".6"/>'
            f'<g transform="translate(0 -250)">{blades}<circle r="12" fill="{arm}"/></g>')


def ger(wall='#F3EDE3', roof='#EAE0CF', trim='#D9772B'):
    return (f'<ellipse cx="0" cy="2" rx="86" ry="8" fill="#000" opacity=".15"/><rect x="-76" y="-62" width="152" height="62" fill="{wall}"/>'
            f'<path d="M-92 -62L0 -128L92 -62Z" fill="{roof}"/><rect x="-92" y="-66" width="184" height="8" fill="{trim}"/>'
            f'<rect x="-14" y="-44" width="28" height="44" fill="{trim}"/><rect x="-3" y="-134" width="6" height="14" fill="#4A3B35"/>')


def horse(c='#2A1D1A'):
    legs = ''.join(f'<rect x="{x}" y="-60" width="8" height="62" rx="3"/>' for x in (-44, -28, 24, 40))
    return (f'<g fill="{c}">{legs}<ellipse cx="0" cy="-78" rx="58" ry="26"/><path d="M36 -94L60 -92L92 -142L70 -150Z"/>'
            f'<ellipse cx="100" cy="-148" rx="22" ry="10" transform="rotate(28 100 -148)"/>'
            f'<path d="M-56 -92Q-84 -70 -78 -30" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round"/></g>')


def liberty(c='#4FA38F', shade='#3C8573', stone='#B9B2A5'):
    spikes = ''.join(
        f'<path d="M{21 * math.cos(math.radians(t)):.1f} {-330 - 21 * math.sin(math.radians(t)):.1f}'
        f'L{44 * math.cos(math.radians(t)):.1f} {-330 - 44 * math.sin(math.radians(t)):.1f}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
        for t in (20, 45, 70, 90, 110, 135, 160))
    return (f'<path d="M-130 0L-90 -40H90L130 0Z" fill="{shade}"/><rect x="-56" y="-150" width="112" height="116" fill="{stone}"/>'
            f'<rect x="-68" y="-160" width="136" height="14" fill="{stone}"/>'
            f'<path d="M-38 -160L-28 -270L-20 -310H20L28 -270L40 -160Z" fill="{c}"/><path d="M0 -310L20 -310L28 -270L40 -160L0 -160Z" fill="{shade}"/>'
            f'<circle cx="0" cy="-330" r="21" fill="{c}"/>' + spikes +
            f'<path d="M14 -300L46 -420L60 -416L32 -292Z" fill="{c}"/><rect x="44" y="-438" width="18" height="12" fill="{shade}"/>'
            f'<path d="M53 -440C40 -462 53 -476 53 -484C68 -468 68 -452 53 -440Z" fill="#FFC93C"/>'
            f'<rect x="-52" y="-262" width="28" height="38" rx="3" fill="{shade}" transform="rotate(-8 -38 -243)"/>')


def pyramid(w, h, light='#C46A58', dark='#8E3C4D'):
    return (f'<path d="M{-w / 2} 0L0 {-h}L{w / 2} 0Z" fill="{dark}"/><path d="M0 {-h}L{w / 2} 0L{w * .1} 0Z" fill="{light}"/>')


def fuji(c='#5B6C8F', snow='#fff'):
    return (f'<path d="M-340 0L-60 -310Q0 -330 60 -310L340 0Z" fill="{c}"/>'
            f'<path d="M-86 -283L-60 -310Q0 -330 60 -310L86 -283L54 -268L22 -292L-6 -262L-40 -286L-62 -266Z" fill="{snow}"/>')


def bungalow(roof='#7A5638', wall='#F2E4CC'):
    stilts = ''.join(f'<rect x="{x}" y="0" width="5" height="40" fill="#6B5240"/>' for x in (-56, -30, 30, 56))
    return (stilts + f'<rect x="-76" y="-6" width="152" height="10" fill="#8C6A4A"/><rect x="-54" y="-44" width="108" height="40" fill="{wall}"/>'
            f'<path d="M-84 -44L0 -100L84 -44Z" fill="{roof}"/><rect x="-14" y="-32" width="28" height="28" fill="#6F4B35"/>')


def aurora(color_a='#4DF0A8', color_b='#7B6BFF', y=330, op=.55):
    return (f'<g filter="url(#au)" opacity="{op}"><path d="M-60 {y + 90}C160 {y - 60} 360 {y + 160} 560 {y + 20}S880 {y - 60} 1060 {y + 60}"'
            f' fill="none" stroke="{color_a}" stroke-width="64" stroke-linecap="round"/>'
            f'<path d="M-60 {y + 190}C180 {y + 60} 380 {y + 230} 600 {y + 110}S900 {y + 40} 1060 {y + 130}" fill="none" stroke="{color_b}" stroke-width="40" stroke-linecap="round" opacity=".7"/></g>')


AURORA_DEF = '<filter id="au" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="26"/></filter>'


def lit_windows(x, y, w, h, seed, color='#FFD98A'):
    r = random.Random(seed)
    out = ''
    for yy in range(int(y) + 10, int(y + h) - 8, 18):
        for xx in range(int(x) + 6, int(x + w) - 8, 14):
            if r.random() < .38:
                out += f'<rect x="{xx}" y="{yy}" width="5" height="7" fill="{color}"/>'
    return out


# ----------------------------------------------------------------------------------------------------------------
# Scenes (each returns an SVG string)
# ----------------------------------------------------------------------------------------------------------------
def scene_fr():
    r = random.Random(11)
    roofs = ''
    x = -10
    while x < 1010:
        w, h = r.randint(70, 120), r.randint(70, 130)
        roofs += (f'<rect x="{x}" y="{880 - h}" width="{w}" height="{h}" fill="#5A4A78"/><path d="M{x - 4} {880 - h}L{x + 12} {880 - h - 28}H{x + w - 12}L{x + w + 4} {880 - h}Z" fill="#3A2F58"/>'
                 + ''.join(f'<rect x="{x + 12 + i * 22}" y="{880 - h + 20}" width="8" height="14" fill="#FFD98A" opacity=".8"/>' for i in range(max(1, (w - 24) // 22))))
        x += w + 4
    defs = vgrad('sky', [(0, '#3A3F8F'), (.5, '#E88CA5'), (1, '#FFD3A5')]) + vgrad('river', [(0, '#6E5A9A'), (1, '#2E2656')]) + glow_def('sg', '#FFD3A5')
    body = (f'<rect width="{W}" height="900" fill="url(#sky)"/>' + stars(40, 3, 380, '#FFF') + sun(720, 780, 74, '#FFE9C9', 'sg') +
            clouds([(60, 360, 1.5, .4, 1, 1), (560, 470, 1.2, .35, 1, 1)], '#FFC4BC') +
            roofs + f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#river)"/>' +
            g(500, 880, .98, eiffel('#2B2140', '#3A2F58')) +
            reflect(g(500, 880, .98, eiffel('#2B2140', '#3A2F58')), 880, .22) +
            ''.join(f'<rect x="{x}" y="{930 + i * 36}" width="{150 - i * 30}" height="5" rx="2.5" fill="#FFD3A5" opacity=".18"/>' for i, x in enumerate((640, 660, 680))) +
            '<path d="M-10 1040C200 1010 420 1050 700 1030C860 1020 960 1040 1010 1036V1250H-10Z" fill="#1B1632"/>' +
            ''.join(f'<g><rect x="{x}" y="900" width="5" height="140" fill="#0F0C20"/><circle cx="{x + 2.5}" cy="900" r="11" fill="#FFD98A"/></g>' for x in (120, 380, 660, 880)))
    return svg('Illustration: the Eiffel Tower over Paris rooftops and the Seine at dusk', defs, '', body)


def scene_in():
    defs = (vgrad('sky', [(0, '#F6B26B'), (.55, '#F9D8A0'), (1, '#FFF0D0')]) + vgrad('pool', [(0, '#7FB6C9'), (1, '#3C7C93')]) +
            vgrad('lawn', [(0, '#4E7A47'), (1, '#2F4E2C')]) + glow_def('sg', '#FFF1D0'))
    cyp = ''.join(f'<g transform="translate({x} 880)"><ellipse cx="0" cy="-70" rx="22" ry="76" fill="#2E4A2C"/><rect x="-3" y="-4" width="6" height="12" fill="#3A2A20"/></g>' for x in (150, 230, 770, 850))
    taj_g = g(500, 860, 1.12, taj())
    body = (f'<rect width="{W}" height="870" fill="url(#sky)"/>' + sun(500, 600, 150, '#FFF6DC', 'sg') +
            clouds([(50, 330, 1.5, .5, 1, 1), (620, 430, 1.2, .45, 1, 1)], '#FFFFFF') +
            hills([(-20, 870), (250, 850), (750, 850), (1020, 870)], 880, '#C9A27A', .5) +
            taj_g + f'<rect y="868" width="{W}" height="{H - 868}" fill="url(#lawn)"/>' +
            '<path d="M430 868L570 868L720 1250L280 1250Z" fill="url(#pool)"/>' +
            f'<g clip-path="url(#poolclip)">{reflect(taj_g, 868, .35)}</g>' + cyp +
            '<path d="M-10 1130C250 1100 400 1160 500 1160C640 1160 780 1100 1010 1130V1250H-10Z" fill="#23361F"/>')
    defs += '<clipPath id="poolclip"><path d="M430 868L570 868L720 1250L280 1250Z"/></clipPath>'
    return svg('Illustration: the Taj Mahal at sunrise reflected in its pool', defs, '', body)


def scene_au():
    arch = ('<g fill="none" stroke="#2D2342" stroke-width="16"><path d="M0 0C140 -230 470 -230 610 0"/></g><rect x="0" y="-12" width="610" height="16" fill="#2D2342"/>'
            + ''.join(f'<path d="M{x} -6V{-round(205 * (1 - ((x - 305) / 305) ** 2) * 1.0)}" stroke="#2D2342" stroke-width="3"/>' for x in range(50, 600, 46)) +
            '<rect x="-10" y="-130" width="34" height="140" fill="#2D2342"/><rect x="586" y="-130" width="34" height="140" fill="#2D2342"/>')
    r = random.Random(4)
    city = ''
    x = -10
    while x < 330:
        w, h = r.randint(36, 64), r.randint(80, 240)
        city += f'<rect x="{x}" y="{880 - h}" width="{w}" height="{h}" fill="#4A3566"/>' + lit_windows(x, 880 - h, w, h, x)
        x += w + 3
    defs = vgrad('sky', [(0, '#3B2A6B'), (.55, '#E8798B'), (1, '#FFC98B')]) + vgrad('sea', [(0, '#5B4F9A'), (1, '#1E1A45')]) + glow_def('sg', '#FFC98B')
    body = (f'<rect width="{W}" height="890" fill="url(#sky)"/>' + stars(30, 8, 360, '#fff') + sun(760, 760, 80, '#FFE5B8', 'sg') +
            clouds([(70, 400, 1.4, .3, 1, 1)], '#FFB6A8') + city + g(395, 890, .84, arch) +
            f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#sea)"/>' + g(120, 905, 1.35, opera()) +
            ''.join(f'<rect x="{x}" y="{930 + i * 30}" width="{200 - i * 24}" height="5" rx="2.5" fill="#FFC98B" opacity=".22"/>' for i, x in enumerate((640, 660, 690, 715))) +
            '<path d="M-10 1150C200 1120 420 1170 700 1140C860 1124 960 1146 1010 1140V1250H-10Z" fill="#150F33"/>')
    return svg('Illustration: Sydney Opera House and Harbour Bridge at sunset', defs, '', body)


def scene_ch():
    defs = vgrad('sky', [(0, '#5FA9F2'), (1, '#D8EEFF')]) + vgrad('meadow', [(0, '#6DBE6B'), (1, '#3C8A45')])
    r = random.Random(2)
    flowers = ''.join(f'<circle cx="{r.randint(20, 980)}" cy="{r.randint(1020, 1230)}" r="{r.choice((3, 4, 5))}" fill="{r.choice(("#FFE066", "#FFFFFF", "#FF8FAB"))}"/>' for _ in range(60))
    chalet = ('<rect x="-62" y="-70" width="124" height="70" fill="#8B5A3C"/><path d="M-84 -70L0 -128L84 -70Z" fill="#5A3A2A"/>'
              '<path d="M-84 -70L0 -128L84 -70L70 -70L0 -116L-70 -70Z" fill="#FFFFFF" opacity=".85"/><rect x="-14" y="-52" width="28" height="52" fill="#4A2E22"/>'
              '<rect x="-48" y="-52" width="22" height="22" fill="#FFD98A"/><rect x="26" y="-52" width="22" height="22" fill="#FFD98A"/><rect x="34" y="-150" width="14" height="30" fill="#5A3A2A"/>')
    body = (f'<rect width="{W}" height="900" fill="url(#sky)"/>' + clouds([(40, 330, 1.5, .85, 1, 1), (600, 420, 1.2, .8, 1, 1)]) +
            g(540, 880, 1.02, matterhorn()) +
            hills([(-20, 860), (200, 820), (420, 860), (720, 830), (1020, 850)], 900, '#7A95B5', .75) +
            f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#meadow)"/>' +
            hills([(-20, 960), (300, 920), (640, 970), (1020, 930)], 1250, '#58AE58') +
            pine(80, 1000, 1.5) + pine(160, 1040, 1.1) + pine(890, 1010, 1.4) + pine(950, 1060, 1.0) + g(300, 1090, 1.25, chalet) + flowers)
    return svg('Illustration: the Matterhorn above an alpine meadow with a wooden chalet', defs, '', body)


def scene_mv():
    defs = (vgrad('sky', [(0, '#7BD3F7'), (.7, '#BFE9F5'), (1, '#FFE6C7')]) + vgrad('sea', [(0, '#2EC4C6'), (.5, '#1E9CC0'), (1, '#0E6FA0')]) + glow_def('sg', '#FFF1C9'))
    huts = ''.join(g(x, y, s, bungalow()) for x, y, s in ((220, 1010, 1.2), (400, 950, 1.0), (550, 905, .82), (660, 872, .66), (740, 850, .54)))
    jetty = '<path d="M60 1060L760 862L772 872L82 1086Z" fill="#8C6A4A"/>'
    body = (f'<rect width="{W}" height="840" fill="url(#sky)"/>' + sun(720, 640, 80, '#FFF6D8', 'sg') +
            clouds([(60, 360, 1.4, .9, 1, 1), (560, 470, 1.1, .85, 1, 1)]) +
            f'<rect y="820" width="{W}" height="{H - 820}" fill="url(#sea)"/>' +
            '<path d="M0 860Q160 840 330 862T700 860T1000 868V900H0Z" fill="#7EE0E0" opacity=".45"/>' +
            ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="#fff" opacity=".35"/>' for x, y, w in ((100, 940, 160), (600, 960, 220), (320, 1120, 260), (700, 1180, 200))) +
            jetty + huts + palm(120, 960, .9, '#2A3B2A') + palm(60, 990, .7, '#1F2E20', -1) +
            '<ellipse cx="110" cy="975" rx="140" ry="22" fill="#F5E3B8"/>')
    return svg('Illustration: overwater bungalows on a jetty over a turquoise lagoon in the Maldives', defs, '', body)


def scene_is():
    defs = vgrad('sky', [(0, '#070B2E'), (1, '#24366E')]) + vgrad('sea', [(0, '#1B2A59'), (1, '#0B1233')]) + AURORA_DEF
    peak = ('<path d="M-300 0L-110 -250L-60 -360L-20 -430L20 -430L60 -360L110 -250L300 0Z" fill="#2E3E66"/>'
            '<path d="M-60 -360L-20 -430L20 -430L60 -360L30 -330L10 -372L-12 -334L-34 -372Z" fill="#E8F0FF"/>'
            '<path d="M-110 -250L-60 -360L-30 -330L-60 -270Z" fill="#E8F0FF" opacity=".5"/>')
    fall = ('<g fill="none" stroke="#E8F0FF" stroke-width="7" stroke-linecap="round" opacity=".85"><path d="M170 880L168 960"/><path d="M192 880L196 954"/><path d="M215 884L216 950"/></g>')
    body = (f'<rect width="{W}" height="880" fill="url(#sky)"/>' + stars(110, 5, 760) + aurora('#4DF0A8', '#9B7BFF', 380, .6) + aurora('#7DFFD0', '#5B8BFF', 520, .35) +
            hills([(-20, 880), (200, 800), (420, 830), (800, 780), (1020, 840)], 900, '#1C2850') + g(560, 890, 1.15, peak) +
            f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#sea)"/>' + reflect(g(560, 890, 1.15, peak), 880, .18) + fall +
            '<path d="M-10 1010C120 970 300 1040 520 1020C720 1002 880 1040 1010 1010V1250H-10Z" fill="#0B0F22"/>' +
            '<path d="M-10 1120C160 1090 360 1150 600 1130C800 1112 920 1140 1010 1120V1250H-10Z" fill="#05070F"/>')
    return svg('Illustration: a snow-capped Icelandic peak under the northern lights over a black shore', defs, '', body)


def scene_gr():
    r = random.Random(21)
    houses = ''
    pts = []
    for row in range(6):
        y = 690 + row * 48
        x = 20 + row * 62
        while x < 700 - row * 6:
            w, h = r.randint(74, 112), r.randint(44, 62)
            houses += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF"/><rect x="{x + w * .72}" y="{y}" width="{w * .28}" height="{h}" fill="#DDE8F4"/>'
                       f'<rect x="{x + 10}" y="{y + 16}" width="12" height="20" fill="#2D6CB5"/>')
            if r.random() < .22:
                houses += f'<path d="M{x + 6} {y}C{x + 6} {y - 40} {x + w - 6} {y - 40} {x + w - 6} {y}Z" fill="#2D6CB5"/>'
            if r.random() < .12:
                houses += f'<circle cx="{x + w - 6}" cy="{y - 2}" r="9" fill="#E0457B"/>'
            x += w + r.randint(6, 16)
    tower = ('<g transform="translate(600 600) scale(1.25)"><rect x="-28" y="0" width="56" height="130" fill="#fff"/><rect x="-28" y="0" width="14" height="130" fill="#DDE8F4"/>'
             '<path d="M-18 0V-22Q0 -40 18 -22V0Z" fill="#2D6CB5"/><path d="M-14 -22C-14 -64 14 -64 14 -22Z" fill="#2D6CB5"/>'
             '<path d="M-10 70V36Q0 26 10 36V70Z" fill="#6E8FB5"/><rect x="-2" y="-84" width="4" height="22" fill="#fff"/></g>')
    defs = vgrad('sky', [(0, '#74B9F5'), (1, '#EAF5FF')]) + vgrad('sea', [(0, '#2D86C9'), (1, '#0E4F8F')]) + glow_def('sg', '#FFF4D2')
    body = (f'<rect width="{W}" height="900" fill="url(#sky)"/>' + sun(780, 520, 70, '#FFF8E0', 'sg') + clouds([(80, 340, 1.4, .9, 1, 1), (600, 440, 1.1, .8, 1, 1)]) +
            f'<rect y="840" width="{W}" height="{H - 840}" fill="url(#sea)"/>' +
            ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="#fff" opacity=".3"/>' for x, y, w in ((560, 960, 280), (640, 1040, 240), (480, 1130, 320))) +
            '<path d="M-10 640C140 650 260 700 360 790C440 870 560 940 700 990L1010 1040V1250H-10Z" fill="#9A6B52"/>' +
            '<path d="M-10 660C140 668 260 716 356 806C436 884 560 950 700 1000L1010 1050V1250H-10Z" fill="#7B523E"/>' + houses + tower +
            '<g fill="#E0457B"><circle cx="44" cy="900" r="22"/><circle cx="80" cy="920" r="18"/><circle cx="20" cy="930" r="16"/></g><g fill="#2D7A3F"><ellipse cx="50" cy="930" rx="60" ry="26" opacity=".9"/></g>')
    return svg('Illustration: whitewashed houses and blue domes on a Santorini cliff above the Aegean', defs, '', body)


def scene_nl():
    cols = ['#E63946', '#FFC300', '#FF6FA5', '#F77F00', '#9B5DE5', '#E63946', '#FFC300', '#FF6FA5']
    vpx, vpy = 500, 846
    strips = ''.join(f'<path d="M{vpx - 2 + (i - 4) * 4} {vpy}L{-700 + i * 260} {H}L{-700 + (i + 1) * 260} {H}L{vpx + 2 + (i - 3) * 4} {vpy}Z" fill="{cols[i % len(cols)]}"/>' for i in range(8))
    defs = vgrad('sky', [(0, '#6FB6F2'), (.7, '#CFE7FA'), (1, '#FFE7D2')])
    body = (f'<rect width="{W}" height="860" fill="url(#sky)"/>' + clouds([(40, 340, 1.8, .95, 1, 1), (560, 440, 1.5, .9, 1, 1), (250, 560, 1.2, .8, 1, 1)]) +
            hills([(-20, 846), (300, 826), (700, 840), (1020, 828)], 900, '#7BB36B') +
            g(540, 850, .55, ''.join(f'<rect x="{x}" y="-44" width="30" height="44" fill="#B5543C"/><path d="M{x - 4} -44L{x + 15} -70L{x + 34} -44Z" fill="#6B3A2E"/>' for x in (-120, -60, 0, 80))) +
            f'<rect y="846" width="{W}" height="{H - 846}" fill="#5E9B52"/>' + strips +
            '<path d="M-10 880L1010 880" stroke="#3E7A3A" stroke-width="10"/>' + g(300, 905, 1.1, windmill()) +
            '<path d="M-10 1210C300 1190 620 1230 1010 1200V1250H-10Z" fill="#3E7A3A" opacity=".8"/>')
    return svg('Illustration: a Dutch windmill beside rows of tulip fields under a big sky', defs, '', body)


def scene_no():
    defs = vgrad('sky', [(0, '#7FB7D6'), (.6, '#F3C6C6'), (1, '#FFE9CF')]) + vgrad('fjord', [(0, '#4B7FA8'), (1, '#1B3F66')]) + glow_def('sg', '#FFF1D2')
    cabin = lambda c: (f'<rect x="-34" y="-36" width="68" height="36" fill="{c}"/><path d="M-42 -36L0 -72L42 -36Z" fill="#3A2E2A"/>'
                       f'<rect x="-8" y="-24" width="16" height="24" fill="#FFF"/><rect x="-26" y="-26" width="10" height="10" fill="#FFF"/>')
    left = '<path d="M-10 420C80 440 150 560 230 700L360 880L-10 880Z" fill="#1E3B52"/><path d="M-10 470C70 480 130 600 200 740L300 880L-10 880Z" fill="#2B4E69"/>'
    right = '<path d="M1010 380C940 420 880 540 820 700L700 880L1010 880Z" fill="#1E3B52"/><path d="M1010 450C950 470 900 590 850 740L770 880L1010 880Z" fill="#2B4E69"/>'
    peaks = hills([(280, 700), (400, 560), (470, 620), (540, 520), (650, 650), (740, 700)], 800, '#9EB6CC', .9)
    body = (f'<rect width="{W}" height="880" fill="url(#sky)"/>' + sun(520, 640, 70, '#FFF6DC', 'sg') + peaks +
            '<path d="M470 620L540 520L600 590L560 600L540 570L510 610Z" fill="#fff" opacity=".85"/>' +
            clouds([(70, 340, 1.4, .6, 1, 1), (600, 440, 1.2, .5, 1, 1)]) + left + right +
            f'<rect y="860" width="{W}" height="{H - 860}" fill="url(#fjord)"/>' +
            ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="#fff" opacity=".22"/>' for x, y, w in ((330, 940, 300), (400, 1010, 220), (300, 1100, 360))) +
            g(120, 930, 1.25, cabin('#B83A32')) + g(240, 950, 1.0, cabin('#C9483C')) + g(70, 1010, 1.4, cabin('#A8332D')) +
            '<path d="M560 1000L640 1000L620 1030L580 1030Z" fill="#3A2E2A"/><path d="M600 1000V952L640 1000Z" fill="#fff"/>' +
            '<path d="M-10 1130C220 1100 380 1180 620 1150C820 1126 940 1160 1010 1140V1250H-10Z" fill="#14293B"/>' + pine(900, 1100, 1.7, '#0F2B2B') + pine(960, 1130, 1.3, '#0F2B2B'))
    return svg('Illustration: a Norwegian fjord with red cabins between steep cliffs at sunrise', defs, '', body)


def scene_mn():
    defs = vgrad('sky', [(0, '#4C97E8'), (1, '#CFE6FA')]) + glow_def('sg', '#FFF3CC')
    body = (f'<rect width="{W}" height="900" fill="url(#sky)"/>' + sun(760, 520, 60, '#FFF6D8', 'sg') +
            clouds([(40, 320, 2.0, .95, 1, 1), (520, 400, 1.6, .9, 1, 1), (250, 520, 1.3, .85, 1, 1)]) +
            hills([(-20, 820), (200, 740), (360, 790), (560, 720), (800, 780), (1020, 740)], 900, '#7D9BC0', .75) +
            hills([(-20, 860), (260, 820), (620, 850), (1020, 820)], 900, '#9BB36B') +
            hills([(-20, 900), (300, 870), (700, 905), (1020, 880)], 1250, '#8FB04F') +
            hills([(-20, 1010), (360, 960), (720, 1020), (1020, 975)], 1250, '#6F9A3F') +
            g(300, 960, 1.15, ger()) + g(470, 935, .75, ger()) +
            g(700, 1040, .95, horse()) + g(850, 1010, .6, horse('#4A322A'), -1) +
            hills([(-20, 1160), (400, 1120), (800, 1170), (1020, 1140)], 1250, '#547A30'))
    return svg('Illustration: white gers and horses on the green Mongolian steppe under a big sky', defs, '', body)


def scene_us():
    r = random.Random(7)
    sky = ''
    x = -10
    while x < 560:
        w, h = r.randint(34, 70), r.randint(110, 330)
        sky += f'<rect x="{x}" y="{880 - h}" width="{w}" height="{h}" fill="#2C2250"/>' + lit_windows(x, 880 - h, w, h, x + 1)
        x += w + 2
    empire = ('<g transform="translate(330 880)" fill="#241B45"><rect x="-44" y="-260" width="88" height="260"/><rect x="-32" y="-320" width="64" height="62"/>'
              '<rect x="-20" y="-364" width="40" height="46"/><rect x="-10" y="-396" width="20" height="34"/><rect x="-2" y="-470" width="4" height="76"/></g>')
    wtc = '<path d="M480 880L494 520L500 440L506 520L520 880Z" fill="#241B45"/>'
    defs = vgrad('sky', [(0, '#35275F'), (.55, '#F28D6B'), (1, '#FFC98B')]) + vgrad('sea', [(0, '#5B4F9A'), (1, '#1E1A45')]) + glow_def('sg', '#FFC98B')
    liberty_g = g(720, 960, 1.18, liberty())
    body = (f'<rect width="{W}" height="890" fill="url(#sky)"/>' + stars(30, 13, 340) + sun(560, 790, 90, '#FFE5B8', 'sg') +
            clouds([(60, 380, 1.4, .3, 1, 1), (560, 470, 1.2, .28, 1, 1)], '#FFB6A8') + sky + empire + wtc +
            f'<rect y="878" width="{W}" height="{H - 878}" fill="url(#sea)"/>' +
            ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="#FFC98B" opacity=".2"/>' for x, y, w in ((140, 930, 220), (380, 980, 200), (150, 1060, 260))) +
            '<path d="M560 1000C640 970 800 960 900 980C960 990 1000 1000 1010 1010V1250H560Z" fill="#1B1638"/>' + liberty_g +
            '<path d="M-10 1160C240 1130 440 1190 700 1160C860 1142 950 1170 1010 1160V1250H-10Z" fill="#120E2A"/>')
    return svg('Illustration: the Statue of Liberty in front of the Manhattan skyline at dusk', defs, '', body)


def scene_gl120():
    defs = vgrad('sky', [(0, '#1C2B6B'), (.45, '#E8766E'), (1, '#FFD9A0')]) + glow_def('sg', '#FFE2A8') + vgrad('sea', [(0, '#3A3466'), (1, '#171332')])
    sil = '#2A1A4A'
    row = (g(110, 880, .27, eiffel(sil, sil)) + g(250, 880, .3, taj(sil, sil, sil)) + g(380, 880, .3, fuji(sil, sil)) +
           g(540, 880, .42, pyramid(300, 210, sil, sil)) + g(660, 880, .3, opera(sil, sil, sil)) + g(830, 880, .3, liberty(sil, sil, sil)))
    plane = ('<g transform="translate(560 520) rotate(-14) scale(1.5)" fill="#fff"><ellipse cx="0" cy="0" rx="86" ry="11"/>'
             '<path d="M-6 0L-48 -66L-28 -66L28 -2Z"/><path d="M-6 0L-48 66L-28 66L28 2Z" opacity=".92"/><path d="M-70 -3L-92 -34L-78 -34L-52 -3Z"/>'
             '<path d="M80 0C84 -6 90 -4 92 0C90 4 84 6 80 0Z" fill="#CFE0FF"/></g>')
    trail = '<path d="M-20 700C200 660 380 600 470 566" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round" opacity=".7"/>'
    body = (f'<rect width="{W}" height="880" fill="url(#sky)"/>' + stars(40, 17, 300) + sun(500, 840, 120, '#FFF0C8', 'sg') +
            clouds([(60, 420, 1.5, .35, 1, 1), (600, 640, 1.4, .3, 1, 1)], '#FFC9B8') + trail + plane + row +
            f'<rect y="878" width="{W}" height="{H - 878}" fill="url(#sea)"/>' +
            ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="#FFD9A0" opacity=".22"/>' for x, y, w in ((380, 930, 240), (330, 1000, 340), (260, 1100, 480))) +
            '<circle cx="500" cy="1180" r="210" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="3"/>' +
            '<ellipse cx="500" cy="1180" rx="210" ry="70" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="3"/>')
    return svg('Illustration: a plane crossing the sky above famous landmarks from around the world at sunrise', defs, '', body)


# Pilot scenes reused as static artwork
SCENES = {
    'fr': scene_fr, 'in': scene_in, 'au': scene_au, 'ch': scene_ch, 'mv': scene_mv, 'is': scene_is,
    'gr': scene_gr, 'nl': scene_nl, 'no': scene_no, 'mn': scene_mn, 'us': scene_us, 'gl-120': scene_gl120,
    'id': da.scene_indonesia, 'jp': da.scene_japan, 'ke': da.scene_kenya, 'af-21': da.scene_africa,
}

PREVIEW = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Destination scenes</title>
<style>
body{margin:0;font-family:ui-sans-serif,system-ui,sans-serif;background:#F7F7F7;color:#111827}
main{max-width:1200px;margin:0 auto;padding:2rem 1.25rem 4rem}h1{margin:0 0 .25rem}p.lead{margin:0 0 1.5rem;color:#5F6672}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:1.25rem}
.card{background:#fff;border:1px solid #E9E9E9;border-radius:20px;padding:.75rem}
.card figure{margin:0;overflow:hidden;border-radius:14px;aspect-ratio:4/5}.card img{display:block;width:100%;height:100%;object-fit:cover}
.wide{margin-top:.5rem;overflow:hidden;border-radius:14px;aspect-ratio:350/240}.wide img{display:block;width:100%;height:100%;object-fit:cover}
.card b{display:block;margin:.6rem 0 0}.card span{font-size:.8125rem;color:#5F6672}
</style></head><body><main><h1>Destination scenes (samples)</h1>
<p class="lead">Static artwork, shown in the desktop (4:5) and the mobile (wide) photo slot.</p><div class="grid">@@CARDS@@</div></main></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--plan', default=None, help='scene-plan.xlsx (adds names to the preview)')
    ap.add_argument('codes', nargs='*')
    a = ap.parse_args()
    meta = {}
    if a.plan and os.path.exists(a.plan):
        import openpyxl
        for row in openpyxl.load_workbook(a.plan, read_only=True).worksheets[0].iter_rows(min_row=2, values_only=True):
            meta[str(row[0]).lower()] = (row[2], row[3], row[4])
    os.makedirs(a.out, exist_ok=True)
    codes = a.codes or list(SCENES)
    cards = ''
    for code in codes:
        out = SCENES[code]()
        open(os.path.join(a.out, f'{code}.svg'), 'w', encoding='utf-8').write(out)
        name, typ, mark = meta.get(code, (code.upper(), '', ''))
        cards += (f'<div class="card"><figure><img src="{code}.svg" alt="{name} illustration"></figure>'
                  f'<div class="wide"><img src="{code}.svg" alt=""></div><b>{name}</b><span>{code.upper()} · {typ}</span></div>')
        print(f'{code + ".svg":12s}{len(out) / 1024:6.1f} KB')
    open(os.path.join(a.out, 'index.html'), 'w', encoding='utf-8').write(PREVIEW.replace('@@CARDS@@', cards))


if __name__ == '__main__':
    main()
