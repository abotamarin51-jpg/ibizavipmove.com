from pathlib import Path

ROOT=Path('_site')
SLUGS=(
'private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning',
'villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')

DATA={
'en':{
 'prefix':'','target':'/private-concierge-ibiza/','kicker':'One point of coordination','title':'When the itinerary has several moving parts.','copy':'A planning note solves one moment. A private concierge becomes useful when arrivals, villas, chauffeurs, yachts, dining, nightlife, aviation or security need to move as one connected stay. The value is not adding more requests; it is keeping confirmed details, dependencies and changes under one accountable line of communication.','cta':'Explore Private Concierge Ibiza →'},
'es':{
 'prefix':'/es','target':'/es/concierge-privado-ibiza/','kicker':'Un solo punto de coordinación','title':'Cuando el itinerario tiene varias piezas en movimiento.','copy':'Una nota de planificación resuelve un momento concreto. Un concierge privado aporta valor cuando llegadas, villas, chóferes, yates, restaurantes, nightlife, aviación o seguridad deben funcionar como una sola estancia conectada. La clave no es sumar más solicitudes, sino mantener confirmaciones, dependencias y cambios bajo una única línea responsable.','cta':'Explorar Concierge Privado Ibiza →'},
'fr':{
 'prefix':'/fr','target':'/fr/conciergerie-privee-ibiza/','kicker':'Un seul point de coordination','title':'Lorsque l’itinéraire comporte plusieurs éléments mobiles.','copy':'Une note de planification répond à un moment précis. Une conciergerie privée devient utile lorsque arrivées, villas, chauffeurs, yachts, restaurants, nightlife, aviation ou sécurité doivent fonctionner comme un séjour connecté. La valeur n’est pas d’ajouter des demandes, mais de garder confirmations, dépendances et changements sous une seule ligne responsable.','cta':'Découvrir la Conciergerie Privée Ibiza →'},
'de':{
 'prefix':'/de','target':'/de/privater-concierge-ibiza/','kicker':'Ein zentraler Koordinationspunkt','title':'Wenn der Reiseplan mehrere bewegliche Teile hat.','copy':'Eine Planungsnotiz löst einen einzelnen Moment. Ein privater Concierge wird wertvoll, wenn Ankünfte, Villen, Chauffeure, Yachten, Dining, Nightlife, Aviation oder Security als ein zusammenhängender Aufenthalt funktionieren müssen. Entscheidend ist nicht mehr Anfragen zu stellen, sondern Bestätigungen, Abhängigkeiten und Änderungen über eine verantwortliche Linie zu steuern.','cta':'Privaten Concierge Ibiza ansehen →'},
'ar':{
 'prefix':'/ar','target':'/ar/private-concierge-ibiza/','kicker':'جهة تنسيق واحدة','title':'عندما يحتوي البرنامج على عدة عناصر متحركة.','copy':'تعالج ملاحظة التخطيط لحظة محددة، بينما تصبح خدمة الكونسيرج الخاص مهمة عندما يجب أن تعمل الوصولات والفلل والسائقون واليخوت والمطاعم والحياة الليلية والطيران والأمن ضمن إقامة واحدة مترابطة. القيمة ليست في إضافة طلبات أكثر، بل في إبقاء التأكيدات والاعتماديات والتغييرات تحت جهة اتصال واحدة مسؤولة.','cta':'استكشف الكونسيرج الخاص في إيبيزا ←'}}

def path_for(lang,slug):
    return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'

def page(path):
    return ROOT/path.strip('/')/'index.html'

def block(d):
    return (f'<section class="editorial ivm-concierge-pathway">'
            f'<div><div class="kicker dark">{d["kicker"]}</div><h2>{d["title"]}</h2></div>'
            f'<div><p class="large">{d["copy"]}</p><p><a href="{d["target"]}">{d["cta"]}</a></p></div>'
            f'</section>')

count=0
for lang,d in DATA.items():
    target=page(d['target'])
    if not target.exists(): raise SystemExit(f'Phase 95 target missing: {d["target"]}')
    for slug in SLUGS:
        path=path_for(lang,slug); f=page(path)
        if not f.exists(): raise SystemExit(f'Phase 95 article missing: {path}')
        html=f.read_text(encoding='utf-8')
        if 'ivm-concierge-pathway' in html: raise SystemExit(f'Phase 95 duplicate pathway: {path}')
        marker='<section class="ivm-intelligence-related"'
        pos=html.find(marker)
        if pos<0: raise SystemExit(f'Phase 95 related-notes marker missing: {path}')
        html=html[:pos]+block(d)+html[pos:]
        f.write_text(html,encoding='utf-8')
        count+=1

if count!=30: raise SystemExit(f'Phase 95 expected 30 articles, changed {count}')
print('PASS: Phase 95 Black Book authority routing — 30 localized planning notes now provide one contextual pathway to the same-language Private Concierge landing')
