from pathlib import Path
from html import unescape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
SLUGS = [
    'private-concierge-marina-botafoch-ibiza',
    'private-concierge-cala-jondal-es-cubells-ibiza',
    'private-concierge-santa-eulalia-roca-llisa-ibiza',
    'private-concierge-santa-gertrudis-ibiza',
]
EXPECTED_AREAS = {
    'private-concierge-marina-botafoch-ibiza': {'Marina Botafoch, Ibiza','Ibiza Town, Ibiza','Talamanca, Ibiza','Cap Martinet, Ibiza'},
    'private-concierge-cala-jondal-es-cubells-ibiza': {'Cala Jondal, Ibiza','Es Cubells, Ibiza','Porroig, Ibiza','Sant Josep de sa Talaia, Ibiza'},
    'private-concierge-santa-eulalia-roca-llisa-ibiza': {'Santa Eulària des Riu, Ibiza','Roca Llisa, Ibiza','Cala Llonga, Ibiza','Siesta, Ibiza'},
    'private-concierge-santa-gertrudis-ibiza': {'Santa Gertrudis de Fruitera, Ibiza','Central Ibiza, Ibiza','Sant Llorenç de Balàfia, Ibiza','San Rafael, Ibiza'},
}
HUBS = ['private-concierge-ibiza','luxury-lifestyle-management-ibiza','private-client-services-ibiza','luxury-villas-ibiza']
SCRIPT_RE = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.I | re.S)

titles=set(); descriptions=set()
for slug in SLUGS:
    target=ROOT/slug/'index.html'
    if not target.exists(): raise SystemExit(f'Phase 103 missing page: {slug}')
    html=target.read_text(encoding='utf-8')
    url=f'{BASE}/{slug}/'

    canon=re.findall(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>',html,re.I)
    if canon != [url]: raise SystemExit(f'Phase 103 canonical mismatch: {slug} -> {canon}')
    tm=re.search(r'<title>(.*?)</title>',html,re.I|re.S)
    if not tm: raise SystemExit(f'Phase 103 title missing: {slug}')
    title=unescape(re.sub(r'\s+',' ',tm.group(1)).strip())
    if title in titles: raise SystemExit(f'Phase 103 duplicate title: {title}')
    titles.add(title)
    dm=re.search(r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*\bcontent=["\']([^"\']+)["\'][^>]*>',html,re.I)
    if not dm: raise SystemExit(f'Phase 103 description missing: {slug}')
    desc=unescape(dm.group(1)).strip()
    if not 110 <= len(desc) <= 200: raise SystemExit(f'Phase 103 description length: {slug} -> {len(desc)}')
    if desc in descriptions: raise SystemExit(f'Phase 103 duplicate description: {slug}')
    descriptions.add(desc)

    if html.count('<h1') != 1: raise SystemExit(f'Phase 103 expected one H1: {slug}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 103 accessibility landmark missing: {slug}')
    if '+34 600 703 303' not in html or '34600703303' not in html:
        raise SystemExit(f'Phase 103 current contact missing: {slug}')
    if '34613756211' in html or '+34 613 75 62 11' in html:
        raise SystemExit(f'Phase 103 old contact leaked: {slug}')
    if 'AggregateRating' in html or 'LocalBusiness' in html or 'PostalAddress' in html or 'GeoCoordinates' in html:
        raise SystemExit(f'Phase 103 invented Maps/review/address/coordinates risk: {slug}')

    visible=unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>',' ',html,flags=re.I|re.S)))
    words=re.findall(r"\b[\w'-]+\b",visible)
    if len(words) < 430: raise SystemExit(f'Phase 103 page too thin: {slug} -> {len(words)} words')
    if len(re.findall(r'<details>',html,re.I)) < 4: raise SystemExit(f'Phase 103 FAQ too small: {slug}')

    alternates=re.findall(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\']([^"\']+)["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>',html,re.I)
    if {k.lower():v for k,v in alternates} != {'en':url,'x-default':url} or len(alternates)!=2:
        raise SystemExit(f'Phase 103 hreflang mismatch: {slug} -> {alternates}')

    schemas=[]
    for m in SCRIPT_RE.finditer(html):
        try: schemas.append(json.loads(m.group(1)))
        except Exception as exc: raise SystemExit(f'Phase 103 invalid JSON-LD {slug}: {exc}')
    nodes=[]
    for data in schemas:
        if isinstance(data,dict) and isinstance(data.get('@graph'),list): nodes.extend(data['@graph'])
        elif isinstance(data,dict): nodes.append(data)
    orgs=[n for n in nodes if isinstance(n,dict) and n.get('@id')==ORG]
    services=[n for n in nodes if isinstance(n,dict) and n.get('@type')=='Service']
    faqs=[n for n in nodes if isinstance(n,dict) and n.get('@type')=='FAQPage']
    bread=[n for n in nodes if isinstance(n,dict) and n.get('@type')=='BreadcrumbList']
    if len(orgs)!=1 or len(services)!=1 or len(faqs)!=1 or len(bread)!=1:
        raise SystemExit(f'Phase 103 schema count mismatch: {slug}')
    if (orgs[0].get('founder') or {}).get('@id') != FOUNDER: raise SystemExit(f'Phase 103 founder relation missing: {slug}')
    svc=services[0]
    if (svc.get('provider') or {}).get('@id') != ORG or svc.get('url') != url:
        raise SystemExit(f'Phase 103 Service relation mismatch: {slug}')
    area=svc.get('areaServed') or []
    names={x.get('name') for x in area if isinstance(x,dict)}
    if names != EXPECTED_AREAS[slug]: raise SystemExit(f'Phase 103 areaServed mismatch: {slug} -> {names}')
    spatial=svc.get('spatialCoverage') or []
    snames={x.get('name') for x in spatial if isinstance(x,dict)}
    if snames != EXPECTED_AREAS[slug]: raise SystemExit(f'Phase 103 spatialCoverage mismatch: {slug}')
    if len(faqs[0].get('mainEntity',[])) != 4: raise SystemExit(f'Phase 103 FAQ schema mismatch: {slug}')

sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
llms=(ROOT/'llms.txt').read_text(encoding='utf-8')
for slug in SLUGS:
    url=f'{BASE}/{slug}/'
    if sitemap.count(url)!=1: raise SystemExit(f'Phase 103 sitemap count mismatch: {slug}')
    if url not in llms: raise SystemExit(f'Phase 103 llms discovery missing: {slug}')
if llms.count('## Local private concierge areas') != 1:
    raise SystemExit('Phase 103 llms local-area section mismatch')

for hub in HUBS:
    target=ROOT/hub/'index.html'
    if not target.exists(): raise SystemExit(f'Phase 103 hub missing: {hub}')
    html=target.read_text(encoding='utf-8')
    if html.count('ivm-local-luxury-areas') != 1: raise SystemExit(f'Phase 103 local cluster mismatch: {hub}')
    for slug in SLUGS:
        if f'/{slug}/' not in html: raise SystemExit(f'Phase 103 hub missing area link: {hub} -> {slug}')

print('PASS: Phase 103 audit — four substantial local concierge pages use real Ibiza Place names, unique intent, clean canonicals, schema GEO coverage, internal links and no invented Maps data')

# Phase 104 runs only after Phase 103 has passed, preserving the same protected
# post-validation chain before the global final audit.
import phase104_enhance
import phase104_audit
