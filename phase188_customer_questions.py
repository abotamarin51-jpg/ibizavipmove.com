"""Improve existing EN/ES customer answers and connect their existing entities.

FAQPage is semantic metadata, not a Google rich-result or AI inclusion promise.
The visible answers and JSON-LD are generated from the same four-item list.
"""
from copy import deepcopy
from html import escape, unescape
from pathlib import Path
import json
import re

BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
LASTMOD = '2026-10-31'
SCRIPT = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.S | re.I)
DETAIL = re.compile(r'<details\b[^>]*>.*?</details>', re.S | re.I)
CORE_SECTION = re.compile(r'<section\b[^>]*class="ivm-service-faq"[^>]*>.*?</section>', re.S | re.I)
CONCIERGE_SECTION = re.compile(r'<section\b[^>]*class="faq"[^>]*>.*?</section>', re.S | re.I)

# Positions refer to the existing four-item service FAQ, whose other answers stay intact.
UPDATES = {
    '/private-chauffeur-ibiza/': {
        0: ('How do I book a private chauffeur in Ibiza?',
            'Contact Ibiza VIP Move through the website WhatsApp link or enquiry form. Share the date, pickup and destination, passengers, luggage and whether you need one transfer or several hours with a driver. For airport arrivals, include the flight details. We confirm the vehicle, schedule, price and booking terms in writing.'),
        1: ('How much does a private driver in Ibiza cost?',
            'The quote depends on the date, route, vehicle, passengers and time required. Tell us whether you need an airport transfer, a return journey or an hourly chauffeur. Before booking, check the agreed hours, waiting time, extra stops, inclusions and cancellation terms in the written quote.'),
        3: ('Can I book a Mercedes-Benz V-Class or Sprinter in Ibiza?',
            'Mercedes-Benz V-Class vehicles and Sprinter minibuses can be requested for private chauffeur services. Share the passenger count and luggage so we can confirm a suitable vehicle or coordinate several vehicles. The model, capacity and availability are confirmed for your dates before booking.'),
    },
    '/es/chauffeur-privado-ibiza/': {
        0: ('¿Cómo reservar un chófer privado en Ibiza?',
            'Contacta con Ibiza VIP Move mediante el enlace de WhatsApp o el formulario de la web. Indica fecha, recogida, destino, pasajeros, equipaje y si necesitas un traslado o varias horas con chófer. Para llegadas al aeropuerto, añade los datos del vuelo. Confirmamos por escrito vehículo, horario, precio y condiciones de reserva.'),
        1: ('¿Cuánto cuesta un chófer privado en Ibiza?',
            'El presupuesto depende de la fecha, el recorrido, el vehículo, los pasajeros y el tiempo necesario. Indica si buscas un traslado de aeropuerto, ida y vuelta o un chófer por horas. Antes de reservar, revisa las horas acordadas, esperas, paradas adicionales, servicios incluidos y condiciones de cancelación del presupuesto escrito.'),
        3: ('¿Puedo reservar un Mercedes-Benz Clase V o Sprinter en Ibiza?',
            'Puedes solicitar vehículos Mercedes-Benz Clase V y minibuses Sprinter para servicios con chófer privado. Comparte el número de pasajeros y el equipaje para confirmar un vehículo adecuado o coordinar varios. El modelo, la capacidad y la disponibilidad se confirman para tus fechas antes de reservar.'),
    },
    '/luxury-villas-ibiza/': {
        0: ('Can I arrange an Ibiza villa with a private chef and staff?',
            'Yes. Ibiza VIP Move can coordinate villa requests with private chefs and staffing. Share the stay dates, guest count, preferred area, meals and daily service hours. The property, staff availability, duties, food shopping and additional charges are confirmed separately in the written scope; these services are not automatically included in the villa booking.'),
    },
    '/es/villas-lujo-ibiza/': {
        0: ('¿Puedo reservar una villa en Ibiza con chef privado y personal?',
            'Sí. Ibiza VIP Move puede coordinar la solicitud de villa con chef privado y personal. Indica fechas, huéspedes, zona preferida, comidas y horas de servicio diarias. La propiedad, disponibilidad del personal, tareas, compra de alimentos y cargos adicionales se confirman por separado y por escrito; estos servicios no se incluyen automáticamente en la reserva de la villa.'),
    },
    '/yacht-charter-ibiza/': {
        0: ('How do I plan a private yacht trip from Ibiza to Formentera?',
            'Yes. You can request a private yacht day from Ibiza with Formentera as the proposed destination. Share the date, guests, departure marina if known, preferred itinerary and lunch plans. The vessel, capacity, route, timings and any marina transfers are confirmed before booking. The route remains subject to weather and the captain\'s decision.'),
        3: ('What should I check in an Ibiza yacht charter quote?',
            'Check the vessel, guest capacity, charter hours, departure point and cancellation terms. Ask which costs are included and which are separate, particularly fuel, crew, catering, marina fees and transfers. Ibiza VIP Move clarifies the operator\'s terms for the selected yacht before you confirm.'),
    },
    '/es/yate-privado-ibiza/': {
        0: ('¿Cómo organizar una excursión en yate privado de Ibiza a Formentera?',
            'Sí. Puedes solicitar un día de yate privado desde Ibiza con Formentera como destino propuesto. Indica fecha, invitados, marina de salida si la conoces, recorrido y planes de comida. Embarcación, capacidad, horarios y posibles traslados a la marina se confirman antes de reservar. La ruta queda sujeta al tiempo y a la decisión del capitán.'),
        3: ('¿Qué debo revisar en el presupuesto de un yate en Ibiza?',
            'Revisa la embarcación, capacidad de pasajeros, horas de alquiler, salida y condiciones de cancelación. Consulta qué gastos están incluidos y cuáles se cobran aparte, especialmente combustible, tripulación, catering, tasas de marina y traslados. Ibiza VIP Move aclara las condiciones del operador para el yate elegido antes de confirmar.'),
    },
    '/restaurants-nightlife-ibiza/': {
        0: ('Can you arrange last-minute restaurant or VIP reservations in Ibiza?',
            'We assess last-minute restaurant, beach club and nightlife requests according to availability. Send the date, time, guest count, preferred venue and any flexibility. Ibiza VIP Move checks options and confirms deposits, minimum spend and access conditions before a reservation is treated as booked. A request does not guarantee a table or entry.'),
    },
    '/es/restaurantes-nightlife-ibiza/': {
        0: ('¿Podéis gestionar reservas de última hora en restaurantes y clubes de Ibiza?',
            'Estudiamos solicitudes de última hora para restaurantes, beach clubs y nightlife según disponibilidad. Envía fecha, hora, número de personas, lugar preferido y posibles alternativas. Ibiza VIP Move revisa opciones y confirma depósitos, consumo mínimo y condiciones de acceso antes de dar la reserva por confirmada. Una solicitud no garantiza mesa ni entrada.'),
    },
    '/private-security-ibiza/': {
        0: ('How do I arrange private security and close protection in Ibiza?',
            'Yes. Ibiza VIP Move coordinates requests for private security and close protection around the client\'s stay. Share the dates, locations, transport plans and broad requirements privately. The appropriate team, scope, availability and service conditions are established for the specific brief before confirmation.'),
    },
    '/es/seguridad-privada-ibiza/': {
        0: ('¿Cómo solicitar seguridad privada y escoltas en Ibiza?',
            'Sí. Ibiza VIP Move coordina solicitudes de seguridad privada y protección personal alrededor de la estancia. Comparte de forma privada fechas, lugares, transporte previsto y necesidades generales. El equipo adecuado, alcance, disponibilidad y condiciones del servicio se concretan para cada solicitud antes de confirmar.'),
    },
    '/private-concierge-ibiza/': {
        0: ('What does a luxury concierge service in Ibiza include?',
            'Ibiza VIP Move coordinates private chauffeurs, villas, yachts, restaurant and VIP reservations, private aviation support, security, chefs and staffing through one local contact. You can request one service or a connected itinerary. Each service, availability, price and supplier terms are agreed separately before confirmation.'),
        2: ('Can you support personal assistants and family offices in Ibiza?',
            'Yes. Our Private Office provides one local point of contact for personal assistants, family offices and travel advisors arranging an Ibiza stay. Share dates, guests, accommodation area, required services, reply time zone and who may approve changes. We coordinate confirmed bookings and itinerary updates through the agreed communication channel.'),
    },
}
ES_CONCIERGE = '/es/concierge-privado-ibiza/'
ES_CONCIERGE_ITEMS = [
    ('¿Qué incluye un servicio de concierge de lujo en Ibiza?',
     'Ibiza VIP Move coordina chóferes privados, villas, yates, reservas de restaurantes y experiencias VIP, apoyo de aviación privada, seguridad, chefs y personal mediante un contacto local. Puedes solicitar un servicio o un itinerario completo. Cada servicio, disponibilidad, precio y condiciones del proveedor se acuerdan por separado antes de confirmar.'),
    ('¿Puedo contratar el concierge para una sola reserva?',
     'Sí. Puedes solicitar una reserva concreta o coordinar varios servicios de tu estancia. Comparte fechas, número de personas y lo que necesitas; confirmamos el alcance y las condiciones aplicables antes de reservar.'),
    ('¿Trabajáis con asistentes personales y family offices en Ibiza?',
     'Sí. Nuestro Private Office ofrece un punto de contacto local para asistentes personales, family offices y asesores de viajes que organizan una estancia en Ibiza. Indica fechas, huéspedes, zona del alojamiento, servicios, zona horaria de respuesta y quién autoriza los cambios. Coordinamos reservas confirmadas y actualizaciones por el canal acordado.'),
    ('¿Están garantizadas las reservas y el acceso VIP?',
     'La disponibilidad, depósitos, consumo mínimo, condiciones de acceso y términos de cada proveedor se comprueban antes de confirmar. Una solicitud de reserva no equivale a una reserva confirmada.'),
]
ROUTES = tuple(UPDATES) + (ES_CONCIERGE,)


def require(condition, message):
    if not condition:
        raise ValueError('Customer questions: ' + message)


def text(value):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', ' ', value))).strip()


def script(node):
    return '<script type="application/ld+json">' + json.dumps(node, ensure_ascii=False).replace('<', '\\u003c') + '</script>'


def transform(html, route):
    canonical = BASE + route
    lang = 'es' if route.startswith('/es/') else 'en'
    require(html.count(f'<link rel="canonical" href="{canonical}">') == 1, 'canonical mismatch: ' + route)
    require(html.count('</head>') == 1 and html.count('</main>') == 1, 'page landmarks: ' + route)
    nodes = [json.loads(m.group(1)) for m in SCRIPT.finditer(html)]
    webpages = [n for n in nodes if n.get('@type') == 'WebPage']
    services = [n for n in nodes if n.get('@type') == 'Service']
    faqs = [n for n in nodes if n.get('@type') == 'FAQPage']
    require(len(webpages) == 1, 'expected one WebPage: ' + route)
    require(webpages[0].get('url') == canonical, 'WebPage URL mismatch: ' + route)
    is_new = route == ES_CONCIERGE
    section_re = CONCIERGE_SECTION if 'concierge-privado' in route or route == '/private-concierge-ibiza/' else CORE_SECTION
    sections = list(section_re.finditer(html))
    if is_new and not sections:
        require(not faqs and not services, 'unexpected Spanish concierge entities')
        items = ES_CONCIERGE_ITEMS
        section = '<section class="faq" id="faq"><div class="section-head"><div class="kicker dark">Preguntas frecuentes</div><h2>Cómo organizar tu estancia en Ibiza.</h2></div>ITEMS</section>'
    else:
        require(len(sections) == 1 and len(faqs) == 1, 'expected one FAQ section and entity: ' + route)
        section = sections[0].group(0)
        details = list(DETAIL.finditer(section))
        require(len(details) == 4, 'expected four visible answers: ' + route)
        items = []
        for item in details:
            q = re.search(r'<summary\b[^>]*>(.*?)</summary>', item.group(0), re.S | re.I)
            a = re.search(r'<p\b[^>]*>(.*?)</p>', item.group(0), re.S | re.I)
            require(q is not None and a is not None, 'malformed visible answer: ' + route)
            items.append((text(q.group(1)), text(a.group(1))))
        recorded = [(q['name'], q['acceptedAnswer']['text']) for q in faqs[0].get('mainEntity', [])]
        require(items == recorded, 'pre-existing FAQ text/schema mismatch: ' + route)
        for position, replacement in UPDATES.get(route, {}).items():
            items[position] = replacement
        if is_new:
            require(items == ES_CONCIERGE_ITEMS, 'Spanish concierge content drift')
        # Retain the existing section heading, structure, classes and explanatory text.
        section = section[:details[0].start()] + 'ITEMS' + section[details[-1].end():]
        if 'id="faq"' not in section:
            section = section.replace('<section ', '<section id="faq" ', 1)

    details_html = ''.join(
        f'<details id="faq-question-{i}"><summary>{escape(q)}</summary><p id="faq-answer-{i}">{escape(a)}</p></details>'
        for i, (q, a) in enumerate(items, 1)
    )
    section = section.replace('ITEMS', details_html, 1)
    if sections:
        html = html[:sections[0].start()] + section + html[sections[0].end():]
    else:
        anchor = '<section class="closing-simple">'
        require(html.count(anchor) == 1, 'Spanish concierge insertion point')
        html = html.replace(anchor, section + anchor, 1)

    webpage = deepcopy(webpages[0])
    webpage.setdefault('@id', canonical + '#webpage')
    webpage['isPartOf'] = {'@id': BASE + '/#website'}
    if services:
        require(len(services) == 1, 'expected one Service: ' + route)
        service = deepcopy(services[0])
        require(service.get('url') == canonical and service.get('provider') == {'@id': ORG}, 'service identity drift: ' + route)
    else:
        require(is_new, 'service missing: ' + route)
        service = {'@context': 'https://schema.org', '@type': 'Service',
                   'name': 'Concierge privado en Ibiza', 'url': canonical,
                   'description': webpage['description'], 'provider': {'@id': ORG},
                   'areaServed': {'@type': 'Place', 'name': 'Ibiza, Spain'}}
    service.setdefault('@id', canonical + '#service')
    service['mainEntityOfPage'] = {'@id': webpage['@id']}
    webpage['mainEntity'] = {'@id': service['@id']}
    faq_id = faqs[0].get('@id', canonical + '#faq') if faqs else canonical + '#faq'
    existing_parts = webpage.get('hasPart', [])
    if isinstance(existing_parts, dict):
        existing_parts = [existing_parts]
    webpage['hasPart'] = [p for p in existing_parts if p.get('@id') != faq_id] + [{'@id': faq_id}]
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': faq_id,
           'url': canonical + '#faq', 'inLanguage': lang, 'isPartOf': {'@id': webpage['@id']},
           'about': {'@id': service['@id']}, 'publisher': {'@id': ORG},
           'mainEntity': [
               {'@type': 'Question', '@id': canonical + f'#faq-question-{i}', 'name': q,
                'acceptedAnswer': {'@type': 'Answer', '@id': canonical + f'#faq-answer-{i}', 'text': a}}
               for i, (q, a) in enumerate(items, 1)]}
    replacements = {'WebPage': webpage, 'Service': service, 'FAQPage': faq}
    found = set()
    def replace_schema(match):
        node = json.loads(match.group(1))
        kind = node.get('@type')
        if kind in replacements:
            found.add(kind)
            return script(replacements[kind])
        return match.group(0)
    html = SCRIPT.sub(replace_schema, html)
    missing = ''.join(script(replacements[k]) for k in ('Service', 'FAQPage') if k not in found)
    if missing:
        html = html.replace('</head>', missing + '</head>', 1)
    return html


def enhance(root=Path('_site')):
    pending = []
    for route in ROUTES:
        path = root / route.strip('/') / 'index.html'
        original = path.read_text(encoding='utf-8')
        updated = transform(original, route)
        # Metadata outside the JSON-LD, contacts, original H1 and assets stay untouched.
        require(SCRIPT.sub('', original.split('</head>')[0]) == SCRIPT.sub('', updated.split('</head>')[0]), 'unrelated head change: ' + route)
        for pattern in (r'<h1\b.*?</h1>', r'<a\b[^>]*>', r'<img\b[^>]*>', r'<script\b(?!\s+type="application/ld\+json")[^>]*>.*?</script>'):
            require(re.findall(pattern, original, re.S | re.I) == re.findall(pattern, updated, re.S | re.I), 'unrelated element change: ' + route)
        pending.append((path, updated))
    sitemap_path = root / 'sitemap.xml'
    sitemap = sitemap_path.read_text(encoding='utf-8')
    for route in ROUTES:
        pattern = rf'(<url>\s*<loc>{re.escape(BASE + route)}</loc>\s*<lastmod>)[^<]+(</lastmod>)'
        sitemap, count = re.subn(pattern, rf'\g<1>{LASTMOD}\g<2>', sitemap)
        require(count == 1, 'expected one existing sitemap entry: ' + route)
    # Complete all preconditions before writing any output.
    for path, updated in pending:
        path.write_text(updated, encoding='utf-8')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print('PASS: Customer questions — 12 existing EN/ES pages; visible answers, stable IDs and connected entities; existing contacts preserved')


if __name__ == '__main__':
    enhance()
