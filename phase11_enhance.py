from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
WA = 'https://wa.me/34600703303'
PHONE = '+34 600 703 303'
EMAIL = 'partnership@ibizavipmove.com'


def replace_nav(text: str) -> str:
    nav = (
        '<nav><a href="/services/">Services</a>'
        '<a href="/private-office/">Private Office</a>'
        '<a href="/ibiza-intelligence/">Ibiza Intelligence</a>'
        '<a href="/about/">About</a><a href="/contact/">Contact</a>'
        f'<a class="nav-cta" href="{WA}">Request Concierge</a></nav>'
    )
    text = re.sub(r'<nav>.*?</nav>', nav, text, count=1, flags=re.S)
    mobile = (
        '<div class="mobile-menu"><a href="/services/">Services</a>'
        '<a href="/private-office/">Private Office</a>'
        '<a href="/ibiza-intelligence/">Ibiza Intelligence</a>'
        '<a href="/about/">About</a><a href="/contact/">Contact</a>'
        f'<a href="{WA}">WhatsApp Concierge</a></div>'
    )
    text = re.sub(r'<div class="mobile-menu">.*?</div>', mobile, text, count=1, flags=re.S)
    return text


def update_english_navigation():
    for path in ROOT.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        if '<html lang="en"' not in text:
            continue
        text = replace_nav(text)
        path.write_text(text, encoding='utf-8')


def service_card(href, image, eyebrow, title, copy):
    return f'''<a class="service-card" href="{href}"><div class="service-card-img"><img src="{image}" alt="{title} in Ibiza — Ibiza VIP Move" loading="lazy" decoding="async" width="1600" height="1000"></div><div class="service-card-copy"><span>{eyebrow}</span><h3>{title}</h3><p>{copy}</p><b>Explore →</b></div></a>'''


def home_main():
    six = ''.join([
        service_card('/private-chauffeur-ibiza/', '/assets/images/chauffeur.jpg', 'Private Mobility', 'Private Chauffeur', 'Airport arrivals, daily chauffeur service, nightlife movements and multi-vehicle coordination.'),
        service_card('/luxury-villas-ibiza/', '/assets/images/villa.jpg', 'Private Stays', 'Luxury Villas', 'Private stays coordinated around location, privacy, guest requirements and the rhythm of your itinerary.'),
        service_card('/yacht-charter-ibiza/', '/assets/images/yacht.jpg', 'At Sea', 'Yachts & Formentera', 'Yacht days and charters aligned with villa, marina, transport, dining and the rest of the stay.'),
        service_card('/restaurants-nightlife-ibiza/', '/assets/images/nightlife.jpg', 'Private Access', 'Dining & Nightlife', 'Restaurants, beach clubs, nightlife and celebrations coordinated around timing, transport and preferences.'),
        service_card('/private-aviation-ibiza/', '/assets/images/aviation.jpg', 'Private Arrivals', 'Private Aviation', 'Ground coordination around private and commercial arrivals, luggage, chauffeurs and onward movements.'),
        service_card('/services/', '/assets/images/chef.jpg', 'Lifestyle Management', 'Beyond Reservations', 'Security, private chefs, wellness, staffing, events and bespoke requirements through one point of contact.'),
    ])
    return f'''<section class="hero hero-with-media"><img class="hero-media" src="/assets/images/hero.jpg" alt="Luxury private concierge experience overlooking the Mediterranean in Ibiza" width="2400" height="1600" fetchpriority="high" decoding="async"><div class="hero-shade"></div><div class="hero-content"><div class="kicker">The private side of Ibiza</div><h1>Exceptional Ibiza,<br><em>handled privately.</em></h1><p>Private concierge and lifestyle management for international clients who expect discretion, responsiveness and seamless execution in Ibiza.</p><div class="hero-actions"><a class="btn gold" href="{WA}">Request Private Concierge</a><a class="btn ghost" href="/services/">Explore Private Services</a></div><div class="hero-proof"><span>Ibiza-based coordination</span><span>Private client support</span><span>One dedicated contact</span></div></div></section>
<section class="intro editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>One contact.<br>An entire island handled.</h2></div><div><p class="large">From arrival to departure, Ibiza VIP Move coordinates the people, places and logistics behind an exceptional stay.</p><p>Chauffeurs, villas, yachts, private aviation, dining, nightlife, security, staffing and bespoke requests can be aligned through one trusted Ibiza contact.</p><div class="micro-proof"><span><b>Local execution</b>Ibiza-based coordination.</span><span><b>Private network</b>Selected suppliers and partners.</span><span><b>One point of contact</b>Every moving part aligned.</span></div></div></section>
<section class="service-showcase home-six"><div class="section-head"><div class="kicker light">Private Services</div><h2>Ibiza, coordinated around you.</h2><p>Six service universes on the homepage. The full specialist service architecture remains available for search and detailed planning.</p></div><div class="service-grid-cards">{six}</div><div class="center-link"><a class="btn ghost" href="/services/">View all private services</a></div></section>
<section class="execution-band"><div class="execution-copy"><div class="kicker dark">How we work</div><h2>One itinerary.<br>Every moving part aligned.</h2><p class="large">A complex stay can involve aviation, several vehicles, villa access, yacht timings, restaurant reservations, security and changing guest movements.</p><p>Our role is to keep those dependencies connected through a single brief and a clear line of communication. When a time changes, the rest of the plan can be reviewed around it.</p></div><div class="execution-flow"><div><span>01</span><b>Brief</b><p>Dates, guests, priorities, privacy and non-negotiables.</p></div><div><span>02</span><b>Align</b><p>Transport, stays, access and suppliers mapped around the itinerary.</p></div><div><span>03</span><b>Coordinate</b><p>Confirmed details kept together through one contact.</p></div><div><span>04</span><b>Adapt</b><p>When plans move, the connected elements are reviewed with them.</p></div></div></section>
<section class="private-office-feature"><div class="private-office-media"><img src="/assets/images/security.jpg" alt="Discreet private client support and close protection coordination in Ibiza" loading="lazy" decoding="async" width="1600" height="1100"></div><div class="private-office-copy"><div class="kicker light">Private Office</div><h2>For requirements that go beyond reservations.</h2><p>High-touch Ibiza support for principals, families, personal assistants and family offices requiring discretion, responsiveness and complete local coordination.</p><div class="office-types"><span><b>Principals & Families</b>Complex private stays coordinated end-to-end.</span><span><b>Personal Assistants</b>A dependable Ibiza contact behind changing requests.</span><span><b>Family Offices</b>Local execution across mobility, hospitality and lifestyle.</span></div><a class="btn gold" href="/private-office/">Explore Private Office</a></div></section>
<section class="editorial speed-block"><div><div class="kicker dark">The Ibiza VIP Move approach</div><h2>Ibiza moves quickly.<br>Your concierge should move faster.</h2></div><div><p class="large">Flights move. Guests arrive early. Weather changes yacht days. Reservations evolve. Priorities shift.</p><p>Our value is not simply making reservations. It is keeping the stay aligned when the plan changes — quietly, precisely and with as little friction for the client as possible.</p><a class="text-link" href="/about/">About Ibiza VIP Move →</a></div></section>
<section class="intelligence-home"><div class="section-head"><div class="kicker dark">Ibiza Intelligence</div><h2>Private insight for exceptional stays.</h2><p>Practical planning notes for clients, assistants and travel professionals coordinating Ibiza at a high level.</p></div><div class="intelligence-grid"><a class="intel-card" href="/ibiza-intelligence/private-arrival/"><span>01 · Arrival</span><h3>The Private Arrival</h3><p>How aviation, luggage, chauffeur and villa readiness connect before the principal lands.</p><b>Read intelligence →</b></a><a class="intel-card" href="/ibiza-intelligence/ibiza-formentera-yacht-day/"><span>02 · At Sea</span><h3>Ibiza & Formentera by Yacht</h3><p>Planning the yacht day around marina timing, transport, dining and the evening that follows.</p><b>Read intelligence →</b></a><a class="intel-card" href="/ibiza-intelligence/ibiza-august-planning/"><span>03 · Peak Season</span><h3>The August Brief</h3><p>What deserves to be arranged early when Ibiza is operating at maximum demand.</p><b>Read intelligence →</b></a></div><div class="center-link dark-link"><a class="btn dark" href="/ibiza-intelligence/">Explore Ibiza Intelligence</a></div></section>
<section class="partners-strip"><div><div class="kicker dark">Travel Trade & Private Offices</div><h2>Your Ibiza operator, on the ground.</h2><p>We support personal assistants, family offices, luxury travel advisors, concierge companies and hospitality partners requiring reliable local execution for their clients — client-facing or discreetly behind the scenes.</p></div><a class="btn dark" href="/partners/">Partner with Ibiza VIP Move</a></section>
<section class="closing-cta private-brief" style="--hero:url('/assets/images/events.jpg')"><div><div class="kicker light">Your private brief</div><h2>Tell us what Ibiza<br>needs to look like.</h2><p>Share the essentials. We will continue the conversation privately and clarify the moving parts that matter.</p><div class="hero-actions"><a class="btn gold" href="/contact/">Send Private Brief</a><a class="btn ghost" href="{WA}">WhatsApp Concierge</a></div></div></section>'''


def article_body(kicker, title, intro, sections):
    body = [f'''<section class="page-hero intelligence-hero" style="--hero:url('/assets/images/hero.jpg')"><div><div class="kicker light">Ibiza Intelligence · {kicker}</div><h1>{title}</h1><p>{intro}</p></div></section><article class="article-shell"><div class="article-meta"><span>Ibiza VIP Move</span><span>Private planning note</span><span>Ibiza · Spain</span></div><div class="article-body">''']
    for heading, paragraphs in sections:
        body.append(f'<section><h2>{heading}</h2>')
        for p in paragraphs:
            body.append(f'<p>{p}</p>')
        body.append('</section>')
    body.append(f'''<aside class="article-cta"><div class="kicker dark">Private assistance</div><h2>Need this coordinated around a real itinerary?</h2><p>Share dates, guests and the moving parts already confirmed. Ibiza VIP Move can clarify the dependencies and continue privately.</p><a class="btn dark" href="{WA}">Speak to Concierge</a></aside></div></article>''')
    return ''.join(body)


def make_page_from_home(template, path, title, desc, main_html, og_image='/assets/images/hero.jpg'):
    text = template
    text = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', text, count=1)
    text = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{BASE}{path}">', text, count=1)
    text = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', text, count=1)
    text = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', text, count=1)
    text = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{BASE}{path}">', text, count=1)
    text = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{BASE}{og_image}">', text, count=1)
    text = re.sub(r'<link[^>]+hreflang="[^"]+"[^>]*>', '', text)
    text = re.sub(r'<main>.*?</main>', f'<main>{main_html}</main>', text, count=1, flags=re.S)
    page_schema = json.dumps({
        '@context': 'https://schema.org', '@type': 'WebPage', 'name': title,
        'url': BASE + path, 'description': desc,
        'isPartOf': {'@type': 'WebSite', 'url': BASE + '/', 'name': 'Ibiza VIP Move'},
        'about': {'@type': 'Organization', 'name': 'Ibiza VIP Move', 'url': BASE + '/'}
    }, ensure_ascii=False)
    text = text.replace('</head>', f'<script type="application/ld+json">{page_schema}</script></head>', 1)
    return text


def add_sitemap_urls(paths):
    sitemap = ROOT / 'sitemap.xml'
    if not sitemap.exists():
        return
    text = sitemap.read_text(encoding='utf-8')
    additions = []
    for path in paths:
        url = BASE + path
        if url not in text:
            additions.append(f'<url><loc>{url}</loc></url>')
    if additions:
        text = text.replace('</urlset>', ''.join(additions) + '</urlset>')
        sitemap.write_text(text, encoding='utf-8')


update_english_navigation()
home_path = ROOT / 'index.html'
home = home_path.read_text(encoding='utf-8')
home = replace_nav(home)
home = re.sub(r'<main>.*?</main>', f'<main>{home_main()}</main>', home, count=1, flags=re.S)
home_path.write_text(home, encoding='utf-8')

# Use the updated home as a fully post-processed shell for new English pages.
template = home_path.read_text(encoding='utf-8')

private_office = f'''<section class="page-hero office-hero" style="--hero:url('/assets/images/security.jpg')"><div><div class="kicker light">Private Office · Ibiza</div><h1>Local execution for<br><em>complex private stays.</em></h1><p>High-touch Ibiza support for principals, families, personal assistants, family offices and professional partners who need one dependable point of coordination on the island.</p></div></section><section class="editorial"><div><div class="kicker dark">Private Office</div><h2>Beyond bookings.<br>Built around the brief.</h2></div><div><p class="large">The more complex the stay, the more valuable a single line of coordination becomes.</p><p>Private Office is designed for briefs involving several guests, multiple vehicles, private aviation, villa operations, yacht movements, dining, security, staffing or evolving schedules. The service is coordination-led: priorities are clarified, dependencies are mapped and confirmed elements are kept aligned as the itinerary develops.</p></div></section><section class="dark-panel"><div class="kicker light">Who it is for</div><h2>Support behind the principal.</h2><div class="trust-grid"><div><b>Principals & Families</b><p>Private stays requiring discretion, responsiveness and several connected services.</p></div><div><b>Personal Assistants</b><p>One Ibiza-based contact to reduce fragmented supplier communication.</p></div><div><b>Family Offices</b><p>Local execution across mobility, hospitality, lifestyle and selected security requirements.</p></div><div><b>Travel Professionals</b><p>On-the-ground support that can work client-facing or discreetly behind the scenes.</p></div></div></section><section class="execution-band"><div class="execution-copy"><div class="kicker dark">Working model</div><h2>Clear brief.<br>Controlled execution.</h2><p>We start with what is known, identify what is dependent on something else and confirm the operating order before the stay. Changes are then handled against the same brief rather than as isolated requests.</p></div><div class="execution-flow"><div><span>01</span><b>Principal brief</b><p>Dates, guests, privacy, priorities and communication preferences.</p></div><div><span>02</span><b>Dependencies</b><p>Flights, vehicles, villa access, marina times and reservations mapped together.</p></div><div><span>03</span><b>Confirmations</b><p>Key details consolidated so the assistant or principal has one operating picture.</p></div><div><span>04</span><b>Live coordination</b><p>Adjustments handled with awareness of the rest of the itinerary.</p></div></div></section><section class="editorial privacy-note"><div><div class="kicker dark">Discretion</div><h2>Privacy is part of the operating model.</h2></div><div><p class="large">Private client information should be shared only to the extent required to coordinate the requested service.</p><p>We do not publish client identities or private itineraries as marketing material without explicit authorization. Professional partners can discuss the preferred client-facing or behind-the-scenes role before a brief is accepted.</p><a class="text-link" href="/partners/">For travel trade & partners →</a></div></section><section class="closing-cta private-brief" style="--hero:url('/assets/images/aviation.jpg')"><div><div class="kicker light">Private Office Brief</div><h2>Share the moving parts.<br>We will help align them.</h2><div class="hero-actions"><a class="btn gold" href="/contact/">Send Private Brief</a><a class="btn ghost" href="{WA}">WhatsApp Concierge</a></div></div></section>'''

intel_hub = '''<section class="page-hero intelligence-hero" style="--hero:url('/assets/images/yacht.jpg')"><div><div class="kicker light">Ibiza Intelligence</div><h1>Local knowledge,<br><em>built for private planning.</em></h1><p>Practical notes on the dependencies behind an exceptional Ibiza stay — written for clients, assistants and travel professionals.</p></div></section><section class="editorial"><div><div class="kicker dark">Planning intelligence</div><h2>Less generic advice.<br>More useful coordination.</h2></div><div><p class="large">Ibiza is simple when each booking is viewed alone. Complexity appears when flights, villas, vehicles, marinas, restaurants and changing guest plans need to work together.</p><p>Ibiza Intelligence focuses on those operational connections: what should be decided early, what depends on timing and where a small planning detail can affect the rest of the day.</p></div></section><section class="intelligence-home hub"><div class="intelligence-grid"><a class="intel-card" href="/ibiza-intelligence/private-arrival/"><span>Arrival</span><h3>The Private Arrival</h3><p>Flight to villa: the coordination points that deserve attention before landing.</p><b>Read →</b></a><a class="intel-card" href="/ibiza-intelligence/ibiza-formentera-yacht-day/"><span>At Sea</span><h3>Ibiza & Formentera by Yacht</h3><p>How to connect marina timing, transport, lunch and the evening plan.</p><b>Read →</b></a><a class="intel-card" href="/ibiza-intelligence/ibiza-august-planning/"><span>Peak Season</span><h3>The August Brief</h3><p>What to prioritize when demand, traffic and availability are at their highest.</p><b>Read →</b></a></div></section><section class="closing-simple"><h2>Planning a complex stay?</h2><p>Use the intelligence as a starting point, then share the actual brief privately.</p><a class="btn dark" href="/contact/">Request Concierge</a></section>'''

pages = {
    '/private-office/': ('Private Office Ibiza | Principals, PAs & Family Offices | Ibiza VIP Move', 'Private Office support in Ibiza for principals, families, personal assistants, family offices and luxury travel professionals requiring discreet local coordination.', private_office, '/assets/images/security.jpg'),
    '/ibiza-intelligence/': ('Ibiza Intelligence | Private Travel Planning | Ibiza VIP Move', 'Private Ibiza planning intelligence for clients, personal assistants and travel professionals covering arrivals, yachts, peak season and connected logistics.', intel_hub, '/assets/images/yacht.jpg'),
}

articles = {
    '/ibiza-intelligence/private-arrival/': (
        'Private Arrival Ibiza | Flight, Chauffeur & Villa Coordination',
        'How to coordinate a private or commercial arrival in Ibiza across flight timing, luggage, chauffeur pickup, villa access and onward plans.',
        article_body('Arrival', 'The Private Arrival', 'The arrival is the first point where several parts of an Ibiza stay meet at once. A small timing mismatch can affect vehicles, villa access, luggage and the first reservation of the day.', [
            ('Start with the arrival facts', ['Confirm the flight number or private aviation movement, expected passengers, luggage volume, children or mobility needs, and the final destination. For private aviation, identify the handling or terminal details available from the flight team. For commercial arrivals, clarify the meeting preference and who should be the primary contact once the aircraft lands.', 'The vehicle plan should be based on people and luggage, not only passenger count. A party that fits into one vehicle may still require additional luggage capacity.']),
            ('Connect the airport to the villa', ['Villa access is a dependency, not a separate booking. The arrival window, key handover, staff readiness and exact access instructions should be clear before the chauffeur leaves the airport.', 'If several guests arrive on different flights, decide whether the priority is individual pickups, consolidation, or keeping one vehicle available for later movements.']),
            ('Protect the first hours of the stay', ['Avoid scheduling an inflexible reservation too close to an arrival unless the client explicitly accepts the risk. Flight delays, baggage delivery and island traffic can compress the first afternoon quickly.', 'When dining, yacht embarkation or another timed activity follows the arrival, those timings should be considered in the transport brief from the beginning.']),
            ('What a useful arrival brief contains', ['A strong brief includes flight details, passenger names or count as required, luggage, destination, villa access contact, communication preference, onward reservations and any privacy or security requirements. Keeping those facts together reduces fragmented messages on arrival day.'])
        ]), '/assets/images/aviation.jpg'),
    '/ibiza-intelligence/ibiza-formentera-yacht-day/': (
        'Ibiza to Formentera Yacht Day | Private Planning Guide',
        'Plan an Ibiza and Formentera yacht day around marina timing, chauffeur transfers, restaurant plans, weather and the evening itinerary.',
        article_body('At Sea', 'Ibiza & Formentera by Yacht', 'A yacht day is rarely just a yacht booking. The experience depends on how the villa departure, marina, route, lunch, return time and evening plan connect.', [
            ('Work backwards from the whole day', ['Start with the evening. If guests have a dinner or nightlife reservation, define the realistic return window before choosing how late the yacht day should run.', 'Then work backwards through disembarkation, marina transfer, villa reset time and the morning pickup. This prevents the yacht day from consuming the evening unintentionally.']),
            ('Marina timing matters', ['Allow time between villa pickup and embarkation. Ibiza traffic, marina access and walking from the vehicle drop point can all add friction. The driver should know the marina, vessel or meeting point and the operating contact where possible.', 'For groups, luggage, beach bags, children or multiple vehicles, the embarkation plan deserves more detail than a simple pickup address.']),
            ('Formentera lunch should fit the route', ['Lunch timing and location should make sense with the vessel route and sea conditions. A reservation that looks perfect in isolation can create unnecessary backtracking or compress swimming time.', 'The yacht operator or captain remains the authority on safe routing and weather. Concierge planning should work around that operational guidance, not against it.']),
            ('Keep the return flexible enough', ['Weather and sea conditions can change. Build enough margin before an important dinner or event, and keep the chauffeur team informed of the expected return window.', 'A good yacht day feels unhurried because the land-side logistics were planned before departure.'])
        ]), '/assets/images/yacht.jpg'),
    '/ibiza-intelligence/ibiza-august-planning/': (
        'Ibiza in August | Private Concierge Planning Guide',
        'A private planning guide to Ibiza in August covering villas, chauffeurs, yachts, dining, nightlife, traffic and last-minute changes during peak demand.',
        article_body('Peak Season', 'The August Brief', 'August rewards preparation. The island is operating at high demand, traffic is heavier and the cost of changing a plan late is often lost flexibility rather than simply a higher price.', [
            ('Secure the structural pieces first', ['Start with the elements that affect the rest of the stay: accommodation, core transport coverage, yacht days, major dining priorities and any important event or nightlife dates.', 'Once those anchors are clear, secondary reservations can be arranged around them instead of creating conflicts.']),
            ('Transport is part of the itinerary', ['In peak season, distance on a map is not the same as travel time. Villa access, beach traffic, marina areas and nightlife departures can all add variability.', 'For a busy itinerary, chauffeur coverage should be planned around the day as a whole rather than treating every movement as an isolated transfer.']),
            ('Leave controlled flexibility', ['Not every hour needs to be booked months in advance. The useful goal is to secure the hard-to-replace elements while keeping enough space to adapt to weather, energy levels and changing preferences.', 'A concierge brief should distinguish non-negotiables from preferences. That makes last-minute decision-making much faster.']),
            ('Use one source of truth', ['For groups, personal assistants or several suppliers, keep the latest confirmed timings in one operating itinerary. When a flight, yacht or reservation changes, update the connected movements at the same time.', 'Peak season becomes much easier when changes are coordinated rather than passed separately between guests, drivers, venues and suppliers.'])
        ]), '/assets/images/hero.jpg'),
}

pages.update(articles)
for route, (title, desc, main_html, image) in pages.items():
    target = ROOT / route.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(make_page_from_home(template, route, title, desc, main_html, image), encoding='utf-8')

add_sitemap_urls(list(pages.keys()))
print(f'Phase 11 complete: redesigned home + {len(pages)} new indexable pages')
