from pathlib import Path
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
IMAGE = BASE + '/assets/images/private-office.jpg'

PAGES = [
 '/partners/','/private-office/',
 '/es/partners/','/es/private-office/',
 '/fr/partners/','/fr/private-office/',
 '/de/partners/','/de/private-office/',
 '/ar/partners/','/ar/private-office/'
]


def title_of(html):
    m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def desc_of(html):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
    return m.group(1).strip() if m else ''


def set_meta(html, attr, key, value):
    pattern = rf'(<meta\s+{attr}="{re.escape(key)}"\s+content=")[^"]*(")'
    if re.search(pattern, html, re.I):
        return re.sub(pattern, lambda m: m.group(1) + value + m.group(2), html, count=1, flags=re.I)
    return html.replace('</head>', f'<meta {attr}="{key}" content="{value}"></head>', 1)

updated = 0
for path in PAGES:
    file = ROOT / path.strip('/') / 'index.html'
    if not file.exists():
        raise SystemExit(f'Phase 56 target missing: {path}')
    html = file.read_text(encoding='utf-8')
    title = title_of(html)
    desc = desc_of(html)
    if not title or not desc:
        raise SystemExit(f'Phase 56 metadata missing: {path}')
    html = set_meta(html, 'property', 'og:title', title)
    html = set_meta(html, 'property', 'og:description', desc)
    html = set_meta(html, 'property', 'og:image', IMAGE)
    html = set_meta(html, 'property', 'og:image:secure_url', IMAGE)
    html = set_meta(html, 'property', 'og:image:type', 'image/jpeg')
    html = set_meta(html, 'property', 'og:image:alt', 'Ibiza VIP Move · Private Office & B2B Partnerships in Ibiza')
    html = set_meta(html, 'name', 'twitter:card', 'summary_large_image')
    html = set_meta(html, 'name', 'twitter:title', title)
    html = set_meta(html, 'name', 'twitter:description', desc)
    html = set_meta(html, 'name', 'twitter:image', IMAGE)
    file.write_text(html, encoding='utf-8')
    updated += 1

for path in PAGES:
    html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
    assert f'property="og:image" content="{IMAGE}"' in html, path
    assert f'name="twitter:image" content="{IMAGE}"' in html, path
    assert 'name="twitter:card" content="summary_large_image"' in html, path
    assert html.count('<h1') == 1, path

print(f'PASS: Phase 56 premium social preview metadata applied to {updated} five-language B2B pages')
