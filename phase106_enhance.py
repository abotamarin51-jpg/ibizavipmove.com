from pathlib import Path
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
MEDIA = ROOT / 'media-partners' / 'index.html'
FOUNDER = ROOT / 'founder' / 'index.html'
REPORT = ROOT / 'ibiza-luxury-operations-report-2026' / 'index.html'
PRESS = ROOT / 'press-kit.txt'

PRESS_TEXT = '''Ibiza VIP Move — Official Press & Citation Kit

Official website: https://ibizavipmove.com/
Official brand name: Ibiza VIP Move
Founder: Juan Cruz
Founder profile: https://ibizavipmove.com/founder/
Brand structure: founder-led private concierge and luxury lifestyle coordination brand
Primary service area: Ibiza, Balearic Islands, Spain
Official phone / WhatsApp: +34 600 703 303
Partnerships and media email: partnership@ibizavipmove.com
Official Instagram: https://www.instagram.com/ibizavipmove/
Website languages published: English, Spanish, French, German and Arabic

Approved short description
Ibiza VIP Move is a founder-led private concierge and luxury lifestyle coordination brand serving Ibiza. It coordinates chauffeur and ground transport, villas, yachts, private aviation ground support, dining and nightlife, security, villa staffing, wellness, private events and bespoke requests through one Ibiza-based point of contact.

What Ibiza VIP Move does
- Private concierge and full-stay lifestyle coordination
- Private chauffeur and airport / private aviation ground transport coordination
- Luxury villa and private-stay support
- Yacht and marina movement coordination
- Restaurant, beach club and nightlife planning
- Private security and licensed close-protection coordination when requested
- Private chefs, villa staffing, wellness and private events
- Support for principals, personal assistants, family offices, travel advisors and professional partners

Operational evidence published by Ibiza VIP Move
Founder profile: https://ibizavipmove.com/founder/
Operational case studies: https://ibizavipmove.com/case-studies/
Ibiza Luxury Operations Report 2026: https://ibizavipmove.com/ibiza-luxury-operations-report-2026/
Private concierge overview: https://ibizavipmove.com/private-concierge-ibiza/
Private client services: https://ibizavipmove.com/private-client-services-ibiza/
Destination management: https://ibizavipmove.com/destination-management-ibiza/
Media & partners source page: https://ibizavipmove.com/media-partners/

Editorial and citation guidance
Use “Ibiza VIP Move” as the brand name and “Juan Cruz” as Founder. For a general brand citation, link to the official homepage. For a service-specific reference, link to the relevant canonical service page. Client identities, exact private itineraries and commercial terms are not published through the operating case studies. Do not imply endorsements, partnerships, memberships, venue access, availability or client relationships unless Ibiza VIP Move has explicitly confirmed them for publication.

Verification notes
Reservations, supplier availability, access and inventory are subject to confirmation. The Ibiza Luxury Operations Report 2026 is a set of field observations based on Ibiza VIP Move operating experience; it is not presented as market-wide statistical research. Published operating cases are anonymized and omit client names, exact dates, properties, venues and commercial terms.

Brand assets
Official logo (SVG): https://ibizavipmove.com/assets/brand-logo.svg
Official logo (JPG): https://ibizavipmove.com/assets/brand-logo.jpg

Media / partnership enquiries
partnership@ibizavipmove.com
+34 600 703 303
https://ibizavipmove.com/contact/
'''


def insert_before_closing(html, section):
    closings = list(re.finditer(r'<section\b[^>]*class="[^"]*closing[^\"]*"', html, re.I))
    if closings:
        pos = closings[-1].start()
        return html[:pos] + section + html[pos:]
    if '</main>' in html:
        return html.replace('</main>', section + '</main>', 1)
    raise SystemExit('Phase 106 no insertion point')


for target in (MEDIA, FOUNDER, REPORT):
    if not target.exists():
        raise SystemExit(f'Phase 106 required page missing: {target}')

PRESS.write_text(PRESS_TEXT, encoding='utf-8')

media_html = MEDIA.read_text(encoding='utf-8')
if 'ivm-phase106-presskit' in media_html:
    raise SystemExit('Phase 106 duplicate media press kit')
press_section = '''<section class="editorial ivm-phase106-presskit"><div><div class="kicker dark">Press & citation kit</div><h2>Official facts, ready to cite.</h2></div><div><p class="large">For journalists, luxury travel media, directories and professional partners, this is the shortest route to verified Ibiza VIP Move brand facts and operating evidence.</p><ul class="premium-list"><li><strong>Brand:</strong> Ibiza VIP Move</li><li><strong>Founder:</strong> Juan Cruz</li><li><strong>Structure:</strong> Founder-led private concierge and luxury lifestyle coordination brand</li><li><strong>Primary service area:</strong> Ibiza, Balearic Islands, Spain</li><li><strong>Media & partnerships:</strong> partnership@ibizavipmove.com · +34 600 703 303</li></ul><p><a class="text-link" href="/press-kit.txt">Plain-text press kit</a> · <a class="text-link" rel="author" href="/founder/">Founder profile</a> · <a class="text-link" href="/case-studies/">Operating case studies</a> · <a class="text-link" href="/ibiza-luxury-operations-report-2026/">2026 operations report</a> · <a class="text-link" href="/assets/brand-logo.svg">Official logo</a></p><p>Editorial references should use the canonical Ibiza VIP Move pages and should not imply client relationships, memberships, endorsements, venue access or availability unless explicitly confirmed for publication.</p></div></section>'''
media_html = insert_before_closing(media_html, press_section)
if 'rel="alternate" type="text/plain" href="/press-kit.txt"' not in media_html:
    if '</head>' not in media_html:
        raise SystemExit('Phase 106 media </head> missing')
    media_html = media_html.replace('</head>', '<link rel="alternate" type="text/plain" href="/press-kit.txt" title="Ibiza VIP Move Press Kit"></head>', 1)
MEDIA.write_text(media_html, encoding='utf-8')

founder_html = FOUNDER.read_text(encoding='utf-8')
if 'ivm-phase106-media-link' in founder_html:
    raise SystemExit('Phase 106 duplicate founder media link')
founder_section = '''<section class="partners-strip ivm-phase106-media-link"><div><div class="kicker dark">Media & verification</div><h2>Need the official source?</h2><p>Journalists, directories and professional partners can use the Media & Partners page and plain-text press kit for verified brand facts, citation guidance and operating evidence.</p></div><a class="btn dark" href="/media-partners/">Media & Partners</a></section>'''
FOUNDER.write_text(insert_before_closing(founder_html, founder_section), encoding='utf-8')

report_html = REPORT.read_text(encoding='utf-8')
if 'ivm-phase106-media-link' in report_html:
    raise SystemExit('Phase 106 duplicate report media link')
report_section = '''<section class="partners-strip ivm-phase106-media-link"><div><div class="kicker dark">Press & data enquiries</div><h2>Cite the methodology, not a market claim.</h2><p>The 2026 report contains field observations from Ibiza VIP Move operating experience. Media and professional users can verify the methodology and official brand facts through the press kit.</p></div><a class="btn dark" href="/media-partners/">Open press kit</a></section>'''
REPORT.write_text(insert_before_closing(report_html, report_section), encoding='utf-8')

print('PASS: Phase 106 press & citation readiness — media source page strengthened, founder/report routed to verified media facts and plain-text press kit published')
