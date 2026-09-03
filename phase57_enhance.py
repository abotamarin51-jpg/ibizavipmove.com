from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)

SERVICES = [
 ('Private Chauffeur Ibiza','/private-chauffeur-ibiza/'),
 ('Luxury Villas Ibiza','/luxury-villas-ibiza/'),
 ('Yacht Charter Ibiza','/yacht-charter-ibiza/'),
 ('Private Aviation Ibiza','/private-aviation-ibiza/'),
 ('Restaurants & Nightlife Ibiza','/restaurants-nightlife-ibiza/'),
 ('Private Security Ibiza','/private-security-ibiza/'),
 ('Private Chef & Staffing Ibiza','/private-chef-staffing-ibiza/'),
 ('Luxury Car Rental Ibiza','/luxury-car-rental-ibiza/'),
 ('Wellness Ibiza','/wellness-ibiza/'),
 ('Private Events Ibiza','/private-events-ibiza/'),
 ('Bespoke Concierge Ibiza','/bespoke-concierge-ibiza/'),
]

catalog = {
 '@type':'OfferCatalog',
 'name':'Ibiza VIP Move Private Services',
 'itemListElement':[
  {
   '@type':'Offer',
   'itemOffered':{
    '@type':'Service',
    'name':name,
    'url':BASE+path,
    'provider':{'@id':ORG},
    'areaServed':{'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},
   }
  } for name,path in SERVICES
 ]
}

updated = 0
entity_count = 0
for file in ROOT.rglob('*.html'):
    html = file.read_text(encoding='utf-8')
    state = {'changed':False}

    def repl(match):
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
        nonlocal_state = state
        obj['@id'] = ORG
        obj['hasOfferCatalog'] = catalog
        nonlocal_state['changed'] = True
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

    before = html
    html = SCRIPT_RE.sub(repl, html)
    if state['changed']:
        entity_count += 1
        file.write_text(html, encoding='utf-8')
        updated += 1

if entity_count == 0:
    raise SystemExit('Phase 57 organization entity not found')

verified = 0
for file in ROOT.rglob('*.html'):
    html = file.read_text(encoding='utf-8')
    for m in SCRIPT_RE.finditer(html):
        try: obj = json.loads(m.group(1))
        except Exception: continue
        if not isinstance(obj, dict) or obj.get('@id') != ORG:
            continue
        c = obj.get('hasOfferCatalog')
        assert isinstance(c, dict) and c.get('@type') == 'OfferCatalog', file
        items = c.get('itemListElement')
        assert isinstance(items, list) and len(items) == len(SERVICES), file
        urls = {x.get('itemOffered',{}).get('url') for x in items if isinstance(x,dict)}
        assert urls == {BASE+p for _,p in SERVICES}, file
        assert all('price' not in x for x in items if isinstance(x,dict)), file
        verified += 1

assert verified == entity_count, (verified, entity_count)
print(f'PASS: Phase 57 organization OfferCatalog links {len(SERVICES)} canonical private services across {updated} entity pages')
