from pathlib import Path
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
CSS='/assets/phase86.css?v=86'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

HUBS={
'en':{
 'path':'/services/','eyebrow':'Ibiza service area','title':'Private services, coordinated across Ibiza.','lead':'Ibiza VIP Move coordinates confirmed private services around the actual geography of each stay — airport, villa, marina, dining, nightlife and onward movements — rather than treating locations as isolated bookings.','note':'These are service areas, not public walk-in offices. Meetings and services are coordinated at villas, hotels, marinas, Ibiza Airport and other agreed locations.',
 'areas':[
  ('Eivissa · Ibiza Town','Airport arrivals, hotels, Dalt Vila, city dining and central movements.'),
  ('Marina Botafoch · Talamanca','Marina, yacht, hotel, dining and nightlife coordination close to Ibiza Town.'),
  ('Sant Josep de sa Talaia','Villa stays, airport-side logistics and south-west island movements.'),
  ('Cala Jondal · Es Cubells','South-coast villas, beach plans, yacht days and chauffeur timing.'),
  ('Santa Eulària des Riu','Hotels, villas, marina movements and family or multi-day itineraries.'),
  ('Roca Llisa · Cala Llonga','East-coast villas, resort stays and private movements around the itinerary.'),
  ('Sant Antoni de Portmany','Hotels, villas, sunset plans, nightlife and west-coast movements.'),
  ('Santa Gertrudis · central Ibiza','Villa stays and island-wide itineraries linking north, east, west and Ibiza Town.')]
},
'es':{
 'path':'/es/servicios/','eyebrow':'Cobertura en Ibiza','title':'Servicios privados coordinados por toda Ibiza.','lead':'Ibiza VIP Move coordina los servicios confirmados alrededor de la geografía real de cada estancia — aeropuerto, villa, marina, restaurantes, nightlife y desplazamientos — en lugar de tratar cada ubicación como una reserva aislada.','note':'Estas son zonas de servicio, no oficinas abiertas al público. Las reuniones y los servicios se coordinan en villas, hoteles, marinas, Ibiza Airport y otros puntos acordados.',
 'areas':[
  ('Eivissa · Ibiza Town','Llegadas al aeropuerto, hoteles, Dalt Vila, restaurantes y movimientos por la ciudad.'),
  ('Marina Botafoch · Talamanca','Coordinación de marina, yates, hoteles, restaurantes y nightlife junto a Ibiza Town.'),
  ('Sant Josep de sa Talaia','Villas, logística cercana al aeropuerto y desplazamientos por el suroeste de la isla.'),
  ('Cala Jondal · Es Cubells','Villas del sur, beach plans, días de yate y timing de chauffeur.'),
  ('Santa Eulària des Riu','Hoteles, villas, marina y estancias familiares o itinerarios de varios días.'),
  ('Roca Llisa · Cala Llonga','Villas de la costa este, resorts y movimientos privados alrededor del itinerario.'),
  ('Sant Antoni de Portmany','Hoteles, villas, sunsets, nightlife y movimientos por la costa oeste.'),
  ('Santa Gertrudis · centro de Ibiza','Villas e itinerarios que conectan norte, este, oeste e Ibiza Town.')]
},
'fr':{
 'path':'/fr/services/','eyebrow':'Couverture à Ibiza','title':'Services privés coordonnés dans toute Ibiza.','lead':'Ibiza VIP Move coordonne les services confirmés autour de la géographie réelle de chaque séjour — aéroport, villa, marina, restaurants, nightlife et déplacements — plutôt que de traiter chaque lieu comme une réservation isolée.','note':'Il s’agit de zones de service et non de bureaux ouverts au public. Les rendez-vous et services sont coordonnés dans les villas, hôtels, marinas, à Ibiza Airport et dans d’autres lieux convenus.',
 'areas':[
  ('Eivissa · Ibiza Town','Arrivées aéroport, hôtels, Dalt Vila, restaurants et déplacements en ville.'),
  ('Marina Botafoch · Talamanca','Coordination marina, yachts, hôtels, restaurants et nightlife près d’Ibiza Town.'),
  ('Sant Josep de sa Talaia','Villas, logistique proche de l’aéroport et déplacements dans le sud-ouest.'),
  ('Cala Jondal · Es Cubells','Villas du sud, beach plans, journées yacht et timing chauffeur.'),
  ('Santa Eulària des Riu','Hôtels, villas, marina et itinéraires famille ou multi-jours.'),
  ('Roca Llisa · Cala Llonga','Villas de la côte est, resorts et déplacements privés liés à l’itinéraire.'),
  ('Sant Antoni de Portmany','Hôtels, villas, sunsets, nightlife et déplacements sur la côte ouest.'),
  ('Santa Gertrudis · centre d’Ibiza','Villas et itinéraires reliant le nord, l’est, l’ouest et Ibiza Town.')]
},
'de':{
 'path':'/de/services/','eyebrow':'Servicegebiet Ibiza','title':'Private Services auf ganz Ibiza koordiniert.','lead':'Ibiza VIP Move koordiniert bestätigte private Services entlang der tatsächlichen Geografie jedes Aufenthalts — Flughafen, Villa, Marina, Dining, Nightlife und weitere Fahrten — statt einzelne Orte als getrennte Buchungen zu behandeln.','note':'Dies sind Servicegebiete, keine öffentlich zugänglichen Büros. Meetings und Services werden an Villen, Hotels, Marinas, am Ibiza Airport und an weiteren vereinbarten Orten koordiniert.',
 'areas':[
  ('Eivissa · Ibiza Town','Flughafenankünfte, Hotels, Dalt Vila, Dining und zentrale Fahrten.'),
  ('Marina Botafoch · Talamanca','Marina-, Yacht-, Hotel-, Dining- und Nightlife-Koordination nahe Ibiza Town.'),
  ('Sant Josep de sa Talaia','Villen, flughafennahe Logistik und Fahrten im Südwesten der Insel.'),
  ('Cala Jondal · Es Cubells','Villen an der Südküste, Beach-Pläne, Yachttage und Chauffeur-Timing.'),
  ('Santa Eulària des Riu','Hotels, Villen, Marina und Familien- oder mehrtägige Reisepläne.'),
  ('Roca Llisa · Cala Llonga','Villen an der Ostküste, Resorts und private Fahrten rund um den Reiseplan.'),
  ('Sant Antoni de Portmany','Hotels, Villen, Sunset-Pläne, Nightlife und Fahrten an der Westküste.'),
  ('Santa Gertrudis · zentrales Ibiza','Villen und Inselrouten zwischen Norden, Osten, Westen und Ibiza Town.')]
},
'ar':{
 'path':'/ar/services/','eyebrow':'نطاق الخدمة في إيبيزا','title':'خدمات خاصة منسقة في مختلف مناطق إيبيزا.','lead':'تنسق Ibiza VIP Move الخدمات المؤكدة وفق جغرافية الإقامة الفعلية — المطار والفيلا والمارينا والمطاعم والحياة الليلية والتنقلات — بدلاً من التعامل مع كل موقع كحجز منفصل.','note':'هذه مناطق خدمة وليست مكاتب مفتوحة للجمهور. يتم تنسيق الاجتماعات والخدمات في الفلل والفنادق والمراسي ومطار إيبيزا وغيرها من المواقع المتفق عليها.',
 'areas':[
  ('Eivissa · Ibiza Town','الوصول من المطار والفنادق وDalt Vila والمطاعم والتنقلات داخل المدينة.'),
  ('Marina Botafoch · Talamanca','تنسيق المارينا واليخوت والفنادق والمطاعم والحياة الليلية قرب Ibiza Town.'),
  ('Sant Josep de sa Talaia','الفلل والخدمات اللوجستية قرب المطار والتنقلات في جنوب غرب الجزيرة.'),
  ('Cala Jondal · Es Cubells','فلل الساحل الجنوبي وخطط الشاطئ وأيام اليخت وتوقيت السائق الخاص.'),
  ('Santa Eulària des Riu','الفنادق والفلل والمارينا وبرامج العائلات أو الإقامات متعددة الأيام.'),
  ('Roca Llisa · Cala Llonga','فلل الساحل الشرقي والمنتجعات والتنقلات الخاصة المرتبطة بالبرنامج.'),
  ('Sant Antoni de Portmany','الفنادق والفلل وخطط الغروب والحياة الليلية والتنقلات على الساحل الغربي.'),
  ('Santa Gertrudis · وسط إيبيزا','الفلل وبرامج الجزيرة التي تربط الشمال والشرق والغرب وIbiza Town.')]
}
}

PLACE_NAMES=['Eivissa / Ibiza Town','Marina Botafoch / Talamanca','Sant Josep de sa Talaia','Cala Jondal / Es Cubells','Santa Eulària des Riu','Roca Llisa / Cala Llonga','Sant Antoni de Portmany','Santa Gertrudis de Fruitera']

def fpath(path):return ROOT/path.strip('/')/'index.html'

def section(data):
    cards=''.join(f'<div class="ivm-local-area"><b>{name}</b><p>{copy}</p></div>' for name,copy in data['areas'])
    return f'<section class="ivm-local-coverage" aria-label="Ibiza service area"><div class="ivm-local-coverage-inner"><div class="ivm-local-coverage-head"><div><div class="eyebrow">{data["eyebrow"]}</div><h2>{data["title"]}</h2></div><p>{data["lead"]}</p></div><div class="ivm-local-grid">{cards}</div><p class="ivm-local-note">{data["note"]}</p></div></section>'

def patch_collection(html):
    found=0
    def repl(m):
        nonlocal found
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        if not isinstance(o,dict) or o.get('@type')!='CollectionPage':return m.group(0)
        o['spatialCoverage']=[{'@type':'Place','name':name} for name in PLACE_NAMES]
        found+=1
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    html=SCRIPT_RE.sub(repl,html)
    if found!=1:raise SystemExit(f'Phase 86 expected one CollectionPage, found {found}')
    return html

for lang,data in HUBS.items():
    f=fpath(data['path'])
    if not f.exists():raise SystemExit(f'Phase 86 hub missing: {data["path"]}')
    html=f.read_text(encoding='utf-8')
    if 'ivm-local-coverage' in html:raise SystemExit(f'Phase 86 duplicate local coverage: {data["path"]}')
    if CSS not in html:
        html=html.replace('</head>',f'<link rel="stylesheet" href="{CSS}"></head>',1)
    marker='<section class="ivm-trade-bridge"'
    pos=html.find(marker)
    if pos<0:raise SystemExit(f'Phase 86 trade bridge marker missing: {data["path"]}')
    html=html[:pos]+section(data)+html[pos:]
    html=patch_collection(html)
    f.write_text(html,encoding='utf-8')

print('PASS: Phase 86 local Ibiza relevance — five multilingual Services hubs enriched with eight real service areas and structured spatialCoverage')
