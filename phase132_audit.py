"""Audit the Phase 132 English services-hub heading clarity change."""
from pathlib import Path
import re

ROOT = Path('_site')
PAGE = ROOT / 'services' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
URL = 'https://ibizavipmove.com/services/'
EXPECTED_H1_TEXT = 'Luxury concierge services in Ibiza, connected through one trusted contact.'
EXPECTED_TITLE = 'Luxury Concierge Services Ibiza | Ibiza VIP Move'
REQUIRED_LINKS = (
    '/personal-concierge-ibiza/',
    '/luxury-travel-concierge-ibiza/',
    '/luxury-lifestyle-management-ibiza/',
    '/vip-services-ibiza/',
    '/private-client-services-ibiza/',
    '/destination-management-ibiza/',
)

if not PAGE.is_file():
    raise SystemExit('Phase 132 audit missing services page')
html = PAGE.read_text(encoding='utf-8')

h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', html, re.I | re.S)
if len(h1s) != 1:
    raise SystemExit(f'Phase 132 audit expected one H1: {len(h1s)}')
h1_text = re.sub(r'<[^>]+>', ' ', h1s[0])
h1_text = re.sub(r'\s+', ' ', h1_text).strip()
if h1_text != EXPECTED_H1_TEXT:
    raise SystemExit(f'Phase 132 audit unexpected H1: {h1_text!r}')

m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
if not m or re.sub(r'\s+', ' ', m.group(1)).strip() != EXPECTED_TITLE:
    raise SystemExit('Phase 132 audit title drift')

if not re.search(r'<meta\s+name=["\']description["\'][^>]+content=["\'][^"\']*luxury concierge services in Ibiza', html, re.I):
    raise SystemExit('Phase 132 audit meta description no longer states luxury concierge services in Ibiza')
if html.count(f'<link rel="canonical" href="{URL}">') != 1:
    raise SystemExit('Phase 132 audit self-canonical drift')
if re.search(r'<meta\s+name=["\']robots["\'][^>]+noindex', html, re.I):
    raise SystemExit('Phase 132 audit services page unexpectedly noindex')

for href in REQUIRED_LINKS:
    if f'href="{href}"' not in html:
        raise SystemExit(f'Phase 132 audit missing Phase 128 service-model link: {href}')

if not SITEMAP.is_file():
    raise SystemExit('Phase 132 audit sitemap missing')
xml = SITEMAP.read_text(encoding='utf-8')
if xml.count(f'<loc>{URL}</loc>') != 1:
    raise SystemExit('Phase 132 audit services sitemap URL cardinality drift')
if xml.count('<loc>') != 156:
    raise SystemExit(f'Phase 132 audit sitemap inventory drift: {xml.count("<loc>")}')

print('PASS: Phase 132 audit — /services/ has one descriptive Ibiza concierge H1, preserved metadata/canonical/indexability, all six service-model links, and the unchanged 156-URL sitemap')
