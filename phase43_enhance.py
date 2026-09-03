from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
CSS_HREF = '/assets/phase43.css?v=43'

ARTICLES = {
    'private-arrival': {
        'label': 'Private Arrival',
        'title': 'The Private Arrival',
        'summary': 'Aviation, luggage, chauffeur and villa readiness aligned before the principal lands.',
        'service': ('/private-aviation-ibiza/', 'Private Aviation', 'Coordinate the ground movement around the aircraft, luggage and onward itinerary.'),
        'related': ['private-aviation-ground-coordination', 'villa-arrival-planning', 'ibiza-august-planning'],
    },
    'ibiza-formentera-yacht-day': {
        'label': 'At Sea',
        'title': 'Ibiza & Formentera by Yacht',
        'summary': 'Marina timing, chauffeur movements, dining and the evening connected as one sea-day plan.',
        'service': ('/yacht-charter-ibiza/', 'Yachts & Formentera', 'Build the yacht day into the wider stay, from villa pickup to the return ashore.'),
        'related': ['ibiza-august-planning', 'nightlife-transport-planning', 'private-arrival'],
    },
    'ibiza-august-planning': {
        'label': 'Peak Season',
        'title': 'The August Brief',
        'summary': 'A practical framework for Ibiza when availability, traffic and operational pressure are at their highest.',
        'service': ('/private-concierge-ibiza/', 'Private Concierge', 'Keep the peak-season brief under one Ibiza-based line of coordination.'),
        'related': ['nightlife-transport-planning', 'villa-arrival-planning', 'ibiza-formentera-yacht-day'],
    },
    'villa-arrival-planning': {
        'label': 'Private Stays',
        'title': 'The Villa Arrival Brief',
        'summary': 'Access, luggage, chauffeur timing and the first hours of a private villa stay aligned in advance.',
        'service': ('/luxury-villas-ibiza/', 'Private Villas', 'Coordinate the stay around access, privacy, guest movements and the wider itinerary.'),
        'related': ['private-arrival', 'private-aviation-ground-coordination', 'ibiza-august-planning'],
    },
    'nightlife-transport-planning': {
        'label': 'Access & Movement',
        'title': 'The Nightlife Movement Plan',
        'summary': 'Villa, dinner, nightlife, changing pickup times and split departures planned as one movement.',
        'service': ('/restaurants-nightlife-ibiza/', 'Dining & Nightlife', 'Align reservations and access with the private transport plan around the evening.'),
        'related': ['ibiza-august-planning', 'ibiza-formentera-yacht-day', 'villa-arrival-planning'],
    },
    'private-aviation-ground-coordination': {
        'label': 'Private Aviation',
        'title': 'From Aircraft to Ibiza',
        'summary': 'Flight timing, luggage, vehicle capacity and villa readiness connected into one ground handoff.',
        'service': ('/private-aviation-ibiza/', 'Private Aviation', 'Connect aircraft arrival, luggage and onward chauffeur movements through one local brief.'),
        'related': ['private-arrival', 'villa-arrival-planning', 'ibiza-august-planning'],
    },
}


def related_markup(slug, data):
    cards = []
    for rel_slug in data['related']:
        rel = ARTICLES[rel_slug]
        cards.append(
            f'<a class="ivm-intelligence-related-card" href="/ibiza-intelligence/{rel_slug}/">'
            f'<span>{rel["label"]}</span><strong>{rel["title"]}</strong>'
            f'<p>{rel["summary"]}</p><b>Read next →</b></a>'
        )
    service_href, service_title, service_copy = data['service']
    related = (
        '<section class="ivm-intelligence-related" aria-label="Related Ibiza Black Book notes">'
        '<div class="ivm-intelligence-related-inner">'
        '<div class="ivm-intelligence-related-head"><div><div class="eyebrow">Continue the Black Book</div>'
        '<h2>Related planning notes.</h2></div><p>Keep the operational context connected. These notes cover the adjacent moments most likely to affect the same private itinerary.</p></div>'
        f'<div class="ivm-intelligence-related-grid">{"".join(cards)}</div></div></section>'
    )
    service = (
        '<section class="ivm-intelligence-service"><div class="ivm-intelligence-service-inner">'
        f'<div><h3>{service_title}</h3><p>{service_copy}</p></div>'
        f'<a class="btn dark" href="{service_href}">Explore service</a></div></section>'
    )
    return service + related


def enrich_schema(text, slug, data):
    canonical = BASE + f'/ibiza-intelligence/{slug}/'
    related_urls = [BASE + f'/ibiza-intelligence/{s}/' for s in data['related']]
    service_url = BASE + data['service'][0]
    pattern = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)

    def repl(match):
        try:
            obj = json.loads(match.group(1))
        except Exception:
            return match.group(0)
        if not isinstance(obj, dict):
            return match.group(0)
        typ = obj.get('@type')
        if typ in ('Article', 'BlogPosting', 'WebPage') and obj.get('url', canonical).rstrip('/') == canonical.rstrip('/'):
            obj['isRelatedTo'] = [{'@type': 'WebPage', 'url': url} for url in related_urls]
            obj['mentions'] = {'@type': 'Service', 'name': data['service'][1], 'url': service_url}
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

    return pattern.sub(repl, text)


# Deploy the dedicated editorial stylesheet.
source_css = Path('phase43.css')
if not source_css.exists():
    raise SystemExit('phase43.css missing')
asset_css = ROOT / 'assets' / 'phase43.css'
asset_css.write_text(source_css.read_text(encoding='utf-8'), encoding='utf-8')

updated = 0
for slug, data in ARTICLES.items():
    path = ROOT / 'ibiza-intelligence' / slug / 'index.html'
    if not path.exists():
        raise SystemExit(f'Black Book article missing: {slug}')
    text = path.read_text(encoding='utf-8')
    if CSS_HREF not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{CSS_HREF}"></head>', 1)
    if 'ivm-intelligence-related' not in text:
        text = text.replace('</main>', related_markup(slug, data) + '</main>', 1)
    text = enrich_schema(text, slug, data)
    path.write_text(text, encoding='utf-8')
    updated += 1

# Add a collection relationship to the Black Book hub itself.
hub = ROOT / 'ibiza-intelligence' / 'index.html'
if hub.exists():
    text = hub.read_text(encoding='utf-8')
    if CSS_HREF not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{CSS_HREF}"></head>', 1)
    hub.write_text(text, encoding='utf-8')

# Validation: every article must have exactly three editorial links and one commercial pathway.
for slug, data in ARTICLES.items():
    text = (ROOT / 'ibiza-intelligence' / slug / 'index.html').read_text(encoding='utf-8')
    assert text.count('ivm-intelligence-related-card') == 3, slug
    assert 'ivm-intelligence-service' in text, slug
    assert data['service'][0] in text, slug
    for related_slug in data['related']:
        assert f'/ibiza-intelligence/{related_slug}/' in text, (slug, related_slug)
    assert CSS_HREF in text, slug
assert asset_css.exists() and asset_css.stat().st_size > 1000
print(f'PASS: Phase 43 Black Book interlinked across {updated} planning notes with service pathways')
