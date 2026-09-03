from pathlib import Path
from html import escape
import re

ROOT = Path('_site')
STYLE = '/assets/phase61.css?v=61'
LANGS = ('en','es','fr','de','ar')

SERVICES = {
 'chauffeur': {
  'eyebrow':'Move',
  'paths':{'en':'/private-chauffeur-ibiza/','es':'/es/chauffeur-privado-ibiza/','fr':'/fr/chauffeur-prive-ibiza/','de':'/de/privater-chauffeur-ibiza/','ar':'/ar/private-chauffeur-ibiza/'},
  'titles':{'en':'Private Chauffeur & Transport','es':'Chófer privado y transporte','fr':'Chauffeur privé & transport','de':'Privater Chauffeur & Transport','ar':'سائق خاص وتنقل'},
  'copy':{'en':'Airport, villa and nightlife movements.','es':'Aeropuerto, villas, restaurantes y nightlife.','fr':'Aéroport, villas, restaurants et nightlife.','de':'Flughafen, Villen, Dining und Nightlife.','ar':'تنقلات المطار والفلل والمطاعم والحياة الليلية.'}},
 'villas': {
  'eyebrow':'Stay',
  'paths':{'en':'/luxury-villas-ibiza/','es':'/es/villas-lujo-ibiza/','fr':'/fr/villas-luxe-ibiza/','de':'/de/luxusvillen-ibiza/','ar':'/ar/luxury-villas-ibiza/'},
  'titles':{'en':'Luxury Villas & Private Stays','es':'Villas de lujo y estancias privadas','fr':'Villas de luxe & séjours privés','de':'Luxusvillen & private Aufenthalte','ar':'فلل فاخرة وإقامات خاصة'},
  'copy':{'en':'Stays, access and in-villa coordination.','es':'Estancia, acceso y coordinación dentro de la villa.','fr':'Séjour, accès et coordination dans la villa.','de':'Aufenthalt, Zugang und Koordination in der Villa.','ar':'الإقامة والدخول والتنسيق داخل الفيلا.'}},
 'yacht': {
  'eyebrow':'Sea',
  'paths':{'en':'/yacht-charter-ibiza/','es':'/es/yate-privado-ibiza/','fr':'/fr/location-yacht-ibiza/','de':'/de/yachtcharter-ibiza/','ar':'/ar/yacht-charter-ibiza/'},
  'titles':{'en':'Yachts & Charters','es':'Yates y charters privados','fr':'Yachts & charters privés','de':'Yachten & Charter','ar':'يخوت وتأجير خاص'},
  'copy':{'en':'Marina, Formentera and shore logistics.','es':'Marina, Formentera y logística en tierra.','fr':'Marina, Formentera et logistique à terre.','de':'Marina, Formentera und Logistik an Land.','ar':'المارينا وفورمينتيرا واللوجستيات البرية.'}},
 'aviation': {
  'eyebrow':'Fly',
  'paths':{'en':'/private-aviation-ibiza/','es':'/es/aviacion-privada-ibiza/','fr':'/fr/aviation-privee-ibiza/','de':'/de/private-aviation-ibiza/','ar':'/ar/private-aviation-ibiza/'},
  'titles':{'en':'Private Aviation','es':'Aviación privada','fr':'Aviation privée','de':'Private Aviation','ar':'طيران خاص'},
  'copy':{'en':'Flight, baggage and ground coordination.','es':'Vuelo, equipaje y coordinación terrestre.','fr':'Vol, bagages et coordination au sol.','de':'Flug, Gepäck und Bodenkoordination.','ar':'الرحلة والأمتعة والتنسيق الأرضي.'}},
 'access': {
  'eyebrow':'Access',
  'paths':{'en':'/restaurants-nightlife-ibiza/','es':'/es/restaurantes-nightlife-ibiza/','fr':'/fr/restaurants-nightlife-ibiza/','de':'/de/restaurants-nightlife-ibiza/','ar':'/ar/restaurants-nightlife-ibiza/'},
  'titles':{'en':'Restaurants, Beach Clubs & Nightlife','es':'Restaurantes, Beach Clubs y Nightlife','fr':'Restaurants, Beach Clubs & Nightlife','de':'Restaurants, Beach Clubs & Nightlife','ar':'مطاعم وBeach Clubs وحياة ليلية'},
  'copy':{'en':'Dining and nightlife aligned with the itinerary.','es':'Dining y nightlife alineados con el itinerario.','fr':'Dining et nightlife alignés avec l’itinéraire.','de':'Dining und Nightlife mit der Reiseroute abgestimmt.','ar':'المطاعم والحياة الليلية منسقة مع البرنامج.'}},
 'security': {
  'eyebrow':'Protect',
  'paths':{'en':'/private-security-ibiza/','es':'/es/seguridad-privada-ibiza/','fr':'/fr/securite-privee-ibiza/','de':'/de/private-sicherheit-ibiza/','ar':'/ar/private-security-ibiza/'},
  'titles':{'en':'Security & Close Protection','es':'Seguridad y protección privada','fr':'Sécurité & protection rapprochée','de':'Security & Close Protection','ar':'أمن وحماية خاصة'},
  'copy':{'en':'Discreet protection around confirmed movements.','es':'Protección discreta alrededor de movimientos confirmados.','fr':'Protection discrète autour des déplacements confirmés.','de':'Diskreter Schutz rund um bestätigte Bewegungen.','ar':'حماية سرية حول التحركات المؤكدة.'}},
 'chef': {
  'eyebrow':'At Home',
  'paths':{'en':'/private-chef-staffing-ibiza/','es':'/es/chef-privado-staffing-ibiza/','fr':'/fr/chef-prive-personnel-villa-ibiza/','de':'/de/privatkoch-villa-staff-ibiza/','ar':'/ar/private-chef-staffing-ibiza/'},
  'titles':{'en':'Private Chefs & Villa Staffing','es':'Chef privado y personal de villa','fr':'Chef privé & personnel de villa','de':'Privatkoch & Villa Staff','ar':'شيف خاص وطاقم فيلا'},
  'copy':{'en':'Chef, villa staff and in-stay support.','es':'Chef, villa staff y soporte durante la estancia.','fr':'Chef, personnel de villa et support pendant le séjour.','de':'Koch, Villa Staff und Support im Aufenthalt.','ar':'شيف وطاقم فيلا ودعم أثناء الإقامة.'}},
 'car': {
  'eyebrow':'Drive',
  'paths':{'en':'/luxury-car-rental-ibiza/','es':'/es/alquiler-coches-lujo-ibiza/','fr':'/fr/location-voiture-luxe-ibiza/','de':'/de/luxusauto-mieten-ibiza/','ar':'/ar/luxury-car-rental-ibiza/'},
  'titles':{'en':'Luxury & Supercar Rental','es':'Alquiler de coches de lujo','fr':'Location de voiture de luxe','de':'Luxusauto & Supercar Rental','ar':'تأجير سيارات فاخرة'},
  'copy':{'en':'Luxury vehicle delivery and rental logistics.','es':'Entrega y logística de vehículos de lujo.','fr':'Livraison et logistique de véhicules de luxe.','de':'Übergabe und Logistik für Luxusfahrzeuge.','ar':'تسليم ولوجستيات السيارات الفاخرة.'}},
 'wellness': {
  'eyebrow':'Wellness',
  'paths':{'en':'/wellness-ibiza/','es':'/es/wellness-ibiza/','fr':'/fr/wellness-ibiza/','de':'/de/wellness-ibiza/','ar':'/ar/wellness-ibiza/'},
  'titles':{'en':'Wellness & Beauty','es':'Wellness y beauty privado','fr':'Wellness & beauté','de':'Wellness & Beauty','ar':'Wellness وجمال خاص'},
  'copy':{'en':'Private wellness and beauty sessions.','es':'Sesiones privadas de wellness y beauty.','fr':'Séances privées de wellness et beauté.','de':'Private Wellness- und Beauty-Sessions.','ar':'جلسات Wellness وجمال خاصة.'}},
 'events': {
  'eyebrow':'Occasions',
  'paths':{'en':'/private-events-ibiza/','es':'/es/eventos-privados-ibiza/','fr':'/fr/evenements-prives-ibiza/','de':'/de/private-events-ibiza/','ar':'/ar/private-events-ibiza/'},
  'titles':{'en':'Private Events & Celebrations','es':'Eventos y celebraciones privadas','fr':'Événements & célébrations privées','de':'Private Events & Feiern','ar':'فعاليات واحتفالات خاصة'},
  'copy':{'en':'Guest logistics and private occasions.','es':'Logística de invitados y ocasiones privadas.','fr':'Logistique invités et occasions privées.','de':'Gästelogistik und private Anlässe.','ar':'لوجستيات الضيوف والمناسبات الخاصة.'}},
 'bespoke': {
  'eyebrow':'Bespoke',
  'paths':{'en':'/bespoke-concierge-ibiza/','es':'/es/concierge-a-medida-ibiza/','fr':'/fr/conciergerie-sur-mesure-ibiza/','de':'/de/bespoke-concierge-ibiza/','ar':'/ar/bespoke-concierge-ibiza/'},
  'titles':{'en':'Lifestyle & Bespoke Requests','es':'Lifestyle y solicitudes a medida','fr':'Lifestyle & demandes sur mesure','de':'Lifestyle & individuelle Wünsche','ar':'Lifestyle وطلبات مخصصة'},
  'copy':{'en':'Special requests handled through one trusted contact.','es':'Solicitudes especiales desde un único contacto de confianza.','fr':'Demandes spéciales via un seul contact de confiance.','de':'Besondere Wünsche über einen vertrauenswürdigen Kontakt.','ar':'طلبات خاصة عبر جهة اتصال موثوقة واحدة.'}},
}

RELATED = {
 'chauffeur':['villas','access','aviation'],
 'villas':['chauffeur','chef','wellness'],
 'yacht':['chauffeur','access','villas'],
 'aviation':['chauffeur','security','villas'],
 'access':['chauffeur','yacht','security'],
 'security':['chauffeur','aviation','access'],
 'chef':['villas','wellness','events'],
 'car':['chauffeur','villas','yacht'],
 'wellness':['villas','chef','events'],
 'events':['chef','chauffeur','security'],
 'bespoke':['villas','access','chauffeur'],
}

COPY = {
 'en':{'eyebrow':'Complete the itinerary','title':'Designed to work together.','intro':'High-level Ibiza stays usually involve several moving parts. These services are commonly coordinated together through one point of contact.','cta':'Explore service →','aria':'Related private services'},
 'es':{'eyebrow':'Completa el itinerario','title':'Diseñados para funcionar juntos.','intro':'Las estancias privadas en Ibiza suelen incluir varias piezas. Estos servicios se coordinan habitualmente dentro del mismo brief y desde un único contacto.','cta':'Explorar servicio →','aria':'Servicios privados relacionados'},
 'fr':{'eyebrow':'Complétez l’itinéraire','title':'Pensés pour fonctionner ensemble.','intro':'Les séjours privés à Ibiza réunissent souvent plusieurs éléments. Ces services sont couramment coordonnés dans un même brief par un seul contact.','cta':'Découvrir le service →','aria':'Services privés associés'},
 'de':{'eyebrow':'Reise sinnvoll ergänzen','title':'Für gemeinsame Koordination gedacht.','intro':'Private Ibiza-Aufenthalte bestehen meist aus mehreren Elementen. Diese Services werden häufig innerhalb eines Briefings über einen Ansprechpartner koordiniert.','cta':'Service entdecken →','aria':'Verwandte private Services'},
 'ar':{'eyebrow':'أكمل برنامج الإقامة','title':'خدمات مصممة للعمل معاً.','intro':'غالباً ما تتضمن الإقامة الخاصة في إيبيزا عدة عناصر مترابطة. يمكن تنسيق هذه الخدمات ضمن طلب واحد ومن خلال جهة اتصال واحدة.','cta':'استكشف الخدمة ←','aria':'خدمات خاصة مرتبطة'},
}

# Publish styling.
assets = ROOT / 'assets'
assets.mkdir(parents=True, exist_ok=True)
(assets / 'phase61.css').write_text(Path('phase61.css').read_text(encoding='utf-8'), encoding='utf-8')


def page_for(path):
    return ROOT / path.strip('/') / 'index.html'


def related_section(service_key, lang):
    c = COPY[lang]
    cards = []
    for target_key in RELATED[service_key]:
        target = SERVICES[target_key]
        href = target['paths'][lang]
        cards.append(
            f'<a class="ivm-related-card" href="{href}">'
            f'<small>{escape(target["eyebrow"])}</small>'
            f'<div><strong>{escape(target["titles"][lang])}</strong><p>{escape(target["copy"][lang])}</p></div>'
            f'<b>{escape(c["cta"])}</b></a>'
        )
    return (
        f'<section class="ivm-related" aria-label="{escape(c["aria"])}"><div class="ivm-related-inner">'
        f'<div class="ivm-related-head"><div><div class="eyebrow">{escape(c["eyebrow"])}</div><h2>{escape(c["title"])}</h2></div>'
        f'<p>{escape(c["intro"])}</p></div><div class="ivm-related-grid">{"".join(cards)}</div></div></section>'
    )

# Validate every declared URL exists before touching HTML.
for key, service in SERVICES.items():
    for lang in LANGS:
        p = page_for(service['paths'][lang])
        if not p.exists():
            raise SystemExit(f'Phase 61 target missing: {key}/{lang} -> {service["paths"][lang]}')

updated = 0
for key, service in SERVICES.items():
    for lang in LANGS:
        path = service['paths'][lang]
        file = page_for(path)
        html = file.read_text(encoding='utf-8')
        # Replace the original English Phase 29 module instead of duplicating it.
        html = re.sub(r'<section class="ivm-related"[^>]*>.*?</section>', '', html, count=1, flags=re.I|re.S)
        html = re.sub(r'<link rel="stylesheet" href="/assets/phase29\.css\?v=29">', '', html, flags=re.I)
        if STYLE not in html:
            html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
        marker = '<section class="closing-simple">'
        if marker not in html:
            raise SystemExit(f'Phase 61 closing marker missing: {path}')
        html = html.replace(marker, related_section(key, lang) + marker, 1)
        file.write_text(html, encoding='utf-8')
        updated += 1

# Strong validation: one module, three distinct same-language targets, no self-link.
for key, service in SERVICES.items():
    for lang in LANGS:
        path = service['paths'][lang]
        html = page_for(path).read_text(encoding='utf-8')
        assert html.count('class="ivm-related"') == 1, (key, lang, 'module')
        assert html.count('class="ivm-related-card"') == 3, (key, lang, 'cards')
        assert STYLE in html, (key, lang, 'style')
        assert '/assets/phase29.css?v=29' not in html, (key, lang, 'old style')
        targets = RELATED[key]
        hrefs = [SERVICES[t]['paths'][lang] for t in targets]
        assert len(set(hrefs)) == 3 and path not in hrefs, (key, lang, 'target uniqueness')
        for href in hrefs:
            assert f'href="{href}"' in html, (key, lang, href)
            assert page_for(href).exists(), (key, lang, 'broken target', href)
        if lang != 'en':
            prefix = '/' + lang + '/'
            assert all(h.startswith(prefix) for h in hrefs), (key, lang, 'cross-language leak', hrefs)

assert updated == 55, updated
assert (ROOT/'assets'/'phase61.css').exists() and (ROOT/'assets'/'phase61.css').stat().st_size > 1000
print('PASS: Phase 61 smart multilingual interlinking active across 55 service landings with 165 same-language related-service links')
