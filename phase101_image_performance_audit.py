from pathlib import Path
import re

ROOT = Path('_site')
IMG = ROOT / 'assets' / 'images'
HOME = ROOT / 'index.html'

LIMITS = {
    'hero-desktop.jpg': 500_000,
    'hero-mobile.jpg': 190_000,
    'hero.jpg': 700_000,
    'villa.jpg': 720_000,
    'yacht.jpg': 460_000,
    'chauffeur.jpg': 395_000,
    'nightlife.jpg': 515_000,
    'events.jpg': 335_000,
    'chef.jpg': 270_000,
    'aviation.jpg': 485_000,
}

sizes = {}
for name, limit in LIMITS.items():
    p = IMG / name
    if not p.exists():
        raise SystemExit(f'Phase 101 audit missing image: {name}')
    size = p.stat().st_size
    sizes[name] = size
    if size >= limit:
        raise SystemExit(f'Phase 101 audit image exceeds performance ceiling: {name} {size} >= {limit}')

# The former production set was ~4.68 MB for these ten assets. Require a
# material aggregate improvement while leaving visual dimensions unchanged.
total = sum(sizes.values())
if total >= 4_350_000:
    raise SystemExit(f'Phase 101 audit aggregate image budget exceeded: {total:,} bytes')

html = HOME.read_text(encoding='utf-8')
if '/assets/images/hero-mobile.jpg' not in html or '/assets/images/hero-desktop.jpg' not in html:
    raise SystemExit('Phase 101 audit responsive homepage hero sources missing')
hero = re.search(r'<img\b[^>]*class=["\'][^"\']*hero-media[^"\']*["\'][^>]*>', html, re.I)
if not hero:
    raise SystemExit('Phase 101 audit semantic hero image missing')
tag = hero.group(0)
if 'fetchpriority="high"' not in tag or 'loading="lazy"' in tag:
    raise SystemExit('Phase 101 audit homepage hero priority regressed')
if 'width="2200"' not in tag or 'height="1400"' not in tag:
    raise SystemExit('Phase 101 audit homepage hero rendered dimensions changed')

print(f'PASS: Phase 101 image performance audit — 10 key assets total {total:,} bytes; responsive LCP hero priority and dimensions preserved')
