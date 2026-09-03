from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
WA = 'https://wa.me/34600703303'
IMAGE = '/assets/images/nightlife.jpg'
TODAY = '2026-09-03'
EN_PATH = '/restaurants-nightlife-ibiza/'

SOURCES = {
 'es': ROOT/'es'/'concierge-privado-ibiza'/'index.html',
 'fr': ROOT/'fr'/'conciergerie-privee-ibiza'/'index.html',
 'de': ROOT/'de'/'privater-concierge-ibiza'/'index.html',
 'ar': ROOT/'ar'/'private-concierge-ibiza'/'index.html',
}

DATA = {
'es': {
 'path':'/es/restaurantes-nightlife-ibiza/','title':'Restaurantes, Beach Clubs y Nightlife Ibiza | Ibiza VIP Move','desc':'Reservas de restaurantes, beach clubs y nightlife en Ibiza con coordinación privada de horarios, transporte y movimientos de invitados por Ibiza VIP Move.','kicker':'Access · Ibiza','h1':'Dining y nightlife, integrados en tu itinerario.','lead':'Restaurantes, beach clubs y nightlife se coordinan mejor cuando horarios, transporte y movimientos de invitados forman parte del mismo brief.','section':'El acceso funciona mejor cuando el día está conectado.','large':'Coordinamos solicitudes de reservas y acceso junto con la logística confirmada alrededor de la estancia. Toda reserva o acceso depende siempre de disponibilidad, políticas del venue y confirmación.','items':[('01','El brief','Fecha, número de invitados, preferencias, horarios y contexto de la estancia.'),('02','Disponibilidad','Revisamos opciones relevantes; reservas y acceso permanecen sujetos a disponibilidad y confirmación del venue.'),('03','Movilidad','El chauffeur y los movimientos confirmados pueden alinearse con los horarios de dining o nightlife.'),('04','Cambios','Si el planning cambia, revisamos los elementos afectados según disponibilidad y condiciones aplicables.')],
 'cta':'Solicitar Access privado','faq':[('¿Qué información debo enviar?','Fecha, número de invitados, preferencias, horarios aproximados y cualquier prioridad relevante.'),('¿Podéis coordinar también el transporte?','Sí. Los movimientos de chauffeur confirmados pueden alinearse con los horarios de restaurantes, beach clubs o nightlife.'),('¿Las reservas o mesas están garantizadas?','No. Toda reserva, mesa o acceso depende de disponibilidad, políticas del venue y confirmación final.'),('¿Qué ocurre si cambia el horario?','Podemos revisar los elementos afectados y recoordinar cuando sea posible, sujeto a disponibilidad y condiciones aplicables.')]
},
'fr': {
 'path':'/fr/restaurants-nightlife-ibiza/','title':'Restaurants, Beach Clubs & Nightlife à Ibiza | Ibiza VIP Move','desc':'Restaurants, beach clubs et nightlife à Ibiza avec coordination privée des horaires, du chauffeur et des mouvements des invités par Ibiza VIP Move.','kicker':'Access · Ibiza','h1':'Dining et nightlife, intégrés à votre itinéraire.','lead':'Restaurants, beach clubs et nightlife sont plus fluides lorsque horaires, transport et mouvements des invités font partie du même brief.','section':'L’accès fonctionne mieux lorsque la journée est connectée.','large':'Nous coordonnons les demandes de réservation et d’accès avec la logistique confirmée du séjour. Toute réservation ou entrée reste soumise à disponibilité, aux politiques du lieu et à confirmation.','items':[('01','Le brief','Date, nombre d’invités, préférences, horaires et contexte du séjour.'),('02','Disponibilité','Nous examinons les options pertinentes ; réservations et accès restent soumis à disponibilité et confirmation du lieu.'),('03','Mobilité','Les mouvements chauffeur confirmés peuvent être alignés sur les horaires dining ou nightlife.'),('04','Changements','Si le planning évolue, nous réexaminons les éléments concernés selon disponibilité et conditions applicables.')],
 'cta':'Demander un Access privé','faq':[('Quelles informations faut-il envoyer ?','Date, nombre d’invités, préférences, horaires approximatifs et toute priorité utile.'),('Pouvez-vous coordonner aussi le transport ?','Oui. Les mouvements chauffeur confirmés peuvent être alignés sur les horaires des restaurants, beach clubs ou nightlife.'),('Les réservations ou tables sont-elles garanties ?','Non. Toute réservation, table ou entrée dépend de la disponibilité, des politiques du lieu et de la confirmation finale.'),('Que se passe-t-il si l’horaire change ?','Nous pouvons réexaminer et réorganiser les éléments concernés lorsque cela est possible, sous réserve de disponibilité et des conditions applicables.')]
},
'de': {
 'path':'/de/restaurants-nightlife-ibiza/','title':'Restaurants & Nightlife auf Ibiza | Ibiza VIP Move','desc':'Restaurants, Beach Clubs und Nightlife auf Ibiza mit privater Koordination von Zeiten, Chauffeur und Gästebewegungen durch Ibiza VIP Move.','kicker':'Access · Ibiza','h1':'Dining und Nightlife, in Ihre Reiseroute integriert.','lead':'Restaurants, Beach Clubs und Nightlife funktionieren reibungsloser, wenn Zeiten, Transport und Gästebewegungen Teil desselben Briefings sind.','section':'Access funktioniert besser, wenn der Tag verbunden ist.','large':'Wir koordinieren Reservierungs- und Access-Anfragen zusammen mit der bestätigten Logistik des Aufenthalts. Reservierungen und Einlass bleiben stets abhängig von Verfügbarkeit, Venue-Richtlinien und Bestätigung.','items':[('01','Briefing','Datum, Gästezahl, Präferenzen, Zeiten und Kontext des Aufenthalts.'),('02','Verfügbarkeit','Wir prüfen passende Optionen; Reservierungen und Access bleiben von Verfügbarkeit und Venue-Bestätigung abhängig.'),('03','Mobilität','Bestätigte Chauffeur-Bewegungen können mit Dining- oder Nightlife-Zeiten abgestimmt werden.'),('04','Änderungen','Wenn sich der Plan ändert, prüfen wir betroffene Elemente nach Verfügbarkeit und geltenden Bedingungen neu.')],
 'cta':'Privaten Access anfragen','faq':[('Welche Angaben sollte ich senden?','Datum, Gästezahl, Präferenzen, ungefähre Zeiten und relevante Prioritäten.'),('Können Sie auch den Transport koordinieren?','Ja. Bestätigte Chauffeur-Bewegungen können auf Restaurant-, Beach-Club- oder Nightlife-Zeiten abgestimmt werden.'),('Sind Reservierungen oder Tische garantiert?','Nein. Reservierungen, Tische und Einlass hängen von Verfügbarkeit, Venue-Richtlinien und finaler Bestätigung ab.'),('Was passiert bei Zeitplanänderungen?','Betroffene Elemente können, soweit möglich, neu geprüft und koordiniert werden – abhängig von Verfügbarkeit und geltenden Bedingungen.')]
},
'ar': {
 'path':'/ar/restaurants-nightlife-ibiza/','title':'مطاعم وBeach Clubs وحياة ليلية في إيبيزا | Ibiza VIP Move','desc':'تنسيق المطاعم وBeach Clubs والحياة الليلية في إيبيزا مع المواعيد والسائق وحركة الضيوف عبر Ibiza VIP Move.','kicker':'Access · إيبيزا','h1':'المطاعم والحياة الليلية ضمن برنامج واحد متكامل.','lead':'تكون تجربة المطاعم وBeach Clubs والحياة الليلية أكثر سلاسة عندما تكون المواعيد والتنقل وحركة الضيوف جزءاً من نفس الطلب.','section':'الوصول يعمل بشكل أفضل عندما يكون اليوم مترابطاً.','large':'ننسق طلبات الحجز والوصول مع اللوجستيات المؤكدة للإقامة. وتبقى جميع الحجوزات أو إمكانيات الدخول خاضعة للتوفر وسياسات المكان والتأكيد النهائي.','items':[('01','تفاصيل الطلب','التاريخ وعدد الضيوف والتفضيلات والمواعيد وسياق الإقامة.'),('02','التوفر','نراجع الخيارات المناسبة؛ وتبقى الحجوزات والدخول خاضعة للتوفر وتأكيد المكان.'),('03','التنقل','يمكن تنسيق تحركات السائق المؤكدة مع مواعيد المطاعم أو الحياة الليلية.'),('04','التغييرات','عند تغير البرنامج نراجع العناصر المتأثرة حسب التوفر والشروط المطبقة.')],
 'cta':'طلب Access خاص','faq':[('ما المعلومات التي يجب إرسالها؟','التاريخ وعدد الضيوف والتفضيلات والمواعيد التقريبية وأي أولوية مهمة.'),('هل يمكن تنسيق النقل أيضاً؟','نعم. يمكن ربط تحركات السائق المؤكدة بمواعيد المطاعم وBeach Clubs والحياة الليلية.'),('هل الحجوزات أو الطاولات مضمونة؟','لا. كل حجز أو طاولة أو دخول يعتمد على التوفر وسياسات المكان والتأكيد النهائي.'),('ماذا يحدث إذا تغير الموعد؟','يمكن مراجعة العناصر المتأثرة وإعادة تنسيقها عندما يكون ذلك ممكناً، وفق التوفر والشروط المطبقة.')]
}}

PATHS = {'en':EN_PATH, **{lang:d['path'] for lang,d in DATA.items()}}
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I|re.S)


def alternates():
    tags=''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{path}">' for lang,path in PATHS.items())
    return tags+f'<link rel="alternate" hreflang="x-default" href="{BASE}{EN_PATH}">'


def faq_schema(data):
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in data['faq']]}


def service_schema(lang,data):
    return {'@context':'https://schema.org','@type':'Service','name':data['h1'],'serviceType':'Restaurants, beach clubs and nightlife coordination in Ibiza','url':BASE+data['path'],'inLanguage':lang,'provider':{'@id':ORG},'areaServed':{'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},'image':BASE+IMAGE}


def breadcrumb_schema(data):
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Services','item':BASE+'/services/'},{'@type':'ListItem','position':3,'name':data['h1'],'item':BASE+data['path']}]}


def main_html(data):
    process=''.join(f'<article><span>{n}</span><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for n,h,p in data['items'])
    faq=''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in data['faq'])
    return f'''<main id="main-content"><section class="page-hero"><div class="page-hero-media"><img src="{IMAGE}" alt="{escape(data['h1'])} — Ibiza VIP Move" width="1800" height="1200" fetchpriority="high" decoding="async"></div><div><div class="kicker light">{escape(data['kicker'])}</div><h1>{escape(data['h1'])}</h1><p>{escape(data['lead'])}</p><a class="btn gold" href="{WA}">{escape(data['cta'])}</a></div></section><section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>{escape(data['section'])}</h2></div><div><p class="large">{escape(data['large'])}</p></div></section><section class="process"><div class="section-head"><div class="kicker dark">Private coordination</div><h2>{escape(data['section'])}</h2></div><div class="process-grid">{process}</div></section><section class="ivm-service-faq"><div class="section-head"><div class="kicker dark">Private brief</div><h2>{escape(data['cta'])}</h2></div><div class="ivm-service-faq-list">{faq}</div></section><section class="closing-simple"><h2>{escape(data['cta'])}</h2><p>Ibiza VIP Move · Private client support · Ibiza</p><a class="btn dark" href="{WA}">{escape(data['cta'])}</a></section></main>'''


def update_schemas(html,lang,data):
    seen={'web':False,'service':False,'bread':False,'faq':False}
    def repl(m):
        try:o=json.loads(m.group(1))
        except Exception:return m.group(0)
        if not isinstance(o,dict):return m.group(0)
        typ=o.get('@type')
        if typ in ('WebPage','AboutPage','CollectionPage') and not seen['web']:
            o['@type']='WebPage';o['name']=data['title'];o['url']=BASE+data['path'];o['description']=data['desc'];o['inLanguage']=lang;o['about']={'@id':ORG};o['publisher']={'@id':ORG};o['primaryImageOfPage']={'@type':'ImageObject','url':BASE+IMAGE};seen['web']=True
        elif typ=='Service':
            o=service_schema(lang,data);seen['service']=True
        elif typ=='BreadcrumbList':
            o=breadcrumb_schema(data);seen['bread']=True
        elif typ=='FAQPage':
            o=faq_schema(data);seen['faq']=True
        return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
    html=SCRIPT_RE.sub(repl,html)
    additions=[]
    if not seen['service']:additions.append(service_schema(lang,data))
    if not seen['bread']:additions.append(breadcrumb_schema(data))
    if not seen['faq']:additions.append(faq_schema(data))
    if additions:
        html=html.replace('</head>',''.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>' for o in additions)+'</head>',1)
    return html

created=[]
for lang,data in DATA.items():
    source=SOURCES[lang]
    if not source.exists():raise SystemExit(f'Phase 59 localized source missing: {lang}')
    html=source.read_text(encoding='utf-8')
    canonical=BASE+data['path']
    html=re.sub(r'<title>.*?</title>',f'<title>{escape(data["title"])}</title>',html,count=1,flags=re.I|re.S)
    html=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(data['desc'])+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")',lambda m:m.group(1)+canonical+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">','',html,flags=re.I)
    for prop,val in [('og:title',data['title']),('og:description',data['desc']),('og:url',canonical),('og:image',BASE+IMAGE)]:
        html=re.sub(rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")',lambda m,v=val:m.group(1)+escape(v)+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<main\b[^>]*>.*?</main>',main_html(data),html,count=1,flags=re.I|re.S)
    html=update_schemas(html,lang,data)
    html=html.replace('</head>',alternates()+'</head>',1)
    dest=ROOT/data['path'].strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8')
    created.append(data['path'])

# Reciprocal hreflang on the English canonical page.
en=ROOT/EN_PATH.strip('/')/'index.html'
if not en.exists():raise SystemExit('Phase 59 English Access canonical missing')
en_html=en.read_text(encoding='utf-8')
en_html=re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">','',en_html,flags=re.I)
en_html=en_html.replace('</head>',alternates()+'</head>',1)
en.write_text(en_html,encoding='utf-8')

# Point each localized Services hub to its localized Access page and keep Phase 58 ItemList accurate.
HUBS={'es':'/es/servicios/','fr':'/fr/services/','de':'/de/services/','ar':'/ar/services/'}
for lang,hub in HUBS.items():
    file=ROOT/hub.strip('/')/'index.html';html=file.read_text(encoding='utf-8')
    html=html.replace('href="/restaurants-nightlife-ibiza/"',f'href="{DATA[lang]["path"]}"')
    html=html.replace(BASE+EN_PATH,BASE+DATA[lang]['path'])
    file.write_text(html,encoding='utf-8')

# Sitemap additions.
sitemap=ROOT/'sitemap.xml';ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
tree=ET.parse(sitemap);root=tree.getroot();ns='http://www.sitemaps.org/schemas/sitemap/0.9'
existing={u.find(f'{{{ns}}}loc').text for u in root.findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for path in created:
    url=BASE+path
    if url not in existing:
        u=ET.SubElement(root,f'{{{ns}}}url');ET.SubElement(u,f'{{{ns}}}loc').text=url;ET.SubElement(u,f'{{{ns}}}lastmod').text=TODAY;ET.SubElement(u,f'{{{ns}}}changefreq').text='monthly';ET.SubElement(u,f'{{{ns}}}priority').text='0.78'
tree.write(sitemap,encoding='utf-8',xml_declaration=True)

# Validation.
assert len(created)==4
for lang,data in DATA.items():
    html=(ROOT/data['path'].strip('/')/'index.html').read_text(encoding='utf-8')
    assert html.count('<h1')==1,(lang,'h1')
    assert 'id="main-content"' in html and 'ivm-skip-link' in html,(lang,'a11y')
    assert BASE+data['path'] in html,(lang,'canonical')
    assert html.count('<details>')==4,(lang,'faq visible')
    assert 'FAQPage' in html and 'BreadcrumbList' in html and '"@type": "Service"' in html,(lang,'schema')
    for l,p in PATHS.items():assert f'hreflang="{l}" href="{BASE}{p}"' in html,(lang,l,'hreflang')
    hub=(ROOT/HUBS[lang].strip('/')/'index.html').read_text(encoding='utf-8')
    assert f'href="{data["path"]}"' in hub,(lang,'hub href')
    assert BASE+data['path'] in hub,(lang,'hub itemlist')
    assert BASE+EN_PATH not in hub,(lang,'old access url remains')
print('PASS: Phase 59 localized Access pages complete the six core service universes in ES/FR/DE/AR')
