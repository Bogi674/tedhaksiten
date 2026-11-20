import math, random

PAL = dict(
    leaf=['#3d5628', '#4f6d32', '#5f7d3a', '#71904a', '#86a356'],
    leaf_dark='#2a3d1c', leaf_light='#a9bd6e',
    red=['#5a0c12', '#7a1016', '#9b1c1f', '#b8322c', '#cf4a3a'],
    orange=['#b8501a', '#d9661f', '#ec8a32', '#f4a849', '#f9c56d'],
    cream=['#a8875a', '#e6d3aa', '#f5e9cf', '#fffaf0', '#ffffff'],
    pink=['#a8433f', '#c45f55', '#dc8577', '#ecaa9a'],
)

_id = [0]
def uid(p='g'):
    _id[0] += 1
    return f'{p}{_id[0]}'

def svg(w, h, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{body}</svg>')

def lin(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'

def rad(id_, stops, cx=.5, cy=.5, r=.5):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'

def blur(id_, sd):
    return f'<filter id="{id_}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>'

def shadow(id_, sd=2, dx=1, dy=2, op=.35):
    return (f'<filter id="{id_}" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{sd}" flood-color="#1a0f08" flood-opacity="{op}"/></filter>')

# ---------------------------------------------------------------- leaves
def leaf(x, y, L, W, ang, col, dark=None, vein=True, curve=0.0):
    """Lanceolate leaf from base (x,y) pointing at ang (deg)."""
    dark = dark or PAL['leaf_dark']
    c = curve * L
    p = (f'M0,0 C{L*.25},{-W} {L*.7},{-W*.8+c} {L},{c} '
         f'C{L*.7},{W*.8+c} {L*.25},{W} 0,0Z')
    half = (f'M0,0 C{L*.25},{W} {L*.7},{W*.8+c} {L},{c} '
            f'Q{L*.5},{c*.5} 0,0Z')
    v = ''
    if vein:
        v = f'<path d="M0,0 Q{L*.5},{c*.5} {L*.97},{c}" stroke="{dark}" stroke-opacity=".55" stroke-width="{max(.4,W*.08):.2f}" fill="none"/>'
        for t in (.25, .45, .65):
            vx = L * t
            v += (f'<path d="M{vx:.1f},{c*t*.5:.1f} q{L*.1:.1f},{-W*.45:.1f} {L*.18:.1f},{-W*.55:.1f}" stroke="{dark}" stroke-opacity=".3" stroke-width="{max(.3,W*.05):.2f}" fill="none"/>'
                  f'<path d="M{vx:.1f},{c*t*.5:.1f} q{L*.1:.1f},{W*.45:.1f} {L*.18:.1f},{W*.55:.1f}" stroke="{dark}" stroke-opacity=".3" stroke-width="{max(.3,W*.05):.2f}" fill="none"/>')
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
            f'<path d="{p}" fill="{col}"/><path d="{half}" fill="{dark}" fill-opacity=".28"/>{v}</g>')

def frond(x, y, L, ang, col, n=14, lw=None, rnd=None, droop=0.25):
    """Fern / palm frond: curved rachis with leaflets."""
    rnd = rnd or random
    lw = lw or L * .16
    out = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">']
    out.append(f'<path d="M0,0 Q{L*.5},{L*droop*.3} {L},{L*droop}" stroke="{PAL["leaf_dark"]}" stroke-width="{max(.6,L*.012):.2f}" fill="none"/>')
    for i in range(1, n + 1):
        t = i / (n + 1)
        px = L * t
        py = L * droop * t * t
        size = lw * (1 - t * .7)
        for s in (-1, 1):
            out.append(leaf(px, py, size * 1.0, size * .22, s * (55 - t * 20) + droop * 40 * t, col, vein=False))
    out.append('</g>')
    return ''.join(out)

def monstera(x, y, S, ang, col, rnd):
    """Monstera leaf, base at (x,y) pointing to ang."""
    mid = uid('m')
    holes = ''
    for i in range(5):
        t = .25 + i * .14
        for s in (-1, 1):
            a = s * (40 + i * 6)
            r = S * (.38 - abs(t - .55) * .35)
            cx = S * t
            holes += (f'<path d="M{cx:.1f},0 l{math.cos(math.radians(a))*r*1.4:.1f},{math.sin(math.radians(a))*r*1.4:.1f} '
                      f'l{-S*.035:.1f},{s*S*.02:.1f}Z" fill="black" stroke="black" stroke-width="{S*.03:.1f}" stroke-linejoin="round"/>')
    shape = (f'M0,0 C{S*.05},{-S*.55} {S*.75},{-S*.6} {S},{-S*.05} C{S*1.02},0 {S*1.02},0 {S},{S*.05} '
             f'C{S*.75},{S*.6} {S*.05},{S*.55} 0,0Z')
    mask = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{-S}" y="{-S}" width="{3*S}" height="{3*S}">'
            f'<path d="{shape}" fill="white"/>{holes}</mask>')
    veins = ''.join(
        f'<path d="M{S*(.2+i*.14):.1f},0 q{S*.1:.1f},{s*S*.15:.1f} {S*.2:.1f},{s*S*.32:.1f}" stroke="{PAL["leaf_dark"]}" stroke-opacity=".35" stroke-width="{S*.012:.2f}" fill="none"/>'
        for i in range(5) for s in (-1, 1))
    gid = uid('mg')
    return (f'<defs>{mask}{lin(gid, [(0, col, 1), (1, PAL["leaf_dark"], 1)], 0, 0, 1, 1)}</defs>'
            f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})"><g mask="url(#{mid})">'
            f'<path d="{shape}" fill="url(#{gid})"/>'
            f'<path d="M0,0 C{S*.05},{S*.55} {S*.75},{S*.6} {S},{S*.05} L{S},0 L0,0Z" fill="#000" fill-opacity=".12"/>{veins}</g>'
            f'<path d="M0,0 L{S*.98},0" stroke="{PAL["leaf_light"]}" stroke-opacity=".6" stroke-width="{S*.015:.2f}"/></g>')

def banana(x, y, L, ang, col, rnd):
    W = L * .22
    tears = ''
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
            f'<path d="M0,0 C{L*.2},{-W} {L*.8},{-W} {L},0 C{L*.8},{W} {L*.2},{W} 0,0Z" fill="{col}"/>'
            f'<path d="M0,0 C{L*.2},{W} {L*.8},{W} {L},0Z" fill="#000" fill-opacity=".18"/>'
            f'{tears}<path d="M0,0 L{L},0" stroke="{PAL["leaf_light"]}" stroke-opacity=".7" stroke-width="{L*.012:.2f}"/></g>')

# ---------------------------------------------------------------- flowers
def rose(x, y, r, pal, rnd, rot=None):
    rot = rnd.uniform(0, 360) if rot is None else rot
    d, m, l, hl = pal[0], pal[1], pal[2], pal[3]
    sw = max(.35, r * .07)
    o = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.0f})">', f'<circle r="{r*.55:.1f}" fill="{d}"/>']
    for k, (sc, n, col) in enumerate([(1.0, 5, m), (.8, 5, l), (.6, 4, m)]):
        off = k * 36 + rnd.uniform(-8, 8)
        R = r * sc
        for i in range(n):
            a = off + i * 360 / n
            o.append(f'<g transform="rotate({a:.0f})"><path d="M{-R*.62:.1f},{-R*.05:.1f} C{-R*.75:.1f},{-R*.9:.1f} {R*.75:.1f},{-R*.9:.1f} {R*.62:.1f},{-R*.05:.1f} Q0,{-R*.3:.1f} {-R*.62:.1f},{-R*.05:.1f}Z" '
                     f'fill="{col}" stroke="{d}" stroke-width="{sw:.2f}" stroke-linejoin="round"/>'
                     f'<path d="M{-R*.4:.1f},{-R*.62:.1f} Q0,{-R*.8:.1f} {R*.4:.1f},{-R*.62:.1f}" stroke="{hl}" stroke-width="{sw*.8:.2f}" fill="none" opacity=".7"/></g>')
    # cupped centre spiral
    c = r * .36
    o.append(f'<circle r="{c:.1f}" fill="{l}" stroke="{d}" stroke-width="{sw:.2f}"/>')
    o.append(f'<path d="M{-c*.7:.1f},{c*.2:.1f} C{-c*.7:.1f},{-c*.8:.1f} {c*.7:.1f},{-c*.8:.1f} {c*.6:.1f},{c*.1:.1f} C{c*.5:.1f},{c*.6:.1f} {-c*.3:.1f},{c*.6:.1f} {-c*.3:.1f},{0:.1f} C{-c*.3:.1f},{-c*.35:.1f} {c*.25:.1f},{-c*.35:.1f} {c*.2:.1f},{c*.05:.1f}" '
             f'stroke="{d}" stroke-width="{sw:.2f}" fill="{hl}" fill-opacity=".6"/>')
    o.append('</g>')
    return ''.join(o)

def mum(x, y, r, pal, rnd):
    """Chrysanthemum / marigold: dense radial petals."""
    out = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({rnd.uniform(0,360):.0f})">',
           f'<circle r="{r*.95:.1f}" fill="{pal[0]}"/>']
    rings = [(1.0, 18, pal[1]), (.82, 16, pal[2]), (.64, 14, pal[2]), (.46, 11, pal[3]), (.28, 8, pal[4])]
    for rr, n, col in rings:
        off = rnd.uniform(0, 30)
        R = r * rr
        for i in range(n):
            a = off + i * 360 / n
            out.append(f'<ellipse transform="rotate({a:.1f}) translate(0,{-R*.62:.1f})" rx="{R*.2:.1f}" ry="{R*.42:.1f}" '
                       f'fill="{col}" stroke="{pal[0]}" stroke-opacity=".5" stroke-width="{max(.25,r*.025):.2f}"/>')
    out.append(f'<circle r="{r*.12:.1f}" fill="{pal[1]}"/></g>')
    return ''.join(out)

def hibiscus(x, y, r, pal, rnd, ang=None):
    ang = rnd.uniform(0, 360) if ang is None else ang
    out = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f})">']
    for i in range(5):
        a = i * 72
        out.append(f'<g transform="rotate({a})"><path d="M0,0 C{-r*.7},{-r*.3} {-r*.7},{-r*1.05} 0,{-r} C{r*.7},{-r*1.05} {r*.7},{-r*.3} 0,0Z" fill="{pal[2]}" stroke="{pal[0]}" stroke-width="{r*.03:.2f}"/>'
                   f'<path d="M0,0 L0,{-r*.85}" stroke="{pal[0]}" stroke-opacity=".35" stroke-width="{r*.03:.2f}"/></g>')
    out.append(f'<circle r="{r*.25:.1f}" fill="{pal[0]}"/>')
    out.append(f'<path d="M0,0 Q{r*.4},{-r*.2} {r*.9},{-r*.35}" stroke="{PAL["orange"][3]}" stroke-width="{r*.06:.2f}" fill="none"/>'
               f'<circle cx="{r*.9:.1f}" cy="{-r*.35:.1f}" r="{r*.08:.1f}" fill="{PAL["orange"][4]}"/></g>')
    return ''.join(out)

def lily(x, y, r, pal, rnd, ang=None):
    ang = rnd.uniform(0, 360) if ang is None else ang
    out = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f})">']
    for i in range(6):
        a = i * 60 + (15 if i % 2 else 0)
        L = r * (1 if i % 2 == 0 else .9)
        out.append(f'<g transform="rotate({a})"><path d="M0,0 C{-L*.32},{-L*.35} {-L*.18},{-L*.85} 0,{-L} C{L*.18},{-L*.85} {L*.32},{-L*.35} 0,0Z" '
                   f'fill="{pal[3]}" stroke="{pal[0]}" stroke-opacity=".6" stroke-width="{r*.025:.2f}"/>'
                   f'<path d="M0,0 L0,{-L*.8}" stroke="{pal[1]}" stroke-opacity=".7" stroke-width="{r*.04:.2f}"/></g>')
    for i in range(6):
        a = i * 60 + 30
        out.append(f'<g transform="rotate({a})"><path d="M0,0 L0,{-r*.55}" stroke="{PAL["leaf"][2]}" stroke-width="{r*.025:.2f}"/>'
                   f'<ellipse cy="{-r*.58}" rx="{r*.05}" ry="{r*.1}" fill="{PAL["orange"][0]}"/></g>')
    out.append('</g>')
    return ''.join(out)

def bud(x, y, r, col, ang):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f})">'
            f'<path d="M0,0 C{-r*.6},{-r*.4} {-r*.4},{-r*1.4} 0,{-r*1.6} C{r*.4},{-r*1.4} {r*.6},{-r*.4} 0,0Z" fill="{col}"/>'
            f'<path d="M0,0 C{-r*.5},{-r*.3} {-r*.5},{-r*.7} {-r*.2},{-r*.9} M0,0 C{r*.5},{-r*.3} {r*.5},{-r*.7} {r*.2},{-r*.9}" stroke="{PAL["leaf"][1]}" stroke-width="{r*.25:.2f}" fill="none"/></g>')

def berries(x, y, r, col, rnd, n=6):
    return ''.join(f'<circle cx="{x+rnd.uniform(-r,r):.1f}" cy="{y+rnd.uniform(-r,r):.1f}" r="{rnd.uniform(r*.18,r*.3):.1f}" fill="{col}"/>' for _ in range(n))
