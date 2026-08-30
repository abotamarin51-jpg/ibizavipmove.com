from pathlib import Path
import json
import re

ROOT = Path('_site')
OLD_PHONE = '+34 613 75 62 11'
OLD_WA = '34613756211'
NEW_PHONE = '+34 600 703 303'
NEW_WA = '34600703303'

all_pages = sorted(p for p in ROOT.rglob('index.html'))
pages = [
    p for p in all_pages
    if not re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', p.read_text(encoding='utf-8'), re.I)
]
if not pages:
    raise SystemExit('No indexable HTML pages were generated')

errors = []
titles = {}
canonicals = {}

for path in pages:
    text = path.read_text(encoding='utf-8')
    label = str(path.relative_to(ROOT))

    title = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', text, re.I)
    canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', text, re.I)
    h1s = re.findall(r'<h1\b[^>]*>', text, re.I)
    schemas = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.I | re.S)

    if not title or not title.group(1).strip():
        errors.append(f'{label}: missing title')
    else:
        value = re.sub(r'\s+', ' ', title.group(1)).strip()
        titles.setdefault(value, []).append(label)

    if not desc or len(desc.group(1).strip()) < 50:
        errors.append(f'{label}: missing or weak meta description')

    if not canonical or not canonical.group(1).startswith('https://ibizavipmove.com'):
        errors.append(f'{label}: missing/invalid canonical')
    else:
        canonicals.setdefault(canonical.group(1), []).append(label)

    if len(h1s) != 1:
        errors.append(f'{label}: expected exactly one H1, found {len(h1s)}')

    if '/assets/brand-logo.svg' not in text:
        errors.append(f'{label}: logo reference missing')

    if OLD_PHONE in text or OLD_WA in text:
        errors.append(f'{label}: old contact details still present')

    if not schemas:
        errors.append(f'{label}: no JSON-LD found')
    for idx, payload in enumerate(schemas, start=1):
        try:
            json.loads(payload)
        except Exception as exc:
            errors.append(f'{label}: invalid JSON-LD #{idx}: {exc}')

for title, files in titles.items():
    if len(files) > 1:
        errors.append(f'duplicate title "{title}" in {files}')

for canonical, files in canonicals.items():
    if len(files) > 1:
        errors.append(f'duplicate canonical "{canonical}" in {files}')

combined = '\n'.join(p.read_text(encoding='utf-8') for p in pages)
if NEW_PHONE not in combined or NEW_WA not in combined:
    errors.append('new phone/WhatsApp details are not present in generated pages')

sitemap = ROOT / 'sitemap.xml'
robots = ROOT / 'robots.txt'
if not sitemap.is_file() or 'https://ibizavipmove.com/' not in sitemap.read_text(encoding='utf-8'):
    errors.append('sitemap.xml missing or invalid')
if not robots.is_file() or 'Sitemap: https://ibizavipmove.com/sitemap.xml' not in robots.read_text(encoding='utf-8'):
    errors.append('robots.txt missing sitemap declaration')

if errors:
    print('\n'.join('FAIL: ' + e for e in errors))
    raise SystemExit(f'{len(errors)} validation issue(s) found')

print(f'PASS: validated {len(pages)} indexable pages, unique titles/canonicals, H1s, JSON-LD, contact details, sitemap and robots')
