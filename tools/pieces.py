import math, random
from lib import *

G = PAL['leaf']

def flower_mix(x, y, s, rnd, kinds=('rose', 'mum', 'cream', 'hib')):
    k = rnd.choice(kinds)
    if k == 'rose': return rose(x, y, s, PAL['red'], rnd)
    if k == 'mum': return mum(x, y, s, PAL['orange'], rnd)
    if k == 'cream': return rose(x, y, s * .7, PAL['cream'], rnd)
    if k == 'hib': return hibiscus(x, y, s * 1.1, PAL['red'][1:], rnd)
    if k == 'lily': return lily(x, y, s * 1.2, PAL['cream'], rnd)
    return ''

# ------------------------------------------------------------ cloud 250x115
def cloud():
    rnd = random.Random(3)
    defs = blur('cb', 3) + blur('cb2', 7) + lin('cg', [(0, '#ffffff', 1), (.65, '#fbf6ec', 1), (1, '#e6d8bf', 1)])
    blobs = [(70, 70, 34), (105, 52, 42), (150, 48, 40), (185, 66, 32), (125, 75, 38), (45, 82, 22), (210, 82, 20), (165, 82, 30)]
    shade = ''.join(f'<circle cx="{x}" cy="{y+6}" r="{r}" fill="#d8c6a6" opacity=".55"/>' for x, y, r in blobs)
    main = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#cg)"/>' for x, y, r in blobs)
    puffs = ''.join(f'<circle cx="{rnd.uniform(40,210):.0f}" cy="{rnd.uniform(30,70):.0f}" r="{rnd.uniform(6,14):.0f}" fill="#fff" opacity=".7"/>' for _ in range(14))
    body = f'<g filter="url(#cb2)" opacity=".7">{shade}</g><g filter="url(#cb)">{main}{puffs}</g>'
    return svg(250, 115, body, defs)

# ------------------------------------------------------------ butterflies
def butterfly(c1, c2, c3, seed):
    rnd = random.Random(seed)
    def wing(flip):
        s = -1 if flip else 1
        up = (f'M0,0 C{s*10},-28 {s*40},-38 {s*44},-22 C{s*46},-10 {s*30},2 0,4Z')
        lo = (f'M0,4 C{s*24},6 {s*34},22 {s*24},32 C{s*14},38 {s*4},22 0,8Z')
        veins = ''.join(f'<path d="M0,2 L{s*x},{y}" stroke="{c3}" stroke-width=".9" opacity=".8"/>' for x, y in [(42, -24), (36, -32), (28, -6), (26, 26), (16, 32)])
        dots = ''.join(f'<circle cx="{s*x}" cy="{y}" r="1.6" fill="#fff8e8"/>' for x, y in [(40, -22), (42, -15), (36, -30), (24, 30), (30, 22)])
        return (f'<path d="{up}" fill="url(#bw)" stroke="{c3}" stroke-width="2.2"/>'
                f'<path d="{lo}" fill="{c2}" stroke="{c3}" stroke-width="2"/>{veins}{dots}')
    defs = lin('bw', [(0, c2, 1), (1, c1, 1)], 0, 1, 1, 0)
    body = (f'<g transform="translate(39,40) rotate(-18) scale(.8)">'
            f'<g transform="scale(.82,1)">{wing(True)}</g>{wing(False)}'
            f'<ellipse cx="0" cy="8" rx="2.4" ry="13" fill="{c3}"/>'
            f'<path d="M0,-4 Q-4,-16 -9,-20 M0,-4 Q4,-16 9,-20" stroke="{c3}" stroke-width=".9" fill="none"/></g>')
    return svg(75, 75, body, defs)

# ------------------------------------------------------------ cream flower stem 75x147 (origin bottom)
def stem(seed, n=3):
    rnd = random.Random(seed)
    out = []
    pts = [(37 + rnd.uniform(-4, 4), 147), (38, 100), (36 + rnd.uniform(-6, 6), 55), (40, 20)]
    out.append(f'<path d="M{pts[0][0]:.0f},{pts[0][1]} C{pts[1][0]},{pts[1][1]} {pts[2][0]:.0f},{pts[2][1]} {pts[3][0]},{pts[3][1]}" stroke="#4f6d32" stroke-width="2.2" fill="none"/>')
    for t, s in [(.25, -1), (.4, 1), (.55, -1), (.72, 1), (.85, -1)]:
        y = 147 - t * 127
        out.append(leaf(38, y, rnd.uniform(16, 22), 5.5, -90 + s * rnd.uniform(35, 60), rnd.choice(G[1:4])))
    # side branches with flowers
    heads = [(40, 22, 15), (22 + rnd.uniform(-3, 3), 52, 12), (54, 72, 11)][:n]
    for hx, hy, r in heads:
        out.append(f'<path d="M38,{hy+18} Q{(38+hx)/2},{hy+10} {hx},{hy}" stroke="#4f6d32" stroke-width="1.6" fill="none"/>')
    for hx, hy, r in heads:
        out.append(rose(hx, hy, r, PAL['cream'], rnd))
    out.append(bud(30, 92, 5, PAL['cream'][1], -25))
    return svg(75, 147, ''.join(out), shadow('ds', 1.5, 1, 1.5, .3).replace('id="ds"', 'id="ds"'))

# ------------------------------------------------------------ monstera corner 160x165 (anchored top-left)
def corner(seed):
    rnd = random.Random(seed)
    out = []
    out.append(frond(-5, -5, 150, 62, G[0], n=12, rnd=rnd, droop=.15))
    out.append(monstera(-10, 10, 120, 38, G[2], rnd))
    out.append(monstera(-8, -6, 95, 12, G[3], rnd))
    out.append(banana(0, 0, 110, 75, G[1], rnd))
    out.append(monstera(10, -10, 70, 58, G[4], rnd))
    return svg(160, 165, ''.join(out), shadow('cs', 2, 2, 3, .35))

# ------------------------------------------------------------ garland 750x318 (hanging from top)
def garland(seed):
    rnd = random.Random(seed)
    W, H = 750, 318
    back, mid, front = [], [], []
    def depth(x):  # hanging length profile: long at sides, short in center
        d = abs(x - W / 2) / (W / 2)
        return 60 + 230 * d ** 1.6
    x = -20
    while x < W + 20:
        L = depth(x) * rnd.uniform(.7, 1.05)
        ang = 90 + rnd.uniform(-35, 35) + (x - W / 2) / W * -30
        r = rnd.random()
        if r < .35:
            back.append(frond(x, -10, L, ang, rnd.choice(G[:2]), n=12, rnd=rnd, droop=rnd.uniform(-.2, .2)))
        elif r < .6:
            mid.append(monstera(x, -10, L * .55, ang + rnd.uniform(-20, 20), rnd.choice(G[1:4]), rnd))
        elif r < .8:
            mid.append(banana(x, -10, L * .8, ang, rnd.choice(G[1:4]), rnd))
        else:
            front.append(leaf(x, -6, L * .45, L * .1, ang, rnd.choice(G[2:]), curve=rnd.uniform(-.1, .1)))
        x += rnd.uniform(14, 30)
    # vines
    for _ in range(9):
        vx = rnd.uniform(30, W - 30)
        L = depth(vx) * rnd.uniform(.6, 1.2)
        front.append(f'<path d="M{vx:.0f},0 q{rnd.uniform(-20,20):.0f},{L/2:.0f} {rnd.uniform(-10,10):.0f},{L:.0f}" stroke="#4f6d32" stroke-width="1.2" fill="none"/>')
        for k in range(6):
            t = (k + 1) / 7
            front.append(leaf(vx + rnd.uniform(-6, 6), L * t, 9, 3.5, rnd.choice((30, 150)) + rnd.uniform(-15, 15), rnd.choice(G[2:])))
    # a few flowers tucked at sides
    for _ in range(10):
        side = rnd.choice((0, 1))
        fx = rnd.uniform(0, 140) if side == 0 else rnd.uniform(W - 140, W)
        fy = rnd.uniform(10, depth(fx) * .55)
        front.append(flower_mix(fx, fy, rnd.uniform(8, 13), rnd))
    defs = shadow('gs', 2.5, 0, 3, .4)
    body = f'<g opacity=".9">{"".join(back)}</g><g filter="url(#gs)">{"".join(mid)}{"".join(front)}</g>'
    return svg(W, H, body, defs)

# ------------------------------------------------------------ flowerbed 750x398 (bottom)
def flowerbed(seed):
    rnd = random.Random(seed)
    W, H = 750, 398
    def top(x):  # mound height: tall sides, low centre
        d = abs(x - W / 2) / (W / 2)
        return H - (110 + 230 * d ** 1.3)
    back, mid, fl, front = [], [], [], []
    x = -30
    while x < W + 30:
        base = H + 10
        L = (base - top(x)) * rnd.uniform(.8, 1.15)
        ang = -90 + rnd.uniform(-38, 38) + (x - W / 2) / W * 40
        r = rnd.random()
        if r < .3:
            back.append(banana(x, base, L, ang, rnd.choice(G[:3]), rnd))
        elif r < .55:
            back.append(monstera(x, base, L * .62, ang, rnd.choice(G[1:4]), rnd))
        elif r < .8:
            mid.append(frond(x, base, L * .9, ang, rnd.choice(G[:3]), n=13, rnd=rnd, droop=rnd.uniform(-.25, .25)))
        else:
            mid.append(leaf(x, base, L * .7, L * .09, ang, rnd.choice(G[2:]), curve=rnd.uniform(-.15, .15)))
        x += rnd.uniform(8, 15)
    # flowers clustered along the mound line
    for _ in range(120):
        fx = rnd.uniform(-10, W + 10)
        t = top(fx)
        fy = rnd.uniform(t + 60, H + 5)
        s = rnd.uniform(9, 17) * (1.15 if abs(fx - W / 2) > 200 else .85)
        fl.append(flower_mix(fx, fy, s, rnd, ('rose', 'rose', 'mum', 'mum', 'cream', 'hib', 'lily')))
    for _ in range(26):
        fx = rnd.uniform(0, W); fy = rnd.uniform(top(fx) + 50, H)
        fl.append(berries(fx, fy, 7, PAL['red'][2], rnd))
    # foreground leaves at the very bottom
    for i in range(40):
        fx = rnd.uniform(-20, W + 20)
        front.append(leaf(fx, H + 8, rnd.uniform(35, 70), rnd.uniform(7, 12), -90 + rnd.uniform(-60, 60), rnd.choice(G[1:]), curve=rnd.uniform(-.2, .2)))
    defs = shadow('fs', 2, 0, 2, .35) + lin('fade', [(0, '#000', 0), (1, '#000', .25)])
    body = (f'<g opacity=".92">{"".join(back)}</g><g filter="url(#fs)">{"".join(mid)}{"".join(fl)}{"".join(front)}</g>')
    return svg(W, H, body, defs)

# ------------------------------------------------------------ corner bouquet 200x163 (bottom-left)
def bouquet(seed):
    rnd = random.Random(seed)
    out = []
    for i in range(10):
        out.append(banana(rnd.uniform(0, 60), 170, rnd.uniform(90, 140), -90 + rnd.uniform(-10, 55), rnd.choice(G[:4]), rnd))
    for i in range(6):
        out.append(frond(rnd.uniform(20, 120), 170, rnd.uniform(70, 110), -90 + rnd.uniform(-30, 60), rnd.choice(G), rnd=rnd))
    out.append(lily(48, 92, 34, PAL['orange'], rnd, ang=-10))
    out.append(lily(150, 128, 26, PAL['cream'], rnd, ang=15))
    out.append(hibiscus(105, 110, 22, PAL['red'][1:], rnd))
    out.append(rose(22, 140, 18, PAL['red'], rnd))
    out.append(mum(80, 145, 17, PAL['orange'], rnd))
    out.append(rose(130, 158, 15, PAL['cream'], rnd))
    for i in range(3):
        out.append(bud(rnd.uniform(110, 180), rnd.uniform(60, 110), 8, PAL['red'][2], rnd.uniform(-20, 40)))
    out.append(leaf(170, 165, 50, 9, -110, G[3]))
    out.append(leaf(190, 165, 40, 8, -70, G[2]))
    return svg(200, 163, ''.join(out), '')

# ------------------------------------------------------------ peacocks 160x224
def peacock(x, y, s, flip, seed):
    rnd = random.Random(seed)
    f = -1 if flip else 1
    o = [f'<g transform="translate({x},{y}) scale({f*s},{s})">']
    # long train: tapered feathers falling down and slightly back
    feathers = []
    for i in range(11):
        a = 78 + (i - 5) * 3.2 + rnd.uniform(-1.5, 1.5)
        L = 135 + rnd.uniform(-12, 18) - abs(i - 5) * 4
        ex, ey = math.cos(math.radians(a)) * L, 10 + math.sin(math.radians(a)) * L
        nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
        w = 9
        cx, cy = ex * .45 + 8, ey * .45
        feathers.append((ex, ey, nx, ny, w, cx, cy, a, L))
    for ex, ey, nx, ny, w, cx, cy, a, L in feathers:
        o.append(f'<path d="M-3,10 Q{cx-nx*w:.1f},{cy-ny*w:.1f} {ex-nx*w*.8:.1f},{ey-ny*w*.8:.1f} L{ex+nx*w*.8:.1f},{ey+ny*w*.8:.1f} Q{cx+nx*w:.1f},{cy+ny*w:.1f} 5,10Z" fill="url(#ptrain)" stroke="#3f4a1e" stroke-width=".5"/>')
    for ex, ey, nx, ny, w, cx, cy, a, L in feathers:
        o.append(f'<path d="M1,10 Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}" stroke="#d9c27a" stroke-width=".6" fill="none" opacity=".8"/>')
        for t, sc in ((.55, .7), (1.0, 1.0)):
            px = (1 - t) ** 2 * 1 + 2 * (1 - t) * t * cx + t * t * ex
            py = (1 - t) ** 2 * 10 + 2 * (1 - t) * t * cy + t * t * ey
            o.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate({a-90:.0f}) scale({sc})">'
                     f'<ellipse rx="6.5" ry="8.5" fill="#a8892f"/><ellipse rx="5" ry="6.6" fill="#e3c76a"/>'
                     f'<ellipse rx="3.6" ry="4.8" fill="#2f7a6a"/><ellipse rx="2.1" ry="2.9" cy="-.4" fill="#1d2f52"/></g>')
    # body
    o.append('<path d="M-13,6 C-12,-10 8,-16 18,-4 C26,8 16,26 0,30 C-12,26 -16,16 -13,6Z" fill="#1f5c6e"/>')
    o.append('<path d="M-2,2 C6,-8 18,-4 20,6 C16,18 4,24 -4,18Z" fill="#b8925a"/>')
    for i in range(6):
        o.append(f'<path d="M{-1+i*3},{2+i*2.4} q7,1 11,7" stroke="#6b4a26" stroke-width=".8" fill="none"/>')
    # neck & head
    o.append('<path d="M-12,4 C-17,-10 -15,-26 -7,-35 C-3,-40 4,-38 4,-32 C2,-26 -4,-18 -2,0Z" fill="#1e6a8a"/>')
    o.append('<path d="M-9,-6 C-12,-16 -10,-26 -5,-31" stroke="#3aa0a8" stroke-width="2" fill="none" opacity=".7"/>')
    o.append('<circle cx="-1" cy="-34" r="5.5" fill="#1e6a8a"/>')
    o.append('<path d="M3.5,-35 l7,2 l-7,2Z" fill="#c9a46a"/>')
    o.append('<path d="M-1,-36.5 l4,0" stroke="#fff" stroke-width="1.3"/><circle cx="1" cy="-35" r="1" fill="#111"/>')
    for i in range(5):
        o.append(f'<path d="M-2,-39 L{-6+i*2.6:.1f},{-50+abs(i-2)}" stroke="#1e6a8a" stroke-width=".7"/><circle cx="{-6+i*2.6:.1f}" cy="{-50+abs(i-2)}" r="1.5" fill="#2e9a8a"/>')
    o.append('<path d="M3,27 l-3,10 M9,25 l1,11" stroke="#6b4a26" stroke-width="1.6"/>')
    o.append('</g>')
    return ''.join(o)

def peacocks(seed):
    rnd = random.Random(seed)
    out = []
    # branch
    out.append('<path d="M-5,100 C40,92 80,90 120,84 C140,80 155,82 165,76" stroke="#5b3d24" stroke-width="5" fill="none" stroke-linecap="round"/>')
    out.append('<path d="M70,90 C80,130 95,170 92,224" stroke="#5b3d24" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    for _ in range(14):
        bx, by = rnd.uniform(10, 150), rnd.uniform(78, 104)
        out.append(leaf(bx, by, rnd.uniform(10, 16), 4, rnd.uniform(-160, 20), rnd.choice(G[1:])))
    out.append(peacock(60, 70, .72, False, seed))
    out.append(peacock(124, 104, .46, True, seed + 1))
    for _ in range(26):
        fx, fy = rnd.uniform(40, 150), rnd.uniform(150, 222)
        out.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{rnd.uniform(2.2,4):.1f}" fill="{rnd.choice(PAL["pink"]+PAL["red"][2:])}"/>')
    for _ in range(8):
        out.append(rose(rnd.uniform(55, 140), rnd.uniform(160, 220), rnd.uniform(5, 8), PAL['red'], rnd))
    return svg(160, 224, ''.join(out), lin('ptrain', [(0, '#3d6b3a', 1), (.6, '#6f7a2e', 1), (1, '#9a8a3a', 1)]))
