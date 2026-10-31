"""Publish three distinct club-planning pages after the legacy 157-page build gates.

Venue facts were checked against each club's official FAQ on 31 October 2026.
These are independent concierge services, not venue-owned booking pages. Reuse the
final VIP page shell, approved imagery and organization identity; keep new copy,
page metadata, language links and schema local to each new canonical.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
from pathlib import Path
import re
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from phase180_enhance import json_nodes, node_by_id, schema_script, set_meta, set_title, SCRIPT_RE

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
HUB = '/vip-tables-club-access-ibiza/'
ACCESS = '/restaurants-nightlife-ibiza/'
DATE = '2026-10-31'
IMAGE = '/assets/images/vip-tables-social.jpg'
IMAGE_ALT = 'Illustrative editorial photograph for private concierge planning'
SM = 'http://www.sitemaps.org/schemas/sitemap/0.9'
IM = 'http://www.google.com/schemas/sitemap-image/1.1'

CLUBS = (
    {
        'slug': 'pacha-ibiza-vip-tables',
        'name': 'Pacha Ibiza',
        'title': 'Pacha Ibiza VIP Tables & Night Planning | Ibiza VIP Move',
        'description': 'Request a Pacha Ibiza VIP table with Ibiza VIP Move. Coordinate dinner, your table brief and private transport, with availability and terms checked for your date.',
        'intro': 'An Ibiza Town night, planned around your table. Bring dinner, the club and the journey home into one clear brief.',
        'area': 'Ibiza Town',
        'format': 'Dinner & club planning',
        'focus': 'Keep dinner and your club table distinct',
        'heading': 'A Pacha table starts with the whole evening.',
        'answer': 'Ibiza VIP Move coordinates Pacha Ibiza VIP table requests alongside dinner reservations and private transport. Send the event date, number of guests and whether you want dinner first. We check the available table options and provide the proposed spend, inclusions and conditions before you decide.',
        'sections': (
            ('Dinner before the club', 'Two reservations, one evening.',
             '<p>A restaurant table and a club VIP table serve different parts of the night. Pacha describes restaurant-linked admission as subject to a qualifying spend; this does not describe a reserved club VIP table.</p>'
             '<p>Tell us whether dinner should be at Pacha Restaurant or elsewhere in Ibiza Town. We can then coordinate the dining request, the club request and any movement between them. Keep the agreed dinner time and club arrival time together in the final itinerary.</p>'),
            ('Your table brief', 'Choose what matters to your group.',
             '<p>Start with the event date and the full guest count. Add whether the priority is a particular table position, keeping the group together or a spending limit. If your budget covers the whole evening, distinguish the table allowance from dinner and transport.</p>'
             '<p>Ask for the proposed table location, included guests, drinks allowance, any separate charges, deposit and cancellation terms in writing. If the first option does not fit, we can discuss which part of the brief is flexible before checking alternatives.</p>'),
            ('Arrival & return', 'Plan the Ibiza Town handover.',
             '<p>Pacha lists its address as Avenida 8 de Agosto, 07800 Ibiza. Share your hotel or villa area when requesting transport; the pickup time should follow your confirmed dinner and club arrangements.</p>'
             '<p>For a group arriving separately, name one lead guest and flag the different arrival times. Decide whether everyone returns together or needs separate departures, and note any early flight or yacht departure the following day.</p>'),
        ),
        'brief': 'Pacha event date; total guests; dinner at Pacha or another restaurant; preferred table arrangement; table budget or total evening budget; accommodation area; and return transport.',
        'faqs': (
            ('Does a Pacha Restaurant booking reserve a club VIP table?', 'No. Treat dinner and a club VIP table as separate requests. Tell us if you want both so each reservation and its inclusions can be checked explicitly.'),
            ('What does a Pacha VIP table cost?', 'Request a proposal for your event date and guest count. We confirm the table spend, included items, any concierge or transport charges and payment conditions in writing before you decide.'),
            ('Can you coordinate dinner and the chauffeur as well?', 'Yes. Include your preferred dinner area, accommodation area and whether the group needs one shared return or separate departures. Each requested service is confirmed separately within the evening plan.'),
        ),
        'source': 'https://pacha.com/contact-us',
        'source_label': 'Pacha location and official FAQ',
    },
    {
        'slug': 'hi-ibiza-vip-tables',
        'name': 'Hï Ibiza',
        'title': 'Hï Ibiza VIP Tables & Arrival Planning | Ibiza VIP Move',
        'description': 'Plan a Hï Ibiza VIP table with Ibiza VIP Move. Discuss the event, table layout, group arrivals and chauffeur return, with availability and written terms checked first.',
        'intro': 'Your Hï Ibiza night, from the table brief to the last pickup. Keep the event, arrival and return aligned.',
        'area': "Playa d’en Bossa",
        'format': 'Late-night club planning',
        'focus': 'Match the table to the event and group',
        'heading': 'The right brief goes beyond “VIP access”.',
        'answer': 'Ibiza VIP Move coordinates Hï Ibiza VIP table requests and the transport around your night. Share the event date, guest count and what matters about the table position. We check the proposed layout, spend and entry arrangements so you can review a specific option.',
        'sections': (
            ('Table or VIP ticket', 'Be clear about the experience you want.',
             '<p>Hï offers VIP common-area tickets for some events. That access is different from reserving a table for your group. Its table layout and price information are supplied after a request and can change.</p>'
             '<p>If a particular room, artist or view is the reason for your visit, put that in the brief. Ask to review the proposed table location and guest capacity before accepting it. A general wish for “the best table” leaves too much open to interpretation.</p>'),
            ('The event date', 'Make the after-midnight timing clear.',
             '<p>Use the event date shown on your booking when requesting the table. Separately record the actual local date and time for each chauffeur pickup, particularly when arrival or the return falls after midnight.</p>'
             '<p>For example, a return at 04:00 belongs to the following calendar day. If some guests join after dinner while others arrive later, share both movements so the lead guest and driver have the same plan.</p>'),
            ('Before & after Hï', 'Connect the night without assuming access.',
             '<p>Hï is in Playa d’en Bossa. Its official FAQ places the VIP entrance at the front, on the right. Use the instructions in your booking for the final meeting point.</p>'
             '<p>Combining Ushuaïa and Hï requires separate admission arrangements. Tell us which event you plan first, whether you need time back at your accommodation and who is continuing to Hï. Then we can plan each movement and request independently.</p>'),
        ),
        'brief': 'Hï event date; guest count; preferred room or table position; spending guidance; earlier dinner or Ushuaïa plans; separate guest arrivals; and the local date and time for the return.',
        'faqs': (
            ('Is a Hï VIP ticket the same as a reserved table?', 'No. A VIP common-area ticket, where offered, is a different option. Specify that you want a table and ask for its location, capacity and booking conditions.'),
            ('How many guests can share a Hï table?', 'The capacity depends on the proposed table. Give us the full guest count and any separate arrivals so capacity and admission can be checked against that exact option.'),
            ('Can you coordinate the return after Hï?', 'Yes. State the return destination, actual local date and preferred pickup time. If the group may split, ask for the separate movements and any waiting arrangements to be quoted in advance.'),
        ),
        'source': 'https://www.hiibiza.com/contact-faq',
        'source_label': 'Hï Ibiza official access and VIP FAQ',
    },
    {
        'slug': 'ushuaia-ibiza-vip-tables',
        'name': 'Ushuaïa Ibiza',
        'title': 'Ushuaïa Ibiza VIP Tables & Event Planning | Ibiza VIP Move',
        'description': 'Request an Ushuaïa Ibiza VIP table with Ibiza VIP Move. Plan your group, bottle-service brief, event arrival and onward transport with clear written booking terms.',
        'intro': 'An open-air Ibiza event with the details coordinated. Plan your table, arrival and what comes next.',
        'area': "Playa d’en Bossa",
        'format': 'Open-air event planning',
        'focus': 'Plan the afternoon and onward evening',
        'heading': 'Build the day around your Ushuaïa event.',
        'answer': 'Ibiza VIP Move coordinates Ushuaïa Ibiza VIP table requests with transport and the plans either side of the event. Share the date, number of guests and your earlier activities so the proposed table and arrival arrangements fit the day you actually want.',
        'sections': (
            ('Before the event', 'Leave space between a yacht day and the club.',
             '<p>An Ushuaïa request needs an event-specific arrival plan. If you are coming from a yacht, beach lunch or airport arrival, share that schedule before fixing the transfer. Allow time to return to your accommodation, change and meet the group where needed.</p>'
             '<p>Choose the event first, then confirm its published hours and the arrival instructions attached to your table. Avoid building the plan around a generic opening time that may not apply to your date.</p>'),
            ('Your table proposal', 'Understand the bottle-service allowance.',
             '<p>Ushuaïa describes its VIP table offer as including admission and bottle service up to the reserved value. Food is outside the minimum spend, and unused credit does not carry to another event.</p>'
             '<p>Ask for your proposed table capacity, position, included guests and full payment terms. Have transport, food requests and any other extras listed separately, so the total budget is clear before confirming.</p>'),
            ('Arrival & onward plans', 'Agree the handover before the music starts.',
             '<p>The official VIP entrance is on the beach side of Ushuaïa. Confirm the approach and meeting point in your booking instructions and give the driver the same information.</p>'
             '<p>Decide whether the group returns to the villa, goes to dinner or continues to another club. If Hï is next, it needs its own admission arrangement. Split the guest count by onward destination rather than assuming everyone follows the same plan.</p>'),
        ),
        'brief': 'Ushuaïa event date; total guests; table preferences and budget; earlier yacht, lunch or arrival plans; accommodation area; and dinner, Hï or return transport afterwards.',
        'faqs': (
            ('Should I request an Ushuaïa table before planning the yacht day?', 'Coordinate both together. Share the proposed sailing return, accommodation stop and event date so the arrival plan can be checked before either schedule becomes fixed.'),
            ('Is food included in the Ushuaïa table minimum spend?', 'The venue lists food outside the minimum spend. Ask for any dining or food requirements to be itemised separately in the proposal for your event.'),
            ('Can part of the group continue to Hï afterwards?', 'Yes, that can be included in the planning brief. Give us the separate guest counts and transport needs; Hï access must be requested and confirmed separately.'),
        ),
        'source': 'https://www.theushuaiaexperience.com/club/en/faq',
        'source_label': 'Ushuaïa official event and VIP FAQ',
    },
)


def route(club: dict) -> str:
    return '/' + club['slug'] + '/'


def page(path: str) -> Path:
    return ROOT / path.strip('/') / 'index.html'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError('Club guides: ' + message)


def whatsapp(club: dict) -> str:
    return 'https://wa.me/34600703303?' + urlencode({'text': (
        f"Hello Ibiza VIP Move, I would like to request a VIP table at {club['name']}. "
        'Event date: __. Guests: __. Table preferences or budget: __. '
        'Accommodation area and transport plans: __.'
    )})


def main_html(club: dict) -> str:
    wa = escape(whatsapp(club), quote=True)
    sections = ''.join(
        f'<section class="editorial"><div><div class="kicker dark">{escape(kicker)}</div>'
        f'<h2>{escape(heading)}</h2></div><div>{body}</div></section>'
        for kicker, heading, body in club['sections']
    )
    faqs = ''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in club['faqs'])
    others = ' · '.join(f'<a class="text-link" href="{route(other)}">{escape(other["name"])} table planning</a>' for other in CLUBS if other != club)
    return f'''<main id="main-content" class="ivm-club-guide">
<section class="page-hero" style="--hero:url('{IMAGE}')">
 <div class="page-hero-media"><img src="{IMAGE}" alt="{IMAGE_ALT}" width="1200" height="630" fetchpriority="high" decoding="async"></div>
 <div><div class="kicker light">Ibiza VIP Move · Independent concierge</div>
 <h1>{escape(club['name'])} VIP tables.</h1><p>{escape(club['intro'])}</p>
 <a class="btn gold" data-ivm190="brief" href="{wa}">Request {escape(club['name'])} availability</a>
 <div class="ivm-inner-rail">
 <article><span>Location</span><strong>{escape(club['area'])}</strong><small>{escape(club['format'])}</small></article>
 <article><span>Your brief</span><strong>One evening, coordinated</strong><small>{escape(club['focus'])}</small></article>
 <article><span>Confirmation</span><strong>Written terms first</strong><small>Review the available option before committing.</small></article>
 </div></div>
</section>
<nav class="ivm-club-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><a href="{HUB}">VIP tables in Ibiza</a><span aria-hidden="true"> / </span><span aria-current="page">{escape(club['name'])}</span></nav>
<section class="editorial service-detail"><div><div class="kicker dark">Your night in Ibiza</div><h2>{escape(club['heading'])}</h2></div><div><p class="large">{escape(club['answer'])}</p></div></section>
{sections}
<section class="dark-panel"><div class="kicker light">A useful first message</div><h2>Send the details that shape your night.</h2><p>{escape(club['brief'])}</p><p>If an assistant or travel advisor is arranging the evening, include who approves the proposal and who receives the final itinerary.</p><a class="btn gold" data-ivm190="brief" href="{wa}">Discuss your {escape(club['name'])} plans</a></section>
<section class="editorial"><div><div class="kicker dark">From request to confirmation</div><h2>Know what is agreed.</h2></div><div><p>We check the request for your date, share the proposed table and clarify the spend, inclusions, deposit, cancellation conditions and arrival instructions. A request becomes a booking only after the venue accepts it and its confirmation requirements are met.</p><p>Ibiza VIP Move is an independent concierge, not affiliated with or endorsed by {escape(club['name'])}. Venue availability and entry remain subject to the venue's confirmation and policies.</p><p>Venue information checked on 31 October 2026: <a class="text-link" href="{club['source']}">{escape(club['source_label'])}</a>. Review the current event details, age, ID and dress requirements before visiting.</p></div></section>
<section class="faq"><div class="section-head"><div class="kicker dark">Planning questions</div><h2>{escape(club['name'])}: before you request.</h2></div>{faqs}</section>
<section class="partners-strip"><div><div class="kicker dark">The rest of your stay</div><h2>Connect the plans around your table.</h2><p>Coordinate <a class="text-link" href="/private-chauffeur-ibiza/">private chauffeur transport</a>, <a class="text-link" href="{ACCESS}">restaurant reservations</a> or a <a class="text-link" href="/yacht-charter-ibiza/">yacht day</a> with the evening.</p><p>Comparing venues? {others}. Explore <a class="text-link" href="{HUB}">VIP tables and club access in Ibiza</a> for the wider options.</p></div></section>
<section class="closing-simple"><h2>Your {escape(club['name'])} night starts here.</h2><p>Share your date, guest count and the plans around the event.</p><a class="btn dark" data-ivm190="brief" href="{wa}">Request availability on WhatsApp</a></section>
</main>'''


STYLE = '''<style data-ivm190="club-layout">
.ivm-club-breadcrumb{padding:22px 7vw;display:flex;align-items:center;flex-wrap:wrap;gap:10px;font-size:13px}
.ivm-club-breadcrumb a{display:inline-flex;align-items:center;min-height:44px;text-decoration:underline;text-underline-offset:4px}
.ivm-club-guide .dark-panel>p{max-width:760px;margin:20px 0;line-height:1.8}
.ivm-club-guide .editorial p+p,.ivm-club-guide .partners-strip p+p{margin-top:20px}
.ivm-club-guide .page-hero h1{max-width:20ch}
.ivm-club-guide a:focus-visible{outline:2px solid currentColor;outline-offset:5px}
@media(max-width:600px){.ivm-club-guide .btn{white-space:normal;text-align:center;max-width:100%}}
</style>'''


def render(template: str, club: dict) -> str:
    canonical = BASE + route(club)
    html = set_title(template, club['title'])
    for attr, name, value in (
        ('name', 'description', club['description']),
        ('property', 'og:title', club['title']), ('name', 'twitter:title', club['title']),
        ('property', 'og:description', club['description']), ('name', 'twitter:description', club['description']),
        ('property', 'og:url', canonical),
    ):
        html = set_meta(html, attr, name, value)
    html, n = re.subn(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', f'<link rel="canonical" href="{canonical}">', html)
    require(n == 1, 'one template canonical required')
    html = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>', '', html)
    html = SCRIPT_RE.sub('', html)
    nodes = json_nodes(template)
    organization = node_by_id(nodes, BASE + '/#organization', 'Organization')
    website = node_by_id(nodes, BASE + '/#website', 'WebSite')
    require(organization is not None and website is not None, 'canonical identity nodes missing')
    webpage = {'@context': 'https://schema.org', '@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': club['title'], 'description': club['description'], 'inLanguage': 'en', 'dateModified': DATE, 'isPartOf': {'@id': BASE + '/#website'}, 'publisher': {'@id': BASE + '/#organization'}, 'about': {'@id': canonical + '#service'}}
    service = {'@context': 'https://schema.org', '@type': 'Service', '@id': canonical + '#service', 'url': canonical, 'name': club['name'] + ' VIP table concierge', 'serviceType': 'Independent VIP table request and evening coordination', 'description': club['answer'], 'provider': {'@id': BASE + '/#organization'}, 'areaServed': {'@type': 'Place', 'name': 'Ibiza, Spain'}}
    breadcrumb = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': name, 'item': BASE + path} for i, (name, path) in enumerate((('Home', '/'), ('VIP tables in Ibiza', HUB), (club['name'], route(club))), 1)]}
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': canonical + '#faq', 'inLanguage': 'en', 'isPartOf': {'@id': canonical + '#webpage'}, 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in club['faqs']]}
    head = ''.join(schema_script(deepcopy(node)) for node in (organization, website, webpage, service, breadcrumb, faq))
    head += f'<link rel="alternate" hreflang="en" href="{canonical}"><link rel="alternate" hreflang="x-default" href="{canonical}">' + STYLE
    html = html.replace('</head>', head + '</head>', 1)
    html, n = re.subn(r'<main\b[^>]*>.*?</main>', lambda _: main_html(club), html, flags=re.S)
    require(n == 1, 'one template main required')
    nav = f'<nav class="ivm-language-links" aria-label="Choose language"><a href="{canonical}" hreflang="en" lang="en" aria-current="page" style="min-width:24px;min-height:44px;display:inline-flex;align-items:center;justify-content:center"><b>EN</b><small>English</small></a></nav>'
    html, n = re.subn(r'<nav\b[^>]*class="ivm-language-links"[^>]*>.*?</nav>', lambda _: nav, html, flags=re.S)
    require(n == 1, 'one template language selector required')
    return html


def update_discovery() -> None:
    hub = page(HUB)
    html = hub.read_text(encoding='utf-8')
    for club in CLUBS:
        old = f'<td>{escape(club["name"])}</td>'
        new = f'<td><a class="text-link" data-ivm190="venue-link" href="{route(club)}">{escape(club["name"])}</a></td>'
        require(html.count(old) + html.count(new) == 1, 'venue table insertion point changed: ' + club['name'])
        html = html.replace(old, new, 1)
    # The hub's visible and structured freshness follow the new venue links.
    html = html.replace('Last updated: 21 October 2026', 'Last updated: 31 October 2026')
    html = html.replace('"dateModified":"2026-10-21"', f'"dateModified":"{DATE}"')
    hub.write_text(html, encoding='utf-8')
    target = page(ACCESS)
    html = target.read_text(encoding='utf-8')
    marker = 'data-ivm190="venue-guides"'
    if marker not in html:
        anchor = '<a class="text-link" data-ivm180="vip-tables-link" href="/vip-tables-club-access-ibiza/">VIP Tables &amp; Club Access Ibiza</a>.</p>'
        require(html.count(anchor) == 1, 'nightlife insertion point changed')
        links = ', '.join(f'<a class="text-link" href="{route(club)}">{escape(club["name"])}</a>' for club in CLUBS)
        html = html.replace(anchor, anchor + f'<p {marker}>Planning a specific night? Explore our table and arrival guides for {links}.</p>', 1)
        target.write_text(html, encoding='utf-8')

    ET.register_namespace('', SM)
    ET.register_namespace('image', IM)
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    root = sitemap.getroot()
    for path in [HUB, ACCESS] + [route(club) for club in CLUBS]:
        canonical = BASE + path
        matches = [node for node in root.findall(f'{{{SM}}}url') if node.findtext(f'{{{SM}}}loc') == canonical]
        require(len(matches) <= 1, 'duplicate sitemap entry: ' + canonical)
        if matches:
            node = matches[0]
        else:
            require(path not in (HUB, ACCESS), 'existing discovery page missing from sitemap')
            node = ET.SubElement(root, f'{{{SM}}}url')
            ET.SubElement(node, f'{{{SM}}}loc').text = canonical
        lastmod = node.find(f'{{{SM}}}lastmod')
        if lastmod is None:
            lastmod = ET.SubElement(node, f'{{{SM}}}lastmod')
        lastmod.text = DATE
    sitemap.write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    image_sitemap = ET.parse(ROOT / 'image-sitemap.xml')
    root = image_sitemap.getroot()
    for club in CLUBS:
        canonical = BASE + route(club)
        matches = [node for node in root.findall(f'{{{SM}}}url') if node.findtext(f'{{{SM}}}loc') == canonical]
        require(len(matches) <= 1, 'duplicate image sitemap entry')
        if not matches:
            node = ET.SubElement(root, f'{{{SM}}}url')
            ET.SubElement(node, f'{{{SM}}}loc').text = canonical
            image = ET.SubElement(node, f'{{{IM}}}image')
            ET.SubElement(image, f'{{{IM}}}loc').text = BASE + IMAGE
    image_sitemap.write(ROOT / 'image-sitemap.xml', encoding='utf-8', xml_declaration=True)


def enhance() -> None:
    template = page(HUB).read_text(encoding='utf-8')
    require((ROOT / IMAGE.lstrip('/')).is_file(), 'approved editorial image missing')
    require('data-ivm190="club-layout"' not in template, 'template must be the general VIP page')
    for club in CLUBS:
        target = page(route(club))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(template, club), encoding='utf-8')
    update_discovery()
    print('PASS: Phase 190 — Pacha, Hï and Ushuaïa planning pages, contextual links and sitemaps generated')


if __name__ == '__main__':
    enhance()
