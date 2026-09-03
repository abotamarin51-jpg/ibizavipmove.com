from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)

HUBS = {
'en': {
 'path':'/services/','name':'Private Services in Ibiza',
 'items':[
  ('Private Chauffeur Ibiza','/private-chauffeur-ibiza/'),('Luxury Villas Ibiza','/luxury-villas-ibiza/'),('Yacht Charter Ibiza','/yacht-charter-ibiza/'),('Restaurants & Nightlife Ibiza','/restaurants-nightlife-ibiza/'),('Private Aviation Ibiza','/private-aviation-ibiza/'),('Private Security Ibiza','/private-security-ibiza/'),('Private Chef & Staffing Ibiza','/private-chef-staffing-ibiza/'),('Luxury Car Rental Ibiza','/luxury-car-rental-ibiza/'),('Wellness Ibiza','/wellness-ibiza/'),('Private Events Ibiza','/private-events-ibiza/'),('Bespoke Concierge Ibiza','/bespoke-concierge-ibiza/')]
},
'es': {
 'path':'/es/servicios/','name':'Servicios privados en Ibiza',
 'items':[
  ('Chófer privado en Ibiza','/es/chauffeur-privado-ibiza/'),('Villas de lujo en Ibiza','/es/villas-lujo-ibiza/'),('Yate privado en Ibiza','/es/yate-privado-ibiza/'),('Restaurantes y nightlife en Ibiza','/restaurants-nightlife-ibiza/'),('Aviación privada en Ibiza','/es/aviacion-privada-ibiza/'),('Seguridad privada en Ibiza','/es/seguridad-privada-ibiza/'),('Chef privado y staffing en Ibiza','/private-chef-staffing-ibiza/'),('Luxury car rental Ibiza','/luxury-car-rental-ibiza/'),('Wellness Ibiza','/wellness-ibiza/'),('Eventos privados Ibiza','/private-events-ibiza/'),('Concierge a medida Ibiza','/bespoke-concierge-ibiza/')]
},
'fr': {
 'path':'/fr/services/','name':'Services privés à Ibiza',
 'items':[
  ('Chauffeur privé à Ibiza','/fr/chauffeur-prive-ibiza/'),('Villas de luxe à Ibiza','/fr/villas-luxe-ibiza/'),('Location de yacht à Ibiza','/fr/location-yacht-ibiza/'),('Restaurants et nightlife à Ibiza','/restaurants-nightlife-ibiza/'),('Aviation privée à Ibiza','/fr/aviation-privee-ibiza/'),('Sécurité privée à Ibiza','/fr/securite-privee-ibiza/'),('Chef privé et personnel de villa','/private-chef-staffing-ibiza/'),('Luxury car rental Ibiza','/luxury-car-rental-ibiza/'),('Wellness à Ibiza','/wellness-ibiza/'),('Événements privés à Ibiza','/private-events-ibiza/'),('Conciergerie sur mesure Ibiza','/bespoke-concierge-ibiza/')]
},
'de': {
 'path':'/de/services/','name':'Private Services auf Ibiza',
 'items':[
  ('Privater Chauffeur auf Ibiza','/de/privater-chauffeur-ibiza/'),('Luxusvillen auf Ibiza','/de/luxusvillen-ibiza/'),('Yachtcharter auf Ibiza','/de/yachtcharter-ibiza/'),('Restaurants und Nightlife auf Ibiza','/restaurants-nightlife-ibiza/'),('Private Aviation auf Ibiza','/de/private-aviation-ibiza/'),('Private Sicherheit auf Ibiza','/de/private-sicherheit-ibiza/'),('Private Köche und Villa Staff','/private-chef-staffing-ibiza/'),('Luxury Car Rental Ibiza','/luxury-car-rental-ibiza/'),('Wellness Ibiza','/wellness-ibiza/'),('Private Events Ibiza','/private-events-ibiza/'),('Bespoke Concierge Ibiza','/bespoke-concierge-ibiza/')]
},
'ar': {
 'path':'/ar/services/','name':'الخدمات الخاصة في إيبيزا',
 'items':[
  ('سائق خاص في إيبيزا','/ar/private-chauffeur-ibiza/'),('فلل فاخرة في إيبيزا','/ar/luxury-villas-ibiza/'),('يخوت خاصة في إيبيزا','/ar/yacht-charter-ibiza/'),('مطاعم وحياة ليلية في إيبيزا','/restaurants-nightlife-ibiza/'),('طيران خاص في إيبيزا','/ar/private-aviation-ibiza/'),('أمن خاص في إيبيزا','/ar/private-security-ibiza/'),('طهاة وطاقم فلل','/private-chef-staffing-ibiza/'),('تأجير سيارات فاخرة','/luxury-car-rental-ibiza/'),('عافية في إيبيزا','/wellness-ibiza/'),('فعاليات خاصة في إيبيزا','/private-events-ibiza/'),('كونسيرج مخصص في إيبيزا','/bespoke-concierge-ibiza/')]
},
}


def types_in(html):
    found=[]
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if isinstance(o,dict):
            t=o.get('@type'); found.extend(t if isinstance(t,list) else [t])
    return found


def collection_schema(lang, data):
    url=BASE+data['path']
    item_list={
      '@type':'ItemList','name':data['name'],'numberOfItems':len(data['items']),
      'itemListElement':[
        {'@type':'ListItem','position':i,'name':name,'url':BASE+path}
        for i,(name,path) in enumerate(data['items'],1)
      ]
    }
    return {
      '@context':'https://schema.org','@type':'CollectionPage','name':data['name'],'url':url,
      'inLanguage':lang,'about':{'@id':ORG},'publisher':{'@id':ORG},'mainEntity':item_list,
    }


def breadcrumb_schema(data):
    return {
      '@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},
        {'@type':'ListItem','position':2,'name':data['name'],'item':BASE+data['path']},
      ]
    }

updated=0
for lang,data in HUBS.items():
    file=ROOT/data['path'].strip('/')/'index.html'
    if not file.exists():raise SystemExit(f'Phase 58 hub missing: {data["path"]}')
    html=file.read_text(encoding='utf-8')
    current=types_in(html)
    additions=[]
    if 'CollectionPage' not in current:additions.append(collection_schema(lang,data))
    if 'BreadcrumbList' not in current:additions.append(breadcrumb_schema(data))
    if additions:
        payload=''.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>' for o in additions)
        html=html.replace('</head>',payload+'</head>',1)
        file.write_text(html,encoding='utf-8')
    updated+=1

for lang,data in HUBS.items():
    html=(ROOT/data['path'].strip('/')/'index.html').read_text(encoding='utf-8')
    collection=None
    bread=False
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if not isinstance(o,dict):continue
        if o.get('@type')=='CollectionPage':collection=o
        if o.get('@type')=='BreadcrumbList':bread=True
    assert collection is not None,(lang,'collection')
    assert bread,(lang,'breadcrumb')
    main=collection.get('mainEntity')
    assert isinstance(main,dict) and main.get('@type')=='ItemList',(lang,'itemlist')
    items=main.get('itemListElement')
    assert isinstance(items,list) and len(items)==11,(lang,'11 items')
    assert [x.get('position') for x in items]==list(range(1,12)),(lang,'positions')
    urls={x.get('url') for x in items}
    assert urls=={BASE+p for _,p in data['items']},(lang,'urls')
    assert collection.get('about',{}).get('@id')==ORG,(lang,'org')
    assert html.count('<h1')==1,(lang,'h1')

print(f'PASS: Phase 58 five multilingual Services hubs expressed as CollectionPage + 11-item ItemList with breadcrumbs')
