from pathlib import Path
from html import escape
from urllib.parse import urlparse
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
WA = 'https://wa.me/34600703303'
TODAY = '2026-09-03'

SOURCE = {
    'fr': ROOT / 'fr' / 'conciergerie-privee-ibiza' / 'index.html',
    'de': ROOT / 'de' / 'privater-concierge-ibiza' / 'index.html',
    'ar': ROOT / 'ar' / 'private-concierge-ibiza' / 'index.html',
}

SERVICES = {
    'villas': {
        'en': '/luxury-villas-ibiza/',
        'image': '/assets/images/villa.jpg',
        'fr': {
            'path': '/fr/villas-luxe-ibiza/',
            'title': 'Villas de luxe à Ibiza | Conciergerie privée | Ibiza VIP Move',
            'desc': 'Villas de luxe à Ibiza avec coordination privée de l’arrivée, du séjour, du personnel, du transport et des demandes lifestyle par Ibiza VIP Move.',
            'kicker': 'Séjour privé · Ibiza',
            'h1': 'Villas de luxe à Ibiza, coordonnées autour de votre séjour.',
            'lead': 'Une villa privée ne se résume pas à une adresse. Arrivée, accès, transport, personnel et rythme du séjour doivent fonctionner ensemble.',
            'section': 'Le séjour commence avant l’arrivée.',
            'large': 'Nous coordonnons les éléments pratiques autour de la villa afin que le séjour reste fluide dès les premières heures.',
            'items': [('01','Brief villa','Dates, invités, localisation, accès et priorités du séjour.'),('02','Pré-arrivée','Horaires, arrivée, transport et besoins pratiques alignés avant l’arrivée.'),('03','Pendant le séjour','Chauffeur, personnel, wellness, restauration et demandes lifestyle peuvent être connectés.'),('04','Adaptation','Si le planning évolue, les éléments concernés peuvent être réorganisés autour du nouveau brief.')],
            'cta': 'Demander une villa privée',
        },
        'de': {
            'path': '/de/luxusvillen-ibiza/',
            'title': 'Luxusvillen Ibiza | Private Villa Concierge | Ibiza VIP Move',
            'desc': 'Luxusvillen auf Ibiza mit privater Koordination von Ankunft, Aufenthalt, Personal, Chauffeur und Lifestyle-Anfragen durch Ibiza VIP Move.',
            'kicker': 'Privater Aufenthalt · Ibiza',
            'h1': 'Luxusvillen auf Ibiza, rund um Ihren Aufenthalt koordiniert.',
            'lead': 'Eine private Villa ist mehr als eine Adresse. Ankunft, Zugang, Mobilität, Personal und Tagesablauf sollten als ein Aufenthalt funktionieren.',
            'section': 'Der Aufenthalt beginnt vor der Ankunft.',
            'large': 'Wir koordinieren die praktischen Elemente rund um die Villa, damit der Aufenthalt von den ersten Stunden an klar organisiert ist.',
            'items': [('01','Villa-Briefing','Reisedaten, Gäste, Lage, Zugang und Prioritäten des Aufenthalts.'),('02','Vor Anreise','Zeiten, Ankunft, Chauffeur und praktische Anforderungen vorab abstimmen.'),('03','Während des Aufenthalts','Chauffeur, Personal, Wellness, Dining und Lifestyle-Anfragen können verbunden werden.'),('04','Anpassen','Wenn sich der Zeitplan ändert, können betroffene Elemente rund um das neue Briefing neu abgestimmt werden.')],
            'cta': 'Private Villa anfragen',
        },
        'ar': {
            'path': '/ar/luxury-villas-ibiza/',
            'title': 'فلل فاخرة في إيبيزا | كونسيرج خاص | Ibiza VIP Move',
            'desc': 'فلل فاخرة في إيبيزا مع تنسيق خاص للوصول والإقامة والطاقم والسائق وطلبات أسلوب الحياة عبر Ibiza VIP Move.',
            'kicker': 'إقامة خاصة · إيبيزا',
            'h1': 'فلل فاخرة في إيبيزا، منسقة حول تفاصيل إقامتك.',
            'lead': 'الفيلا الخاصة ليست مجرد عنوان. الوصول والدخول والتنقل والطاقم وإيقاع الإقامة يجب أن تعمل كمنظومة واحدة.',
            'section': 'تبدأ الإقامة قبل الوصول.',
            'large': 'ننسق التفاصيل العملية المحيطة بالفيلا حتى تكون الساعات الأولى وما بعدها أكثر سلاسة ووضوحاً.',
            'items': [('01','تفاصيل الفيلا','التواريخ والضيوف والموقع والدخول وأولويات الإقامة.'),('02','قبل الوصول','تنسيق التوقيت والوصول والسائق والمتطلبات العملية مسبقاً.'),('03','أثناء الإقامة','يمكن ربط السائق والطاقم والعافية والمطاعم وطلبات أسلوب الحياة.'),('04','التكيف','عند تغير الجدول يمكن إعادة تنسيق العناصر المتأثرة وفق التفاصيل الجديدة.')],
            'cta': 'طلب فيلا خاصة',
        },
    },
    'yacht': {
        'en': '/yacht-charter-ibiza/',
        'image': '/assets/images/yacht.jpg',
        'fr': {
            'path': '/fr/location-yacht-ibiza/',
            'title': 'Location yacht Ibiza & Formentera | Ibiza VIP Move',
            'desc': 'Yacht privé et charter à Ibiza et Formentera avec coordination de la marina, du chauffeur, du catering et du planning par Ibiza VIP Move.',
            'kicker': 'Yacht privé · Ibiza & Formentera',
            'h1': 'Une journée en yacht, intégrée à votre itinéraire.',
            'lead': 'Le yacht, la marina, le transport terrestre et la suite de la journée sont coordonnés autour du même planning.',
            'section': 'De la villa au pont, sans rupture.',
            'large': 'Le meilleur planning en mer tient compte de ce qui se passe avant l’embarquement et après le retour à terre.',
            'items': [('01','Brief mer','Date, invités, préférences, timing et type de journée souhaité.'),('02','Marina','Point de départ, horaire et détails pratiques clarifiés avant la journée.'),('03','À bord','Catering et besoins confirmés alignés avec le charter.'),('04','Retour','Chauffeur, dîner ou programme du soir peuvent être coordonnés autour de l’heure de retour.')],
            'cta': 'Demander un yacht privé',
        },
        'de': {
            'path': '/de/yachtcharter-ibiza/',
            'title': 'Yachtcharter Ibiza & Formentera | Ibiza VIP Move',
            'desc': 'Private Yacht und Charter auf Ibiza und Formentera mit Marina-, Chauffeur-, Catering- und Zeitplan-Koordination durch Ibiza VIP Move.',
            'kicker': 'Private Yacht · Ibiza & Formentera',
            'h1': 'Ein privater Yachttag, eingebunden in Ihre Reiseroute.',
            'lead': 'Yacht, Marina, Bodentransport und der weitere Tagesablauf werden rund um denselben Zeitplan koordiniert.',
            'section': 'Von der Villa bis an Bord.',
            'large': 'Ein gut geplanter Tag auf dem Wasser berücksichtigt, was vor dem Ablegen und nach der Rückkehr passiert.',
            'items': [('01','Sea Brief','Datum, Gäste, Präferenzen, Timing und gewünschter Tagesablauf.'),('02','Marina','Abfahrtsort, Uhrzeit und praktische Details vorab klären.'),('03','An Bord','Bestätigte Catering- und Servicewünsche mit dem Charter abstimmen.'),('04','Rückkehr','Chauffeur, Dinner oder Abendprogramm können rund um die Rückkehrzeit koordiniert werden.')],
            'cta': 'Private Yacht anfragen',
        },
        'ar': {
            'path': '/ar/yacht-charter-ibiza/',
            'title': 'يخت خاص في إيبيزا وفورمينتيرا | Ibiza VIP Move',
            'desc': 'يخت خاص وتأجير في إيبيزا وفورمينتيرا مع تنسيق المرسى والسائق والضيافة والجدول عبر Ibiza VIP Move.',
            'kicker': 'يخت خاص · إيبيزا وفورمينتيرا',
            'h1': 'يوم على اليخت، منسق كجزء من برنامج إقامتك.',
            'lead': 'ننسق اليخت والمرسى والتنقل البري وما بعد العودة ضمن جدول واحد واضح.',
            'section': 'من الفيلا إلى اليخت بسلاسة.',
            'large': 'اليوم المثالي في البحر يعتمد أيضاً على ما يحدث قبل الإبحار وبعد العودة إلى الجزيرة.',
            'items': [('01','تفاصيل اليوم','التاريخ والضيوف والتفضيلات والتوقيت ونمط اليوم المطلوب.'),('02','المرسى','تأكيد نقطة الانطلاق والوقت والتفاصيل العملية مسبقاً.'),('03','على متن اليخت','تنسيق الضيافة والطلبات المؤكدة مع برنامج الرحلة.'),('04','العودة','يمكن ربط السائق والعشاء أو برنامج المساء بوقت العودة المتوقع.')],
            'cta': 'طلب يخت خاص',
        },
    },
    'aviation': {
        'en': '/private-aviation-ibiza/',
        'image': '/assets/images/aviation.jpg',
        'fr': {
            'path': '/fr/aviation-privee-ibiza/',
            'title': 'Aviation privée Ibiza | Coordination au sol | Ibiza VIP Move',
            'desc': 'Aviation privée à Ibiza avec coordination du vol, FBO, bagages, chauffeur et transfert vers villa ou hôtel par Ibiza VIP Move.',
            'kicker': 'Aviation privée · Ibiza',
            'h1': 'Du vol au transport terrestre, un seul brief.',
            'lead': 'L’arrivée ou le départ est coordonné avec les éléments terrestres qui suivent : bagages, véhicules, destination et timing.',
            'section': 'Le vol n’est qu’une partie de l’arrivée.',
            'large': 'Nous connectons les détails de l’aviation privée avec le mouvement au sol afin de réduire les ruptures de communication.',
            'items': [('01','Vol','Timing, passagers, bagages et destination clarifiés.'),('02','Arrivée','Les besoins opérationnels autour de l’arrivée sont alignés avant le mouvement.'),('03','Transport','Le nombre de véhicules et le profil bagages sont considérés ensemble.'),('04','Suite du séjour','Villa, hôtel, sécurité ou autres services peuvent être coordonnés autour de l’arrivée.')],
            'cta': 'Demander une coordination aviation',
        },
        'de': {
            'path': '/de/private-aviation-ibiza/',
            'title': 'Private Aviation Ibiza | Ground Coordination | Ibiza VIP Move',
            'desc': 'Private Aviation auf Ibiza mit Koordination von Flug, FBO, Gepäck, Chauffeur und Weiterfahrt zu Villa oder Hotel durch Ibiza VIP Move.',
            'kicker': 'Private Aviation · Ibiza',
            'h1': 'Vom Flug bis zum Bodentransport in einem Briefing.',
            'lead': 'Ankunft oder Abflug werden mit den anschließenden Bodenelementen verbunden: Gepäck, Fahrzeuge, Ziel und Timing.',
            'section': 'Der Flug ist nur ein Teil der Ankunft.',
            'large': 'Wir verbinden die Details der privaten Luftfahrt mit der Bodenbewegung, damit weniger getrennte Kommunikation nötig ist.',
            'items': [('01','Flug','Timing, Passagiere, Gepäck und Ziel klären.'),('02','Ankunft','Operative Anforderungen rund um die Ankunft vorab abstimmen.'),('03','Fahrzeuge','Fahrzeugbedarf und Gepäckprofil gemeinsam berücksichtigen.'),('04','Weiterer Aufenthalt','Villa, Hotel, Security oder andere Services können rund um die Ankunft koordiniert werden.')],
            'cta': 'Aviation-Koordination anfragen',
        },
        'ar': {
            'path': '/ar/private-aviation-ibiza/',
            'title': 'طيران خاص في إيبيزا | تنسيق أرضي | Ibiza VIP Move',
            'desc': 'تنسيق الطيران الخاص في إيبيزا للرحلة والأمتعة والسائق والانتقال إلى الفيلا أو الفندق عبر Ibiza VIP Move.',
            'kicker': 'طيران خاص · إيبيزا',
            'h1': 'من الطائرة إلى التنقل الأرضي ضمن طلب واحد.',
            'lead': 'نربط الوصول أو المغادرة بالتفاصيل الأرضية التالية: الأمتعة والمركبات والوجهة والتوقيت.',
            'section': 'الرحلة جزء واحد من تجربة الوصول.',
            'large': 'نربط تفاصيل الطيران الخاص بالحركة الأرضية لتقليل تعدد المحادثات وجعل الوصول أكثر وضوحاً.',
            'items': [('01','الرحلة','تأكيد التوقيت والركاب والأمتعة والوجهة.'),('02','الوصول','تنسيق المتطلبات التشغيلية المحيطة بالوصول مسبقاً.'),('03','المركبات','دراسة عدد المركبات وحجم الأمتعة ضمن خطة واحدة.'),('04','باقي الإقامة','يمكن ربط الفيلا أو الفندق أو الأمن والخدمات الأخرى بوقت الوصول.')],
            'cta': 'طلب تنسيق طيران خاص',
        },
    },
    'security': {
        'en': '/private-security-ibiza/',
        'image': '/assets/images/security.jpg',
        'fr': {
            'path': '/fr/securite-privee-ibiza/',
            'title': 'Sécurité privée Ibiza | Close Protection | Ibiza VIP Move',
            'desc': 'Sécurité privée et close protection à Ibiza avec coordination discrète des déplacements, lieux et horaires autour du client.',
            'kicker': 'Sécurité privée · Ibiza',
            'h1': 'La sécurité privée, intégrée discrètement au séjour.',
            'lead': 'Les besoins de protection sont coordonnés autour du client, des déplacements, des lieux et du planning confirmé.',
            'section': 'La protection fonctionne mieux dans son contexte.',
            'large': 'Transport, lieux, horaires et exigences privées peuvent être considérés ensemble afin d’éviter une coordination fragmentée.',
            'items': [('01','Brief sécurité','Principal, invités, planning et contexte opérationnel.'),('02','Déplacements','Les mouvements confirmés peuvent être alignés avec les besoins de protection.'),('03','Lieux','Les détails utiles autour des villas, événements ou nightlife sont clarifiés selon le besoin.'),('04','Discrétion','Les informations sensibles restent limitées aux personnes nécessaires à l’exécution confirmée.')],
            'cta': 'Demander une sécurité privée',
        },
        'de': {
            'path': '/de/private-sicherheit-ibiza/',
            'title': 'Private Sicherheit Ibiza | Close Protection | Ibiza VIP Move',
            'desc': 'Private Security und Close Protection auf Ibiza mit diskreter Koordination von Bewegungen, Orten und Zeitplan rund um den Kunden.',
            'kicker': 'Private Sicherheit · Ibiza',
            'h1': 'Private Sicherheit, diskret in den Aufenthalt integriert.',
            'lead': 'Schutzanforderungen werden rund um den Kunden, Bewegungen, Orte und den bestätigten Zeitplan koordiniert.',
            'section': 'Schutz funktioniert am besten im richtigen Kontext.',
            'large': 'Transport, Orte, Zeiten und private Anforderungen können zusammen betrachtet werden, um fragmentierte Koordination zu vermeiden.',
            'items': [('01','Security Brief','Principal, Gäste, Zeitplan und operativer Kontext.'),('02','Bewegungen','Bestätigte Fahrten können mit den Schutzanforderungen abgestimmt werden.'),('03','Orte','Relevante Details zu Villen, Events oder Nightlife werden nach Bedarf geklärt.'),('04','Diskretion','Sensible Informationen bleiben auf die für die bestätigte Ausführung notwendigen Personen begrenzt.')],
            'cta': 'Private Security anfragen',
        },
        'ar': {
            'path': '/ar/private-security-ibiza/',
            'title': 'أمن خاص وحماية شخصية في إيبيزا | Ibiza VIP Move',
            'desc': 'أمن خاص وحماية شخصية في إيبيزا مع تنسيق سري للتنقل والمواقع والجدول حول العميل عبر Ibiza VIP Move.',
            'kicker': 'أمن خاص · إيبيزا',
            'h1': 'أمن خاص مندمج مع الإقامة بسرية وهدوء.',
            'lead': 'ننسق متطلبات الحماية حول العميل والتنقل والمواقع والجدول المؤكد.',
            'section': 'الحماية تعمل بشكل أفضل ضمن سياق الرحلة.',
            'large': 'يمكن النظر إلى التنقل والمواقع والتوقيت والمتطلبات الخاصة كخطة واحدة بدلاً من تنسيق منفصل.',
            'items': [('01','تفاصيل الأمن','الشخص الرئيسي والضيوف والجدول والسياق التشغيلي.'),('02','التنقل','يمكن تنسيق الحركات المؤكدة مع متطلبات الحماية.'),('03','المواقع','توضيح التفاصيل اللازمة حول الفلل أو الفعاليات أو الحياة الليلية حسب الحاجة.'),('04','السرية','تبقى المعلومات الحساسة ضمن نطاق الأشخاص الضروريين لتنفيذ الخدمة المؤكدة.')],
            'cta': 'طلب أمن خاص',
        },
    },
}


def head_links(service_key):
    s = SERVICES[service_key]
    links = [f'<link rel="alternate" hreflang="en" href="{BASE}{s["en"]}">']
    for lang in ('fr','de','ar'):
        links.append(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{s[lang]["path"]}">')
    links.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}{s["en"]}">')
    return ''.join(links)


def main_html(lang, data, image):
    process = ''.join(f'<article><span>{num}</span><h3>{escape(title)}</h3><p>{escape(copy)}</p></article>' for num,title,copy in data['items'])
    return f'''<main id="main-content"><section class="page-hero"><div class="page-hero-media"><img src="{image}" alt="{escape(data['h1'])} — Ibiza VIP Move" width="1800" height="1200" fetchpriority="high" decoding="async"></div><div><div class="kicker light">{escape(data['kicker'])}</div><h1>{escape(data['h1'])}</h1><p>{escape(data['lead'])}</p><a class="btn gold" href="{WA}">{escape(data['cta'])}</a></div></section><section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>{escape(data['section'])}</h2></div><div><p class="large">{escape(data['large'])}</p></div></section><section class="process"><div class="section-head"><div class="kicker dark">Private coordination</div><h2>{escape(data['section'])}</h2></div><div class="process-grid">{process}</div></section><section class="closing-simple"><h2>{escape(data['cta'])}</h2><p>Ibiza VIP Move · Private client support · Ibiza</p><a class="btn dark" href="{WA}">{escape(data['cta'])}</a></section></main>'''


def update_jsonld(text, canonical, title, desc, image, lang):
    patt = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)
    def repl(m):
        try:
            obj = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if not isinstance(obj, dict):
            return m.group(0)
        typ = obj.get('@type')
        if typ == 'WebPage':
            obj['name'] = title
            obj['url'] = canonical
            obj['description'] = desc
            obj['inLanguage'] = lang
            obj['primaryImageOfPage'] = {'@type':'ImageObject','url':BASE+image}
        elif typ == 'Service':
            obj['url'] = canonical
            obj['areaServed'] = {'@type':'Place','name':'Ibiza, Spain'}
            obj['image'] = BASE + image
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'
    return patt.sub(repl, text)


created=[]
for lang in ('fr','de','ar'):
    if not SOURCE[lang].exists():
        raise SystemExit(f'Missing Phase 36 source page: {SOURCE[lang]}')
    source = SOURCE[lang].read_text(encoding='utf-8')
    for key, service in SERVICES.items():
        data = service[lang]
        canonical = BASE + data['path']
        html = source
        html = re.sub(r'<title>.*?</title>', f'<title>{escape(data["title"])}</title>', html, count=1, flags=re.I|re.S)
        html = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1)+escape(data['desc'])+m.group(2), html, count=1, flags=re.I)
        html = re.sub(r'<link[^>]+rel="alternate"[^>]*>', '', html, flags=re.I)
        html = re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', lambda m: m.group(1)+canonical+m.group(2), html, count=1, flags=re.I)
        for prop,val in [('og:title',data['title']),('og:description',data['desc']),('og:url',canonical),('og:image',BASE+service['image'])]:
            html = re.sub(rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")', lambda m,v=val: m.group(1)+escape(v)+m.group(2), html, count=1, flags=re.I)
        html = re.sub(r'<main\b[^>]*>.*?</main>', main_html(lang,data,service['image']), html, count=1, flags=re.I|re.S)
        html = update_jsonld(html,canonical,data['title'],data['desc'],service['image'],lang)
        html = html.replace('</head>', head_links(key) + '</head>', 1)
        dest = ROOT / data['path'].strip('/') / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html,encoding='utf-8')
        created.append((key,lang,data['path'],service['image']))

# Reciprocal hreflang across English canonical service pages and all localized siblings.
for key, service in SERVICES.items():
    tags = head_links(key)
    paths = [service['en']] + [service[l]['path'] for l in ('fr','de','ar')]
    for rel in paths:
        p = ROOT/'index.html' if rel=='/' else ROOT/rel.strip('/')/'index.html'
        if not p.exists():
            continue
        html=p.read_text(encoding='utf-8')
        html=re.sub(r'<link[^>]+rel="alternate"[^>]*>', '', html, flags=re.I)
        html=html.replace('</head>',tags+'</head>',1)
        p.write_text(html,encoding='utf-8')

# Main sitemap.
sitemap=ROOT/'sitemap.xml'
ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
tree=ET.parse(sitemap); root=tree.getroot(); ns='http://www.sitemaps.org/schemas/sitemap/0.9'
existing={u.find(f'{{{ns}}}loc').text for u in root.findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for _,_,path,_ in created:
    url=BASE+path
    if url not in existing:
        u=ET.SubElement(root,f'{{{ns}}}url'); ET.SubElement(u,f'{{{ns}}}loc').text=url; ET.SubElement(u,f'{{{ns}}}lastmod').text=TODAY; ET.SubElement(u,f'{{{ns}}}changefreq').text='monthly'; ET.SubElement(u,f'{{{ns}}}priority').text='0.75'
tree.write(sitemap,encoding='utf-8',xml_declaration=True)

# Image sitemap.
image_sitemap=ROOT/'image-sitemap.xml'
if image_sitemap.exists():
    SM='http://www.sitemaps.org/schemas/sitemap/0.9'; IMG='http://www.google.com/schemas/sitemap-image/1.1'
    ET.register_namespace('',SM); ET.register_namespace('image',IMG)
    it=ET.parse(image_sitemap); ir=it.getroot(); ie={u.find(f'{{{SM}}}loc').text for u in ir.findall(f'{{{SM}}}url') if u.find(f'{{{SM}}}loc') is not None}
    for _,_,path,image in created:
        url=BASE+path
        if url not in ie:
            u=ET.SubElement(ir,f'{{{SM}}}url'); ET.SubElement(u,f'{{{SM}}}loc').text=url; im=ET.SubElement(u,f'{{{IMG}}}image'); ET.SubElement(im,f'{{{IMG}}}loc').text=BASE+image
    it.write(image_sitemap,encoding='utf-8',xml_declaration=True)

# Discovery resource.
llms=ROOT/'llms.txt'
if llms.exists():
    text=llms.read_text(encoding='utf-8')
    if '/fr/villas-luxe-ibiza/' not in text:
        lines=['','## International core service pages']
        for key,service in SERVICES.items():
            for lang in ('fr','de','ar'):
                d=service[lang]; lines.append(f'- [{d["h1"]}]({BASE}{d["path"]})')
        llms.write_text(text+'\n'.join(lines)+'\n',encoding='utf-8')

# Validation.
assert len(created)==12
for key,lang,path,image in created:
    html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    assert html.count('<h1')==1,(lang,key)
    assert BASE+path in html,(lang,key)
    assert image in html,(lang,key)
    assert f'hreflang="{lang}"' in html,(lang,key)
    assert 'id="main-content"' in html,(lang,key)
    assert 'ivm-skip-link' in html,(lang,key)
    assert 'application/ld+json' in html,(lang,key)
for key,service in SERVICES.items():
    en=(ROOT/service['en'].strip('/')/'index.html').read_text(encoding='utf-8')
    for lang in ('fr','de','ar'):
        assert BASE+service[lang]['path'] in en,(key,lang)
print('PASS: Phase 36 created 12 localized FR/DE/AR core-service pages with reciprocal hreflang, sitemap and image discovery')
