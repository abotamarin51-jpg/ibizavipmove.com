from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'

# Phase 12: search appearance + editorial polish.
# Keep this post-processing small and deterministic so the existing architecture remains stable.

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if '</head>' not in text:
        continue

    # Stable, crawlable favicon for Google Search plus iOS homescreen icon.
    if '/favicon-96.png' not in text:
        icons = (
            '<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">'
            '<link rel="apple-touch-icon" href="/favicon-96.png">'
            '<meta name="theme-color" content="#090e13">'
        )
        text = text.replace('</head>', icons + '</head>', 1)

    # Make preferred image signals explicit and consistent where an OG image exists.
    og = re.search(r'<meta property="og:image" content="([^"]+)">', text)
    if og and 'itemprop="image"' not in text:
        image_url = og.group(1)
        text = text.replace(
            og.group(0),
            og.group(0) + f'<meta itemprop="image" content="{image_url}">',
            1,
        )

    path.write_text(text, encoding='utf-8')

# Remove internal/SEO-sounding copy from the public homepage.
home = ROOT / 'index.html'
if home.exists():
    text = home.read_text(encoding='utf-8')
    text = text.replace(
        'Six service universes on the homepage. The full specialist service architecture remains available for search and detailed planning.',
        'Private mobility, stays, yachts, access, aviation and lifestyle support — coordinated around the rhythm of your stay.'
    )
    home.write_text(text, encoding='utf-8')

# Give Private Office its own visual identity rather than reusing Security.
office = ROOT / 'private-office' / 'index.html'
if office.exists():
    text = office.read_text(encoding='utf-8')
    text = text.replace("--hero:url('/assets/images/security.jpg')", "--hero:url('/assets/images/private-office.jpg')")
    text = text.replace('https://ibizavipmove.com/assets/images/security.jpg', 'https://ibizavipmove.com/assets/images/private-office.jpg')
    text = text.replace('/assets/images/security.jpg', '/assets/images/private-office.jpg')
    office.write_text(text, encoding='utf-8')

# Add ImageObject to the Private Office page so the preferred visual is explicit.
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

# Hard checks specific to this phase.
checks = {
    'favicon copied': (ROOT / 'favicon-96.png').is_file() and (ROOT / 'favicon-96.png').stat().st_size > 1000,
    'home favicon link': '/favicon-96.png' in (ROOT / 'index.html').read_text(encoding='utf-8'),
    'home copy polished': 'Six service universes on the homepage' not in (ROOT / 'index.html').read_text(encoding='utf-8'),
    'private office image': (ROOT / 'assets' / 'images' / 'private-office.jpg').is_file(),
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if failed:
    raise SystemExit('Phase 12 validation failed: ' + ', '.join(failed))
