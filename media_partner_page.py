from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
TEL = '+34600703303'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'
LOGO = '/assets/brand-logo.svg?v=8'

services = [
    ('Private Concierge Ibiza', '/private-concierge-ibiza/'),
    ('Private Chauffeur Ibiza', '/private-chauffeur-ibiza/'),
    ('Luxury Villas Ibiza', '/luxury-villas-ibiza/'),
    ('Yacht Charter Ibiza & Formentera', '/yacht-charter-ibiza/'),
    ('Private Aviation Ibiza', '/private-aviation-ibiza/'),
    ('Restaurants, Beach Clubs & Nightlife', '/restaurants-nightlife-ibiza/'),
    ('Private Security Ibiza', '/private-security-ibiza/'),
    ('Private Chef & Villa Staffing', '/private-chef-staffing-ibiza/'),
]

schema = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    'name': 'Media & Partner Information | Ibiza VIP Move',
    'url': BASE + '/media-partners/',
    'description': 'Official Ibiza VIP Move information for travel partners, concierge companies, media, private aviation, villa and yacht partners.',
    'about': {'@id': BASE + '/#organization'},
    'isPartOf': {'@id': BASE + '/#website'},
    'inLanguage': 'en',
}

service_links = ''.join(f'<a href="{url}">{name}</a>' for name, url in services)

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Media & Partner Information | Ibiza VIP Move</title><meta name="description" content="Official Ibiza VIP Move information for travel partners, concierge companies, media, private aviation, villa and yacht partners."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}/media-partners/"><meta property="og:type" content="website"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:title" content="Media & Partner Information | Ibiza VIP Move"><meta property="og:description" content="Official brand, service and contact information for Ibiza VIP Move partners and media."><meta property="og:url" content="{BASE}/media-partners/"><meta property="og:image" content="{BASE}/assets/images/aviation.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/premium.css?v=8"><link rel="stylesheet" href="/assets/ui-fixes.css?v=1"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body><header class="site-header"><a class="wordmark" href="/" aria-label="Ibiza VIP Move home"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a><nav><a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Partners</a><a href="/about/">About</a><a href="/contact/">Contact</a><a class="nav-cta" href="{WA}">Request Concierge</a></nav><button class="menu-btn" aria-label="Open menu" aria-controls="mobileMenu">Menu</button></header><div class="mobile-menu" id="mobileMenu"><a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Partners</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="{WA}">WhatsApp Concierge</a></div><main><section class="page-hero" style="--hero:url('/assets/images/aviation.jpg')"><div><div class="kicker light">Official brand resource</div><h1>Media & Partner<br><em>Information.</em></h1><p>Verified information for travel advisors, concierge companies, private aviation partners, villa agencies, yacht brokers and media referencing Ibiza VIP Move.</p></div></section><section class="editorial"><div><div class="kicker dark">Official identity</div><h2>One clear source of truth.</h2></div><div><p class="large"><strong>Ibiza VIP Move</strong> is a private concierge, chauffeur and luxury lifestyle management service in Ibiza, Spain.</p><p>We coordinate private chauffeur transportation, villas, yacht charters, private aviation support, dining and nightlife, security, staffing, wellness, events and bespoke requests through one point of contact.</p><ul class="premium-list"><li><strong>Official name:</strong> Ibiza VIP Move</li><li><strong>Official website:</strong> ibizavipmove.com</li><li><strong>Service area:</strong> Ibiza, Spain</li><li><strong>Phone / WhatsApp:</strong> {PHONE}</li><li><strong>Partnership email:</strong> {EMAIL}</li></ul></div></section><section class="dark-panel"><div class="kicker light">Partner-ready information</div><h2>Easy to reference.<br>Easy to verify.</h2><div class="trust-grid"><div><b>Suggested attribution</b><p>Ibiza VIP Move — Private Concierge & Luxury Lifestyle Management in Ibiza.</p></div><div><b>Official logo</b><p><a href="/assets/brand-logo.svg" style="color:inherit;text-decoration:underline">View the official Ibiza VIP Move logo</a>.</p></div><div><b>International coordination</b><p>For PAs, family offices, luxury travel advisors, concierge companies and international client teams.</p></div><div><b>Editorial enquiries</b><p>For factual brand information, service references or collaboration requests, contact our partnerships team.</p></div></div></section><section class="service-showcase compact"><div class="section-head"><div class="kicker light">Primary service pages</div><h2>Link directly to the relevant service.</h2><p>Partners and media can reference the most relevant official page rather than a generic landing page.</p></div><div class="footer-grid" style="padding:0;border:0">{service_links}</div></section><section class="partners-strip"><div><div class="kicker dark">International partners</div><h2>Coordinating Ibiza from abroad?</h2><p>Our international client and partner page explains how briefs are handled for teams arranging Ibiza from overseas.</p></div><a class="btn dark" href="/international-clients/">International clients</a></section><section class="closing-simple"><h2>Partnership or media enquiry?</h2><p>Send the brief, proposed collaboration or editorial request directly to our partnerships team.</p><div class="hero-actions" style="justify-content:center"><a class="btn dark" href="mailto:{EMAIL}">Email Partnerships</a><a class="btn dark" href="{WA}">WhatsApp</a></div></section></main><footer><div class="footer-grid"><div><div class="footer-brand"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div><p>Private concierge, chauffeur and lifestyle management in Ibiza. One trusted point of contact for an effortless stay.</p></div><div><h4>Contact</h4><a href="tel:{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}">WhatsApp Concierge</a></div><div><h4>Explore</h4><a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Travel Partners</a><a href="/media-partners/">Media & Partner Info</a><a href="/about/">About</a><a href="/contact/">Request Concierge</a></div></div><div class="footer-bottom"><span>© 2026 Ibiza VIP Move</span><span><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/cookies/">Cookies</a></span></div></footer><div class="mobile-bar"><a href="tel:{TEL}">Call</a><a href="{WA}">WhatsApp</a></div><script src="/assets/premium.js?v=8"></script></body></html>'''

out = ROOT / 'media-partners'
out.mkdir(parents=True, exist_ok=True)
(out / 'index.html').write_text(html, encoding='utf-8')

# Make the page discoverable from every existing premium footer without changing layout.
for path in ROOT.rglob('*.html'):
    if path == out / 'index.html':
        continue
    text = path.read_text(encoding='utf-8')
    if '/media-partners/' not in text and '<a href="/partners/">Travel Partners</a>' in text:
        text = text.replace('<a href="/partners/">Travel Partners</a>', '<a href="/partners/">Travel Partners</a><a href="/media-partners/">Media & Partner Info</a>')
    path.write_text(text, encoding='utf-8')

sitemap = ROOT / 'sitemap.xml'
if sitemap.exists():
    text = sitemap.read_text(encoding='utf-8')
    url = BASE + '/media-partners/'
    if url not in text:
        entry = f'<url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>'
        text = text.replace('</urlset>', entry + '</urlset>')
        sitemap.write_text(text, encoding='utf-8')

llms = ROOT / 'llms.txt'
if llms.exists():
    text = llms.read_text(encoding='utf-8')
    line = '- [Media & Partner Information](https://ibizavipmove.com/media-partners/)\n'
    if line not in text:
        marker = '## Services\n'
        text = text.replace(marker, line + '\n' + marker)
        llms.write_text(text, encoding='utf-8')

print('PASS: media and partner authority page created and linked')
