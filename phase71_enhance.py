from pathlib import Path
from html import escape
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'; ORG=BASE+'/#organization'
SLUGS=['private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning','villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination']
REL={
'private-arrival':['private-aviation-ground-coordination','villa-arrival-planning','ibiza-august-planning'],
'ibiza-formentera-yacht-day':['ibiza-august-planning','nightlife-transport-planning','private-arrival'],
'ibiza-august-planning':['nightlife-transport-planning','villa-arrival-planning','ibiza-formentera-yacht-day'],
'villa-arrival-planning':['private-arrival','private-aviation-ground-coordination','ibiza-august-planning'],
'nightlife-transport-planning':['ibiza-august-planning','ibiza-formentera-yacht-day','villa-arrival-planning'],
'private-aviation-ground-coordination':['private-arrival','villa-arrival-planning','ibiza-august-planning']}
IMG={'private-arrival':'hero-desktop.jpg','ibiza-formentera-yacht-day':'yacht.jpg','ibiza-august-planning':'hero-desktop.jpg','villa-arrival-planning':'villa.jpg','nightlife-transport-planning':'nightlife.jpg','private-aviation-ground-coordination':'aviation.jpg'}
SHELL={'es':'es/sobre-nosotros/index.html','fr':'fr/a-propos/index.html','de':'de/ueber-uns/index.html','ar':'ar/about/index.html'}
CONTACT={'es':'/es/contacto/','fr':'/fr/contact/','de':'/de/kontakt/','ar':'/ar/contact/'}
SERVICE={
'es':['/es/aviacion-privada-ibiza/','/es/yate-privado-ibiza/','/es/concierge-privado-ibiza/','/es/villas-lujo-ibiza/','/es/restaurantes-nightlife-ibiza/','/es/aviacion-privada-ibiza/'],
'fr':['/fr/aviation-privee-ibiza/','/fr/location-yacht-ibiza/','/fr/conciergerie-privee-ibiza/','/fr/villas-luxe-ibiza/','/fr/restaurants-nightlife-ibiza/','/fr/aviation-privee-ibiza/'],
'de':['/de/private-aviation-ibiza/','/de/yachtcharter-ibiza/','/de/privater-concierge-ibiza/','/de/luxusvillen-ibiza/','/de/restaurants-nightlife-ibiza/','/de/private-aviation-ibiza/'],
'ar':['/ar/private-aviation-ibiza/','/ar/yacht-charter-ibiza/','/ar/private-concierge-ibiza/','/ar/luxury-villas-ibiza/','/ar/restaurants-nightlife-ibiza/','/ar/private-aviation-ibiza/']}
UI={
'es':{'hub':'Inteligencia privada de Ibiza','intro':'Notas prácticas para coordinar una estancia excepcional en Ibiza.','read':'Leer →','related':'Notas relacionadas.','next':'Leer después →','service':'Explorar servicio','cta':'Hablar con Concierge','private':'Asistencia privada','s1':'Confirma los datos esenciales','s2':'Conecta las dependencias','s3':'Mantén margen operativo'},
'fr':{'hub':'Intelligence privée d’Ibiza','intro':'Notes pratiques pour coordonner un séjour d’exception à Ibiza.','read':'Lire →','related':'Notes associées.','next':'Lire ensuite →','service':'Découvrir le service','cta':'Parler au Concierge','private':'Assistance privée','s1':'Confirmer les faits essentiels','s2':'Relier les dépendances','s3':'Garder une marge opérationnelle'},
'de':{'hub':'Private Ibiza Intelligence','intro':'Praktische Notizen für die Koordination eines außergewöhnlichen Ibiza-Aufenthalts.','read':'Lesen →','related':'Verwandte Planungsnotizen.','next':'Weiterlesen →','service':'Service ansehen','cta':'Concierge kontaktieren','private':'Private Unterstützung','s1':'Die wichtigsten Fakten bestätigen','s2':'Abhängigkeiten verbinden','s3':'Operative Reserve behalten'},
'ar':{'hub':'دليل التخطيط الخاص في إيبيزا','intro':'ملاحظات عملية لتنسيق إقامة استثنائية في إيبيزا.','read':'اقرأ ←','related':'ملاحظات ذات صلة.','next':'اقرأ التالي ←','service':'استكشف الخدمة','cta':'تحدث مع الكونسيرج','private':'مساعدة خاصة','s1':'أكد المعلومات الأساسية','s2':'اربط التفاصيل المترابطة','s3':'احتفظ بهامش تشغيلي'}}
TOP={
'es':[
('Llegada privada','La llegada privada','Llegada privada a Ibiza | Vuelo, chófer y villa','Coordina vuelo, equipaje, chófer, acceso a la villa y primeras reservas en una llegada privada a Ibiza.','Aviación, equipaje, chófer y villa alineados antes de que aterrice el principal.','vuelo, pasajeros, equipaje, vehículos y acceso a la villa'),
('En el mar','Ibiza & Formentera en yate','Ibiza y Formentera en yate | Guía privada','Planifica un día de yate entre Ibiza y Formentera conectando marina, chófer, almuerzo, regreso y noche.','Marina, chófer, almuerzo y noche conectados como un único día en el mar.','salida de la villa, marina, ruta, almuerzo y regreso'),
('Temporada alta','El briefing de agosto','Ibiza en agosto | Guía privada de planificación','Planifica villas, chófer, yates, restaurantes, nightlife y cambios de última hora durante agosto en Ibiza.','Un marco práctico cuando demanda, tráfico y presión operativa están en su punto más alto.','alojamiento, transporte, yates, reservas prioritarias y tráfico'),
('Estancias privadas','El briefing de llegada a la villa','Llegada a una villa en Ibiza | Briefing privado','Planificación privada de acceso, equipaje, chófer y primeras horas de una estancia en villa en Ibiza.','Acceso, equipaje, chófer y primeras horas alineados con antelación.','acceso, equipaje, staff de la villa, habitaciones y siguiente movimiento'),
('Acceso y movimiento','El plan de movimientos nocturnos','Transporte nightlife Ibiza | Plan privado','Planificación privada de transporte nocturno para villas, restaurantes, clubs, cambios de horario y regreso.','Villa, cena, nightlife y regreso planificados como un solo movimiento.','villa, cena, venue, puntos de recogida, salidas separadas y regreso'),
('Aviación privada','Del avión a Ibiza','Coordinación en tierra de aviación privada en Ibiza','Coordina horario de vuelo, equipaje, vehículos, acceso a la villa y cambios de ETA en una llegada de aviación privada.','Vuelo, equipaje, capacidad de vehículos y villa conectados en una sola entrega en tierra.','horario del vuelo, equipaje, capacidad de vehículos, destino y ETA')],
'fr':[
('Arrivée privée','L’arrivée privée','Arrivée privée à Ibiza | Vol, chauffeur et villa','Coordonner vol, bagages, chauffeur, accès villa et premiers rendez-vous lors d’une arrivée privée à Ibiza.','Aviation, bagages, chauffeur et villa alignés avant l’atterrissage du principal.','vol, voyageurs, bagages, véhicules et accès à la villa'),
('En mer','Ibiza & Formentera en yacht','Ibiza et Formentera en yacht | Guide privé','Planifier une journée yacht Ibiza–Formentera avec marina, chauffeur, déjeuner, retour et soirée.','Marina, chauffeur, déjeuner et soirée connectés comme une seule journée en mer.','départ villa, marina, route, déjeuner et retour'),
('Haute saison','Le brief d’août','Ibiza en août | Guide privé de planification','Planifier villas, chauffeurs, yachts, restaurants, nightlife et changements de dernière minute en août à Ibiza.','Un cadre pratique quand disponibilité, trafic et pression opérationnelle atteignent leur maximum.','hébergement, transport, yachts, réservations prioritaires et trafic'),
('Séjours privés','Le brief d’arrivée à la villa','Arrivée villa à Ibiza | Brief privé','Planification privée de l’accès, des bagages, du chauffeur et des premières heures d’un séjour villa à Ibiza.','Accès, bagages, chauffeur et premières heures alignés en amont.','accès, bagages, staff villa, chambres et prochain mouvement'),
('Accès & mobilité','Le plan de mobilité nocturne','Transport nightlife Ibiza | Plan privé','Planification privée des transports nightlife pour villas, restaurants, clubs, changements d’horaires et retours.','Villa, dîner, nightlife et retour planifiés comme un seul mouvement.','villa, dîner, lieu, points de pickup, départs séparés et retour'),
('Aviation privée','De l’avion à Ibiza','Coordination au sol aviation privée Ibiza','Coordonner horaire de vol, bagages, véhicules, accès villa et changements d’ETA pour une arrivée en aviation privée.','Vol, bagages, capacité véhicules et villa connectés dans un seul relais au sol.','horaire du vol, bagages, capacité véhicules, destination et ETA')],
'de':[
('Private Ankunft','Die private Ankunft','Private Ankunft auf Ibiza | Flug, Chauffeur und Villa','Private Ankunft auf Ibiza koordinieren: Flug, Gepäck, Chauffeur, Villenzugang und erste Termine.','Aviation, Gepäck, Chauffeur und Villa abgestimmt, bevor der Principal landet.','Flug, Gäste, Gepäck, Fahrzeuge und Villenzugang'),
('Auf See','Ibiza & Formentera mit der Yacht','Ibiza & Formentera mit der Yacht | Private Planung','Yachttag Ibiza–Formentera planen: Marina, Chauffeur, Lunch, Rückkehr und Abendprogramm.','Marina, Chauffeur, Lunch und Abend als ein zusammenhängender Tag auf See.','Villa-Abfahrt, Marina, Route, Lunch und Rückkehr'),
('Hochsaison','Das August-Briefing','Ibiza im August | Private Planungsnotiz','Villen, Chauffeure, Yachten, Restaurants, Nightlife und kurzfristige Änderungen im August auf Ibiza planen.','Ein praktischer Rahmen, wenn Verfügbarkeit, Verkehr und operativer Druck am höchsten sind.','Unterkunft, Transport, Yachten, priorisierte Reservierungen und Verkehr'),
('Private Aufenthalte','Das Villa-Ankunftsbriefing','Villa-Ankunft auf Ibiza | Privates Briefing','Private Planung von Zugang, Gepäck, Chauffeur und ersten Stunden eines Villa-Aufenthalts auf Ibiza.','Zugang, Gepäck, Chauffeur und erste Villastunden im Voraus abgestimmt.','Zugang, Gepäck, Villa-Staff, Zimmer und nächste Bewegung'),
('Zugang & Bewegung','Der Nightlife-Bewegungsplan','Nightlife Transport Ibiza | Privater Bewegungsplan','Private Nightlife-Transportplanung für Villen, Restaurants, Clubs, Zeitänderungen und Rückfahrten.','Villa, Dinner, Nightlife und Rückfahrt als eine Bewegung geplant.','Villa, Dinner, Venue, Pickup-Punkte, getrennte Abfahrten und Rückfahrt'),
('Private Aviation','Vom Flugzeug nach Ibiza','Private Aviation Bodenkoordination Ibiza','Flugzeit, Gepäck, Fahrzeuge, Villenzugang und ETA-Änderungen bei einer Private-Aviation-Ankunft koordinieren.','Flug, Gepäck, Fahrzeugkapazität und Villa in einer Bodenübergabe verbunden.','Flugzeit, Gepäck, Fahrzeugkapazität, Ziel und ETA')],
'ar':[
('وصول خاص','الوصول الخاص','الوصول الخاص إلى إيبيزا | الطيران والسائق والفيلا','تنسيق الرحلة والأمتعة والسائق والدخول إلى الفيلا والخطط الأولى عند الوصول الخاص إلى إيبيزا.','تنسيق الطيران والأمتعة والسائق والفيلا قبل هبوط الضيف الرئيسي.','الرحلة والضيوف والأمتعة والسيارات والدخول إلى الفيلا'),
('في البحر','إيبيزا وفورمينتيرا باليخت','إيبيزا وفورمينتيرا باليخت | دليل خاص','تخطيط يوم يخت بين إيبيزا وفورمينتيرا مع المرسى والسائق والغداء والعودة وبرنامج المساء.','ربط المرسى والسائق والغداء والمساء ضمن يوم بحري واحد.','مغادرة الفيلا والمرسى والمسار والغداء والعودة'),
('موسم الذروة','خطة أغسطس','إيبيزا في أغسطس | دليل تخطيط خاص','تخطيط الفلل والسائقين واليخوت والمطاعم والحياة الليلية والتغييرات الأخيرة خلال أغسطس في إيبيزا.','إطار عملي عندما يصل الطلب وحركة المرور والضغط التشغيلي إلى أعلى مستوياته.','السكن والنقل واليخوت والحجوزات ذات الأولوية وحركة المرور'),
('إقامات خاصة','خطة الوصول إلى الفيلا','الوصول إلى فيلا في إيبيزا | خطة خاصة','تخطيط خاص للدخول والأمتعة والسائق والساعات الأولى من الإقامة في فيلا في إيبيزا.','تنسيق الدخول والأمتعة والسائق والساعات الأولى في الفيلا مسبقاً.','الدخول والأمتعة وفريق الفيلا والغرف والحركة التالية'),
('الدخول والتنقل','خطة التنقل الليلي','تنقلات الحياة الليلية في إيبيزا | خطة خاصة','تخطيط خاص للنقل الليلي للفلل والمطاعم والنوادي وتغييرات الوقت والعودة.','تنسيق الفيلا والعشاء والحياة الليلية والعودة كحركة واحدة.','الفيلا والعشاء والمكان ونقاط الاستلام والمغادرات المنفصلة والعودة'),
('الطيران الخاص','من الطائرة إلى إيبيزا','تنسيق الطيران الخاص على الأرض في إيبيزا','تنسيق توقيت الرحلة والأمتعة والسيارات والدخول إلى الفيلا وتغيّر ETA عند الوصول بطيران خاص.','ربط الرحلة والأمتعة وسعة السيارات واستعداد الفيلا ضمن تسليم أرضي واحد.','وقت الرحلة والأمتعة وسعة السيارات والوجهة ووقت الوصول')]}
BODY={
'es':('Reúne {focus} en una sola versión del briefing antes de confirmar los movimientos conectados.','Trata {focus} como partes del mismo itinerario, no como reservas aisladas. Un cambio en una pieza debe revisarse en las demás.','Deja margen para tráfico, clima, horarios y cambios del grupo. Define qué es fijo, qué puede moverse y quién autoriza el cambio.'),
'fr':('Réunissez {focus} dans une seule version du brief avant de confirmer les mouvements connectés.','Traitez {focus} comme des éléments du même itinéraire, pas comme des réservations isolées. Tout changement doit être répercuté sur les dépendances.','Gardez une marge pour trafic, météo, horaires et changements du groupe. Identifiez ce qui est fixe, flexible et qui peut autoriser une modification.'),
'de':('Führen Sie {focus} in einer einzigen Briefing-Version zusammen, bevor verbundene Bewegungen bestätigt werden.','Behandeln Sie {focus} als Teile desselben Reiseplans, nicht als isolierte Buchungen. Änderungen müssen auf die verbundenen Elemente übertragen werden.','Lassen Sie Reserve für Verkehr, Wetter, Zeitplan und Gruppenänderungen. Definieren Sie feste und flexible Elemente sowie die Person, die Änderungen freigibt.'),
'ar':('اجمع {focus} في نسخة واحدة من الخطة قبل تأكيد الحركات المرتبطة.','تعامل مع {focus} كعناصر من برنامج رحلة واحد، لا كحجوزات منفصلة. أي تغيير يجب أن ينعكس على العناصر المرتبطة.','اترك هامشاً لحركة المرور والطقس والتوقيت وتغييرات المجموعة. حدد ما هو ثابت وما يمكن تغييره ومن يملك قرار التعديل.')}

def url(lang,slug=None):
    if lang=='en': return '/ibiza-intelligence/' if slug is None else f'/ibiza-intelligence/{slug}/'
    return f'/{lang}/ibiza-intelligence/' if slug is None else f'/{lang}/ibiza-intelligence/{slug}/'
def fp(path): return ROOT/path.strip('/')/'index.html'
def alt(slug=None):
    return ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{url(l,slug)}">' for l in ('en','es','fr','de','ar'))+f'<link rel="alternate" hreflang="x-default" href="{BASE}{url("en",slug)}">'

def strip_schema(html):
    pat=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
    def f(m):
        try:o=json.loads(m.group(1))
        except:return m.group(0)
        return '' if isinstance(o,dict) and o.get('@type') in ('WebPage','Article','BlogPosting','CollectionPage','BreadcrumbList') else m.group(0)
    return pat.sub(f,html)

def set_head(html,title,desc,canonical,image,slug=None):
    html=re.sub(r'<title>.*?</title>',f'<title>{escape(title)}</title>',html,count=1,flags=re.I|re.S)
    html=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(desc,quote=True)+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<link\b[^>]*rel="canonical"[^>]*>',f'<link rel="canonical" href="{canonical}">',html,count=1,flags=re.I)
    html=re.sub(r'<link\b[^>]*rel="alternate"[^>]*hreflang="[^"]+"[^>]*>','',html,flags=re.I)
    for key,val in [('og:title',title),('og:description',desc),('og:url',canonical),('og:image',BASE+image)]:
        pat=rf'(<meta\s+property="{re.escape(key)}"\s+content=")[^"]*(")'
        if re.search(pat,html,re.I): html=re.sub(pat,lambda m:m.group(1)+escape(val,quote=True)+m.group(2),html,count=1,flags=re.I)
    return html.replace('</head>',alt(slug)+'</head>',1)

def add_schema(html,*objs): return html.replace('</head>',''.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>' for o in objs)+'</head>',1)

def article_schema(lang,slug,d):
    c=BASE+url(lang,slug); svc=SERVICE[lang][SLUGS.index(slug)]
    a={'@context':'https://schema.org','@type':'Article','headline':d[1],'name':d[1],'url':c,'description':d[3],'image':BASE+'/assets/images/'+IMG[slug],'inLanguage':lang,'dateModified':'2026-09-03','author':{'@id':ORG},'publisher':{'@id':ORG},'mainEntityOfPage':{'@type':'WebPage','@id':c},'isRelatedTo':[{'@type':'WebPage','url':BASE+url(lang,s)} for s in REL[slug]],'mentions':{'@type':'Service','url':BASE+svc}}
    b={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'+lang+'/'},{'@type':'ListItem','position':2,'name':'The Ibiza Black Book','item':BASE+url(lang)},{'@type':'ListItem','position':3,'name':d[1],'item':c}]}
    return a,b

def hub_schema(lang):
    c=BASE+url(lang)
    coll={'@context':'https://schema.org','@type':'CollectionPage','name':'The Ibiza Black Book','url':c,'description':UI[lang]['intro'],'inLanguage':lang,'publisher':{'@id':ORG},'mainEntity':{'@type':'ItemList','numberOfItems':6,'itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+url(lang,s),'name':TOP[lang][i][1]} for i,s in enumerate(SLUGS)]}}
    b={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'+lang+'/'},{'@type':'ListItem','position':2,'name':'The Ibiza Black Book','item':c}]}
    return coll,b

def article_main(lang,slug,d):
    ui=UI[lang]; body=BODY[lang]; svc=SERVICE[lang][SLUGS.index(slug)]
    secs=''.join(f'<section><h2>{escape(h)}</h2><p>{escape(p.format(focus=d[5]))}</p></section>' for h,p in zip((ui['s1'],ui['s2'],ui['s3']),body))
    cards=''.join(f'<a class="ivm-intelligence-related-card" href="{url(lang,r)}"><span>{escape(TOP[lang][SLUGS.index(r)][0])}</span><strong>{escape(TOP[lang][SLUGS.index(r)][1])}</strong><p>{escape(TOP[lang][SLUGS.index(r)][4])}</p><b>{escape(ui["next"])}</b></a>' for r in REL[slug])
    return f'''<main id="main-content"><section class="page-hero intelligence-hero"><div class="page-hero-media"><img src="/assets/images/{IMG[slug]}" alt="{escape(d[1])} — Ibiza VIP Move" width="2200" height="1400" fetchpriority="high" decoding="async"></div><div><div class="kicker light">The Ibiza Black Book · {escape(d[0])}</div><h1>{escape(d[1])}</h1><p>{escape(d[4])}</p></div></section><article class="article-shell"><div class="article-meta"><span>Ibiza VIP Move</span><span>{escape(ui["hub"])}</span><span>Ibiza · Spain</span></div><div class="article-body">{secs}<aside class="article-cta"><div class="kicker dark">{escape(ui["private"])}</div><h2>{escape(ui["hub"])}</h2><p>{escape(ui["intro"])}</p><a class="btn dark" href="{CONTACT[lang]}">{escape(ui["cta"])}</a></aside></div></article><section class="ivm-intelligence-service"><div class="ivm-intelligence-service-inner"><div><h3>{escape(d[0])}</h3><p>{escape(d[3])}</p></div><a class="btn dark" href="{svc}">{escape(ui["service"])}</a></div></section><section class="ivm-intelligence-related"><div class="ivm-intelligence-related-inner"><div class="ivm-intelligence-related-head"><div><div class="eyebrow">The Ibiza Black Book</div><h2>{escape(ui["related"])}</h2></div><p>{escape(ui["intro"])}</p></div><div class="ivm-intelligence-related-grid">{cards}</div></div></section></main>'''

def hub_main(lang):
    ui=UI[lang]
    cards=''.join(f'<a class="intel-card" href="{url(lang,s)}"><span>{escape(TOP[lang][i][0])}</span><h3>{escape(TOP[lang][i][1])}</h3><p>{escape(TOP[lang][i][4])}</p><b>{escape(ui["read"])}</b></a>' for i,s in enumerate(SLUGS))
    return f'''<main id="main-content"><section class="page-hero intelligence-hero"><div class="page-hero-media"><img src="/assets/images/hero-desktop.jpg" alt="The Ibiza Black Book — Ibiza VIP Move" width="2200" height="1400" fetchpriority="high" decoding="async"></div><div><div class="kicker light">The Ibiza Black Book</div><h1>The Ibiza Black Book</h1><p>{escape(ui["intro"])}</p></div></section><section class="editorial"><div><div class="kicker dark">{escape(ui["hub"])}</div><h2>{escape(ui["intro"])}</h2></div><div><p class="large">{escape(ui["intro"])}</p></div></section><section class="intelligence-home hub"><div class="intelligence-grid">{cards}</div></section><section class="closing"><h2>{escape(ui["hub"])}</h2><p>{escape(ui["intro"])}</p><a class="btn dark" href="{CONTACT[lang]}">{escape(ui["cta"])}</a></section></main>'''

created=[]
for lang in ('es','fr','de','ar'):
    shell=(ROOT/SHELL[lang]).read_text(encoding='utf-8')
    if '/assets/phase43.css' not in shell: shell=shell.replace('</head>','<link rel="stylesheet" href="/assets/phase43.css?v=43"></head>',1)
    h=set_head(strip_schema(shell),'The Ibiza Black Book | '+UI[lang]['hub']+' | Ibiza VIP Move',UI[lang]['intro'],BASE+url(lang),'/assets/images/hero-desktop.jpg')
    h=re.sub(r'<main\b[^>]*>.*?</main>',hub_main(lang),h,count=1,flags=re.I|re.S); h=add_schema(h,*hub_schema(lang))
    dst=fp(url(lang)); dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(h,encoding='utf-8'); created.append(dst)
    for i,slug in enumerate(SLUGS):
        d=TOP[lang][i]
        a=set_head(strip_schema(shell),d[2],d[3],BASE+url(lang,slug),'/assets/images/'+IMG[slug],slug)
        a=re.sub(r'<main\b[^>]*>.*?</main>',article_main(lang,slug,d),a,count=1,flags=re.I|re.S); a=add_schema(a,*article_schema(lang,slug,d))
        dst=fp(url(lang,slug)); dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(a,encoding='utf-8'); created.append(dst)

for slug in [None]+SLUGS:
    p=fp(url('en',slug)); t=p.read_text(encoding='utf-8')
    t=re.sub(r'<link\b[^>]*rel="alternate"[^>]*hreflang="[^"]+"[^>]*>','',t,flags=re.I)
    p.write_text(t.replace('</head>',alt(slug)+'</head>',1),encoding='utf-8')

for lang in ('es','fr','de','ar'):
    for p in (ROOT/lang).rglob('*.html'):
        t=p.read_text(encoding='utf-8')
        if url(lang) not in t and '</footer>' in t:
            p.write_text(t.replace('</footer>',f'<a class="ivm-footer-black-book" href="{url(lang)}">The Ibiza Black Book</a></footer>',1),encoding='utf-8')

for slug in [None]+SLUGS:
    exp={BASE+url(l,slug) for l in ('en','es','fr','de','ar')}
    for lang in ('en','es','fr','de','ar'):
        p=fp(url(lang,slug)); t=p.read_text(encoding='utf-8')
        assert p.exists() and t.lower().count('<h1')==1,(lang,slug)
        got={href for code,href in re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',t,re.I) if code!='x-default'}
        assert got==exp,(lang,slug)
        if slug and lang!='en': assert t.count('ivm-intelligence-related-card')==3,(lang,slug)
print(f'PASS: Phase 71 international Black Book — {len(created)} new pages; 7 complete five-language editorial clusters')