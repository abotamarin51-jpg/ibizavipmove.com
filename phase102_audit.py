from pathlib import Path
from html import unescape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
SLUGS = [
    'luxury-lifestyle-management-ibiza',
    'personal-concierge-ibiza',
    'luxury-travel-concierge-ibiza',
    'vip-services-ibiza',
    'private-client-services-ibiza',
    'destination-management-ibiza',
]
HUBS = [
    'private-concierge-ibiza',
    'services',
    'international-clients',
    'partners',
]
SCRIPT_RE = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.I | re.S)

titles = set()
descriptions = set()

for slug in SLUGS:
    target = ROOT / slug / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 102 audit missing page: /{slug}/')
    html = target.read_text(encoding='utf-8')
    url = f'{BASE}/{slug}/'

    canonical = re.findall(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', html, re.I)
    if canonical != [url]:
        raise SystemExit(f'Phase 102 audit canonical mismatch: {slug} -> {canonical}')

    title_match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    if not title_match:
        raise SystemExit(f'Phase 102 audit title missing: {slug}')
    title = unescape(re.sub(r'\s+', ' ', title_match.group(1)).strip())
    if title in titles:
        raise SystemExit(f'Phase 102 audit duplicate title: {title}')
    titles.add(title)

    desc_match = re.search(r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*\bcontent=["\']([^"\']+)["\'][^>]*>', html, re.I)
    if not desc_match:
        raise SystemExit(f'Phase 102 audit description missing: {slug}')
    desc = unescape(desc_match.group(1)).strip()
    if not 110 <= len(desc) <= 190:
        raise SystemExit(f'Phase 102 audit description length outside target: {slug} -> {len(desc)}')
    if desc in descriptions:
        raise SystemExit(f'Phase 102 audit duplicate description: {slug}')
    descriptions.add(desc)

    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit(f'Phase 102 audit expected one H1: {slug}')
    if 'Ibiza · Balearic Islands · Spain' not in html:
        raise SystemExit(f'Phase 102 audit local Ibiza signal missing: {slug}')
    if '34600703303' not in html or '+34 600 703 303' not in html:
        raise SystemExit(f'Phase 102 audit current contact missing: {slug}')
    if '34613756211' in html or '+34 613 75 62 11' in html:
        raise SystemExit(f'Phase 102 audit old contact leaked into page: {slug}')
    if 'AggregateRating' in html or 'LocalBusiness' in html or 'PostalAddress' in html:
        raise SystemExit(f'Phase 102 audit must not invent ratings, storefront or address: {slug}')
    if html.count('hreflang="en"') != 1 or html.count('hreflang="x-default"') != 1:
        raise SystemExit(f'Phase 102 audit English hreflang mismatch: {slug}')

    # Guard against thin doorway-style pages: require a substantial visible body
    # and four distinct visible FAQ questions.
    visible = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.I | re.S)
    visible = unescape(re.sub(r'<[^>]+>', ' ', visible))
    words = re.findall(r"\b[\w'-]+\b", visible)
    if len(words) < 430:
        raise SystemExit(f'Phase 102 audit page too thin: {slug} -> {len(words)} words')
    if len(re.findall(r'<details>', html, re.I)) < 4:
        raise SystemExit(f'Phase 102 audit visible FAQ too small: {slug}')

    schemas = []
    for match in SCRIPT_RE.finditer(html):
        try:
            schemas.append(json.loads(match.group(1)))
        except Exception as exc:
            raise SystemExit(f'Phase 102 audit invalid JSON-LD on {slug}: {exc}')
    nodes = []
    for data in schemas:
        if isinstance(data, dict) and isinstance(data.get('@graph'), list):
            nodes.extend(data['@graph'])
        elif isinstance(data, dict):
            nodes.append(data)

    organizations = [n for n in nodes if isinstance(n, dict) and n.get('@id') == ORG]
    services = [n for n in nodes if isinstance(n, dict) and n.get('@type') == 'Service']
    faqs = [n for n in nodes if isinstance(n, dict) and n.get('@type') == 'FAQPage']
    breadcrumbs = [n for n in nodes if isinstance(n, dict) and n.get('@type') == 'BreadcrumbList']
    if len(organizations) != 1 or len(services) != 1 or len(faqs) != 1 or len(breadcrumbs) != 1:
        raise SystemExit(
            f'Phase 102 audit schema cardinality mismatch: {slug} '
            f'org={len(organizations)} service={len(services)} faq={len(faqs)} breadcrumb={len(breadcrumbs)}'
        )
    org = organizations[0]
    if (org.get('founder') or {}).get('@id') != FOUNDER:
        raise SystemExit(f'Phase 102 audit founder relation missing: {slug}')
    service = services[0]
    if (service.get('provider') or {}).get('@id') != ORG:
        raise SystemExit(f'Phase 102 audit provider relation missing: {slug}')
    area = service.get('areaServed') or {}
    if 'Ibiza' not in area.get('name', '') or 'Balearic Islands' not in json.dumps(area, ensure_ascii=False):
        raise SystemExit(f'Phase 102 audit service area missing Ibiza/Balearic Islands: {slug}')
    if service.get('url') != url:
        raise SystemExit(f'Phase 102 audit service URL mismatch: {slug}')
    if len(faqs[0].get('mainEntity', [])) != 4:
        raise SystemExit(f'Phase 102 audit FAQ schema mismatch: {slug}')

sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
for slug in SLUGS:
    url = f'{BASE}/{slug}/'
    if sitemap.count(url) != 1:
        raise SystemExit(f'Phase 102 audit sitemap URL count mismatch: {slug} -> {sitemap.count(url)}')
    if url not in llms:
        raise SystemExit(f'Phase 102 audit llms discovery missing: {slug}')

if llms.count('## High-intent concierge pathways') != 1:
    raise SystemExit('Phase 102 audit llms intent section cardinality mismatch')

for hub in HUBS:
    target = ROOT / hub / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 102 audit hub missing: /{hub}/')
    html = target.read_text(encoding='utf-8')
    if html.count('ivm-intent-cluster') != 1:
        raise SystemExit(f'Phase 102 audit internal-link cluster mismatch: /{hub}/')
    if not any(f'/{slug}/' in html for slug in SLUGS):
        raise SystemExit(f'Phase 102 audit hub has no new intent links: /{hub}/')

print('PASS: Phase 102 audit — six substantial intent pages are canonical, locally grounded to Ibiza, schema-linked, internally discoverable and protected from invented Maps/review data')
