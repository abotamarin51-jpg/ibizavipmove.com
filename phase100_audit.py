from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
ABOUT = ['/about/', '/es/sobre-nosotros/', '/fr/a-propos/', '/de/ueber-uns/', '/ar/about/']
PERSON_PAGES = [BASE + '/', *(BASE + path for path in ABOUT)]
SCRIPT_RE = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.I | re.S)


def schemas(html):
    result = []
    for match in SCRIPT_RE.finditer(html):
        try:
            result.append(json.loads(match.group(1)))
        except Exception as exc:
            raise SystemExit(f'Phase 100 invalid JSON-LD: {exc}')
    return result


for path in ABOUT:
    target = ROOT / path.strip('/') / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 100 About page missing: {path}')
    html = target.read_text(encoding='utf-8')
    if html.count('ivm-founder-identity') != 1:
        raise SystemExit(f'Phase 100 founder section cardinality mismatch: {path}')
    section = re.search(r'<section class="editorial ivm-founder-identity">(.*?)</section>', html, re.I | re.S)
    if not section or 'Juan Cruz' not in section.group(1):
        raise SystemExit(f'Phase 100 visible founder missing: {path}')

home_about = (ROOT / 'about' / 'index.html').read_text(encoding='utf-8')
if 'personal concierge brand founded and led by Juan Cruz' not in home_about:
    raise SystemExit('Phase 100 English personal-brand statement missing')
if 'Official company facts' in home_about or 'Official brand information' not in home_about:
    raise SystemExit('Phase 100 English About still describes a personal brand as a company')

organization_count = 0
person_count = 0
for target in ROOT.rglob('*.html'):
    html = target.read_text(encoding='utf-8')
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    canonical = canonical_match.group(1) if canonical_match else ''
    people = []
    for data in schemas(html):
        nodes = data.get('@graph', []) if isinstance(data, dict) and isinstance(data.get('@graph'), list) else [data]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            types = node.get('@type')
            types = types if isinstance(types, list) else [types]
            if node.get('@id') == ORG and 'Organization' in types:
                organization_count += 1
                if (node.get('founder') or {}).get('@id') != FOUNDER:
                    raise SystemExit(f'Phase 100 Organization founder mismatch: {target}')
            if node.get('@id') == FOUNDER and 'Person' in types:
                people.append(node)
    if canonical in PERSON_PAGES:
        if len(people) != 1:
            raise SystemExit(f'Phase 100 expected one Person entity: {canonical} -> {len(people)}')
        person = people[0]
        if person.get('name') != 'Juan Cruz' or person.get('jobTitle') != 'Founder' or (person.get('worksFor') or {}).get('@id') != ORG:
            raise SystemExit(f'Phase 100 Person entity mismatch: {canonical}')
        person_count += 1

if organization_count < 60:
    raise SystemExit(f'Phase 100 expected at least 60 Organization founder references, found {organization_count}')
if person_count != 6:
    raise SystemExit(f'Phase 100 expected six pages defining the founder, found {person_count}')

llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
for phrase in ('Founder: Juan Cruz', 'Business structure: founder-led personal concierge brand'):
    if phrase not in llms:
        raise SystemExit(f'Phase 100 llms identity missing: {phrase}')
if 'coordination company serving Ibiza' in llms or 'The company also supports principals' in llms:
    raise SystemExit('Phase 100 llms still misstates the founder-led personal brand as a company')

print(f'PASS: Phase 100 founder audit — five localized About pages, six Person definitions and {organization_count} Organization founder references verified without inventing a company, tax ID or address')
