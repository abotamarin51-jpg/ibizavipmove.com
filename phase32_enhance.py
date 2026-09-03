from pathlib import Path
import re

ROOT = Path('_site')
STYLE = '/assets/phase32.css?v=32'
CSS_SRC = Path('phase32.css')
CSS_DEST = ROOT / 'assets' / 'phase32.css'
WA = 'https://wa.me/34600703303'
PHONE = '+34 600 703 303'
EMAIL = 'partnership@ibizavipmove.com'

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'), encoding='utf-8')

page = ROOT / 'contact' / 'index.html'
if not page.exists():
    raise SystemExit('Missing contact page')
html = page.read_text(encoding='utf-8')

# Preserve the existing header/footer, tracking and JSON-LD. Replace only the main contact experience.
services = [
    'Full Concierge',
    'Private Chauffeur & Transportation',
    'Luxury Villas & Private Stays',
    'Yachts & Charters',
    'Private Aviation',
    'Restaurants, Beach Clubs & Nightlife',
    'Security & Close Protection',
    'Private Chefs & Villa Staffing',
    'Luxury & Supercar Rental',
    'Wellness & Beauty',
    'Private Events & Celebrations',
    'Lifestyle & Bespoke Requests',
]
options = ''.join(f'<option>{x}</option>' for x in services)

main = f'''<main>
<section class="ivm-desk">
  <div class="ivm-desk-shell">
    <div class="ivm-desk-intro">
      <div class="eyebrow">Private Members Desk · Ibiza</div>
      <h1>Tell us what needs to happen.</h1>
      <p>Share the essentials. One private point of contact will continue the conversation and coordinate the next steps around your Ibiza stay.</p>
      <div class="ivm-desk-actions">
        <a class="btn gold" href="{WA}">WhatsApp 24/7</a>
        <a class="btn ghost" href="tel:+34600703303">Call Concierge</a>
      </div>
      <div class="ivm-desk-meta">
        <div><span>Private line</span><a href="tel:+34600703303">{PHONE}</a></div>
        <div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div><span>Coverage</span><strong>Ibiza · Private client support</strong></div>
      </div>
    </div>
    <div class="ivm-desk-form">
      <div class="ivm-desk-form-head">
        <div><div class="eyebrow">Private brief</div><h2>Start with the essentials.</h2></div>
        <p>You do not need to have the full itinerary ready. Dates, guests and the main requirement are enough to begin.</p>
      </div>
      <form id="conciergeForm">
        <label>Name<input id="fName" autocomplete="name" required></label>
        <label>WhatsApp / Phone<input id="fPhone" autocomplete="tel" required></label>
        <label>Arrival<input id="fArrival" type="date"></label>
        <label>Departure<input id="fDeparture" type="date"></label>
        <label class="full">Primary service<select id="fService"><option>Full Concierge</option>{options}</select></label>
        <label>Guests<input id="fGuests" type="number" min="1" inputmode="numeric" placeholder="Number of guests"></label>
        <label class="full">Private brief<textarea id="fBrief" rows="4" placeholder="Villa, transport, yacht, reservations, flight details, security, special requests..."></textarea></label>
        <div class="form-submit"><button class="btn dark" type="submit">Send Private Brief</button><small>Submitting opens a private WhatsApp conversation with the details above. Nothing is treated as confirmed until availability and terms are agreed.</small></div>
      </form>
    </div>
  </div>
  <div class="ivm-desk-trust">
    <article><span>01 · One contact</span><strong>Your brief stays connected.</strong><p>Multiple confirmed services can be coordinated through one line of communication.</p></article>
    <article><span>02 · Private handling</span><strong>Discretion by design.</strong><p>Only the operational details required for each confirmed request are shared.</p></article>
    <article><span>03 · Responsive support</span><strong>Plans can evolve.</strong><p>When timings or requirements change, the itinerary can be realigned around the new brief.</p></article>
  </div>
</section>
</main>'''

html, count = re.subn(r'<main>.*?</main>', main, html, count=1, flags=re.I | re.S)
if count != 1:
    raise SystemExit('Could not replace contact main')

# Add final contact-specific class and stylesheet.
body = re.search(r'<body(?:\s+class="([^"]*)")?>', html, re.I)
if body:
    classes = (body.group(1) or '').split()
    if 'ivm-private-desk' not in classes:
        classes.append('ivm-private-desk')
    replacement = '<body class="' + ' '.join(x for x in classes if x) + '">'
    html = html[:body.start()] + replacement + html[body.end():]
if STYLE not in html:
    html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)

page.write_text(html, encoding='utf-8')

# Validation.
final = page.read_text(encoding='utf-8')
assert CSS_DEST.exists() and CSS_DEST.stat().st_size > 3500
assert 'ivm-private-desk' in final
assert STYLE in final
assert final.count('<h1') == 1
assert 'id="conciergeForm"' in final
for field in ('fName','fPhone','fArrival','fDeparture','fService','fGuests','fBrief'):
    assert f'id="{field}"' in final
assert 'WhatsApp 24/7' in final
assert PHONE in final and EMAIL in final
assert '<link rel="canonical"' in final
assert 'application/ld+json' in final
print('PASS: Phase 32 private members desk contact experience')
