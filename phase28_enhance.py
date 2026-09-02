from pathlib import Path
import re

ROOT=Path('_site')
WA='https://wa.me/34600703303'
STYLE='/assets/reference-home.css?v=28'

# Deploy CSS final override.
(ROOT/'assets'/'reference-home.css').write_text(Path('reference-home.css').read_text(encoding='utf-8'),encoding='utf-8')

home_path=ROOT/'index.html'
home=home_path.read_text(encoding='utf-8')
if STYLE not in home:
    home=home.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)

icons={
'move':'<svg viewBox="0 0 64 40" aria-hidden="true"><path d="M9 28h46M14 27l4-10h27l6 10M22 17l5-7h14l5 7M18 31a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm28 0a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"/></svg>',
'stay':'<svg viewBox="0 0 64 48" aria-hidden="true"><path d="M9 40h46M14 40V18h15v22M29 40V9h21v31M18 24h7M18 30h7M35 16h8M35 23h8M35 30h8"/></svg>',
'sea':'<svg viewBox="0 0 64 44" aria-hidden="true"><path d="M8 29h47l-8 8H18l-10-8Zm18 0 6-10h11l5 10M37 19v-7M30 12h18M6 40c5-3 9 3 14 0s9 3 14 0 9 3 14 0 9 3 14 0"/></svg>',
'access':'<svg viewBox="0 0 64 48" aria-hidden="true"><path d="M20 41V18c0-8 5-13 12-13s12 5 12 13v23M25 41V19c0-5 3-8 7-8s7 3 7 8v22M14 41h36M47 31h7v10"/></svg>',
'fly':'<svg viewBox="0 0 64 44" aria-hidden="true"><path d="m6 25 22-4 11-15 5 1-7 13 16-3 6 4-23 7-7 11-4-1 2-9-14 4-7-8Z"/></svg>',
'protect':'<svg viewBox="0 0 64 48" aria-hidden="true"><path d="M32 4 48 10v12c0 11-6 18-16 23C22 40 16 33 16 22V10l16-6Zm0 8v23M24 23h16"/></svg>'}

services=[
('move','Move','Chauffeur, cars & ground experiences.','/private-chauffeur-ibiza/'),
('stay','Stay','Private villas & curated stays.','/luxury-villas-ibiza/'),
('sea','Sea','Yachts, charters & sea experiences.','/yacht-charter-ibiza/'),
('access','Access','Reservations, access & VIP experiences.','/restaurants-nightlife-ibiza/'),
('fly','Fly','Private aviation & flight support.','/private-aviation-ibiza/'),
('protect','Protect','Security, privacy & peace of mind.','/private-security-ibiza/')]
rail=''.join(f'<a class="ivm-ref-service" href="{href}"><span class="ivm-ref-icon">{icons[key]}</span><strong>{label}</strong><small>{copy}</small><b>Explore →</b></a>' for key,label,copy,href in services)

main=f'''<section class="ivm-ref-hero">
<picture class="ivm-ref-hero-picture"><source media="(max-width:700px)" srcset="/assets/images/hero-mobile.jpg"><img src="/assets/images/hero-desktop.jpg" alt="Cinematic Ibiza sunset over the Mediterranean" width="2200" height="1400" fetchpriority="high" decoding="async"></picture>
<div class="ivm-ref-hero-inner"><div class="ivm-ref-copy"><div class="kicker light">Private Concierge · Ibiza</div><h1>Exceptional Ibiza,<br>handled privately.</h1><div class="ivm-ref-rule"></div><p class="ivm-ref-sub">Discretion. Access. Excellence.<br>Your time is our highest standard.</p><div class="ivm-ref-actions"><a class="btn gold" href="/contact/">Request Concierge</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div></div><div class="ivm-ref-service-rail">{rail}</div></div>
</section>
<section class="ivm-ref-triptych">
<a class="ivm-ref-panel" href="/ibiza-intelligence/"><img src="/assets/images/nightlife.jpg" alt="The Ibiza Black Book private island intelligence" loading="lazy" decoding="async"><div class="ivm-ref-panel-copy"><div class="eyebrow">The Ibiza Black Book</div><h2>Insider knowledge.</h2><p>Seasonal access, local expertise and a curated view of the island.</p><span>Explore the Black Book →</span></div></a>
<a class="ivm-ref-panel ivory" href="/private-office/"><img src="/assets/images/private-office.jpg" alt="Private Office concierge coordination in Ibiza" loading="lazy" decoding="async"><div class="ivm-ref-panel-copy"><div class="eyebrow">Private Office</div><h2>One point of contact.</h2><p>For principals, PAs and family offices. Discreet, precise and always aligned.</p><span>Discover Private Office →</span></div></a>
<a class="ivm-ref-panel" href="/bespoke-concierge-ibiza/"><img src="/assets/images/bespoke.jpg" alt="Bespoke private concierge in Ibiza" loading="lazy" decoding="async"><div class="ivm-ref-panel-copy"><div class="eyebrow">Bespoke. Precise. Personal.</div><h2>Every detail managed.</h2><p>Every preference anticipated. Every request handled with discretion.</p><span>Our approach →</span></div></a>
</section>
<section class="ivm-ref-manifesto"><div class="ivm-ref-manifesto-inner"><div><div class="kicker dark">Ibiza VIP Move</div><h2>One trusted contact for the island.</h2></div><div><p>From airport to villa, marina to dinner, security to last-minute changes, Ibiza VIP Move keeps confirmed services connected through one clear line of communication.</p><p>Private chauffeur, villas, yachts, aviation, access and protection are coordinated around the stay rather than treated as isolated bookings.</p></div></div></section>
<section class="ivm-ref-final"><div class="ivm-ref-final-inner"><div><h2>Ready to experience Ibiza without limits?</h2><p>Our team is available around the clock.</p></div><div class="ivm-ref-actions"><a class="btn gold" href="/contact/">Request Concierge</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div></div></section>'''

home=re.sub(r'<main>.*?</main>',f'<main>{main}</main>',home,count=1,flags=re.I|re.S)
home_path.write_text(home,encoding='utf-8')

# Validation: final home composition only, all URLs already exist in previous validated phases.
check=home_path.read_text(encoding='utf-8')
assert check.count('<h1')==1
for token in ['Exceptional Ibiza,','Request Concierge','WhatsApp 24/7','>Move<','>Stay<','>Sea<','>Access<','>Fly<','>Protect<','The Ibiza Black Book','Private Office','Bespoke. Precise. Personal.']:
    assert token in check, token+' missing'
assert STYLE in check
assert (ROOT/'assets'/'reference-home.css').stat().st_size>5000
print('PASS: Phase 28 final reference-home composition')
