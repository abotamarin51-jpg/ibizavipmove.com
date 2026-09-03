from pathlib import Path
import re

ROOT = Path('_site')
STYLE = '/assets/phase31.css?v=31'
CSS_SRC = Path('phase31.css')
CSS_DEST = ROOT / 'assets' / 'phase31.css'

TARGETS = {
    'private-concierge-ibiza': [
        ('Private Office', 'One point of contact', 'Concierge, transport and lifestyle requests aligned around one brief.'),
        ('Ibiza based', 'Local coordination', 'A clear on-island line of communication throughout the stay.'),
        ('Private support', 'From arrival to departure', 'Support scales from one request to a complete itinerary.'),
    ],
    'private-chauffeur-ibiza': [
        ('Move', 'Airport to after-hours', 'Private transport around villas, hotels, marinas, dining and nightlife.'),
        ('Private itinerary', 'One movement plan', 'Single transfers and multi-stop schedules coordinated around the same brief.'),
        ('Connected service', 'More than the drive', 'Transport can be aligned with aviation, security and concierge requests.'),
    ],
    'luxury-villas-ibiza': [
        ('Stay', 'Curated private stays', 'Villa sourcing and stay requirements coordinated around the client brief.'),
        ('Before arrival', 'Ready when you land', 'Preparation, practical requirements and arrival timing clarified in advance.'),
        ('During the stay', 'Lifestyle support', 'Staffing, transport, wellness and dining can be connected around the villa.'),
    ],
    'yacht-charter-ibiza': [
        ('Sea', 'Ibiza & Formentera', 'Private yacht and day-charter planning around the confirmed itinerary.'),
        ('On the water', 'Details aligned', 'Marina, crew, catering and timing coordinated before departure.'),
        ('Door to deck', 'Ground coordination', 'Chauffeur and shore-side plans can be connected to the yacht day.'),
    ],
    'restaurants-nightlife-ibiza': [
        ('Access', 'Day into night', 'Dining, beach clubs and nightlife requests coordinated around the stay.'),
        ('Timing matters', 'Transport aligned', 'Movements can be planned around reservations and confirmed access.'),
        ('By request', 'Availability confirmed', 'Access, deposits and supplier terms are clarified before confirmation.'),
    ],
    'private-aviation-ibiza': [
        ('Fly', 'Flight to ground', 'Private aviation support coordinated with the Ibiza arrival or departure plan.'),
        ('Arrival detail', 'FBO, luggage, timing', 'Operational requirements are clarified before the movement.'),
        ('Connected service', 'Chauffeur on landing', 'Ground transport and other private services can be aligned around the flight.'),
    ],
    'private-security-ibiza': [
        ('Protect', 'Discreet private support', 'Close protection and private security coordinated around the client itinerary.'),
        ('Movement', 'Security in context', 'Transport, venues and schedules can be considered as one operational brief.'),
        ('Private handling', 'Need-to-know coordination', 'Sensitive details are kept within the confirmed service workflow.'),
    ],
}


def add_body_class(text, cls):
    m = re.search(r'<body(?:\s+class="([^"]*)")?>', text, re.I)
    if not m:
        return text
    classes = (m.group(1) or '').split()
    if cls not in classes:
        classes.append(cls)
    replacement = '<body class="' + ' '.join(x for x in classes if x) + '">'
    return text[:m.start()] + replacement + text[m.end():]


def build_rail(items):
    parts = []
    for eyebrow, title, copy in items:
        parts.append(
            '<article>'
            f'<span>{eyebrow}</span>'
            f'<strong>{title}</strong>'
            f'<small>{copy}</small>'
            '</article>'
        )
    return '<div class="ivm-inner-rail">' + ''.join(parts) + '</div>'


def insert_rail(text, rail):
    hero = re.search(r'(<section class="[^"]*\bpage-hero\b[^"]*".*?</section>)', text, re.I | re.S)
    if not hero:
        raise SystemExit('Signature page missing page-hero')
    block = hero.group(1)
    if 'ivm-inner-rail' in block:
        return text
    marker = '</div></section>'
    pos = block.rfind(marker)
    if pos == -1:
        raise SystemExit('Signature page hero wrapper marker missing')
    block = block[:pos] + rail + block[pos:]
    return text[:hero.start()] + block + text[hero.end():]


CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'), encoding='utf-8')

for slug, items in TARGETS.items():
    page = ROOT / slug / 'index.html'
    if not page.exists():
        raise SystemExit(f'Missing Phase 31 target: {slug}')
    html = page.read_text(encoding='utf-8')
    if '<html lang="en"' not in html:
        raise SystemExit(f'Unexpected non-English Phase 31 target: {slug}')
    html = add_body_class(html, 'ivm-signature-inner')
    if STYLE not in html:
        html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
    html = insert_rail(html, build_rail(items))
    page.write_text(html, encoding='utf-8')

# Release validation.
assert CSS_DEST.exists() and CSS_DEST.stat().st_size > 5000
for slug in TARGETS:
    html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
    assert 'ivm-signature-inner' in html, slug
    assert STYLE in html, slug
    assert html.count('class="ivm-inner-rail"') == 1, slug
    assert html.count('<article>') >= 3, slug
    assert 'page-hero-media' in html, slug
    assert html.count('<h1') == 1, slug
    assert '<link rel="canonical"' in html, slug

print(f'PASS: Phase 31 signature editorial treatment applied to {len(TARGETS)} core inner pages')
