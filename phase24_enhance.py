from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
WA = 'https://wa.me/34600703303'
TODAY = '2026-09-02'

ALTS = {
    'en': '/contact/',
    'es': '/es/contacto/',
    'fr': '/fr/contact/',
    'de': '/de/kontakt/',
    'ar': '/ar/contact/'
}

DATA = {
'es': {
'path':'/es/contacto/','dir':'ltr','title':'Solicitar Concierge Privado en Ibiza | Ibiza VIP Move','desc':'Envía tu brief privado a Ibiza VIP Move para coordinar chófer, villas, yates, restaurantes, aviación privada, seguridad y servicios de lifestyle en Ibiza.','kicker':'Private Brief · Ibiza','h1':'Cuéntanos cómo quieres vivir Ibiza.','intro':'Comparte lo esencial. Continuaremos la conversación de forma privada y coordinaremos los siguientes pasos alrededor de tu estancia.','name':'Nombre','phone':'WhatsApp / Teléfono','arrival':'Llegada','departure':'Salida','service':'Servicio principal','guests':'Huéspedes','brief':'Brief / Detalles','button':'Enviar brief por WhatsApp','note':'Al enviar, se abrirá una conversación privada de WhatsApp con los datos anteriores.','direct':'¿Necesitas hablar directamente?','directcopy':'Para solicitudes urgentes o del mismo día, WhatsApp suele ser la forma más rápida de contactar con nuestro concierge.','whatsapp':'WhatsApp Concierge','next':'Qué ocurre después','nextsub':'De tu primer mensaje a una estancia coordinada.','steps':[('Envía lo esencial','Fechas, huéspedes, servicio principal y prioridades que ya conozcas.'),('Aclaramos el brief','Confirmamos los detalles necesarios para entender correctamente la solicitud.'),('Coordinamos','Una vez definido el alcance, alineamos los servicios y la logística en Ibiza.'),('Seguimos disponibles','Mantenemos soporte mientras evoluciona el itinerario o cambian los planes.')],
'options':['Concierge completo','Chófer privado','Villa privada','Yate / Charter','Aviación privada','Restaurantes / Nightlife','Seguridad privada','Chef / Staffing','Wellness','Evento privado','Solicitud a medida']},
'fr': {
'path':'/fr/contact/','dir':'ltr','title':'Demander une Conciergerie Privée à Ibiza | Ibiza VIP Move','desc':'Envoyez votre brief privé à Ibiza VIP Move pour coordonner chauffeur, villa, yacht, aviation privée, restaurants, sécurité et lifestyle à Ibiza.','kicker':'Private Brief · Ibiza','h1':'Dites-nous à quoi votre Ibiza doit ressembler.','intro':'Partagez l’essentiel. Nous poursuivrons la conversation en privé et coordonnerons les prochaines étapes autour de votre séjour.','name':'Nom','phone':'WhatsApp / Téléphone','arrival':'Arrivée','departure':'Départ','service':'Service principal','guests':'Invités','brief':'Brief / Détails','button':'Envoyer le brief via WhatsApp','note':'L’envoi ouvrira une conversation WhatsApp privée avec les informations ci-dessus.','direct':'Besoin de parler directement ?','directcopy':'Pour une demande urgente ou le jour même, WhatsApp est généralement le moyen le plus rapide de joindre la conciergerie.','whatsapp':'WhatsApp Concierge','next':'La suite','nextsub':'Du premier message à un séjour coordonné.','steps':[('Partagez l’essentiel','Dates, invités, service principal et priorités déjà connues.'),('Nous clarifions le brief','Nous confirmons les détails nécessaires pour comprendre correctement la demande.'),('Nous coordonnons','Une fois le périmètre confirmé, les services et la logistique à Ibiza sont alignés.'),('Nous restons disponibles','Nous restons joignables lorsque l’itinéraire évolue ou que les plans changent.')],
'options':['Conciergerie complète','Chauffeur privé','Villa privée','Yacht / Charter','Aviation privée','Restaurants / Nightlife','Sécurité privée','Chef / Personnel de villa','Wellness','Événement privé','Demande sur mesure']},
'de': {
'path':'/de/kontakt/','dir':'ltr','title':'Private Concierge Anfrage Ibiza | Ibiza VIP Move','desc':'Senden Sie Ihr privates Ibiza-Briefing für Chauffeur, Villen, Yachten, Privatluftfahrt, Restaurants, Sicherheit und Lifestyle-Koordination.','kicker':'Private Brief · Ibiza','h1':'Sagen Sie uns, wie sich Ihr Ibiza anfühlen soll.','intro':'Teilen Sie die wichtigsten Angaben. Wir führen das Gespräch privat weiter und koordinieren die nächsten Schritte rund um Ihren Aufenthalt.','name':'Name','phone':'WhatsApp / Telefon','arrival':'Anreise','departure':'Abreise','service':'Hauptservice','guests':'Gäste','brief':'Briefing / Details','button':'Briefing per WhatsApp senden','note':'Beim Absenden öffnet sich eine private WhatsApp-Unterhaltung mit den oben angegebenen Informationen.','direct':'Direkt sprechen?','directcopy':'Für dringende oder kurzfristige Anfragen ist WhatsApp in der Regel der schnellste Weg zu unserem Concierge-Team.','whatsapp':'WhatsApp Concierge','next':'Wie es weitergeht','nextsub':'Von der ersten Nachricht bis zum koordinierten Aufenthalt.','steps':[('Das Wesentliche senden','Daten, Gäste, Hauptservice und bereits bekannte Prioritäten.'),('Briefing klären','Wir bestätigen die Details, die für ein klares Verständnis der Anfrage notwendig sind.'),('Koordination','Nach Bestätigung des Umfangs werden die relevanten Services und die Logistik auf Ibiza abgestimmt.'),('Laufende Unterstützung','Wir bleiben verfügbar, wenn sich Zeitplan oder Anforderungen während des Aufenthalts ändern.')],
'options':['Full Concierge','Privater Chauffeur','Private Villa','Yacht / Charter','Private Aviation','Restaurants / Nightlife','Private Security','Private Chef / Villa Staff','Wellness','Private Event','Bespoke Request']},
'ar': {
'path':'/ar/contact/','dir':'rtl','title':'طلب كونسيرج خاص في إيبيزا | Ibiza VIP Move','desc':'أرسل تفاصيل إقامتك الخاصة إلى Ibiza VIP Move لتنسيق السائقين والفلل واليخوت والطيران الخاص والمطاعم والأمن وخدمات أسلوب الحياة في إيبيزا.','kicker':'Private Brief · Ibiza','h1':'أخبرنا كيف تريد أن تكون تجربتك في إيبيزا.','intro':'شارك معنا المعلومات الأساسية، وسنكمل المحادثة بشكل خاص وننسق الخطوات التالية حول إقامتك.','name':'الاسم','phone':'واتساب / الهاتف','arrival':'الوصول','departure':'المغادرة','service':'الخدمة الرئيسية','guests':'عدد الضيوف','brief':'التفاصيل / الطلب','button':'إرسال الطلب عبر واتساب','note':'عند الإرسال سيتم فتح محادثة واتساب خاصة تتضمن المعلومات أعلاه.','direct':'هل ترغب في التحدث مباشرة؟','directcopy':'للطلبات العاجلة أو في نفس اليوم، يكون واتساب عادةً أسرع وسيلة للتواصل مع فريق الكونسيرج.','whatsapp':'واتساب الكونسيرج','next':'ماذا يحدث بعد ذلك','nextsub':'من الرسالة الأولى إلى إقامة منسقة بالكامل.','steps':[('أرسل المعلومات الأساسية','التواريخ والضيوف والخدمة الرئيسية وأي أولويات معروفة.'),('نوضح الطلب','نؤكد التفاصيل اللازمة لفهم متطلباتك بشكل دقيق.'),('ننسق الخدمات','بعد تأكيد نطاق الطلب، نقوم بمواءمة الخدمات واللوجستيات المناسبة في إيبيزا.'),('نبقى متاحين','نواصل الدعم عندما يتغير الجدول أو تتطور احتياجات الإقامة.')],
'options':['كونسيرج كامل','سائق خاص','فيلا خاصة','يخت / تشارتر','طيران خاص','مطاعم / حياة ليلية','أمن خاص','شيف / طاقم فيلا','عافية وجمال','فعالية خاصة','طلب مخصص']}
}

SERVICES = ['/private-chauffeur-ibiza/','/luxury-villas-ibiza/','/yacht-charter-ibiza/','/restaurants-nightlife-ibiza/','/private-aviation-ibiza/','/private-security-ibiza/']
NAV_NAMES = ['Move','Stay','Sea','Access','Fly','Protect']

def alternate_links():
    links = ''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{path}">' for lang,path in ALTS.items())
    return links + f'<link rel="alternate" hreflang="x-default" href="{BASE}/contact/">'

def header(cta):
    nav=''.join(f'<a href="{path}">{name}</a>' for name,path in zip(NAV_NAMES,SERVICES))
    return f'''<header class="site-header"><a class="wordmark" href="/"><img src="/assets/brand-logo.svg" alt="Ibiza VIP Move" style="height:44px;width:auto"></a><nav>{nav}<a href="/ibiza-intelligence/">Black Book</a><a class="nav-cta" href="{WA}">{cta}</a></nav><button class="menu-btn" aria-label="Open menu">Menu</button></header><div class="mobile-menu">{nav}<a href="/ibiza-intelligence/">Black Book</a><a href="{WA}">{cta}</a></div>'''

def footer(cta):
    return f'''<footer><div class="footer-grid"><div><div class="footer-brand">IBIZA VIP MOVE</div><p>Private concierge · Ibiza</p></div><div><h4>Contact</h4><a href="tel:+34600703303">{PHONE}</a><a href="{WA}">{cta}</a></div><div><h4>Explore</h4><a href="/private-office/">Private Office</a><a href="/ibiza-intelligence/">The Ibiza Black Book</a><a href="/international-clients/">International Clients</a></div></div><div class="footer-bottom"><span>© 2026 Ibiza VIP Move</span><span>Discretion · Precision · Ibiza</span></div></footer><div class="mobile-bar"><a href="tel:+34600703303">Call</a><a href="{WA}">WhatsApp</a></div><script src="/assets/premium.js?v=24"></script>'''

def page(lang,d):
    canonical=BASE+d['path']
    opts=''.join(f'<option value="{o}">{o}</option>' for o in d['options'])
    steps=''.join(f'<article><span>0{i}</span><h3>{title}</h3><p>{copy}</p></article>' for i,(title,copy) in enumerate(d['steps'],1))
    schema={
        '@context':'https://schema.org','@type':'ContactPage','name':d['title'].split('|')[0].strip(),
        'url':canonical,'inLanguage':lang,'about':{'@id':BASE+'/#organization'}
    }
    body=f'''{header(d['whatsapp'])}<main><section class="contact-hero"><div><div class="kicker dark">{d['kicker']}</div><h1>{d['h1']}</h1><p>{d['intro']}</p><div class="premium-list"><li>{PHONE}</li><li>24/7 private client support · Ibiza</li></div></div><form id="conciergeForm"><label>{d['name']}<input id="fName" name="name" autocomplete="name" required></label><label>{d['phone']}<input id="fPhone" name="phone" autocomplete="tel" inputmode="tel" required></label><div class="form-row"><label>{d['arrival']}<input id="fArrival" name="arrival" type="date"></label><label>{d['departure']}<input id="fDeparture" name="departure" type="date"></label></div><div class="form-row"><label>{d['service']}<select id="fService" name="service"><option value="">—</option>{opts}</select></label><label>{d['guests']}<input id="fGuests" name="guests" type="number" min="1" inputmode="numeric"></label></div><label>{d['brief']}<textarea id="fBrief" name="brief" rows="5"></textarea></label><button class="btn dark" type="submit">{d['button']}</button><small>{d['note']}</small></form></section><section class="process"><div class="section-head"><div class="kicker dark">Private coordination</div><h2>{d['next']}</h2><p>{d['nextsub']}</p></div><div class="process-grid">{steps}</div></section><section class="closing-simple"><h2>{d['direct']}</h2><p>{d['directcopy']}</p><a class="btn dark" href="{WA}">{d['whatsapp']}</a></section></main>{footer(d['whatsapp'])}'''
    head=f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{d['title']}</title><meta name="description" content="{d['desc']}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">{alternate_links()}<meta property="og:type" content="website"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:title" content="{d['title']}"><meta property="og:description" content="{d['desc']}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/images/hero-desktop.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/premium.css"><link rel="stylesheet" href="/assets/luxury-overrides.css"><link rel="stylesheet" href="/assets/editorial-black.css"><link rel="stylesheet" href="/assets/editorial-inner.css"><link rel="stylesheet" href="/assets/editorial-multilingual.css"><link rel="stylesheet" href="/assets/premium-motion.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>'''
    direction=f' dir="{d["dir"]}"' if d['dir']=='rtl' else ''
    return f'<!doctype html><html lang="{lang}"{direction}>{head}<body class="ivm-editorial-inner ivm-localized-contact">{body}</body></html>'

for lang,d in DATA.items():
    target=ROOT/d['path'].lstrip('/')/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page(lang,d),encoding='utf-8')

# Reciprocal hreflang on the existing English contact page.
en_contact=ROOT/'contact'/'index.html'
text=en_contact.read_text(encoding='utf-8')
text=re.sub(r'<link rel="alternate" hreflang="(?:en|es|fr|de|ar|x-default)"[^>]*>','',text,flags=re.I)
text=re.sub(r'</head>',alternate_links()+'</head>',text,count=1,flags=re.I)
en_contact.write_text(text,encoding='utf-8')

# Route language-page Contact links to their localized private brief.
for lang,d in DATA.items():
    lang_root=ROOT/lang
    if not lang_root.exists():
        continue
    for p in lang_root.rglob('*.html'):
        txt=p.read_text(encoding='utf-8')
        txt=txt.replace('href="/contact/"',f'href="{d["path"]}"')
        p.write_text(txt,encoding='utf-8')

# Add new URLs to sitemap after Phase 15 has already added lastmod to prior URLs.
sitemap=ROOT/'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
tree=ET.parse(sitemap); root=tree.getroot(); ns='http://www.sitemaps.org/schemas/sitemap/0.9'
existing={u.find(f'{{{ns}}}loc').text for u in root.findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for d in DATA.values():
    loc=BASE+d['path']
    if loc not in existing:
        u=ET.SubElement(root,f'{{{ns}}}url')
        ET.SubElement(u,f'{{{ns}}}loc').text=loc
        ET.SubElement(u,f'{{{ns}}}lastmod').text=TODAY
tree.write(sitemap,encoding='utf-8',xml_declaration=True)

# Keep llms.txt supplemental summary current.
llms=ROOT/'llms.txt'
lt=llms.read_text(encoding='utf-8')
marker='## Localized private brief pages\n'
if marker not in lt:
    lt += '\n'+marker
    lt += f'- [Español]({BASE}/es/contacto/)\n- [Français]({BASE}/fr/contact/)\n- [Deutsch]({BASE}/de/kontakt/)\n- [العربية]({BASE}/ar/contact/)\n'
llms.write_text(lt,encoding='utf-8')

# Release validation.
for lang,d in DATA.items():
    target=ROOT/d['path'].lstrip('/')/'index.html'
    txt=target.read_text(encoding='utf-8')
    assert txt.count('<h1')==1, f'{lang}: expected one H1'
    assert f'<link rel="canonical" href="{BASE}{d["path"]}">' in txt, f'{lang}: canonical missing'
    assert '<form id="conciergeForm">' in txt, f'{lang}: form missing'
    assert 'hreflang="en"' in txt and 'hreflang="x-default"' in txt, f'{lang}: hreflang missing'
assert 'hreflang="es"' in en_contact.read_text(encoding='utf-8'), 'English contact missing reciprocal ES hreflang'
urls={u.find(f'{{{ns}}}loc').text for u in ET.parse(sitemap).getroot().findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for d in DATA.values(): assert BASE+d['path'] in urls, d['path']+' missing from sitemap'
print('PASS: Phase 24 localized private brief pages + reciprocal hreflang + sitemap')
