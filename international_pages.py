from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'
LOGO = '/assets/brand-logo.svg?v=8'
CSS = '/assets/premium.css?v=8'
JS = '/assets/premium.js?v=8'
HERO = '/assets/images/villa.jpg'

LANGS = {
    'en': ('English', '/'),
    'fr': ('Français', '/fr/'),
    'de': ('Deutsch', '/de/'),
    'ar': ('العربية', '/ar/'),
}

TRANSLATIONS = {
    'fr': {
        'lang':'fr','dir':'ltr',
        'title':'Conciergerie de luxe à Ibiza | Ibiza VIP Move',
        'desc':'Conciergerie privée de luxe à Ibiza : chauffeur, villas, yachts, aviation privée, réservations VIP, sécurité et services sur mesure.',
        'kicker':'Conciergerie privée · Ibiza',
        'h1':'Ibiza, orchestrée autour de vous.',
        'lead':'Ibiza VIP Move coordonne votre séjour privé à Ibiza avec discrétion, réactivité et un seul point de contact.',
        'intro_title':'Un contact. Tous les détails alignés.',
        'intro':'Chauffeur privé, villas, yachts, aviation privée, restaurants, beach clubs, nightlife, sécurité, chefs privés, wellness et demandes sur mesure — coordonnés autour de votre planning et de vos préférences.',
        'services':'Services privés',
        's1':'Chauffeur privé','s2':'Villas de luxe','s3':'Yachts & charters','s4':'Aviation privée','s5':'Réservations VIP','s6':'Sécurité & protection',
        'process':'Notre approche',
        'p1':'Partagez vos dates, vos invités et vos priorités.','p2':'Nous clarifions le brief et alignons les services appropriés.','p3':'Nous coordonnons les détails locaux autour de votre itinéraire.','p4':'Nous restons disponibles lorsque vos plans évoluent.',
        'cta':'Demander une conciergerie privée','contact':'Contacter la conciergerie',
    },
    'de': {
        'lang':'de','dir':'ltr',
        'title':'Luxus Concierge Ibiza | Ibiza VIP Move',
        'desc':'Privater Luxus-Concierge auf Ibiza für Chauffeur, Villen, Yachten, Privatflüge, VIP-Reservierungen, Sicherheit und maßgeschneiderte Services.',
        'kicker':'Privater Concierge · Ibiza',
        'h1':'Ibiza, diskret für Sie organisiert.',
        'lead':'Ibiza VIP Move koordiniert private Aufenthalte auf Ibiza mit Diskretion, schneller Kommunikation und einem zentralen Ansprechpartner.',
        'intro_title':'Ein Kontakt. Alle Details abgestimmt.',
        'intro':'Privater Chauffeur, Luxusvillen, Yachten, private Aviation, Restaurants, Beach Clubs, Nightlife, Sicherheit, private Köche, Wellness und individuelle Wünsche — abgestimmt auf Ihren Zeitplan und Ihre Prioritäten.',
        'services':'Private Services',
        's1':'Privater Chauffeur','s2':'Luxusvillen','s3':'Yachten & Charter','s4':'Private Aviation','s5':'VIP-Reservierungen','s6':'Security & Close Protection',
        'process':'So arbeiten wir',
        'p1':'Teilen Sie Reisedaten, Gäste und Prioritäten mit uns.','p2':'Wir präzisieren den Brief und stimmen passende Services ab.','p3':'Wir koordinieren die lokalen Details rund um Ihre Reiseroute.','p4':'Wir bleiben erreichbar, wenn sich Pläne ändern.',
        'cta':'Privaten Concierge anfragen','contact':'Concierge kontaktieren',
    },
    'ar': {
        'lang':'ar','dir':'rtl',
        'title':'كونسيرج فاخر في إيبيزا | Ibiza VIP Move',
        'desc':'خدمة كونسيرج خاصة وفاخرة في إيبيزا تشمل السائق الخاص والفلل واليخوت والطيران الخاص والحجوزات الراقية والأمن والخدمات المصممة حسب الطلب.',
        'kicker':'كونسيرج خاص · إيبيزا',
        'h1':'إيبيزا، بتنسيق خاص يليق بك.',
        'lead':'تنسق Ibiza VIP Move إقامتك الخاصة في إيبيزا بسرية وسرعة ومن خلال نقطة اتصال واحدة.',
        'intro_title':'جهة اتصال واحدة. كل التفاصيل منسقة.',
        'intro':'سائق خاص، فلل فاخرة، يخوت، طيران خاص، مطاعم ونوادٍ شاطئية، حياة ليلية، أمن خاص، طهاة، عافية وطلبات مخصصة — كلها منسقة وفق جدولك وتفضيلاتك.',
        'services':'الخدمات الخاصة',
        's1':'سائق خاص','s2':'فلل فاخرة','s3':'يخوت وتأجير خاص','s4':'طيران خاص','s5':'حجوزات VIP','s6':'أمن وحماية خاصة',
        'process':'طريقة العمل',
        'p1':'أرسل التواريخ وعدد الضيوف والأولويات.','p2':'نوضح التفاصيل ونحدد الخدمات الأنسب للطلب.','p3':'ننسق التفاصيل المحلية وفق برنامج الإقامة.','p4':'نبقى متاحين عندما تتغير الخطط أو تظهر احتياجات جديدة.',
        'cta':'طلب كونسيرج خاص','contact':'تواصل مع الكونسيرج',
    },
}


def hreflang_tags():
    tags = [f'<link rel="alternate" hreflang="{code}" href="{BASE}{path}">' for code,(_,path) in LANGS.items()]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    return ''.join(tags)


def lang_links():
    return ' · '.join(f'<a href="{path}">{label}</a>' for _,(label,path) in LANGS.items())


def header():
    return f'''<header class="site-header"><a class="wordmark" href="/" aria-label="Ibiza VIP Move home"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a><nav><a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Partners</a><a href="/contact/">Contact</a><a class="nav-cta" href="{WA}">Request Concierge</a></nav><button class="menu-btn" aria-label="Open menu" aria-controls="mobileMenu">Menu</button></header><div class="mobile-menu" id="mobileMenu"><a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Partners</a><a href="/contact/">Contact</a><a href="{WA}">WhatsApp Concierge</a></div>'''


def footer():
    return f'''<footer><div class="footer-grid"><div><div class="footer-brand"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div><p>Private concierge, chauffeur and lifestyle management in Ibiza.</p></div><div><h4>Contact</h4><a href="tel:+34600703303">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}">WhatsApp Concierge</a></div><div><h4>International</h4><a href="/international-clients/">International Clients & Partners</a><div style="margin-top:10px">{lang_links()}</div></div></div><div class="footer-bottom"><span>© 2026 Ibiza VIP Move</span><span>Discretion · Precision · Ibiza</span></div></footer><div class="mobile-bar"><a href="tel:+34600703303">Call</a><a href="{WA}">WhatsApp</a></div><script src="{JS}"></script>'''


def head(title, desc, url, lang='en', alternates=False):
    schema={
        '@context':'https://schema.org','@type':'WebPage','name':title,'url':url,'description':desc,
        'inLanguage':lang,'isPartOf':{'@type':'WebSite','name':'Ibiza VIP Move','url':BASE+'/'},
        'about':{'@type':'ProfessionalService','name':'Ibiza VIP Move','url':BASE+'/'},
    }
    alt = hreflang_tags() if alternates else ''
    return f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">{alt}<meta property="og:type" content="website"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/images/villa.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="{CSS}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>'''


def translated_page(code, t):
    url=f'{BASE}/{code}/'
    direction=t['dir']
    body=f'''<section class="page-hero" style="--hero:url('{HERO}')"><div><div class="kicker light">{t['kicker']}</div><h1>{t['h1']}</h1><p>{t['lead']}</p><a class="btn gold" href="{WA}">{t['cta']}</a></div></section><section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>{t['intro_title']}</h2></div><div><p class="large">{t['intro']}</p><a class="text-link" href="/international-clients/">International private client support →</a></div></section><section class="dark-panel"><div class="kicker light">{t['services']}</div><h2>{t['services']}</h2><div class="trust-grid"><div><b>{t['s1']}</b></div><div><b>{t['s2']}</b></div><div><b>{t['s3']}</b></div><div><b>{t['s4']}</b></div><div><b>{t['s5']}</b></div><div><b>{t['s6']}</b></div></div></section><section class="process"><div class="section-head"><div class="kicker dark">{t['process']}</div><h2>{t['process']}</h2></div><div class="process-grid"><article><span>01</span><p>{t['p1']}</p></article><article><span>02</span><p>{t['p2']}</p></article><article><span>03</span><p>{t['p3']}</p></article><article><span>04</span><p>{t['p4']}</p></article></div></section><section class="closing-simple"><h2>{t['cta']}</h2><a class="btn dark" href="{WA}">{t['contact']}</a></section>'''
    return f'<!doctype html><html lang="{t["lang"]}" dir="{direction}">'+head(t['title'],t['desc'],url,t['lang'],True)+f'<body>{header()}<main>{body}</main>{footer()}</body></html>'


def international_page():
    title='International Ibiza Concierge for Private Clients & Travel Partners | Ibiza VIP Move'
    desc='Ibiza concierge support for international private clients, PAs, family offices, luxury travel advisors and concierge partners coordinating stays from abroad.'
    url=BASE+'/international-clients/'
    body=f'''<section class="page-hero" style="--hero:url('/assets/images/aviation.jpg')"><div><div class="kicker light">International Private Clients & Partners</div><h1>Ibiza execution,<br><em>coordinated from anywhere.</em></h1><p>One Ibiza-based point of contact for private clients, PAs, family offices, travel advisors and concierge partners arranging complex stays from abroad.</p><a class="btn gold" href="{WA}">Request Ibiza Support</a></div></section><section class="editorial"><div><div class="kicker dark">International coordination</div><h2>Your local operator<br>before you land.</h2></div><div><p class="large">Whether the brief originates in London, New York, Dubai, Riyadh, Geneva, Paris, Frankfurt, Doha or elsewhere, the operational requirement is the same: clear communication and reliable execution on the island.</p><p>Ibiza VIP Move coordinates chauffeur transportation, villas, yachts, private aviation, reservations, security, staffing, wellness and bespoke requests around one itinerary.</p></div></section><section class="process"><div class="section-head"><div class="kicker dark">Built for cross-border briefs</div><h2>Simple handover. Local execution.</h2></div><div class="process-grid"><article><span>01</span><h3>International brief</h3><p>Share dates, principal or guest requirements, priorities and preferred communication structure.</p></article><article><span>02</span><h3>One Ibiza contact</h3><p>Keep transport, hospitality and lifestyle requests aligned through one local coordination point.</p></article><article><span>03</span><h3>Pre-arrival alignment</h3><p>Coordinate essential services before the client reaches the island.</p></article><article><span>04</span><h3>On-island support</h3><p>Maintain responsive communication as timings, requests and itineraries evolve.</p></article></div></section><section class="dark-panel"><div class="kicker light">Relevant for</div><h2>Private and professional briefs.</h2><div class="trust-grid"><div><b>Private Clients & Families</b><p>One point of contact across the stay.</p></div><div><b>Personal Assistants</b><p>Local execution around principal priorities.</p></div><div><b>Family Offices</b><p>Discreet coordination across multiple services.</p></div><div><b>Luxury Travel Advisors</b><p>Reliable Ibiza support for client itineraries.</p></div><div><b>Concierge Companies</b><p>Local execution and partner communication.</p></div><div><b>Private Aviation Partners</b><p>Ground coordination around arrivals and departures.</p></div></div></section><section class="closing-simple"><h2>Coordinate your Ibiza brief.</h2><p>Send the dates, guest profile and required services. We will take the conversation from there.</p><div class="hero-actions" style="justify-content:center"><a class="btn dark" href="{WA}">WhatsApp Concierge</a><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a></div></section>'''
    return '<!doctype html><html lang="en">'+head(title,desc,url,'en',False)+f'<body>{header()}<main>{body}</main>{footer()}</body></html>'


# Create international pages.
for code,t in TRANSLATIONS.items():
    d=ROOT/code; d.mkdir(parents=True,exist_ok=True)
    (d/'index.html').write_text(translated_page(code,t),encoding='utf-8')

d=ROOT/'international-clients'; d.mkdir(parents=True,exist_ok=True)
(d/'index.html').write_text(international_page(),encoding='utf-8')

# Add hreflang and language discovery to the English homepage without changing its main layout.
home=ROOT/'index.html'
text=home.read_text(encoding='utf-8')
if 'hreflang="fr"' not in text:
    text=text.replace('</head>',hreflang_tags()+'</head>')
if '/international-clients/' not in text:
    marker='</footer>'
    text=text.replace(marker,f'<div style="text-align:center;padding:0 20px 28px;font-size:12px;opacity:.72"><a href="/international-clients/">International Clients</a> · {lang_links()}</div>{marker}',1)
home.write_text(text,encoding='utf-8')

# Add new URLs to sitemap once.
sitemap=ROOT/'sitemap.xml'
sm=sitemap.read_text(encoding='utf-8')
entries=['/fr/','/de/','/ar/','/international-clients/']
for path in entries:
    loc=f'{BASE}{path}'
    if loc not in sm:
        sm=sm.replace('</urlset>',f'<url><loc>{loc}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url></urlset>')
sitemap.write_text(sm,encoding='utf-8')

print('PASS: international hub, FR/DE/AR pages, hreflang and sitemap entries created')
