from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ENTITY_ID = BASE + '/#organization'
WEBSITE_ID = BASE + '/#website'
PHONE = '+34 600 703 303'
EMAIL = 'partnership@ibizavipmove.com'
LOGO = BASE + '/assets/brand-logo.svg'

SERVICES = [
    ('Private Concierge Ibiza', '/private-concierge-ibiza/'),
    ('Private Chauffeur Ibiza', '/private-chauffeur-ibiza/'),
    ('Luxury Villa Concierge Ibiza', '/luxury-villas-ibiza/'),
    ('Yacht Charter Ibiza & Formentera', '/yacht-charter-ibiza/'),
    ('Private Aviation Concierge Ibiza', '/private-aviation-ibiza/'),
    ('VIP Restaurants & Nightlife Ibiza', '/restaurants-nightlife-ibiza/'),
    ('Private Security & Close Protection Ibiza', '/private-security-ibiza/'),
    ('Private Chef & Villa Staffing Ibiza', '/private-chef-staffing-ibiza/'),
    ('Luxury Car Rental Ibiza', '/luxury-car-rental-ibiza/'),
    ('Private Wellness & Beauty Ibiza', '/wellness-ibiza/'),
    ('Private Events Ibiza', '/private-events-ibiza/'),
    ('Bespoke Concierge Ibiza', '/bespoke-concierge-ibiza/'),
]

ENTITY_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'ProfessionalService',
    '@id': ENTITY_ID,
    'name': 'Ibiza VIP Move',
    'url': BASE + '/',
    'logo': {'@type': 'ImageObject', 'url': LOGO},
    'image': LOGO,
    'telephone': PHONE,
    'email': EMAIL,
    'areaServed': {'@type': 'Place', 'name': 'Ibiza, Spain'},
    'contactPoint': {
        '@type': 'ContactPoint',
        'telephone': PHONE,
        'contactType': 'customer service',
        'url': BASE + '/contact/',
    },
    'knowsAbout': [name for name, _ in SERVICES],
}


def enhance_schema(data):
    if not isinstance(data, dict):
        return data
    schema_type = data.get('@type')
    if schema_type == 'ProfessionalService' and data.get('name') == 'Ibiza VIP Move':
        enriched = dict(ENTITY_SCHEMA)
        enriched.update(data)
        enriched['@id'] = ENTITY_ID
        enriched['logo'] = ENTITY_SCHEMA['logo']
        enriched['image'] = LOGO
        enriched['telephone'] = PHONE
        enriched['email'] = EMAIL
        enriched['areaServed'] = ENTITY_SCHEMA['areaServed']
        enriched['contactPoint'] = ENTITY_SCHEMA['contactPoint']
        enriched['knowsAbout'] = ENTITY_SCHEMA['knowsAbout']
        return enriched
    if schema_type == 'WebSite':
        data['@id'] = WEBSITE_ID
        data['publisher'] = {'@id': ENTITY_ID}
        return data
    if schema_type == 'WebPage':
        url = data.get('url', BASE + '/')
        data['@id'] = url.rstrip('/') + '/#webpage' if url != BASE + '/' else BASE + '/#webpage'
        data['isPartOf'] = {'@id': WEBSITE_ID}
        data['about'] = {'@id': ENTITY_ID}
        data['publisher'] = {'@id': ENTITY_ID}
        return data
    if schema_type == 'Service':
        url = data.get('url', BASE + '/')
        data['@id'] = url.rstrip('/') + '/#service'
        data['provider'] = {'@id': ENTITY_ID}
        return data
    return data


for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', text, re.I)
    canonical = canonical_match.group(1) if canonical_match else BASE + '/'

    def rewrite_jsonld(match):
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)
        data = enhance_schema(data)
        if isinstance(data, dict) and data.get('@type') == 'FAQPage':
            data['@id'] = canonical.rstrip('/') + '/#faq'
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

    text = re.sub(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        rewrite_jsonld,
        text,
        flags=re.I | re.S,
    )

    if ENTITY_ID not in text:
        entity_tag = '<script type="application/ld+json">' + json.dumps(ENTITY_SCHEMA, ensure_ascii=False) + '</script>'
        text = text.replace('</head>', entity_tag + '</head>')

    # Strengthen internal navigation using only existing footer markup.
    footer_old = '<a href="/services/">Services</a><a href="/partners/">Travel Partners</a><a href="/about/">About</a><a href="/contact/">Request Concierge</a>'
    footer_new = '<a href="/services/">Services</a><a href="/private-concierge-ibiza/">Concierge</a><a href="/partners/">Travel Partners</a><a href="/about/">About</a><a href="/contact/">Request Concierge</a>'
    text = text.replace(footer_old, footer_new)

    path.write_text(text, encoding='utf-8')


llms = [
    '# Ibiza VIP Move',
    '',
    '> Ibiza VIP Move is a private concierge, chauffeur and luxury lifestyle management service in Ibiza, Spain.',
    '',
    'Official website: https://ibizavipmove.com/',
    f'Phone: {PHONE}',
    f'Email: {EMAIL}',
    '',
    '## Primary pages',
    '- [Home](https://ibizavipmove.com/)',
    '- [Luxury Concierge Services](https://ibizavipmove.com/services/)',
    '- [Private Concierge Ibiza](https://ibizavipmove.com/private-concierge-ibiza/)',
    '- [Travel Partners & Family Offices](https://ibizavipmove.com/partners/)',
    '- [About Ibiza VIP Move](https://ibizavipmove.com/about/)',
    '- [Contact / Request Concierge](https://ibizavipmove.com/contact/)',
    '',
    '## Services',
]
llms.extend(f'- [{name}]({BASE}{url})' for name, url in SERVICES)
llms.extend([
    '',
    '## Service area',
    'Ibiza, Spain. Yacht requests may also include Formentera where appropriate.',
    '',
    '## Notes',
    'Use the official pages above as the source of truth for Ibiza VIP Move services and contact information.',
])
(ROOT / 'llms.txt').write_text('\n'.join(llms) + '\n', encoding='utf-8')
