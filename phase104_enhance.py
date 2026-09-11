from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
PHONE = '+34 600 703 303'
EMAIL = 'partnership@ibizavipmove.com'
WA = 'https://wa.me/34600703303'
INSTAGRAM = 'https://www.instagram.com/ibizavipmove/'
PUBLISHED = '2026-09-11T07:30:00+02:00'
TEMPLATE = ROOT / 'private-concierge-ibiza' / 'index.html'

CASES = [
    {
        'slug': 'case-studies/private-aviation-arrival-seven-guests',
        'title': 'Case Study: Private Aviation Arrival for Seven Guests | Ibiza VIP Move',
        'description': 'An anonymized Ibiza VIP Move case study showing how a seven-guest private aviation arrival was coordinated with two V-Class vehicles, dedicated luggage capacity and onward transport.',
        'kicker': 'Operational Case Study · Private Aviation',
        'h1': 'Seven guests.<br><em>Three vehicles. One arrival plan.</em>',
        'hero': 'aviation.jpg',
        'summary': 'A private-flight arrival for seven guests required more than counting seats. The operating brief combined two Mercedes-Benz V-Class vehicles for the passengers, a separate luggage vehicle, flight monitoring, terminal meeting and onward movement to a north-Ibiza destination. The objective was to make the handover from aircraft arrival to road transport feel like one continuous movement.',
        'challenge': 'Seven passengers can technically fit into a single large people carrier, but that calculation ignores comfort, luggage volume, privacy and the quality expected after a private flight. The destination also meant the vehicles needed to leave the airport together and remain aligned through the onward journey. A delay at the aircraft, baggage handover or meeting point could otherwise split the group and create multiple client-facing conversations.',
        'plan': 'The movement was designed around passenger experience rather than minimum vehicle capacity. Two V-Class vehicles were assigned to the guest party and a separate vehicle was allocated to luggage. The driver team received the flight details, guest count, contact information and onward destination before arrival. The private arrival was treated as a single operating event with several linked vehicles instead of three unrelated transfers.',
        'execution': 'The team followed the flight timing, positioned the vehicles for the confirmed arrival window and kept the guest and luggage movements synchronized. Passenger vehicles could leave without being overloaded, while the luggage vehicle absorbed the practical volume that often creates delays or compromises cabin comfort. Communication was kept through one coordinating point so the client did not need to manage individual drivers.',
        'outcome': 'The important result was not simply that seven people reached their destination. The movement preserved cabin comfort, separated luggage from passenger space and reduced the number of operational decisions the guests had to make after landing. The same structure also created a cleaner basis for any later on-call transport during the stay.',
        'lessons': [
            ('Passenger count is not the same as vehicle requirement', 'Luxury arrival planning has to consider luggage, cabin comfort, privacy and destination—not only legal seating capacity.'),
            ('Private aviation needs a ground handover plan', 'The aircraft arrival, meeting point, vehicles, luggage and onward destination should be treated as one connected timeline.'),
            ('One coordinator reduces client friction', 'Several drivers can operate behind one communication channel so the client receives one clear answer rather than multiple operational messages.'),
            ('Redundancy can improve experience', 'An additional luggage vehicle may look inefficient on paper, but it can materially improve comfort and departure speed for a private group.'),
        ],
        'related': [('/private-aviation-ibiza/', 'Private Aviation Ibiza'),('/private-chauffeur-ibiza/', 'Private Chauffeur Ibiza'),('/private-client-services-ibiza/', 'Private Client Services')],
    },
    {
        'slug': 'case-studies/principal-chauffeur-security-three-days',
        'title': 'Case Study: Three-Day Chauffeur & Security Brief | Ibiza VIP Move',
        'description': 'An anonymized three-day Ibiza private-client case study combining daily chauffeur coverage of about 11.5 hours with licensed security and a single coordinated operating brief.',
        'kicker': 'Operational Case Study · Principal Support',
        'h1': 'Three days of movement.<br><em>One protected operating brief.</em>',
        'hero': 'security.jpg',
        'summary': 'A private principal required chauffeur and licensed security coverage across three consecutive days, with operating windows of approximately eleven and a half hours per day. The work was not a sequence of point-to-point transfers: driver availability, protection coverage, waiting time, venue movements and changes during the day all had to remain connected.',
        'challenge': 'Long private-client days create a different operational problem from a normal transfer. The vehicle and security professional need to remain available while the guest schedule changes, and both roles must have the same understanding of pickup points, destinations, waiting periods and any sensitive movements. Fragmented communication can quickly produce mismatched arrival times or leave one supplier working from an outdated itinerary.',
        'plan': 'The chauffeur and security requirements were treated as a combined daily operating window. Before each day, the known schedule and likely movement pattern were reviewed as one brief. The driver remained responsible for mobility while the licensed protection professional retained the security role; coordination did not blur those responsibilities. One client-facing contact remained the reference for changes.',
        'execution': 'Across the three days, confirmed movements and waiting periods were managed inside the same daily coverage window. When timing changed, the revised information could be communicated against the shared operating picture rather than as isolated instructions. The structure made it possible for driver and security availability to remain aligned without asking the principal to coordinate them directly.',
        'outcome': 'The principal had continuous mobility and protection coverage without having to rebuild the brief at every stop. From an operational perspective, the value came from keeping two independent professional services synchronized while preserving clear responsibility, discretion and a single line of communication.',
        'lessons': [
            ('Disposition is different from a transfer', 'When the day is fluid, a dedicated operating window is often more appropriate than pricing and planning every movement separately.'),
            ('Security and transport must share timing', 'The professionals remain independent in role, but they need the same current itinerary to avoid gaps.'),
            ('Changes need one source of truth', 'A single coordinating brief reduces the risk of one supplier receiving an update that another supplier misses.'),
            ('Long days require realistic scheduling', 'Waiting, meal periods, venue access and driver/security endurance should be considered when building multi-day coverage.'),
        ],
        'related': [('/private-security-ibiza/', 'Private Security Ibiza'),('/private-chauffeur-ibiza/', 'Private Chauffeur Ibiza'),('/private-client-services-ibiza/', 'Private Client Services')],
    },
    {
        'slug': 'case-studies/weekend-concierge-two-guests',
        'title': 'Case Study: Two-Guest Ibiza Weekend Concierge | Ibiza VIP Move',
        'description': 'An anonymized Ibiza weekend concierge case study connecting airport transfers, a beach day, dinner and show, nightlife, wellness appointments and timed private transport for two guests.',
        'kicker': 'Operational Case Study · Weekend Concierge',
        'h1': 'A weekend itinerary<br><em>with every handover connected.</em>',
        'hero': 'nightlife.jpg',
        'summary': 'A two-guest weekend brief combined airport arrival and departure, a premium beach-club day, dinner and show, late-night house music, scheduled wellness appointments and private transport between each part of the itinerary. The value was not any single reservation; it was making the transitions between them realistic.',
        'challenge': 'Short stays can be more operationally demanding than long ones because the guest wants to fit several experiences into a limited window. A beach-club lunch affects the time available before wellness. Wellness timing affects the dinner departure. Dinner and show timing affects the nightlife movement and return. If those elements are booked independently, each can look correct while the overall itinerary is impossible.',
        'plan': 'The itinerary was built backward from fixed-time commitments. Airport movements were separated from the active leisure schedule. The beach day was placed early enough to allow a return and recovery window before the evening. Wellness appointments were positioned between daytime and evening plans. Dinner/show arrival was treated as a hard timing point, with the nightlife movement and late return planned around it.',
        'execution': 'Transport was attached to the itinerary rather than requested ad hoc. Each meaningful change of location had a vehicle plan, and the evening return remained part of the operating picture instead of becoming an afterthought at the end of the night. The client could still make lifestyle choices, but those choices were evaluated against actual travel and preparation time.',
        'outcome': 'The weekend remained ambitious without forcing the guests to manage the logistics themselves. The case demonstrates why private concierge work is often about sequencing: a strong individual reservation has limited value if the client cannot move comfortably from the previous commitment to the next one.',
        'lessons': [
            ('Fixed-time experiences should anchor the day', 'Shows, treatments, flights and yacht departures are harder to move than informal leisure time, so the itinerary should be built around them.'),
            ('Return transport is part of nightlife planning', 'The operating plan should include how the client leaves, not only how they arrive.'),
            ('Wellness needs transition time', 'Treatments placed between beach and nightlife plans require realistic travel, shower and preparation windows.'),
            ('Concierge value is often in sequencing', 'The best outcome comes from making several good experiences compatible with one another.'),
        ],
        'related': [('/personal-concierge-ibiza/', 'Personal Concierge Ibiza'),('/vip-services-ibiza/', 'VIP Services Ibiza'),('/luxury-lifestyle-management-ibiza/', 'Lifestyle Management Ibiza')],
    },
    {
        'slug': 'case-studies/multi-day-executive-chauffeur-program',
        'title': 'Case Study: Multi-Day Executive Chauffeur Program | Ibiza VIP Move',
        'description': 'An anonymized multi-day Ibiza executive transport case study showing how chauffeur operating windows ranging from roughly 8 to 18 hours were managed under one evolving schedule.',
        'kicker': 'Operational Case Study · Executive Mobility',
        'h1': 'Variable days.<br><em>Consistent executive mobility.</em>',
        'hero': 'chauffeur.jpg',
        'summary': 'A multi-day executive brief required private chauffeur coverage across several consecutive days with very different operating lengths—some around a standard full day and others extending toward eighteen hours. The schedule changed by day, but the client needed the transport experience to remain consistent.',
        'challenge': 'A multi-day corporate or executive itinerary rarely behaves like a repeated airport transfer. Meeting times move, lunches extend, evening commitments are added, and different passengers may join or leave the vehicle. Long operating days also create practical questions around driver planning, waiting, rest and how late changes should be communicated.',
        'plan': 'Instead of treating every movement as a separate new booking, the work was managed as a continuing chauffeur program. Each day had an expected operating window, principal contact and known commitments. The structure allowed daily detail to change without losing the continuity of the wider brief. Additional hours or material changes remained subject to the applicable service terms.',
        'execution': 'The chauffeur schedule was refreshed around the client’s latest confirmed agenda. Pickup points, meeting locations, hospitality stops and evening movements were kept in the same operating view. The driver did not need to negotiate each change directly with multiple passengers; the client side had one point of contact for the evolving itinerary.',
        'outcome': 'The transport remained predictable even when the days were not. The useful result was continuity: the client could change business and hospitality plans while the mobility layer adapted around the revised schedule. This is particularly important for executive groups where transport problems create visible disruption for several people at once.',
        'lessons': [
            ('Multi-day mobility benefits from a retained brief', 'Continuity matters when the itinerary changes every day and several movements depend on the same driver or vehicle plan.'),
            ('Operating windows need to be explicit', 'A ten-hour day and an eighteen-hour day are operationally different and should not be treated as interchangeable.'),
            ('One contact protects executive time', 'The client should not have to coordinate every route change separately with operational suppliers.'),
            ('The schedule must remain current', 'A beautifully prepared itinerary is only useful if the driver team receives the latest confirmed version.'),
        ],
        'related': [('/private-chauffeur-ibiza/', 'Private Chauffeur Ibiza'),('/private-office/', 'Private Office'),('/destination-management-ibiza/', 'Destination Management Ibiza')],
    },
    {
        'slug': 'case-studies/late-night-dual-vehicle-arrival',
        'title': 'Case Study: Late-Night Dual-Vehicle Arrival | Ibiza VIP Move',
        'description': 'An anonymized Ibiza late-night arrival case study involving two private vans, a 03:45 operating window, luggage, approximately one hour of waiting and coordinated onward transport.',
        'kicker': 'Operational Case Study · Night Arrival',
        'h1': '03:45 arrival.<br><em>No room for fragmented logistics.</em>',
        'hero': 'hero.jpg',
        'summary': 'A late-night movement required two private vans around 03:45, luggage handling and approximately one hour of waiting before the onward movement could be completed. At that hour, the operational cost of a missed instruction is higher because alternative vehicles and support are harder to source instantly.',
        'challenge': 'Night arrivals often look simple on an itinerary: airport, vehicle, destination. In practice, a delayed handover, luggage issue, client pause or change in readiness can extend the movement. When two vehicles are involved, both need to understand whether they should wait, depart together or split. The client should not be resolving that at four in the morning.',
        'plan': 'The vehicles were positioned around a shared late-night brief with passenger and luggage requirements understood in advance. Waiting was treated as a possible operating requirement rather than an unexpected exception. The onward movement remained coordinated so both vehicles worked from the same readiness signal.',
        'execution': 'The drivers remained aligned during the waiting period and departed according to the confirmed client readiness. Because the movement had one coordinating logic, the client did not need to negotiate separately with two vehicles. The plan also protected against the common late-night failure of one vehicle leaving based on an outdated assumption while the other continues waiting.',
        'outcome': 'The movement absorbed the delay without turning it into a client-facing problem. The case is a useful reminder that premium transport is often judged most clearly when something does not happen exactly on schedule. The ability to wait, communicate and adapt can matter more than the original pickup time.',
        'lessons': [
            ('Night work needs contingency', 'Late-night availability is thinner, so realistic waiting and backup thinking matter more.'),
            ('Two vehicles require one departure logic', 'Passenger and luggage vehicles should not make independent assumptions about when the movement is ready.'),
            ('Waiting is an operational state', 'If a client is not ready immediately, the plan should define how vehicles remain available and how time is handled.'),
            ('Premium service is visible during disruption', 'The quality of coordination becomes clearest when the original timing changes.'),
        ],
        'related': [('/private-chauffeur-ibiza/', 'Private Chauffeur Ibiza'),('/luxury-travel-concierge-ibiza/', 'Luxury Travel Concierge'),('/vip-services-ibiza/', 'VIP Services Ibiza')],
    },
]


def ppath(path):
    return ROOT / path.strip('/') / 'index.html'


def remove_meta(html, key):
    pattern = r'<meta\b(?=[^>]*(?:name|property)=["\']' + re.escape(key) + r'["\'])[^>]*>\s*'
    return re.sub(pattern, '', html, flags=re.I)


def normalize_head(template, title, desc, path, image, schema):
    html = template
    html = re.sub(r'<title>.*?</title>\s*', '', html, count=1, flags=re.I | re.S)
    html = re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>\s*', '', html, flags=re.I)
    html = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>\s*', '', html, flags=re.I)
    for key in ('description','og:type','og:title','og:description','og:url','og:image','twitter:card','twitter:title','twitter:description','twitter:image'):
        html = remove_meta(html, key)
    html = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>\s*', '', html, flags=re.I | re.S)
    url = BASE + path
    meta = (
        f'<title>{escape(title)}</title>'
        f'<meta name="description" content="{escape(desc, quote=True)}">'
        '<meta name="robots" content="index,follow,max-image-preview:large">'
        f'<link rel="canonical" href="{url}">'
        f'<link rel="alternate" hreflang="en" href="{url}">'
        f'<link rel="alternate" hreflang="x-default" href="{url}">'
        '<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{escape(title, quote=True)}">'
        f'<meta property="og:description" content="{escape(desc, quote=True)}">'
        f'<meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{BASE}/assets/images/{image}">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{escape(title, quote=True)}">'
        f'<meta name="twitter:description" content="{escape(desc, quote=True)}">'
        f'<meta name="twitter:image" content="{BASE}/assets/images/{image}">'
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>'
    )
    if '</head>' not in html:
        raise SystemExit(f'Phase 104 template missing head close: {path}')
    return html.replace('</head>', meta + '</head>', 1)


def org_node():
    return {
        '@type': 'Organization', '@id': ORG, 'name': 'Ibiza VIP Move', 'url': BASE + '/',
        'telephone': PHONE, 'email': EMAIL, 'founder': {'@id': FOUNDER}, 'sameAs': [INSTAGRAM],
        'areaServed': {'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},
    }


def person_node():
    return {
        '@type': 'Person', '@id': FOUNDER, 'name': 'Juan Cruz', 'jobTitle': 'Founder',
        'url': BASE + '/founder/', 'worksFor': {'@id': ORG},
        'knowsAbout': [
            'Private concierge operations in Ibiza','Luxury chauffeur coordination in Ibiza',
            'Private aviation ground coordination in Ibiza','Private client logistics in Ibiza',
            'Villa, yacht, hospitality and lifestyle coordination in Ibiza',
        ],
    }


def article_schema(data):
    path = '/' + data['slug'].strip('/') + '/'
    url = BASE + path
    return {
        '@context': 'https://schema.org',
        '@graph': [
            org_node(), person_node(),
            {
                '@type': 'Article', '@id': url + '#article', 'headline': re.sub('<.*?>','',data['h1']).replace('<br>',' '),
                'description': data['description'], 'url': url, 'datePublished': PUBLISHED, 'dateModified': PUBLISHED,
                'author': {'@id': FOUNDER}, 'publisher': {'@id': ORG},
                'mainEntityOfPage': {'@id': url + '#webpage'},
                'about': [{'@type':'Thing','name':'Luxury private-client operations in Ibiza'}],
                'inLanguage': 'en',
            },
            {'@type':'WebPage','@id':url+'#webpage','url':url,'name':data['title'],'description':data['description'],'about':{'@id':url+'#article'},'inLanguage':'en'},
            {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[
                {'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},
                {'@type':'ListItem','position':2,'name':'Case Studies','item':BASE+'/case-studies/'},
                {'@type':'ListItem','position':3,'name':re.sub('<.*?>','',data['h1']).replace('<br>',' '),'item':url},
            ]},
        ],
    }


def case_body(data):
    lessons = ''.join(f'<div><b>{escape(t)}</b><p>{escape(x)}</p></div>' for t,x in data['lessons'])
    related = ' · '.join(f'<a class="text-link" href="{u}">{escape(label)}</a>' for u,label in data['related'])
    return f'''<section class="page-hero service-hero" style="--hero:url('/assets/images/{data['hero']}')"><div><div class="kicker light">{data['kicker']}</div><h1>{data['h1']}</h1><p>{escape(data['description'])}</p></div></section>
<section class="editorial"><div><div class="kicker dark">Based on a real operating brief</div><h2>What had to work.</h2></div><div><p class="large">{escape(data['summary'])}</p><p><strong>Privacy note:</strong> This case study is based on a real Ibiza VIP Move operating brief. Client names, exact dates, properties, venue names and commercial terms are omitted or generalized to protect confidentiality.</p><p><a class="text-link" href="/founder/">By Juan Cruz · Founder →</a></p></div></section>
<section class="dark-panel"><div class="kicker light">The operating challenge</div><h2>Why the brief was more complex than it looked.</h2><p style="max-width:850px;color:rgba(255,255,255,.68)">{escape(data['challenge'])}</p></section>
<section class="editorial"><div><div class="kicker dark">Planning</div><h2>The operating model.</h2></div><div><p class="large">{escape(data['plan'])}</p><p>{escape(data['execution'])}</p></div></section>
<section class="process"><div class="section-head"><div class="kicker dark">Operational lessons</div><h2>What this brief demonstrates.</h2><p>These are practical lessons from the operating brief, not generic travel advice or market-wide statistics.</p></div><div class="trust-grid">{lessons}</div></section>
<section class="editorial"><div><div class="kicker dark">Outcome</div><h2>The value was in the coordination.</h2></div><div><p class="large">{escape(data['outcome'])}</p><p>{related}</p></div></section>
<section class="closing-simple"><h2>Planning a complex Ibiza brief?</h2><p>Share the dates, guests, movements and priorities. Ibiza VIP Move can assess the operating structure before services are confirmed.</p><a class="btn dark" href="{WA}">Request private support</a></section>'''


def write_page(path, title, desc, image, schema, body):
    template = TEMPLATE.read_text(encoding='utf-8')
    html = normalize_head(template, title, desc, path, image, schema)
    html, count = re.subn(r'<main\b[^>]*>.*?</main>', '<main id="main-content">' + body + '</main>', html, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit(f'Phase 104 main replacement failed: {path}')
    target = ppath(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')


if not TEMPLATE.exists():
    raise SystemExit('Phase 104 template missing')

# Dedicated founder profile: a single-person page that can be referenced by article author markup.
founder_path = '/founder/'
founder_title = 'Juan Cruz | Founder of Ibiza VIP Move'
founder_desc = 'Meet Juan Cruz, founder of Ibiza VIP Move: an Ibiza-based private concierge operator focused on chauffeur, private-client logistics, hospitality and lifestyle coordination.'
founder_schema = {
    '@context':'https://schema.org','@graph':[
        org_node(), person_node(),
        {'@type':'ProfilePage','@id':BASE+founder_path+'#profile','url':BASE+founder_path,'name':founder_title,'description':founder_desc,'mainEntity':{'@id':FOUNDER},'dateModified':PUBLISHED,'inLanguage':'en'},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},
            {'@type':'ListItem','position':2,'name':'Juan Cruz · Founder','item':BASE+founder_path},
        ]},
    ]
}
founder_body = f'''<section class="page-hero service-hero" style="--hero:url('/assets/images/hero.jpg')"><div><div class="kicker light">Founder · Ibiza VIP Move</div><h1>Juan Cruz.<br><em>Private Ibiza operations, personally led.</em></h1><p>{escape(founder_desc)}</p></div></section>
<section class="editorial"><div><div class="kicker dark">Founder profile</div><h2>One accountable point of contact.</h2></div><div><p class="large">Juan Cruz founded Ibiza VIP Move around a simple operating idea: a private client should not need to coordinate every driver, reservation, villa request, yacht movement, security requirement or last-minute change separately.</p><p>His role is operational rather than ceremonial. The brief begins with the client, personal assistant, travel advisor or partner, and the work is then coordinated through a selected network of independent Ibiza specialists. The objective is to keep timing, supplier handovers and client communication aligned through one trusted contact.</p></div></section>
<section class="dark-panel"><div class="kicker light">Field expertise</div><h2>Built from real Ibiza operating briefs.</h2><div class="trust-grid"><div><b>Private mobility</b><p>Airport, chauffeur, multi-vehicle, luggage and late-night movement coordination.</p></div><div><b>Private clients</b><p>Principals, families, PAs, family offices, executive groups and professional partners.</p></div><div><b>Connected stays</b><p>Villas, yachts, dining, nightlife, private aviation, wellness, staffing and protection.</p></div><div><b>Operational discretion</b><p>Client identities, itineraries and commercial details are not used publicly without authorization.</p></div></div></section>
<section class="editorial"><div><div class="kicker dark">How Juan works</div><h2>Clarity before promises.</h2></div><div><p class="large">Availability, access and service scope are confirmed before they are represented as secured. When a brief involves several suppliers, the priority is to identify the dependencies first: flights, guest count, luggage, vehicle capacity, property access, marina timing, reservation times, security needs and the person authorized to approve changes.</p><p>This approach is documented in the <a href="/case-studies/">Ibiza VIP Move operational case studies</a> and the <a href="/ibiza-luxury-operations-report-2026/">Ibiza Luxury Operations Report 2026</a>.</p></div></section>
<section class="closing-simple"><h2>Speak directly about an Ibiza brief.</h2><p>For private-client requests and professional partnerships, contact Ibiza VIP Move through the official channels on this site.</p><a class="btn dark" href="/contact/">Contact Ibiza VIP Move</a></section>'''
write_page(founder_path, founder_title, founder_desc, 'hero.jpg', founder_schema, founder_body)

# Case-study hub.
hub_path = '/case-studies/'
hub_title = 'Ibiza Private Concierge Case Studies | Ibiza VIP Move'
hub_desc = 'Anonymized operational case studies from real Ibiza VIP Move briefs covering private aviation arrivals, chauffeur and security, weekend concierge, executive mobility and night logistics.'
hub_url = BASE + hub_path
item_list = []
case_cards = []
for pos, data in enumerate(CASES, 1):
    path = '/' + data['slug'].strip('/') + '/'
    url = BASE + path
    item_list.append({'@type':'ListItem','position':pos,'url':url,'name':re.sub('<.*?>','',data['h1']).replace('<br>',' ')})
    case_cards.append(f'''<a class="service-card" href="{path}"><div class="service-card-img" style="background-image:linear-gradient(180deg,rgba(8,12,16,.05),rgba(8,12,16,.48)),url('/assets/images/{data['hero']}')"></div><div class="service-card-copy"><span>Real brief · anonymized</span><h3>{re.sub('<.*?>','',data['h1']).replace('<br>',' ')}</h3><p>{escape(data['description'])}</p><b>Read case study →</b></div></a>''')
hub_schema = {'@context':'https://schema.org','@graph':[org_node(),person_node(),{'@type':'CollectionPage','@id':hub_url+'#collection','url':hub_url,'name':hub_title,'description':hub_desc,'mainEntity':{'@type':'ItemList','itemListElement':item_list},'inLanguage':'en'},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Case Studies','item':hub_url}]}]}
hub_body = f'''<section class="page-hero service-hero" style="--hero:url('/assets/images/chauffeur.jpg')"><div><div class="kicker light">Operational evidence · Ibiza</div><h1>Real briefs.<br><em>Client identities protected.</em></h1><p>{escape(hub_desc)}</p></div></section>
<section class="editorial"><div><div class="kicker dark">Why publish case studies</div><h2>Experience should be visible.</h2></div><div><p class="large">Luxury concierge websites often describe what they can arrange. These case studies focus on what had to be coordinated in real operating briefs: passenger capacity, luggage, timing, waiting, protection, fixed reservations and changing schedules.</p><p>Every case is anonymized. Client names, exact dates, properties, venue names and commercial terms are omitted or generalized. The operational patterns are real and are published to explain how Ibiza VIP Move approaches complex private-client work.</p><a class="text-link" href="/founder/">Meet Juan Cruz · Founder →</a></div></section>
<section class="service-showcase compact"><div class="section-head"><div class="kicker light">Five operating briefs</div><h2>How private Ibiza logistics actually behave.</h2></div><div class="service-grid-cards">{''.join(case_cards)}</div></section>
<section class="closing-simple"><h2>Field experience, not generic concierge copy.</h2><p>For broader operating observations, read the Ibiza Luxury Operations Report 2026.</p><a class="btn dark" href="/ibiza-luxury-operations-report-2026/">Read the report</a></section>'''
write_page(hub_path, hub_title, hub_desc, 'chauffeur.jpg', hub_schema, hub_body)

# Five individual case studies.
for data in CASES:
    path = '/' + data['slug'].strip('/') + '/'
    write_page(path, data['title'], data['description'], data['hero'], article_schema(data), case_body(data))
    print(f'Phase 104 created {path}')

# Experience-based field report. It deliberately avoids market-share or island-wide statistical claims.
report_path = '/ibiza-luxury-operations-report-2026/'
report_title = 'Ibiza Luxury Operations Report 2026 | Ibiza VIP Move'
report_desc = 'Founder-led field observations from real Ibiza private-client operations: arrivals, chauffeur capacity, villas, nightlife, multi-day mobility, private aviation and professional partner workflows.'
report_url = BASE + report_path
report_schema = {'@context':'https://schema.org','@graph':[org_node(),person_node(),{'@type':'Article','@id':report_url+'#report','headline':'Ibiza Luxury Operations Report 2026','description':report_desc,'url':report_url,'datePublished':PUBLISHED,'dateModified':PUBLISHED,'author':{'@id':FOUNDER},'publisher':{'@id':ORG},'mainEntityOfPage':{'@id':report_url+'#webpage'},'inLanguage':'en'},{'@type':'WebPage','@id':report_url+'#webpage','url':report_url,'name':report_title,'description':report_desc,'about':{'@id':report_url+'#report'},'inLanguage':'en'},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Ibiza Luxury Operations Report 2026','item':report_url}]}]}
observations = [
    ('01','Capacity is more than passenger count','A premium transport plan should consider luggage volume, cabin comfort, privacy, child equipment, security personnel and whether guests need to travel together. A vehicle that is technically legal for the passenger count may still be the wrong operational choice.'),
    ('02','Private aviation is a handover, not just an airport pickup','Flight timing, terminal or FBO meeting, passenger readiness, luggage, vehicle positioning and onward destination form one connected arrival event. The strongest plans reduce the number of decisions the client must make after landing.'),
    ('03','Nightlife needs a return strategy','Restaurant and nightlife planning is incomplete if it only solves arrival. Late return availability, waiting, changing venue times and the client’s likely end-of-night location should be considered before the evening begins.'),
    ('04','Multi-day clients often need disposition, not repeated transfers','When daily schedules are fluid, a retained chauffeur or operating window can produce more continuity than rebuilding every movement separately. The same principle applies when security or other private support must stay synchronized.'),
    ('05','Villa stays create hidden dependencies','Property access, guest arrivals, luggage, housekeeping, chefs, wellness, security, vehicles and yacht or restaurant movements can all depend on the same villa schedule. Treating those services independently creates avoidable handover risk.'),
    ('06','Professional partners value one accountable local contact','Travel advisors, concierge firms, PAs and family offices often already own the client relationship. What they need in Ibiza is clear local execution, controlled communication and a partner who can work client-facing or behind the scenes as agreed.'),
    ('07','The confirmation standard matters','A request, preference or inquiry is not the same as a confirmed service. Strong private-client operations distinguish clearly between requested, available, held and confirmed—especially for venues, yachts, villas, security and high-demand dates.'),
    ('08','Luxury is often operational silence','The guest should not need to see the number of calls, supplier checks, timing changes or vehicle decisions behind a stay. The work is successful when complexity is absorbed before it becomes the client’s problem.'),
]
obs_html = ''.join(f'<article><span>{n}</span><h3>{escape(t)}</h3><p>{escape(x)}</p></article>' for n,t,x in observations)
report_body = f'''<section class="page-hero service-hero" style="--hero:url('/assets/images/villa.jpg')"><div><div class="kicker light">Founder field report · 2026</div><h1>Ibiza luxury operations,<br><em>from the ground.</em></h1><p>{escape(report_desc)}</p></div></section>
<section class="editorial"><div><div class="kicker dark">Methodology</div><h2>Operational observations, not market statistics.</h2></div><div><p class="large">This report is based on recurring patterns observed across real Ibiza VIP Move private-client and professional-partner briefs during the 2026 season.</p><p>It is not presented as a statistically representative survey of the Ibiza luxury market. No market-share, island-wide demand or competitor-performance claims are made. Client identities and confidential commercial information are excluded. The purpose is to publish practical, first-hand operating insight that can help principals, PAs, family offices and luxury travel professionals plan Ibiza more realistically.</p><p><a class="text-link" href="/founder/">Juan Cruz · Founder →</a></p></div></section>
<section class="process"><div class="section-head"><div class="kicker dark">Eight field observations</div><h2>What repeatedly matters in high-value Ibiza briefs.</h2></div><div class="process-grid">{obs_html}</div></section>
<section class="dark-panel"><div class="kicker light">What changes for professional partners</div><h2>The client relationship and the local operation are different jobs.</h2><p style="max-width:900px;color:rgba(255,255,255,.68)">A travel advisor, family office or international concierge may already understand the principal perfectly. Ibiza VIP Move does not need to replace that relationship. The local role is to translate the agreed client brief into workable timings, capacity, supplier handovers and on-island communication. That separation is one reason behind our B2B and destination-management structure.</p><p><a class="text-link" style="color:#fff;border-color:#fff" href="/destination-management-ibiza/">Destination Management Ibiza →</a></p></section>
<section class="editorial"><div><div class="kicker dark">Evidence behind the observations</div><h2>Read the operating briefs.</h2></div><div><p class="large">The report is supported by anonymized case studies covering private aviation arrival planning, chauffeur and security, weekend concierge sequencing, multi-day executive mobility and late-night transport.</p><p><a class="text-link" href="/case-studies/">Explore operational case studies →</a></p></div></section>
<section class="closing-simple"><h2>Planning an Ibiza brief for a principal or client?</h2><p>Share the operational requirements and preferred communication model.</p><a class="btn dark" href="/contact/">Contact Ibiza VIP Move</a></section>'''
write_page(report_path, report_title, report_desc, 'villa.jpg', report_schema, report_body)

# Enrich the existing founder Person nodes to point to the dedicated profile page.
script_re = re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)', re.I | re.S)
for target in ROOT.rglob('*.html'):
    html = target.read_text(encoding='utf-8')
    changed = False
    def fix_person(match):
        nonlocal_marker = None
        try:
            data = json.loads(match.group(2))
        except Exception:
            return match.group(0)
        nodes = data.get('@graph', []) if isinstance(data, dict) and isinstance(data.get('@graph'), list) else [data]
        local = False
        for node in nodes:
            if isinstance(node, dict) and node.get('@id') == FOUNDER:
                node['url'] = BASE + '/founder/'
                local = True
        if local:
            return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + match.group(3)
        return match.group(0)
    updated = script_re.sub(fix_person, html)
    if updated != html:
        target.write_text(updated, encoding='utf-8')

# Contextual authority links from four existing strong hubs.
def add_authority(path, title, text, links):
    target = ppath(path)
    if not target.exists():
        raise SystemExit(f'Phase 104 authority hub missing: {path}')
    html = target.read_text(encoding='utf-8')
    if 'ivm-phase104-authority' in html:
        return
    linked = ' · '.join(f'<a class="text-link" href="{url}">{escape(label)}</a>' for label,url in links)
    section = f'<section class="editorial ivm-phase104-authority"><div><div class="kicker dark">Operational authority</div><h2>{escape(title)}</h2></div><div><p class="large">{escape(text)}</p><p>{linked}</p></div></section>'
    if '</main>' not in html:
        raise SystemExit(f'Phase 104 authority hub missing main close: {path}')
    target.write_text(html.replace('</main>', section + '</main>', 1), encoding='utf-8')

add_authority('/about/','Meet the founder behind the operating brief.','Ibiza VIP Move now publishes a dedicated founder profile, anonymized operational case studies and a field report so private clients and professional partners can evaluate the experience behind the service.', [('Juan Cruz · Founder','/founder/'),('Operational case studies','/case-studies/'),('2026 field report','/ibiza-luxury-operations-report-2026/')])
add_authority('/private-concierge-ibiza/','See how complex private briefs are actually coordinated.','The operating case studies show how chauffeur, luggage, private aviation, protection, reservations and changing schedules are connected in real anonymized briefs.', [('Case studies','/case-studies/'),('Ibiza Luxury Operations Report','/ibiza-luxury-operations-report-2026/')])
add_authority('/partners/','Evidence for travel advisors and private offices.','Professional partners can review anonymized operating briefs and founder field observations before assigning an active Ibiza client brief.', [('Operational case studies','/case-studies/'),('Founder profile','/founder/'),('2026 field report','/ibiza-luxury-operations-report-2026/')])
add_authority('/ibiza-intelligence/','From destination guidance to operating evidence.','The Black Book explains how to plan Ibiza; the operational case studies and field report show how real private-client logistics behave once the itinerary meets the island.', [('Operational case studies','/case-studies/'),('2026 operations report','/ibiza-luxury-operations-report-2026/')])

# Sitemap + llms discovery.
sitemap_path = ROOT / 'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
new_paths = [founder_path, hub_path, report_path] + ['/' + x['slug'].strip('/') + '/' for x in CASES]
entries = []
for path in new_paths:
    url = BASE + path
    if url not in sitemap:
        entries.append(f'  <url><loc>{url}</loc></url>')
if entries:
    sitemap = sitemap.replace('</urlset>', '\n' + '\n'.join(entries) + '\n</urlset>', 1)
    sitemap_path.write_text(sitemap, encoding='utf-8')

llms_path = ROOT / 'llms.txt'
llms = llms_path.read_text(encoding='utf-8')
marker = '## Founder and operational evidence'
if marker not in llms:
    llms += f'''\n\n{marker}\n- Founder profile: {BASE}/founder/ — Juan Cruz, founder of Ibiza VIP Move and operator behind the private-client coordination model.\n- Operational case studies: {BASE}/case-studies/ — anonymized real Ibiza VIP Move operating briefs; client identities and commercial terms omitted.\n- Ibiza Luxury Operations Report 2026: {report_url} — founder field observations based on recurring operational patterns; explicitly not an island-wide statistical market survey.\n'''
    for data in CASES:
        llms += f"- Case study: {BASE}/{data['slug'].strip('/')}/ — {data['description']}\n"
    llms_path.write_text(llms, encoding='utf-8')

print('PASS: Phase 104 global authority — founder ProfilePage, five anonymized real operating case studies, 2026 field report, authority links, sitemap and AI discovery published')
