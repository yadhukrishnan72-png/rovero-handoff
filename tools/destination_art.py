#!/usr/bin/env python3
"""Destination artwork generator (pilot).

Makes two kinds of animated SVG for destination pages, both 1000x1250 (4:5) so one file works for the tall desktop
slot and the wide mobile slot (`object-fit: cover`; keep the subject in the middle band):

  *-map.svg    country outline (or a region with only its included countries highlighted) from Natural Earth
               (public domain). No border lines are drawn anywhere, so disputed borders are never depicted.
  *-scene.svg  flat sunset scene built from a small motif library (gate, Fuji, acacia, giraffe, pyramids...).

Usage:  python tools/destination_art.py --data path/to/ne_50m_admin_0_countries.geojson --out destination-art/pilot
Data:   https://github.com/nvkelso/natural-earth-vector (geojson/ne_50m_admin_0_countries.geojson), not stored in the repo.
"""
import argparse
import json
import math
import os

W, H = 1000, 1250
BRAND = '#6415FE'
ANIMATE = True  # False drops every animation (static artwork)
REDUCED = '@media (prefers-reduced-motion: reduce){*{animation:none!important}}'


def svg(title, defs, style, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">'
            f'<defs>{defs}</defs>' + (f'<style>{style}{REDUCED}</style>' if ANIMATE else '') + f'{body}</svg>\n')


# ----------------------------------------------------------------------------------------------------------------
# Map style
# ----------------------------------------------------------------------------------------------------------------
def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        ll = dx * dx + dy * dy
        md, mi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            if ll == 0:
                d = (px - ax) ** 2 + (py - ay) ** 2
            else:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / ll))
                d = (px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2
            if d > md:
                md, mi = d, i
        if md > eps * eps:
            keep[mi] = True
            stack += [(a, mi), (mi, b)]
    return [p for p, k in zip(pts, keep) if k]


def polygons(feature):
    g = feature['geometry']
    return g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]


def code_of(f):
    p = f['properties']
    for k in ('ISO_A3', 'ADM0_A3'):
        if p.get(k) and p[k] != '-99':
            return p[k]
    return p.get('ADM0_A3')


def map_art(features, title, highlight, clip=None, pin=False):
    """features: GeoJSON features to draw. highlight: set of codes drawn in brand colour, the rest as context."""
    polys = []  # (is_highlight, rings)
    for f in features:
        hl = code_of(f) in highlight
        for rings in polygons(f):
            lons = [p[0] for p in rings[0]]
            lats = [p[1] for p in rings[0]]
            cx, cy = (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2
            if clip and not (clip[0] <= cx <= clip[2] and clip[1] <= cy <= clip[3]):
                continue
            polys.append((hl, rings))

    pts = [p for hl, rings in polys if hl for p in rings[0]] or [p for _, rings in polys for p in rings[0]]
    lon0 = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2
    lat0 = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
    k = math.cos(math.radians(lat0))
    proj = lambda p: ((p[0] - lon0) * k, -(p[1] - lat0))
    xs = [proj(p)[0] for p in pts]
    ys = [proj(p)[1] for p in pts]
    s = min(880 / (max(xs) - min(xs)), 620 / (max(ys) - min(ys)))
    ox = 500 - s * (max(xs) + min(xs)) / 2
    oy = 625 - s * (max(ys) + min(ys)) / 2
    place = lambda p: (proj(p)[0] * s + ox, proj(p)[1] * s + oy)

    def path_of(rings, eps=0.8):
        out = []
        for ring in rings:
            q = rdp([place(p) for p in ring], eps)
            if len(q) < 3:
                continue
            out.append('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in q) + 'Z')
        return ''.join(out)

    ctx, hi = [], []
    biggest, best = None, -1
    for hl, rings in polys:
        outer = [place(p) for p in rings[0]]
        bw = max(x for x, _ in outer) - min(x for x, _ in outer)
        bh = max(y for _, y in outer) - min(y for _, y in outer)
        if math.hypot(bw, bh) < (0.9 if hl else 1.6):
            continue
        d = path_of(rings)
        if not d:
            continue
        (hi if hl else ctx).append(d)
        if hl and bw * bh > best:
            best, biggest = bw * bh, outer

    # pin at the centroid of the largest highlighted polygon
    pcx = pcy = None
    if pin and biggest:
        a = cx_ = cy_ = 0.0
        for i in range(len(biggest)):
            x1, y1 = biggest[i]
            x2, y2 = biggest[(i + 1) % len(biggest)]
            cr = x1 * y2 - x2 * y1
            a += cr
            cx_ += (x1 + x2) * cr
            cy_ += (y1 + y2) * cr
        pcx, pcy = cx_ / (3 * a), cy_ / (3 * a)

    defs = (f'<linearGradient id="fill" gradientUnits="userSpaceOnUse" x1="0" y1="300" x2="0" y2="950"><stop offset="0" stop-color="#8E5CFF"/>'
            f'<stop offset="1" stop-color="{BRAND}"/></linearGradient>'
            '<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".95"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            '<pattern id="dots" width="34" height="34" patternUnits="userSpaceOnUse"><circle cx="17" cy="17" r="2.2" '
            f'fill="{BRAND}" opacity=".09"/></pattern>'
            '<filter id="blur" x="-10%" y="-10%" width="120%" height="130%"><feGaussianBlur stdDeviation="9"/></filter>')
    style = ('.ring{fill:none;stroke:#6415FE;stroke-width:3;transform-box:fill-box;transform-origin:center;opacity:0;'
             'animation:ring 5s ease-out infinite}.r2{animation-delay:1.65s}.r3{animation-delay:3.3s}'
             '@keyframes ring{0%{transform:scale(.18);opacity:.5}100%{transform:scale(1);opacity:0}}'
             '.float{animation:float 6s ease-in-out infinite alternate}'
             '@keyframes float{from{transform:translateY(0)}to{transform:translateY(-12px)}}'
             '.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}'
             '@keyframes pulse{0%{transform:scale(1);opacity:.55}100%{transform:scale(3.2);opacity:0}}'
             '.tw{animation:tw 3.4s ease-in-out infinite alternate}'
             '@keyframes tw{from{opacity:.78}to{opacity:1}}')

    body = (f'<rect width="{W}" height="{H}" fill="#F1EAFF"/><rect width="{W}" height="{H}" fill="url(#dots)"/>'
            f'<circle cx="500" cy="625" r="560" fill="url(#glow)"/>')
    if pin and pcx is not None:
        body += ''.join(f'<circle class="ring r{i}" cx="{pcx:.1f}" cy="{pcy:.1f}" r="420"/>' for i in (1, 2, 3))
    if ctx:
        body += f'<path d="{"".join(ctx)}" fill="#DCCFF7" fill-rule="evenodd"/>'
    shadow = f'<path d="{"".join(hi)}" fill="#3B0A9E" opacity=".28" fill-rule="evenodd" transform="translate(0 16)" filter="url(#blur)"/>'
    body += shadow + '<g class="float">'
    if pin:
        body += f'<path d="{"".join(hi)}" fill="url(#fill)" stroke="#fff" stroke-opacity=".7" stroke-width="2" fill-rule="evenodd"/>'
        body += (f'<circle class="pulse" cx="{pcx:.1f}" cy="{pcy:.1f}" r="9" fill="#fff"/>'
                 f'<circle cx="{pcx:.1f}" cy="{pcy:.1f}" r="11" fill="#fff"/><circle cx="{pcx:.1f}" cy="{pcy:.1f}" r="5.5" fill="{BRAND}"/>')
    else:
        # region: each included country twinkles on its own beat; no outlines anywhere
        for i, d in enumerate(hi):
            body += f'<path class="tw" style="animation-delay:-{(i * 0.37) % 3.4:.2f}s" d="{d}" fill="url(#fill)" fill-rule="evenodd"/>'
    body += '</g>'
    return svg(title, defs, style, body)


# ----------------------------------------------------------------------------------------------------------------
# Scenic style: shared pieces
# ----------------------------------------------------------------------------------------------------------------
SCENE_CSS = (
    '.cl{animation:cl linear infinite}@keyframes cl{from{transform:translateX(-380px)}to{transform:translateX(1420px)}}'
    '.bd{animation:bd linear infinite}@keyframes bd{from{transform:translate(-80px,30px)}to{transform:translate(1100px,-70px)}}'
    '.glow{transform-box:fill-box;transform-origin:center;animation:gl 5s ease-in-out infinite alternate}'
    '@keyframes gl{from{transform:scale(1);opacity:.85}to{transform:scale(1.08);opacity:1}}'
    '.wv{animation:wv linear infinite}@keyframes wv{from{transform:translateX(0)}to{transform:translateX(-200px)}}'
    '.sway{transform-box:fill-box;transform-origin:50% 100%;animation:sway 6s ease-in-out infinite alternate}'
    '@keyframes sway{from{transform:rotate(-1.6deg)}to{transform:rotate(1.6deg)}}'
    '.fall{animation:fall linear infinite}'
    '@keyframes fall{from{transform:translate(0,-40px) rotate(0)}to{transform:translate(120px,1320px) rotate(540deg)}}'
    '.twk{animation:twk 3s ease-in-out infinite alternate}@keyframes twk{from{opacity:.55}to{opacity:1}}'
)

CLOUD = 'M0 40Q0 20 24 22Q30 0 58 6Q76 -8 98 8Q130 6 132 34Q132 46 120 46H12Q0 46 0 40Z'
BIRD = 'M0 0q9 -9 18 0q9 -9 18 0'
ACACIA_CANOPY = ('M170 420C210 392 300 380 360 392C440 364 560 372 600 408C650 400 720 416 730 440C690 452 640 448 '
                 '600 440C560 458 480 456 430 440C380 460 300 458 250 444C210 450 170 440 170 420Z')
ACACIA_TRUNK = ('M300 650L306 520C306 500 300 480 282 462L260 440L286 452C300 460 308 470 312 484C318 462 330 446 352 '
                '436L384 424L350 450C326 466 316 486 314 520L322 650Z')


def clouds(specs, color='#fff'):
    return ''.join(
        f'<g class="cl" style="animation-duration:{dur}s;animation-delay:-{delay}s"><g transform="translate({x} {y}) scale({sc})" '
        f'fill="{color}" opacity="{op}"><path d="{CLOUD}"/></g></g>' for x, y, sc, op, dur, delay in specs)


def birds(specs, color='#2A1A2E'):
    return ''.join(
        f'<g class="bd" style="animation-duration:{dur}s;animation-delay:-{delay}s"><path d="{BIRD}" transform="translate({x} {y}) scale({sc})" '
        f'fill="none" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/></g>' for x, y, sc, dur, delay in specs)


def sun(cx, cy, r, core, glow):
    return (f'<circle class="glow" cx="{cx}" cy="{cy}" r="{r * 3.2:.0f}" fill="url(#{glow})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{core}"/>')


def glow_def(gid, color):
    return (f'<radialGradient id="{gid}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{color}" stop-opacity=".75"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def vgrad(gid, stops):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">' +
            ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>')


def hills(points, bottom, fill, opacity=1):
    p = points
    d = f'M{p[0][0]} {p[0][1]}'
    for i in range(1, len(p) - 1):
        mx, my = (p[i][0] + p[i + 1][0]) / 2, (p[i][1] + p[i + 1][1]) / 2
        d += f'Q{p[i][0]} {p[i][1]} {mx:.0f} {my:.0f}'
    d += f'L{p[-1][0]} {p[-1][1]}V{bottom}H{p[0][0]}Z'
    return f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>'


def acacia(cx, y, s, color):
    """cx = centre of the canopy (the tree's canopy is wider on the right of its trunk)."""
    x = cx - 140 * s
    return (f'<g transform="translate({x - 310 * s:.1f} {y - 650 * s:.1f}) scale({s})" fill="{color}">'
            f'<path d="{ACACIA_CANOPY}"/><path d="{ACACIA_TRUNK}"/></g>')


def palm(x, y, s, color, flip=1):
    fronds = ''.join(
        f'<path transform="translate(40 -260) rotate({a})" d="M0 0C40 -36 100 -38 160 4C100 -14 46 -10 0 0Z"/>'
        for a in (-60, -25, 10, 45, 85, 125, 165, 200))
    return (f'<g transform="translate({x} {y}) scale({s * flip} {s})"><g class="sway">'
            f'<path d="M0 0C-10 -90 10 -190 40 -260" fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round"/>'
            f'<g fill="{color}">{fronds}</g></g></g>')


def giraffe(x, y, s, color, flip=1):
    legs = ''.join(f'<path d="M{lx} -96h9l-2 96h-6z"/>' for lx in (-58, -38, 30, 48))
    return (f'<g transform="translate({x} {y}) scale({s * flip} {s})" fill="{color}">{legs}'
            '<ellipse cx="0" cy="-122" rx="74" ry="34"/>'
            '<path d="M36 -138L70 -132L120 -300L96 -308Z"/>'
            '<ellipse cx="114" cy="-314" rx="27" ry="12" transform="rotate(-20 114 -314)"/>'
            '<path d="M100 -322L97 -344M111 -325L113 -346" stroke="' + color + '" stroke-width="3" stroke-linecap="round"/>'
            '<circle cx="97" cy="-346" r="4"/><circle cx="113" cy="-348" r="4"/>'
            '<path d="M-72 -134Q-92 -108 -88 -56" fill="none" stroke="' + color + '" stroke-width="4" stroke-linecap="round"/></g>')


def waves(y, color, opacity, dur, amp=14):
    seg = f'q50 -{amp} 100 0t100 0'
    return (f'<g class="wv" style="animation-duration:{dur}s"><path d="M-200 {y}{seg * 16}V{H}H-200Z" '
            f'fill="{color}" opacity="{opacity}"/></g>')


# ----------------------------------------------------------------------------------------------------------------
# Scenes
# ----------------------------------------------------------------------------------------------------------------
def scene_indonesia():
    gate_half = 'M0 0H-120V-50H-100V-90H-80V-130H-60V-165H-40V-195H-20V-215L-6 -232H0Z'
    gate = (f'<g transform="translate(330 935) scale(1.1)" fill="#1F2A2C"><path d="{gate_half}" transform="translate(-46 0)"/>'
            f'<path d="{gate_half}" transform="translate(46 0) scale(-1 1)"/></g>')
    glimmer = ''.join(
        f'<rect class="twk" style="animation-delay:-{i * .5:.1f}s" x="{640 - w / 2}" y="{812 + i * 26}" width="{w}" height="7" rx="3.5" fill="#FFF1C9"/>'
        for i, w in enumerate((150, 120, 96, 70, 44)))
    defs = (vgrad('sky', [(0, '#2F9C95'), (.55, '#F7D79B'), (1, '#FF9E80')]) +
            vgrad('sea', [(0, '#2A8C97'), (1, '#0E4F63')]) + glow_def('sg', '#FFE6A8'))
    body = (f'<rect width="{W}" height="810" fill="url(#sky)"/>' + sun(640, 760, 92, '#FFF1C9', 'sg') +
            clouds([(60, 320, 1.4, .8, 90, 10), (520, 450, 1, .7, 70, 40), (300, 560, 1.1, .6, 110, 80)]) +
            hills([(-20, 800), (140, 640), (300, 560), (350, 520), (400, 560), (560, 690), (700, 800)], 820, '#4E8A88', .75) +
            hills([(300, 810), (520, 700), (760, 770), (1020, 760)], 830, '#3C7C7A', .6) +
            f'<rect y="800" width="{W}" height="{H - 800}" fill="url(#sea)"/>' + glimmer +
            waves(850, '#4FB3B8', .35, 14) + waves(930, '#2A8C97', .45, 10) + waves(1020, '#0E4F63', .5, 7, 18) +
            '<path d="M-10 935C150 915 300 935 430 975C600 1030 800 1055 1010 1060V1250H-10Z" fill="#1F2A2C"/>' +
            '<path d="M700 1065C800 1000 930 990 1010 1000V1250H700Z" fill="#1F2A2C"/>' + gate +
            palm(90, 1010, 1.0, '#1F2A2C') + palm(880, 1030, .85, '#1F2A2C', -1) +
            birds([(120, 380, 1.3, 38, 4), (300, 300, 1, 52, 22), (620, 250, 1.1, 44, 33)], '#1F3B3A'))
    return svg('Illustration: a Balinese split gate on a tropical beach at sunset, with palm trees', defs, SCENE_CSS, body)


def scene_japan():
    fuji = 'M-340 0L-60 -310Q0 -330 60 -310L340 0Z'
    snow = 'M-86 -283L-60 -310Q0 -330 60 -310L86 -283L54 -268L22 -292L-6 -262L-40 -286L-62 -266Z'
    petals = ''.join(
        f'<g class="fall" style="animation-duration:{d}s;animation-delay:-{dl}s"><ellipse cx="{x}" cy="{(x * 7) % 1000 + 120}" rx="6" ry="3.6" fill="#F9B8C8"/></g>'
        for x, d, dl in ((90, 11, 2), (210, 14, 7), (340, 10, 4), (470, 16, 11), (600, 12, 1), (730, 15, 9), (860, 13, 5), (160, 17, 13)))
    blossoms = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in (
        (70, 340, 22, '#F7A8BA'), (110, 318, 16, '#FBC9D6'), (160, 330, 20, '#F7A8BA'), (210, 300, 14, '#FBC9D6'),
        (250, 280, 22, '#F7A8BA'), (300, 262, 15, '#FBC9D6'), (340, 270, 20, '#F7A8BA'), (400, 246, 14, '#FBC9D6'),
        (30, 380, 14, '#FBC9D6'), (190, 356, 14, '#FBC9D6'), (275, 312, 12, '#F7A8BA')))
    torii = ('<g transform="translate(790 1010)"><path d="M-100 0L-94 -214H-72L-66 0Z" fill="#D9342B"/>'
             '<path d="M66 0L72 -214H94L100 0Z" fill="#D9342B"/><rect x="-122" y="-170" width="244" height="18" fill="#D9342B"/>'
             '<path d="M-165 -242C-150 -224 -120 -216 -90 -216H90C120 -216 150 -224 165 -242L165 -228C150 -210 120 -200 90 -200H-90C-120 -200 -150 -210 -165 -228Z" fill="#1F1A1A"/>'
             '<rect x="-12" y="-198" width="24" height="30" fill="#1F1A1A"/></g>')
    defs = (vgrad('sky', [(0, '#F4A9B8'), (.6, '#FBD5D5'), (1, '#FFF1E0')]) +
            vgrad('lake', [(0, '#7E9CBC'), (1, '#3B5778')]) + glow_def('sg', '#FFB3B0'))
    body = (f'<rect width="{W}" height="870" fill="url(#sky)"/>' + sun(640, 470, 118, '#D7263D', 'sg') +
            clouds([(40, 260, 1.3, .85, 100, 20), (560, 380, 1, .8, 80, 50)]) +
            hills([(-20, 870), (160, 800), (330, 835), (560, 790), (760, 830), (1020, 800)], 880, '#9AA9C4', .8) +
            f'<g transform="translate(500 870)"><path d="{fuji}" fill="#5B6C8F"/><path d="{snow}" fill="#fff"/>'
            '<path d="M-340 0L-60 -310L-20 -150L-170 0Z" fill="#4A5A7C" opacity=".35"/></g>' +
            '<g opacity=".7"><ellipse class="cl" style="animation-duration:120s;animation-delay:-30s" cx="300" cy="820" rx="260" ry="26" fill="#fff"/>'
            '<ellipse class="cl" style="animation-duration:150s;animation-delay:-90s" cx="400" cy="858" rx="320" ry="22" fill="#fff"/></g>' +
            f'<rect y="868" width="{W}" height="{H - 868}" fill="url(#lake)"/>' +
            f'<g transform="translate(500 868) scale(1 -1)" opacity=".28"><path d="{fuji}" fill="#fff"/></g>' +
            waves(900, '#fff', .12, 16, 8) + waves(990, '#fff', .1, 12, 10) + waves(1100, '#2B4566', .35, 9, 12) +
            torii + '<g class="sway"><path d="M-30 340C120 330 260 300 440 240" fill="none" stroke="#4A2E2A" stroke-width="14" stroke-linecap="round"/>'
            + blossoms + '</g>' + petals)
    return svg('Illustration: Mount Fuji at sunrise with a red torii gate on a lake and falling cherry blossom petals', defs, SCENE_CSS, body)


def scene_kenya():
    defs = (vgrad('sky', [(0, '#3B2A5A'), (.45, '#D2547A'), (.8, '#F9A64B'), (1, '#FFD27A')]) +
            vgrad('ground', [(0, '#5A2A3C'), (1, '#1E0F1F')]) + glow_def('sg', '#FFD27A'))
    grass = 'M0 1250V1170' + ''.join(f'L{x} {1130 - (x * 7 % 40)}L{x + 14} 1180' for x in range(10, 1000, 28)) + 'L1000 1170V1250Z'
    body = (f'<rect width="{W}" height="840" fill="url(#sky)"/>' + sun(500, 740, 108, '#FFE9A8', 'sg') +
            clouds([(80, 300, 1.4, .35, 100, 20), (600, 420, 1.1, .3, 80, 60)], '#FFB7A0') +
            hills([(-20, 800), (140, 740), (260, 600), (330, 650), (400, 520), (470, 650), (560, 700), (760, 780), (1020, 770)], 840, '#7A3E62', .8) +
            '<path d="M380 560L400 520L420 566L400 552Z" fill="#fff" opacity=".7"/>' +
            hills([(-20, 820), (300, 790), (640, 815), (1020, 790)], 850, '#5A2A4A', .9) +
            f'<rect y="820" width="{W}" height="{H - 820}" fill="url(#ground)"/>' +
            acacia(700, 905, .95, '#1E0F1F') + acacia(170, 880, .55, '#2A1530') +
            giraffe(290, 930, .85, '#1E0F1F') + giraffe(470, 905, .5, '#2A1530') +
            f'<path d="{grass}" fill="#150A18"/>' +
            birds([(100, 360, 1.3, 40, 5), (330, 280, 1, 55, 25), (700, 330, 1.1, 46, 35)]))
    return svg('Illustration: giraffes and acacia trees on the Kenyan savanna at sunset', defs, SCENE_CSS, body)


def scene_africa():
    def pyramid(x, y, w, h, light, dark):
        return (f'<g transform="translate({x} {y})"><path d="M{-w / 2} 0L0 {-h}L{w / 2} 0Z" fill="{dark}"/>'
                f'<path d="M0 {-h}L{w / 2} 0L{w * .1} 0Z" fill="{light}"/></g>')
    defs = (vgrad('sky', [(0, '#F6B25C'), (.55, '#F28A4B'), (1, '#B8476B')]) +
            vgrad('sand', [(0, '#7A2E4B'), (1, '#23102A')]) + glow_def('sg', '#FFD27A'))
    body = (f'<rect width="{W}" height="900" fill="url(#sky)"/>' + sun(640, 700, 100, '#FFF0C2', 'sg') +
            clouds([(60, 330, 1.4, .5, 100, 15), (560, 470, 1.1, .45, 85, 50)], '#FFE2B8') +
            hills([(-20, 820), (260, 770), (560, 800), (1020, 760)], 900, '#8D3A55', .65) +
            pyramid(250, 880, 360, 270, '#C46A58', '#8E3C4D') + pyramid(480, 880, 210, 160, '#C46A58', '#8E3C4D') +
            hills([(-20, 905), (250, 870), (520, 900), (1020, 860)], 940, '#4A1C3A') +
            f'<rect y="900" width="{W}" height="{H - 900}" fill="url(#sand)"/>' +
            hills([(-20, 1000), (300, 960), (620, 1010), (1020, 970)], 1250, '#23102A') +
            acacia(740, 985, .85, '#150A18') + palm(560, 1000, .5, '#150A18') + palm(110, 1040, .62, '#150A18') +
            birds([(120, 360, 1.3, 40, 5), (360, 280, 1, 55, 25), (700, 340, 1.1, 46, 35)], '#3A1830'))
    return svg('Illustration: pyramids, an acacia tree and palms on an African landscape at sunset', defs, SCENE_CSS, body)


# ----------------------------------------------------------------------------------------------------------------
AFRICA_21 = ['DZA', 'CMR', 'TCD', 'CIV', 'COD', 'EGY', 'ETH', 'GAB', 'GHA', 'KEN', 'MAR', 'MOZ', 'NGA', 'RWA', 'SEN',
             'ZAF', 'TZA', 'TUN', 'UGA', 'ZMB', 'ZWE']

PILOT = [
    # slug, label, map features, scene
    ('indonesia', 'Indonesia', scene_indonesia),
    ('japan', 'Japan', scene_japan),
    ('kenya', 'Kenya', scene_kenya),
    ('africa', 'Africa', scene_africa),
]

PREVIEW = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Destination art pilot</title>
<style>
body{margin:0;font-family:ui-sans-serif,system-ui,sans-serif;background:#F7F7F7;color:#111827}
main{max-width:1200px;margin:0 auto;padding:2rem 1.25rem 4rem}
h1{font-size:1.75rem;margin:0 0 .25rem}p.lead{margin:0 0 2rem;color:#5F6672}
section{margin-bottom:3rem}h2{font-size:1.25rem;margin:0 0 1rem}
.row{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem}
.style h3{font-size:.875rem;margin:0 0 .5rem;color:#6415FE;text-transform:uppercase;letter-spacing:.04em}
.frames{display:flex;gap:1rem;align-items:flex-start;flex-wrap:wrap}
figure{margin:0;overflow:hidden;border-radius:24px;background:#DDE3EA}
figure img{display:block;width:100%;height:100%;object-fit:cover}
.d{width:220px;aspect-ratio:4/5}.m{width:320px;height:210px}
@media(max-width:820px){.row{grid-template-columns:1fr}}
</style></head><body><main>
<h1>Destination art pilot</h1>
<p class="lead">Left: map style. Right: scenic style. Each shown in the desktop (4:5) and mobile (wide) photo slots. Images are animated.</p>
@@ROWS@@
</main></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True, help='Natural Earth ne_50m_admin_0_countries.geojson')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    feats = json.load(open(a.data, encoding='utf-8'))['features']
    by_code = {code_of(f): f for f in feats}
    os.makedirs(a.out, exist_ok=True)

    maps = {
        'indonesia': map_art([by_code['IDN']], 'Map of Indonesia', {'IDN'}, pin=True),
        'japan': map_art([by_code['JPN']], 'Map of Japan', {'JPN'}, pin=True),
        'kenya': map_art([by_code['KEN']], 'Map of Kenya', {'KEN'}, pin=True),
        'africa': map_art([f for f in feats if f['properties'].get('CONTINENT') == 'Africa'],
                          'Map of Africa with the included countries highlighted', set(AFRICA_21),
                          clip=(-20, -36, 52, 38)),
    }
    rows = ''
    for slug, label, scene in PILOT:
        open(os.path.join(a.out, f'{slug}-map.svg'), 'w', encoding='utf-8').write(maps[slug])
        open(os.path.join(a.out, f'{slug}-scene.svg'), 'w', encoding='utf-8').write(scene())
        cell = lambda kind: ''.join(
            f'<figure class="{c}"><img src="{slug}-{kind}.svg" alt="{label} {kind} illustration"></figure>' for c in 'dm')
        rows += (f'<section><h2>{label}</h2><div class="row"><div class="style"><h3>Map</h3><div class="frames">{cell("map")}</div></div>'
                 f'<div class="style"><h3>Scene</h3><div class="frames">{cell("scene")}</div></div></div></section>')
    open(os.path.join(a.out, 'index.html'), 'w', encoding='utf-8').write(PREVIEW.replace('@@ROWS@@', rows))
    for fn in sorted(os.listdir(a.out)):
        print(f'{fn:24s}{os.path.getsize(os.path.join(a.out, fn)) / 1024:7.1f} KB')


if __name__ == '__main__':
    main()
