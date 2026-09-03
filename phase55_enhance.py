from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
EMAIL = 'partnership@ibizavipmove.com'
PHONE = '+34 600 703 303'
LANGUAGES = ['English','Spanish','French','German','Arabic']
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)

CLIENT_CONTACT = {
    '@type':'ContactPoint',
    'telephone':PHONE,
    'contactType':'private concierge',
    'url':BASE + '/contact/',
    'availableLanguage':LANGUAGES,
}
PARTNER_CONTACT = {
    '@type':'ContactPoint',
    'telephone':PHONE,
    'email':EMAIL,
    'contactType':'partnerships',
    'url':BASE + '/partners/',
    'availableLanguage':LANGUAGES,
}

updated = 0
entity_scripts = 0
for file in ROOT.rglob('*.html'):
    html = file.read_text(encoding='utf-8')
    changed = False

    def repl(match):
        nonlocal changed, entity_scripts
        try:
            obj = json.loads(match.group(1))
        except Exception:
            return match.group(0)
        if not isinstance(obj, dict):
            return match.group(0)
        typ = obj.get('@type')
        types = typ if isinstance(typ, list) else [typ]
        is_entity = obj.get('@id') == ORG or (
            obj.get('name') == 'Ibiza VIP Move' and any(t in ('Organization','ProfessionalService','LocalBusiness') for t in types)
        )
        if not is_entity:
            return match.group(0)
        entity_scripts += 1
        obj['@id'] = ORG
        obj['contactPoint'] = [CLIENT_CONTACT, PARTNER_CONTACT]
        changed = True
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

    html = SCRIPT_RE.sub(repl, html)
    if changed:
        file.write_text(html, encoding='utf-8')
        updated += 1

if entity_scripts == 0:
    raise SystemExit('Phase 55 organization entity not found')

verified = 0
for file in ROOT.rglob('*.html'):
    html = file.read_text(encoding='utf-8')
    for match in SCRIPT_RE.finditer(html):
        try: obj = json.loads(match.group(1))
        except Exception: continue
        if not isinstance(obj, dict) or obj.get('@id') != ORG:
            continue
        cps = obj.get('contactPoint')
        assert isinstance(cps, list) and len(cps) == 2, file
        types = {cp.get('contactType') for cp in cps if isinstance(cp, dict)}
        assert types == {'private concierge','partnerships'}, (file, types)
        partner = next(cp for cp in cps if cp.get('contactType') == 'partnerships')
        client = next(cp for cp in cps if cp.get('contactType') == 'private concierge')
        assert partner.get('email') == EMAIL and partner.get('url') == BASE + '/partners/', file
        assert client.get('url') == BASE + '/contact/' and 'email' not in client, file
        assert partner.get('availableLanguage') == LANGUAGES, file
        verified += 1

assert verified == entity_scripts, (verified, entity_scripts)
print(f'PASS: Phase 55 organization authority split into private concierge + partnerships contact points across {updated} pages')
