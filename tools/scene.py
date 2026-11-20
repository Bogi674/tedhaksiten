import math, random
from lib import *

# ------------------------------------------------------------ misty forest 500x848
def tree(x, base, h, w, cols, rnd, canopy=True, lean=0, trunk=None):
    col, dark, light = cols
    trunk = trunk or dark
    top = base - h
    tw = w * .08
    o = [f'<path d="M{x-tw:.1f},{base} C{x-tw*.8+lean*.3:.1f},{base-h*.5:.1f} {x-tw*.35+lean:.1f},{top+h*.2:.1f} {x+lean:.1f},{top:.1f} '
         f'C{x+tw*.35+lean:.1f},{top+h*.2:.1f} {x+tw*.8+lean*.3:.1f},{base-h*.5:.1f} {x+tw:.1f},{base}Z" fill="{trunk}"/>',
         f'<path d="M{x-tw*.3:.1f},{base} C{x-tw*.3+lean*.3:.1f},{base-h*.5:.1f} {x+lean*.9:.1f},{top+h*.25:.1f} {x+lean:.1f},{top+h*.1:.1f}" stroke="{light}" stroke-opacity=".35" stroke-width="{tw*.35:.1f}" fill="none"/>']
    for _ in range(rnd.randint(1, 3)):
        by = base - h * rnd.uniform(.4, .75); s = rnd.choice((-1, 1))
        o.append(f'<path d="M{x+lean*.5:.1f},{by:.1f} q{s*w*.2:.1f},{-h*.06:.1f} {s*w*.4:.1f},{-h*.16:.1f}" stroke="{trunk}" stroke-width="{tw*.5:.1f}" fill="none" stroke-linecap="round"/>')
    if canopy:
        n = int(110 + w * 1.1)
        pts = [(x + lean + max(-w*.55, min(w*.55, rnd.gauss(0, w * .28))), top + min(h*.32, abs(rnd.gauss(0, h * .14))) - h * .03, rnd.uniform(w * .03, w * .07)) for _ in range(n)]
        o += [f'<circle cx="{cx+r*.25:.1f}" cy="{cy+r*.3:.1f}" r="{r:.1f}" fill="{dark}"/>' for cx, cy, r in pts]
        o += [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*.9:.1f}" fill="{col}"/>' for cx, cy, r in pts]
        o += [f'<circle cx="{cx-r*.3:.1f}" cy="{cy-r*.35:.1f}" r="{r*.45:.1f}" fill="{light}" opacity=".8"/>' for cx, cy, r in pts if rnd.random() < .55]
    return ''.join(o)

def forest(seed):
    rnd = random.Random(seed)
    W, H = 500, 848
    defs = (lin('sky', [(0, '#fdf9f1', 1), (.45, '#f4ead8', 1), (1, '#e9dbc2', 1)]) +
            rad('glow', [(0, '#fffdf7', 1), (.5, '#fbf3e3', .8), (1, '#f6ecda', 0)], .5, .32, .55) +
            lin('fog', [(0, '#f8f0e1', 0), (.5, '#f8f0e1', .85), (1, '#f8f0e1', 0)]) +
            lin('fogUp', [(0, '#f6ecdb', 0), (1, '#f6ecdb', .95)]) +
            lin('ground', [(0, '#c4bea0', 1), (1, '#7f7c5c', 1)]) +
            lin('path', [(0, '#f5eedd', .95), (1, '#ddd0b0', .95)]) +
            lin('mtn', [(0, '#fffaf0', 1), (.25, '#efe2c8', 1), (1, '#d8c5a3', 1)]) +
            blur('b6', 6) + blur('b3', 3.5) + blur('b1', 1.6) + blur('b12', 14) + blur('b2', 2.2))
    o = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # distant mountain range
    o.append('<g filter="url(#b3)" opacity=".85">'
             '<path d="M80,420 L190,330 L230,300 L250,262 L268,292 L310,328 L420,420Z" fill="url(#mtn)"/>'
             '<path d="M250,262 L240,285 L252,280 L262,296 L268,292Z" fill="#fffdf7"/>'
             '<path d="M-20,440 L60,380 L120,400 L170,360 L230,410Z M270,410 L330,360 L380,395 L440,370 L520,440Z" fill="#e2dcc6"/></g>')
    o.append('<rect y="300" width="500" height="200" fill="url(#fog)"/>')
    # far trees (pale, blurred)
    far = []
    for i in range(34):
        x = rnd.uniform(-20, W + 20)
        if 190 < x < 310 and rnd.random() < .7: continue
        far.append(tree(x, rnd.uniform(560, 620), rnd.uniform(260, 420), rnd.uniform(40, 80), ('#d6d5bd', '#c9c8ae', '#e4e2cd'), rnd, trunk='#cfc9b1'))
    o.append(f'<g filter="url(#b3)" opacity=".9">{"".join(far)}</g>')
    o.append('<rect y="380" width="500" height="260" fill="url(#fog)"/>')
    # mid trees
    mid = []
    for i in range(26):
        side = rnd.choice((0, 1))
        x = rnd.uniform(-30, 175) if side == 0 else rnd.uniform(325, W + 30)
        mid.append(tree(x, rnd.uniform(640, 720), rnd.uniform(380, 560), rnd.uniform(60, 110), rnd.choice((('#bdbd9d', '#a9aa88', '#d3d2b5'), ('#b4b593', '#a0a17f', '#cccbae'))), rnd, lean=rnd.uniform(-15, 15), trunk='#9c9378'))
    o.append(f'<g filter="url(#b2)">{"".join(mid)}</g>')
    o.append(f'<ellipse cx="250" cy="290" rx="230" ry="330" fill="url(#glow)"/>')
    # ground & path
    o.append('<path d="M0,690 Q250,650 500,690 L500,848 L0,848Z" fill="url(#ground)"/>')
    o.append('<path d="M232,668 Q246,664 262,668 L330,848 L170,848Z" fill="url(#path)"/>')
    o.append('<path d="M240,672 Q236,720 210,760 Q190,800 200,848" stroke="#efe4cd" stroke-width="5" fill="none" opacity=".6" filter="url(#b1)"/>')
    # near trees on the sides
    near = []
    for i in range(16):
        side = i % 2
        x = rnd.uniform(-60, 110) if side == 0 else rnd.uniform(390, W + 60)
        near.append(tree(x, rnd.uniform(760, 860), rnd.uniform(620, 820), rnd.uniform(110, 170), rnd.choice((('#8f9670', '#767d58', '#adb38b'), ('#88916a', '#6f7852', '#a7ae86'))), rnd, lean=(18 if side == 0 else -18) * rnd.random(), trunk='#857a62'))
    o.append(f'<g filter="url(#b2)" opacity=".92">{"".join(near)}</g>')
    # darker frame foliage at extreme edges
    edge = []
    for i in range(26):
        side = i % 2
        x = rnd.uniform(-50, 25) if side == 0 else rnd.uniform(475, 550)
        y = rnd.uniform(-20, H)
        r = rnd.uniform(18, 36)
        edge.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*1.2:.0f}" ry="{r:.0f}" fill="{rnd.choice(("#79805c","#838a65","#707755"))}"/>')
    o.append(f'<g filter="url(#b3)" opacity=".9">{"".join(edge)}</g>')
    # low fog over ground + light rays
    o.append('<rect width="500" height="848" fill="#f6efe1" opacity=".18"/>')
    o.append('<rect y="600" width="500" height="160" fill="url(#fog)" opacity=".9"/>')
    o.append('<rect y="760" width="500" height="88" fill="url(#fogUp)" opacity=".55"/>')
    rays = ''.join(f'<path d="M{250+dx},120 L{250+dx*3.5-30},700 L{250+dx*3.5+30},700Z" fill="#fffaf0" opacity=".10"/>' for dx in (-40, -15, 15, 40))
    o.append(f'<g filter="url(#b12)">{rays}</g>')
    return svg(W, H, ''.join(o), defs)

# ------------------------------------------------------------ candi (Prambanan style) 500x760, doorway transparent
STONE_L, STONE_M, STONE_D, LINE = '#e3d3b4', '#c7b08b', '#9c8462', '#6e5a41'

def ratna(x, by, s):
    return (f'<g transform="translate({x:.1f},{by:.1f})">'
            f'<path d="M{-s*.55:.1f},0 L{s*.55:.1f},0 L{s*.45:.1f},{-s*.18:.1f} C{s*.5:.1f},{-s*.55:.1f} {s*.25:.1f},{-s*.85:.1f} {s*.1:.1f},{-s*.95:.1f} '
            f'L{s*.06:.1f},{-s*1.25:.1f} L{-s*.06:.1f},{-s*1.25:.1f} L{-s*.1:.1f},{-s*.95:.1f} C{-s*.25:.1f},{-s*.85:.1f} {-s*.5:.1f},{-s*.55:.1f} {-s*.45:.1f},{-s*.18:.1f}Z" '
            f'fill="url(#stone)" stroke="{LINE}" stroke-width=".8"/>'
            f'<circle cy="{-s*1.32:.1f}" r="{s*.1:.1f}" fill="{STONE_M}" stroke="{LINE}" stroke-width=".6"/>'
            f'<path d="M{-s*.42:.1f},{-s*.3:.1f} H{s*.42:.1f}" stroke="{LINE}" stroke-width=".6" opacity=".7"/></g>')

def band(x1, x2, y1, y2, niches=0, ratnas=0, rsize=16):
    o = [f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="url(#stone)" stroke="{LINE}" stroke-width="1"/>']
    # cornice moldings
    o.append(f'<rect x="{x1-8}" y="{y2-8}" width="{x2-x1+16}" height="8" fill="{STONE_M}" stroke="{LINE}" stroke-width="1"/>')
    o.append(f'<rect x="{x1-4}" y="{y1}" width="{x2-x1+8}" height="6" fill="{STONE_L}" stroke="{LINE}" stroke-width=".8"/>')
    if niches:
        step = (x2 - x1) / niches
        for i in range(niches):
            nx = x1 + step * i + step * .2
            nw = step * .6
            o.append(f'<path d="M{nx:.1f},{y2-10} V{y1+14} q{nw/2:.1f},-6 {nw:.1f},0 V{y2-10}Z" fill="{STONE_D}" stroke="{LINE}" stroke-width=".7"/>')
    if ratnas:
        step = (x2 - x1) / (ratnas - 1)
        for i in range(ratnas):
            o.append(ratna(x1 + step * i, y1, rsize))
    return ''.join(o)

def candi():
    rnd = random.Random(4)
    W, H = 500, 760
    defs = (lin('stone', [(0, STONE_L, 1), (.55, STONE_M, 1), (1, STONE_D, 1)], 0, 0, 1, 0) +
            lin('stoneV', [(0, STONE_L, 1), (1, STONE_M, 1)]) +
            shadow('cds', 4, 0, 6, .35))
    o = ['<g filter="url(#cds)">']
    # roof tiers (top down)
    o.append(ratna(250, 52, 46))
    o.append(band(190, 310, 52, 92, niches=3, ratnas=4, rsize=18))
    o.append(band(150, 350, 92, 140, niches=5, ratnas=6, rsize=20))
    o.append(band(105, 395, 140, 192, niches=7, ratnas=8, rsize=22))
    o.append(band(62, 438, 192, 250, niches=9, ratnas=10, rsize=24))
    # main cornice
    o.append(f'<rect x="40" y="250" width="420" height="16" fill="{STONE_M}" stroke="{LINE}"/>')
    o.append(f'<rect x="50" y="266" width="400" height="10" fill="{STONE_D}" stroke="{LINE}"/>')
    # body
    body = 'M60,276 H440 V650 H60Z'
    door = 'M118,650 V340 H150 V322 H350 V340 H382 V650Z'
    o.append(f'<path d="{body} {door}" fill="url(#stone)" fill-rule="evenodd" stroke="{LINE}" stroke-width="1.2"/>')
    # stone courses
    for y in range(296, 650, 22):
        o.append(f'<path d="M60,{y} H118 M382,{y} H440" stroke="{LINE}" stroke-width=".6" opacity=".55"/>')
        off = 14 if (y // 22) % 2 else 0
        for x in range(60 + off, 118, 28):
            o.append(f'<path d="M{x},{y} v-22" stroke="{LINE}" stroke-width=".5" opacity=".4"/>')
        for x in range(382 + off, 440, 28):
            o.append(f'<path d="M{x},{y} v-22" stroke="{LINE}" stroke-width=".5" opacity=".4"/>')
    # side relief panels
    for px in (68, 394):
        for py in (360, 470, 570):
            o.append(f'<rect x="{px}" y="{py}" width="38" height="70" rx="3" fill="{STONE_D}" stroke="{LINE}" stroke-width=".8"/>'
                     f'<path d="M{px+19},{py+60} q-12,-14 0,-28 q12,-14 0,-26" stroke="{STONE_L}" stroke-width="2" fill="none" opacity=".7"/>'
                     f'<circle cx="{px+19}" cy="{py+16}" r="5" fill="none" stroke="{STONE_L}" stroke-width="1.5" opacity=".7"/>')
    # door frame with kala head and makara curls
    o.append(f'<path d="M104,650 V328 H136 V308 H364 V328 H396 V650 H382 V340 H350 V322 H150 V340 H118 V650Z" fill="{STONE_M}" stroke="{LINE}" stroke-width="1.2"/>')
    med = ['<g transform="translate(250,296)">',
           f'<path d="M-52,14 C-50,-18 -26,-36 0,-36 C26,-36 50,-18 52,14 L34,26 L-34,26Z" fill="{STONE_M}" stroke="{LINE}" stroke-width="1.2"/>']
    for i in range(8):
        med.append(f'<g transform="rotate({i*45})"><path d="M0,0 C-6,-6 -6,-16 0,-22 C6,-16 6,-6 0,0Z" fill="{STONE_L}" stroke="{LINE}" stroke-width=".9"/></g>')
    med.append(f'<circle r="6" fill="{STONE_D}" stroke="{LINE}"/><circle r="2.5" fill="{STONE_L}"/>')
    for sx in (-1, 1):
        med.append(f'<path d="M{sx*26},16 q{sx*10},-6 {sx*20},2 q{sx*6},6 {sx*0},10" stroke="{LINE}" stroke-width="1.4" fill="none"/>'
                   f'<path d="M{sx*52},14 q{sx*16},2 {sx*24},-12 q{sx*-4},-8 {sx*-12},-4" stroke="{LINE}" stroke-width="1.4" fill="none"/>')
    med.append('</g>')
    o.append(''.join(med))
    for sx in (-1, 1):
        cx = 250 + sx * 139
        o.append(f'<path d="M{cx},640 c{sx*-0},-30 {sx*22},-34 {sx*26},-12 c{sx*3},14 {sx*-12},20 {sx*-18},10" stroke="{LINE}" stroke-width="2" fill="none"/>')
    # base / steps
    o.append(f'<rect x="30" y="650" width="440" height="34" fill="url(#stone)" stroke="{LINE}"/>')
    o.append(f'<rect x="14" y="684" width="472" height="38" fill="url(#stone)" stroke="{LINE}"/>')
    o.append(f'<rect x="0" y="722" width="500" height="38" fill="url(#stone)" stroke="{LINE}"/>')
    for x in range(30, 470, 40):
        o.append(f'<rect x="{x+6}" y="658" width="28" height="18" fill="{STONE_D}" opacity=".55"/>')
    for i, y in enumerate(range(650, 760, 14)):
        w = 150 + i * 10
        o.append(f'<rect x="{250-w/2}" y="{y}" width="{w}" height="14" fill="{STONE_L}" stroke="{LINE}" stroke-width=".8"/>')
    for sx in (-1, 1):
        o.append(f'<path d="M{250+sx*80},650 L{250+sx*130},760 L{250+sx*112},760 L{250+sx*66},650Z" fill="{STONE_M}" stroke="{LINE}"/>')
    # weathering specks
    for _ in range(260):
        x, y = rnd.uniform(40, 460), rnd.uniform(60, 755)
        if 118 < x < 382 and 322 < y < 650: continue
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(.4,1.4):.1f}" fill="{LINE}" opacity="{rnd.uniform(.15,.4):.2f}"/>')
    o.append('</g>')
    # moss & small plants on ledges
    for _ in range(18):
        x = rnd.choice([rnd.uniform(60, 120), rnd.uniform(380, 440), rnd.uniform(20, 480)])
        y = rnd.choice([250, 192, 650, 684, 722])
        o.append(leaf(x, y, rnd.uniform(8, 14), 3, rnd.uniform(-160, -20), rnd.choice(PAL['leaf'][1:])))
    return svg(W, H, ''.join(o), defs)

# ------------------------------------------------------------ small emblem above event title 120x90
def emblem():
    rnd = random.Random(8)
    defs = lin('em', [(0, '#fffaf0', 1), (.3, '#efe2c8', 1), (1, '#cdb68a', 1)])
    o = ['<path d="M5,88 L45,40 L60,22 L75,40 L115,88Z" fill="url(#em)"/>',
         '<path d="M60,22 L54,34 L61,31 L66,38 L75,40Z" fill="#fff"/>']
    for a, L in [(-120, 30), (-60, 30), (-100, 22), (-80, 24)]:
        o.append(leaf(60, 60, L, 6, a, rnd.choice(PAL['leaf'][2:])))
    o.append(rose(52, 46, 9, PAL['cream'], rnd))
    o.append(rose(68, 50, 8, PAL['cream'], rnd))
    o.append(rose(60, 34, 7, PAL['cream'], rnd))
    return svg(120, 90, ''.join(o), defs)
