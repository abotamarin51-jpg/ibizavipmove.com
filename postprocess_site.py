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
ASSET_VERSION = '7'
BASE = 'https://ibizavipmove.com'

base_tags = '''<link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/brand-mark.svg"><meta name="theme-color" content="#090e13"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:locale" content="en_GB">'''

old_wordmark = '<a class="wordmark" href="/"><span class="mark">IVM</span><span><strong>IBIZA VIP MOVE</strong><small>PRIVATE CONCIERGE · IBIZA</small></span></a>'
new_wordmark = f'<a class="wordmark" href="/" aria-label="Ibiza VIP Move home"><img src="/assets/brand-logo.svg?v={ASSET_VERSION}" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a>'
old_footer_brand = '<div class="footer-brand">IBIZA VIP MOVE</div>'
new_footer_brand = f'<div class="footer-brand"><img src="/assets/brand-logo.svg?v={ASSET_VERSION}" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div>'

def grab(pattern, text, default=''):
    match = re.search(pattern, text, re.I | re.S)
    return match.group(1).strip() if match else default

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

    # Page-specific social metadata for WhatsApp, iMessage and social platforms.
    title = grab(r'<title>(.*?)</title>', text, 'Ibiza VIP Move')
    desc = grab(r'<meta\s+name="description"\s+content="([^"]*)"', text, 'Private concierge and luxury lifestyle management in Ibiza.')
    canonical = grab(r'<link\s+rel="canonical"\s+href="([^"]*)"', text, BASE + '/')
    og_image = grab(r'<meta\s+property="og:image"\s+content="([^"]*)"', text, BASE + '/assets/images/villa.jpg')
    page_name = title.split('|')[0].strip()

    # Give direct WhatsApp CTAs contextual, pre-filled messages while keeping the form custom.
    interest = service_label(canonical, page_name)
    wa_message = f"Hello Ibiza VIP Move, I'm interested in {interest}. Could you please help me with availability and the next steps? Thank you."
    contextual_wa = NEW_WA + '?text=' + quote(wa_message)
    text = re.sub(
        rf'href="{re.escape(NEW_WA)}"',
        f'href="{contextual_wa}"',
        text,
    )

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
    if og_image.startswith('/assets/'):
        social_tags += f'<link rel="preload" as="image" href="{escape(og_image)}">'

    # Extra WebPage/Breadcrumb structured data without inventing address or credentials.
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
    else:
        schemas.append({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Ibiza VIP Move', 'item': BASE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': page_name, 'item': canonical},
            ],
        })
    schema_tags = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)

    if 'property="og:site_name"' not in text:
        text = text.replace('</head>', social_tags + schema_tags + '</head>')
    path.write_text(text, encoding='utf-8')

not_found = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Ibiza VIP Move</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/brand-mark.svg" type="image/svg+xml"><meta name="theme-color" content="#090e13"><link rel="stylesheet" href="/assets/premium.css?v={ASSET_VERSION}"></head><body style="background:#090e13;color:#fff;min-height:100vh;display:grid;place-items:center;margin:0"><main style="text-align:center;padding:32px;max-width:760px"><img src="/assets/brand-logo.svg?v={ASSET_VERSION}" alt="Ibiza VIP Move" style="width:min(420px,80vw);height:auto;margin:0 auto 54px"><div class="kicker light">404 · Ibiza VIP Move</div><h1 style="color:#fff;font-size:clamp(54px,9vw,100px)">This page has moved.</h1><p style="color:rgba(255,255,255,.65);max-width:560px;margin:28px auto">Return to the private side of Ibiza or contact our concierge team directly.</p><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn gold" href="/">Return home</a><a class="btn ghost" href="{NEW_WA}?text={quote('Hello Ibiza VIP Move, I would like private concierge assistance in Ibiza.')}">WhatsApp Concierge</a></div></main></body></html>'''
(ROOT/'404.html').write_text(not_found, encoding='utf-8')
