from pathlib import Path

ROOT = Path('_site')
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'


def replace_once(path, old, new):
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'Marker not found in {path}: {old[:90]}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


# HOME: strengthen the existing partner message without introducing new claims.
home = ROOT / 'index.html'
old_home = '<p>We support personal assistants, family offices, luxury travel advisors, concierge companies and hospitality partners requiring a reliable Ibiza operator.</p>'
new_home = '<p>We support personal assistants, family offices, luxury travel advisors, concierge companies and hospitality partners requiring a reliable Ibiza operator. Client-facing or discreet behind-the-scenes coordination can be aligned to the brief.</p>'
replace_once(home, old_home, new_home)


# PARTNERS: explain who the service is for and how the handover works.
partners = ROOT / 'partners' / 'index.html'
old_partner_close = f'''<section class="closing-simple"><h2>Need a reliable Ibiza partner?</h2><p>Send your client brief or introduce your team.</p><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a></section>'''
new_partner_close = f'''<section class="process"><div class="section-head"><div class="kicker dark">Built for professional partners</div><h2>A clear handover. One dedicated local contact.</h2><p>Designed for teams that need Ibiza execution without adding unnecessary layers of communication.</p></div><div class="process-grid"><article><span>01</span><h3>Personal Assistants</h3><p>Direct coordination around the principal, guests, timings and changing priorities.</p></article><article><span>02</span><h3>Family Offices</h3><p>Discreet local support across multiple services through one point of contact.</p></article><article><span>03</span><h3>Travel & Concierge</h3><p>Local execution for luxury travel advisors, concierge firms and hospitality partners.</p></article><article><span>04</span><h3>Multi-service Briefs</h3><p>Transport, villas, yachts, aviation, dining and lifestyle requests aligned around one itinerary.</p></article></div></section><section class="dark-panel"><div class="kicker light">Partner workflow</div><h2>Simple communication.<br>Detailed execution.</h2><div class="trust-grid"><div><b>Share the brief</b><p>Dates, guest profile, priorities, service requirements and any important preferences.</p></div><div><b>Align the details</b><p>We clarify the operational points needed before options or coordination begin.</p></div><div><b>Coordinate locally</b><p>Relevant services are managed around the confirmed itinerary and partner instructions.</p></div><div><b>Stay connected</b><p>Communication remains available as timings, guest needs or plans evolve.</p></div></div></section><section class="closing-simple"><h2>Need a reliable Ibiza partner?</h2><p>Send your client brief or introduce your team. For time-sensitive requests, WhatsApp is usually the fastest route.</p><div class="hero-actions" style="justify-content:center"><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a><a class="btn dark" href="{WA}">WhatsApp</a></div></section>'''
replace_once(partners, old_partner_close, new_partner_close)


# CONTACT: remove uncertainty after form submission and reinforce direct contact options.
contact = ROOT / 'contact' / 'index.html'
old_contact_end = '''</section><section class="contact-direct"><div><span>WhatsApp</span>'''
# Keep existing contact-direct markup intact; insert the trust/process section after it using its known closing marker.
text = contact.read_text(encoding='utf-8')
marker = '</section></main>'
if marker not in text:
    raise SystemExit('Contact closing marker not found')
contact_extra = f'''<section class="process"><div class="section-head"><div class="kicker dark">What happens next</div><h2>From first message to coordinated stay.</h2><p>You do not need to have every detail finalised before contacting us.</p></div><div class="process-grid"><article><span>01</span><h3>Send the essentials</h3><p>Dates, guests, primary service and any priorities you already know.</p></article><article><span>02</span><h3>Clarify the brief</h3><p>We identify the details needed to understand the request properly.</p></article><article><span>03</span><h3>Coordinate</h3><p>Once the direction is confirmed, the relevant Ibiza services and logistics are aligned.</p></article><article><span>04</span><h3>Stay supported</h3><p>We remain available as the itinerary develops or plans change during the stay.</p></article></div></section><section class="closing-simple"><h2>Need to speak directly?</h2><p>For urgent or same-day requests, WhatsApp is usually the quickest way to reach the concierge team.</p><a class="btn dark" href="{WA}">WhatsApp Concierge</a></section>'''
text = text.replace(marker, contact_extra + marker, 1)
contact.write_text(text, encoding='utf-8')

print('PASS: trust and conversion enhancements applied to Home, Partners and Contact')
