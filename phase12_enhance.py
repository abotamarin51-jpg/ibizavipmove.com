from pathlib import Path
import base64
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'

# Stable 180x180 PNG favicon generated from the Ibiza VIP Move visual identity.
FAVICON_B64 = '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'

favicon = ROOT / 'favicon.png'
favicon.write_bytes(base64.b64decode(FAVICON_B64))

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if '</head>' not in text:
        continue

    if '/favicon.png' not in text:
        icons = (
            '<link rel="icon" type="image/png" sizes="180x180" href="/favicon.png">'
            '<link rel="apple-touch-icon" href="/favicon.png">'
            '<meta name="theme-color" content="#090e13">'
        )
        text = text.replace('</head>', icons + '</head>', 1)

    og = re.search(r'<meta property="og:image" content="([^"]+)">', text)
    if og and 'itemprop="image"' not in text:
        image_url = og.group(1)
        text = text.replace(og.group(0), og.group(0) + f'<meta itemprop="image" content="{image_url}">', 1)

    path.write_text(text, encoding='utf-8')

home = ROOT / 'index.html'
if home.exists():
    text = home.read_text(encoding='utf-8')
    text = text.replace(
        'Six service universes on the homepage. The full specialist service architecture remains available for search and detailed planning.',
        'Private mobility, stays, yachts, access, aviation and lifestyle support — coordinated around the rhythm of your stay.'
    )
    home.write_text(text, encoding='utf-8')

office = ROOT / 'private-office' / 'index.html'
if office.exists():
    text = office.read_text(encoding='utf-8')
    text = text.replace("--hero:url('/assets/images/security.jpg')", "--hero:url('/assets/images/private-office.jpg')")
    text = text.replace('https://ibizavipmove.com/assets/images/security.jpg', 'https://ibizavipmove.com/assets/images/private-office.jpg')
    text = text.replace('/assets/images/security.jpg', '/assets/images/private-office.jpg')
    office.write_text(text, encoding='utf-8')

if office.exists():
    text = office.read_text(encoding='utf-8')
    if '"@type": "ImageObject"' not in text:
        image_schema = json.dumps({
            '@context': 'https://schema.org',
            '@type': 'ImageObject',
            'contentUrl': BASE + '/assets/images/private-office.jpg',
            'caption': 'Private Office support for principals, personal assistants and family offices in Ibiza',
            'representativeOfPage': True,
        }, ensure_ascii=False)
        text = text.replace('</head>', f'<script type="application/ld+json">{image_schema}</script></head>', 1)
        office.write_text(text, encoding='utf-8')

checks = {
    'favicon generated': favicon.is_file() and favicon.stat().st_size > 1000,
    'home favicon link': '/favicon.png' in (ROOT / 'index.html').read_text(encoding='utf-8'),
    'home copy polished': 'Six service universes on the homepage' not in (ROOT / 'index.html').read_text(encoding='utf-8'),
    'private office image': (ROOT / 'assets' / 'images' / 'private-office.jpg').is_file(),
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if failed:
    raise SystemExit('Phase 12 validation failed: ' + ', '.join(failed))
