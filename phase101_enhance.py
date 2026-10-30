from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import re

ROOT = Path('_site')
IMG = ROOT / 'assets' / 'images'
HOME = ROOT / 'index.html'

# Preserve the reviewed, currently published image bytes during unrelated releases.
# Villa and chauffeur already use checksum-verified repository assets. Extend the
# existing same-origin hero checksum gate to the six remaining optimized images;
# a changed or unavailable source fails the build instead of changing the design.
# Dimensions, crop, image URLs and the original performance assertions stay intact.
SOURCES = {
    'hero.jpg': 'https://ibizavipmove.com/assets/images/hero.jpg',
    'yacht.jpg': 'https://ibizavipmove.com/assets/images/yacht.jpg',
    'nightlife.jpg': 'https://ibizavipmove.com/assets/images/nightlife.jpg',
    'events.jpg': 'https://ibizavipmove.com/assets/images/events.jpg',
    'chef.jpg': 'https://ibizavipmove.com/assets/images/chef.jpg',
    'aviation.jpg': 'https://ibizavipmove.com/assets/images/aviation.jpg',
    'hero-desktop.jpg': 'https://ibizavipmove.com/assets/images/hero-desktop.jpg',
    'hero-mobile.jpg': 'https://ibizavipmove.com/assets/images/hero-mobile.jpg',
}

FROZEN_VILLA = Path('editorial-assets/villa.jpg')
FROZEN_VILLA_SHA256 = '920a2d479f869c385e47bbaf7cec73235da990c450283a75c0fb8d687de945dd'
FROZEN_CHAUFFEUR = Path('editorial-assets/chauffeur.jpg')
FROZEN_CHAUFFEUR_SHA256 = '4e286f6c4a91148c0beb248ca354beba7a3f281c95d3b746b17ef102d9649484'

APPROVED_HERO_SHA256 = '10c61dbded805b7d23359f79ed59957988d55d2159a5cd8954adf55dab4b047f'
APPROVED_HERO_BYTES = 667_271
APPROVED_HERO_MOBILE_SHA256 = '93e8146cff4a8cfe66ecb412be2fca12d07a2d4e37aab081bca44703265eba78'
APPROVED_HERO_MOBILE_BYTES = 187_724

# Verified against the pre-release public site; no re-encoding or fallback.
APPROVED_REMOTE = {
    'hero.jpg': (APPROVED_HERO_BYTES, APPROVED_HERO_SHA256),
    'yacht.jpg': (439253, '3afc331cc9af5ec06dc51a51da8961ad37bdb1e96b879bdbc5c4c367e9754580'),
    'nightlife.jpg': (496646, '5f177be5068e0f9f15a407fdd622ea215dd289ec5a9ba120825f311bf6588233'),
    'events.jpg': (324693, '7436ca1bc46c164faea9e3d940de745a809a3654e3f81da7ea4599d99680b85f'),
    'chef.jpg': (261773, 'c799052b8f835cba2b09a22ad660e9428c33b7338f756a7cb0cce160b244eb4b'),
    'aviation.jpg': (452600, '1deee3ae10859b3b17fa930216b78cb3a5d71b12b3c00993d79b225765863d98'),
    'hero-desktop.jpg': (402346, '9c8452a6a47c701b3f71b7d8c9eb02c96c8874a578d90bd0b618e0945c37d225'),
    'hero-mobile.jpg': (APPROVED_HERO_MOBILE_BYTES, APPROVED_HERO_MOBILE_SHA256),
}

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
    expected = APPROVED_REMOTE[name]
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != expected[0] or digest != expected[1]:
        raise SystemExit(
            f'Phase 101 {name} production-baseline mismatch: '
            f'{len(data)} bytes / {digest}'
        )
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
