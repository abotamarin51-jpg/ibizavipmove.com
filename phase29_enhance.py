from pathlib import Path
from html import escape

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
STYLE = '/assets/phase29.css?v=29'

# Publish Phase 29 stylesheet.
assets = ROOT / 'assets'
assets.mkdir(parents=True, exist_ok=True)
(assets / 'phase29.css').write_text(Path('phase29.css').read_text(encoding='utf-8'), encoding='utf-8')

SERVICE_META = {
    'private-chauffeur-ibiza': ('Move', 'Private Chauffeur & Transportation', 'Airport, hourly, full-day and multi-vehicle mobility.'),
    'luxury-villas-ibiza': ('Stay', 'Luxury Villas & Private Stays', 'Villa sourcing, preparation and in-stay coordination.'),
    'yacht-charter-ibiza': ('Sea', 'Yachts & Charters', 'Private yacht days, marinas and Formentera planning.'),
    'private-aviation-ibiza': ('Fly', 'Private Aviation', 'Flight, FBO, luggage and ground coordination.'),
    'restaurants-nightlife-ibiza': ('Access', 'Restaurants, Beach Clubs & Nightlife', 'Reservations, VIP tables, daybeds and nightlife logistics.'),
    'private-security-ibiza': ('Protect', 'Security & Close Protection', 'Discreet security support around the confirmed itinerary.'),
    'private-chef-staffing-ibiza': ('Stay', 'Private Chefs & Villa Staffing', 'Chefs, butlers, housekeeping and family support.'),
    'luxury-car-rental-ibiza': ('Move', 'Luxury & Supercar Rental', 'Executive cars, SUVs and supercars delivered discreetly.'),
    'wellness-ibiza': ('Stay', 'Wellness & Beauty', 'Private wellness, beauty and recovery at villa or hotel.'),
    'private-events-ibiza': ('Access', 'Private Events & Celebrations', 'Private occasions with guest logistics and production aligned.'),
    'bespoke-concierge-ibiza': ('Private Office', 'Lifestyle & Bespoke Requests', 'Tailor-made requests handled through one trusted contact.'),
}

RELATED = {
    'private-chauffeur-ibiza': ['luxury-villas-ibiza', 'restaurants-nightlife-ibiza', 'private-aviation-ibiza'],
    'luxury-villas-ibiza': ['private-chauffeur-ibiza', 'private-chef-staffing-ibiza', 'wellness-ibiza'],
    'yacht-charter-ibiza': ['private-chauffeur-ibiza', 'restaurants-nightlife-ibiza', 'luxury-villas-ibiza'],
    'private-aviation-ibiza': ['private-chauffeur-ibiza', 'private-security-ibiza', 'luxury-villas-ibiza'],
    'restaurants-nightlife-ibiza': ['private-chauffeur-ibiza', 'yacht-charter-ibiza', 'private-security-ibiza'],
    'private-security-ibiza': ['private-chauffeur-ibiza', 'private-aviation-ibiza', 'restaurants-nightlife-ibiza'],
    'private-chef-staffing-ibiza': ['luxury-villas-ibiza', 'wellness-ibiza', 'private-events-ibiza'],
    'luxury-car-rental-ibiza': ['private-chauffeur-ibiza', 'luxury-villas-ibiza', 'yacht-charter-ibiza'],
    'wellness-ibiza': ['luxury-villas-ibiza', 'private-chef-staffing-ibiza', 'private-events-ibiza'],
    'private-events-ibiza': ['private-chef-staffing-ibiza', 'private-chauffeur-ibiza', 'private-security-ibiza'],
    'bespoke-concierge-ibiza': ['luxury-villas-ibiza', 'restaurants-nightlife-ibiza', 'private-chauffeur-ibiza'],
}


def related_section(slug):
    cards = []
    for target in RELATED[slug]:
        eyebrow, title, copy = SERVICE_META[target]
        cards.append(
            f'<a class="ivm-related-card" href="/{target}/">'
            f'<small>{escape(eyebrow)}</small>'
            f'<div><strong>{escape(title)}</strong><p>{escape(copy)}</p></div>'
            f'<b>Explore service →</b></a>'
        )
    return (
        '<section class="ivm-related"><div class="ivm-related-inner">'
        '<div class="ivm-related-head"><div><div class="eyebrow">Complete the itinerary</div>'
        '<h2>Designed to work together.</h2></div>'
        '<p>Most high-level Ibiza stays involve more than one moving part. These services are commonly coordinated together through one point of contact.</p></div>'
        f'<div class="ivm-related-grid">{"".join(cards)}</div>'
        '</div></section>'
    )


# Add elegant cross-service navigation to every core service page.
for slug in SERVICE_META:
    page = ROOT / slug / 'index.html'
    if not page.exists():
        raise SystemExit(f'Missing canonical service page: {page}')
    html = page.read_text(encoding='utf-8')
    if STYLE not in html:
        html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
    if 'class="ivm-related"' not in html:
        marker = '<section class="closing-simple">'
        if marker not in html:
            raise SystemExit(f'Closing CTA marker missing on {slug}')
        html = html.replace(marker, related_section(slug) + marker, 1)
    page.write_text(html, encoding='utf-8')


# Consolidate verified legacy service paths without placing aliases in the sitemap.
ALIASES = {
    'services/chauffeur': '/private-chauffeur-ibiza/',
    'services/transfers': '/private-chauffeur-ibiza/',
    'services/villas': '/luxury-villas-ibiza/',
    'services/yachts': '/yacht-charter-ibiza/',
    'services/aviation': '/private-aviation-ibiza/',
    'services/nightlife': '/restaurants-nightlife-ibiza/',
    'services/security': '/private-security-ibiza/',
    'services/staffing': '/private-chef-staffing-ibiza/',
}


def alias_page(target):
    canonical = BASE + target
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ibiza VIP Move</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{canonical}"><meta http-equiv="refresh" content="0;url={canonical}"><script>location.replace({canonical!r});</script></head><body><main><p>This page has moved to <a href="{canonical}">{canonical}</a>.</p></main></body></html>'''

for legacy, target in ALIASES.items():
    d = ROOT / legacy
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(alias_page(target), encoding='utf-8')

# Phase 29 validation.
for slug in SERVICE_META:
    html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
    assert STYLE in html
    assert html.count('class="ivm-related"') == 1
    assert html.count('class="ivm-related-card"') == 3

sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
for legacy, target in ALIASES.items():
    alias_html = (ROOT / legacy / 'index.html').read_text(encoding='utf-8')
    assert 'noindex,follow' in alias_html
    assert f'<link rel="canonical" href="{BASE + target}">' in alias_html
    assert f'{BASE}/{legacy}/' not in sitemap

assert (ROOT / 'assets' / 'phase29.css').stat().st_size > 1000
print('PASS: Phase 29 architecture, related services and legacy consolidation')
