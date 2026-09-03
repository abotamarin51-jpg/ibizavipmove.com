from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LLMS = ROOT / 'llms.txt'

EXPECTED_SERVICES = {
    '/private-chauffeur-ibiza/',
    '/luxury-villas-ibiza/',
    '/yacht-charter-ibiza/',
    '/private-aviation-ibiza/',
    '/restaurants-nightlife-ibiza/',
    '/private-security-ibiza/',
    '/private-chef-staffing-ibiza/',
    '/luxury-car-rental-ibiza/',
    '/wellness-ibiza/',
    '/private-events-ibiza/',
    '/bespoke-concierge-ibiza/',
}
EXPECTED_LANG_HUBS = {
    '/', '/services/', '/ibiza-intelligence/', '/contact/',
    '/es/', '/es/servicios/', '/es/ibiza-intelligence/', '/es/contacto/',
    '/fr/', '/fr/services/', '/fr/ibiza-intelligence/', '/fr/contact/',
    '/de/', '/de/services/', '/de/ibiza-intelligence/', '/de/kontakt/',
    '/ar/', '/ar/services/', '/ar/ibiza-intelligence/', '/ar/contact/',
}
EXPECTED_BLACK_BOOK = {
    '/ibiza-intelligence/',
    '/ibiza-intelligence/private-arrival/',
    '/ibiza-intelligence/ibiza-formentera-yacht-day/',
    '/ibiza-intelligence/ibiza-august-planning/',
    '/ibiza-intelligence/villa-arrival-planning/',
    '/ibiza-intelligence/nightlife-transport-planning/',
    '/ibiza-intelligence/private-aviation-ground-coordination/',
}

if not LLMS.exists():
    raise SystemExit('Phase 76 llms.txt missing')
text = LLMS.read_text(encoding='utf-8')

required_phrases = [
    '# Ibiza VIP Move',
    'Canonical organization entity: https://ibizavipmove.com/#organization',
    'Primary service area: Ibiza, Balearic Islands, Spain',
    'Languages published: English, Spanish, French, German and Arabic',
    '## Canonical service catalog — 11 services',
    '## International discovery',
    '## The Ibiza Black Book',
    '## B2B and professional coordination',
    '## Source-of-truth and accuracy notes',
    'not guaranteed until specifically confirmed',
    'Wellness coordination does not replace medical advice',
    'Bespoke requests must be legal, safe and viable',
]
for phrase in required_phrases:
    if phrase not in text:
        raise SystemExit(f'Phase 76 missing required phrase: {phrase}')

urls = re.findall(r'\(https://ibizavipmove\.com([^)]*)\)', text)
paths = {path or '/' for path in urls}

missing_services = EXPECTED_SERVICES - paths
if missing_services:
    raise SystemExit(f'Phase 76 missing canonical services: {sorted(missing_services)}')
missing_lang = EXPECTED_LANG_HUBS - paths
if missing_lang:
    raise SystemExit(f'Phase 76 missing language hubs: {sorted(missing_lang)}')
missing_black = EXPECTED_BLACK_BOOK - paths
if missing_black:
    raise SystemExit(f'Phase 76 missing Black Book pages: {sorted(missing_black)}')

# Every HTML URL referenced in llms.txt must exist in the built site.
for path in sorted(paths):
    if path in ('/sitemap.xml', '/image-sitemap.xml', '/robots.txt'):
        target = ROOT / path.lstrip('/')
    elif path == '/':
        target = ROOT / 'index.html'
    else:
        target = ROOT / path.strip('/') / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 76 llms URL does not exist: {path}')

# The 11 canonical services must also be present in sitemap.xml.
ns = {'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
root = ET.parse(ROOT/'sitemap.xml').getroot()
sitemap_urls = {u.find('sm:loc', ns).text for u in root.findall('sm:url', ns) if u.find('sm:loc', ns) is not None}
for path in EXPECTED_SERVICES:
    if BASE + path not in sitemap_urls:
        raise SystemExit(f'Phase 76 service missing from sitemap: {path}')

# Protect the file from drifting back to an obsolete small summary.
if len(text.splitlines()) < 70:
    raise SystemExit('Phase 76 llms.txt unexpectedly short')
if text.count('## ') < 7:
    raise SystemExit('Phase 76 llms.txt missing section structure')

print(f'PASS: Phase 76 AI/GEO audit — {len(paths)} official discovery URLs verified; 11 services, 5 language hubs and 7 Black Book entries aligned')
