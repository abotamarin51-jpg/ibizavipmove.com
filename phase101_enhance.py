from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import re

ROOT = Path('_site')
IMG = ROOT / 'assets' / 'images'
HOME = ROOT / 'index.html'

# Phase 101 keeps the exact same editorial sources and visual treatment used by
# the mature site. Phase 157 supplies villa.jpg and Phase 160 supplies
# chauffeur.jpg from checksum-verified, production-approved repository assets
# before this optimizer runs. The remaining eight assets keep their rendered
# dimensions and receive a leaner JPEG encode.
# The desktop LCP hero keeps the exact same aspect/crop but is delivered at
# 2000x1273 instead of 2200x1400 — still above typical desktop display needs
# while reducing global transfer cost.
SOURCES = {
    'hero.jpg': 'https://images.unsplash.com/photo-1782113326494-87602b41cbdf?auto=format&fit=crop&w=2000&q=76&fm=jpg',
    'yacht.jpg': 'https://images.unsplash.com/photo-1779987680720-ca6e1b6fb4b0?auto=format&fit=crop&w=2000&q=78&fm=jpg',
    'nightlife.jpg': 'https://images.unsplash.com/photo-1778694276945-a3ee92331709?auto=format&fit=crop&w=1800&q=76&fm=jpg',
    'events.jpg': 'https://images.unsplash.com/photo-1770140304098-46700a5c45c8?auto=format&fit=crop&w=1800&q=78&fm=jpg',
    'chef.jpg': 'https://images.unsplash.com/photo-1653233797467-1a528819fd4f?auto=format&fit=crop&w=1800&q=76&fm=jpg',
    'aviation.jpg': 'https://images.unsplash.com/photo-1770334618960-d246fc142297?auto=format&fit=crop&fm=jpg&q=78&w=2200',
    'hero-desktop.jpg': 'https://images.unsplash.com/photo-1631193722492-9eee3ca45896?auto=format&fit=crop&w=2000&h=1273&q=78&fm=jpg',
    # Keep extra headroom under the existing 190 KB audit ceiling because this
    # live Unsplash transform is re-encoded upstream and its bytes can vary.
    'hero-mobile.jpg': 'https://images.unsplash.com/photo-1631193722492-9eee3ca45896?auto=format&fit=crop&w=900&h=1250&q=72&fm=jpg',
}

FROZEN_VILLA = Path('editorial-assets/villa.jpg')
FROZEN_VILLA_SHA256 = '920a2d479f869c385e47bbaf7cec73235da990c450283a75c0fb8d687de945dd'
FROZEN_CHAUFFEUR = Path('editorial-assets/chauffeur.jpg')
FROZEN_CHAUFFEUR_SHA256 = '4e286f6c4a91148c0beb248ca354beba7a3f281c95d3b746b17ef102d9649484'

before = {}
after = {}

# Phase 13 predates the final performance pass and still replaces villa.jpg
# from a mutable transform. Restore the reviewed production bytes here so the
# final artifact is deterministic while preserving the established phase order.
villa_target = IMG / 'villa.jpg'
if not villa_target.exists() or not FROZEN_VILLA.exists():
    raise SystemExit('Phase 101 expected villa source and target')
villa_data = FROZEN_VILLA.read_bytes()
villa_digest = hashlib.sha256(villa_data).hexdigest()
if villa_digest != FROZEN_VILLA_SHA256:
    raise SystemExit(f'Phase 101 frozen villa checksum mismatch: {villa_digest}')
before['villa.jpg'] = villa_target.stat().st_size
villa_target.write_bytes(villa_data)
after['villa.jpg'] = len(villa_data)
print(
    f'Phase 101 villa.jpg: {before["villa.jpg"]:,} -> {after["villa.jpg"]:,} bytes '
    f'(pinned {villa_digest[:12]})'
)

# Restore the last reviewed production chauffeur bytes. The mutable upstream
# transform changed pixels during an unrelated release, so this asset must not
# drift silently in future builds.
chauffeur_target = IMG / 'chauffeur.jpg'
if not chauffeur_target.exists() or not FROZEN_CHAUFFEUR.exists():
    raise SystemExit('Phase 101 expected chauffeur source and target')
chauffeur_data = FROZEN_CHAUFFEUR.read_bytes()
chauffeur_digest = hashlib.sha256(chauffeur_data).hexdigest()
if chauffeur_digest != FROZEN_CHAUFFEUR_SHA256:
    raise SystemExit(f'Phase 101 frozen chauffeur checksum mismatch: {chauffeur_digest}')
before['chauffeur.jpg'] = chauffeur_target.stat().st_size
chauffeur_target.write_bytes(chauffeur_data)
after['chauffeur.jpg'] = len(chauffeur_data)
print(
    f'Phase 101 chauffeur.jpg: {before["chauffeur.jpg"]:,} -> {after["chauffeur.jpg"]:,} bytes '
    f'(pinned {chauffeur_digest[:12]})'
)

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
