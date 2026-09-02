from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'
CSS = '/assets/premium.css?v=8'
JS = '/assets/premium.js?v=8'
LOGO = '/assets/brand-logo.svg?v=8'

GROUPS = {
    'concierge': {
        'en': '/private-concierge-ibiza/',
        'es': '/es/concierge-privado-ibiza/',
        'fr': '/fr/conciergerie-privee-ibiza/',
        'de': '/de/privater-concierge-ibiza/',
        'ar': '/ar/private-concierge-ibiza/',
        'image': '/assets/images/villa.jpg',
    },
    'chauffeur': {
        'en': '/private-chauffeur-ibiza/',
        'es': '/es/chauffeur-privado-ibiza/',
        'fr': '/fr/chauffeur-prive-ibiza/',
        'de': '/de/privater-chauffeur-ibiza/',
        'ar': '/ar/private-chauffeur-ibiza/',
        'image': '/assets/images/chauffeur.jpg',
    },
}

COPY = {
    ('fr','concierge'): {
        'title':'Conciergerie privée Ibiza | Luxury Concierge | Ibiza VIP Move',
        'desc':'Conciergerie privée à Ibiza pour chauffeur, villas, yachts, aviation privée, restaurants, sécurité, wellness et demandes sur mesure via un seul contact.',
        'h1':'Conciergerie privée à Ibiza, gérée comme un seul service.',
        'lead':'Un point de contact unique pour coordonner votre séjour privé à Ibiza, de l’arrivée au départ.',
        'eyebrow':'Conciergerie privée · Ibiza','section':'Du brief à l’exécution.','cta':'Demander une assistance privée',
        'items':[('01','Brief','Dates, invités, priorités, confidentialité et services requis.'),('02','Aligner','Chauffeur, séjour, réservations et partenaires organisés autour du même itinéraire.'),('03','Coordonner','Les détails confirmés restent centralisés dans une seule ligne de communication.'),('04','Adapter','Si le planning change, les éléments concernés sont réévalués avec lui.')],
    },
    ('fr','chauffeur'): {
        'title':'Chauffeur privé Ibiza | Service de luxe | Ibiza VIP Move',
        'desc':'Chauffeur privé à Ibiza pour aéroport, villas, hôtels, marinas, restaurants, nightlife, mise à disposition et coordination multi-véhicules.',
        'h1':'Chauffeur privé à Ibiza, autour de votre agenda.',
        'lead':'Mobilité privée pour arrivées, villas, hôtels, marinas, restaurants, nightlife et journées complètes à Ibiza.',
        'eyebrow':'Chauffeur privé · Ibiza','section':'Une mobilité privée, clairement coordonnée.','cta':'Demander un chauffeur privé',
        'items':[('01','Aéroport','Arrivées et départs coordonnés avec vol, bagages et destination.'),('02','À l’heure','Mise à disposition autour d’un planning confirmé et de plusieurs étapes.'),('03','Journée complète','Chauffeur privé pour journées complètes et changements de lieux.'),('04','Multi-véhicules','Coordination de groupes, bagages et plusieurs véhicules si nécessaire.')],
    },
    ('de','concierge'): {
        'title':'Privater Concierge Ibiza | Luxury Concierge | Ibiza VIP Move',
        'desc':'Privater Concierge auf Ibiza für Chauffeur, Villen, Yachten, private Aviation, Restaurants, Security, Wellness und individuelle Wünsche über einen Ansprechpartner.',
        'h1':'Privater Concierge auf Ibiza, zentral koordiniert.',
        'lead':'Ein Ansprechpartner für einen privaten Ibiza-Aufenthalt – von der Ankunft bis zur Abreise.',
        'eyebrow':'Privater Concierge · Ibiza','section':'Vom Briefing zur Umsetzung.','cta':'Private Unterstützung anfragen',
        'items':[('01','Briefing','Reisedaten, Gäste, Prioritäten, Privatsphäre und benötigte Services.'),('02','Abstimmen','Mobilität, Aufenthalt, Reservierungen und Partner rund um eine Route ausrichten.'),('03','Koordinieren','Bestätigte Details bleiben über einen zentralen Kontakt gebündelt.'),('04','Anpassen','Wenn sich Zeiten ändern, werden die betroffenen Elemente entsprechend neu abgestimmt.')],
    },
    ('de','chauffeur'): {
        'title':'Privater Chauffeur Ibiza | Luxus Fahrservice | Ibiza VIP Move',
        'desc':'Privater Chauffeur auf Ibiza für Flughafen, Villen, Hotels, Marinas, Restaurants, Nightlife, stundenweise Verfügbarkeit und mehrere Fahrzeuge.',
        'h1':'Privater Chauffeur auf Ibiza, passend zu Ihrem Zeitplan.',
        'lead':'Private Mobilität für Ankünfte, Villen, Hotels, Marinas, Restaurants, Nightlife und ganze Tage auf Ibiza.',
        'eyebrow':'Privater Chauffeur · Ibiza','section':'Private Mobilität, klar koordiniert.','cta':'Privaten Chauffeur anfragen',
        'items':[('01','Flughafen','Ankunft und Abflug mit Flug, Gepäck und Ziel abgestimmt.'),('02','Stundenweise','Verfügbarkeit für mehrere Stopps innerhalb eines bestätigten Zeitplans.'),('03','Ganztägig','Privater Chauffeur für ganze Tage und mehrere Ortswechsel.'),('04','Mehrere Fahrzeuge','Koordination von Gruppen, Gepäck und mehreren Fahrzeugen bei Bedarf.')],
    },
    ('ar','concierge'): {
        'title':'كونسيرج خاص في إيبيزا | Ibiza VIP Move',
        'desc':'كونسيرج خاص في إيبيزا لتنسيق السائق والفلل واليخوت والطيران الخاص والمطاعم والأمن والعافية والطلبات المخصصة عبر نقطة اتصال واحدة.',
        'h1':'كونسيرج خاص في إيبيزا، بتنسيق مركزي.',
        'lead':'نقطة اتصال واحدة لتنسيق الإقامة الخاصة في إيبيزا من الوصول حتى المغادرة.',
        'eyebrow':'كونسيرج خاص · إيبيزا','section':'من الطلب إلى التنفيذ.','cta':'طلب مساعدة خاصة',
        'items':[('01','الطلب','التواريخ والضيوف والأولويات والخصوصية والخدمات المطلوبة.'),('02','التنسيق','ربط التنقل والإقامة والحجوزات والشركاء ضمن برنامج واحد.'),('03','الإدارة','الحفاظ على التفاصيل المؤكدة عبر جهة اتصال واحدة.'),('04','التكيف','عند تغيّر التوقيت تتم مراجعة العناصر المرتبطة به.')],
    },
    ('ar','chauffeur'): {
        'title':'سائق خاص في إيبيزا | خدمة فاخرة | Ibiza VIP Move',
        'desc':'سائق خاص في إيبيزا للمطار والفلل والفنادق والمراسي والمطاعم والحياة الليلية والحجز بالساعة وتنسيق عدة سيارات.',
        'h1':'سائق خاص في إيبيزا، وفق جدولك.',
        'lead':'تنقل خاص للوصول والمغادرة والفلل والفنادق والمراسي والمطاعم والحياة الليلية والأيام الكاملة في إيبيزا.',
        'eyebrow':'سائق خاص · إيبيزا','section':'تنقل خاص بتنسيق واضح.','cta':'طلب سائق خاص',
        'items':[('01','المطار','تنسيق الوصول والمغادرة مع الرحلة والأمتعة والوجهة.'),('02','بالساعة','توفر لعدة محطات ضمن جدول مؤكد.'),('03','يوم كامل','سائق خاص ليوم كامل والتنقل بين عدة مواقع.'),('04','عدة سيارات','تنسيق المجموعات والأمتعة وعدة مركبات عند الحاجة.')],
    },
}

LANG_LABELS = {'en':'English','es':'Español','fr':'Français','de':'Deutsch','ar':'العربية'}

def hreflangs(group):
    tags=[]
    for code,path in GROUPS[group].items():
        if code == 'image':
            continue
        tags.append(f'<link rel="alternate" hreflang="{code}" href="{BASE}{path}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}{GROUPS[group]["en"]}">')
    return ''.join(tags)

def footer(lang):
    links=' · '.join(f'<a href="{GROUPS["concierge"].get(code,"/") if code!="en" else "/"}">{label}</a>' for code,label in LANG_LABELS.items())
    contact_title={'fr':'Contact','de':'Kontakt','ar':'التواصل'}[lang]
    return f'''<footer><div class="footer-grid"><div><div class="footer-brand"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div><p>Private concierge, chauffeur and lifestyle management in Ibiza.</p></div><div><h4>{contact_title}</h4><a href="tel:+34600703303">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}">WhatsApp Concierge</a></div><div><h4>Languages</h4><div>{links}</div></div></div><div class="footer-bottom"><span>© 2026 Ibiza VIP Move</span><span>Discretion · Precision · Ibiza</span></div></footer><div class="mobile-bar"><a href="tel:+34600703303">Call</a><a href="{WA}">WhatsApp</a></div><script src="{JS}"></script>'''

def header(lang, group):
    labels={
        'fr':('Conciergerie','Chauffeur','Contact','Demander'),
        'de':('Concierge','Chauffeur','Kontakt','Anfragen'),
        'ar':('الكونسيرج','السائق','تواصل','طلب الخدمة'),
    }[lang]
    return f'''<header class="site-header"><a class="wordmark" href="/{lang}/" aria-label="Ibiza VIP Move"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a><nav><a href="{GROUPS['concierge'][lang]}">{labels[0]}</a><a href="{GROUPS['chauffeur'][lang]}">{labels[1]}</a><a href="/private-office/">Private Office</a><a href="/contact/">{labels[2]}</a><a class="nav-cta" href="{WA}">{labels[3]}</a></nav><button class="menu-btn" aria-label="Menu" aria-controls="mobileMenu">Menu</button></header><div class="mobile-menu" id="mobileMenu"><a href="{GROUPS['concierge'][lang]}">{labels[0]}</a><a href="{GROUPS['chauffeur'][lang]}">{labels[1]}</a><a href="/private-office/">Private Office</a><a href="/contact/">{labels[2]}</a><a href="{WA}">WhatsApp</a></div>'''

def head(lang, group, data):
    path=GROUPS[group][lang]
    image=GROUPS[group]['image']
    locale={'fr':'fr_FR','de':'de_DE','ar':'ar_AR'}[lang]
    direction='rtl' if lang=='ar' else 'ltr'
    schema={'@context':'https://schema.org','@type':'WebPage','name':data['title'],'url':BASE+path,'description':data['desc'],'inLanguage':lang,'isPartOf':{'@type':'WebSite','name':'Ibiza VIP Move','url':BASE+'/'},'about':{'@type':'Organization','name':'Ibiza VIP Move','url':BASE+'/'},'primaryImageOfPage':{'@type':'ImageObject','contentUrl':BASE+image}}
    return direction, f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(data['title'])}</title><meta name="description" content="{escape(data['desc'])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}{path}">{hreflangs(group)}<meta property="og:type" content="website"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:locale" content="{locale}"><meta property="og:title" content="{escape(data['title'])}"><meta property="og:description" content="{escape(data['desc'])}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}{image}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" sizes="180x180" href="/favicon.png"><link rel="apple-touch-icon" href="/favicon.png"><meta name="theme-color" content="#090e13"><link rel="stylesheet" href="{CSS}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>'''

def body(group,data):
    cards=''.join(f'<article><span>{num}</span><h3>{title}</h3><p>{copy}</p></article>' for num,title,copy in data['items'])
    image=GROUPS[group]['image']
    return f'''<section class="page-hero" style="--hero:url('{image}')"><div><div class="kicker light">{data['eyebrow']}</div><h1>{data['h1']}</h1><p>{data['lead']}</p><a class="btn gold" href="{WA}">{data['cta']}</a></div></section><section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>{data['section']}</h2></div><div><p class="large">One Ibiza-based point of contact keeps the confirmed moving parts aligned around the guest itinerary.</p><p>Availability, supplier terms and operational details remain subject to confirmation for each specific request.</p></div></section><section class="process"><div class="process-grid">{cards}</div></section><section class="closing-simple"><h2>{data['cta']}</h2><a class="btn dark" href="{WA}">WhatsApp Concierge</a></section>'''

for (lang,group),data in COPY.items():
    path=GROUPS[group][lang]
    direction,head_html=head(lang,group,data)
    dest=ROOT/path.strip('/')/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(f'<!doctype html><html lang="{lang}" dir="{direction}">{head_html}<body>{header(lang,group)}<main>{body(group,data)}</main>{footer(lang)}</body></html>',encoding='utf-8')

# Reciprocal hreflang on all five language equivalents for both commercial intents.
for group,paths in GROUPS.items():
    tags=hreflangs(group)
    for code,path in paths.items():
        if code=='image':
            continue
        file=ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'
        if not file.exists():
            continue
        text=file.read_text(encoding='utf-8')
        text=re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">','',text)
        text=text.replace('</head>',tags+'</head>',1)
        file.write_text(text,encoding='utf-8')

sitemap=ROOT/'sitemap.xml'
text=sitemap.read_text(encoding='utf-8')
new_paths=[GROUPS[g][l] for g in GROUPS for l in ('fr','de','ar')]
adds=[]
for path in new_paths:
    url=BASE+path
    if url not in text:
        adds.append(f'<url><loc>{url}</loc></url>')
if adds:
    text=text.replace('</urlset>',''.join(adds)+'</urlset>')
    sitemap.write_text(text,encoding='utf-8')

checks=[]
for path in new_paths:
    file=ROOT/path.strip('/')/'index.html'
    checks.append(file.is_file() and '<h1>' in file.read_text(encoding='utf-8'))
for group in GROUPS:
    en_file=ROOT/GROUPS[group]['en'].strip('/')/'index.html'
    en_text=en_file.read_text(encoding='utf-8')
    checks.append(all(f'hreflang="{code}"' in en_text for code in ('en','es','fr','de','ar','x-default')))
assert all(checks), 'Phase 16 validation failed'
print('PASS: Phase 16 six international high-intent pages + reciprocal hreflang')
