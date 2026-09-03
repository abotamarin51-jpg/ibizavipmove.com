from pathlib import Path
import re

ROOT=Path('_site')
STYLE='/assets/phase40.css?v=40'
CSS_SRC=Path('phase40.css')
CSS_DEST=ROOT/'assets'/'phase40.css'
WA='https://wa.me/34600703303'

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'),encoding='utf-8')
page=ROOT/'services'/'index.html'
if not page.exists():raise SystemExit('Services page missing')
html=page.read_text(encoding='utf-8')

CORE=[
('Move','Private Chauffeur & Transportation','Private mobility aligned around arrivals, villas, marinas, restaurants, nightlife and full-day schedules.','/private-chauffeur-ibiza/','/assets/images/chauffeur.jpg'),
('Stay','Luxury Villas & Private Stays','Private stays coordinated around access, guest requirements, staffing and the rhythm of the itinerary.','/luxury-villas-ibiza/','/assets/images/villa.jpg'),
('Sea','Yachts & Charters','Ibiza and Formentera from the water, connected with marina timing, transport, dining and the rest of the day.','/yacht-charter-ibiza/','/assets/images/yacht.jpg'),
('Access','Restaurants, Beach Clubs & Nightlife','Reservations, VIP tables and private access coordinated with timings, transport and guest movements.','/restaurants-nightlife-ibiza/','/assets/images/nightlife.jpg'),
('Fly','Private Aviation','Flight, luggage and ground coordination aligned with onward transport and the confirmed Ibiza itinerary.','/private-aviation-ibiza/','/assets/images/aviation.jpg'),
('Protect','Security & Close Protection','Discreet private security support coordinated around the principal, movements, locations and schedule.','/private-security-ibiza/','/assets/images/security.jpg')]
EXT=[
('At Home','Private Chefs & Villa Staffing','Chefs, butlers, housekeeping and family support around the private stay.','/private-chef-staffing-ibiza/'),
('Drive','Luxury & Supercar Rental','Executive vehicles, SUVs, sports cars and discreet delivery.','/luxury-car-rental-ibiza/'),
('Wellness','Wellness & Beauty','Massage, trainers, yoga, beauty and private recovery sessions.','/wellness-ibiza/'),
('Occasions','Private Events & Celebrations','Private dinners, celebrations, entertainment and guest logistics.','/private-events-ibiza/'),
('Bespoke','Lifestyle & Bespoke Requests','Tailor-made sourcing, special requests and support outside standard categories.','/bespoke-concierge-ibiza/')]

index=''.join(f'<a href="{href}"><span>{label}</span><strong>{title.split(" & ")[0]}</strong><small>{copy.split(".")[0]}.</small></a>' for label,title,copy,href,_ in CORE)
core=''.join(f'<a class="ivm-core-card" href="{href}"><img src="{img}" alt="{title} in Ibiza — Ibiza VIP Move" loading="lazy" decoding="async" width="1800" height="1200"><div class="ivm-core-copy"><span>{label}</span><h3>{title}</h3><p>{copy}</p><b>Explore {label} →</b></div></a>' for label,title,copy,href,img in CORE)
ext=''.join(f'<a class="ivm-extended-card" href="{href}"><span>{label}</span><strong>{title}</strong><p>{copy}</p><b>Explore →</b></a>' for label,title,copy,href in EXT)

main=f'''<main id="main-content">
<section class="page-hero"><div class="page-hero-media"><img src="/assets/images/hero-desktop.jpg" alt="Ibiza VIP Move private concierge services in Ibiza" width="2200" height="1400" fetchpriority="high" decoding="async"></div><div><div class="kicker light">Private Services · Ibiza</div><h1>One private ecosystem.<br>Every moving part connected.</h1><p>Private mobility, stays, yachts, access, aviation, protection and lifestyle support coordinated through one trusted Ibiza contact.</p><a class="btn gold" href="/contact/">Request Concierge</a><div class="ivm-services-index">{index}</div></div></section>
<section class="ivm-core-services"><div class="ivm-core-head"><div><div class="eyebrow">Six core universes</div><h2>The structure behind an exceptional stay.</h2></div><p>Each service can be requested independently. When several are required, the value comes from connecting the timings, people and operational details around the same itinerary.</p></div><div class="ivm-core-grid">{core}</div></section>
<section class="ivm-extended"><div class="ivm-extended-inner"><div class="ivm-extended-head"><div><div class="eyebrow">Beyond the core</div><h2>Lifestyle support around the stay.</h2></div><p>The private brief often extends beyond transport, accommodation and access. These additional services can be coordinated when they are relevant to the client and confirmed itinerary.</p></div><div class="ivm-extended-grid">{ext}</div></div></section>
<section class="ivm-services-concierge"><div class="ivm-services-concierge-inner"><div><h2>Need several services handled together?</h2></div><div><p>Use the concierge rather than managing each category separately. Share dates, guests and priorities; we will clarify the moving parts and continue privately.</p><div class="ivm-services-actions"><a class="btn dark" href="/contact/">Start a Private Brief</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div></div></div></section>
</main>'''

html,n=re.subn(r'<main\b[^>]*>.*?</main>',main,html,count=1,flags=re.I|re.S)
if n!=1:raise SystemExit('Unable to replace Services main')
body=re.search(r'<body(?:\s+class="([^"]*)")?>',html,re.I)
if body:
    classes=(body.group(1) or '').split()
    if 'ivm-services-hub' not in classes:classes.append('ivm-services-hub')
    repl='<body class="'+' '.join(x for x in classes if x)+'">';html=html[:body.start()]+repl+html[body.end():]
if STYLE not in html:html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
page.write_text(html,encoding='utf-8')

final=page.read_text(encoding='utf-8')
assert CSS_DEST.exists() and CSS_DEST.stat().st_size>5000
assert STYLE in final and 'ivm-services-hub' in final
assert final.count('<h1')==1
for token in ('>Move<','>Stay<','>Sea<','>Access<','>Fly<','>Protect<','Private Chefs & Villa Staffing','Lifestyle & Bespoke Requests'):assert token in final,token
assert final.count('class="ivm-core-card"')==6
assert final.count('class="ivm-extended-card"')==5
assert '<link rel="canonical"' in final and 'application/ld+json' in final
assert 'id="main-content"' in final and 'ivm-skip-link' in final
print('PASS: Phase 40 Services hub reorganized into six core universes + extended lifestyle support')
