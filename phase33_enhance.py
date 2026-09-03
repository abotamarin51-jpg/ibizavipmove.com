from pathlib import Path
import re

ROOT = Path('_site')
STYLE = '/assets/phase33.css?v=33'
CSS_SRC = Path('phase33.css')
CSS_DEST = ROOT / 'assets' / 'phase33.css'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'), encoding='utf-8')

PAGES = {
    'private-office': {
        'kicker': 'Private Office · Ibiza',
        'h1': 'Your private office on the island.',
        'lead': 'For principals, families, personal assistants and family offices who need one discreet Ibiza-based point of contact behind a complex stay.',
        'rail': [
            ('Principals', 'Private handling', 'High-touch coordination around the principal and confirmed itinerary.'),
            ('PAs & EAs', 'One operational line', 'A single local contact for changing schedules and multiple services.'),
            ('Family Offices', 'Need-to-know detail', 'Private requests handled with clear scope and discreet communication.'),
            ('Complex stays', 'Arrival to departure', 'Transport, villas, access, aviation, security and lifestyle aligned together.'),
        ],
        'overview_kicker': 'Private client infrastructure',
        'overview_h2': 'Less supplier management. More control.',
        'overview_lead': 'The value is not another reservation. It is having one accountable local operator connecting the moving parts behind the stay.',
        'overview_p': 'Ibiza VIP Move supports principals and their representatives with practical, on-island coordination. The service can begin before arrival, continue throughout the stay and adapt when plans move.',
        'audiences': [('Principal & family','Private, high-touch local support'),('Personal assistant','One line for itinerary execution'),('Family office','Dependable on-island coordination'),('Executive assistant','Fast operational communication')],
        'cta_h2': 'Place Ibiza under one point of contact.',
        'cta_p': 'Send the dates, guest profile and the level of coordination required. We can continue the brief privately.',
    },
    'partners': {
        'kicker': 'B2B Partnerships · Ibiza',
        'h1': 'Your Ibiza operator, on the ground.',
        'lead': 'Local execution for luxury travel advisors, concierge companies, hospitality partners, PAs and international private-client teams.',
        'rail': [
            ('Travel advisors', 'Local execution', 'A dependable Ibiza point of contact behind your client itinerary.'),
            ('Concierge firms', 'Direct or discreet', 'Client-facing or behind-the-scenes support according to the agreed workflow.'),
            ('Hospitality', 'Connected logistics', 'Transport and private services coordinated around guest requirements.'),
            ('International teams', 'Fast communication', 'Clear WhatsApp and email coordination before and during the stay.'),
        ],
        'overview_kicker': 'Built for professional partners',
        'overview_h2': 'Protect the client relationship. Strengthen the execution.',
        'overview_lead': 'Your client should experience one seamless itinerary, not the complexity of coordinating separate Ibiza suppliers.',
        'overview_p': 'We support professional partners who need responsive local execution across transport, villas, yachts, aviation, dining, nightlife, security, staffing and bespoke requests. The communication structure is agreed around the partner and client brief.',
        'audiences': [('Luxury travel advisors','On-island execution for private clients'),('Concierge companies','Local support across multiple services'),('Hotels & hospitality','Private guest logistics and requests'),('PAs & private offices','Direct operational coordination')],
        'cta_h2': 'Need an Ibiza partner you can brief directly?',
        'cta_p': 'Introduce your team or send a live client request. We will clarify scope, availability and the preferred communication structure.',
    },
}


def rail(items):
    return '<div class="ivm-b2b-rail">' + ''.join(
        f'<article><span>{a}</span><strong>{b}</strong><small>{c}</small></article>' for a,b,c in items
    ) + '</div>'


def main(data):
    audiences = ''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a,b in data['audiences'])
    return f'''<main>
<section class="page-hero">
  <div class="page-hero-media"><img src="/assets/images/private-office.jpg" alt="Private Office and B2B concierge coordination in Ibiza" width="1800" height="1200" fetchpriority="high" decoding="async"></div>
  <div><div class="kicker light">{data['kicker']}</div><h1>{data['h1']}</h1><p>{data['lead']}</p><a class="btn gold" href="{WA}">Start a private brief</a>{rail(data['rail'])}</div>
</section>
<section class="ivm-b2b-overview"><div class="ivm-b2b-overview-inner">
  <div><div class="eyebrow">{data['overview_kicker']}</div><h2>{data['overview_h2']}</h2></div>
  <div><p class="lead">{data['overview_lead']}</p><p>{data['overview_p']}</p><div class="ivm-b2b-audiences">{audiences}</div></div>
</div></section>
<section class="ivm-b2b-operating"><div class="ivm-b2b-operating-inner">
  <div class="ivm-b2b-operating-head"><div><div class="eyebrow">Operating model</div><h2>Simple externally. Detailed behind the scenes.</h2></div><p>The partner or representative keeps one clear line of communication while the relevant confirmed services are coordinated around the same itinerary.</p></div>
  <div class="ivm-b2b-steps">
    <article><span>01 · Brief</span><h3>Send the essentials.</h3><p>Dates, guests, priorities, required services and the preferred client/partner communication structure.</p></article>
    <article><span>02 · Clarify</span><h3>Define the scope.</h3><p>Availability, timing, operational requirements and applicable supplier terms are clarified before confirmation.</p></article>
    <article><span>03 · Align</span><h3>Connect the itinerary.</h3><p>Confirmed transport, stays, access, aviation, security and other services are aligned around the same brief.</p></article>
    <article><span>04 · Support</span><h3>Stay responsive.</h3><p>If plans evolve, affected elements can be reviewed and re-coordinated through the same Ibiza point of contact.</p></article>
  </div>
</div></section>
<section class="ivm-b2b-cta"><div class="ivm-b2b-cta-inner"><div><h2>{data['cta_h2']}</h2><p>{data['cta_p']}</p></div><div class="ivm-b2b-actions"><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div></div></section>
</main>'''

for slug, data in PAGES.items():
    path = ROOT / slug / 'index.html'
    if not path.exists():
        raise SystemExit(f'Missing Phase 33 page: {slug}')
    html = path.read_text(encoding='utf-8')
    html, n = re.subn(r'<main>.*?</main>', main(data), html, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f'Unable to replace main on {slug}')
    body = re.search(r'<body(?:\s+class="([^"]*)")?>', html, re.I)
    if body:
        classes = (body.group(1) or '').split()
        if 'ivm-b2b-signature' not in classes:
            classes.append('ivm-b2b-signature')
        repl = '<body class="' + ' '.join(x for x in classes if x) + '">'
        html = html[:body.start()] + repl + html[body.end():]
    if STYLE not in html:
        html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
    path.write_text(html, encoding='utf-8')

# Validation.
assert CSS_DEST.exists() and CSS_DEST.stat().st_size > 5000
for slug in PAGES:
    html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
    assert 'ivm-b2b-signature' in html, slug
    assert STYLE in html, slug
    assert html.count('<h1') == 1, slug
    assert html.count('class="ivm-b2b-rail"') == 1, slug
    assert 'Operating model' in html, slug
    assert EMAIL in html and 'WhatsApp 24/7' in html, slug
    assert '<link rel="canonical"' in html, slug
    assert 'application/ld+json' in html, slug
print('PASS: Phase 33 Private Office and B2B partner conversion pages')
