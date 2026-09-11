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
        'slug': 'luxury-lifestyle-management-ibiza',
        'title': 'Luxury Lifestyle Management Ibiza | Ibiza VIP Move',
        'description': 'Luxury lifestyle management in Ibiza for private clients who want chauffeur, villas, yachts, dining, wellness, security and changing plans coordinated through one trusted contact.',
        'kicker': 'Luxury Lifestyle Management · Ibiza',
        'h1': 'Your Ibiza lifestyle,<br><em>managed as one.</em>',
        'hero': 'villa.jpg',
        'lead_title': 'Full-stay lifestyle management, not a list of separate bookings.',
        'lead': 'Ibiza VIP Move coordinates the moving parts of a private stay around one brief: arrival, chauffeur transport, villas, yachts, dining, nightlife, wellness, staffing, security and last-minute requests.',
        'detail': 'Lifestyle management is most valuable when several services depend on each other. We keep confirmed timings, suppliers and changes aligned through one Ibiza-based point of contact.',
        'service_type': 'Luxury lifestyle management in Ibiza',
        'alternate': ['Lifestyle management Ibiza', 'Private lifestyle services Ibiza', 'Luxury concierge management Ibiza'],
        'audience': 'Private clients, couples, families, principals and personal assistants',
        'pillars': [
            ('Full-stay view', 'Confirmed services are coordinated around the same itinerary rather than handled as isolated bookings.'),
            ('One private contact', 'A single Ibiza-based line of communication reduces fragmented supplier conversations.'),
            ('Lifestyle network', 'Mobility, stays, sea, dining, wellness, staffing and protection can be connected around the brief.'),
            ('Responsive changes', 'When plans move, affected confirmed elements are reviewed against the updated itinerary.'),
        ],
        'process': [
            ('01', 'Define the stay', 'Dates, guests, priorities, privacy and the level of support are clarified first.'),
            ('02', 'Map dependencies', 'Flights, villa access, vehicles, marina times, reservations and staffing are aligned.'),
            ('03', 'Confirm', 'Availability, scope, timing and applicable terms are agreed before each service is treated as confirmed.'),
            ('04', 'Coordinate', 'The confirmed itinerary is kept connected as the stay develops.'),
        ],
        'faqs': [
            ('What is luxury lifestyle management in Ibiza?', 'It is the coordination of multiple private services around one stay and one operating brief, rather than managing transport, villas, yachts, dining and other requests separately.'),
            ('How is lifestyle management different from a single concierge booking?', 'A single booking solves one request. Lifestyle management is designed for several connected requirements and changing schedules across a stay.'),
            ('Can a personal assistant or family office brief Ibiza VIP Move?', 'Yes. A principal, PA, family office or professional representative can share the operating brief and preferred communication structure before the stay.'),
            ('Can lifestyle management include chauffeur, villa and yacht arrangements together?', 'Yes. Confirmed chauffeur, villa, yacht, dining, security, staffing, wellness and other requests can be coordinated around the same itinerary.'),
        ],
        'related': [
            ('Private Concierge Ibiza', '/private-concierge-ibiza/'),
            ('Private Client Services Ibiza', '/private-client-services-ibiza/'),
            ('Luxury Travel Concierge Ibiza', '/luxury-travel-concierge-ibiza/'),
        ],
    },
    {
        'slug': 'personal-concierge-ibiza',
        'title': 'Personal Concierge Ibiza | Dedicated Private Assistance',
        'description': 'Personal concierge in Ibiza for individuals, couples and families seeking one dedicated contact for reservations, transport, villas, yachts, experiences and day-to-day private assistance.',
        'kicker': 'Personal Concierge · Ibiza',
        'h1': 'A personal Ibiza concierge,<br><em>built around you.</em>',
        'hero': 'hero.jpg',
        'lead_title': 'Dedicated assistance for the details that shape your stay.',
        'lead': 'A personal concierge is for clients who want one trusted contact who understands the dates, preferences and practical details behind the trip—not a different conversation for every request.',
        'detail': 'From airport arrival and restaurant planning to a yacht day, villa support, chauffeur movements or an unexpected change, requests can be coordinated around the same client context.',
        'service_type': 'Personal concierge service in Ibiza',
        'alternate': ['Personal concierge Ibiza', 'Personal assistant Ibiza travel', 'Dedicated concierge Ibiza'],
        'audience': 'Individuals, couples, families and private leisure travellers',
        'pillars': [
            ('Personal brief', 'Preferences, pace, priorities and practical requirements are kept connected to the same stay.'),
            ('Everyday support', 'Reservations, transport and lifestyle requests can be handled without restarting the brief each time.'),
            ('Ibiza based', 'Local coordination supports faster communication when timings or requirements change.'),
            ('Private handling', 'Only the operational details needed for a confirmed request are shared with the relevant supplier.'),
        ],
        'process': [
            ('01', 'Tell us the essentials', 'Dates, guests, accommodation and the first priorities are enough to begin.'),
            ('02', 'Build the context', 'We clarify preferences, timings and dependencies that matter to the requests.'),
            ('03', 'Confirm services', 'Each service is subject to availability, scope and written confirmation.'),
            ('04', 'Stay connected', 'Further requests can be handled against the same Ibiza brief as the stay evolves.'),
        ],
        'faqs': [
            ('What can a personal concierge in Ibiza help with?', 'Requests can include private transport, dining, beach clubs, yachts, villa support, wellness, staffing, security and other practical or lifestyle needs, subject to availability and confirmation.'),
            ('Can I use the concierge for only one or two requests?', 'Yes. The service can begin with a specific request and expand only if additional coordination is useful.'),
            ('Can the same contact help before and during the trip?', 'Yes. Pre-arrival planning and on-island coordination can remain connected through the same private communication line.'),
            ('Is access to restaurants or clubs guaranteed?', 'No. Availability and access depend on the venue, date, party profile and applicable terms. No reservation or access is treated as confirmed until it is agreed in writing.'),
        ],
        'related': [
            ('Luxury Lifestyle Management Ibiza', '/luxury-lifestyle-management-ibiza/'),
            ('VIP Services Ibiza', '/vip-services-ibiza/'),
            ('Private Concierge Ibiza', '/private-concierge-ibiza/'),
        ],
    },
    {
        'slug': 'luxury-travel-concierge-ibiza',
        'title': 'Luxury Travel Concierge Ibiza | Private Trip Coordination',
        'description': 'Luxury travel concierge in Ibiza for pre-arrival planning and on-island coordination across chauffeur, villas, yachts, private aviation, dining, security and bespoke requests.',
        'kicker': 'Luxury Travel Concierge · Ibiza',
        'h1': 'The trip is connected<br><em>before you land.</em>',
        'hero': 'aviation.jpg',
        'lead_title': 'Pre-arrival planning and local execution under one Ibiza brief.',
        'lead': 'Luxury travel concierge support connects the itinerary before arrival: flights, ground transport, accommodation, marina movements, dining, experiences and the practical handovers between them.',
        'detail': 'The objective is not to over-plan every minute. It is to make sure confirmed services use the same timing, guest information and operating priorities so the trip feels simple to the client.',
        'service_type': 'Luxury travel concierge in Ibiza',
        'alternate': ['Luxury travel services Ibiza', 'Private travel management Ibiza', 'Bespoke travel Ibiza'],
        'audience': 'Luxury travellers, travel advisors, personal assistants and private offices',
        'pillars': [
            ('Pre-arrival', 'Important arrival, accommodation and transport details can be aligned before the client reaches Ibiza.'),
            ('Travel continuity', 'Flights, vehicle capacity, luggage, villa access and marina timings can be treated as connected dependencies.'),
            ('Local execution', 'An Ibiza-based contact supports the handover from international planning to on-island delivery.'),
            ('Professional briefs', 'Travel advisors and assistants can define the preferred client-facing or behind-the-scenes workflow.'),
        ],
        'process': [
            ('01', 'Receive the itinerary', 'Share confirmed travel details, guests, accommodation and priority requests.'),
            ('02', 'Identify gaps', 'We clarify timing, capacity, access and handover points that affect the client journey.'),
            ('03', 'Align confirmed services', 'Booked elements are consolidated around one operating timeline.'),
            ('04', 'Support the stay', 'New requests or timing changes are handled with awareness of the wider itinerary.'),
        ],
        'faqs': [
            ('When should I contact a luxury travel concierge for Ibiza?', 'The most useful time is before arrival, once core dates and accommodation are known, but support can also begin during an active stay.'),
            ('Can you coordinate private aviation arrivals with ground transport?', 'Yes. Flight timing, passenger count, luggage, onward destination and vehicle requirements can be aligned as one arrival brief.'),
            ('Do you work with luxury travel advisors?', 'Yes. Professional partners can send an active client brief and agree whether Ibiza VIP Move works client-facing or behind the scenes.'),
            ('Can the itinerary change after services are confirmed?', 'Yes, but changes remain subject to supplier availability and applicable terms. A revised timing may affect other confirmed elements, which are reviewed accordingly.'),
        ],
        'related': [
            ('International Clients', '/international-clients/'),
            ('Destination Management Ibiza', '/destination-management-ibiza/'),
            ('Private Chauffeur Ibiza', '/private-chauffeur-ibiza/'),
        ],
    },
    {
        'slug': 'vip-services-ibiza',
        'title': 'VIP Services Ibiza | Access, Transport & Private Hospitality',
        'description': 'VIP services in Ibiza combining private transport, dining and nightlife coordination, yachts, villas, security, hospitality support and bespoke requests through one private contact.',
        'kicker': 'VIP Services · Ibiza',
        'h1': 'VIP services in Ibiza,<br><em>without fragmented planning.</em>',
        'hero': 'nightlife.jpg',
        'lead_title': 'Private hospitality, access and mobility coordinated around the guest.',
        'lead': 'VIP services can involve far more than a table or a car. The quality of the experience depends on how transport, reservations, guest timing, security, accommodation and changing plans work together.',
        'detail': 'Ibiza VIP Move coordinates confirmed private services through one contact and keeps the practical handovers aligned. Venue access, tables and special requests always remain subject to actual availability and written confirmation.',
        'service_type': 'VIP services and private hospitality in Ibiza',
        'alternate': ['VIP hospitality Ibiza', 'VIP access Ibiza', 'Exclusive services Ibiza'],
        'audience': 'Private clients, VIP guests, executive groups and hospitality partners',
        'pillars': [
            ('Private mobility', 'Chauffeur and multi-vehicle movements can be planned around venues, villas, marinas and airport timings.'),
            ('Dining & nightlife', 'Restaurant, beach club and nightlife requests can be coordinated with the surrounding itinerary.'),
            ('Guest support', 'Hospitality logistics can be aligned for couples, families, executive groups and hosted guests.'),
            ('Protection', 'Licensed security requirements can be coordinated where relevant and confirmed for the specific brief.'),
        ],
        'process': [
            ('01', 'Guest profile', 'Dates, group size, priorities and the type of hospitality required are clarified.'),
            ('02', 'Availability', 'Venues, services and practical constraints are checked for the specific request.'),
            ('03', 'Operating plan', 'Confirmed times, transport and handovers are aligned around the guest schedule.'),
            ('04', 'Live support', 'Changes are coordinated against the confirmed itinerary and current availability.'),
        ],
        'faqs': [
            ('What do VIP services in Ibiza usually include?', 'They can include private chauffeur transport, restaurant and beach club coordination, nightlife requests, yachts, villas, security, staffing and other hospitality needs.'),
            ('Can you guarantee a VIP table or sold-out reservation?', 'No. Access depends on the venue, date, availability and applicable conditions. Nothing is represented as guaranteed until the venue or supplier confirms it.'),
            ('Can VIP transport and nightlife be coordinated together?', 'Yes. Pickup timing, venue arrival, waiting requirements and return movements can be planned around the confirmed booking.'),
            ('Do you support hospitality partners with VIP guests?', 'Yes. Hotels, travel professionals and other hospitality partners can send a guest brief and agree the preferred communication workflow.'),
        ],
        'related': [
            ('Restaurants & Nightlife Ibiza', '/restaurants-nightlife-ibiza/'),
            ('Private Security Ibiza', '/private-security-ibiza/'),
            ('Personal Concierge Ibiza', '/personal-concierge-ibiza/'),
        ],
    },
    {
        'slug': 'private-client-services-ibiza',
        'title': 'Private Client Services Ibiza | Principals, PAs & Family Offices',
        'description': 'Private client services in Ibiza for principals, families, PAs and family offices needing discreet local coordination across transport, villas, yachts, aviation, hospitality and security.',
        'kicker': 'Private Client Services · Ibiza',
        'h1': 'Local Ibiza support<br><em>behind the principal.</em>',
        'hero': 'chauffeur.jpg',
        'lead_title': 'A dependable on-island coordination layer for complex private stays.',
        'lead': 'Private client services are designed for briefs where discretion, communication structure and operational dependencies matter as much as the individual bookings themselves.',
        'detail': 'Ibiza VIP Move can act as the local coordination point for a principal, family, PA or family office, connecting confirmed mobility, hospitality, lifestyle and selected protection requirements without exposing more client information than operations require.',
        'service_type': 'Private client services in Ibiza',
        'alternate': ['UHNW concierge Ibiza', 'Family office support Ibiza', 'Principal support Ibiza'],
        'audience': 'Principals, families, personal assistants, executive assistants and family offices',
        'pillars': [
            ('Principal-led brief', 'Guest priorities, privacy, decision makers and authorized contacts are clarified at the start.'),
            ('Need-to-know handling', 'Operational information is shared only to the extent required for a confirmed service.'),
            ('Complex itineraries', 'Multiple vehicles, private aviation, villa access, yachts, security and staffing can be mapped together.'),
            ('Partner compatible', 'The operating role can be client-facing or discreetly behind a PA, family office or travel professional.'),
        ],
        'process': [
            ('01', 'Authority & contacts', 'Clarify who can approve changes and who should receive operational updates.'),
            ('02', 'Dependencies', 'Flights, accommodation access, mobility, reservations and protection requirements are mapped.'),
            ('03', 'Confirmations', 'Scope, availability, timings and supplier terms are documented before execution.'),
            ('04', 'Controlled changes', 'Updates are applied against the same brief so affected services remain aligned.'),
        ],
        'faqs': [
            ('Do you work directly with family offices and personal assistants?', 'Yes. A PA, EA, family office or other authorized representative can brief Ibiza VIP Move and define the preferred communication structure.'),
            ('How is private client information handled?', 'Only information needed to coordinate the requested and confirmed service should be shared with the relevant supplier. Client identities and itineraries are not used as marketing material without explicit authorization.'),
            ('Can you coordinate several vehicles and security for one principal?', 'Multi-vehicle and licensed security requirements can be assessed together with passenger, luggage, timing and route needs, subject to availability and confirmation.'),
            ('Can you work behind another concierge or travel company?', 'Yes. Professional partners can agree a behind-the-scenes operating role where appropriate to protect their client relationship.'),
        ],
        'related': [
            ('Private Office Ibiza', '/private-office/'),
            ('International Clients', '/international-clients/'),
            ('Destination Management Ibiza', '/destination-management-ibiza/'),
        ],
    },
    {
        'slug': 'destination-management-ibiza',
        'title': 'Luxury DMC & Destination Management Ibiza | Ibiza VIP Move',
        'description': 'Luxury destination management in Ibiza for travel advisors, concierge firms, private offices and hospitality partners needing one local operator for transport, villas, yachts and guest logistics.',
        'kicker': 'Luxury DMC · Destination Management · Ibiza',
        'h1': 'One Ibiza operator<br><em>behind the itinerary.</em>',
        'hero': 'events.jpg',
        'lead_title': 'Destination management for professional briefs and high-value private travel.',
        'lead': 'A luxury DMC in Ibiza should make local execution easier for the advisor or partner who owns the client relationship. Ibiza VIP Move provides one on-island coordination point across confirmed transport, villas, yachts, dining, private aviation, staffing, security and guest logistics.',
        'detail': 'The service is designed for luxury travel advisors, concierge companies, PAs, private offices and hospitality teams that need a reliable Ibiza handover rather than a collection of unrelated supplier introductions.',
        'service_type': 'Luxury destination management company services in Ibiza',
        'alternate': ['Luxury DMC Ibiza', 'Destination management Ibiza', 'Ibiza ground operator luxury travel'],
        'audience': 'Luxury travel advisors, concierge companies, DMC partners, private offices and hospitality teams',
        'pillars': [
            ('Local operator', 'One Ibiza contact can coordinate multiple confirmed local suppliers around the partner brief.'),
            ('B2B workflow', 'Client-facing, white-label-style or behind-the-scenes communication can be discussed before execution.'),
            ('Guest logistics', 'Arrival, luggage, vehicles, accommodation access, marina movements and reservations can be connected.'),
            ('Partner continuity', 'The objective is to reinforce the originating partner relationship while improving local execution.'),
        ],
        'process': [
            ('01', 'Partner brief', 'Share dates, guest profile, required services and preferred client communication model.'),
            ('02', 'Scope & feasibility', 'Local availability, dependencies and operational constraints are clarified.'),
            ('03', 'Confirm local delivery', 'Confirmed services and handovers are consolidated into an Ibiza operating picture.'),
            ('04', 'Report & adapt', 'The partner receives clear updates as confirmed timings or client requirements evolve.'),
        ],
        'faqs': [
            ('What is a luxury DMC in Ibiza?', 'A destination management company or local operator coordinates on-the-ground services for a client itinerary, often on behalf of a travel advisor, concierge firm, private office or hospitality partner.'),
            ('Can Ibiza VIP Move work behind the travel advisor?', 'Yes. The preferred client-facing or behind-the-scenes workflow can be agreed before an active brief is accepted.'),
            ('Which Ibiza services can be coordinated for a partner?', 'Requests can include private chauffeur transport, villas, yachts, private aviation ground coordination, dining, nightlife, staffing, wellness, security and bespoke guest logistics.'),
            ('Do you offer referral or partnership arrangements?', 'B2B commercial structures can be discussed directly for suitable professional relationships and active briefs; the applicable terms are agreed case by case in writing.'),
        ],
        'related': [
            ('Travel Partners', '/partners/'),
            ('Luxury Travel Concierge Ibiza', '/luxury-travel-concierge-ibiza/'),
            ('Private Client Services Ibiza', '/private-client-services-ibiza/'),
        ],
    },
]


def page_path(slug):
    return ROOT / slug / 'index.html'


def remove_meta(html, key):
    pattern = r'<meta\b(?=[^>]*(?:name|property)=["\']' + re.escape(key) + r'["\'])[^>]*>\s*'
    return re.sub(pattern, '', html, flags=re.I)


def schema_for(data):
    url = f"{BASE}/{data['slug']}/"
    area = {
        '@type': 'Place',
        'name': 'Ibiza, Balearic Islands, Spain',
        'containedInPlace': {
            '@type': 'AdministrativeArea',
            'name': 'Balearic Islands, Spain',
        },
    }
    organization = {
        '@type': 'Organization',
        '@id': ORG,
        'name': 'Ibiza VIP Move',
        'url': BASE + '/',
        'telephone': PHONE,
        'email': EMAIL,
        'founder': {'@id': FOUNDER},
        'sameAs': [INSTAGRAM],
        'areaServed': area,
    }
    service = {
        '@type': 'Service',
        '@id': url + '#service',
        'name': data['service_type'],
        'alternateName': data['alternate'],
        'url': url,
        'description': data['description'],
        'provider': {'@id': ORG},
        'areaServed': area,
        'audience': {
            '@type': 'Audience',
            'audienceType': data['audience'],
        },
        'availableChannel': {
            '@type': 'ServiceChannel',
            'serviceUrl': url,
            'servicePhone': {
                '@type': 'ContactPoint',
                'telephone': PHONE,
                'contactType': 'customer service',
                'availableLanguage': ['English', 'Spanish', 'French', 'German', 'Arabic'],
            },
        },
    }
    webpage = {
        '@type': 'WebPage',
        '@id': url + '#webpage',
        'url': url,
        'name': data['title'],
        'description': data['description'],
        'isPartOf': {'@id': BASE + '/#website'},
        'about': {'@id': url + '#service'},
        'inLanguage': 'en',
    }
    breadcrumb = {
        '@type': 'BreadcrumbList',
        '@id': url + '#breadcrumb',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ibiza VIP Move', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': data['service_type'], 'item': url},
        ],
    }
    faq = {
        '@type': 'FAQPage',
        '@id': url + '#faq',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a},
            }
            for q, a in data['faqs']
        ],
    }
    return {
        '@context': 'https://schema.org',
        '@graph': [organization, service, webpage, breadcrumb, faq],
    }


def render_body(data):
    pillars = ''.join(
        f'<div><b>{escape(title)}</b><p>{escape(text)}</p></div>'
        for title, text in data['pillars']
    )
    process = ''.join(
        f'<article><span>{escape(num)}</span><h3>{escape(title)}</h3><p>{escape(text)}</p></article>'
        for num, title, text in data['process']
    )
    faqs = ''.join(
        f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
        for q, a in data['faqs']
    )
    related = ' · '.join(
        f'<a class="text-link" href="{escape(url, quote=True)}">{escape(label)}</a>'
        for label, url in data['related']
    )
    whatsapp_text = escape(data['service_type'], quote=True).replace(' ', '%20')
    return f'''<section class="page-hero service-hero" style="--hero:url('/assets/images/{escape(data["hero"], quote=True)}')"><div><div class="kicker light">{data["kicker"]}</div><h1>{data["h1"]}</h1><p>{escape(data["description"])}</p><div class="hero-actions"><a class="btn gold" href="{WA}?text=Hello%20Ibiza%20VIP%20Move%2C%20I%20would%20like%20to%20discuss%20{whatsapp_text}.">Start a private brief</a><a class="btn ghost" href="/private-concierge-ibiza/">Private Concierge</a></div></div></section>
<section class="editorial"><div><div class="kicker dark">Ibiza · Balearic Islands · Spain</div><h2>{escape(data["lead_title"])}</h2></div><div><p class="large">{escape(data["lead"])}</p><p>{escape(data["detail"])}</p><a class="text-link" href="/contact/">Request private support →</a></div></section>
<section class="dark-panel"><div class="kicker light">Why this service exists</div><h2>Local coordination.<br>Clear private execution.</h2><div class="trust-grid">{pillars}</div></section>
<section class="process"><div class="section-head"><div class="kicker dark">Working model</div><h2>From brief to coordinated stay.</h2><p>Availability, scope and terms are confirmed for each request. No service, reservation or access is represented as confirmed until it has been agreed in writing.</p></div><div class="process-grid">{process}</div></section>
<section class="faq"><div class="section-head"><div class="kicker dark">Private client FAQ</div><h2>What clients and partners usually ask.</h2></div>{faqs}</section>
<section class="partners-strip"><div><div class="kicker dark">Related private support</div><h2>Choose the pathway closest to your brief.</h2><p>{related}</p></div><a class="btn dark" href="{WA}">WhatsApp Concierge</a></section>
<section class="closing-simple"><h2>Need an Ibiza-based point of contact?</h2><p>Share dates, guests and the main requirement. We will clarify the next practical step.</p><a class="btn dark" href="/contact/">Start your brief</a></section>'''


def build_page(template, data):
    html = template
    # Remove template-specific search metadata and structured data, keeping global
    # analytics, styles, consent and navigation intact.
    html = re.sub(r'<title>.*?</title>\s*', '', html, count=1, flags=re.I | re.S)
    html = re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>\s*', '', html, flags=re.I)
    html = re.sub(
        r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>\s*',
        '',
        html,
        flags=re.I,
    )
    for key in (
        'description', 'og:type', 'og:title', 'og:description', 'og:url', 'og:image',
        'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'
    ):
        html = remove_meta(html, key)
    html = re.sub(
        r'<script\s+type=["\']application/ld\+json["\']>.*?</script>\s*',
        '',
        html,
        flags=re.I | re.S,
    )
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
        raise SystemExit(f'Phase 102 template missing </head> for {data["slug"]}')
    html = html.replace('</head>', meta + '</head>', 1)
    body = render_body(data)
    html, count = re.subn(r'<main\b[^>]*>.*?</main>', '<main>' + body + '</main>', html, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit(f'Phase 102 template main replacement failed for {data["slug"]}: {count}')
    return html


def add_cluster(path, title, links):
    target = ROOT / path.strip('/') / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 102 internal-link target missing: {path}')
    html = target.read_text(encoding='utf-8')
    marker = 'ivm-intent-cluster'
    if marker in html:
        return
    link_html = ' · '.join(
        f'<a class="text-link" href="{url}">{escape(label)}</a>'
        for label, url in links
    )
    section = (
        f'<section class="partners-strip {marker}"><div>'
        f'<div class="kicker dark">More ways clients search for this support</div>'
        f'<h2>{escape(title)}</h2><p>{link_html}</p></div>'
        f'<a class="btn dark" href="/contact/">Private brief</a></section>'
    )
    if '</main>' not in html:
        raise SystemExit(f'Phase 102 internal-link target missing </main>: {path}')
    html = html.replace('</main>', section + '</main>', 1)
    target.write_text(html, encoding='utf-8')


if not TEMPLATE.exists():
    raise SystemExit('Phase 102 private-concierge template missing')

template = TEMPLATE.read_text(encoding='utf-8')
for data in PAGES:
    target = page_path(data['slug'])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_page(template, data), encoding='utf-8')
    print(f'Phase 102 created /{data["slug"]}/')

# Build a controlled internal-link network from the strongest existing hubs.
add_cluster('/private-concierge-ibiza/', 'Private support, matched to the intent.', [
    ('Luxury Lifestyle Management', '/luxury-lifestyle-management-ibiza/'),
    ('Personal Concierge', '/personal-concierge-ibiza/'),
    ('Luxury Travel Concierge', '/luxury-travel-concierge-ibiza/'),
    ('VIP Services', '/vip-services-ibiza/'),
    ('Private Client Services', '/private-client-services-ibiza/'),
    ('Destination Management', '/destination-management-ibiza/'),
])
add_cluster('/services/', 'Explore private-client pathways beyond individual services.', [
    ('Lifestyle Management', '/luxury-lifestyle-management-ibiza/'),
    ('VIP Services', '/vip-services-ibiza/'),
    ('Private Client Services', '/private-client-services-ibiza/'),
    ('Luxury DMC', '/destination-management-ibiza/'),
])
add_cluster('/international-clients/', 'International planning, executed locally in Ibiza.', [
    ('Luxury Travel Concierge', '/luxury-travel-concierge-ibiza/'),
    ('Private Client Services', '/private-client-services-ibiza/'),
    ('Destination Management', '/destination-management-ibiza/'),
])
add_cluster('/partners/', 'Local Ibiza pathways for professional partners.', [
    ('Luxury DMC & Destination Management', '/destination-management-ibiza/'),
    ('Private Client Services', '/private-client-services-ibiza/'),
    ('Luxury Travel Concierge', '/luxury-travel-concierge-ibiza/'),
])

# Add the six canonical URLs to the XML sitemap. IndexNow reads this sitemap
# automatically after a successful deployment.
sitemap_path = ROOT / 'sitemap.xml'
if not sitemap_path.exists():
    raise SystemExit('Phase 102 sitemap.xml missing')
sitemap = sitemap_path.read_text(encoding='utf-8')
entries = []
for data in PAGES:
    url = f"{BASE}/{data['slug']}/"
    if url not in sitemap:
        entries.append(f'  <url><loc>{url}</loc></url>')
if entries:
    if '</urlset>' not in sitemap:
        raise SystemExit('Phase 102 sitemap closing tag missing')
    sitemap = sitemap.replace('</urlset>', '\n' + '\n'.join(entries) + '\n</urlset>', 1)
    sitemap_path.write_text(sitemap, encoding='utf-8')

# Give search/AI systems a concise machine-readable description of the new
# intent architecture without keyword stuffing.
llms_path = ROOT / 'llms.txt'
if not llms_path.exists():
    raise SystemExit('Phase 102 llms.txt missing')
llms = llms_path.read_text(encoding='utf-8')
marker = '## High-intent concierge pathways'
if marker not in llms:
    llms += '\n\n' + marker + '\n'
    for data in PAGES:
        llms += f"- {data['service_type']}: {BASE}/{data['slug']}/ — {data['description']}\n"
    llms_path.write_text(llms, encoding='utf-8')

print('PASS: Phase 102 global concierge intent architecture — six distinct intent pages, local Ibiza entity signals, internal links, sitemap and llms discovery added')
