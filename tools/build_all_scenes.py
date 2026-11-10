#!/usr/bin/env python3
"""Generates the static scene SVG for every destination in scene-plan.xlsx (named by lower-case code) plus preview sheets.

Usage: python tools/build_all_scenes.py --plan destination-art/scene-plan.xlsx --out destination-art/scenes [codes...]
"""
import argparse
import html
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl  # noqa: E402

import destination_art as da  # noqa: E402
import make_scenes as ms  # noqa: E402
import scene_backdrops as bd  # noqa: E402
import scene_data  # noqa: E402

da.ANIMATE = False
ALLOWED = {'volcanic': [1, 2], 'arctic': [1], 'boreal-forest': [0, 1, 2], 'city-skyline': [0, 1, 2]}


def compose(code, typ, mark):
    keys = scene_data.KEYS.get(code.upper(), [])
    v = bd.VAR[(ALLOWED.get(typ) or [0, 1, 2])[zlib.crc32(code.encode()) % len(ALLOWED.get(typ) or [0, 1, 2])]]
    import random
    rnd = random.Random(zlib.crc32(code.encode()))
    defs, body = bd.BACKDROPS[typ](keys, v, rnd)
    return da.svg(f'Illustration: {html.escape(mark)}', defs, '', body)


def scene_gl139():
    out = ms.scene_gl120()
    # same scene, different landmark icons along the horizon
    sil = '#2A1A4A'
    old = (ms.g(110, 880, .27, ms.eiffel(sil, sil)) + ms.g(250, 880, .3, ms.taj(sil, sil, sil)) + ms.g(380, 880, .3, ms.fuji(sil, sil)) +
           ms.g(540, 880, .42, ms.pyramid(300, 210, sil, sil)) + ms.g(660, 880, .3, ms.opera(sil, sil, sil)) + ms.g(830, 880, .3, ms.liberty(sil, sil, sil)))
    new = (ms.g(110, 880, .3, ms.windmill(sil, sil, sil, sil)) + ms.g(260, 880, .42, ms.pyramid(300, 210, sil, sil)) + ms.g(400, 880, .3, ms.taj(sil, sil, sil)) +
           ms.g(580, 880, .3, ms.opera(sil, sil, sil)) + ms.g(740, 880, .3, ms.fuji(sil, sil)) + ms.g(880, 880, .27, ms.eiffel(sil, sil)))
    assert old in out
    return out.replace(old, new).replace('landmarks from around the world', 'landmarks from every continent')


SHEET = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>@@T@@</title>
<style>
body{margin:0;font-family:ui-sans-serif,system-ui,sans-serif;background:#F7F7F7;color:#111827}
main{max-width:1240px;margin:0 auto;padding:1.25rem}h1{font-size:1.25rem;margin:0 0 .75rem}
nav{margin:0 0 1rem;font-size:.875rem}nav a{margin-right:.75rem;color:#6415FE}
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.9rem}
.card{background:#fff;border:1px solid #E9E9E9;border-radius:14px;padding:.5rem}
.card figure{margin:0;overflow:hidden;border-radius:10px;aspect-ratio:4/5}.card img{display:block;width:100%;height:100%;object-fit:cover}
.card b{display:block;margin-top:.4rem;font-size:.8rem}.card span{font-size:.7rem;color:#5F6672}
</style></head><body><main><h1>@@T@@</h1><nav>@@NAV@@</nav><div class="grid">@@CARDS@@</div></main></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--per-sheet', type=int, default=20)
    ap.add_argument('codes', nargs='*')
    a = ap.parse_args()
    rows = [r for r in openpyxl.load_workbook(a.plan, read_only=True).worksheets[0].iter_rows(min_row=2, values_only=True) if r[0]]
    os.makedirs(a.out, exist_ok=True)
    cards, total = [], 0
    for code, kind, name, typ, mark, note, *_ in rows:
        low = code.lower()
        if a.codes and low not in [c.lower() for c in a.codes]:
            continue
        if low in ms.SCENES:
            out = ms.SCENES[low]()
        elif low == 'gl-139':
            out = scene_gl139()
        else:
            out = compose(code, typ, mark)
        open(os.path.join(a.out, f'{low}.svg'), 'w', encoding='utf-8').write(out)
        total += len(out)
        cards.append(f'<div class="card"><figure><img src="{low}.svg" alt="{html.escape(name)} illustration" loading="lazy"></figure><b>{html.escape(name)}</b><span>{code} · {typ}</span></div>')
    pages = [cards[i:i + a.per_sheet] for i in range(0, len(cards), a.per_sheet)]
    nav = ''.join(f'<a href="sheet-{i + 1}.html">{i + 1}</a>' for i in range(len(pages)))
    for i, page in enumerate(pages):
        open(os.path.join(a.out, f'sheet-{i + 1}.html'), 'w', encoding='utf-8').write(
            SHEET.replace('@@T@@', f'Destination scenes: sheet {i + 1} of {len(pages)}').replace('@@NAV@@', nav).replace('@@CARDS@@', ''.join(page)))
    open(os.path.join(a.out, 'index.html'), 'w', encoding='utf-8').write(
        SHEET.replace('@@T@@', f'Destination scenes ({len(cards)})').replace('@@NAV@@', nav).replace('@@CARDS@@', ''.join(cards)))
    print(f'{len(cards)} scenes, {total / 1024:.0f} KB total, {len(pages)} sheets -> {a.out}')


if __name__ == '__main__':
    main()
