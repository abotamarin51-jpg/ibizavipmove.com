from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
WA = 'https://wa.me/34600703303'
STYLE = '/assets/phase40.css?v=40'

HUBS = {
    'en': '/services/',
    'es': '/es/servicios/',
    'fr': '/fr/services/',
    'de': '/de/services/',
    'ar': '/ar/services/',
}

COPY = {
'es': {
 'title':'Servicios de concierge privado en Ibiza | Ibiza VIP Move',
 'desc':'Servicios privados en Ibiza: chófer, villas, yates, restaurantes y nightlife, aviación, seguridad, chefs, wellness, eventos y peticiones a medida.',
 'kicker':'Servicios privados · Ibiza','h1':'Un ecosistema privado.\nTodo conectado.','lead':'Movilidad, estancias, yates, acceso, aviación, protección y lifestyle coordinados desde un único contacto de confianza en Ibiza.',
 'core_label':'Seis universos principales','core_h2':'La estructura detrás de una estancia excepcional.','core_p':'Cada servicio puede solicitarse de forma independiente. Cuando el brief incluye varios, coordinamos horarios, personas y detalles operativos alrededor de un mismo itinerario.',
 'extended_label':'Más allá del núcleo','extended_h2':'Lifestyle alrededor de la estancia.','extended_p':'El brief privado suele ir más allá de transporte, alojamiento y acceso. Estos servicios adicionales pueden coordinarse cuando son relevantes para el cliente y su itinerario.',
 'cta_h2':'¿Necesitas varios servicios coordinados?','cta_p':'Utiliza el concierge en lugar de gestionar cada categoría por separado. Comparte fechas, invitados y prioridades; aclaramos las piezas y continuamos en privado.','cta':'Iniciar private brief','explore':'Explorar','request':'Solicitar concierge',
 'core':[('Move','Chófer privado y transporte','Movilidad privada para aeropuerto, villas, marinas, restaurantes, nightlife y jornadas completas.','/es/chauffeur-privado-ibiza/','/assets/images/chauffeur.jpg'),('Stay','Villas de lujo y estancias privadas','Estancias coordinadas alrededor de acceso, invitados, personal y ritmo del itinerario.','/es/villas-lujo-ibiza/','/assets/images/villa.jpg'),('Sea','Yates y charters','Ibiza y Formentera desde el mar, conectadas con marina, transporte, dining y el resto del día.','/es/yate-privado-ibiza/','/assets/images/yacht.jpg'),('Access','Restaurantes, beach clubs y nightlife','Reservas, mesas VIP y acceso coordinados con horarios, transporte y movimientos de invitados.','/restaurants-nightlife-ibiza/','/assets/images/nightlife.jpg'),('Fly','Aviación privada','Vuelo, equipaje y coordinación terrestre alineados con el transporte y el itinerario confirmado.','/es/aviacion-privada-ibiza/','/assets/images/aviation.jpg'),('Protect','Seguridad y close protection','Seguridad privada discreta coordinada alrededor del principal, movimientos, ubicaciones y agenda.','/es/seguridad-privada-ibiza/','/assets/images/security.jpg')],
 'ext':[('At Home','Chefs privados y personal de villa','Chefs, mayordomos, housekeeping y soporte familiar.','/private-chef-staffing-ibiza/'),('Drive','Luxury & supercar rental','Vehículos ejecutivos, SUV, deportivos y entrega discreta.','/luxury-car-rental-ibiza/'),('Wellness','Wellness & beauty','Masajes, trainers, yoga, belleza y sesiones privadas.','/wellness-ibiza/'),('Occasions','Eventos y celebraciones privadas','Cenas privadas, celebraciones, entretenimiento y logística de invitados.','/private-events-ibiza/'),('Bespoke','Lifestyle y peticiones a medida','Sourcing, solicitudes especiales y necesidades fuera de categorías estándar.','/bespoke-concierge-ibiza/')]
},
'fr': {
 'title':'Services de conciergerie privée à Ibiza | Ibiza VIP Move','desc':'Services privés à Ibiza : chauffeur, villas, yachts, restaurants et nightlife, aviation, sécurité, chefs, wellness, événements et demandes sur mesure.',
 'kicker':'Services privés · Ibiza','h1':'Un écosystème privé.\nTout est connecté.','lead':'Mobilité, séjours, yachts, accès, aviation, protection et lifestyle coordonnés par un seul contact de confiance à Ibiza.',
 'core_label':'Six univers principaux','core_h2':'La structure derrière un séjour exceptionnel.','core_p':'Chaque service peut être demandé séparément. Lorsqu’un brief en réunit plusieurs, les horaires, les personnes et les détails opérationnels sont alignés autour du même itinéraire.',
 'extended_label':'Au-delà du cœur','extended_h2':'Lifestyle autour du séjour.','extended_p':'Le brief privé va souvent au-delà du transport, du séjour et de l’accès. Ces services complémentaires peuvent être coordonnés lorsqu’ils sont pertinents.',
 'cta_h2':'Plusieurs services à coordonner ?','cta_p':'Passez par le concierge plutôt que de gérer chaque catégorie séparément. Partagez dates, invités et priorités ; nous clarifions le brief et poursuivons en privé.','cta':'Commencer le brief','explore':'Découvrir','request':'Demander concierge',
 'core':[('Move','Chauffeur privé & transport','Mobilité privée pour aéroport, villas, marinas, restaurants, nightlife et journées complètes.','/fr/chauffeur-prive-ibiza/','/assets/images/chauffeur.jpg'),('Stay','Villas de luxe & séjours privés','Séjours coordonnés autour de l’accès, des invités, du personnel et du rythme de l’itinéraire.','/fr/villas-luxe-ibiza/','/assets/images/villa.jpg'),('Sea','Yachts & charters','Ibiza et Formentera par la mer, reliées aux horaires de marina, transport, dining et soirée.','/fr/location-yacht-ibiza/','/assets/images/yacht.jpg'),('Access','Restaurants, beach clubs & nightlife','Réservations, tables VIP et accès coordonnés avec horaires, transport et mouvements des invités.','/restaurants-nightlife-ibiza/','/assets/images/nightlife.jpg'),('Fly','Aviation privée','Vol, bagages et coordination au sol alignés avec le transport et l’itinéraire confirmé.','/fr/aviation-privee-ibiza/','/assets/images/aviation.jpg'),('Protect','Sécurité & protection rapprochée','Sécurité privée discrète coordonnée autour du principal, des mouvements, lieux et horaires.','/fr/securite-privee-ibiza/','/assets/images/security.jpg')],
 'ext':[('At Home','Chefs privés & personnel de villa','Chefs, majordomes, housekeeping et support familial.','/private-chef-staffing-ibiza/'),('Drive','Luxury & supercar rental','Véhicules exécutifs, SUV, sportives et livraison discrète.','/luxury-car-rental-ibiza/'),('Wellness','Wellness & beauté','Massage, trainers, yoga, beauté et récupération privée.','/wellness-ibiza/'),('Occasions','Événements & célébrations privées','Dîners privés, célébrations, entertainment et logistique invités.','/private-events-ibiza/'),('Bespoke','Lifestyle & demandes sur mesure','Sourcing et demandes spéciales hors catégories standard.','/bespoke-concierge-ibiza/')]
},
'de': {
 'title':'Private Concierge Services Ibiza | Ibiza VIP Move','desc':'Private Services auf Ibiza: Chauffeur, Villen, Yachten, Restaurants und Nightlife, private Aviation, Security, Köche, Wellness, Events und individuelle Wünsche.',
 'kicker':'Private Services · Ibiza','h1':'Ein privates Ökosystem.\nAlles verbunden.','lead':'Mobilität, Aufenthalte, Yachten, Access, Aviation, Schutz und Lifestyle über einen vertrauenswürdigen Ibiza-Kontakt koordiniert.',
 'core_label':'Sechs Kernbereiche','core_h2':'Die Struktur hinter einem außergewöhnlichen Aufenthalt.','core_p':'Jeder Service kann einzeln angefragt werden. Wenn mehrere benötigt werden, stimmen wir Zeiten, Personen und operative Details rund um dieselbe Reiseroute ab.',
 'extended_label':'Über den Kern hinaus','extended_h2':'Lifestyle rund um den Aufenthalt.','extended_p':'Private Anforderungen gehen oft über Transport, Unterkunft und Access hinaus. Diese zusätzlichen Services können passend zum Brief koordiniert werden.',
 'cta_h2':'Mehrere Services gemeinsam koordinieren?','cta_p':'Nutzen Sie den Concierge, statt jede Kategorie separat zu verwalten. Teilen Sie Daten, Gäste und Prioritäten; wir strukturieren die Details und setzen das Gespräch privat fort.','cta':'Private Anfrage starten','explore':'Entdecken','request':'Concierge anfragen',
 'core':[('Move','Privater Chauffeur & Transport','Private Mobilität für Flughafen, Villen, Marinas, Restaurants, Nightlife und ganze Tage.','/de/privater-chauffeur-ibiza/','/assets/images/chauffeur.jpg'),('Stay','Luxusvillen & private Aufenthalte','Aufenthalte abgestimmt auf Zugang, Gäste, Personal und den Rhythmus der Reiseroute.','/de/luxusvillen-ibiza/','/assets/images/villa.jpg'),('Sea','Yachten & Charter','Ibiza und Formentera auf dem Wasser, verbunden mit Marina-Zeiten, Transport, Dining und Abendplanung.','/de/yachtcharter-ibiza/','/assets/images/yacht.jpg'),('Access','Restaurants, Beach Clubs & Nightlife','Reservierungen, VIP-Tische und Access mit Zeiten, Transport und Gästebewegungen abgestimmt.','/restaurants-nightlife-ibiza/','/assets/images/nightlife.jpg'),('Fly','Private Aviation','Flug, Gepäck und Bodenkoordination mit Weiterfahrt und bestätigter Ibiza-Route verbunden.','/de/private-aviation-ibiza/','/assets/images/aviation.jpg'),('Protect','Security & Close Protection','Diskrete private Security rund um Principal, Bewegungen, Orte und Zeitplan.','/de/private-sicherheit-ibiza/','/assets/images/security.jpg')],
 'ext':[('At Home','Private Köche & Villa Staff','Köche, Butler, Housekeeping und Family Support.','/private-chef-staffing-ibiza/'),('Drive','Luxury & Supercar Rental','Executive Fahrzeuge, SUVs, Sportwagen und diskrete Lieferung.','/luxury-car-rental-ibiza/'),('Wellness','Wellness & Beauty','Massage, Trainer, Yoga, Beauty und private Recovery.','/wellness-ibiza/'),('Occasions','Private Events & Feiern','Private Dinner, Feiern, Entertainment und Gästelogistik.','/private-events-ibiza/'),('Bespoke','Lifestyle & individuelle Wünsche','Sourcing und besondere Anforderungen außerhalb Standardkategorien.','/bespoke-concierge-ibiza/')]
},
'ar': {
 'title':'خدمات كونسيرج خاصة في إيبيزا | Ibiza VIP Move','desc':'خدمات خاصة في إيبيزا تشمل السائق والفلل واليخوت والمطاعم والحياة الليلية والطيران الخاص والأمن والطهاة والعافية والفعاليات والطلبات المخصصة.',
 'kicker':'خدمات خاصة · إيبيزا','h1':'منظومة خاصة واحدة.\nكل التفاصيل مترابطة.','lead':'التنقل والإقامة واليخوت والوصول والطيران والحماية واللايف ستايل بتنسيق من جهة اتصال موثوقة واحدة في إيبيزا.',
 'core_label':'ستة مجالات أساسية','core_h2':'الهيكل الذي يقف خلف إقامة استثنائية.','core_p':'يمكن طلب كل خدمة بشكل مستقل. وعند الحاجة إلى عدة خدمات، يتم تنسيق المواعيد والأشخاص والتفاصيل التشغيلية حول برنامج واحد.',
 'extended_label':'ما بعد الأساسيات','extended_h2':'دعم لايف ستايل حول الإقامة.','extended_p':'غالباً ما تتجاوز المتطلبات الخاصة النقل والإقامة والوصول. ويمكن تنسيق الخدمات الإضافية عندما تكون مناسبة للضيف والبرنامج.',
 'cta_h2':'هل تحتاج إلى تنسيق عدة خدمات معاً؟','cta_p':'استخدم الكونسيرج بدلاً من إدارة كل فئة منفصلة. أرسل التواريخ والضيوف والأولويات وسنرتب التفاصيل ونواصل بشكل خاص.','cta':'بدء الطلب الخاص','explore':'اكتشف','request':'طلب كونسيرج',
 'core':[('Move','سائق خاص وتنقل','تنقل خاص للمطار والفلل والمراسي والمطاعم والحياة الليلية والأيام الكاملة.','/ar/private-chauffeur-ibiza/','/assets/images/chauffeur.jpg'),('Stay','فلل فاخرة وإقامات خاصة','إقامات منسقة حول الوصول والضيوف والطاقم وإيقاع البرنامج.','/ar/luxury-villas-ibiza/','/assets/images/villa.jpg'),('Sea','يخوت وتأجير خاص','إيبيزا وفورمينتيرا بحراً مع تنسيق المرسى والتنقل والطعام وبقية اليوم.','/ar/yacht-charter-ibiza/','/assets/images/yacht.jpg'),('Access','مطاعم وBeach Clubs وحياة ليلية','حجوزات وطاولات VIP ووصول منسق مع المواعيد والتنقل وحركة الضيوف.','/restaurants-nightlife-ibiza/','/assets/images/nightlife.jpg'),('Fly','طيران خاص','تنسيق الرحلة والأمتعة والحركة الأرضية مع النقل والبرنامج المؤكد.','/ar/private-aviation-ibiza/','/assets/images/aviation.jpg'),('Protect','أمن وحماية خاصة','أمن خاص وسري منسق حول الضيف الرئيسي والحركة والمواقع والجدول.','/ar/private-security-ibiza/','/assets/images/security.jpg')],
 'ext':[('At Home','طهاة خاصون وطاقم الفلل','طهاة وخدمة منزلية ودعم عائلي.','/private-chef-staffing-ibiza/'),('Drive','سيارات فاخرة وسوبركار','سيارات تنفيذية وSUV ورياضية مع تسليم خاص.','/luxury-car-rental-ibiza/'),('Wellness','عافية وجمال','مساج ومدربون ويوغا وجمال وجلسات خاصة.','/wellness-ibiza/'),('Occasions','فعاليات واحتفالات خاصة','عشاء خاص واحتفالات وترفيه ولوجستيات الضيوف.','/private-events-ibiza/'),('Bespoke','لايف ستايل وطلبات مخصصة','توفير خاص وطلبات خارج الفئات المعتادة.','/bespoke-concierge-ibiza/')]
}}


def alternates():
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{path}">' for lang,path in HUBS.items()) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/services/">'


def main_html(t):
    index=''.join(f'<a href="{href}"><span>{label}</span><strong>{title.split(" & ")[0]}</strong><small>{copy.split(".")[0]}.</small></a>' for label,title,copy,href,_ in t['core'])
    core=''.join(f'<a class="ivm-core-card" href="{href}"><img src="{img}" alt="{escape(title)} — Ibiza VIP Move" loading="lazy" decoding="async" width="1800" height="1200"><div class="ivm-core-copy"><span>{label}</span><h3>{title}</h3><p>{copy}</p><b>{t["explore"]} {label} →</b></div></a>' for label,title,copy,href,img in t['core'])
    ext=''.join(f'<a class="ivm-extended-card" href="{href}"><span>{label}</span><strong>{title}</strong><p>{copy}</p><b>{t["explore"]} →</b></a>' for label,title,copy,href in t['ext'])
    h1=t['h1'].replace('\n','<br>')
    return f'''<main id="main-content"><section class="page-hero"><div class="page-hero-media"><img src="/assets/images/hero-desktop.jpg" alt="Ibiza VIP Move private services" width="2200" height="1400" fetchpriority="high" decoding="async"></div><div><div class="kicker light">{t['kicker']}</div><h1>{h1}</h1><p>{t['lead']}</p><a class="btn gold" href="/contact/">{t['request']}</a><div class="ivm-services-index">{index}</div></div></section><section class="ivm-core-services"><div class="ivm-core-head"><div><div class="eyebrow">{t['core_label']}</div><h2>{t['core_h2']}</h2></div><p>{t['core_p']}</p></div><div class="ivm-core-grid">{core}</div></section><section class="ivm-extended"><div class="ivm-extended-inner"><div class="ivm-extended-head"><div><div class="eyebrow">{t['extended_label']}</div><h2>{t['extended_h2']}</h2></div><p>{t['extended_p']}</p></div><div class="ivm-extended-grid">{ext}</div></div></section><section class="ivm-services-concierge"><div class="ivm-services-concierge-inner"><div><h2>{t['cta_h2']}</h2></div><div><p>{t['cta_p']}</p><div class="ivm-services-actions"><a class="btn dark" href="/contact/">{t['cta']}</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div></div></div></section></main>'''


def update_schema(text, lang, path, t):
    canonical=BASE+path
    pattern=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
    def repl(m):
        try: obj=json.loads(m.group(1))
        except Exception:return m.group(0)
        if isinstance(obj,dict) and obj.get('@type')=='WebPage':
            obj['name']=t['title'];obj['url']=canonical;obj['description']=t['desc'];obj['inLanguage']=lang
        return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>'
    return pattern.sub(repl,text)

# English hub: complete reciprocal hreflang cluster.
en=ROOT/'services'/'index.html'
text=en.read_text(encoding='utf-8')
text=re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">','',text,flags=re.I)
text=text.replace('</head>',alternates()+'</head>',1)
en.write_text(text,encoding='utf-8')

for lang,path in HUBS.items():
    if lang=='en':continue
    t=COPY[lang]
    source=ROOT/lang/'index.html'
    if not source.exists():raise SystemExit(f'Language shell missing: {lang}')
    html=source.read_text(encoding='utf-8')
    html=re.sub(r'<html\s+lang="[^"]+"(?:\s+dir="[^"]+")?',f'<html lang="{lang}"'+(' dir="rtl"' if lang=='ar' else ''),html,count=1,flags=re.I)
    html=re.sub(r'<title>.*?</title>',f'<title>{escape(t["title"])}</title>',html,count=1,flags=re.I|re.S)
    html=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(t['desc'])+m.group(2),html,count=1,flags=re.I)
    canonical=BASE+path
    html=re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")',lambda m:m.group(1)+canonical+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">','',html,flags=re.I)
    html=html.replace('</head>',alternates()+'</head>',1)
    html=re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(t['title'])+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(t['desc'])+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'(<meta\s+property="og:url"\s+content=")[^"]*(")',lambda m:m.group(1)+canonical+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<main\b[^>]*>.*?</main>',main_html(t),html,count=1,flags=re.I|re.S)
    body=re.search(r'<body(?:\s+class="([^"]*)")?>',html,re.I)
    if body:
        classes=(body.group(1) or '').split()
        if 'ivm-services-hub' not in classes:classes.append('ivm-services-hub')
        repl='<body class="'+' '.join(classes)+'">';html=html[:body.start()]+repl+html[body.end():]
    if STYLE not in html:html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
    html=update_schema(html,lang,path,t)
    dest=ROOT/path.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8')

# Add all hubs to sitemap; Phase 41 will normalize sitemap parity later.
sitemap=ROOT/'sitemap.xml'
s=sitemap.read_text(encoding='utf-8')
for path in HUBS.values():
    url=BASE+path
    if url not in s:s=s.replace('</urlset>',f'<url><loc>{url}</loc></url></urlset>')
sitemap.write_text(s,encoding='utf-8')

# Validation.
for lang,path in HUBS.items():
    p=ROOT/path.strip('/')/'index.html'
    h=p.read_text(encoding='utf-8')
    assert h.count('<h1')==1,(lang,'h1')
    assert h.count('class="ivm-core-card"')==6,(lang,'core')
    assert h.count('class="ivm-extended-card"')==5,(lang,'extended')
    assert h.count('hreflang=')>=6,(lang,'hreflang')
    assert BASE+path in h,(lang,'canonical')
    assert STYLE in h,(lang,'style')
print('PASS: Phase 44 multilingual Services hubs complete across EN/ES/FR/DE/AR')
