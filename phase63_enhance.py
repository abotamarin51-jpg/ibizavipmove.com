from pathlib import Path
from html import escape
import re

ROOT=Path('_site')
SCRIPT='/assets/phase63.js?v=63'
source=Path('phase63.js')
dest=ROOT/'assets'/'phase63.js'
dest.write_text(source.read_text(encoding='utf-8'),encoding='utf-8')

SERVICE_PAGES=[
'/private-chauffeur-ibiza/','/es/chauffeur-privado-ibiza/','/fr/chauffeur-prive-ibiza/','/de/privater-chauffeur-ibiza/','/ar/private-chauffeur-ibiza/',
'/luxury-villas-ibiza/','/es/villas-lujo-ibiza/','/fr/villas-luxe-ibiza/','/de/luxusvillen-ibiza/','/ar/luxury-villas-ibiza/',
'/yacht-charter-ibiza/','/es/yate-privado-ibiza/','/fr/location-yacht-ibiza/','/de/yachtcharter-ibiza/','/ar/yacht-charter-ibiza/',
'/private-aviation-ibiza/','/es/aviacion-privada-ibiza/','/fr/aviation-privee-ibiza/','/de/private-aviation-ibiza/','/ar/private-aviation-ibiza/',
'/restaurants-nightlife-ibiza/','/es/restaurantes-nightlife-ibiza/','/fr/restaurants-nightlife-ibiza/','/de/restaurants-nightlife-ibiza/','/ar/restaurants-nightlife-ibiza/',
'/private-security-ibiza/','/es/seguridad-privada-ibiza/','/fr/securite-privee-ibiza/','/de/private-sicherheit-ibiza/','/ar/private-security-ibiza/',
'/private-chef-staffing-ibiza/','/es/chef-privado-staffing-ibiza/','/fr/chef-prive-personnel-villa-ibiza/','/de/privatkoch-villa-staff-ibiza/','/ar/private-chef-staffing-ibiza/',
'/luxury-car-rental-ibiza/','/es/alquiler-coches-lujo-ibiza/','/fr/location-voiture-luxe-ibiza/','/de/luxusauto-mieten-ibiza/','/ar/luxury-car-rental-ibiza/',
'/wellness-ibiza/','/es/wellness-ibiza/','/fr/wellness-ibiza/','/de/wellness-ibiza/','/ar/wellness-ibiza/',
'/private-events-ibiza/','/es/eventos-privados-ibiza/','/fr/evenements-prives-ibiza/','/de/private-events-ibiza/','/ar/private-events-ibiza/',
'/bespoke-concierge-ibiza/','/es/concierge-a-medida-ibiza/','/fr/conciergerie-sur-mesure-ibiza/','/de/bespoke-concierge-ibiza/','/ar/bespoke-concierge-ibiza/'
]
CONTACTS={
'en':('/contact/',['Full Concierge','Private Chauffeur & Transportation','Luxury Villas & Private Stays','Yachts & Charters','Private Aviation','Restaurants, Beach Clubs & Nightlife','Security & Close Protection','Private Chefs & Villa Staffing','Luxury & Supercar Rental','Wellness & Beauty','Private Events & Celebrations','Lifestyle & Bespoke Requests']),
'es':('/es/contacto/',['Concierge completo','Chófer privado','Villa privada','Yate / Charter','Aviación privada','Restaurantes / Nightlife','Seguridad privada','Chef / Staffing','Alquiler de coche de lujo','Wellness','Evento privado','Solicitud a medida']),
'fr':('/fr/contact/',['Conciergerie complète','Chauffeur privé','Villa privée','Yacht / Charter','Aviation privée','Restaurants / Nightlife','Sécurité privée','Chef / Personnel de villa','Location de voiture de luxe','Wellness','Événement privé','Demande sur mesure']),
'de':('/de/kontakt/',['Full Concierge','Privater Chauffeur','Private Villa','Yacht / Charter','Private Aviation','Restaurants / Nightlife','Private Security','Private Chef / Villa Staff','Luxusauto / Supercar Rental','Wellness','Private Event','Bespoke Request']),
'ar':('/ar/contact/',['كونسيرج كامل','سائق خاص','فيلا خاصة','يخت / تشارتر','طيران خاص','مطاعم / حياة ليلية','أمن خاص','شيف / طاقم فيلا','تأجير سيارة فاخرة','عافية وجمال','فعالية خاصة','طلب مخصص'])
}


def page_for(path):
    return ROOT/path.strip('/')/'index.html'

# Normalize the Private Members Desk service selector to exactly the full 11-service catalog + Full Concierge.
for lang,(path,options) in CONTACTS.items():
    file=page_for(path)
    if not file.exists():raise SystemExit(f'Phase 63 contact missing: {path}')
    html=file.read_text(encoding='utf-8')
    opts=''.join(f'<option value="{escape(o)}">{escape(o)}</option>' for o in options)
    html,n=re.subn(r'<select\s+id="fService"[^>]*>.*?</select>',f'<select id="fService">{opts}</select>',html,count=1,flags=re.I|re.S)
    if n!=1:raise SystemExit(f'Phase 63 fService select missing: {path}')
    tag=f'<script src="{SCRIPT}"></script>'
    if tag not in html:html=html.replace('</body>',tag+'</body>',1)
    file.write_text(html,encoding='utf-8')

# Every service page receives the final routing layer after earlier scripts, so it wins deterministically.
for path in SERVICE_PAGES:
    file=page_for(path)
    if not file.exists():raise SystemExit(f'Phase 63 service missing: {path}')
    html=file.read_text(encoding='utf-8')
    tag=f'<script src="{SCRIPT}"></script>'
    if tag not in html:html=html.replace('</body>',tag+'</body>',1)
    file.write_text(html,encoding='utf-8')

# Validation: 55 service landings + 5 contact desks, no duplicate script and full selector coverage.
assert len(SERVICE_PAGES)==55
assert len(CONTACTS)==5
for path in SERVICE_PAGES:
    html=page_for(path).read_text(encoding='utf-8')
    assert html.count(SCRIPT)==1,path
    assert html.count('<h1')==1,path
    assert '<link rel="canonical"' in html,path
for lang,(path,options) in CONTACTS.items():
    html=page_for(path).read_text(encoding='utf-8')
    assert html.count(SCRIPT)==1,(lang,'script')
    m=re.search(r'<select\s+id="fService"[^>]*>(.*?)</select>',html,re.I|re.S)
    assert m,(lang,'select')
    assert m.group(1).count('<option')==12,(lang,'option count')
    for o in options:assert escape(o) in m.group(1),(lang,o)
    assert 'Luxury & Supercar Rental' in m.group(1) if lang=='en' else True
assert dest.exists() and dest.stat().st_size>4000
js=source.read_text(encoding='utf-8')
for key in ('chauffeur','villas','yacht','aviation','access','security','chef','car','wellness','events','bespoke'):assert f"'{key}'" in js or f":'{key}'" in js,key
assert 'templates' in js and 'SERVICE_BY_PATH' in js and 'CONTACT' in js
print('PASS: Phase 63 conversion routing covers 55 service pages + 5 Private Members Desks with localized WhatsApp context')
