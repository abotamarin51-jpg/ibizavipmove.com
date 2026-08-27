from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
EMAIL = 'partnership@ibizavipmove.com'
UPDATED = '27 August 2026'

home = (ROOT / 'index.html').read_text(encoding='utf-8')
header_match = re.search(r'(<header class="site-header">.*?</header><div class="mobile-menu">.*?</div>)', home, re.I | re.S)
footer_match = re.search(r'(<footer>.*?</footer><div class="mobile-bar">.*?</div><script src="/assets/premium\.js\?v=\d+"></script>)', home, re.I | re.S)
css_match = re.search(r'href="(/assets/premium\.css\?v=\d+)"', home, re.I)

if not header_match or not footer_match or not css_match:
    raise SystemExit('Could not safely extract the current site shell for legal pages')

HEADER = header_match.group(1)
FOOTER = footer_match.group(1)
CSS = css_match.group(1)

LEGAL_LINKS = '<a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/cookies/">Cookies</a>'

def add_legal_links(text):
    if '/privacy/' in text and '/terms/' in text and '/cookies/' in text:
        return text
    needle = '<a href="/contact/">Request Concierge</a>'
    return text.replace(needle, needle + LEGAL_LINKS)

HEADER = add_legal_links(HEADER)
FOOTER = add_legal_links(FOOTER)

legal_css = '''
.legal-page{width:min(900px,92vw);margin:0 auto;padding:160px 0 110px;display:block}
.legal-page .kicker{margin-bottom:14px}
.legal-page h1{font-size:clamp(52px,7vw,86px);max-width:850px;margin-bottom:18px}
.legal-page .updated{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#9a7854;margin-bottom:48px}
.legal-page h2{font-size:34px;line-height:1.05;letter-spacing:-.02em;margin:46px 0 15px}
.legal-page p,.legal-page li{color:var(--muted);font-size:14px;line-height:1.8}
.legal-page ul{padding-left:20px}
.legal-page a{text-decoration:underline;text-underline-offset:3px}
.legal-note{margin-top:48px;padding-top:24px;border-top:1px solid var(--line)}
@media(max-width:600px){.legal-page{width:calc(100% - 36px);padding:125px 0 80px}.legal-page h1{font-size:50px}.legal-page h2{font-size:30px}}
'''.strip() + '\n'
(ROOT / 'assets' / 'legal.css').write_text(legal_css, encoding='utf-8')

PAGES = {
    'privacy': {
        'title': 'Privacy Policy | Ibiza VIP Move',
        'desc': 'Privacy information for Ibiza VIP Move website visitors and clients contacting us about private concierge services in Ibiza.',
        'heading': 'Privacy Policy',
        'body': f'''
<p>This Privacy Policy explains how Ibiza VIP Move handles personal information when you visit this website or contact us about concierge, chauffeur or related private services.</p>
<h2>Information we may receive</h2>
<p>When you contact us by WhatsApp, email, telephone or the website enquiry form, you may provide information such as your name, telephone number, email address, travel dates, guest numbers, preferences, itinerary details and the services you request.</p>
<h2>How we use information</h2>
<p>We use personal information to respond to enquiries, prepare and coordinate requested services, communicate about bookings, manage operational requirements and maintain appropriate business records. We may also use limited information where necessary to protect our legitimate business interests, prevent misuse or comply with legal obligations.</p>
<h2>Service providers and suppliers</h2>
<p>Where necessary to fulfil a request, relevant details may be shared with selected service providers involved in the requested service, such as transport operators, accommodation providers, yacht or aviation partners, hospitality venues, security providers or other suppliers. We aim to share only information reasonably required for the service.</p>
<h2>WhatsApp, email and third-party platforms</h2>
<p>If you choose to communicate through WhatsApp, email or another third-party platform, that provider processes information under its own privacy terms. Some providers may process data outside the European Economic Area using their own lawful transfer mechanisms.</p>
<h2>Retention</h2>
<p>Information is retained only for as long as reasonably necessary for enquiries, service delivery, record keeping, dispute management and applicable legal or accounting requirements. Retention periods may vary depending on the nature of the interaction.</p>
<h2>Your rights</h2>
<p>Where the GDPR or other applicable privacy law applies, you may have rights to request access, correction, deletion, restriction, portability or objection to certain processing. You may also have the right to lodge a complaint with the competent data protection authority.</p>
<h2>Contact</h2>
<p>For privacy questions or requests, contact <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:+34600703303">{PHONE}</a>.</p>
<div class="legal-note"><p>This policy may be updated when our website, services or legal requirements change.</p></div>''',
    },
    'terms': {
        'title': 'Terms & Conditions | Ibiza VIP Move',
        'desc': 'General website and service terms for enquiries and private concierge services coordinated by Ibiza VIP Move in Ibiza.',
        'heading': 'Terms & Conditions',
        'body': f'''
<p>These Terms & Conditions apply to the use of this website and provide general conditions for enquiries made to Ibiza VIP Move. Specific bookings may be subject to additional written terms, quotations, supplier conditions or cancellation rules provided before confirmation.</p>
<h2>Website information</h2>
<p>The website describes the types of private concierge and lifestyle services that may be coordinated. Content is provided for general information and does not constitute a guaranteed offer of availability, price or access.</p>
<h2>Requests and confirmations</h2>
<p>An enquiry does not create a confirmed booking. A service is confirmed only after the relevant details, availability, price and any required payment or acceptance conditions have been agreed. Availability can change until confirmation is completed.</p>
<h2>Third-party services</h2>
<p>Many concierge requests involve independent third-party providers. Their own operating rules, availability, safety requirements, admission policies, cancellation conditions and contractual terms may apply. Ibiza VIP Move coordinates services but cannot guarantee matters that remain under the control of an independent provider.</p>
<h2>Prices and payments</h2>
<p>Prices, taxes, deposits, payment schedules and cancellation conditions are communicated as part of the relevant quotation or booking. Extra waiting time, itinerary changes, additional hours, guest changes or services requested after confirmation may result in additional charges where communicated or reasonably applicable.</p>
<h2>Client responsibilities</h2>
<p>Clients are responsible for providing accurate contact, passenger, itinerary and timing information and for complying with lawful instructions, venue policies and supplier requirements. Material changes should be communicated as early as possible.</p>
<h2>Cancellations and changes</h2>
<p>Cancellation and amendment conditions depend on the service and supplier involved and will be communicated where relevant. Non-refundable supplier costs already incurred may remain payable.</p>
<h2>Liability</h2>
<p>Nothing in these terms excludes liability that cannot lawfully be excluded. To the extent permitted by applicable law, Ibiza VIP Move is not responsible for losses caused solely by events outside reasonable control or by the acts or omissions of independent third-party providers.</p>
<h2>Intellectual property</h2>
<p>The Ibiza VIP Move name, branding, website design, text and original materials may not be copied or commercially reused without permission, except where applicable law permits.</p>
<h2>Applicable rights</h2>
<p>These general terms are subject to applicable law. Any mandatory consumer protections or other rights that cannot legally be limited remain unaffected.</p>
<h2>Contact</h2>
<p>Questions about these terms can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''',
    },
    'cookies': {
        'title': 'Cookie Policy | Ibiza VIP Move',
        'desc': 'Cookie and website technology information for visitors to Ibiza VIP Move.',
        'heading': 'Cookie Policy',
        'body': '''
<p>This page explains how cookies and similar website technologies are currently used on Ibiza VIP Move.</p>
<h2>Current use of cookies</h2>
<p>The website does not currently use advertising cookies or an analytics platform that intentionally places non-essential tracking cookies for visitor profiling. Essential browser or hosting functions may still use technical mechanisms required to deliver pages securely and reliably.</p>
<h2>Third-party services</h2>
<p>The website may connect to third-party services needed for functionality or presentation, including externally hosted web fonts. If you choose a WhatsApp, email or telephone contact link, your browser or device then interacts with that external provider under its own terms and privacy practices.</p>
<h2>Future changes</h2>
<p>If non-essential analytics, advertising or other consent-based cookies are introduced in the future, this policy will be updated and an appropriate consent mechanism will be provided where required by applicable law.</p>
<h2>Browser controls</h2>
<p>You can use your browser settings to view, restrict or delete cookies and site data. Blocking essential technical storage may affect how some websites function.</p>
<h2>Contact</h2>
<p>Questions about website privacy or cookie use can be sent to <a href="mailto:partnership@ibizavipmove.com">partnership@ibizavipmove.com</a>.</p>''',
    },
}

def page_html(slug, info):
    canonical = f'{BASE}/{slug}/'
    schema = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': info['heading'],
        'url': canonical,
        'description': info['desc'],
        'isPartOf': {'@type': 'WebSite', 'name': 'Ibiza VIP Move', 'url': BASE + '/'},
        'inLanguage': 'en',
    }
    head = f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(info['title'])}</title><meta name="description" content="{escape(info['desc'])}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(info['title'])}"><meta property="og:description" content="{escape(info['desc'])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/images/villa.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><meta name="theme-color" content="#090e13"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="{CSS}"><link rel="stylesheet" href="/assets/legal.css?v=1"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>'''
    body = f'''<section class="legal-page"><div class="kicker dark">Ibiza VIP Move</div><h1>{escape(info['heading'])}</h1><div class="updated">Last updated · {UPDATED}</div>{info['body']}</section>'''
    return '<!doctype html><html lang="en">' + head + '<body>' + HEADER + '<main>' + body + '</main>' + FOOTER + '</body></html>'

for slug, info in PAGES.items():
    directory = ROOT / slug
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'index.html').write_text(page_html(slug, info), encoding='utf-8')

# Add legal navigation to all existing pages without changing the footer structure.
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    text = add_legal_links(text)
    path.write_text(text, encoding='utf-8')

# Include the pages in the sitemap.
sitemap_path = ROOT / 'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
for slug in PAGES:
    url = f'{BASE}/{slug}/'
    if f'<loc>{url}</loc>' not in sitemap:
        entry = f'<url><loc>{url}</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>'
        sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
sitemap_path.write_text(sitemap, encoding='utf-8')

print('Legal pages generated: privacy, terms, cookies')
