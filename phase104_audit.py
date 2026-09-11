from pathlib import Path
from html import unescape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
NEW_PATHS = [
    '/founder/',
    '/case-studies/',
    '/case-studies/private-aviation-arrival-seven-guests/',
    '/case-studies/principal-chauffeur-security-three-days/',
    '/case-studies/weekend-concierge-two-guests/',
    '/case-studies/multi-day-executive-chauffeur-program/',
    '/case-studies/late-night-dual-vehicle-arrival/',
    '/ibiza-luxury-operations-report-2026/',
]
CASE_PATHS = [x for x in NEW_PATHS if x.startswith('/case-studies/') and x != '/case-studies/']
HUBS = ['/about/','/private-concierge-ibiza/','/partners/','/ibiza-intelligence/']
FORBIDDEN_PRIVATE_TERMS = [
    'Ryan Hurt','Ryan Huber','Lucinda Edwards','Princess Noura','Princesa Noura',
    'AEROAFFAIRES','Sahab Travel','Optimum Chauffeurs','Corporate Paris',
]
SCRIPT_RE = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.I | re.S)


def page(path):
    return ROOT / path.strip('/') / 'index.html'


def schemas(html):
    out = []
    for m in SCRIPT_RE.finditer(html):
        try:
            data = json.loads(m.group(1))
        except Exception as exc:
            raise SystemExit(f'Phase 104 invalid JSON-LD: {exc}')
        if isinstance(data, dict) and isinstance(data.get('@graph'), list):
            out.extend(data['@graph'])
        elif isinstance(data, dict):
            out.append(data)
    return out


def visible_words(html):
    text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.I | re.S)
    text = unescape(re.sub(r'<[^>]+>', ' ', text))
    return re.findall(r"\b[\w'-]+\b", text)


titles = set()
for path in NEW_PATHS:
    target = page(path)
    if not target.exists():
        raise SystemExit(f'Phase 104 missing page: {path}')
    html = target.read_text(encoding='utf-8')
    url = BASE + path

    canonical = re.findall(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', html, re.I)
    if canonical != [url]:
        raise SystemExit(f'Phase 104 canonical mismatch: {path} -> {canonical}')
    title_m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    if not title_m:
        raise SystemExit(f'Phase 104 title missing: {path}')
    title = unescape(re.sub(r'\s+',' ',title_m.group(1))).strip()
    if title in titles:
        raise SystemExit(f'Phase 104 duplicate title: {title}')
    titles.add(title)
    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit(f'Phase 104 expected one H1: {path}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 104 accessibility landmark missing: {path}')
    if '+34 600 703 303' not in html or '34600703303' not in html:
        raise SystemExit(f'Phase 104 current contact missing: {path}')
    if '+34 613 75 62 11' in html or '34613756211' in html:
        raise SystemExit(f'Phase 104 old contact leaked: {path}')
    if 'AggregateRating' in html or 'PostalAddress' in html:
        raise SystemExit(f'Phase 104 invented rating/address forbidden: {path}')
    for term in FORBIDDEN_PRIVATE_TERMS:
        if term.lower() in html.lower():
            raise SystemExit(f'Phase 104 privacy leak on {path}: {term}')
    for required in ('og:title','og:description','og:url','og:image','twitter:card','twitter:title','twitter:description','twitter:image'):
        if required not in html:
            raise SystemExit(f'Phase 104 social metadata missing {required}: {path}')

    alt_links = re.findall(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\']([^"\']+)["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', html, re.I)
    if {lang.lower(): href for lang,href in alt_links} != {'en':url,'x-default':url} or len(alt_links) != 2:
        raise SystemExit(f'Phase 104 standalone English hreflang mismatch: {path} -> {alt_links}')

    words = visible_words(html)
    floor = 300 if path in ('/founder/','/case-studies/') else 430
    if len(words) < floor:
        raise SystemExit(f'Phase 104 content too thin: {path} -> {len(words)} words')

# Founder page: Google-style ProfilePage with one canonical Person.
founder_html = page('/founder/').read_text(encoding='utf-8')
founder_nodes = schemas(founder_html)
profiles = [n for n in founder_nodes if n.get('@type') == 'ProfilePage']
people = [n for n in founder_nodes if n.get('@id') == FOUNDER and n.get('@type') == 'Person']
if len(profiles) != 1 or len(people) != 1:
    raise SystemExit(f'Phase 104 founder schema mismatch: ProfilePage={len(profiles)} Person={len(people)}')
if (profiles[0].get('mainEntity') or {}).get('@id') != FOUNDER:
    raise SystemExit('Phase 104 ProfilePage mainEntity mismatch')
if people[0].get('name') != 'Juan Cruz' or people[0].get('jobTitle') != 'Founder' or people[0].get('url') != BASE + '/founder/':
    raise SystemExit('Phase 104 founder Person identity mismatch')
if (people[0].get('worksFor') or {}).get('@id') != ORG:
    raise SystemExit('Phase 104 founder worksFor mismatch')

# Case-study hub: one collection with five unique real-brief articles.
hub_nodes = schemas(page('/case-studies/').read_text(encoding='utf-8'))
collections = [n for n in hub_nodes if n.get('@type') == 'CollectionPage']
if len(collections) != 1:
    raise SystemExit('Phase 104 case-study CollectionPage missing')
items = (collections[0].get('mainEntity') or {}).get('itemListElement') or []
if len(items) != 5 or len({x.get('url') for x in items}) != 5:
    raise SystemExit('Phase 104 case-study ItemList must contain five unique studies')

# Each case is authored by the founder and explicitly protects client identity.
for path in CASE_PATHS:
    html = page(path).read_text(encoding='utf-8')
    if 'based on a real Ibiza VIP Move operating brief' not in html:
        raise SystemExit(f'Phase 104 real-brief disclosure missing: {path}')
    if 'Client names, exact dates, properties' not in html:
        raise SystemExit(f'Phase 104 privacy disclosure missing: {path}')
    nodes = schemas(html)
    articles = [n for n in nodes if n.get('@type') == 'Article']
    if len(articles) != 1:
        raise SystemExit(f'Phase 104 expected one Article: {path}')
    article = articles[0]
    if (article.get('author') or {}).get('@id') != FOUNDER or (article.get('publisher') or {}).get('@id') != ORG:
        raise SystemExit(f'Phase 104 Article author/publisher mismatch: {path}')
    if article.get('datePublished') != '2026-09-11T07:30:00+02:00':
        raise SystemExit(f'Phase 104 Article publication date mismatch: {path}')

# Report must be explicit about methodology and avoid pretending to be market-wide research.
report_html = page('/ibiza-luxury-operations-report-2026/').read_text(encoding='utf-8')
for phrase in (
    'Operational observations, not market statistics.',
    'not presented as a statistically representative survey of the Ibiza luxury market',
    'No market-share, island-wide demand or competitor-performance claims are made',
    'Eight field observations',
):
    if phrase not in report_html:
        raise SystemExit(f'Phase 104 report methodology phrase missing: {phrase}')
report_articles = [n for n in schemas(report_html) if n.get('@type') == 'Article']
if len(report_articles) != 1 or (report_articles[0].get('author') or {}).get('@id') != FOUNDER:
    raise SystemExit('Phase 104 report Article author mismatch')

# Existing canonical Person entities must resolve to the dedicated founder profile.
person_refs = 0
for target in ROOT.rglob('*.html'):
    html = target.read_text(encoding='utf-8')
    for node in schemas(html):
        if node.get('@id') == FOUNDER and node.get('@type') == 'Person':
            person_refs += 1
            if node.get('url') != BASE + '/founder/':
                raise SystemExit(f'Phase 104 Person URL drift: {target}')
if person_refs < 10:
    raise SystemExit(f'Phase 104 expected founder Person references across authority pages, found {person_refs}')

# Authority hubs link visibly to the new evidence cluster.
for path in HUBS:
    html = page(path).read_text(encoding='utf-8')
    if html.count('ivm-phase104-authority') != 1:
        raise SystemExit(f'Phase 104 authority section mismatch: {path}')
    if '/case-studies/' not in html:
        raise SystemExit(f'Phase 104 case-study link missing from hub: {path}')

sitemap = (ROOT/'sitemap.xml').read_text(encoding='utf-8')
llms = (ROOT/'llms.txt').read_text(encoding='utf-8')
for path in NEW_PATHS:
    url = BASE + path
    if sitemap.count(url) != 1:
        raise SystemExit(f'Phase 104 sitemap count mismatch: {path} -> {sitemap.count(url)}')
    if url not in llms:
        raise SystemExit(f'Phase 104 llms discovery missing: {path}')
if llms.count('## Founder and operational evidence') != 1:
    raise SystemExit('Phase 104 llms authority section mismatch')

print(f'PASS: Phase 104 audit — founder ProfilePage, 5 privacy-safe real case studies, field report, {person_refs} founder entity references, authority links, sitemap and AI discovery verified')
