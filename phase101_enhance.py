from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path('_site')
IMG = ROOT / 'assets' / 'images'
HOME = ROOT / 'index.html'

# Phase 101 keeps the exact same editorial sources and visual treatment used by
# the mature site. Nine assets keep their rendered dimensions and receive a
# leaner JPEG encode. The desktop LCP hero keeps the exact same aspect/crop but
# is delivered at 2000x1273 instead of 2200x1400 — still above typical desktop
# display needs while reducing global transfer cost.
SOURCES = {
    'hero.jpg': 'https://images.unsplash.com/photo-1782113326494-87602b41cbdf?auto=format&fit=crop&w=2000&q=76&fm=jpg',
    'villa.jpg': 'https://images.unsplash.com/photo-1778694276931-056406c4f4d9?auto=format&fit=crop&w=2000&q=76&fm=jpg',
    'yacht.jpg': 'https://images.unsplash.com/photo-1779987680720-ca6e1b6fb4b0?auto=format&fit=crop&w=2000&q=78&fm=jpg',
    'chauffeur.jpg': 'https://images.unsplash.com/photo-1780296269553-84ec2dd53065?auto=format&fit=crop&w=2000&q=78&fm=jpg',
    'nightlife.jpg': 'https://images.unsplash.com/photo-1778694276945-a3ee92331709?auto=format&fit=crop&w=1800&q=76&fm=jpg',
    'events.jpg': 'https://images.unsplash.com/photo-1770140304098-46700a5c45c8?auto=format&fit=crop&w=1800&q=78&fm=jpg',
    'chef.jpg': 'https://images.unsplash.com/photo-1653233797467-1a528819fd4f?auto=format&fit=crop&w=1800&q=76&fm=jpg',
    'aviation.jpg': 'https://images.unsplash.com/photo-1770334618960-d246fc142297?auto=format&fit=crop&fm=jpg&q=78&w=2200',
    'hero-desktop.jpg': 'https://images.unsplash.com/photo-1631193722492-9eee3ca45896?auto=format&fit=crop&w=2000&h=1273&q=78&fm=jpg',
    'hero-mobile.jpg': 'https://images.unsplash.com/photo-1631193722492-9eee3ca45896?auto=format&fit=crop&w=900&h=1250&q=76&fm=jpg',
}

before = {}
after = {}
for name, url in SOURCES.items():
    target = IMG / name
    if not target.exists():
        raise SystemExit(f'Phase 101 expected existing image: {name}')
    before[name] = target.stat().st_size
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 IbizaVIPMoveBuild/1.0'})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    if len(data) < 40_000:
        raise SystemExit(f'Phase 101 optimized image unexpectedly small: {name} -> {len(data)} bytes')
    if len(data) >= before[name]:
        raise SystemExit(f'Phase 101 image did not improve: {name} {before[name]} -> {len(data)} bytes')
    target.write_bytes(data)
    after[name] = len(data)
    saved = before[name] - after[name]
    print(f'Phase 101 {name}: {before[name]:,} -> {after[name]:,} bytes (-{saved:,})')

# Target the stable LCP asset URL rather than a presentation class, because
# later visual phases may legitimately normalize classes while keeping this src.
html = HOME.read_text(encoding='utf-8')
hero = re.search(r'<img\b(?=[^>]*\bsrc=["\']/assets/images/hero-desktop\.jpg["\'])[^>]*>', html, re.I)
if not hero:
    raise SystemExit('Phase 101 homepage desktop hero img tag missing')
tag = hero.group(0)
new_tag, w_count = re.subn(r'\bwidth=["\']\d+["\']', 'width="2000"', tag, count=1, flags=re.I)
new_tag, h_count = re.subn(r'\bheight=["\']\d+["\']', 'height="1273"', new_tag, count=1, flags=re.I)
if w_count != 1 or h_count != 1:
    raise SystemExit(f'Phase 101 expected one hero width/height pair, found width={w_count} height={h_count}')
html = html[:hero.start()] + new_tag + html[hero.end():]
HOME.write_text(html, encoding='utf-8')

before_total = sum(before.values())
after_total = sum(after.values())
if after_total >= before_total:
    raise SystemExit('Phase 101 total image bytes did not improve')
print(f'PASS: Phase 101 global image performance — 10 key assets reduced from {before_total:,} to {after_total:,} bytes; desktop hero kept same crop/aspect at 2000x1273')
