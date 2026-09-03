from pathlib import Path
from html import unescape
import json
import re

# Keep Black Book Article semantics protected inside the post-validate audit layer.
import phase77_article_audit

ROOT=Path('_site')

PATHS=[
'/private-chauffeur-ibiza/','/luxury-villas-ibiza/','/yacht-charter-ibiza/','/restaurants-nightlife-ibiza/','/private-aviation-ibiza/','/private-security-ibiza/','/private-chef-staffing-ibiza/','/luxury-car-rental-ibiza/','/wellness-ibiza/','/private-events-ibiza/','/bespoke-concierge-ibiza/',
'/es/chauffeur-privado-ibiza/','/es/villas-lujo-ibiza/','/es/yate-privado-ibiza/','/es/restaurantes-nightlife-ibiza/','/es/aviacion-privada-ibiza/','/es/seguridad-privada-ibiza/','/es/chef-privado-staffing-ibiza/','/es/alquiler-coches-lujo-ibiza/','/es/wellness-ibiza/','/es/eventos-privados-ibiza/','/es/concierge-a-medida-ibiza/',
'/fr/chauffeur-prive-ibiza/','/fr/villas-luxe-ibiza/','/fr/location-yacht-ibiza/','/fr/restaurants-nightlife-ibiza/','/fr/aviation-privee-ibiza/','/fr/securite-privee-ibiza/','/fr/chef-prive-personnel-villa-ibiza/','/fr/location-voiture-luxe-ibiza/','/fr/wellness-ibiza/','/fr/evenements-prives-ibiza/','/fr/conciergerie-sur-mesure-ibiza/',
'/de/privater-chauffeur-ibiza/','/de/luxusvillen-ibiza/','/de/yachtcharter-ibiza/','/de/restaurants-nightlife-ibiza/','/de/private-aviation-ibiza/','/de/private-sicherheit-ibiza/','/de/privatkoch-villa-staff-ibiza/','/de/luxusauto-mieten-ibiza/','/de/wellness-ibiza/','/de/private-events-ibiza/','/de/bespoke-concierge-ibiza/',
'/ar/private-chauffeur-ibiza/','/ar/luxury-villas-ibiza/','/ar/yacht-charter-ibiza/','/ar/restaurants-nightlife-ibiza/','/ar/private-aviation-ibiza/','/ar/private-security-ibiza/','/ar/private-chef-staffing-ibiza/','/ar/luxury-car-rental-ibiza/','/ar/wellness-ibiza/','/ar/private-events-ibiza/','/ar/bespoke-concierge-ibiza/'
]

if len(PATHS)!=55 or len(set(PATHS))!=55:
    raise SystemExit('Phase 75 path matrix must contain 55 unique service landings')

def clean(s):
    s=re.sub(r'<[^>]+>',' ',s)
    s=unescape(s)
    return re.sub(r'\s+',' ',s).strip()

for path in PATHS:
    p=ROOT/path.strip('/')/'index.html'
    if not p.exists(): raise SystemExit(f'Phase 75 missing service page: {path}')
    html=p.read_text(encoding='utf-8')
    sections=re.findall(r'<section\b[^>]*class="[^"]*ivm-service-faq[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
    if len(sections)!=1: raise SystemExit(f'Phase 75 expected one visible FAQ section: {path} ({len(sections)})')
    section=sections[0]
    details=re.findall(r'<details\b[^>]*>(.*?)</details>',section,re.I|re.S)
    if len(details)!=4: raise SystemExit(f'Phase 75 expected four FAQ details: {path} ({len(details)})')
    visible=[]
    for d in details:
        qm=re.search(r'<summary\b[^>]*>(.*?)</summary>',d,re.I|re.S)
        am=re.search(r'<p\b[^>]*>(.*?)</p>',d,re.I|re.S)
        if not qm or not am: raise SystemExit(f'Phase 75 malformed FAQ detail: {path}')
        q,a=clean(qm.group(1)),clean(am.group(1))
        if len(q)<8 or len(a)<15: raise SystemExit(f'Phase 75 thin visible FAQ content: {path}')
        visible.append((q,a))

    faq_schemas=[]
    for m in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>',html,re.I|re.S):
        try: obj=json.loads(m.group(1))
        except Exception: continue
        if isinstance(obj,dict) and obj.get('@type')=='FAQPage': faq_schemas.append(obj)
    if len(faq_schemas)!=1: raise SystemExit(f'Phase 75 expected one FAQPage schema: {path} ({len(faq_schemas)})')
    entities=faq_schemas[0].get('mainEntity') or []
    if len(entities)!=4: raise SystemExit(f'Phase 75 expected four FAQ schema entities: {path}')
    structured=[]
    for item in entities:
        if not isinstance(item,dict) or item.get('@type')!='Question': raise SystemExit(f'Phase 75 invalid Question schema: {path}')
        ans=item.get('acceptedAnswer') or {}
        q=clean(str(item.get('name',''))); a=clean(str(ans.get('text','')))
        if ans.get('@type')!='Answer' or len(q)<8 or len(a)<15: raise SystemExit(f'Phase 75 invalid Answer schema: {path}')
        structured.append((q,a))
    if visible != structured:
        raise SystemExit(f'Phase 75 visible FAQ/schema mismatch: {path}')

print('PASS: Phase 75 FAQ integrity audit — 55 service landings, 220 visible Q&As matched exactly to 55 four-item FAQPage schemas')
