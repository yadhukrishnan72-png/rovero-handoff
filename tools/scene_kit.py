"""Landmark / feature motifs for destination scenes.

Every motif is a function (c, s, d) -> svg fragment with its origin at the centre of its base (y grows downward, so the
structure is drawn with negative y). c = main colour, s = shade, d = detail colour. M[key] = (fn, nominal_height, layer).
layer 'back' motifs (mountains, volcanoes, karst) are drawn behind the ground band, 'front' motifs on top of it.
"""
import math
import random

M = {}


def motif(key, h0, layer='front'):
    def deco(fn):
        M[key] = (fn, h0, layer)
        return fn
    return deco


def P(d, f, extra=''):
    return f'<path d="{d}" fill="{f}"{extra}/>'


def R(x, y, w, h, f, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}"' + (f' rx="{rx}"' if rx else '') + '/>'


def C(x, y, r, f):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}"/>'


def E(x, y, rx, ry, f, extra=''):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{f}"{extra}/>'


def dome(cx, base, r, h, f):
    return P(f'M{cx - r} {base}C{cx - r} {base - h} {cx + r} {base - h} {cx + r} {base}Z', f)


def spire(cx, base, w, h, f):
    return P(f'M{cx - w / 2} {base}L{cx} {base - h}L{cx + w / 2} {base}Z', f)


def tower(cx, base, w, h, f, top='flat'):
    out = R(cx - w / 2, base - h, w, h, f)
    if top == 'point':
        out += spire(cx, base - h, w * 1.1, w * 1.3, f)
    elif top == 'dome':
        out += dome(cx, base - h, w / 2, w * .8, f)
    return out


def arches(x, y, w, h, n, f):
    aw = w / n
    return ''.join(P(f'M{x + i * aw + aw * .18} {y + h}V{y + h * .4}Q{x + i * aw + aw * .5} {y - h * .1} {x + i * aw + aw * .82} {y + h * .4}V{y + h}Z', f)
                   for i in range(n))


def windows(x, y, w, h, nx, ny, f):
    return ''.join(R(x + (i + .5) * w / nx - 3, y + (j + .5) * h / ny - 4, 6, 8, f)
                   for i in range(nx) for j in range(ny))


# ----------------------------------------------------------------------------------------------------------------
# Skyscrapers and modern towers
# ----------------------------------------------------------------------------------------------------------------
@motif('burj', 600)
def burj(c, s, d):
    body = 'M-34 0L-30 -200H-24V-330H-16V-440H-8V-520L0 -610L8 -520V-440H16V-330H24V-200H30L34 0Z'
    return P(body, c) + P('M0 -610L8 -520V-440H16V-330H24V-200H30L34 0H0Z', s)


@motif('flame', 440)
def flame(c, s, d):
    return (P('M-120 0C-150 -140 -100 -290 -60 -360C-40 -240 -50 -100 -50 0Z', s) + P('M-40 0C-70 -190 -20 -340 30 -440C60 -300 60 -120 60 0Z', c)
            + P('M70 0C50 -120 90 -240 130 -310C150 -200 140 -80 140 0Z', s))


@motif('petronas', 480)
def petronas(c, s, d):
    def tw(x):
        return (P(f'M{x - 44} 0V-250L{x - 36} -320L{x - 26} -380L{x - 14} -420L{x} -470L{x + 14} -420L{x + 26} -380L{x + 36} -320L{x + 44} -250V0Z', c)
                + P(f'M{x} -470L{x + 14} -420L{x + 26} -380L{x + 36} -320L{x + 44} -250V0H{x}Z', s))
    return tw(-62) + tw(62) + R(-22, -240, 44, 16, s)


@motif('marina', 330)
def marina(c, s, d):
    t = ''.join(P(f'M{x - 40} 0L{x - 30 + i * 6} -250H{x + 30 + i * 6}L{x + 40} 0Z', c if i != 1 else s) for i, x in enumerate((-100, 0, 100)))
    return t + P('M-170 -262H190C210 -262 214 -276 196 -286L-150 -286C-170 -286 -180 -270 -170 -262Z', c) + R(-170, -266, 360, 8, s)


@motif('kuwait', 420)
def kuwait(c, s, d):
    return (P('M-70 0L-62 -250L-56 -300L-54 -430L-50 -300L-44 -250L-38 0Z', c) + E(-54, -270, 26, 30, s) + E(-54, -330, 14, 16, c)
            + P('M30 0L36 -200L40 -300L44 -200L50 0Z', c) + E(40, -230, 14, 18, s) + P('M-2 0L2 -360L6 0Z', s))


@motif('kingdom', 330)
def kingdom(c, s, d):
    return (P('M-70 0V-300Q-70 -330 -40 -330H40Q70 -330 70 -300V0Z', c) + P('M-34 -330V-250Q0 -190 34 -250V-330Z', d)
            + P('M0 -330H40Q70 -330 70 -300V0H0Z', s))


@motif('skyline', 360)
def skyline(c, s, d):
    r = random.Random(5)
    out = ''
    x = -240
    while x < 240:
        w, h = r.randint(36, 70), r.randint(100, 330)
        out += R(x, -h, w, h, c if r.random() < .6 else s) + windows(x + 4, -h + 8, w - 8, h - 16, max(1, int(w / 14)), max(1, int(h / 22)), d)
        if r.random() < .3:
            out += R(x + w / 2 - 1.5, -h - 44, 3, 44, s)
        x += w + 4
    return out


@motif('seoul', 460)
def seoul(c, s, d):
    return (P('M-24 0L-10 -330H10L24 0Z', c) + E(0, -340, 36, 14, c) + E(0, -350, 28, 10, s) + R(-2, -470, 4, 120, s)
            + P('M-110 0Q-60 -60 0 -40Q60 -60 110 0Z', s))


@motif('taipei', 520)
def taipei(c, s, d):
    out = ''
    for i in range(8):
        y = -i * 52
        out += P(f'M{-30 - (i % 2) * 6} {y}L{-38} {y - 52}H38L{30 + (i % 2) * 6} {y}Z', c if i % 2 else s)
    return out + P('M-36 -420L0 -480L36 -420Z', s) + R(-2, -540, 4, 70, s)


@motif('hk', 380)
def hk(c, s, d):
    out = skyline(c, s, d)
    return out + R(-14, -420, 28, 420, c) + R(-2, -470, 4, 50, s) + P('M-14 -420H14L8 -440H-8Z', s)


@motif('macao', 300)
def macao(c, s, d):
    return (R(-130, -260, 260, 260, c) + P('M-130 -260L0 -330L130 -260Z', s) + R(-30, -200, 60, 200, d)
            + ''.join(R(x, -230, 30, 40, s) for x in (-100, -60, 60, 100)) + P('M-60 0V-20H60V0Z', s) + ''.join(R(-70 + i * 14, -i * 3, 140 - i * 28, 3, d) for i in range(4)))


@motif('baiterek', 400)
def baiterek(c, s, d):
    return (P('M-16 0L-6 -260H6L16 0Z', c) + C(0, -300, 52, s) + P('M-56 -300Q0 -380 56 -300Q0 -340 -56 -300Z', c) + R(-2, -420, 4, 70, c))


@motif('doha', 420)
def doha(c, s, d):
    return (R(-170, -150, 54, 150, s) + R(-110, -230, 50, 230, c) + P('M-50 0L0 -420L50 0Z', c) + P('M0 -420L50 0H0Z', s)
            + R(60, -260, 50, 260, c) + R(112, -180, 54, 180, s))


# ----------------------------------------------------------------------------------------------------------------
# Historic buildings
# ----------------------------------------------------------------------------------------------------------------
@motif('bigben', 500)
def bigben(c, s, d):
    return (R(-70, -120, 140, 120, c) + R(-36, -330, 72, 210, c) + R(-42, -344, 84, 16, s) + spire(0, -344, 84, 90, s) + R(-2, -470, 4, 36, s)
            + C(0, -280, 24, d) + C(0, -280, 18, '#F6EBD0') + R(-36, -330, 20, 210, s) + windows(-30, -110, 140, 80, 5, 1, d))


@motif('sagrada', 560)
def sagrada(c, s, d):
    out = R(-170, -170, 340, 170, c) + arches(-160, -150, 320, 120, 6, d)
    for x, h in ((-140, 360), (-70, 440), (70, 440), (140, 360)):
        out += P(f'M{x - 22} -170L{x - 12} {-h}Q{x} {-h - 60} {x + 12} {-h}L{x + 22} -170Z', c) + P(f'M{x} {-h - 40}L{x + 12} {-h}L{x + 22} -170H{x}Z', s)
    return out + P('M-30 -170L-12 -520Q0 -580 12 -520L30 -170Z', s)


@motif('brandenburg', 300)
def brandenburg(c, s, d):
    out = R(-170, -30, 340, 30, s) + R(-190, -240, 380, 22, c) + R(-170, -262, 340, 26, s)
    out += ''.join(R(x - 14, -218, 28, 188, c) for x in (-150, -90, -30, 30, 90, 150))
    out += R(-40, -310, 80, 48, c) + P('M-34 -310L0 -350L34 -310Z', s) + E(0, -330, 22, 10, d)
    return out


@motif('colosseum', 260)
def colosseum(c, s, d):
    out = P('M-230 0L-210 -230L210 -230L230 0Z', c) + P('M60 0L130 -230L210 -230L230 0Z', s)
    for i, y in enumerate((-60, -120, -180)):
        out += arches(-200, y, 400, 46, 12, d)
    return out + P('M-130 -230L-90 -270L40 -270L80 -250L210 -230Z', c)


@motif('onion', 480)
def onion(c, s, d):
    cols = ('#C8102E', '#2E8B57', '#F2C230', '#3B6FD4', '#C8102E')
    out = R(-170, -150, 340, 150, '#B5543C') + windows(-160, -140, 320, 130, 8, 2, '#3A2A28')
    out += P('M-18 -150L-12 -420L0 -480L12 -420L18 -150Z', '#2E8B57')
    for i, x in enumerate((-130, -70, 70, 130)):
        out += R(x - 22, -250, 44, 100, '#E8DCC4') + P(f'M{x - 26} -250Q{x - 40} -310 {x} -380Q{x + 40} -310 {x + 26} -250Z', cols[i])
    return out + P('M-26 -250Q-44 -330 0 -400Q44 -330 26 -250Z', cols[2])


@motif('cappadocia', 560)
def cappadocia(c, s, d):
    out = ''
    for x, h in ((-150, 160), (-60, 240), (50, 200), (140, 130)):
        out += P(f'M{x - 40} 0L{x - 16} {-h}H{x + 16}L{x + 40} 0Z', c) + P(f'M{x - 26} {-h}Q{x} {-h - 36} {x + 26} {-h}Z', d) + P(f'M{x} {-h}H{x + 16}L{x + 40} 0H{x}Z', s)
    for bx, by, col in ((-110, -380, '#E63946'), (30, -450, '#FFC300'), (130, -340, '#3A86FF')):
        out += E(bx, by, 36, 44, col) + P(f'M{bx - 26} {by + 28}L{bx - 10} {by + 66}H{bx + 10}L{bx + 26} {by + 28}Z', '#6B4A35') + R(bx - 8, by + 66, 16, 10, '#6B4A35')
    return out


@motif('greatwall', 300)
def greatwall(c, s, d):
    out = P('M-340 0L-250 -60L-130 -110L-30 -90L60 -170L190 -190L330 -260L340 -230L200 -160L70 -140L-20 -60L-130 -80L-240 -30L-330 20Z', c)
    for x, y in ((-250, -60), (-90, -105), (60, -170), (250, -224)):
        out += R(x - 20, y - 52, 40, 52, s) + R(x - 26, y - 62, 52, 12, c) + ''.join(R(x - 26 + i * 18, y - 74, 10, 12, c) for i in range(3))
    return out


@motif('prang', 540)
def prang(c, s, d):
    out = R(-150, -40, 300, 40, s)
    out += P('M-52 -40L-44 -200L-30 -300L-14 -400L0 -540L14 -400L30 -300L44 -200L52 -40Z', c) + P('M0 -540L14 -400L30 -300L44 -200L52 -40H0Z', s)
    for x in (-120, 120):
        out += P(f'M{x - 26} -40L{x - 16} -150L{x} -240L{x + 16} -150L{x + 26} -40Z', c)
    return out + ''.join(R(-50 + 6 * i, -120 - i * 60, 100 - 12 * i, 5, d) for i in range(4))


@motif('angkor', 480)
def angkor(c, s, d):
    out = R(-250, -40, 500, 40, s) + R(-200, -90, 400, 50, c) + R(-150, -140, 300, 50, s)
    for x, h in ((-130, 260), (-65, 340), (0, 440), (65, 340), (130, 260)):
        out += P(f'M{x - 24} -140L{x - 22} {-h + 70}Q{x - 26} {-h + 20} {x} {-h}Q{x + 26} {-h + 20} {x + 22} {-h + 70}L{x + 24} -140Z', c) + P(f'M{x} {-h}Q{x + 26} {-h + 20} {x + 22} {-h + 70}L{x + 24} -140H{x}Z', s)
    return out


@motif('sigiriya', 420)
def sigiriya(c, s, d):
    return (P('M-250 0L-210 -200L-170 -280L-130 -330L-90 -350H110L150 -330L190 -260L250 0Z', c) + P('M40 -350H110L150 -330L190 -260L250 0H60Z', s)
            + R(-110, -372, 190, 22, '#4E7A47') + ''.join(C(-90 + i * 36, -378, 16, '#3E6A3C') for i in range(5)))


@motif('petra', 420)
def petra(c, s, d):
    out = P('M-220 0V-380Q0 -440 220 -380V0Z', c) + P('M0 -420Q120 -400 220 -380V0H0Z', s)
    out += R(-80, -300, 160, 300, '#D8A07A') + ''.join(R(x - 9, -260, 18, 200, c) for x in (-60, -20, 20, 60))
    return out + P('M-90 -260H90L0 -330Z', c) + R(-90, -270, 180, 12, s) + R(-20, -90, 40, 90, d) + C(0, -340, 14, c)


@motif('registan', 340)
def registan(c, s, d):
    out = ''
    for x, w, h in ((-190, 120, 220), (0, 150, 260), (190, 120, 220)):
        out += R(x - w / 2, -h, w, h, '#D9BF92') + P(f'M{x - w * .3} 0V{-h * .6}Q{x} {-h * .9} {x + w * .3} {-h * .6}V0Z', '#2F6FB5')
        out += dome(x, -h, w * .28, w * .5, '#2FA3B5')
    return out + R(-250, -10, 500, 10, '#B8A07A')


@motif('goldmosque', 400)
def goldmosque(c, s, d):
    return (R(-130, -120, 260, 120, c) + arches(-120, -100, 240, 80, 5, d) + dome(0, -120, 80, 140, '#F2C230') + R(-3, -280, 6, 36, '#F2C230')
            + R(150, -300, 26, 300, c) + dome(163, -300, 18, 40, '#F2C230'))


@motif('mudmosque', 360)
def mudmosque(c, s, d):
    c, s, d = '#C9A27A', '#A57B58', '#6B4A35'
    out = R(-170, -170, 340, 170, c) + R(-170, -170, 120, 170, s)
    for x, h in ((-120, 280), (0, 330), (120, 280)):
        out += P(f'M{x - 26} -170L{x - 18} {-h}H{x + 18}L{x + 26} -170Z', c) + R(x - 22, -h - 14, 44, 14, s)
        out += ''.join(R(x + (-26 if k % 2 else 24), -h + 30 + k * 30, 12, 4, d) for k in range(5))
    return out + P('M-30 0V-100Q0 -140 30 -100V0Z', d)


@motif('minaret', 400)
def minaret(c, s, d):
    c, s, d = '#C9A27A', '#A57B58', '#6B4A35'
    out = P('M-50 0L-30 -280L30 -280L50 0Z', c) + P('M0 -280H30L50 0H0Z', s)
    out += ''.join(R(-34 + (k % 2) * 6, -60 - k * 52, 68 - (k % 2) * 12, 6, d) for k in range(5))
    return out + P('M-30 -280L0 -400L30 -280Z', c)


@motif('shibam', 400)
def shibam(c, s, d):
    c, s, d = '#C9A27A', '#A57B58', '#6B4A35'
    r = random.Random(9)
    out = ''
    x = -240
    while x < 220:
        w, h = r.randint(44, 70), r.randint(200, 380)
        out += R(x, -h, w, h, c if r.random() < .6 else s) + ''.join(R(x + 8, -h + 16 + k * 36, 8, 12, d) + R(x + w - 16, -h + 16 + k * 36, 8, 12, d) for k in range(int(h / 36) - 1))
        x += w + 6
    return out


@motif('kasbah', 330)
def kasbah(c, s, d):
    c, s, d = '#C9A27A', '#A57B58', '#6B4A35'
    out = R(-210, -110, 420, 110, c)
    for x, h in ((-170, 250), (-40, 190), (110, 280), (190, 180)):
        out += R(x - 34, -h, 68, h, c if x < 100 else s) + R(x - 40, -h - 14, 80, 14, s) + ''.join(R(x - 22 + k * 22, -h - 24, 12, 10, s) for k in range(3))
        out += ''.join(R(x - 6, -h + 30 + k * 40, 12, 16, d) for k in range(max(1, int(h / 60))))
    return out + P('M-30 0V-70Q0 -100 30 -70V0Z', d)


@motif('leptis', 240)
def leptis(c, s, d):
    out = ''.join(R(x - 12, -200, 24, 200, c) + R(x - 18, -212, 36, 14, s) + R(x - 18, -12, 36, 12, s) for x in (-150, -80, -10, 60, 130))
    return out + R(-170, -230, 320, 20, s) + P('M60 -230H130Q130 -300 95 -330Q60 -300 60 -230Z', c)


@motif('ennedi', 300, 'back')
def ennedi(c, s, d):
    c, s = '#B5835A', '#8A5A3C'
    return (P('M-300 0V-150Q-300 -260 -190 -280Q-80 -300 -60 -190Q-40 -120 0 -120Q40 -120 60 -190Q80 -300 190 -280Q300 -260 300 -150V0Z', c)
            + P('M0 -120Q40 -120 60 -190Q80 -300 190 -280Q300 -260 300 -150V0H80Q90 -80 0 -90Z', s))


@motif('meroe', 220)
def meroe(c, s, d):
    return ''.join(P(f'M{x - w / 2} 0L{x} {-h}L{x + w / 2} 0Z', c) + P(f'M{x} {-h}L{x + w / 2} 0H{x}Z', s) for x, w, h in ((-110, 110, 170), (10, 130, 210), (130, 90, 150)))


@motif('ziggurat', 260)
def ziggurat(c, s, d):
    out = ''.join(R(-190 + i * 40, -i * 62 - 62, 380 - i * 80, 62, c if i % 2 == 0 else s) for i in range(4))
    return out + P('M-30 0L-10 -190H10L30 0Z', d)


@motif('dubrovnik', 260)
def dubrovnik(c, s, d):
    r = random.Random(3)
    out = R(-300, -90, 600, 90, c) + ''.join(R(-300 + i * 24, -102, 14, 12, c) for i in range(25))
    for x in (-250, -20, 220):
        out += R(x - 36, -200, 72, 200, c) + P(f'M{x - 42} -200H{x + 42}L{x + 30} -250H{x - 30}Z', '#C8593A')
    for i in range(9):
        x = -260 + i * 62 + r.randint(-6, 6)
        out += R(x, -150 - r.randint(0, 40), 44, 70, '#E8DCC4') + P(f'M{x - 4} -150H{x + 48}L{x + 40} -178H{x + 4}Z', '#C8593A')
    return out


@motif('mostar', 260)
def mostar(c, s, d):
    return (P('M-230 -40H-170Q0 -250 170 -40H230V10H-230Z', c) + P('M-130 -40Q0 -190 130 -40Q0 -150 -130 -40Z', d)
            + R(-250, -200, 54, 180, c) + P('M-254 -200L-223 -260L-192 -200Z', s) + R(196, -170, 54, 150, c) + P('M192 -170L223 -230L254 -170Z', s))


@motif('prague', 420)
def prague(c, s, d):
    out = R(-260, -60, 520, 60, s)
    for x, h, w in ((-120, 360, 36), (-30, 420, 40), (80, 340, 34), (160, 250, 30), (-190, 220, 28)):
        out += R(x - w / 2, -h, w, h - 40, c) + spire(x, -h, w * 1.4, w * 2.6, d) + R(x - w / 2 - 6, -h * .6, w + 12, 8, s)
    out += R(-250, -180, 130, 130, c) + R(100, -170, 150, 120, c)
    return out + arches(-250, -30, 500, 30, 8, d)


@motif('medieval', 380)
def medieval(c, s, d):
    out = R(-270, -90, 540, 90, c)
    for x, h, w in ((-210, 280, 56), (-90, 340, 60), (40, 250, 54), (160, 320, 58), (250, 200, 46)):
        out += R(x - w / 2, -h, w, h - 40, c) + spire(x, -h, w * 1.3, w * 1.9, '#B5543C') + R(x - 6, -h * .6, 12, 18, d)
    return out + ''.join(R(-270 + i * 22, -102, 12, 14, c) for i in range(25))


@motif('trakai', 260)
def trakai(c, s, d):
    out = E(0, 14, 250, 22, '#4E7A47') + R(-160, -130, 320, 130, '#B5543C') + R(-160, -130, 120, 130, '#8C3F2E')
    for x, h in ((-150, 230), (150, 220), (0, 300)):
        out += R(x - 34, -h, 68, h, '#B5543C') + P(f'M{x - 42} -{h}L{x} -{h + 70}L{x + 42} -{h}Z', '#7A2E22')
    return out + ''.join(R(x, -100, 10, 16, d) for x in (-110, -60, 50, 100))


@motif('castle', 340)
def castle(c, s, d):
    out = R(-190, -110, 380, 110, c) + R(-190, -110, 130, 110, s)
    for x, h, w in ((-150, 260, 50), (0, 330, 64), (150, 240, 50)):
        out += R(x - w / 2, -h, w, h, c) + spire(x, -h, w * 1.3, w * 1.5, d) + R(x - 5, -h + 40, 10, 18, s)
    return out + ''.join(R(-190 + i * 24, -122, 14, 12, c) for i in range(16)) + P('M-26 0V-70Q0 -100 26 -70V0Z', d)


@motif('parliament', 300)
def parliament(c, s, d):
    out = R(-290, -110, 580, 110, c) + arches(-280, -90, 560, 70, 18, s)
    out += R(-60, -190, 120, 90, c) + dome(0, -190, 50, 110, c) + spire(0, -290, 20, 70, s)
    for x in (-230, -140, 140, 230):
        out += spire(x, -110, 36, 130, s) + R(x - 14, -110, 28, 12, c)
    return out


@motif('belem', 300)
def belem(c, s, d):
    out = R(-110, -70, 220, 70, c) + R(-70, -230, 140, 160, c) + R(-70, -230, 50, 160, s) + R(-84, -250, 168, 22, c)
    out += ''.join(P(f'M{x - 14} -250Q{x} -300 {x + 14} -250Z', s) for x in (-70, 70)) + ''.join(R(x, -190, 16, 26, d) for x in (-44, 30))
    out += R(-120, -30, 240, 8, d)
    return out + dome(0, -250, 36, 56, s)


@motif('valletta', 300)
def valletta(c, s, d):
    out = R(-290, -100, 580, 100, c) + arches(-280, -80, 560, 50, 14, d)
    r = random.Random(7)
    for i in range(9):
        x = -270 + i * 62
        h = r.randint(70, 130)
        out += R(x, -100 - h, 50, h, '#E3CFA4' if i % 2 else '#D8BD8C') + R(x + 12, -100 - h + 20, 10, 18, d)
    return out + dome(40, -230, 58, 100, '#8FB2C9') + R(36, -354, 8, 34, c) + R(-160, -300, 40, 200, '#E3CFA4') + spire(-140, -300, 46, 60, '#C8593A')


@motif('gibraltar', 420, 'back')
def gibraltar(c, s, d):
    return (P('M-380 0L-330 -70L-200 -200L-100 -300L-10 -400L40 -370L120 -300L220 -200L380 0Z', c) + P('M-10 -400L40 -370L120 -300L220 -200L380 0H20Q10 -200 -10 -400Z', s))


@motif('stpeters', 380)
def stpeters(c, s, d):
    out = R(-210, -120, 420, 120, c) + arches(-200, -100, 400, 70, 14, s) + R(-110, -210, 220, 90, c) + R(-60, -250, 120, 40, s)
    out += dome(0, -250, 62, 110, c) + R(-8, -392, 16, 36, s) + R(-3, -416, 6, 24, d)
    return out + ''.join(R(x - 8, -200, 16, 80, d) for x in (-84, -40, 40, 84))


@motif('stsava', 330)
def stsava(c, s, d):
    out = R(-130, -150, 260, 150, c) + dome(0, -150, 100, 130, '#FFFFFF') + R(-100, -150, 200, 14, s) + R(-3, -310, 6, 50, '#E8B93A') + R(-14, -296, 28, 6, '#E8B93A')
    out += ''.join(P(f'M{x - 14} -150V-190Q{x} -210 {x + 14} -190V-150Z', d) for x in (-80, -30, 30, 80))
    return out + dome(-108, -150, 36, 60, c) + dome(108, -150, 36, 60, c)


@motif('lighthouse', 280)
def lighthouse(c, s, d):
    return (P('M-30 0L-18 -200H18L30 0Z', '#F4F1EA') + P('M-24 -60L-21 -90H21L24 -60Z', '#C8102E') + P('M-20 -130L-18 -160H18L20 -130Z', '#C8102E')
            + R(-24, -216, 48, 16, d) + R(-14, -250, 28, 34, '#FFE9A0') + P('M-24 -250H24L0 -288Z', '#C8102E') + P('M-40 0H40L30 -18H-30Z', s))


@motif('church_onion', 360)
def church_onion(c, s, d):
    return (R(-60, -130, 120, 130, '#F4EEDC') + P('M-70 -130L0 -190L70 -130Z', '#B5543C') + R(-26, -280, 52, 150, '#F4EEDC')
            + P('M-32 -280Q-44 -330 0 -380Q44 -330 32 -280Z', '#2E8B57') + R(-2, -420, 4, 44, '#E8B93A') + P('M-14 0V-50Q0 -76 14 -50V0Z', '#6B4A35') + R(-10, -250, 20, 34, d))


@motif('cliff_monastery', 360, 'back')
def cliff_monastery(c, s, d):
    out = P('M-240 0L-200 -250L-130 -380L-60 -400L-10 -350L-30 -150L-20 0Z', '#8C7B6A') + P('M-60 -400L-10 -350L-30 -150L-20 0H-70Z', '#6F5F50')
    out += R(-70, -330, 90, 60, '#F4EEDC') + R(-80, -346, 110, 14, '#C8102E') + R(-54, -400, 58, 50, '#F4EEDC') + P('M-64 -400H12L-26 -440Z', '#E8B93A')
    return out + R(-44, -300, 10, 20, d) + R(-18, -300, 10, 20, d)


@motif('church_hill', 300)
def church_hill(c, s, d):
    return (P('M-200 0Q-120 -100 0 -110Q120 -100 200 0Z', '#7BA05B') + R(-34, -190, 68, 80, '#F4EEDC') + P('M-42 -190L0 -234L42 -190Z', '#B5543C')
            + R(-18, -250, 36, 70, '#F4EEDC') + spire(0, -250, 36, 56, '#B5543C') + R(-2, -318, 4, 22, d) + P('M-10 -110V-150Q0 -170 10 -150V-110Z', d))


@motif('stupa', 340)
def stupa(c, s, d):
    out = R(-120, -20, 240, 20, c) + R(-96, -44, 192, 24, s) + dome(0, -44, 90, 110, '#FFFFFF') + R(-30, -186, 60, 36, '#FFFFFF') + R(-30, -186, 60, 36, '#fff')
    out += R(-30, -186, 60, 36, c) + R(-32, -222, 64, 36, '#E8B93A') + ''.join(R(-26 + i * 10, -250 - i * 6, 52 - i * 20, 8, '#E8B93A') for i in range(4))
    out += ''.join(C(x, -166, 4, '#1F3F7A') for x in (-14, 14)) + P('M-110 -20L-250 -120M110 -20L250 -120', 'none', ' stroke="#C8102E" stroke-width="3"')
    out += ''.join(R(-230 + i * 22, -112 + i * 10, 14, 20, col) for i, col in enumerate(('#2E64C8', '#F4F1EA', '#C8102E', '#2E8B57', '#F2C230')))
    return out


@motif('temple_roof', 320)
def temple_roof(c, s, d):
    out = R(-120, -90, 240, 90, '#F4EEDC') + R(-120, -90, 240, 10, '#C8102E')
    for i, w in enumerate((260, 210, 150)):
        out += P(f'M{-w / 2} {-90 - i * 60}Q0 {-130 - i * 60} {w / 2} {-90 - i * 60}L{w / 2 - 20} {-60 - i * 60}H{-w / 2 + 20}Z', '#C8593A' if i % 2 == 0 else '#8C3F2E')
    return out + spire(0, -270, 14, 60, '#E8B93A')


@motif('rocket', 480)
def rocket(c, s, d):
    out = ''.join(R(-70 + i * 4, -i * 38 - 38, 14, 38, '#D8D2C8') for i in range(0)) + R(-90, -420, 12, 420, '#9A8F85') + R(-90, -420, 80, 10, '#9A8F85')
    for y in range(-380, 0, 60):
        out += P(f'M-90 {y}L-30 {y + 60}', 'none', ' stroke="#6F6560" stroke-width="3"')
    return out + P('M-30 0V-300Q-30 -400 0 -440Q30 -400 30 -300V0Z', '#FFFFFF') + R(-30, -150, 60, 24, '#C8102E') + P('M-30 0L-56 30V-60L-30 -80Z', '#C8102E') + P('M30 0L56 30V-60L30 -80Z', '#C8102E')


@motif('bridge_arch', 260)
def bridge_arch(c, s, d):
    return (P('M-300 -150H300V-130H-300Z', s) + P('M-260 0Q0 -300 260 0H210Q0 -230 -210 0Z', c) + ''.join(R(x, -140, 6, 90 - abs(x) * .25, s) for x in range(-200, 210, 40))
            + R(-290, -160, 20, 30, s) + R(270, -160, 20, 30, s))


@motif('laxey', 340)
def laxey(c, s, d):
    out = R(-30, -10, 60, 10, d)
    out += R(-150, -330, 28, 330, '#8C7B6A') + C(-30, -200, 150, 'none')
    out = out.replace(f'<circle cx="-30" cy="-200" r="150" fill="none"/>', '<circle cx="-30" cy="-200" r="150" fill="none" stroke="#B5543C" stroke-width="12"/>')
    out += ''.join(P(f'M-30 -200L{-30 + 150 * math.cos(math.radians(a)):.0f} {-200 + 150 * math.sin(math.radians(a)):.0f}', 'none', ' stroke="#B5543C" stroke-width="6"') for a in range(0, 360, 30))
    return out + C(-30, -200, 14, '#7A2E22') + R(-170, -350, 40, 24, '#B5543C')


# ----------------------------------------------------------------------------------------------------------------
# Natural features
# ----------------------------------------------------------------------------------------------------------------
@motif('christ', 560, 'back')
def christ(c, s, d):
    out = P('M-340 0Q-200 -180 -80 -260Q0 -300 80 -260Q200 -180 340 0Z', '#5E8A5B') + P('M0 -296Q80 -260 200 -180Q270 -110 340 0H60Z', '#4A7048')
    out += R(-24, -340, 48, 50, '#EFEAE0') + R(-24, -330, 12, 40, '#D6CFC0')
    out += P('M-18 -340L-14 -470H14L18 -340Z', '#EFEAE0') + R(-120, -464, 240, 22, '#EFEAE0') + C(0, -486, 20, '#EFEAE0') + R(-120, -464, 240, 6, '#D6CFC0')
    return out


@motif('machu', 420, 'back')
def machu(c, s, d):
    out = P('M-300 0L-200 -140L-120 -300L-90 -420L-50 -440L-20 -380L30 -260L120 -170L300 0Z', '#6B8F5B') + P('M-50 -440L-20 -380L30 -260L120 -170L300 0H0L-60 -260Z', '#557A49')
    for i in range(6):
        out += P(f'M{100 + i * 40} {-150 + i * 20}h{160 - i * 40}', 'none', ' stroke="#A8C07A" stroke-width="10" opacity=".7"')
    return out + ''.join(R(x, -120 + (x - 120) * .0, 36, 22, '#C9BDA4') for x in (150, 196, 242)) + ''.join(P(f'M{x} -142l18 -18l18 18Z', '#8C7B6A') for x in (150, 196, 242))


@motif('chichen', 380)
def chichen(c, s, d):
    out = ''
    for i in range(9):
        w = 420 - i * 40
        out += R(-w / 2, -(i + 1) * 30, w, 30, c if i % 2 == 0 else s)
    out += R(-60, -330, 120, 56, c) + R(-60, -330, 120, 8, s) + R(-14, -300, 28, 28, d)
    return out + P('M-16 0L-16 -270H16V0Z', s)


@motif('tikal', 420)
def tikal(c, s, d):
    out = ''.join(R(-120 + i * 18, -i * 50 - 50, 240 - i * 36, 50, c if i % 2 == 0 else s) for i in range(5))
    return out + R(-34, -330, 68, 60, c) + R(-50, -410, 100, 84, s) + R(-8, -280, 16, 30, d) + P('M-50 -410H50L36 -440H-36Z', c) + P('M-12 0L-12 -250H12L12 0Z', d)


@motif('peaks', 520, 'back')
def peaks(c, s, d):
    out = P('M-400 0L-300 -140L-220 -260L-200 -420L-170 -480L-140 -420L-120 -260L-60 -160L0 0Z', '#9A9AA8') + P('M-170 -480L-140 -420L-120 -260L-60 -160L0 0H-190L-196 -260Z', '#7B7B8C')
    out += P('M-60 0L-10 -140L40 -330L70 -450L100 -330L140 -150L200 0Z', '#A6A6B4') + P('M70 -450L100 -330L140 -150L200 0H60Z', '#808090')
    out += P('M140 0L200 -130L250 -260L290 -380L320 -250L360 -120L440 0Z', '#9A9AA8')
    return out + P('M-186 -450L-170 -480L-154 -450L-170 -430Z', '#fff') + P('M60 -420L70 -450L82 -418L70 -402Z', '#fff')


@motif('table', 340, 'back')
def table(c, s, d):
    return (P('M-420 0L-340 -70L-250 -250L-210 -300H230L290 -260L350 -110L440 0Z', '#7A8FA8') + P('M80 -300H230L290 -260L350 -110L440 0H100Z', '#5E738C')
            + P('M-210 -300H230L225 -312H-205Z', '#E8EEF5') + ''.join(E(x, -320, 80, 10, '#fff', ' opacity=".6"') for x in (-100, 60)))


@motif('kili', 380, 'back')
def kili(c, s, d):
    return (P('M-440 0L-300 -80L-160 -230L-80 -330L-30 -360H60L130 -330L220 -230L340 -90L460 0Z', '#7B6A8F') + P('M60 -360L130 -330L220 -230L340 -90L460 0H120Z', '#5E4F73')
            + P('M-30 -360H60L100 -340L60 -318L30 -340L-6 -318L-60 -338Z', '#FFFFFF') + P('M-80 -330L-60 -338L-6 -318L-60 -300Z', '#fff', ' opacity=".7"'))


@motif('vicfalls', 300, 'back')
def vicfalls(c, s, d):
    out = P('M-440 -80H-120L-100 -60L-60 0H-440Z', '#7A6A55') + P('M120 -80H440V0H60L100 -60Z', '#7A6A55')
    out += R(-110, -80, 220, 80, '#E8F4FB') + ''.join(R(-100 + i * 26, -80, 10, 80, '#BFE0F0') for i in range(8))
    out += E(0, -4, 160, 36, '#fff', ' opacity=".55"') + P('M-150 -120Q0 -260 150 -120', 'none', ' stroke="#FF8FAB" stroke-width="5" opacity=".55"') + P('M-130 -120Q0 -240 130 -120', 'none', ' stroke="#FFE066" stroke-width="5" opacity=".5"')
    return out


@motif('baobab', 340)
def baobab(c, s, d):
    c = '#6B4A35'
    def tree(x, h, w):
        return (P(f'M{x - w} 0Q{x - w * .6} {-h * .6} {x - w * .4} {-h}H{x + w * .4}Q{x + w * .6} {-h * .6} {x + w} 0Z', c)
                + ''.join(P(f'M{x + dx} {-h}L{x + dx * 2.4} {-h - 60}', 'none', f' stroke="{c}" stroke-width="10" stroke-linecap="round"') for dx in (-30, 0, 30)))
    return tree(-110, 240, 54) + tree(40, 300, 66) + tree(170, 200, 44)


@motif('zuma', 340, 'back')
def zuma(c, s, d):
    c, s, d = '#8B7B6E', '#6B5C50', '#4A3E34'
    return (P('M-200 0Q-190 -200 -150 -300Q-110 -380 -30 -400Q60 -400 120 -330Q190 -240 200 0Z', c) + P('M-30 -400Q60 -400 120 -330Q190 -240 200 0H60Q70 -200 -30 -400Z', s)
            + P('M-100 -120Q-60 -200 -90 -300', 'none', f' stroke="{d}" stroke-width="5" opacity=".5"'))


@motif('pitons', 460, 'back')
def pitons(c, s, d):
    out = P('M-260 0Q-230 -200 -170 -330Q-150 -380 -128 -420Q-110 -380 -88 -330Q-40 -200 -20 0Z', '#4F7F55') + P('M-128 -420Q-110 -380 -88 -330Q-40 -200 -20 0H-120Z', '#3B6A44')
    out += P('M-30 0Q-10 -160 40 -270Q60 -320 80 -350Q100 -320 118 -270Q160 -160 190 0Z', '#4F7F55') + P('M80 -350Q100 -320 118 -270Q160 -160 190 0H70Z', '#3B6A44')
    return out + P('M-300 0Q-120 -40 80 -30Q250 -20 330 0Z', '#3B6A44', ' opacity=".6"')


@motif('morne', 420, 'back')
def morne(c, s, d):
    return (P('M-300 0Q-280 -150 -230 -250Q-200 -400 -100 -420Q-40 -430 0 -410Q60 -380 90 -250Q140 -120 200 0Z', '#6B7F5B') + P('M-40 -428Q0 -410 60 -380Q90 -250 140 -120Q170 -50 200 0H-60Q-10 -200 -40 -428Z', '#4E6244'))


@motif('otemanu', 440, 'back')
def otemanu(c, s, d):
    return (P('M-320 0Q-300 -120 -240 -180Q-200 -220 -170 -260Q-150 -380 -100 -440Q-70 -420 -50 -300Q0 -240 80 -200Q220 -120 340 0Z', '#5C7A55')
            + P('M-100 -440Q-70 -420 -50 -300Q0 -240 80 -200Q220 -120 340 0H-60Q-110 -200 -100 -440Z', '#456243'))


@motif('cone', 460, 'back')
def cone(c, s, d):
    return (P('M-420 0L-260 -140L-120 -300L-50 -410Q0 -440 50 -410L120 -300L260 -140L420 0Z', '#4A3F52') + P('M50 -410L120 -300L260 -140L420 0H80Z', '#352C3D')
            + P('M-50 -410Q0 -440 50 -410Q0 -396 -50 -410Z', '#FF8A3D') + P('M-10 -418Q0 -470 12 -418Z', '#FFB347', ' opacity=".8"') + P('M-6 -396L-20 -300L-2 -330L-10 -200', 'none', ' stroke="#FF6B2B" stroke-width="5" opacity=".7"'))


@motif('glaciercone', 420, 'back')
def glaciercone(c, s, d):
    return (P('M-440 0L-300 -90L-160 -230L-90 -340L-40 -400H50L110 -340L200 -230L340 -90L460 0Z', '#4E5C7F') + P('M50 -400L110 -340L200 -230L340 -90L460 0H120Z', '#394667')
            + P('M-40 -400H50L90 -352L50 -330L20 -362L-20 -330L-70 -352Z', '#E8F0FF') + P('M-160 -230L-90 -340L-40 -330L-90 -270Z', '#E8F0FF', ' opacity=".6"'))


@motif('icebergs', 300, 'back')
def icebergs(c, s, d):
    out = ''
    for x, w, h in ((-250, 160, 180), (-60, 220, 260), (170, 180, 200)):
        out += P(f'M{x - w / 2} 0L{x - w * .3} {-h * .7}L{x - w * .1} {-h}L{x + w * .15} {-h * .6}L{x + w * .35} {-h * .8}L{x + w / 2} 0Z', '#F1F7FC') + P(f'M{x + w * .15} {-h * .6}L{x + w * .35} {-h * .8}L{x + w / 2} 0H{x}Z', '#BFD6EA')
    return out


@motif('turf', 240)
def turf(c, s, d):
    out = ''
    for x, col in ((-150, '#B5543C'), (-20, '#F4EEDC'), (110, '#B5543C')):
        out += R(x - 48, -70, 96, 70, col) + P(f'M{x - 58} -70L{x} -110L{x + 58} -70Z', '#4E7A3B') + R(x - 10, -40, 20, 40, '#3A2E2A')
    return out


@motif('falls', 440, 'back')
def falls(c, s, d):
    return (P('M-300 0V-300L-250 -440H80L130 -300V0Z', '#6B7F5B') + P('M-300 0V-300L-250 -440H-180Q-200 -300 -200 0Z', '#556A47')
            + R(-30, -430, 46, 430, '#E8F4FB') + R(-20, -430, 8, 430, '#BFE0F0') + E(-8, -6, 80, 20, '#fff', ' opacity=".65"'))


@motif('halong', 360, 'back')
def halong(c, s, d):
    out = ''
    for x, w, h in ((-250, 130, 240), (-120, 100, 320), (20, 150, 260), (170, 110, 340), (290, 120, 200)):
        out += P(f'M{x - w / 2} 0Q{x - w / 2 + 6} {-h * .5} {x - w * .2} {-h}Q{x} {-h - 20} {x + w * .2} {-h}Q{x + w / 2 - 6} {-h * .5} {x + w / 2} 0Z', '#6C8A7A') + P(f'M{x + w * .1} {-h}Q{x + w / 2 - 6} {-h * .5} {x + w / 2} 0H{x}Z', '#4E6B5C')
        out += P(f'M{x - w * .3} {-h * .4}Q{x} {-h * .3} {x + w * .3} {-h * .42}', 'none', ' stroke="#8FB59E" stroke-width="5" opacity=".6"')
    return out


@motif('karst', 340, 'back')
def karst(c, s, d):
    return halong(c, s, d)


# ----------------------------------------------------------------------------------------------------------------
# Boats, huts, animals, small props
# ----------------------------------------------------------------------------------------------------------------
@motif('dhow', 200)
def dhow(c, s, d):
    return P('M-120 0L-90 30H100L130 -10Z', '#5A3A2A') + R(0, -170, 5, 180, '#3A2A22') + P('M5 -170L130 -20L5 -30Z', '#F4EEDC') + P('M-5 -140L-100 -22L-5 -28Z', '#E8DCC4')


@motif('sailboat', 200)
def sailboat(c, s, d):
    return P('M-90 0L-60 26H70L100 0Z', '#F4F1EA') + R(0, -170, 4, 170, '#7A6A5A') + P('M6 -170L84 -14L6 -14Z', '#FFFFFF') + P('M-6 -130L-62 -14L-6 -14Z', '#E8F0FA')


@motif('canoe', 140)
def canoe(c, s, d):
    return P('M-110 0Q0 30 110 0L90 -14H-90Z', '#8C5A3C') + P('M-70 6H70', 'none', ' stroke="#5A3A2A" stroke-width="5"') + R(-90, 30, 180, 5, '#7A4E34') + P('M-70 -14L-80 30M70 -14L80 30', 'none', ' stroke="#5A3A2A" stroke-width="4"')


@motif('junk', 220)
def junk(c, s, d):
    return (P('M-120 0L-100 36H110L130 -4Z', '#7A2E22') + R(-6, -190, 5, 190, '#3A2A22') + P('M-1 -190Q80 -150 100 -26H-1Z', '#C8593A') + P('M-5 -170Q-70 -140 -86 -30H-5Z', '#A8432E')
            + ''.join(P(f'M{x} -190V-20', 'none', ' stroke="#7A2E22" stroke-width="2"') for x in (30, 60)))


@motif('longtail', 200)
def longtail(c, s, d):
    return P('M-130 0Q0 20 130 -20L100 -30H-110Z', '#C8593A') + P('M-90 -30Q0 -70 90 -34Z', '#F2C230') + P('M100 -20L190 -50', 'none', ' stroke="#3A2A22" stroke-width="5"')


@motif('banca', 200)
def banca(c, s, d):
    return (canoe(c, s, d) + P('M-130 -30L-110 -10M130 -30L110 -10', 'none', ' stroke="#2E8B57" stroke-width="5"') + P('M-130 -30H130', 'none', ' stroke="#2E8B57" stroke-width="4"'))


@motif('pirogue', 150)
def pirogue(c, s, d):
    return P('M-130 -8Q0 26 130 -12L110 -30H-100Z', '#5A3A2A') + P('M-60 -30L-40 -66H50L70 -30Z', '#F2C230') + R(-2, -90, 4, 30, '#5A3A2A') + P('M-130 -8L-150 -34', 'none', ' stroke="#5A3A2A" stroke-width="6" stroke-linecap="round"')


@motif('rondavel', 160)
def rondavel(c, s, d):
    out = ''
    for x, sc in ((-70, 1), (60, .8)):
        out += f'<g transform="translate({x} 0) scale({sc})">' + R(-40, -50, 80, 50, '#C9A27A') + P('M-52 -50L0 -110L52 -50Z', '#8C6A3F') + R(-9, -34, 18, 34, '#4A3A2A') + '</g>'
    return out


@motif('fale', 180)
def fale(c, s, d):
    return (''.join(R(x, -50, 6, 50, '#7A5A3A') for x in (-60, -20, 20, 54)) + E(0, -62, 80, 40, '#C9A27A') + P('M-84 -60Q0 -130 84 -60Z', '#C9A27A') + R(-70, -10, 140, 8, '#8C6A4A'))


@motif('stilt', 180)
def stilt(c, s, d):
    return ''.join(R(x - 3, -30, 6, 40, '#6B5240') for x in (-70, -30, 30, 70)) + R(-90, -50, 180, 20, '#8C6A4A') + R(-70, -100, 140, 50, '#E8DCC4') + P('M-90 -100L0 -150L90 -100Z', '#8C3F2E') + R(-14, -86, 28, 36, '#4A3A2A')


@motif('colorhouses', 220)
def colorhouses(c, s, d):
    cols = ['#E63946', '#F4A261', '#2A9D8F', '#E9C46A', '#6C8EBF', '#C77DFF', '#F28482']
    out = ''
    for i in range(9):
        x = -230 + i * 54
        h = 110 + (i * 37 % 5) * 18
        col = cols[i % len(cols)]
        out += R(x, -h, 50, h, col) + P(f'M{x - 3} {-h}L{x + 25} {-h - 34}L{x + 53} {-h}Z', '#5A4A42') + R(x + 8, -h + 22, 10, 14, '#FFF5D6') + R(x + 30, -h + 22, 10, 14, '#FFF5D6') + R(x + 8, -h + 56, 10, 14, '#FFF5D6') + R(x + 30, -h + 56, 10, 14, '#FFF5D6')
    return out


@motif('elephant', 200)
def elephant(c, s, d):
    c, s = '#6F6A66', '#55514E'
    return (''.join(R(x, -50, 22, 52, c) for x in (-78, -44, 30, 62)) + E(0, -90, 100, 56, c) + C(100, -112, 36, c) + P('M120 -100Q150 -70 130 -30', 'none', f' stroke="{c}" stroke-width="20" stroke-linecap="round"')
            + E(80, -108, 26, 34, s) + P('M122 -88L156 -80', 'none', ' stroke="#fff" stroke-width="5" stroke-linecap="round"'))


@motif('gorilla', 190)
def gorilla(c, s, d):
    c, s = '#3A3632', '#2A2724'
    return (E(0, -90, 70, 64, c) + C(30, -170, 30, c) + P('M-40 -130Q-110 -60 -80 0H-50Q-60 -50 -20 -80Z', c) + P('M40 -120Q100 -60 78 0H48Q52 -50 20 -80Z', s)
            + R(-50, -40, 30, 40, c) + R(10, -40, 30, 40, c))


@motif('flamingo', 220)
def flamingo(c, s, d):
    col = '#F28AA8'
    return (R(-2, -110, 4, 110, '#E36A8D') + E(0, -130, 34, 22, col) + P('M10 -140Q50 -200 28 -230', 'none', f' stroke="{col}" stroke-width="9" stroke-linecap="round"') + C(30, -232, 9, col)
            + P('M36 -234L56 -226L38 -222Z', '#2A1A1A'))


@motif('llama', 200)
def llama(c, s, d):
    return (''.join(R(x, -60, 8, 62, '#EFE6D6') for x in (-50, -30, 24, 42)) + E(0, -90, 58, 34, '#EFE6D6') + P('M30 -104Q50 -170 60 -190L76 -184Q70 -140 58 -96Z', '#EFE6D6')
            + E(76, -192, 18, 10, '#EFE6D6', ' transform="rotate(-20 76 -192)"') + P('M70 -198L66 -218M82 -200L88 -218', 'none', ' stroke="#EFE6D6" stroke-width="5" stroke-linecap="round"'))


@motif('bison', 190)
def bison(c, s, d):
    return (''.join(R(x, -50, 12, 52, '#3A2A22') for x in (-60, -34, 34, 56)) + P('M-90 -70Q-70 -150 0 -140Q70 -150 90 -90Q80 -50 0 -50Q-70 -40 -90 -70Z', '#4A3428')
            + E(100, -88, 28, 24, '#2E211A') + P('M96 -108L90 -126M112 -108L120 -124', 'none', ' stroke="#E8DCC4" stroke-width="5" stroke-linecap="round"'))


@motif('whale', 200)
def whale(c, s, d):
    return (P('M-120 0Q-80 -60 -20 -90Q-30 -140 -70 -160Q-20 -160 0 -110Q20 -160 70 -160Q30 -140 20 -90Q80 -60 120 0Z', '#2F4A66')
            + P('M-30 -92Q0 -80 30 -92', 'none', ' stroke="#BFD6EA" stroke-width="4"'))


@motif('toucan', 160)
def toucan(c, s, d):
    return (R(-4, -50, 8, 50, '#5A4030') + E(0, -90, 32, 44, '#1F1A1A') + C(8, -130, 18, '#1F1A1A') + P('M18 -134L68 -128Q60 -106 18 -118Z', '#F28C28') + E(12, -66, 14, 20, '#F4F1EA'))


@motif('ibis', 170)
def ibis(c, s, d):
    return (E(0, -80, 40, 24, '#E2403C') + P('M20 -88Q54 -130 40 -170', 'none', ' stroke="#E2403C" stroke-width="9" stroke-linecap="round"') + C(40, -172, 10, '#E2403C')
            + P('M46 -170L76 -150L48 -162Z', '#2A1A1A') + R(-12, -60, 3, 60, '#3A2A2A') + R(8, -60, 3, 60, '#3A2A2A'))


@motif('shoebill', 190)
def shoebill(c, s, d):
    return (R(-4, -90, 6, 90, '#4A4A52') + E(0, -120, 34, 50, '#6F7480') + C(10, -184, 20, '#6F7480') + P('M20 -190Q60 -184 62 -160Q40 -150 18 -166Z', '#C9B89A'))


@motif('okapi', 200)
def okapi(c, s, d):
    return (''.join(R(x, -70, 10, 72, '#5A3A2A') + R(x, -40, 10, 8, '#F4EEDC') for x in (-52, -30, 28, 46)) + E(0, -100, 62, 34, '#5A3A2A') + P('M36 -112L62 -110L74 -156L56 -160Z', '#5A3A2A') + E(72, -164, 18, 10, '#5A3A2A'))


@motif('gelada', 160)
def gelada(c, s, d):
    return E(0, -50, 44, 34, '#6B4A35') + C(34, -86, 22, '#4E3426') + E(-10, -40, 30, 24, '#C8593A') + R(-40, -20, 14, 22, '#4E3426') + R(10, -20, 14, 22, '#4E3426')


@motif('birdofparadise', 220)
def birdofparadise(c, s, d):
    return (E(0, -90, 36, 24, '#F2C230') + C(34, -104, 14, '#2E8B57') + P('M-30 -86Q-120 -60 -150 20Q-90 -20 -26 -76Z', '#E8892B') + P('M-24 -78Q-100 -20 -110 60Q-60 20 -20 -68Z', '#E2403C') + P('M44 -104L66 -98L46 -96Z', '#2A1A1A'))


@motif('stingbird', 100)
def stingbird(c, s, d):
    return ''


@motif('divi', 200)
def divi(c, s, d):
    return (P('M0 0Q-10 -60 30 -110Q90 -150 150 -130', 'none', ' stroke="#4A3A2A" stroke-width="12" stroke-linecap="round"')
            + E(110, -130, 90, 28, '#2E7D32') + E(60, -120, 54, 20, '#3E8E41'))


@motif('pinnacles', 160, 'back')
def pinnacles(c, s, d):
    return ''.join(P(f'M{x - w / 2} 0L{x - w * .15} {-h}L{x + w * .15} {-h * .95}L{x + w / 2} 0Z', '#4A4A52') for x, w, h in ((-100, 60, 150), (-20, 80, 190), (70, 70, 140), (150, 56, 110)))


@motif('boulders', 150)
def boulders(c, s, d):
    return (E(-90, -50, 70, 50, '#B5A8A0') + E(40, -70, 90, 70, '#A99C94') + E(150, -36, 50, 36, '#B5A8A0') + E(-30, -36, 50, 36, '#9E918A'))


@motif('moai', 150)
def moai(c, s, d):
    return ''.join(P(f'M{x - 26} 0V-100Q{x - 28} -150 {x - 14} -170H{x + 14}Q{x + 28} -150 {x + 26} -100V0Z', '#6E6258') for x in (-70, 0, 70))


@motif('citadel', 300, 'back')
def citadel(c, s, d):
    return (P('M-300 0Q-260 -160 -150 -240Q-60 -300 0 -300Q80 -290 160 -230Q260 -150 300 0Z', '#5E7A52') + R(-110, -340, 220, 60, '#C9BFA6') + P('M-110 -340L-70 -380H70L110 -340Z', '#8C8070')
            + ''.join(R(x, -318, 12, 20, '#4A4238') for x in (-80, -30, 20, 70)))


@motif('pagoda', 380)
def pagoda(c, s, d):
    out = R(-60, -60, 120, 60, '#C8593A')
    for i in range(5):
        w = 150 - i * 20
        out += P(f'M{-w} {-60 - i * 60}Q0 {-80 - i * 60} {w} {-60 - i * 60}L{w - 24} {-40 - i * 60}H{-w + 24}Z', '#8C3F2E' if i % 2 else '#B5543C') + R(-w * .38, -100 - i * 60, w * .76, 40, '#F4EEDC' if i % 2 == 0 else '#E8DCC4')
    return out + R(-2, -420, 4, 50, '#E8B93A')


@motif('mayanstela', 150)
def mayanstela(c, s, d):
    return R(-30, -150, 60, 150, '#8C8078') + ''.join(R(-18, -130 + i * 30, 36, 14, '#6E6258') for i in range(4))


@motif('caravan', 140)
def caravan(c, s, d):
    out = ''
    for x, sc in ((-150, 1.0), (-10, 1.0), (130, 1.0)):
        col = '#3A2A22'
        out += (f'<g transform="translate({x} 0) scale({sc})" fill="{col}">'
                + ''.join(f'<rect x="{lx}" y="-58" width="7" height="60" rx="2"/>' for lx in (-34, -22, 22, 34))
                + '<ellipse cx="0" cy="-74" rx="46" ry="20"/><ellipse cx="-6" cy="-98" rx="14" ry="16"/>'
                + f'<path d="M34 -80Q52 -100 50 -128" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>'
                + '<ellipse cx="58" cy="-132" rx="14" ry="8" transform="rotate(-12 58 -132)"/></g>')
    return out


@motif('hut_stone', 150)
def hut_stone(c, s, d):
    return R(-60, -60, 120, 60, '#B5A89A') + P('M-72 -60L0 -120L72 -60Z', '#7A6A5A') + R(-12, -40, 24, 40, '#4A3E34')


@motif('yacht', 160)
def yacht(c, s, d):
    return P('M-120 0L-90 24H100L130 -10Z', '#F4F1EA') + R(-60, -50, 120, 40, '#FFFFFF') + R(-30, -80, 70, 32, '#E8F0FA') + R(-120, 0, 250, 6, '#B8C4D0')


@motif('crater', 200, 'back')
def crater(c, s, d):
    return cone(c, s, d)


@motif('ruins', 200)
def ruins(c, s, d):
    return leptis(c, s, d)


@motif('cabin', 180)
def cabin(c, s, d):
    return R(-60, -60, 120, 60, '#B83A32') + P('M-72 -60L0 -112L72 -60Z', '#3A2E2A') + R(-12, -44, 24, 44, '#FFF') + R(-48, -44, 20, 20, '#FFF') + R(28, -44, 20, 20, '#FFF')


@motif('sauna', 180)
def sauna(c, s, d):
    return cabin(c, s, d) + R(40, -140, 14, 30, '#3A2E2A')


@motif('house_beach', 160)
def house_beach(c, s, d):
    return R(-70, -70, 140, 70, '#F4EEDC') + P('M-82 -70L0 -120L82 -70Z', '#C8593A') + R(-12, -48, 24, 48, '#2E7D8F')


@motif('totem', 100)
def totem(c, s, d):
    return ''


def render(key, c, s, d):
    return M[key][0](c, s, d)


# ----------------------------------------------------------------------------------------------------------------
# Motifs shared with the hand-made sample scenes (same geometry as make_scenes.py)
# ----------------------------------------------------------------------------------------------------------------
@motif('eiffel', 540)
def eiffel(c, s, d):
    return (P('M0 -540L10 -470L20 -380C32 -280 56 -180 112 0L72 0C64 -40 40 -88 0 -88C-40 -88 -64 -40 -72 0L-112 0C-56 -180 -32 -280 -20 -380L-10 -470Z', c)
            + R(-66, -176, 132, 12, s) + R(-38, -338, 76, 9, s) + R(-14, -468, 28, 7, s))


@motif('taj', 340)
def taj(c, s, d):
    out = R(-300, 0, 600, 36, s) + R(-250, -34, 500, 34, c)
    for sx in (-1, 1):
        out += (f'<g transform="translate({sx * 215} 0)">' + R(-17, -30, 34, 30, s) + R(-10, -250, 20, 220, c) + R(-14, -140, 28, 7, s) + R(-14, -196, 28, 7, s)
                + P('M-14 -250C-14 -284 14 -284 14 -250Z', c) + R(-1.5, -296, 3, 16, s) + '</g>')
    out += R(-112, -170, 224, 140, c) + P('M-36 -30V-98Q-36 -128 0 -140Q36 -128 36 -98V-30Z', d, ' opacity=".6"')
    out += R(-64, -196, 128, 30, c) + P('M-70 -196C-96 -330 96 -330 70 -196Z', c) + R(-2, -340, 4, 30, s) + C(0, -346, 5, s)
    return out + P('M-104 -170C-108 -216 -66 -216 -70 -170Z', c) + P('M104 -170C108 -216 66 -216 70 -170Z', c)


@motif('opera', 260)
def opera(c, s, d):
    sail = 'M0 0C0 -80 70 -190 200 -225C170 -150 120 -70 104 0Z'
    shade = 'M0 0C0 -80 70 -190 200 -225C120 -120 70 -50 60 0Z'
    parts = ''
    for dx, sc in ((0, 1.0), (70, .86), (136, .72), (190, .58)):
        parts += f'<g transform="translate({dx} 0) scale({sc})"><path d="{sail}" fill="{c}"/><path d="{shade}" fill="{s}" opacity=".65"/></g>'
    right = ''.join(f'<g transform="translate({300 + dx} 0) scale({-sc} {sc})"><path d="{sail}" fill="{c}"/><path d="{shade}" fill="{s}" opacity=".65"/></g>' for dx, sc in ((0, .78), (60, .62), (110, .48)))
    return R(-30, -4, 420, 44, d, 0) + parts + right


@motif('windmill', 340)
def windmill(c, s, d):
    blades = ''
    for a in (40, 130, 220, 310):
        blades += f'<g transform="rotate({a})">' + R(-6, -230, 12, 230, '#3A2C2C') + f'<rect x="6" y="-226" width="46" height="130" fill="#F1E6D2" stroke="#3A2C2C" stroke-width="3"/></g>'
    return (P('M-46 0L-30 -240L30 -240L46 0Z', '#8A5A44') + R(-54, -26, 108, 26, '#2E2424') + P('M-34 -240C-34 -290 34 -290 34 -240Z', '#2E2424')
            + f'<g transform="translate(0 -250)">{blades}<circle r="12" fill="#3A2C2C"/></g>')


@motif('ger', 140)
def ger(c, s, d):
    return (E(0, 2, 86, 8, '#000', ' opacity=".15"') + R(-76, -62, 152, 62, '#F3EDE3') + P('M-92 -62L0 -128L92 -62Z', '#EAE0CF') + R(-92, -66, 184, 8, '#D9772B')
            + R(-14, -44, 28, 44, '#D9772B') + R(-3, -134, 6, 14, '#4A3B35'))


@motif('liberty', 480)
def liberty(c, s, d):
    col, shade = '#4FA38F', '#3C8573'
    spikes = ''.join(f'<path d="M{21 * math.cos(math.radians(t)):.1f} {-330 - 21 * math.sin(math.radians(t)):.1f}L{44 * math.cos(math.radians(t)):.1f} {-330 - 44 * math.sin(math.radians(t)):.1f}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
                     for t in (20, 45, 70, 90, 110, 135, 160))
    return (P('M-130 0L-90 -40H90L130 0Z', shade) + R(-56, -150, 112, 116, '#B9B2A5') + R(-68, -160, 136, 14, '#B9B2A5')
            + P('M-38 -160L-28 -270L-20 -310H20L28 -270L40 -160Z', col) + P('M0 -310L20 -310L28 -270L40 -160L0 -160Z', shade) + C(0, -330, 21, col) + spikes
            + P('M14 -300L46 -420L60 -416L32 -292Z', col) + R(44, -438, 18, 12, shade) + P('M53 -440C40 -462 53 -476 53 -484C68 -468 68 -452 53 -440Z', '#FFC93C'))


@motif('pyramids', 280)
def pyramids(c, s, d):
    def py(x, w, h):
        return P(f'M{x - w / 2} 0L{x} {-h}L{x + w / 2} 0Z', c) + P(f'M{x} {-h}L{x + w / 2} 0H{x + w * .1}Z', s)
    return py(-120, 360, 270) + py(130, 210, 160) + py(250, 130, 96)


@motif('fuji', 330, 'back')
def fuji(c, s, d):
    return (P('M-340 0L-60 -310Q0 -330 60 -310L340 0Z', '#5B6C8F') + P('M-86 -283L-60 -310Q0 -330 60 -310L86 -283L54 -268L22 -292L-6 -262L-40 -286L-62 -266Z', '#fff'))


@motif('bungalow', 120)
def bungalow(c, s, d):
    stilts = ''.join(R(x, 0, 5, 40, '#6B5240') for x in (-56, -30, 30, 56))
    return (stilts + R(-76, -6, 152, 10, '#8C6A4A') + R(-54, -44, 108, 40, '#F2E4CC') + P('M-84 -44L0 -100L84 -44Z', '#7A5638') + R(-14, -32, 28, 28, '#6F4B35'))


@motif('atomium', 400)
def atomium(c, s, d):
    pts = [(0, -300), (-110, -230), (110, -230), (-110, -90), (110, -90), (0, -20), (0, -160), (-200, -160), (200, -160)]
    out = ''.join(f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" stroke="{s}" stroke-width="16"/>' for a, b in (
        (pts[0], pts[1]), (pts[0], pts[2]), (pts[1], pts[3]), (pts[2], pts[4]), (pts[3], pts[5]), (pts[4], pts[5]), (pts[1], pts[2]), (pts[3], pts[4]), (pts[0], pts[6]), (pts[6], pts[5]), (pts[7], pts[8])))
    return out + ''.join(C(x, y, 40 if (x, y) != (0, -160) else 34, c) + C(x - 12, y - 12, 10, '#fff') for x, y in pts)
