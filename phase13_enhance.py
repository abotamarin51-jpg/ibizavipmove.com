from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path('_site')

# Same editorial photos, delivered at dimensions/quality that are ample for modern desktop and mobile.
OPTIMIZED = {
    'hero': 'https://images.unsplash.com/photo-1782113326494-87602b41cbdf?auto=format&fit=crop&w=2000&q=84&fm=jpg',
    'villa': 'https://images.unsplash.com/photo-1778694276931-056406c4f4d9?auto=format&fit=crop&w=2000&q=84&fm=jpg',
    'yacht': 'https://images.unsplash.com/photo-1779987680720-ca6e1b6fb4b0?auto=format&fit=crop&w=2000&q=84&fm=jpg',
    'chauffeur': 'https://images.unsplash.com/photo-1780296269553-84ec2dd53065?auto=format&fit=crop&w=2000&q=84&fm=jpg',
    'nightlife': 'https://images.unsplash.com/photo-1778694276945-a3ee92331709?auto=format&fit=crop&w=1800&q=84&fm=jpg',
    'events': 'https://images.unsplash.com/photo-1770140304098-46700a5c45c8?auto=format&fit=crop&w=1800&q=84&fm=jpg',
    'chef': 'https://images.unsplash.com/photo-1653233797467-1a528819fd4f?auto=format&fit=crop&w=1800&q=82&fm=jpg',
}

out = ROOT / 'assets' / 'images'
for name, url in OPTIMIZED.items():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 IbizaVIPMoveBuild/1.0'})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    if len(data) < 40_000:
        raise SystemExit(f'Optimized {name} unexpectedly small: {len(data)}')
    (out / f'{name}.jpg').write_bytes(data)
    print(f'Optimized {name}: {len(data):,} bytes')

# Phase 12 PNG favicon is the single favicon declaration.
svg_icon = '<link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml">'
svg_apple = '<link rel="apple-touch-icon" href="/assets/brand-mark.svg">'
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    text = text.replace(svg_icon, '').replace(svg_apple, '')
    path.write_text(text, encoding='utf-8')

home = (ROOT / 'index.html').read_text(encoding='utf-8')
if home.count('rel="icon"') != 1 or '/favicon.png' not in home:
    raise SystemExit('Expected exactly one PNG favicon declaration on homepage')
if (out / 'hero.jpg').stat().st_size > 900_000:
    raise SystemExit('Hero remains heavier than performance target')
if (out / 'chef.jpg').stat().st_size > 900_000:
    raise SystemExit('Chef remains heavier than performance target')
print('PASS: Phase 13 performance polish')
