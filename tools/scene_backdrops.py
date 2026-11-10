"""The 14 base scenes. Each takes the destination's motif keys, a colour mood (variant 0 day, 1 sunset, 2 golden) and a
seeded random generator, and returns (defs, body). make_scenes.py wraps them into the final SVG."""
import random

from destination_art import W, H, vgrad, glow_def, sun, clouds, hills, acacia, palm
from scene_kit import M, R, C, E, P

VAR = [
    dict(name='day', sky=[(0, '#5FA9F2'), (.6, '#B9DDF7'), (1, '#EAF5FF')], sun='#FFF6D8', sun_xy=(740, 540), c='#DCCDB5', s='#B3A088', d='#6A5A4A',
         cloud='#FFFFFF', cloud_op=.9, far='#9DB8D4', mid='#6FA862', near='#3F7E45', fg='#2F5F38', sea=[(0, '#2EC4C6'), (1, '#0E6FA0')], sand='#F5E3B8',
         dune=['#F2D3A0', '#E0B67C', '#C99A62'], lake=[(0, '#7FB6D6'), (1, '#2E6A9A')], rock='#8C8A96', snow='#FFFFFF'),
    dict(name='sunset', sky=[(0, '#3B2A6B'), (.55, '#E8798B'), (1, '#FFC98B')], sun='#FFE5B8', sun_xy=(690, 780), c='#34284F', s='#271E3F', d='#5B4A80',
         cloud='#FFB6A8', cloud_op=.35, far='#6A4A7E', mid='#4B2F5B', near='#2D1B3E', fg='#170F26', sea=[(0, '#5B4F9A'), (1, '#1E1A45')], sand='#6A4A5A',
         dune=['#9A4F5E', '#6E3550', '#40213F'], lake=[(0, '#6B5A9A'), (1, '#241E4A')], rock='#4A3A5E', snow='#F4DCE8'),
    dict(name='golden', sky=[(0, '#F6B25C'), (.55, '#F9D8A0'), (1, '#FFF0D0')], sun='#FFF6DC', sun_xy=(300, 640), c='#E2CFAE', s='#B99E76', d='#7A6246',
         cloud='#FFFFFF', cloud_op=.55, far='#C9B27A', mid='#A9A85A', near='#77823F', fg='#3A4526', sea=[(0, '#4FB3B8'), (1, '#1B6F7A')], sand='#EBD3A0',
         dune=['#F0C58A', '#D9A263', '#B07B45'], lake=[(0, '#9CC6CF'), (1, '#3C7C93')], rock='#9C8670', snow='#FFFFFF'),
]
HZ = 860  # horizon line


def g(x, y, s, body, flip=1):
    return f'<g transform="translate({x:.0f} {y:.0f}) scale({s * flip:.3f} {s:.3f})">{body}</g>'


def sky(v, hz=HZ, glow=True, sun_r=84, show_sun=True):
    sx, sy = v['sun_xy']
    out = f'<rect width="{W}" height="{hz + 40}" fill="url(#sky)"/>'
    if show_sun:
        out += sun(sx, sy, sun_r, '#FFF3C9' if v['name'] != 'sunset' else '#FFE5B8', 'sg') if glow else ''
    return out


def sky_defs(v):
    return vgrad('sky', v['sky']) + glow_def('sg', '#FFE7A8' if v['name'] != 'sunset' else '#FFC98B')


def cl(v, specs=((60, 330, 1.5), (560, 440, 1.2))):
    return clouds([(x, y, s, v['cloud_op'], 1, 1) for x, y, s in specs], v['cloud'])


def stars(n, seed, y_max=600):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.randint(10, 990)}" cy="{r.randint(20, y_max)}" r="{r.choice((1, 1.3, 1.8, 2.4))}" fill="#fff" opacity="{r.choice((.5, .7, .9))}"/>' for _ in range(n))


def pine(x, y, s, col):
    t = ''.join(f'<path d="M{-46 + i * 7} {-i * 44}L0 {-i * 44 - 80}L{46 - i * 7} {-i * 44}Z"/>' for i in range(3))
    return g(x, y, s, f'<g fill="{col}">{t}<rect x="-6" y="0" width="12" height="20"/></g>')


def reflect(body, y, op=.25):
    return f'<g transform="translate(0 {2 * y}) scale(1 -1)" opacity="{op}">{body}</g>'


def stripes(rows, color='#fff', op=.3):
    return ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="{color}" opacity="{op}"/>' for x, y, w in rows)


def motif_svg(key, v, x, base, h_target, flip=1):
    fn, h0, layer = M[key]
    sc = min(h_target / h0, 2.4)
    return g(x, base, sc, fn(v['c'], v['s'], v['d']), flip)


def stage(keys, v, cx, base, main_h=400, sec_h=210, spread=270):
    """Returns (back, front): back-layer motifs (mountains etc.) and front-layer motifs, positioned around cx."""
    keys = [k for k in keys if k in M]
    back = front = ''
    n_side = 0
    for i, k in enumerate(keys):
        layer = M[k][2]
        if i == 0:
            x, h = cx, main_h
        else:
            n_side += 1
            x = cx + (-1 if n_side % 2 else 1) * (spread + ((n_side - 1) // 2) * 140)
            h = sec_h
        flip = -1 if (i > 0 and i % 2 == 0) else 1
        s = motif_svg(k, v, x, base, h, flip)
        if layer == 'back':
            back += s
        else:
            front += s
    return back, front


def ground_band(v, y, color_key='near'):
    return f'<rect y="{y}" width="{W}" height="{H - y}" fill="{v[color_key]}"/>'


def wave_rows(v, y0):
    return stripes([(120, y0 + 50, 200), (580, y0 + 90, 260), (300, y0 + 170, 300), (640, y0 + 240, 240)], '#fff', .28 if v['name'] != 'sunset' else .16)


# ----------------------------------------------------------------------------------------------------------------
def bd_tropical(keys, v, rnd):
    defs = sky_defs(v) + vgrad('sea', v['sea'])
    back, front = stage(keys, v, 560, 862, 380, 190, 280)
    body = (sky(v) + cl(v) + hills([(-20, 850), (160, 800), (330, 836), (700, 820), (1020, 846)], 870, v['far'], .6) + back +
            f'<rect y="850" width="{W}" height="{H - 850}" fill="url(#sea)"/>' + wave_rows(v, 850) +
            f'<ellipse cx="560" cy="872" rx="250" ry="26" fill="{v["sand"]}"/><ellipse cx="560" cy="866" rx="210" ry="14" fill="#6FA862" opacity=".7"/>' + front +
            f'<path d="M-10 1100C200 1070 360 1130 520 1110C700 1090 840 1130 1010 1100V1250H-10Z" fill="{v["sand"]}"/>' +
            palm(110, 1040, 1.1, v['fg']) + palm(900, 1080, .95, v['fg'], -1) + palm(40, 1090, .8, v['fg']))
    return defs, body


def bd_desert(keys, v, rnd):
    defs = sky_defs(v)
    back, front = stage(keys, v, 500, 900, 400, 200, 300)
    d1, d2, d3 = v['dune']
    body = (sky(v, sun_r=96) + cl(v, ((60, 360, 1.4),)) + back +
            hills([(-20, 850), (260, 800), (560, 850), (1020, 800)], 920, d1) +
            hills([(-20, 905), (300, 880), (700, 915), (1020, 880)], 1250, d2) + front +
            hills([(-20, 1010), (360, 960), (720, 1030), (1020, 975)], 1250, d3) +
            hills([(-20, 1140), (400, 1100), (800, 1160), (1020, 1120)], 1250, v['fg']) +
            ''.join(f'<path d="M{x} 1010Q{x + 60} 970 {x + 130} 1012" fill="none" stroke="#fff" stroke-opacity=".15" stroke-width="3"/>' for x in (100, 520, 760)))
    return defs, body


def bd_savanna(keys, v, rnd):
    defs = sky_defs(v) + vgrad('gr', [(0, v['mid']), (1, v['fg'])])
    back, front = stage(keys, v, 500, 940, 380, 200, 300)
    grass = 'M0 1250V1170' + ''.join(f'L{x} {1130 - (x * 7 % 40)}L{x + 14} 1180' for x in range(10, 1000, 28)) + 'L1000 1170V1250Z'
    body = (sky(v, sun_r=100) + cl(v) + hills([(-20, 820), (200, 770), (420, 810), (760, 760), (1020, 800)], 860, v['far'], .7) + back +
            f'<rect y="840" width="{W}" height="{H - 840}" fill="url(#gr)"/>' + front +
            acacia(720, 925, .9, v['fg']) + acacia(170, 905, .55, v['fg']) + f'<path d="{grass}" fill="{v["fg"]}" opacity=".95"/>')
    return defs, body


def bd_alpine(keys, v, rnd):
    defs = sky_defs(v) + vgrad('mead', [(0, v['mid']), (1, v['near'])])
    back, front = stage(keys, v, 520, 960, 420, 230, 300)

    def range_(pts, col, snow=True):
        out = hills(pts, 900, col)
        return out
    peaks = ''
    if not any(M[k][2] == 'back' for k in keys):
        peaks += g(560, 880, 1.0, '<path d="M-380 0L-120 -250L-60 -300L-40 -420L0 -540L30 -470L70 -360L120 -300L200 -170L380 0Z" fill="' + v['far'] + '"/>'
                   '<path d="M0 -540L30 -470L70 -360L120 -300L200 -170L380 0H60L40 -200L18 -380Z" fill="' + v['rock'] + '"/>'
                   '<path d="M-40 -420L0 -540L30 -470L10 -440L-6 -470L-22 -430Z" fill="' + v['snow'] + '"/>')
    body = (sky(v, sun_r=70) + cl(v) + hills([(-20, 820), (160, 700), (300, 780), (480, 640), (700, 780), (860, 700), (1020, 790)], 900, v['far'], .8) + peaks + back +
            f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#mead)"/>' +
            hills([(-20, 960), (300, 925), (640, 975), (1020, 935)], 1250, v['mid']) + front +
            pine(80, 1010, 1.5, v['fg']) + pine(160, 1050, 1.1, v['fg']) + pine(900, 1020, 1.4, v['fg']) + pine(950, 1070, 1.0, v['fg']) +
            hills([(-20, 1180), (400, 1140), (800, 1190), (1020, 1160)], 1250, v['near']))
    return defs, body


def bd_steppe(keys, v, rnd):
    defs = sky_defs(v)
    back, front = stage(keys or ['ger'], v, 500, 930, 330, 200, 300)
    body = (sky(v, sun_r=62) + cl(v, ((40, 320, 2.0), (520, 400, 1.6), (250, 520, 1.3))) +
            hills([(-20, 820), (200, 740), (360, 790), (560, 720), (800, 780), (1020, 740)], 900, v['far'], .75) + back +
            hills([(-20, 860), (260, 820), (620, 850), (1020, 820)], 900, v['mid'], .9) +
            hills([(-20, 905), (300, 875), (700, 910), (1020, 885)], 1250, v['mid']) +
            hills([(-20, 1010), (360, 960), (720, 1020), (1020, 975)], 1250, v['near']) + front +
            hills([(-20, 1160), (400, 1120), (800, 1170), (1020, 1140)], 1250, v['fg']))
    return defs, body


def bd_boreal(keys, v, rnd):
    night = v['name'] == 'sunset'
    defs = sky_defs(v) + vgrad('lake', v['lake'])
    if night:
        defs = vgrad('sky', [(0, '#070B2E'), (1, '#24366E')]) + glow_def('sg', '#FFC98B') + vgrad('lake', [(0, '#1B2A59'), (1, '#0B1233')]) + '<filter id="au" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="26"/></filter>'
    back, front = stage(keys or ['cabin'], v, 360, 960, 260, 190, 300)
    r = random.Random(3)
    treeline = ''.join(pine(x, 880, r.uniform(1.2, 2.0), v['fg'] if not night else '#0B1A22') for x in range(-20, 1040, 70))
    au = ('<g filter="url(#au)" opacity=".6"><path d="M-60 440C160 300 360 520 560 380S880 300 1060 380" fill="none" stroke="#4DF0A8" stroke-width="64" stroke-linecap="round"/>'
          '<path d="M-60 540C180 420 380 600 600 480S900 420 1060 500" fill="none" stroke="#9B7BFF" stroke-width="40" stroke-linecap="round" opacity=".7"/></g>')
    body = (f'<rect width="{W}" height="900" fill="url(#sky)"/>' + (stars(90, 2, 700) + au if night else sun(v['sun_xy'][0], v['sun_xy'][1], 70, '#FFF3C9', 'sg') + cl(v)) +
            hills([(-20, 880), (200, 790), (420, 840), (700, 780), (1020, 850)], 900, v['far'] if not night else '#1C2850') + treeline +
            f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#lake)"/>' + reflect(treeline, 880, .3) + back + front +
            stripes([(300, 1000, 300), (400, 1080, 220), (240, 1160, 360)], '#fff', .2) +
            '<path d="M-10 1160C260 1130 420 1190 640 1160C820 1138 940 1170 1010 1150V1250H-10Z" fill="' + (v['fg'] if not night else '#05070F') + '"/>' +
            pine(880, 1130, 1.7, v['fg'] if not night else '#05070F') + pine(950, 1160, 1.3, v['fg'] if not night else '#05070F'))
    return defs, body


def bd_city(keys, v, rnd):
    defs = sky_defs(v) + vgrad('sea', v['sea'])
    r = random.Random(8)
    row = ''
    x = -10
    while x < 1010:
        w, h = r.randint(34, 72), r.randint(80, 300)
        col = v['s'] if v['name'] != 'day' else '#7C8FA6'
        row += f'<rect x="{x}" y="{870 - h}" width="{w}" height="{h}" fill="{col}"/>'
        row += ''.join(f'<rect x="{x + 6 + i * 14}" y="{870 - h + 10 + j * 20}" width="5" height="7" fill="#FFD98A" opacity=".{r.choice(("3", "5", "6"))}"/>'
                       for i in range(max(1, (w - 8) // 14)) for j in range(int((h - 16) / 20)) if r.random() < .4) if v['name'] != 'day' else ''
        x += w + 3
    back, front = stage(keys or ['skyline'], v, 500, 884, 440, 230, 300)
    body = (sky(v) + cl(v) + row + back + front.replace('', '') +
            f'<rect y="872" width="{W}" height="{H - 872}" fill="url(#sea)"/>' + stripes([(140, 930, 220), (620, 960, 260), (200, 1040, 300), (560, 1110, 240)], '#FFE9B8', .22) +
            f'<path d="M-10 1150C200 1120 420 1170 700 1140C860 1124 960 1146 1010 1140V1250H-10Z" fill="{v["fg"]}"/>')
    return defs, body


def bd_fjord(keys, v, rnd):
    defs = sky_defs(v) + vgrad('lake', v['sea'])
    back, front = stage(keys or ['cabin'], v, 250, 960, 220, 180, 280)
    left = f'<path d="M-10 420C80 440 150 560 230 700L360 880L-10 880Z" fill="{v["rock"]}"/><path d="M-10 480C70 490 130 600 200 740L300 880L-10 880Z" fill="{v["near"]}"/>'
    right = f'<path d="M1010 380C940 420 880 540 820 700L700 880L1010 880Z" fill="{v["rock"]}"/><path d="M1010 450C950 470 900 590 850 740L770 880L1010 880Z" fill="{v["near"]}"/>'
    body = (sky(v, sun_r=70) + hills([(280, 720), (400, 580), (470, 640), (540, 540), (650, 660), (740, 720)], 820, v['far'], .9) +
            '<path d="M470 640L540 540L600 610L560 620L540 590L510 630Z" fill="#fff" opacity=".8"/>' + cl(v, ((70, 340, 1.4), (600, 440, 1.2))) + left + right +
            f'<rect y="860" width="{W}" height="{H - 860}" fill="url(#lake)"/>' + stripes([(330, 940, 300), (400, 1010, 220), (300, 1100, 360)], '#fff', .2) + back + front +
            f'<path d="M-10 1130C220 1100 380 1180 620 1150C820 1126 940 1160 1010 1140V1250H-10Z" fill="{v["fg"]}"/>' + pine(900, 1100, 1.7, v['fg']) + pine(960, 1130, 1.3, v['fg']))
    return defs, body


def bd_volcanic(keys, v, rnd):
    defs = sky_defs(v) + vgrad('sea', v['sea'])
    keys = keys or ['cone']
    first_back = M[keys[0]][2] == 'back'
    back, front = stage(keys if first_back else ['cone'] + keys, v, 500, 880, 470, 200, 300)
    body = (sky(v, sun_r=70) + cl(v) + hills([(-20, 840), (200, 800), (420, 830), (800, 790), (1020, 830)], 880, v['far'], .6) + back +
            f'<rect y="868" width="{W}" height="{H - 868}" fill="url(#sea)"/>' + wave_rows(v, 868) +
            f'<path d="M-10 1000C160 960 360 1040 560 1010C760 982 900 1030 1010 1000V1250H-10Z" fill="{v["fg"]}"/>' + front +
            f'<path d="M-10 1130C200 1100 420 1160 700 1130C860 1112 960 1140 1010 1130V1250H-10Z" fill="#0B0A12" opacity=".9"/>')
    return defs, body


def bd_rainforest(keys, v, rnd):
    defs = sky_defs(v) + vgrad('river', v['lake'])
    keys = keys or []
    back, front = stage(keys, v, 500, 900, 400, 220, 280)
    r = random.Random(12)

    def canopy(y0, col, n, size):
        return ''.join(f'<ellipse cx="{x}" cy="{y0 - r.randint(0, 30)}" rx="{r.randint(size, size + 50)}" ry="{r.randint(size - 10, size + 20)}" fill="{col}"/>' for x in range(-20, 1040, int(1000 / n)))
    v = dict(v)
    if v['name'] == 'day':
        v.update(mid='#5E9B52', near='#3E7A3A', fg='#2A5E2D', far='#8FB8C8')
    elif v['name'] == 'golden':
        v.update(mid='#7BA05B', near='#4E7A3B', fg='#2F5A2F', far='#B5B77A')
    body = (sky(v, glow=True, sun_r=70) + cl(v) + hills([(-20, 820), (240, 740), (480, 800), (760, 720), (1020, 790)], 900, v['far'], .75) +
            f'<ellipse cx="500" cy="840" rx="600" ry="70" fill="#fff" opacity=".28"/>' + back + canopy(900, v['mid'], 9, 70) +
            f'<rect y="900" width="{W}" height="{H - 900}" fill="url(#river)"/>' + stripes([(200, 960, 260), (540, 1010, 280), (180, 1100, 320)], '#fff', .2) + canopy(980, v['near'], 7, 80) + front +
            canopy(1230, v['fg'], 6, 110) + palm(90, 1180, 1.0, v['fg']) + palm(900, 1190, .9, v['fg'], -1))
    return defs, body


def bd_mediterranean(keys, v, rnd):
    defs = sky_defs(v) + vgrad('sea', v['sea'])
    keys_all = keys or []
    keys = keys or []
    back, front = stage(keys, v, 640, 940, 330, 190, 260)
    r = random.Random(21)
    houses = ''
    for row in range(6):
        y = 700 + row * 46
        x = 20 + row * 56
        while x < 640 - row * 14:
            w, h = r.randint(70, 108), r.randint(42, 60)
            roof = '#C8593A' if v['name'] != 'sunset' else '#6E3550'
            wall = '#FFFFFF' if v['name'] != 'sunset' else '#E8C4C0'
            houses += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}"/><rect x="{x + w * .72}" y="{y}" width="{w * .28}" height="{h}" fill="#000" opacity=".1"/>'
                       f'<rect x="{x + 10}" y="{y + 14}" width="11" height="18" fill="#2D6CB5"/>')
            if r.random() < .22 and 'nodome' not in keys_all:
                houses += f'<path d="M{x + 6} {y}C{x + 6} {y - 38} {x + w - 6} {y - 38} {x + w - 6} {y}Z" fill="#2D6CB5"/>'
            elif r.random() < .3:
                houses += f'<path d="M{x - 4} {y}L{x + w / 2} {y - 22}L{x + w + 4} {y}Z" fill="{roof}"/>'
            x += w + r.randint(6, 16)
    body = (sky(v, sun_r=70) + cl(v) + hills([(-20, 600), (200, 640), (400, 700), (700, 780), (1020, 840)], 880, v['far'], .4) +
            f'<rect y="820" width="{W}" height="{H - 820}" fill="url(#sea)"/>' + wave_rows(v, 820) + back +
            f'<path d="M-10 640C140 650 260 700 360 790C440 870 560 940 700 990L1010 1040V1250H-10Z" fill="{v["mid"] if v["name"] != "day" else "#B58A6A"}"/>' + houses + front +
            ''.join(f'<g transform="translate({x} {y})"><ellipse cx="0" cy="-60" rx="14" ry="60" fill="{v["fg"]}"/></g>' for x, y in ((80, 960), (110, 975), (880, 1130))) +
            g(790, 1040, 1.0, M['sailboat'][0](v['c'], v['s'], v['d'])))
    return defs, body


def bd_farmland(keys, v, rnd):
    defs = sky_defs(v) + vgrad('field', [(0, v['mid']), (1, v['near'])])
    back, front = stage(keys or ['windmill'], v, 500, 900, 360, 210, 290)
    cols = [v['mid'], v['near'], '#C9B55A', '#8BB04F']
    r = random.Random(4)
    fields = ''.join(f'<path d="M{-100 + i * 220} 1250L{400 + (i - 2) * 80} 850H{600 + (i - 2) * 80}L{120 + i * 220} 1250Z" fill="{cols[i % 4]}" opacity=".9"/>' for i in range(8))
    body = (sky(v, sun_r=70) + cl(v, ((40, 340, 1.8), (560, 440, 1.5), (250, 560, 1.2))) + hills([(-20, 846), (300, 826), (700, 840), (1020, 828)], 900, v['far'], .8) + back +
            f'<rect y="846" width="{W}" height="{H - 846}" fill="url(#field)"/>' + fields + front +
            f'<path d="M-10 880L1010 880" stroke="{v["fg"]}" stroke-width="8" opacity=".6"/>' +
            hills([(-20, 1180), (400, 1140), (800, 1190), (1020, 1160)], 1250, v['fg']))
    return defs, body


def bd_oldtown(keys, v, rnd):
    defs = sky_defs(v) + vgrad('river', v['lake'])
    r = random.Random(11)
    roofs = ''
    x = -10
    wall = v['s'] if v['name'] != 'day' else '#B9A8A0'
    roof = v['c'] if v['name'] == 'sunset' else '#6E5A5A'
    while x < 1010:
        w, h = r.randint(70, 120), r.randint(70, 130)
        roofs += f'<rect x="{x}" y="{880 - h}" width="{w}" height="{h}" fill="{wall}"/><path d="M{x - 4} {880 - h}L{x + 12} {880 - h - 28}H{x + w - 12}L{x + w + 4} {880 - h}Z" fill="{roof}"/>'
        roofs += ''.join(f'<rect x="{x + 12 + i * 22}" y="{880 - h + 20}" width="8" height="14" fill="#FFD98A" opacity=".{r.choice(("5", "8"))}"/>' for i in range(max(1, (w - 24) // 22)))
        x += w + 4
    back, front = stage(keys or ['medieval'], v, 500, 884, 480, 240, 330)
    body = (sky(v, sun_r=74) + (stars(40, 3, 380) if v['name'] == 'sunset' else '') + cl(v) + roofs + back + front +
            f'<rect y="880" width="{W}" height="{H - 880}" fill="url(#river)"/>' + stripes([(640, 930, 150), (660, 966, 120), (680, 1002, 90)], '#FFE9B8', .22) +
            f'<path d="M-10 1040C200 1010 420 1050 700 1030C860 1020 960 1040 1010 1036V1250H-10Z" fill="{v["fg"]}"/>' +
            ''.join(f'<g><rect x="{x}" y="900" width="5" height="140" fill="#0F0C20" opacity=".8"/><circle cx="{x + 2.5}" cy="900" r="11" fill="#FFD98A"/></g>' for x in (120, 380, 660, 880)))
    return defs, body


def bd_arctic(keys, v, rnd):
    defs = (vgrad('sky', [(0, '#070B2E'), (1, '#24366E')]) + vgrad('sea', [(0, '#1B2A59'), (1, '#0B1233')]) +
            '<filter id="au" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="26"/></filter>')
    back, front = stage(keys or ['icebergs'], v, 500, 880, 340, 220, 290)
    au = ('<g filter="url(#au)" opacity=".6"><path d="M-60 440C160 300 360 520 560 380S880 300 1060 380" fill="none" stroke="#4DF0A8" stroke-width="64" stroke-linecap="round"/>'
          '<path d="M-60 540C180 420 380 600 600 480S900 420 1060 500" fill="none" stroke="#9B7BFF" stroke-width="40" stroke-linecap="round" opacity=".7"/></g>')
    body = (f'<rect width="{W}" height="880" fill="url(#sky)"/>' + stars(110, 5, 760) + au + hills([(-20, 880), (200, 820), (420, 850), (800, 810), (1020, 850)], 900, '#1C2850') + back +
            f'<rect y="878" width="{W}" height="{H - 878}" fill="url(#sea)"/>' + front + stripes([(200, 960, 240), (560, 1010, 280), (240, 1110, 340)], '#BFD6EA', .18) +
            '<path d="M-10 1150C200 1120 420 1170 700 1140C860 1124 960 1146 1010 1140V1250H-10Z" fill="#05070F"/>')
    return defs, body


BACKDROPS = {
    'tropical-island': bd_tropical, 'desert': bd_desert, 'savanna': bd_savanna, 'alpine': bd_alpine, 'steppe': bd_steppe,
    'boreal-forest': bd_boreal, 'city-skyline': bd_city, 'fjord-coast': bd_fjord, 'volcanic': bd_volcanic, 'rainforest': bd_rainforest,
    'mediterranean': bd_mediterranean, 'farmland': bd_farmland, 'old-town': bd_oldtown, 'arctic': bd_arctic,
}
