from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import re

ROOT = Path('_site')

OLD_PHONE_DISPLAY = '+34 613 75 62 11'
OLD_PHONE_TEL = '+34613756211'
OLD_WA = 'https://wa.me/34613756211'
NEW_PHONE_DISPLAY = '+34 600 703 303'
NEW_PHONE_TEL = '+34600703303'
NEW_WA = 'https://wa.me/34600703303'
ASSET_VERSION = '8'
BASE = 'https://ibizavipmove.com'

base_tags = '''<link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/brand-mark.svg"><meta name="theme-color" content="#090e13"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:locale" content="en_GB">'''

old_wordmark = '<a class="wordmark" href="/"><span class="mark">IVM</span><span><strong>IBIZA VIP MOVE</strong><small>PRIVATE CONCIERGE · IBIZA</small></span></a>'
new_wordmark = f'<a class="wordmark" href="/" aria-label="Ibiza VIP Move home"><img src="/assets/brand-logo.svg?v={ASSET_VERSION}" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a>'
old_footer_brand = '<div class="footer-brand">IBIZA VIP MOVE</div>'
new_footer_brand = f'<div class="footer-brand"><img src="/assets/brand-logo.svg?v={ASSET_VERSION}" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div>'

SEO = {
    '': (
        'Luxury Concierge Ibiza | Chauffeur, Villas & Yachts | Ibiza VIP Move',
        'Luxury concierge in Ibiza for private chauffeur, villas, yachts, private aviation, nightlife, security and bespoke lifestyle support.'
    ),
    'services': (
        'Luxury Concierge Services Ibiza | Ibiza VIP Move',
        'Explore luxury concierge services in Ibiza including private chauffeur, villas, yachts, aviation, security, nightlife, staffing and wellness.'
    ),
    'private-concierge-ibiza': (
        'Private Concierge Ibiza | Luxury Lifestyle Management | Ibiza VIP Move',
        'Private concierge in Ibiza for high-touch lifestyle management, transport, reservations, villas, yachts and discreet on-island coordination.'
    ),
    'private-chauffeur-ibiza': (
        'Private Chauffeur Ibiza | Luxury Driver Service | Ibiza VIP Move',
        'Private chauffeur service in Ibiza for airport transfers, hourly drivers, villas, marinas, nightlife and discreet luxury transportation.'
    ),
    'luxury-villas-ibiza': (
        'Luxury Villa Concierge Ibiza | Private Stays | Ibiza VIP Move',
        'Luxury villa concierge in Ibiza with private stay sourcing, pre-arrival preparation, housekeeping coordination and in-villa lifestyle support.'
    ),
    'yacht-charter-ibiza': (
        'Yacht Charter Ibiza & Formentera | Ibiza VIP Move',
        'Luxury yacht charter in Ibiza and Formentera with private coordination, crew and marina support, catering and day-charter planning.'
    ),
    'private-aviation-ibiza': (
        'Private Jet & Aviation Concierge Ibiza | Ibiza VIP Move',
        'Private aviation concierge in Ibiza with jet, FBO, airport handling, luggage and ground transport coordination for smooth arrivals and departures.'
    ),
    'restaurants-nightlife-ibiza': (
        'VIP Restaurants & Nightlife Ibiza | Ibiza VIP Move',
        'VIP restaurant, beach club and nightlife concierge in Ibiza with reservations, tables, daybeds and private transport coordination.'
    ),
    'private-security-ibiza': (
        'Private Security & Close Protection Ibiza | Ibiza VIP Move',
        'Private security and close protection in Ibiza with discreet support for principals, families, nightlife, events and secure transport coordination.'
    ),
    'private-chef-staffing-ibiza': (
        'Private Chef & Villa Staffing Ibiza | Ibiza VIP Move',
        'Private chefs and villa staffing in Ibiza including butlers, waiters, housekeeping and family support coordinated around your private stay.'
    ),
    'luxury-car-rental-ibiza': (
        'Luxury Car Rental Ibiza | Supercar Concierge | Ibiza VIP Move',
        'Luxury and supercar rental in Ibiza with SUVs, executive vehicles, sports cars and discreet delivery to your villa, hotel or marina.'
    ),
    'wellness-ibiza': (
        'Private Wellness & Beauty Ibiza | Ibiza VIP Move',
        'Private wellness and beauty services in Ibiza including massage, trainers, yoga, hair, makeup and recovery sessions at your villa or hotel.'
    ),
    'private-events-ibiza': (
        'Private Events Ibiza | Luxury Event Concierge | Ibiza VIP Move',
        'Private event concierge in Ibiza for villa dinners, celebrations, proposals, entertainment, DJs, production, décor and guest logistics.'
    ),
    'bespoke-concierge-ibiza': (
        'Bespoke Concierge Ibiza | Luxury Lifestyle Support | Ibiza VIP Move',
        'Bespoke concierge in Ibiza for personal shopping, special access, last-minute sourcing, reservations and tailor-made private requests.'
    ),
    'partners': (
        'Ibiza Concierge Partner for Travel Advisors & Family Offices | Ibiza VIP Move',
        'B2B Ibiza concierge support for family offices, personal assistants, luxury travel advisors, hospitality partners and international concierge firms.'
    ),
    'about': (
        'About Ibiza VIP Move | Private Concierge Ibiza',
        'Discover Ibiza VIP Move, a private concierge and lifestyle management service focused on discreet, responsive and precise Ibiza coordination.'
    ),
    'contact': (
        'Request Private Concierge Ibiza | Ibiza VIP Move',
        'Request private concierge support in Ibiza for chauffeur, villas, yachts, aviation, security, nightlife or a complete bespoke itinerary.'
    ),
}

SERVICE_ALIASES = {
    'private-concierge-ibiza': ['Concierge Ibiza', 'Luxury Concierge Ibiza', 'VIP Concierge Ibiza'],
    'private-chauffeur-ibiza': ['Chauffeur Service Ibiza', 'Private Driver Ibiza', 'Luxury Transportation Ibiza'],
    'luxury-villas-ibiza': ['Luxury Villas Ibiza', 'Villa Concierge Ibiza', 'Private Villa Ibiza'],
    'yacht-charter-ibiza': ['Yacht Charter Ibiza', 'Luxury Yacht Ibiza', 'Formentera Yacht Charter'],
    'private-aviation-ibiza': ['Private Jet Ibiza', 'Aviation Concierge Ibiza', 'FBO Ground Coordination Ibiza'],
    'restaurants-nightlife-ibiza': ['Restaurant Reservations Ibiza', 'VIP Tables Ibiza', 'Ibiza Nightlife Concierge'],
    'private-security-ibiza': ['Private Security Ibiza', 'Close Protection Ibiza', 'Bodyguard Ibiza'],
    'private-chef-staffing-ibiza': ['Private Chef Ibiza', 'Villa Staffing Ibiza', 'Butler Service Ibiza'],
    'luxury-car-rental-ibiza': ['Luxury Car Rental Ibiza', 'Supercar Rental Ibiza', 'Executive Car Ibiza'],
    'wellness-ibiza': ['Private Wellness Ibiza', 'Villa Massage Ibiza', 'Beauty Concierge Ibiza'],
    'private-events-ibiza': ['Private Events Ibiza', 'Villa Events Ibiza', 'Luxury Event Concierge Ibiza'],
    'bespoke-concierge-ibiza': ['Bespoke Concierge Ibiza', 'Lifestyle Management Ibiza', 'VIP Services Ibiza'],
}

def grab(pattern, text, default=''):
    match = re.search(pattern, text, re.I | re.S)
    return match.group(1).strip() if match else default

def clean_html(value):
    value = re.sub(r'<[^>]+>', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()

def service_label(canonical, page_name):
    path = canonical.replace(BASE, '').strip('/')
    labels = {
        'private-chauffeur-ibiza': 'private chauffeur and transportation',
        'luxury-villas-ibiza': 'luxury villas and private stays',
        'yacht-charter-ibiza': 'yacht charter',
        'private-aviation-ibiza': 'private aviation support',
        'restaurants-nightlife-ibiza': 'restaurants, beach clubs and nightlife',
        'private-security-ibiza': 'private security and close protection',
        'private-chef-staffing-ibiza': 'private chefs and villa staffing',
        'luxury-car-rental-ibiza': 'luxury and supercar rental',
        'wellness-ibiza': 'wellness and beauty services',
        'private-events-ibiza': 'private events and celebrations',
        'bespoke-concierge-ibiza': 'bespoke concierge support',
        'private-concierge-ibiza': 'private concierge support',
        'partners': 'a B2B partnership',
        'contact': 'private concierge support',
        'services': 'your private services in Ibiza',
        'about': 'your private concierge services in Ibiza',
    }
    return labels.get(path, 'private concierge support in Ibiza')

service_paths = {
    'private-chauffeur-ibiza',
    'luxury-villas-ibiza',
    'yacht-charter-ibiza',
    'private-aviation-ibiza',
    'restaurants-nightlife-ibiza',
    'private-security-ibiza',
    'private-chef-staffing-ibiza',
    'luxury-car-rental-ibiza',
    'wellness-ibiza',
    'private-events-ibiza',
    'bespoke-concierge-ibiza',
    'private-concierge-ibiza',
}

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')

    # Permanent contact details in generated HTML, metadata and structured data.
    text = text.replace(OLD_PHONE_DISPLAY, NEW_PHONE_DISPLAY)
    text = text.replace(OLD_PHONE_TEL, NEW_PHONE_TEL)
    text = text.replace(OLD_WA, NEW_WA)

    # Render the official logo directly in HTML so it never depends on JavaScript.
    text = text.replace(old_wordmark, new_wordmark)
    text = text.replace(old_footer_brand, new_footer_brand)

    # Cache-safe asset references.
    text = re.sub(r'href="/assets/premium\.css\?v=\d+"', f'href="/assets/premium.css?v={ASSET_VERSION}"', text)
    text = re.sub(r'src="/assets/premium\.js\?v=\d+"', f'src="/assets/premium.js?v={ASSET_VERSION}"', text)

    canonical = grab(r'<link\s+rel="canonical"\s+href="([^"]*)"', text, BASE + '/')
    current_slug = canonical.replace(BASE, '').strip('/')

    # One clear high-intent search target per page, without adding visible keyword-heavy copy.
    if current_slug in SEO:
        seo_title, seo_desc = SEO[current_slug]
        text = re.sub(r'<title>.*?</title>', f'<title>{escape(seo_title)}</title>', text, count=1, flags=re.I | re.S)
        text = re.sub(
            r'(<meta\s+name="description"\s+content=")[^"]*(")',
            lambda m: m.group(1) + escape(seo_desc) + m.group(2),
            text,
            count=1,
            flags=re.I,
        )
        text = re.sub(
            r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
            lambda m: m.group(1) + escape(seo_title) + m.group(2),
            text,
            count=1,
            flags=re.I,
        )
        text = re.sub(
            r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
            lambda m: m.group(1) + escape(seo_desc) + m.group(2),
            text,
            count=1,
            flags=re.I,
        )

    title = grab(r'<title>(.*?)</title>', text, 'Ibiza VIP Move')
    desc = grab(r'<meta\s+name="description"\s+content="([^"]*)"', text, 'Private concierge and luxury lifestyle management in Ibiza.')
    og_image = grab(r'<meta\s+property="og:image"\s+content="([^"]*)"', text, BASE + '/assets/images/villa.jpg')
    page_name = title.split('|')[0].strip()

    # Give direct WhatsApp CTAs contextual, pre-filled messages while keeping the form custom.
    interest = service_label(canonical, page_name)
    wa_message = f"Hello Ibiza VIP Move, I'm interested in {interest}. Could you please help me with availability and the next steps? Thank you."
    contextual_wa = NEW_WA + '?text=' + quote(wa_message)
    text = re.sub(rf'href="{re.escape(NEW_WA)}"', f'href="{contextual_wa}"', text)

    # Social crawlers are more reliable with absolute image URLs.
    if og_image.startswith('/'):
        og_image_absolute = BASE + og_image
        text = re.sub(
            r'(<meta\s+property="og:image"\s+content=")[^"]*(")',
            lambda m: m.group(1) + og_image_absolute + m.group(2),
            text,
            count=1,
            flags=re.I,
        )
    else:
        og_image_absolute = og_image

    social_tags = (
        base_tags
        + f'<meta property="og:image:secure_url" content="{escape(og_image_absolute)}">'
        + f'<meta property="og:image:alt" content="{escape(page_name)} · Ibiza VIP Move">'
        + f'<meta name="twitter:title" content="{escape(title)}">'
        + f'<meta name="twitter:description" content="{escape(desc)}">'
        + f'<meta name="twitter:image" content="{escape(og_image_absolute)}">'
    )
    # The homepage receives a responsive hero preload later in the build.
    # Avoid downloading its legacy social image as a second high-priority asset.
    if og_image.startswith('/assets/') and canonical != BASE + '/':
        social_tags += f'<link rel="preload" as="image" href="{escape(og_image)}">'

    # Core WebPage and breadcrumb data.
    webpage_schema = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': page_name,
        'url': canonical,
        'description': desc,
        'isPartOf': {'@type': 'WebSite', 'name': 'Ibiza VIP Move', 'url': BASE + '/'},
        'inLanguage': 'en',
    }
    schemas = [webpage_schema]

    if canonical.rstrip('/') == BASE:
        schemas.append({
            '@context': 'https://schema.org',
            '@type': 'WebSite',
            'name': 'Ibiza VIP Move',
            'url': BASE + '/',
            'inLanguage': 'en',
        })
        schemas.append({
            '@context': 'https://schema.org',
            '@type': 'ProfessionalService',
            'name': 'Ibiza VIP Move',
            'url': BASE + '/',
            'telephone': NEW_PHONE_DISPLAY,
            'email': 'partnership@ibizavipmove.com',
            'areaServed': {'@type': 'Place', 'name': 'Ibiza, Spain'},
            'description': desc,
            'hasOfferCatalog': {
                '@type': 'OfferCatalog',
                'name': 'Luxury Concierge Services in Ibiza',
                'itemListElement': [
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Private Chauffeur Ibiza'}},
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Luxury Villas Ibiza'}},
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Yacht Charter Ibiza'}},
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Private Aviation Ibiza'}},
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Private Security Ibiza'}},
                    {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Private Events Ibiza'}},
                ],
            },
        })
    else:
        schemas.append({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Ibiza VIP Move', 'item': BASE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': page_name, 'item': canonical},
            ],
        })

    # Service schema for commercial service pages.
    if current_slug in service_paths:
        schemas.append({
            '@context': 'https://schema.org',
            '@type': 'Service',
            'name': page_name,
            'serviceType': service_label(canonical, page_name),
            'alternateName': SERVICE_ALIASES.get(current_slug, []),
            'description': desc,
            'url': canonical,
            'areaServed': {'@type': 'Place', 'name': 'Ibiza, Spain'},
            'provider': {
                '@type': 'ProfessionalService',
                'name': 'Ibiza VIP Move',
                'url': BASE,
                'telephone': NEW_PHONE_DISPLAY,
                'email': 'partnership@ibizavipmove.com',
            },
        })

    # FAQ schema mirrors only questions and answers already visible on the page.
    faq_items = []
    for match in re.finditer(r'<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>', text, re.I | re.S):
        question = clean_html(match.group(1))
        answer = clean_html(match.group(2))
        if question and answer:
            faq_items.append({
                '@type': 'Question',
                'name': question,
                'acceptedAnswer': {'@type': 'Answer', 'text': answer},
            })
    if faq_items:
        schemas.append({
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': faq_items,
        })

    schema_tags = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)

    if 'property="og:site_name"' not in text:
        text = text.replace('</head>', social_tags + schema_tags + '</head>')
    path.write_text(text, encoding='utf-8')

not_found = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Ibiza VIP Move</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><meta name="theme-color" content="#090e13"><link rel="stylesheet" href="/assets/premium.css?v={ASSET_VERSION}"></head><body style="background:#090e13;color:#fff;min-height:100vh;display:grid;place-items:center;margin:0"><main style="text-align:center;padding:32px;max-width:760px"><img src="/assets/brand-logo.svg?v={ASSET_VERSION}" alt="Ibiza VIP Move" style="width:min(420px,80vw);height:auto;margin:0 auto 54px"><div class="kicker light">404 · Ibiza VIP Move</div><h1 style="color:#fff;font-size:clamp(54px,9vw,100px)">This page has moved.</h1><p style="color:rgba(255,255,255,.65);max-width:560px;margin:28px auto">Return to the private side of Ibiza or contact our concierge team directly.</p><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn gold" href="/">Return home</a><a class="btn ghost" href="{NEW_WA}?text={quote('Hello Ibiza VIP Move, I would like private concierge assistance in Ibiza.')}">WhatsApp Concierge</a></div></main></body></html>'''
(ROOT/'404.html').write_text(not_found, encoding='utf-8')

# Run the full SEO/integrity audit as part of every build.
import validate_site
