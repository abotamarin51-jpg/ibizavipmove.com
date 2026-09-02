from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path('_site')
IMG = ROOT / 'assets' / 'images'
SOURCE = 'https://images.unsplash.com/photo-1782113326494-87602b41cbdf'

variants = {
    'hero-desktop.jpg': SOURCE + '?auto=format&fit=crop&w=1920&h=1200&q=82&fm=jpg',
    'hero-mobile.jpg': SOURCE + '?auto=format&fit=crop&w=900&h=1200&q=80&fm=jpg',
}

for name, url in variants.items():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 IbizaVIPMoveBuild/1.0'})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    if len(data) < 50_000:
        raise SystemExit(f'{name} unexpectedly small: {len(data)} bytes')
    (IMG / name).write_bytes(data)
    print(f'Phase 18 {name}: {len(data):,} bytes')

home_path = ROOT / 'index.html'
home = home_path.read_text(encoding='utf-8')
old = re.search(r'<img class="hero-media"[^>]*src="/assets/images/hero\.jpg"[^>]*>', home)
if not old:
    raise SystemExit('Homepage hero image markup not found')

picture = (
    '<picture class="hero-picture">'
    '<source media="(max-width: 700px)" srcset="/assets/images/hero-mobile.jpg">'
    '<img class="hero-media" src="/assets/images/hero-desktop.jpg" '
    'alt="Luxury private concierge experience overlooking the Mediterranean in Ibiza" '
    'width="1920" height="1200" fetchpriority="high" decoding="async">'
    '</picture>'
)
home = home[:old.start()] + picture + home[old.end():]

preload = (
    '<link rel="preload" as="image" href="/assets/images/hero-desktop.jpg" '
    'imagesrcset="/assets/images/hero-mobile.jpg 900w, /assets/images/hero-desktop.jpg 1920w" '
    'imagesizes="100vw" fetchpriority="high">'
)
if 'imagesrcset="/assets/images/hero-mobile.jpg 900w' not in home:
    home = home.replace('</title>', '</title>' + preload, 1)

home = home.replace(
    'https://ibizavipmove.com/assets/images/hero.jpg',
    'https://ibizavipmove.com/assets/images/hero-desktop.jpg'
)
home_path.write_text(home, encoding='utf-8')

# Keep the wrapper fully out of document flow while existing .hero-media styles
# continue to control crop, overlay and focal position.
css_path = ROOT / 'assets' / 'performance.css'
css = css_path.read_text(encoding='utf-8') if css_path.exists() else ''
rule = '\n.hero-picture{position:absolute;inset:0;display:block;width:100%;height:100%;z-index:-2}\n.hero-picture .hero-media{z-index:0}\n'
if '.hero-picture{' not in css:
    css += rule
css_path.write_text(css, encoding='utf-8')

# Release checks for the LCP path.
home = home_path.read_text(encoding='utf-8')
assert '/assets/images/hero-mobile.jpg' in home
assert '/assets/images/hero-desktop.jpg' in home
assert 'fetchpriority="high"' in home
assert 'loading="lazy"' not in picture
assert 'width="1920" height="1200"' in home
assert (IMG / 'hero-desktop.jpg').stat().st_size < 900_000
assert (IMG / 'hero-mobile.jpg').stat().st_size < 600_000
assert '.hero-picture{' in css_path.read_text(encoding='utf-8')
print('PASS: Phase 18 responsive LCP hero ready')
