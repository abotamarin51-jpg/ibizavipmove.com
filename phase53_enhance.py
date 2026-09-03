from pathlib import Path
from urllib.parse import quote

ROOT = Path('_site')
WA = 'https://wa.me/34600703303'
STYLE = '/assets/phase53.css?v=53'

PAGES = {
    'en': '/partners/',
    'es': '/es/partners/',
    'fr': '/fr/partners/',
    'de': '/de/partners/',
    'ar': '/ar/partners/',
}

COPY = {
'en': {
 'eyebrow':'Partner brief','title':'Start with the right context.','intro':'Choose the route closest to your request. WhatsApp opens with the context already included so the conversation can begin with the relevant details.',
 'routes':[
  ('Live client','Client request','A current Ibiza itinerary requiring local execution.','Hello Ibiza VIP Move, I have a live client request for Ibiza and would like to discuss local execution. I can share dates, guest profile and required services.'),
  ('Partnership','Introduce your company','A professional introduction for future Ibiza requests.','Hello Ibiza VIP Move, I am contacting you regarding a potential B2B partnership for Ibiza. I would like to introduce our company and discuss how we could work together.'),
  ('Private office','PA / Family Office','A principal or family stay requiring one local contact.','Hello Ibiza VIP Move, I am contacting you on behalf of a principal / family office regarding private coordination in Ibiza. I would like to share the stay brief privately.'),
  ('Hospitality','Guest coordination','Private guest logistics or multi-service support.','Hello Ibiza VIP Move, I am contacting you regarding private guest coordination in Ibiza. I would like to discuss the guest requirements and operational scope.')],
},
'es': {
 'eyebrow':'Brief de partner','title':'Empieza con el contexto correcto.','intro':'Elige la vía más cercana a tu solicitud. WhatsApp se abrirá con el contexto incluido para comenzar directamente con los datos relevantes.',
 'routes':[
  ('Cliente activo','Solicitud de cliente','Un itinerario actual en Ibiza que necesita ejecución local.','Hola Ibiza VIP Move, tengo una solicitud activa de un cliente para Ibiza y me gustaría hablar sobre la ejecución local. Puedo compartir fechas, perfil de huéspedes y servicios necesarios.'),
  ('Partnership','Presenta tu empresa','Una introducción profesional para futuras solicitudes en Ibiza.','Hola Ibiza VIP Move, contacto por una posible colaboración B2B para Ibiza. Me gustaría presentar nuestra empresa y hablar sobre cómo podríamos trabajar juntos.'),
  ('Private Office','PA / Family Office','Una estancia de principal o familia que necesita un contacto local.','Hola Ibiza VIP Move, contacto en representación de un principal / family office para coordinar una estancia privada en Ibiza. Me gustaría compartir el brief de forma privada.'),
  ('Hospitality','Coordinación de huéspedes','Logística privada o soporte multi-servicio para huéspedes.','Hola Ibiza VIP Move, contacto por una coordinación privada de huéspedes en Ibiza. Me gustaría comentar los requisitos y el alcance operativo.')],
},
'fr': {
 'eyebrow':'Brief partenaire','title':'Commencez avec le bon contexte.','intro':'Choisissez la voie la plus proche de votre demande. WhatsApp s’ouvrira avec le contexte déjà inclus afin de commencer directement avec les informations utiles.',
 'routes':[
  ('Client actif','Demande client','Un itinéraire Ibiza actuel nécessitant une exécution locale.','Bonjour Ibiza VIP Move, j’ai une demande client active pour Ibiza et je souhaite discuter de l’exécution locale. Je peux partager les dates, le profil des invités et les services requis.'),
  ('Partenariat','Présenter votre société','Une introduction professionnelle pour de futures demandes Ibiza.','Bonjour Ibiza VIP Move, je vous contacte au sujet d’un éventuel partenariat B2B pour Ibiza. Je souhaite présenter notre société et discuter de la manière dont nous pourrions travailler ensemble.'),
  ('Private Office','PA / Family Office','Un séjour principal ou famille nécessitant un contact local unique.','Bonjour Ibiza VIP Move, je vous contacte pour le compte d’un principal / family office concernant une coordination privée à Ibiza. Je souhaite partager le brief du séjour en privé.'),
  ('Hospitality','Coordination invités','Logistique privée ou support multi-services pour des invités.','Bonjour Ibiza VIP Move, je vous contacte au sujet d’une coordination privée d’invités à Ibiza. Je souhaite discuter des besoins et du périmètre opérationnel.')],
},
'de': {
 'eyebrow':'Partner Brief','title':'Mit dem richtigen Kontext starten.','intro':'Wählen Sie die Route, die Ihrer Anfrage am nächsten kommt. WhatsApp öffnet sich bereits mit dem passenden Kontext, damit direkt mit den relevanten Angaben begonnen werden kann.',
 'routes':[
  ('Live Client','Kundenanfrage','Eine aktuelle Ibiza-Reise mit Bedarf an lokaler Ausführung.','Hallo Ibiza VIP Move, ich habe eine aktive Kundenanfrage für Ibiza und möchte die lokale Ausführung besprechen. Ich kann Daten, Gästeprofil und benötigte Services teilen.'),
  ('Partnership','Unternehmen vorstellen','Eine professionelle Vorstellung für zukünftige Ibiza-Anfragen.','Hallo Ibiza VIP Move, ich kontaktiere Sie wegen einer möglichen B2B-Partnerschaft für Ibiza. Ich möchte unser Unternehmen vorstellen und besprechen, wie wir zusammenarbeiten könnten.'),
  ('Private Office','PA / Family Office','Ein Principal- oder Familienaufenthalt mit einem lokalen Ansprechpartner.','Hallo Ibiza VIP Move, ich kontaktiere Sie im Namen eines Principals / Family Office wegen privater Koordination auf Ibiza. Ich möchte das Aufenthaltsbriefing vertraulich teilen.'),
  ('Hospitality','Gästekoordination','Private Gästelogistik oder Multi-Service-Support.','Hallo Ibiza VIP Move, ich kontaktiere Sie wegen privater Gästekoordination auf Ibiza. Ich möchte Anforderungen und operativen Umfang besprechen.')],
},
'ar': {
 'eyebrow':'طلب الشريك','title':'ابدأ بالسياق الصحيح.','intro':'اختر المسار الأقرب إلى طلبك. سيفتح واتساب والسياق مضاف مسبقاً حتى تبدأ المحادثة مباشرة بالمعلومات المناسبة.',
 'routes':[
  ('طلب حالي','طلب عميل','برنامج حالي في إيبيزا يحتاج إلى تنفيذ محلي.','مرحباً Ibiza VIP Move، لدي طلب حالي لعميل في إيبيزا وأرغب في مناقشة التنفيذ المحلي. يمكنني مشاركة التواريخ وملف الضيوف والخدمات المطلوبة.'),
  ('شراكة','تقديم الشركة','تعريف مهني لطلبات إيبيزا المستقبلية.','مرحباً Ibiza VIP Move، أتواصل بخصوص شراكة B2B محتملة في إيبيزا. أرغب في تقديم شركتنا ومناقشة كيفية العمل معاً.'),
  ('Private Office','PA / Family Office','إقامة لضيف رئيسي أو عائلة تحتاج إلى جهة اتصال محلية واحدة.','مرحباً Ibiza VIP Move، أتواصل نيابةً عن Principal / Family Office بخصوص تنسيق خاص في إيبيزا. أرغب في مشاركة تفاصيل الإقامة بشكل خاص.'),
  ('Hospitality','تنسيق الضيوف','لوجستيات خاصة أو دعم متعدد الخدمات للضيوف.','مرحباً Ibiza VIP Move، أتواصل بخصوص تنسيق خاص للضيوف في إيبيزا. أرغب في مناقشة المتطلبات والنطاق التشغيلي.')],
}

asset = ROOT / 'assets' / 'phase53.css'
asset.write_text(Path('phase53.css').read_text(encoding='utf-8'), encoding='utf-8')


def route_card(route):
    label, title, copy, message = route
    href = WA + '?text=' + quote(message)
    return f'<a class="ivm-partner-route" href="{href}"><span>{label}</span><strong>{title}</strong><small>{copy}</small></a>'


def section(lang):
    c = COPY[lang]
    cards = ''.join(route_card(r) for r in c['routes'])
    return f'''<section class="ivm-partner-routes" aria-label="Partner brief routes"><div class="ivm-partner-routes-inner"><div class="ivm-partner-routes-head"><div><div class="eyebrow">{c['eyebrow']}</div><h2>{c['title']}</h2></div><p>{c['intro']}</p></div><div class="ivm-partner-route-grid">{cards}</div></div></section>'''

updated = 0
for lang, path in PAGES.items():
    file = ROOT / path.strip('/') / 'index.html'
    if not file.exists():
        raise SystemExit(f'Phase 53 target missing: {path}')
    html = file.read_text(encoding='utf-8')
    if STYLE not in html:
        html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
    if 'class="ivm-partner-routes"' not in html:
        marker = '<section class="ivm-b2b-cta">'
        if marker not in html:
            raise SystemExit(f'Phase 53 CTA marker missing: {path}')
        html = html.replace(marker, section(lang) + marker, 1)
    file.write_text(html, encoding='utf-8')
    updated += 1

for lang, path in PAGES.items():
    html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
    assert html.count('class="ivm-partner-routes"') == 1, path
    assert html.count('class="ivm-partner-route"') == 4, path
    assert STYLE in html, path
    assert html.count('https://wa.me/34600703303?text=') >= 4, path
    assert html.count('<h1') == 1, path

assert asset.exists() and asset.stat().st_size > 1000
print(f'PASS: Phase 53 contextual partner routing active on {updated} EN/ES/FR/DE/AR partner pages')
