from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ENTITY_ID = BASE + '/#organization'
LANGUAGES = ['English', 'Spanish', 'French', 'German', 'Arabic']
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)


def clean_org(data):
    if not isinstance(data, dict) or data.get('@id') != ENTITY_ID:
        return data
    if data.get('@type') not in ('ProfessionalService', 'Organization'):
        return data
    out = dict(data)
    out['@type'] = 'Organization'
    out['name'] = 'Ibiza VIP Move'
    out['url'] = BASE + '/'
    out['telephone'] = '+34 600 703 303'
    out['email'] = 'partnership@ibizavipmove.com'
    out['description'] = 'Private concierge, luxury transportation and lifestyle management in Ibiza for private clients, personal assistants, family offices and luxury travel partners.'
    out['slogan'] = 'Exceptional Ibiza, handled privately.'
    out['areaServed'] = {'@type': 'Place', 'name': 'Ibiza, Balearic Islands, Spain'}
    out['knowsLanguage'] = LANGUAGES
    out['contactPoint'] = [
        {
            '@type': 'ContactPoint',
            'contactType': 'customer service',
            'telephone': '+34 600 703 303',
            'url': BASE + '/contact/',
            'availableLanguage': LANGUAGES,
            'areaServed': 'ES'
        },
        {
            '@type': 'ContactPoint',
            'contactType': 'partnerships',
            'email': 'partnership@ibizavipmove.com',
            'url': BASE + '/partners/',
            'availableLanguage': LANGUAGES
        }
    ]
    # Keep the existing service catalog/logo if earlier phases already built them.
    return out


for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    matches = list(SCRIPT_RE.finditer(text))
    if not matches:
        continue
    changed = False
    out = []
    cursor = 0
    for m in matches:
        out.append(text[cursor:m.start()])
        try:
            data = json.loads(m.group(1))
        except Exception:
            data = None
        cleaned = clean_org(data)
        if cleaned is not data and cleaned != data:
            changed = True
        if isinstance(cleaned, dict):
            out.append('<script type="application/ld+json">' + json.dumps(cleaned, ensure_ascii=False) + '</script>')
        else:
            out.append(m.group(0))
        cursor = m.end()
    out.append(text[cursor:])
    if changed:
        path.write_text(''.join(out), encoding='utf-8')

# Add non-invasive application/entity metadata to every indexable page.
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if '<head' not in text.lower():
        continue
    additions = []
    if 'name="application-name"' not in text:
        additions.append('<meta name="application-name" content="Ibiza VIP Move">')
    if 'name="theme-color"' not in text:
        additions.append('<meta name="theme-color" content="#080807">')
    if additions:
        text = re.sub(r'</head>', ''.join(additions) + '</head>', text, count=1, flags=re.I)
        path.write_text(text, encoding='utf-8')

home = (ROOT / 'index.html').read_text(encoding='utf-8')
orgs = []
for m in SCRIPT_RE.finditer(home):
    try:
        data = json.loads(m.group(1))
    except Exception:
        continue
    if isinstance(data, dict) and data.get('@id') == ENTITY_ID:
        orgs.append(data)

assert len(orgs) == 1, f'Expected exactly one organization entity on home, found {len(orgs)}'
assert orgs[0].get('@type') == 'Organization', 'Organization entity must use Organization type'
assert orgs[0].get('hasOfferCatalog'), 'Service catalog missing from organization entity'
assert isinstance(orgs[0].get('contactPoint'), list) and len(orgs[0]['contactPoint']) == 2, 'Contact points not separated correctly'
assert 'address' not in orgs[0], 'Do not invent or publish an unverified physical address'
assert 'sameAs' not in orgs[0], 'Do not publish unverified sameAs profiles'
print('PASS: Phase 23 clean Organization entity + conversion metadata')
