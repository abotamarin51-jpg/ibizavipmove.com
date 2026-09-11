from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
PHONE = '+34 600 703 303'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'
INSTAGRAM = 'https://www.instagram.com/ibizavipmove/'
TEMPLATE = ROOT / 'private-concierge-ibiza' / 'index.html'

PAGES = [
    {
        'slug': 'private-concierge-marina-botafoch-ibiza',
        'title': 'Private Concierge Marina Botafoch Ibiza | Ibiza VIP Move',
        'description': 'Private concierge for Marina Botafoch, Ibiza Town and Talamanca, coordinating chauffeur transport, yachts, dining, nightlife, villas and private client logistics.',
        'kicker': 'Marina Botafoch · Ibiza Town · Talamanca',
        'h1': 'Private concierge around<br><em>Marina Botafoch.</em>',
        'hero': 'nightlife.jpg',
        'service_type': 'Private concierge Marina Botafoch Ibiza',
        'areas': ['Marina Botafoch, Ibiza', 'Ibiza Town, Ibiza', 'Talamanca, Ibiza', 'Cap Martinet, Ibiza'],
        'lead_title': 'One operating brief across marina, city, hotel and nightlife movements.',
        'lead': 'Marina Botafoch and Ibiza Town often combine several types of movement in the same day: hotel or villa departures, marina handovers, restaurant reservations, nightlife arrivals and late returns. Ibiza VIP Move keeps confirmed transport, hospitality and concierge requests aligned around one itinerary.',
        'detail': 'The purpose of a local concierge brief here is not simply to book individual services. It is to reduce friction between timings, guest movements, luggage, marina access, reservations and changing plans, using one Ibiza-based point of contact.',
        'use_cases': [
            ('Marina handovers', 'Chauffeur, yacht departure or return, luggage and onward reservations can be aligned around the same confirmed timing.'),
            ('Dining & nightlife', 'Restaurant, club and late-night transport requests can be coordinated with guest location and return plans.'),
            ('Hotels & private stays', 'Movements between Ibiza Town, Talamanca, Marina Botafoch and nearby private accommodation can remain under one brief.'),
            ('Professional guests', 'PAs, travel advisors and private offices can define the preferred client-facing or behind-the-scenes workflow.'),
        ],
        'faqs': [
            ('Can you coordinate a yacht day from Marina Botafoch with chauffeur transport?', 'Yes. Confirmed pickup, marina timing, luggage or day bags, yacht departure and post-charter movements can be aligned under one itinerary.'),
            ('Can dinner and nightlife transport be planned together?', 'Yes. Restaurant arrival, venue timing, waiting requirements and return transport can be coordinated around the confirmed plan and current availability.'),
            ('Do you support guests staying around Talamanca or Cap Martinet?', 'Yes. Requests in and around Marina Botafoch, Ibiza Town, Talamanca and Cap Martinet can be coordinated as part of the wider Ibiza stay.'),
            ('Is VIP access guaranteed?', 'No. Restaurants, clubs, tables and special access remain subject to venue availability, conditions and written confirmation.'),
        ],
        'related': [
            ('Private Concierge Ibiza', '/private-concierge-ibiza/'),
            ('Yacht Charter Ibiza', '/yacht-charter-ibiza/'),
            ('VIP Services Ibiza', '/vip-services-ibiza/'),
        ],
    },
    {
        'slug': 'private-concierge-cala-jondal-es-cubells-ibiza',
        'title': 'Private Concierge Cala Jondal & Es Cubells Ibiza | Ibiza VIP Move',
        'description': 'Private concierge for Cala Jondal, Es Cubells and the south of Ibiza, connecting villas, chauffeur transport, beach clubs, yachts, dining, staffing and security.',
        'kicker': 'Cala Jondal · Es Cubells · South Ibiza',
        'h1': 'South Ibiza,<br><em>coordinated privately.</em>',
        'hero': 'villa.jpg',
        'service_type': 'Private concierge Cala Jondal and Es Cubells Ibiza',
        'areas': ['Cala Jondal, Ibiza', 'Es Cubells, Ibiza', 'Porroig, Ibiza', 'Sant Josep de sa Talaia, Ibiza'],
        'lead_title': 'Villa, beach, marina and dining plans connected across the south.',
        'lead': 'Cala Jondal, Es Cubells, Porroig and the wider Sant Josep area attract private villa stays where transport, guest access, beach plans, dining, staffing and sea days often depend on one another. Ibiza VIP Move coordinates those confirmed elements around a single operating brief.',
        'detail': 'For private houses and multi-day stays, the useful layer is continuity: airport arrival, villa access, chauffeur capacity, beach club timing, yacht plans, chefs, wellness or security can be reviewed together instead of through disconnected supplier conversations.',
        'use_cases': [
            ('Villa arrivals', 'Airport timing, luggage, vehicle capacity, property access and guest arrival can be aligned before the movement begins.'),
            ('Beach & dining days', 'Cala Jondal plans can be connected with chauffeur timing, restaurant bookings and later evening movements.'),
            ('Private-house support', 'Chefs, staffing, wellness and selected security requirements can be coordinated around the confirmed villa schedule.'),
            ('Sea connections', 'Yacht and marina movements can be integrated with the same south-Ibiza transport and hospitality brief.'),
        ],
        'faqs': [
            ('Can you coordinate a villa stay in Es Cubells with daily chauffeur service?', 'Yes. Confirmed pickup windows, guest movements, restaurants, beach plans and other stops can be coordinated around the villa itinerary.'),
            ('Do you support Cala Jondal beach club days?', 'Yes. Transport and surrounding confirmed reservations can be coordinated around the requested Cala Jondal schedule, subject to venue availability and terms.'),
            ('Can private chefs, wellness or security be arranged for a villa?', 'These requests can be assessed and coordinated with suitable independent providers, subject to availability, scope and confirmation.'),
            ('Can the same brief include airport, yacht and villa logistics?', 'Yes. Those movements can be treated as connected dependencies so timing, luggage and vehicle requirements stay aligned.'),
        ],
        'related': [
            ('Luxury Villas Ibiza', '/luxury-villas-ibiza/'),
            ('Luxury Lifestyle Management', '/luxury-lifestyle-management-ibiza/'),
            ('Private Chauffeur Ibiza', '/private-chauffeur-ibiza/'),
        ],
    },
    {
        'slug': 'private-concierge-santa-eulalia-roca-llisa-ibiza',
        'title': 'Private Concierge Santa Eulalia & Roca Llisa Ibiza | Ibiza VIP Move',
        'description': 'Private concierge for Santa Eulalia, Roca Llisa and east Ibiza, coordinating villas, family stays, chauffeur transport, dining, yachts, wellness and private support.',
        'kicker': 'Santa Eulària · Roca Llisa · East Ibiza',
        'h1': 'East Ibiza,<br><em>handled through one contact.</em>',
        'hero': 'hero.jpg',
        'service_type': 'Private concierge Santa Eulalia and Roca Llisa Ibiza',
        'areas': ['Santa Eulària des Riu, Ibiza', 'Roca Llisa, Ibiza', 'Cala Llonga, Ibiza', 'Siesta, Ibiza'],
        'lead_title': 'Private-stay coordination for the east coast and family itineraries.',
        'lead': 'Santa Eulària, Roca Llisa, Cala Llonga and nearby east-coast stays often involve a different rhythm from central nightlife: villa logistics, family schedules, marina movements, dining, wellness and day trips. Ibiza VIP Move keeps those confirmed elements connected through one Ibiza-based contact.',
        'detail': 'The local value is continuity. A chauffeur schedule can be coordinated with children or family timing, villa access, restaurant plans, yacht movements, wellness appointments and other private requests without forcing the client to manage every supplier separately.',
        'use_cases': [
            ('Family stays', 'Guest numbers, child-related timing, luggage and multiple daily movements can be kept visible within one operating brief.'),
            ('Villa logistics', 'Arrival, housekeeping-related access, chefs, wellness and transport can be aligned around confirmed property timings.'),
            ('Marina & yacht days', 'Ground movements to and from confirmed sea plans can be integrated with the wider itinerary.'),
            ('Multi-day support', 'The same private contact can continue coordinating new requests as the stay develops.'),
        ],
        'faqs': [
            ('Do you provide concierge support for private villas around Roca Llisa?', 'Yes. Villa-related transport, staffing, dining, wellness, yacht and other confirmed private requests can be coordinated around the stay.'),
            ('Can you support family itineraries in Santa Eulalia?', 'Yes. Passenger numbers, timing, multiple stops and family-specific practical requirements can be included in the operating brief.'),
            ('Can the concierge coordinate both east-coast plans and Ibiza Town evenings?', 'Yes. Confirmed movements can connect east-coast accommodation with dining, marina or nightlife plans elsewhere on the island.'),
            ('Do you operate from a public concierge desk in Santa Eulalia?', 'No. Ibiza VIP Move works as a private on-island coordination service, with services arranged at villas, hotels, marinas, the airport and other agreed locations.'),
        ],
        'related': [
            ('Personal Concierge Ibiza', '/personal-concierge-ibiza/'),
            ('Luxury Travel Concierge', '/luxury-travel-concierge-ibiza/'),
            ('Wellness Ibiza', '/wellness-ibiza/'),
        ],
    },
    {
        'slug': 'private-concierge-santa-gertrudis-ibiza',
        'title': 'Private Concierge Santa Gertrudis Ibiza | Central Ibiza Villas',
        'description': 'Private concierge for Santa Gertrudis and central Ibiza villas, coordinating chauffeur transport, private chefs, family logistics, wellness, dining, yachts and bespoke support.',
        'kicker': 'Santa Gertrudis · Central Ibiza',
        'h1': 'Central Ibiza villas,<br><em>kept connected.</em>',
        'hero': 'events.jpg',
        'service_type': 'Private concierge Santa Gertrudis Ibiza',
        'areas': ['Santa Gertrudis de Fruitera, Ibiza', 'Central Ibiza, Ibiza', 'Sant Llorenç de Balàfia, Ibiza', 'San Rafael, Ibiza'],
        'lead_title': 'A private operating layer for countryside and central-island stays.',
        'lead': 'Santa Gertrudis and central Ibiza are often chosen for private houses, countryside stays and family or group itineraries that move in several directions across the island. Ibiza VIP Move coordinates confirmed transport, chefs, wellness, dining, sea days and other requests through one operational point of contact.',
        'detail': 'Central positioning can simplify some plans but it can also create multiple daily routes. Keeping airport arrivals, villa timing, restaurants, beach plans, marina movements and staff requirements on one brief helps prevent each supplier from working with a different version of the schedule.',
        'use_cases': [
            ('Countryside villas', 'Guest arrivals, access windows, transport and in-villa services can be aligned around the confirmed stay.'),
            ('Private chefs & staffing', 'Chef, waiter, housekeeping or other staffing requests can be coordinated for confirmed dates and scope.'),
            ('Island-wide movements', 'Central-villa departures can connect to south-coast beaches, marinas, Ibiza Town or east-coast plans under one chauffeur brief.'),
            ('Family & group support', 'Multiple guests, vehicles, luggage and changing daily schedules can be handled against the same itinerary.'),
        ],
        'faqs': [
            ('Can you support private villas around Santa Gertrudis?', 'Yes. Confirmed chauffeur, chef, staffing, wellness, dining, yacht and other concierge requests can be coordinated around central-Ibiza stays.'),
            ('Can one chauffeur plan cover several parts of the island in a day?', 'Yes. Multiple confirmed stops can be planned under one itinerary, with timing reviewed when the schedule changes.'),
            ('Can you coordinate private chefs and villa staffing?', 'Yes. Suitable independent providers can be sourced and coordinated subject to dates, scope, availability and confirmation.'),
            ('Is Santa Gertrudis support only for families?', 'No. The service can support couples, private groups, principals, families, PAs and professional travel partners depending on the brief.'),
        ],
        'related': [
            ('Private Client Services', '/private-client-services-ibiza/'),
            ('Private Chef & Staffing', '/private-chef-staffing-ibiza/'),
            ('Luxury Villas Ibiza', '/luxury-villas-ibiza/'),
        ],
    },
]


def page_path(slug):
    return ROOT / slug / 'index.html'


def remove_meta(html, key):
    pattern = r'<meta\b(?=[^>]*(?:name|property)=["\']' + re.escape(key) + r'["\'])[^>]*>\s*'
    return re.sub(pattern, '', html, flags=re.I)


def area_objects(names):
    return [
        {
            '@type': 'Place',
            'name': name,
            'containedInPlace': {
                '@type': 'AdministrativeArea',
                'name': 'Ibiza, Balearic Islands, Spain',
            },
        }
        for name in names
    ]


def schema_for(data):
    url = f"{BASE}/{data['slug']}/"
    areas = area_objects(data['areas'])
    organization = {
        '@type': 'Organization',
        '@id': ORG,
        'name': 'Ibiza VIP Move',
        'url': BASE + '/',
        'telephone': PHONE,
        'email': EMAIL,
        'founder': {'@id': FOUNDER},
        'sameAs': [INSTAGRAM],
        'areaServed': areas,
    }
    service = {
        '@type': 'Service',
        '@id': url + '#service',
        'name': data['service_type'],
        'url': url,
        'description': data['description'],
        'provider': {'@id': ORG},
        'areaServed': areas,
        'spatialCoverage': areas,
        'serviceType': 'Private concierge and luxury lifestyle coordination',
    }
    webpage = {
        '@type': 'WebPage',
        '@id': url + '#webpage',
        'url': url,
        'name': data['title'],
        'description': data['description'],
        'about': {'@id': url + '#service'},
        'inLanguage': 'en',
    }
    breadcrumb = {
        '@type': 'BreadcrumbList',
        '@id': url + '#breadcrumb',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ibiza VIP Move', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Private Concierge Ibiza', 'item': BASE + '/private-concierge-ibiza/'},
            {'@type': 'ListItem', 'position': 3, 'name': data['service_type'], 'item': url},
        ],
    }
    faq = {
        '@type': 'FAQPage',
        '@id': url + '#faq',
        'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
            for q, a in data['faqs']
        ],
    }
    return {'@context': 'https://schema.org', '@graph': [organization, service, webpage, breadcrumb, faq]}


def render_body(data):
    use_cases = ''.join(
        f'<div><b>{escape(title)}</b><p>{escape(text)}</p></div>'
        for title, text in data['use_cases']
    )
    faqs = ''.join(
        f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
        for q, a in data['faqs']
    )
    areas = ' · '.join(escape(x) for x in data['areas'])
    related = ' · '.join(
        f'<a class="text-link" href="{escape(url, quote=True)}">{escape(label)}</a>'
        for label, url in data['related']
    )
    wa_text = escape(data['service_type'], quote=True).replace(' ', '%20')
    return f'''<section class="page-hero service-hero" style="--hero:url('/assets/images/{escape(data["hero"], quote=True)}')"><div><div class="kicker light">{data["kicker"]}</div><h1>{data["h1"]}</h1><p>{escape(data["description"])}</p><div class="hero-actions"><a class="btn gold" href="{WA}?text=Hello%20Ibiza%20VIP%20Move%2C%20I%20would%20like%20private%20support%20for%20{wa_text}.">Start a private brief</a><a class="btn ghost" href="/private-concierge-ibiza/">Ibiza Concierge</a></div></div></section>
<section class="editorial"><div><div class="kicker dark">Local Ibiza coverage</div><h2>{escape(data["lead_title"])}</h2></div><div><p class="large">{escape(data["lead"])}</p><p>{escape(data["detail"])}</p><p><strong>Areas referenced in this brief:</strong> {areas}</p><a class="text-link" href="/contact/">Request private support →</a></div></section>
<section class="dark-panel"><div class="kicker light">Local operating use cases</div><h2>One local brief.<br>Fewer disconnected handovers.</h2><div class="trust-grid">{use_cases}</div></section>
<section class="process"><div class="section-head"><div class="kicker dark">How local coordination works</div><h2>Dates, guests, location, priorities.</h2><p>Share the confirmed accommodation or main pickup area, guest count and first priorities. Availability, scope and supplier terms are checked before anything is treated as confirmed.</p></div><div class="process-grid"><article><span>01</span><h3>Location</h3><p>Confirm the villa, hotel, marina or main operating area.</p></article><article><span>02</span><h3>Guests</h3><p>Passenger count, luggage and relevant privacy or family requirements.</p></article><article><span>03</span><h3>Schedule</h3><p>Fixed timings and flexible requests are separated before confirmation.</p></article><article><span>04</span><h3>Coordinate</h3><p>Confirmed services are kept aligned around the same itinerary.</p></article></div></section>
<section class="faq"><div class="section-head"><div class="kicker dark">Local concierge FAQ</div><h2>Questions that define the brief.</h2></div>{faqs}</section>
<section class="partners-strip"><div><div class="kicker dark">Related private support</div><h2>Connect the local brief to the right service.</h2><p>{related}</p></div><a class="btn dark" href="{WA}">WhatsApp Concierge</a></section>
<section class="closing-simple"><h2>Need a private Ibiza contact for this area?</h2><p>Send the dates, guest count, accommodation or main location and the first requirement.</p><a class="btn dark" href="/contact/">Start your brief</a></section>'''


def build_page(template, data):
    html = template
    html = re.sub(r'<title>.*?</title>\s*', '', html, count=1, flags=re.I | re.S)
    html = re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>\s*', '', html, flags=re.I)
    html = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>\s*', '', html, flags=re.I)
    for key in ('description','og:type','og:title','og:description','og:url','og:image','twitter:card','twitter:title','twitter:description','twitter:image'):
        html = remove_meta(html, key)
    html = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>\s*', '', html, flags=re.I | re.S)
    url = f"{BASE}/{data['slug']}/"
    meta = (
        f'<title>{escape(data["title"])}</title>'
        f'<meta name="description" content="{escape(data["description"], quote=True)}">'
        '<meta name="robots" content="index,follow,max-image-preview:large">'
        f'<link rel="canonical" href="{url}">'
        f'<link rel="alternate" hreflang="en" href="{url}">'
        f'<link rel="alternate" hreflang="x-default" href="{url}">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{escape(data["title"], quote=True)}">'
        f'<meta property="og:description" content="{escape(data["description"], quote=True)}">'
        f'<meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{BASE}/assets/images/{escape(data["hero"], quote=True)}">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{escape(data["title"], quote=True)}">'
        f'<meta name="twitter:description" content="{escape(data["description"], quote=True)}">'
        f'<script type="application/ld+json">{json.dumps(schema_for(data), ensure_ascii=False, separators=(",", ":"))}</script>'
    )
    if '</head>' not in html:
        raise SystemExit(f'Phase 103 template missing head close: {data["slug"]}')
    html = html.replace('</head>', meta + '</head>', 1)
    body = render_body(data)
    html, count = re.subn(r'<main\b[^>]*>.*?</main>', '<main id="main-content">' + body + '</main>', html, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit(f'Phase 103 main replacement failed: {data["slug"]}')
    return html


def add_cluster(path, title, links):
    target = ROOT / path.strip('/') / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 103 hub missing: {path}')
    html = target.read_text(encoding='utf-8')
    marker = 'ivm-local-luxury-areas'
    if marker in html:
        return
    link_html = ' · '.join(f'<a class="text-link" href="{url}">{escape(label)}</a>' for label, url in links)
    section = f'<section class="partners-strip {marker}"><div><div class="kicker dark">Private concierge by Ibiza area</div><h2>{escape(title)}</h2><p>{link_html}</p></div><a class="btn dark" href="/contact/">Private brief</a></section>'
    if '</main>' not in html:
        raise SystemExit(f'Phase 103 hub missing main close: {path}')
    target.write_text(html.replace('</main>', section + '</main>', 1), encoding='utf-8')


if not TEMPLATE.exists():
    raise SystemExit('Phase 103 private-concierge template missing')
template = TEMPLATE.read_text(encoding='utf-8')
for data in PAGES:
    target = page_path(data['slug'])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_page(template, data), encoding='utf-8')
    print(f'Phase 103 created /{data["slug"]}/')

location_links = [
    ('Marina Botafoch & Ibiza Town', '/private-concierge-marina-botafoch-ibiza/'),
    ('Cala Jondal & Es Cubells', '/private-concierge-cala-jondal-es-cubells-ibiza/'),
    ('Santa Eulalia & Roca Llisa', '/private-concierge-santa-eulalia-roca-llisa-ibiza/'),
    ('Santa Gertrudis & Central Ibiza', '/private-concierge-santa-gertrudis-ibiza/'),
]
add_cluster('/private-concierge-ibiza/', 'Choose the local area closest to the stay.', location_links)
add_cluster('/luxury-lifestyle-management-ibiza/', 'Local lifestyle coordination across high-value Ibiza stays.', location_links)
add_cluster('/private-client-services-ibiza/', 'Local operating support for principals, PAs and private offices.', location_links)
add_cluster('/luxury-villas-ibiza/', 'Private villa support by Ibiza area.', location_links)

sitemap_path = ROOT / 'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
entries = []
for data in PAGES:
    url = f"{BASE}/{data['slug']}/"
    if url not in sitemap:
        entries.append(f'  <url><loc>{url}</loc></url>')
if entries:
    sitemap = sitemap.replace('</urlset>', '\n' + '\n'.join(entries) + '\n</urlset>', 1)
    sitemap_path.write_text(sitemap, encoding='utf-8')

llms_path = ROOT / 'llms.txt'
llms = llms_path.read_text(encoding='utf-8')
marker = '## Local private concierge areas'
if marker not in llms:
    llms += '\n\n' + marker + '\n'
    for data in PAGES:
        llms += f"- {data['service_type']}: {BASE}/{data['slug']}/ — Service areas: {', '.join(data['areas'])}.\n"
    llms_path.write_text(llms, encoding='utf-8')

print('PASS: Phase 103 local luxury areas — four distinct Ibiza area pages, Place-based GEO signals, internal links, sitemap and AI discovery added')
