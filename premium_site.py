from pathlib import Path
from html import escape
import json

BASE='https://ibizavipmove.com'
PHONE='+34 613 75 62 11'
WA='https://wa.me/34613756211'
EMAIL='partnership@ibizavipmove.com'

IMG={
'hero':'https://images.unsplash.com/photo-1757439402359-aed14d39fc1b?auto=format&fit=crop&w=2400&q=88',
'villa':'https://images.unsplash.com/photo-1757439402359-aed14d39fc1b?auto=format&fit=crop&w=2200&q=88',
'yacht':'https://www.charteranddreams.com/wp-content/uploads/2024/01/a-gran-abe.jpg',
'aviation':'https://tempusmagazine.co.uk/app/uploads/news_images/9440624415.jpg',
'chauffeur':'https://admin.londonvipchauffeur.co.uk/uploads/mercedes_benz_v_class_chauffeur_driver_5a5bdd584e.jpg',
'nightlife':'https://www.lucasfox.es/blog-images/containers/assets/blog/ibiza-beach-club-%282%29.png/945bd1461891e4848aeda100d02ad638/ibiza-beach-club-%282%29.png',
'security':'https://www.kleininvestigations.com/wp-content/uploads/2019/07/personal-protection-800x1035.jpg',
'chef':'https://www.tombenzon.com/media/pages/blog/the-art-of-in-villa-dining-securin/e42c0fe7b0-1775741021/hero-the-art-of-in-villa-dining-securin-1000x562-crop-50-50.jpg',
'events':'https://www.almabeachibiza.es/img/article-eventos.jpg',
'cars':'https://cdn.prod.website-files.com/675442d885557b7a328aa0aa/69813fcc610f09fb2962f68b_Luxury%20Shopping%20Trip%20Chauffeur%20in%20Mercedes%20V%20Class-m%402x.jpg',
'wellness':'https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=2200&q=88',
'bespoke':'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2200&q=88'
}

SERVICES=[
('private-chauffeur-ibiza','Private Chauffeur & Transportation','Luxury mobility, handled impeccably.','chauffeur',['Airport & private aviation transfers','Hourly and full-day chauffeur','Villa, hotel, marina and nightlife transport','Multi-vehicle and group coordination']),
('luxury-villas-ibiza','Luxury Villas & Private Stays','The right setting for an exceptional stay.','villa',['Curated villa sourcing','Pre-arrival preparation','Housekeeping & maintenance coordination','In-villa lifestyle support']),
('yacht-charter-ibiza','Yachts & Charters','Ibiza and Formentera from the water.','yacht',['Luxury yachts and day charters','Crew & marina coordination','On-board catering and experiences','Beach club and restaurant planning']),
('private-aviation-ibiza','Private Aviation','Smooth coordination around every flight.','aviation',['Private jet support','FBO and airport handling coordination','Arrival & departure alignment','Ground transport and luggage support']),
('restaurants-nightlife-ibiza','Restaurants, Beach Clubs & Nightlife','Access where it matters.','nightlife',['Restaurant reservations','VIP tables and bottle service','Beach clubs and daybeds','Nightlife planning and transport']),
('private-security-ibiza','Security & Close Protection','Discreet support for private clients.','security',['Close protection','Private client security','Event and nightlife support','Security transport coordination']),
('private-chef-staffing-ibiza','Private Chefs & Villa Staffing','Elevate the experience at home.','chef',['Private chefs','Butlers and waiters','Housekeeping coordination','Nannies and family support']),
('luxury-car-rental-ibiza','Luxury & Supercar Rental','The right car for every moment.','cars',['Luxury SUVs and executive vehicles','Sports and supercars','Delivery to villa, hotel or marina','Concierge-led vehicle coordination']),
('wellness-ibiza','Wellness & Beauty','Private wellbeing, brought to you.','wellness',['Massage and spa treatments','Personal trainers and yoga','Hair, makeup and beauty','Recovery and wellness sessions']),
('private-events-ibiza','Private Events & Celebrations','Beautiful moments, precisely executed.','events',['Villa dinners and celebrations','Proposals and private occasions','Entertainment and DJ coordination','Production, décor and guest logistics']),
('bespoke-concierge-ibiza','Lifestyle & Bespoke Requests','Whatever you need, handled discreetly.','bespoke',['Personal shopping and gifts','Last-minute sourcing','Special access and reservations','Tailor-made requests'])
]

NAV=[('Services','/services/'),('Concierge','/private-concierge-ibiza/'),('Partners','/partners/'),('About','/about/'),('Contact','/contact/')]

def head(title,desc,path,img=None):
    url=BASE+path; img=img or IMG['hero']
    schema={"@context":"https://schema.org","@type":"ProfessionalService","name":"Ibiza VIP Move","url":BASE,"telephone":PHONE,"email":EMAIL,"areaServed":"Ibiza, Spain","description":desc}
    return f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/premium.css?v=1"><script type="application/ld+json">{json.dumps(schema)}</script></head>'''

def header():
    links=''.join(f'<a href="{u}">{n}</a>' for n,u in NAV)
    return f'''<header class="site-header"><a class="wordmark" href="/"><span class="mark">IVM</span><span><strong>IBIZA VIP MOVE</strong><small>PRIVATE CONCIERGE · IBIZA</small></span></a><nav>{links}<a class="nav-cta" href="{WA}">Request Concierge</a></nav><button class="menu-btn" aria-label="Open menu">Menu</button></header><div class="mobile-menu"><a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Partners</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="{WA}">WhatsApp Concierge</a></div>'''

def footer():
    return f'''<footer><div class="footer-grid"><div><div class="footer-brand">IBIZA VIP MOVE</div><p>Private concierge, chauffeur and lifestyle management in Ibiza. One trusted point of contact for an effortless stay.</p></div><div><h4>Contact</h4><a href="tel:+34613756211">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}">WhatsApp Concierge</a></div><div><h4>Explore</h4><a href="/services/">Services</a><a href="/partners/">Travel Partners</a><a href="/about/">About</a><a href="/contact/">Request Concierge</a></div></div><div class="footer-bottom"><span>© 2026 Ibiza VIP Move</span><span>Discretion · Precision · Ibiza</span></div></footer><div class="mobile-bar"><a href="tel:+34613756211">Call</a><a href="{WA}">WhatsApp</a></div><script src="/assets/premium.js?v=1"></script>'''

def shell(body,title,desc,path,img=None):
    return '<!doctype html><html lang="en">'+head(title,desc,path,img)+f'<body>{header()}<main>{body}</main>{footer()}</body></html>'

def cards():
    out=[]
    for slug,name,tag,img,items in SERVICES:
        out.append(f'''<a class="service-card" href="/{slug}/"><div class="service-card-img" style="background-image:linear-gradient(180deg,rgba(8,12,16,.05),rgba(8,12,16,.42)),url('{IMG[img]}')"></div><div class="service-card-copy"><span>Private Service</span><h3>{name}</h3><p>{tag}</p><b>Explore service →</b></div></a>''')
    return ''.join(out)

def home():
    body=f'''<section class="hero" style="--hero:url('{IMG['hero']}')"><div class="hero-shade"></div><div class="hero-content"><div class="kicker">The private side of Ibiza</div><h1>Exceptional Ibiza,<br><em>handled privately.</em></h1><p>Private concierge, luxury transportation and lifestyle management for clients who expect discretion, speed and seamless execution.</p><div class="hero-actions"><a class="btn gold" href="{WA}">Request Concierge</a><a class="btn ghost" href="/services/">Explore Services</a></div><div class="hero-proof"><span>24/7 private client support</span><span>Ibiza-based coordination</span><span>One dedicated contact</span></div></div></section><section class="intro editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>One trusted contact.<br>Every detail aligned.</h2></div><div><p class="large">We coordinate the moving parts of a high-level stay in Ibiza—from arrival and transport to villas, yachts, dining, private aviation, security, staffing and last-minute requests.</p><p>Our approach is personal, discreet and execution-led. You tell us what the stay needs to feel like; we coordinate the details around it.</p><a class="text-link" href="/private-concierge-ibiza/">Discover our concierge approach →</a></div></section><section class="service-showcase"><div class="section-head"><div class="kicker light">Private services</div><h2>Everything your stay may require.</h2><p>Curated access, local coordination and private client support across Ibiza.</p></div><div class="service-grid-cards">{cards()}</div></section><section class="levels editorial"><div><div class="kicker dark">Concierge levels</div><h2>From a single reservation<br>to full-stay management.</h2></div><div class="level-list"><article><span>01</span><h3>Arrival</h3><p>Airport, chauffeur, villa readiness and essential reservations aligned before landing.</p></article><article><span>02</span><h3>Signature Stay</h3><p>Full-stay coordination across transport, dining, yachts, nightlife, staffing and lifestyle.</p></article><article><span>03</span><h3>Private Office</h3><p>High-touch support for principals, PAs, family offices, travel advisors and complex itineraries.</p></article></div></section><section class="dark-panel"><div class="kicker light">Designed for privacy</div><h2>Quietly capable.<br>Precisely connected.</h2><div class="trust-grid"><div><b>Local execution</b><p>Ibiza-based coordination with a carefully selected network.</p></div><div><b>Single point of contact</b><p>One line of communication across multiple services and suppliers.</p></div><div><b>Discreet handling</b><p>Private client information and requests handled with care.</p></div><div><b>Responsive support</b><p>Fast coordination when plans change or new needs appear.</p></div></div></section><section class="partners-strip"><div><div class="kicker dark">Travel trade & private offices</div><h2>On-the-ground support for your clients.</h2><p>We support personal assistants, family offices, luxury travel advisors, concierge companies and hospitality partners requiring a reliable Ibiza operator.</p></div><a class="btn dark" href="/partners/">Partner with us</a></section><section class="closing-cta" style="--hero:url('{IMG['events']}')"><div><div class="kicker light">Your Ibiza starts here</div><h2>Tell us what you need.<br>We’ll take it from there.</h2><a class="btn gold" href="{WA}">Speak to Concierge</a></div></section>'''
    return shell(body,'Ibiza VIP Move | Private Concierge & Luxury Lifestyle Management','Private concierge, chauffeur, villas, yachts, private aviation, security, nightlife and bespoke lifestyle management in Ibiza.','/',IMG['hero'])

def service_index():
    body=f'''<section class="page-hero" style="--hero:url('{IMG['nightlife']}')"><div><div class="kicker light">Ibiza VIP Move</div><h1>Private services,<br><em>without the friction.</em></h1><p>A complete private-client ecosystem for Ibiza, coordinated through one trusted contact.</p></div></section><section class="service-showcase compact"><div class="service-grid-cards">{cards()}</div></section><section class="closing-simple"><h2>Need several services coordinated together?</h2><p>Our concierge team can manage the full itinerary around your stay.</p><a class="btn dark" href="{WA}">Request Concierge</a></section>'''
    return shell(body,'Luxury Concierge Services in Ibiza | Ibiza VIP Move','Explore private chauffeur, villas, yachts, aviation, security, nightlife, staffing, wellness, events and bespoke concierge services in Ibiza.','/services/',IMG['nightlife'])

def service_page(slug,name,tag,img,items):
    content = {
        'private-chauffeur-ibiza': {
            'heading': 'Private chauffeur service built around your Ibiza itinerary.',
            'lead': 'Arrange an Ibiza private chauffeur for airport arrivals, hourly or full-day driving, villas, hotels, marinas, yacht connections, restaurants and nightlife. The route, timings, passengers, luggage and vehicle requirements are clarified before confirmation.',
            'detail': 'A chauffeur booking can cover one transfer or several movements under one brief. For complex stays, transport can be coordinated alongside reservations, security, private aviation and other concierge requirements.',
            'faqs': [
                ('Can I book a private driver by the hour in Ibiza?', 'Hourly, half-day, full-day and multi-day chauffeur requests can be assessed subject to the itinerary and confirmed availability. Share the dates, pickup points, estimated schedule, passengers and luggage.'),
                ('Do you coordinate Ibiza Airport transfers?', 'Yes. Airport pickup or departure transport can be included, with the flight, meeting point, destination, passengers and luggage confirmed before travel.'),
                ('Can the chauffeur cover villas, hotels, yachts and clubs?', 'Yes. A confirmed itinerary may include villas, hotels, marinas, yacht connections, restaurants, beach clubs and nightlife venues across Ibiza.'),
            ],
        },
        'luxury-villas-ibiza': {
            'heading': 'Luxury villa concierge from selection to daily support.',
            'lead': 'Coordinate an Ibiza villa stay around the guests, preferred area, dates, privacy requirements and the services needed before arrival. Requests may include villa sourcing, provisioning, housekeeping, chefs, wellness, chauffeur transport and guest logistics.',
            'detail': 'We focus on the complete stay rather than a property alone. Availability, terms and supplier details are confirmed for the specific request before any reservation is accepted.',
            'faqs': [
                ('Can you help source a luxury villa in Ibiza?', 'Villa requests can be assessed around dates, guest count, preferred areas, room requirements, amenities and budget. Suitable options and applicable terms are confirmed for the brief.'),
                ('Can you prepare the villa before arrival?', 'Pre-arrival requests may include provisioning, housekeeping, staffing, transport planning and other practical details, subject to confirmation.'),
                ('Can villa concierge be combined with a chauffeur or yacht?', 'Yes. Villa support can be coordinated with private chauffeur transport, yacht requests, dining, wellness, staffing and other services under one itinerary.'),
            ],
        },
        'yacht-charter-ibiza': {
            'heading': 'Ibiza yacht charter coordinated around the full day.',
            'lead': 'Plan a private yacht or day charter from Ibiza with the guest count, preferred date, departure marina, route, vessel style and onboard requirements clarified before options are presented.',
            'detail': 'The yacht day can be aligned with villa or hotel pickup, marina timing, catering requests, restaurant plans and the return journey. Formentera can be requested where suitable for the confirmed charter and conditions.',
            'faqs': [
                ('Can you arrange a yacht charter from Ibiza to Formentera?', 'Formentera routes can be requested. The vessel, marina, schedule, route and operating conditions must be confirmed for the selected charter.'),
                ('Can transport to and from the marina be included?', 'Yes. Private chauffeur transport can be coordinated around the confirmed departure and return times.'),
                ('What information is needed for a yacht request?', 'Send the date, guest count, preferred duration, departure area, vessel preferences and any catering, restaurant or special requirements.'),
            ],
        },
        'private-aviation-ibiza': {
            'heading': 'Ground coordination around private aviation in Ibiza.',
            'lead': 'Align private aviation arrivals and departures with chauffeur transport, luggage requirements, villa or hotel movements and the wider client itinerary.',
            'detail': 'The flight reference, terminal or handling details, passenger count, luggage and ground destination are clarified with the relevant parties. Access and handling remain subject to the confirmed operator and airport procedures.',
            'faqs': [
                ('Can you coordinate a chauffeur with a private flight?', 'Yes. Ground transport can be planned around the confirmed flight information, passenger requirements and final destination.'),
                ('Do you provide aircraft handling?', 'We coordinate the concierge and ground elements of the brief. Aviation handling, airside access and operator services are subject to the relevant licensed providers and airport procedures.'),
                ('Can private aviation support be part of a full Ibiza itinerary?', 'Yes. It can be aligned with villas, yachts, security, staffing, reservations and on-island chauffeur requirements.'),
            ],
        },
        'restaurants-nightlife-ibiza': {
            'heading': 'Restaurant reservations, VIP tables and nightlife logistics.',
            'lead': 'Coordinate restaurant reservations, beach-club daybeds, VIP table requests and private transport around the guest profile, dates, party size and preferred atmosphere.',
            'detail': 'Access, minimum spend, deposits, cancellation terms and table location depend on the venue and date. Nothing is represented as confirmed until the venue or relevant supplier has accepted the request.',
            'faqs': [
                ('Can you book restaurant reservations in Ibiza?', 'Restaurant requests can be coordinated around the date, time, party size, dietary needs and preferred style. Availability and booking terms depend on the venue.'),
                ('Can you arrange VIP tables at Ibiza clubs?', 'VIP table requests can be submitted for the chosen date and party size. Availability, table position, minimum spend and entry conditions are confirmed by the venue.'),
                ('Can nightlife transport be coordinated as well?', 'Yes. Chauffeur transport can be planned around confirmed restaurant, beach-club and nightlife reservations.'),
            ],
        },
        'private-security-ibiza': {
            'heading': 'Discreet private security and close-protection coordination.',
            'lead': 'Security requests are assessed around the principal or family, dates, movements, venues, transport, events and any relevant risk or privacy considerations.',
            'detail': 'The final team, scope and operating plan depend on the brief and applicable requirements. Security can be coordinated with chauffeur movements, villas, nightlife, events and private aviation.',
            'faqs': [
                ('Can I request a bodyguard or close protection in Ibiza?', 'Private security and close-protection requests can be assessed for principals, families, events and scheduled movements. Share the dates, profile, itinerary and scope required.'),
                ('Can security travel with the client and chauffeur?', 'Secure transport coordination can be included where appropriate to the confirmed brief and operating plan.'),
                ('Is private security available for nightlife or events?', 'Nightlife and event support can be requested. Staffing, access, timing and scope must be confirmed for the specific venue and itinerary.'),
            ],
        },
        'private-chef-staffing-ibiza': {
            'heading': 'Private chefs and villa staff matched to the stay.',
            'lead': 'Coordinate private chefs, butlers, waiters, housekeeping and family support around the property, dates, guest count, service style and daily schedule.',
            'detail': 'Menus, dietary requirements, hours, staffing levels, access and working conditions are clarified before the service is confirmed.',
            'faqs': [
                ('Can you arrange a private chef at an Ibiza villa?', 'Private chef requests can be coordinated around dates, guest count, meal plan, dietary requirements, kitchen facilities and preferred service style.'),
                ('Can you organise additional villa staff?', 'Butlers, waiters, housekeeping and family-support requests can be assessed according to the property, schedule and required duties.'),
                ('Can staffing be coordinated for only one dinner?', 'Single occasions and longer stays can both be requested, subject to the specific brief and confirmed availability.'),
            ],
        },
        'luxury-car-rental-ibiza': {
            'heading': 'Luxury car rental selected around the client and itinerary.',
            'lead': 'Request executive cars, luxury SUVs, sports cars or supercars with delivery details, dates, driver requirements and preferred model category clarified in advance.',
            'detail': 'Vehicle availability, deposit, insurance, mileage, licence requirements and delivery terms depend on the selected supplier and booking.',
            'faqs': [
                ('Can a luxury car be delivered to my villa or hotel?', 'Delivery and collection can be requested for a confirmed Ibiza address, subject to the selected vehicle and supplier terms.'),
                ('Can I request a specific model?', 'A preferred make or model can be requested, although the exact vehicle remains subject to availability and written confirmation.'),
                ('Is a chauffeur available instead of self-drive rental?', 'Yes. If you prefer not to drive, request a private chauffeur service coordinated around the itinerary.'),
            ],
        },
        'wellness-ibiza': {
            'heading': 'Private wellness and beauty brought to your Ibiza stay.',
            'lead': 'Coordinate massage, yoga, personal training, hair, makeup, beauty and recovery sessions at a suitable villa or hotel around the guest schedule.',
            'detail': 'Practitioner availability, treatment suitability, access, setup and cancellation terms are confirmed for each request.',
            'faqs': [
                ('Can wellness services come to an Ibiza villa?', 'In-villa sessions can be requested where the property and service setup are suitable. Access and space requirements are confirmed beforehand.'),
                ('Can you coordinate hair and makeup for an event?', 'Hair, makeup and beauty requests can be planned around the event time, number of guests and preferred look.'),
                ('Can several wellness sessions be scheduled during a stay?', 'Yes. A multi-day schedule can be requested and aligned with the wider itinerary.'),
            ],
        },
        'private-events-ibiza': {
            'heading': 'Private events in Ibiza with the logistics aligned.',
            'lead': 'Coordinate villa dinners, celebrations, proposals and private occasions around the venue, guest count, timing, food, entertainment, production, décor and transport.',
            'detail': 'The event scope, property permissions, suppliers, sound restrictions and operational requirements must be confirmed before execution.',
            'faqs': [
                ('Can you organise a private villa event in Ibiza?', 'Villa event requests can be assessed around the property, permissions, guest count, timings and production requirements.'),
                ('Can you coordinate entertainment and a DJ?', 'Entertainment, DJs, sound, décor and production can be requested as part of the confirmed event brief.'),
                ('Can guest transport be included?', 'Yes. Chauffeur and multi-vehicle transport can be coordinated around arrivals, departures and the confirmed event schedule.'),
            ],
        },
        'bespoke-concierge-ibiza': {
            'heading': 'Bespoke concierge for requests that do not fit a standard menu.',
            'lead': 'Use one Ibiza contact for personal shopping, gifts, special sourcing, itinerary changes, access requests and other private-client needs.',
            'detail': 'We assess what is feasible, clarify the required timing and present the next step. Availability, access and supplier terms remain subject to confirmation.',
            'faqs': [
                ('What is a bespoke concierge request?', 'It is a private request that falls outside a standard service, such as sourcing, gifting, itinerary support or a time-sensitive local need.'),
                ('Can you help with last-minute requests?', 'Last-minute requests can be assessed, but feasibility and availability depend on the timing and requirement.'),
                ('Can bespoke support be added to full-stay concierge?', 'Yes. It can sit alongside transport, villas, yachts, dining, staffing and other confirmed services.'),
            ],
        },
    }
    page = content.get(slug, {
        'heading': 'Private coordination built around your schedule.',
        'lead': 'Every request is coordinated around the client, the itinerary and the level of support required.',
        'detail': 'Share the dates, guests, priorities and practical requirements so the relevant details can be clarified before confirmation.',
        'faqs': [],
    })
    bullets=''.join(f'<li>{x}</li>' for x in items)
    faq_html=''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in page['faqs'])
    body=f'''<section class="page-hero service-hero" style="--hero:url('{IMG[img]}')"><div><div class="kicker light">Ibiza VIP Move · Private Service</div><h1>{name}</h1><p>{tag}</p><a class="btn gold" href="{WA}">Request this service</a></div></section><section class="editorial service-detail"><div><div class="kicker dark">Private coordination</div><h2>{page['heading']}</h2></div><div><p class="large">{page['lead']}</p><p>{page['detail']}</p><ul class="premium-list">{bullets}</ul></div></section><section class="process"><div class="section-head"><div class="kicker dark">How it works</div><h2>Simple for you. Detailed behind the scenes.</h2></div><div class="process-grid"><article><span>01</span><h3>Brief</h3><p>Share dates, guests, preferences and priorities.</p></article><article><span>02</span><h3>Clarify</h3><p>We confirm the operational details needed for the request.</p></article><article><span>03</span><h3>Confirm</h3><p>Availability, scope and applicable terms are agreed in writing.</p></article><article><span>04</span><h3>Coordinate</h3><p>The service is aligned with the confirmed Ibiza itinerary.</p></article></div></section><section class="faq"><div class="section-head"><div class="kicker dark">Private client FAQ</div><h2>Before you book.</h2></div>{faq_html}<details><summary>Can this be combined with other Ibiza VIP Move services?</summary><p>Yes. Multiple confirmed services can be coordinated through one point of contact and aligned around the same itinerary.</p></details></section><section class="closing-simple"><h2>Request {name}</h2><p>Send the dates, guest count and practical requirements for a tailored response.</p><a class="btn dark" href="{WA}">WhatsApp Concierge</a></section>'''
    return shell(body,f'{name} in Ibiza | Ibiza VIP Move',f'{name} in Ibiza with private coordination, discreet support and tailored concierge service.',f'/{slug}/',IMG[img])

def concierge():
    body=f'''<section class="page-hero" style="--hero:url('{IMG['bespoke']}')"><div><div class="kicker light">Luxury Concierge Ibiza</div><h1>Private concierge in Ibiza,<br><em>managed as one.</em></h1><p>One dedicated contact coordinating chauffeur transport, restaurant reservations, VIP tables, villas, yachts, security, staff and the unexpected.</p><a class="btn gold" href="{WA}">Start your brief</a></div></section><section class="editorial"><div><div class="kicker dark">Our approach</div><h2>Less coordination for you.<br>More control behind the scenes.</h2></div><div><p class="large">Ibiza VIP Move is a private concierge for clients who do not want to manage separate suppliers throughout their stay. We centralise communication, align timing and keep the confirmed itinerary moving.</p><p>From a restaurant reservation or airport movement to a complex family, executive or multi-day stay, the service scales around the brief.</p><a class="text-link" href="/services/">Explore all Ibiza concierge services →</a></div></section><section class="dark-panel"><div class="kicker light">What we manage</div><h2>Arrival to departure.</h2><div class="trust-grid"><div><b>Before arrival</b><p>Villa readiness, chauffeur transport, reservations, provisioning and schedule alignment.</p></div><div><b>During the stay</b><p>Daily transport, dining, VIP tables, yacht days, nightlife, staff, wellness and evolving requests.</p></div><div><b>Complex logistics</b><p>Multiple guests, changing schedules, airport movements, security and multi-vehicle coordination.</p></div><div><b>Departure</b><p>Final transport, luggage timing and private aviation or commercial airport coordination.</p></div></div></section><section class="faq"><div class="section-head"><div class="kicker dark">Concierge FAQ</div><h2>Planning private services in Ibiza.</h2></div><details><summary>What can a private concierge arrange in Ibiza?</summary><p>Requests may include chauffeur transport, villas, yachts, private aviation support, restaurant reservations, VIP tables, beach clubs, security, private chefs, staffing, wellness, events and bespoke needs.</p></details><details><summary>Can I use the concierge for only one reservation?</summary><p>Yes. You can request one defined service or coordinate a complete stay through the same point of contact.</p></details><details><summary>Can a PA, family office or travel advisor contact you?</summary><p>Yes. International private-client representatives and travel partners can send the brief directly and agree the preferred communication structure.</p></details><details><summary>Are reservations or access guaranteed?</summary><p>No. Availability, access, deposits, minimum spend and supplier terms are confirmed for each request before it is treated as booked.</p></details></section><section class="closing-simple"><h2>Build your Ibiza brief.</h2><p>Send your dates, guests and priorities to begin.</p><a class="btn dark" href="{WA}">Speak to Concierge</a></section>'''
    return shell(body,'Private Concierge Ibiza | Ibiza VIP Move','High-touch private concierge and lifestyle management in Ibiza for private clients, PAs, family offices and travel advisors.','/private-concierge-ibiza/',IMG['bespoke'])

def about():
    body=f'''<section class="page-hero" style="--hero:url('{IMG['villa']}')"><div><div class="kicker light">About Ibiza VIP Move</div><h1>Local knowledge.<br><em>Private standards.</em></h1><p>A concierge built around discretion, responsiveness and precise on-island coordination.</p></div></section><section class="editorial"><div><div class="kicker dark">Who we are</div><h2>Ibiza, understood from the inside.</h2></div><div><p class="large">Ibiza VIP Move coordinates high-level private services for visitors who value time, privacy and a well-managed experience.</p><p>Our role is not to overwhelm clients with options. It is to understand the brief, select the right solution and manage the details with clarity.</p></div></section><section class="values-grid"><article><span>01</span><h3>Discretion</h3><p>Private requests stay private.</p></article><article><span>02</span><h3>Precision</h3><p>Timing, communication and logistics are treated seriously.</p></article><article><span>03</span><h3>Responsiveness</h3><p>Ibiza changes quickly. We stay available when plans do too.</p></article><article><span>04</span><h3>Quality over volume</h3><p>We prioritise the right solution over simply adding more suppliers.</p></article></section><section class="closing-simple"><h2>Experience Ibiza with less friction.</h2><a class="btn dark" href="{WA}">Request Concierge</a></section>'''
    return shell(body,'About Ibiza VIP Move | Private Concierge Ibiza','Learn about Ibiza VIP Move, a private concierge and lifestyle management service focused on discreet, precise on-island coordination.','/about/',IMG['villa'])

def partners():
    body=f'''<section class="page-hero" style="--hero:url('{IMG['aviation']}')"><div><div class="kicker light">B2B & Private Offices</div><h1>Your Ibiza operator,<br><em>on the ground.</em></h1><p>Private local execution for PAs, family offices, luxury travel advisors, concierge companies and hospitality partners.</p><a class="btn gold" href="mailto:{EMAIL}">Partner with us</a></div></section><section class="editorial"><div><div class="kicker dark">Partner support</div><h2>One local contact for complex client requests.</h2></div><div><p class="large">We help international partners execute Ibiza itineraries without having to coordinate each supplier separately.</p><ul class="premium-list"><li>White-label and direct client support</li><li>Chauffeur and group transport coordination</li><li>Villas, yachts, aviation and lifestyle requests</li><li>Fast WhatsApp communication</li><li>Discreet handling of principal and guest details</li><li>On-island issue resolution and itinerary support</li></ul></div></section><section class="closing-simple"><h2>Need a reliable Ibiza partner?</h2><p>Send your client brief or introduce your team.</p><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a></section>'''
    return shell(body,'Ibiza Concierge Partner for Travel Advisors & Family Offices | Ibiza VIP Move','B2B Ibiza concierge support for personal assistants, family offices, travel advisors, hospitality partners and international concierge companies.','/partners/',IMG['aviation'])

def contact():
    service_opts=''.join(f'<option>{n}</option>' for _,n,_,_,_ in SERVICES)
    body=f'''<section class="contact-hero"><div><div class="kicker dark">Request Concierge</div><h1>Tell us what your Ibiza needs to look like.</h1><p>Share the essentials and we’ll continue the conversation privately.</p></div><form id="conciergeForm"><label>Name<input id="fName" required></label><label>WhatsApp / Phone<input id="fPhone" required></label><div class="form-row"><label>Arrival<input id="fArrival" type="date"></label><label>Departure<input id="fDeparture" type="date"></label></div><label>Primary service<select id="fService"><option>Full Concierge</option>{service_opts}</select></label><label>Guests<input id="fGuests" type="number" min="1" placeholder="Number of guests"></label><label>Brief<textarea id="fBrief" rows="5" placeholder="Villa, transport, yacht, reservations, itinerary, special requests..."></textarea></label><button class="btn dark" type="submit">Send via WhatsApp</button><small>Submitting opens a private WhatsApp conversation with the details above.</small></form></section><section class="contact-direct"><div><span>WhatsApp</span><a href="{WA}">{PHONE}</a></div><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><span>Availability</span><strong>Private client support · Ibiza</strong></div></section>'''
    return shell(body,'Request Private Concierge in Ibiza | Ibiza VIP Move','Request private concierge, chauffeur, villa, yacht, aviation, security or bespoke lifestyle support in Ibiza.','/contact/',IMG['hero'])

def build():
    root=Path('_site'); root.mkdir(exist_ok=True)
    (root/'index.html').write_text(home(),encoding='utf-8')
    pages={'services':service_index(),'private-concierge-ibiza':concierge(),'about':about(),'partners':partners(),'contact':contact()}
    for slug,html in pages.items():
        d=root/slug; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(html,encoding='utf-8')
    for s,n,t,i,items in SERVICES:
        d=root/s; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(service_page(s,n,t,i,items),encoding='utf-8')
    urls=['/','/services/','/private-concierge-ibiza/','/about/','/partners/','/contact/']+[f'/{x[0]}/' for x in SERVICES]
    sm=''.join(f'<url><loc>{BASE}{u}</loc><changefreq>weekly</changefreq><priority>{"1.0" if u=="/" else "0.8"}</priority></url>' for u in urls)
    (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+sm+'</urlset>',encoding='utf-8')
    (root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://ibizavipmove.com/sitemap.xml\n',encoding='utf-8')
    (root/'CNAME').write_text('ibizavipmove.com\n',encoding='utf-8'); (root/'.nojekyll').write_text('',encoding='utf-8')

if __name__=='__main__': build()
