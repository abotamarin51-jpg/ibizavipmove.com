from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ENTITY_ID = BASE + '/#organization'
LANGUAGES = ['English', 'Spanish', 'French', 'German', 'Arabic']
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)


def enhance_entity(data):
    if not isinstance(data, dict):
        return data
    if data.get('@type') != 'ProfessionalService' or data.get('@id') != ENTITY_ID:
        return data
    data = dict(data)
    cp = dict(data.get('contactPoint') or {})
    cp['@type'] = 'ContactPoint'
    cp['telephone'] = '+34 600 703 303'
    cp['contactType'] = 'customer service'
    cp['url'] = BASE + '/contact/'
    cp['availableLanguage'] = LANGUAGES
    data['contactPoint'] = cp
    data['telephone'] = '+34 600 703 303'
    data['email'] = 'partnership@ibizavipmove.com'
    data['areaServed'] = {'@type': 'Place', 'name': 'Ibiza, Spain'}
    data['logo'] = {'@type': 'ImageObject', 'url': BASE + '/assets/brand-logo.svg'}
    return data


for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    matches = list(SCRIPT_RE.finditer(text))
    parsed = []
    for m in matches:
        try:
            data = json.loads(m.group(1))
        except Exception:
            data = None
        parsed.append((m, data))

    entities = [d for _, d in parsed if isinstance(d, dict) and d.get('@type') == 'ProfessionalService' and d.get('@id') == ENTITY_ID]
    if not entities:
        continue

    merged = {}
    for d in entities:
        merged.update(d)
    merged = enhance_entity(merged)

    first_written = False
    out = []
    cursor = 0
    for m, data in parsed:
        out.append(text[cursor:m.start()])
        if isinstance(data, dict) and data.get('@type') == 'ProfessionalService' and data.get('@id') == ENTITY_ID:
            if not first_written:
                out.append('<script type="application/ld+json">' + json.dumps(merged, ensure_ascii=False) + '</script>')
                first_written = True
            # Duplicate organization scripts are intentionally omitted.
        else:
            if isinstance(data, dict):
                out.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>')
            else:
                out.append(m.group(0))
        cursor = m.end()
    out.append(text[cursor:])
    path.write_text(''.join(out), encoding='utf-8')

home = (ROOT / 'index.html').read_text(encoding='utf-8')
entity_count = 0
home_entity = None
for m in SCRIPT_RE.finditer(home):
    try:
        data = json.loads(m.group(1))
    except Exception:
        continue
    if isinstance(data, dict) and data.get('@type') == 'ProfessionalService' and data.get('@id') == ENTITY_ID:
        entity_count += 1
        home_entity = data

assert entity_count == 1, f'Expected one organization entity on home, found {entity_count}'
assert 'Spanish' in home_entity.get('contactPoint', {}).get('availableLanguage', []), 'Spanish missing from availableLanguage'
assert 'hasOfferCatalog' in home_entity, 'Home organization lost service catalog during deduplication'

premium_js = ROOT / 'assets' / 'premium.js'
assert premium_js.is_file() and 'ivm_conversion' in premium_js.read_text(encoding='utf-8'), 'Conversion event readiness missing from premium.js'
print('PASS: Phase 17 entity schema consolidated + five languages + conversion events ready')
