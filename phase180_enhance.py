"""Create the English VIP Tables & Club Access page from the final Private Concierge template.

The source of truth for copy is the approved English VIP tables brief, with specific
factual corrections. The canonical Organization and WebSite nodes come from the site's
generated Private Concierge and Home pages, avoiding invented identity fields.
A separately approved generated-schema.json may optionally add verified properties.
No unconfirmed prices, guaranteed venue access or owner-only placeholders are published.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
TEMPLATE = ROOT / 'private-concierge-ibiza' / 'index.html'
HOME = ROOT / 'index.html'
TARGET = ROOT / 'vip-tables-club-access-ibiza' / 'index.html'
GENERATED_SCHEMA = Path('generated-schema.json')
BASE = 'https://ibizavipmove.com'
PATH = '/vip-tables-club-access-ibiza/'
CANONICAL = BASE + PATH
LASTMOD = '2026-10-31'
TITLE = 'Ibiza VIP Table & Bottle Service Booking | Ibiza VIP Move'
DESCRIPTION = (
    'VIP tables, bottle service and club access in Ibiza, arranged privately. '
    'Minimum spend, deposits and terms confirmed upfront. Request availability today.'
)
WA = (
    'https://wa.me/34600703303?text=Hello%20Ibiza%20VIP%20Move%2C%20I%27d%20like%20to%20request%20a%20VIP%20table%20in%20Ibiza.'
    '%20Could%20you%20please%20help%20me%20with%20availability%20and%20the%20next%20steps%3F%20Thank%20you.'
)
VISIBLE_DATE = '31 October 2026'
SOCIAL_SOURCE = ROOT / 'assets/images/private-office.jpg'
SOCIAL_TARGET = ROOT / 'assets/images/vip-tables-social.jpg'
SOCIAL_PUBLIC = '/assets/images/vip-tables-social.jpg'
SOCIAL_IMAGE = BASE + SOCIAL_PUBLIC
SCRIPT_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
    re.I | re.S,
)

FAQS = [
    (
        'How much does a VIP table cost in Ibiza?',
        "It depends on the venue, the date, the night's program, table position and group size. "
        'Many venues use a minimum spend on drinks or bottle service rather than a fixed table fee. '
        'Whether food counts toward that minimum and whether a deposit is required depend on the venue. '
        'We confirm the minimum spend, inclusions, deposit and terms in writing before booking.',
    ),
    (
        'Can I change or cancel an Ibiza VIP table booking?',
        'Each venue and event has its own deadline, deposit and refund or date-transfer terms. '
        'Before paying, ask us to confirm those terms and how cancellation requests must be submitted. '
        'We can relay a change request, but approval and any refund or credit depend on the provider.',
    ),
    (
        'Can you guarantee a table or entry at a specific club?',
        'No. Availability and access are controlled by each venue and can change quickly in peak season. '
        'We tell you clearly what is requested, what is being checked and what is confirmed, and we do not '
        'describe third-party availability as guaranteed.',
    ),
    (
        'How far in advance should I book a VIP table in Ibiza?',
        'Earlier is better, especially for July and August and for headline nights. Last-minute requests can '
        'still be assessed, but options are usually narrower.',
    ),
    (
        'Does a VIP table include entry?',
        'That varies by venue and night. Some table bookings include entry for the group and others do not. '
        'We confirm this, along with any separate ticket requirement, before you commit.',
    ),
    (
        'What is the difference between bottle service and a VIP table?',
        "A VIP table is the reserved seating. Bottle service is how it is typically served, with bottles and "
        "mixers bought against the table's minimum spend. In practice the two terms are used together.",
    ),
    (
        'Can you arrange transport and security for the night?',
        'Yes. We can coordinate private chauffeur transport to and from the venue and private security where '
        'requested, so arrival and return are planned together with the table.',
    ),
    (
        'Can a PA, family office or travel advisor book on behalf of a client?',
        'Yes. Representatives can send the brief directly and agree who approves changes and how confirmations '
        'are shared.',
    ),
    (
        'What should I bring, and is there a dress code?',
        'Venues set their own age, ID and entry policies. Bring valid photo ID for everyone in your group, and '
        'ask us about dress expectations for your chosen venue.',
    ),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def json_nodes(text: str) -> list[dict]:
    nodes: list[dict] = []
    for match in SCRIPT_RE.finditer(text):
        try:
            payload = json.loads(match.group(1))
        except Exception:
            continue
        if isinstance(payload, dict) and isinstance(payload.get('@graph'), list):
            nodes.extend(node for node in payload['@graph'] if isinstance(node, dict))
        elif isinstance(payload, dict):
            nodes.append(payload)
    return nodes


def node_by_id(nodes: list[dict], node_id: str, node_type: str | None = None) -> dict | None:
    for node in nodes:
        types = node.get('@type')
        types = types if isinstance(types, list) else [types]
        if node.get('@id') == node_id and (node_type is None or node_type in types):
            return deepcopy(node)
    return None


def merge_lists(base: list, overlay: list) -> list:
    out = deepcopy(base)
    seen = {json.dumps(item, sort_keys=True, ensure_ascii=False) for item in out}
    for item in overlay:
        key = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            out.append(deepcopy(item))
            seen.add(key)
    return out


def deep_merge(base, overlay):
    if isinstance(base, dict) and isinstance(overlay, dict):
        out = deepcopy(base)
        for key, value in overlay.items():
            if key in out:
                out[key] = deep_merge(out[key], value)
            else:
                out[key] = deepcopy(value)
        return out
    if isinstance(base, list) and isinstance(overlay, list):
        return merge_lists(base, overlay)
    return deepcopy(overlay)


def load_external_schema() -> tuple[dict | None, dict | None]:
    if not GENERATED_SCHEMA.is_file():
        return None, None
    payload = json.loads(GENERATED_SCHEMA.read_text(encoding='utf-8'))
    nodes = payload.get('@graph', []) if isinstance(payload, dict) else []
    if isinstance(payload, dict) and not nodes:
        nodes = [payload]
    require(isinstance(nodes, list), 'generated-schema.json must contain an object or @graph array')
    clean = [node for node in nodes if isinstance(node, dict)]
    org = node_by_id(clean, BASE + '/#organization', 'Organization')
    website = node_by_id(clean, BASE + '/#website', 'WebSite')
    require(org is not None, 'generated-schema.json has no Organization node with the canonical @id')
    return org, website


def set_title(html: str, value: str) -> str:
    updated, count = re.subn(r'<title>.*?</title>', f'<title>{escape(value)}</title>', html, count=1, flags=re.I | re.S)
    require(count == 1, 'template title missing or duplicated')
    return updated


def set_meta(html: str, attr: str, name: str, value: str) -> str:
    pattern = re.compile(
        rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])[^>]*>',
        re.I,
    )
    tag = f'<meta {attr}="{escape(name, quote=True)}" content="{escape(value, quote=True)}">'
    if pattern.search(html):
        return pattern.sub(tag, html, count=1)
    return html.replace('</head>', tag + '</head>', 1)


def set_canonical(html: str) -> str:
    pattern = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', re.I)
    updated, count = pattern.subn(f'<link rel="canonical" href="{CANONICAL}">', html, count=1)
    require(count == 1, 'template canonical missing or duplicated')
    return updated


def schema_script(node: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(
        node, ensure_ascii=False, separators=(',', ':')
    ) + '</script>'


def page_schema() -> tuple[dict, dict, dict, dict]:
    webpage = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        '@id': CANONICAL + '#webpage',
        'url': CANONICAL,
        'name': TITLE,
        'description': DESCRIPTION,
        'inLanguage': 'en',
        'isPartOf': {'@id': BASE + '/#website'},
        'about': {'@id': CANONICAL + '#service'},
        'publisher': {'@id': BASE + '/#organization'},
        'dateModified': LASTMOD,
    }
    service = {
        '@context': 'https://schema.org',
        '@type': 'Service',
        '@id': CANONICAL + '#service',
        'name': 'VIP Tables & Club Access Ibiza',
        'serviceType': 'VIP table and club access concierge',
        'alternateName': ['Ibiza VIP Table', 'Ibiza Bottle Service', 'Ibiza Club Access'],
        'description': (
            'Private concierge service to request VIP tables, bottle service and club access in Ibiza, '
            'with chauffeur transport and security coordinated around the night.'
        ),
        'url': CANONICAL,
        'provider': {'@id': BASE + '/#organization'},
        'areaServed': {'@type': 'Place', 'name': 'Ibiza, Balearic Islands, Spain'},
        'audience': {
            '@type': 'Audience',
            'audienceType': (
                'Private clients, personal assistants, family offices and travel advisors planning nights out in Ibiza'
            ),
        },
    }
    breadcrumb = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ibiza VIP Move', 'item': BASE + '/'},
            {
                '@type': 'ListItem',
                'position': 2,
                'name': 'Restaurants & Nightlife Ibiza',
                'item': BASE + '/restaurants-nightlife-ibiza/',
            },
            {
                '@type': 'ListItem',
                'position': 3,
                'name': 'VIP Tables & Club Access Ibiza',
                'item': CANONICAL,
            },
        ],
    }
    faq = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': question,
                'acceptedAnswer': {'@type': 'Answer', 'text': answer},
            }
            for question, answer in FAQS
        ],
    }
    return webpage, service, breadcrumb, faq


def data_table(headers: tuple[str, ...], rows: list[tuple[str, ...]], label: str) -> str:
    head = ''.join(f'<th scope="col">{escape(value)}</th>' for value in headers)
    body = ''.join(
        '<tr>' + ''.join(f'<td>{escape(value)}</td>' for value in row) + '</tr>'
        for row in rows
    )
    return (
        '<div style="overflow-x:auto"><table data-ivm180="table" '
        'style="width:100%;border-collapse:collapse" aria-label="' + escape(label, quote=True) + '">'
        '<thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>'
    )


def main_html() -> str:
    options = data_table(
        ('Option', 'What it is', 'Best for'),
        [
            (
                'VIP table / bottle service',
                'A reserved table for your group, with drinks bought against a minimum spend',
                'Groups that want a fixed place to host',
            ),
            ('Tickets / entry', 'Admission to the event without a table', 'Individuals or small groups'),
            (
                'Guest list',
                'Entry arrangement controlled by the venue, available only on certain nights',
                'Flexible plans where a table is not needed',
            ),
        ],
        'VIP tables, tickets and guest list comparison',
    )
    venues = data_table(
        ('Venue', 'Area', 'Format'),
        [
            ('Pacha Ibiza', 'Ibiza Town', 'Club'),
            ("Ushuaïa Ibiza", "Playa d'en Bossa", 'Open-air day and night venue'),
            ('Hï Ibiza', "Playa d'en Bossa", 'Club'),
            ('Amnesia', 'San Rafael', 'Club'),
            ('[UNVRS]', 'San Rafael (Sant Rafel)', 'Nightclub'),
            ('DC10', 'Near Ibiza Airport', 'Club'),
            ('Lío Ibiza', 'Ibiza Town port', 'Dinner and cabaret show'),
            ('O Beach Ibiza', 'Sant Antoni de Portmany', 'Day club'),
        ],
        'Ibiza venues clients ask about',
    )
    faq_html = ''.join(
        '<details><summary>' + escape(question) + '</summary><p>' + escape(answer) + '</p></details>'
        for question, answer in FAQS
    )
    return f'''<main id="main-content">
<section class="page-hero" style="--hero:url('{SOCIAL_PUBLIC}')">
  <div class="page-hero-media"><img src="{SOCIAL_PUBLIC}" alt="Illustrative editorial photograph for private concierge planning" width="1200" height="630" fetchpriority="high" decoding="async"></div>
  <div>
    <div class="kicker light">VIP Tables · Club Access · Ibiza</div>
    <h1>VIP tables and club access in Ibiza, arranged privately.</h1>
    <p>One concierge to request tables, bottle service and club entry, and to coordinate the transport and security around the night.</p>
    <a class="btn gold" href="{WA}">Request a table</a>
    <p>Last updated: {VISIBLE_DATE}</p>
    <div class="ivm-inner-rail">
      <article><span>Table requests</span><strong>Terms before confirmation</strong><small>Minimum spend, deposit, arrival time and entry conditions clarified in writing.</small></article>
      <article><span>Club access</span><strong>Venue-controlled availability</strong><small>Requests are checked for the chosen date and night; third-party access is never guaranteed.</small></article>
      <article><span>Whole night</span><strong>Transport and security</strong><small>Arrival, return and requested private security can be coordinated around the same plan.</small></article>
    </div>
  </div>
</section>
<section class="editorial service-detail">
  <div><div class="kicker dark">Direct answer</div><h2>What is a VIP table in Ibiza?</h2></div>
  <div><p class="large">A VIP table in Ibiza is a reserved table at a club or beach club, often booked against a minimum spend for drinks or bottle service. Whether food counts, any required deposit and the agreed arrival time depend on the venue and event. Ibiza VIP Move requests tables and club access for private clients, assistants and travel advisors, and confirms the price, minimum spend and conditions in writing before anything is treated as booked.</p></div>
</section>
<section class="editorial">
  <div><div class="kicker dark">Choose the format</div><h2>Tables, tickets and guest list: what is the difference?</h2></div>
  <div>{options}<p>Whether a table booking includes entry varies by venue and night. We confirm this, and any separate ticket requirement, before you commit.</p></div>
</section>
<section class="editorial">
  <div><div class="kicker dark">Ibiza venues</div><h2>Venues our clients ask about</h2></div>
  <div><p class="large">These venues are examples for planning, not confirmed booking relationships. Share your preferred venue and date so we can check whether a request is possible.</p>{venues}<p>Programs, policies and availability change by season and by night. Venue names are trademarks of their respective owners and are used for reference only. Ibiza VIP Move is an independent concierge and is not affiliated with or endorsed by these venues.</p></div>
</section>
<section class="process">
  <div class="section-head"><div class="kicker dark">Booking process</div><h2>How booking a VIP table works</h2></div>
  <div class="process-grid">
    <article><span>01 · Brief</span><h3>Send your brief.</h3><p>Dates, group size, preferred venues or nights, and any budget guidance.</p></article>
    <article><span>02 · Check</span><h3>We check availability.</h3><p>You see clearly what is requested, what is being checked and what is confirmed.</p></article>
    <article><span>03 · Terms</span><h3>Terms in writing.</h3><p>Minimum spend, deposit, cancellation terms and arrival time are agreed before anything is secured.</p></article>
    <article><span>04 · Confirm</span><h3>Confirmation.</h3><p>A table is treated as booked only once the venue's terms are agreed.</p></article>
    <article><span>05 · Coordinate</span><h3>The night itself.</h3><p>Chauffeur transport, arrival timing and, where requested, private security are coordinated around the same plan.</p></article>
  </div>
</section>
<section class="editorial">
  <div><div class="kicker dark">Pricing factors</div><h2>What affects the price of a VIP table in Ibiza</h2></div>
  <div><p class="large">Prices are set by each venue and vary by request. The main factors are:</p><ul class="premium-list"><li><strong>The date and season.</strong> Peak summer nights are in highest demand.</li><li><strong>The night's program.</strong> Headline events typically cost more than quieter nights.</li><li><strong>Table position.</strong> Locations closer to the stage or dance floor are usually more sought after.</li><li><strong>Group size.</strong> Larger groups need larger tables and higher minimum spends.</li><li><strong>Format.</strong> Many tables are sold against a minimum spend rather than a flat fee, and a deposit is usually required.</li></ul><p>We confirm the exact figures in writing for each request. We do not quote a price before checking the venue and date.</p></div>
</section>
<section class="dark-panel">
  <div class="kicker light">From the United States</div><h2>Planning tips for US travelers</h2>
  <div class="trust-grid"><div><b>Book early for July and August.</b><p>Peak demand is concentrated in these months, and earlier requests leave more options.</p></div><div><b>Expect late nights.</b><p>Clubs in Ibiza are typically busiest late in the evening and after midnight, so plan dinner and transport around that.</p></div><div><b>Mind the time difference.</b><p>Ibiza is usually six hours ahead of US Eastern time, but the gap can briefly be five hours when daylight-saving dates differ. Check the time for your dates; WhatsApp requires the app and an internet connection.</p></div><div><b>Bring valid photo ID.</b><p>Venues set their own age, ID and entry policies.</p></div><div><b>Plan the way home.</b><p>A pre-booked chauffeur avoids the late-night taxi queue.</p></div></div>
</section>
<section class="editorial">
  <div><div class="kicker dark">Private and professional briefs</div><h2>Who we arrange this for</h2></div>
  <div><p class="large">Groups celebrating birthdays and milestone trips, bachelor and bachelorette weekends, private clients combining the night with a villa or yacht stay, and personal assistants, family offices and travel advisors booking on behalf of a client.</p></div>
</section>
<section class="partners-strip">
  <div><div class="kicker dark">Related services</div><h2>Build the whole night</h2><p>Combine your table with <a class="text-link" href="/private-chauffeur-ibiza/">private chauffeur transport</a>, a <a class="text-link" href="/luxury-villas-ibiza/">villa stay</a>, a <a class="text-link" href="/yacht-charter-ibiza/">yacht day</a>, <a class="text-link" href="/restaurants-nightlife-ibiza/">restaurant reservations</a> or <a class="text-link" href="/private-security-ibiza/">private security</a>. For a full stay under one brief, see <a class="text-link" href="/private-concierge-ibiza/">private concierge in Ibiza</a>.</p></div>
  <a class="btn dark" href="{WA}">Request a table</a>
</section>
<section class="faq">
  <div class="section-head"><div class="kicker dark">Private client FAQ</div><h2>VIP tables in Ibiza: frequently asked questions</h2></div>
  {faq_html}
</section>
<section class="closing-simple"><h2>Request your table.</h2><p>Send your dates, group size and preferred venues to begin.</p><a class="btn dark" href="{WA}">Speak to Concierge</a></section>
</main>'''


def update_head(template: str, home: str) -> str:
    html = template
    html = set_title(html, TITLE)
    html = set_meta(html, 'name', 'description', DESCRIPTION)
    html = set_meta(html, 'name', 'robots', 'index,follow,max-image-preview:large')
    html = set_meta(html, 'property', 'og:type', 'website')
    html = set_meta(html, 'property', 'og:site_name', 'Ibiza VIP Move')
    html = set_meta(html, 'property', 'og:locale', 'en_US')
    html = set_meta(html, 'property', 'og:title', TITLE)
    html = set_meta(html, 'property', 'og:description', DESCRIPTION)
    html = set_meta(html, 'property', 'og:url', CANONICAL)
    html = set_meta(html, 'property', 'og:image', SOCIAL_IMAGE)
    html = set_meta(html, 'property', 'og:image:alt', 'Illustrative editorial photograph for private concierge planning')
    html = set_meta(html, 'name', 'twitter:card', 'summary_large_image')
    html = set_meta(html, 'name', 'twitter:title', TITLE)
    html = set_meta(html, 'name', 'twitter:description', DESCRIPTION)
    html = set_meta(html, 'name', 'twitter:image', SOCIAL_IMAGE)
    html = set_canonical(html)

    # Only English exists for this canonical today. Keep the visible language-bar component,
    # but do not claim non-existent translated equivalents in head hreflang.
    html = re.sub(
        r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\'][^"\']+["\'])[^>]*>',
        '', html, flags=re.I,
    )
    alternates = (
        f'<link rel="alternate" hreflang="en" href="{CANONICAL}">'
        f'<link rel="alternate" hreflang="x-default" href="{CANONICAL}">'
    )
    html = html.replace('</head>', alternates + '</head>', 1)

    template_nodes = json_nodes(template)
    home_nodes = json_nodes(home)
    organization = node_by_id(template_nodes, BASE + '/#organization', 'Organization')
    website = node_by_id(home_nodes, BASE + '/#website', 'WebSite')
    require(organization is not None, 'template Organization schema missing')
    require(website is not None, 'homepage WebSite schema missing')
    external_org, external_website = load_external_schema()
    if external_org is not None:
        organization = deep_merge(organization, external_org)
    if external_website is not None:
        website = deep_merge(website, external_website)

    # Remove template page schemas and insert one Organization plus the requested page nodes.
    html = SCRIPT_RE.sub('', html)
    webpage, service, breadcrumb, faq = page_schema()
    scripts = ''.join(schema_script(node) for node in (
        organization, website, webpage, service, breadcrumb, faq
    ))
    html = html.replace('</head>', scripts + '</head>', 1)
    return html


def replace_main(html: str) -> str:
    updated, count = re.subn(r'<main\b[^>]*>.*?</main>', main_html(), html, count=1, flags=re.I | re.S)
    require(count == 1, 'template main missing or duplicated')
    return updated


def update_language_bar(html: str) -> str:
    nav = (
        '<nav class="ivm-language-links" aria-label="Choose language">'
        f'<a href="{CANONICAL}" hreflang="en" lang="en" aria-current="page"><b>EN</b><small>English</small></a>'
        '</nav>'
    )
    updated, count = re.subn(
        r'<nav\b[^>]*class="ivm-language-links"[^>]*>.*?</nav>',
        nav, html, count=1, flags=re.I | re.S,
    )
    require(count == 1, 'template language bar missing or duplicated')
    return updated


def add_internal_link(path: Path, marker: str, old: str, new: str) -> None:
    html = path.read_text(encoding='utf-8')
    if marker in html:
        require(html.count(marker) == 1, f'duplicate Phase 180 marker in {path}')
        return
    require(html.count(old) == 1, f'expected one insertion point in {path}')
    path.write_text(html.replace(old, new, 1), encoding='utf-8')


def update_links() -> None:
    marker = 'data-ivm180="vip-tables-link"'
    add_internal_link(
        ROOT / 'restaurants-nightlife-ibiza' / 'index.html', marker,
        '<p>Access, minimum spend, deposits, cancellation terms and table location depend on the venue and date. Nothing is represented as confirmed until the venue or relevant supplier has accepted the request.</p>',
        '<p>Access, minimum spend, deposits, cancellation terms and table location depend on the venue and date. Nothing is represented as confirmed until the venue or relevant supplier has accepted the request.</p>'
        '<p>For a dedicated table and bottle-service brief, see <a class="text-link" data-ivm180="vip-tables-link" href="/vip-tables-club-access-ibiza/">VIP Tables &amp; Club Access Ibiza</a>.</p>',
    )
    add_internal_link(
        ROOT / 'private-concierge-ibiza' / 'index.html', marker,
        'restaurant reservations, VIP tables, villas, yachts, security, staff and the unexpected.',
        'restaurant reservations, <a class="text-link" data-ivm180="vip-tables-link" href="/vip-tables-club-access-ibiza/">VIP tables</a>, villas, yachts, security, staff and the unexpected.',
    )
    add_internal_link(
        ROOT / 'vip-services-ibiza' / 'index.html', marker,
        '<a class="text-link" href="/restaurants-nightlife-ibiza/">Restaurants &amp; Nightlife Ibiza</a> · ',
        '<a class="text-link" href="/restaurants-nightlife-ibiza/">Restaurants &amp; Nightlife Ibiza</a> · '
        '<a class="text-link" data-ivm180="vip-tables-link" href="/vip-tables-club-access-ibiza/">VIP Tables &amp; Club Access Ibiza</a> · ',
    )
    add_internal_link(
        ROOT / 'private-chauffeur-ibiza' / 'index.html', marker,
        '<p class="ivm-concierge-continuity">Planning several services as one stay? ',
        '<p class="ivm-club-continuity">Planning a club night? <a class="text-link" data-ivm180="vip-tables-link" href="/vip-tables-club-access-ibiza/">Coordinate VIP tables and club access →</a></p>'
        '<p class="ivm-concierge-continuity">Planning several services as one stay? ',
    )


def update_sitemap() -> None:
    sitemap = ROOT / 'sitemap.xml'
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    tree = ET.parse(sitemap)
    root = tree.getroot()
    entries = []
    for node in root.findall(f'{{{ns}}}url'):
        loc = node.findtext(f'{{{ns}}}loc')
        if loc:
            entries.append((loc, node))
    matches = [node for loc, node in entries if loc.rstrip('/') + '/' == CANONICAL]
    if matches:
        require(len(matches) == 1, 'duplicate VIP Tables sitemap entry')
        node = matches[0]
        children = list(node)
        require([child.tag.split('}', 1)[-1] for child in children] == ['loc', 'lastmod'],
                'existing VIP Tables sitemap entry must contain only loc and lastmod')
        node.find(f'{{{ns}}}lastmod').text = LASTMOD
    else:
        node = ET.Element(f'{{{ns}}}url')
        ET.SubElement(node, f'{{{ns}}}loc').text = CANONICAL
        ET.SubElement(node, f'{{{ns}}}lastmod').text = LASTMOD
        root.append(node)
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)


def enhance() -> None:
    require(TEMPLATE.is_file(), 'final Private Concierge template missing')
    require(HOME.is_file(), 'final homepage missing')
    template = TEMPLATE.read_text(encoding='utf-8')
    home = HOME.read_text(encoding='utf-8')
    require(SOCIAL_TARGET.is_file(), 'licensed social image must be generated by the dedicated image stage')
    html = update_head(template, home)
    html = replace_main(html)
    html = update_language_bar(html)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(html, encoding='utf-8')
    update_links()
    update_sitemap()
    source = 'optional approved schema extension' if GENERATED_SCHEMA.is_file() else 'existing site Organization and WebSite'
    print('PASS: Phase 180 — VIP Tables page, social preview, four internal links and 157th sitemap canonical created; schema source: ' + source)


if __name__ == '__main__':
    enhance()
