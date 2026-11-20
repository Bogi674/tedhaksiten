import asyncio, sys, os, io
sys.path.insert(0, os.path.dirname(__file__))
from playwright.async_api import async_playwright
from PIL import Image
import pieces

OUT = '/home/claude/work/art/out'
os.makedirs(OUT, exist_ok=True)

def jobs():
    import scene
    return {
        'cloud': (pieces.cloud(), 2),
        'butterfly-a': (pieces.butterfly('#d9661f', '#f4a849', '#3a1f10', 1), 3),
        'butterfly-b': (pieces.butterfly('#7a1016', '#cf4a3a', '#2a1208', 2), 3),
        'stem-a': (pieces.stem(11, 3), 3),
        'stem-b': (pieces.stem(23, 2), 3),
        'corner': (pieces.corner(5), 2.5),
        'garland': (pieces.garland(7), 2),
        'flowerbed': (pieces.flowerbed(9), 2),
        'bouquet': (pieces.bouquet(13), 2.5),
        'peacocks': (pieces.peacocks(17), 2.5),
        'forest': (scene.forest(31), 2),
        'candi': (scene.candi(), 2),
        'emblem': (scene.emblem(), 3),
    }

async def main(only=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for name, (s, scale) in jobs().items():
            if only and name not in only:
                continue
            open(f'{OUT}/{name}.svg', 'w').write(s)
            import re
            w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
            pg = await b.new_page(viewport={'width': int(w), 'height': int(h)}, device_scale_factor=scale)
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{s}</body></html>')
            png = await pg.screenshot(omit_background=True, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            im = Image.open(io.BytesIO(png))
            opaque = name == 'forest'
            im.save(f'{OUT}/{name}.webp', 'WEBP', quality=82 if opaque else 88, method=6)
            print(name, im.size, os.path.getsize(f'{OUT}/{name}.webp') // 1024, 'KB', len(s) // 1024, 'KB svg')
            await pg.close()
        await b.close()

asyncio.run(main(sys.argv[1:] or None))
