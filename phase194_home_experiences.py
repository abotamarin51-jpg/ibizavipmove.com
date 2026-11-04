"""Integrate the owner's English Home experiences without replacing the site shell."""
from collections import Counter
import hashlib
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
SOURCE = Path(__file__).resolve().parent
BASE = 'https://ibizavipmove.com'
MARKER = 'data-ivm194="experiences"'
OLD_H1 = '<h1>Luxury concierge in Ibiza,<br>handled privately.</h1>'
NEW_H1 = '<h1>Luxury concierge in Ibiza,<br>personally arranged.</h1>'
SERVICES = {
    'move': '/private-chauffeur-ibiza/', 'stay': '/luxury-villas-ibiza/',
    'sea': '/yacht-charter-ibiza/', 'access': '/restaurants-nightlife-ibiza/',
    'fly': '/private-aviation-ibiza/', 'protect': '/private-security-ibiza/',
}
CARDS = (
    ('villa', '01 / THE PRIVATE VILLA', 'Stay · Move · Private support',
     'Luxury villa<br>in Ibiza', '/luxury-villas-ibiza/',
     'A private villa, with a chauffeur, chef and arrival details arranged around your preferences.',
     ('Villa search and arrival preparation', 'Private chauffeur arrangements', 'Private chef on request'),
     'Plan my villa', 'villas', 'A luxury villa with a private pool in Ibiza'),
    ('yacht', '02 / THE YACHT DAY', 'Sea · Formentera · Private transfers',
     'Formentera,<br>for the day', '/yacht-charter-ibiza/',
     'A yacht day between Ibiza and Formentera, with marina transfers and lunch plans connected around your group.',
     ('Yacht options for your group', 'Transfers to and from the marina', 'Lunch and onboard requests'),
     'Plan my yacht day', 'yacht', 'An illustrative private yacht on Mediterranean water'),
    ('nightlife', '03 / NIGHTLIFE IBIZA', 'Access · Dining · Chauffeur',
     'Nightlife<br>Ibiza', '/restaurants-nightlife-ibiza/',
     'A luxury restaurant, a VIP table and a private chauffeur, arranged around your evening.',
     ('Luxury restaurant reservations', 'VIP table options and terms', 'Private chauffeur and return transfer'),
     'Plan my Ibiza night', 'access', 'Guests and table service at Lío Ibiza'),
)


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags = []; self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, reason):
    if not ok:
        raise SystemExit('Home experiences: ' + reason)


def asset_inputs():
    folder = SOURCE / 'editorial-assets/home-experiences'
    manifest = json.loads((folder / 'manifest.json').read_text())
    require(manifest.get('version') == 1, 'unknown asset manifest')
    expected = {f'experience-{name}-{width}.{ext}' for name, *_ in CARDS
                for width in (480, 960) for ext in ('webp', 'jpg')}
    require(set(manifest['assets']) == expected, 'changed image inventory')
    result = {}
    for name, record in manifest['assets'].items():
        data = (folder / name).read_bytes()
        require(len(data) == record['bytes'] and
                hashlib.sha256(data).hexdigest() == record['sha256'],
                'unreviewed image bytes: ' + name)
        require(0 < len(data) <= 230000, 'image exceeds card budget: ' + name)
        require(record['width'] in (480, 960), 'unexpected card resolution')
        result[name] = data
    return manifest, result


def experiences(manifest):
    cards = []
    for name, number, category, heading, href, summary, items, label, service, alt in CARDS:
        prefix = '/assets/images/experience-' + name
        height = manifest['assets'][f'experience-{name}-960.jpg']['height']
        picture = (
            f'<picture><source type="image/webp" srcset="{prefix}-480.webp 480w, {prefix}-960.webp 960w" '
            'sizes="(max-width:700px) calc(100vw - 40px), (max-width:1000px) 30vw, 380px">'
            f'<img src="{prefix}-960.jpg" srcset="{prefix}-480.jpg 480w, {prefix}-960.jpg 960w" '
            'sizes="(max-width:700px) calc(100vw - 40px), (max-width:1000px) 30vw, 380px" '
            f'alt="{escape(alt, quote=True)}" width="960" height="{height}" loading="lazy" decoding="async"></picture>'
        )
        bullets = ''.join('<li>' + escape(item) + '</li>' for item in items)
        extra = ('<a href="/vip-tables-club-access-ibiza/">Explore VIP tables</a>' if name == 'nightlife'
                 else '<a href="/private-chef-staffing-ibiza/">Explore private chefs and villa staffing</a>'
                 if name == 'villa' else '<a href="/private-chauffeur-ibiza/">Explore marina transfers</a>')
        cards.append(
            f'<article class="ivm-exp-card" data-experience="{name}">'
            f'<div class="ivm-exp-visual">{picture}<span class="ivm-exp-index">{number}</span></div>'
            f'<div class="ivm-exp-copy"><p class="ivm-exp-category">{category}</p>'
            f'<h3><a href="{href}">{heading}</a></h3><p class="ivm-exp-summary">{summary}</p>'
            f'<ul>{bullets}</ul><p class="ivm-exp-related">{extra}</p>'
            f'<a class="ivm-exp-plan" href="/contact/?service={service}">{label}'
            '<span aria-hidden="true">↗</span></a></div></article>'
        )
    return (
        f'<section id="experiences" class="ivm-home-experiences" {MARKER} aria-labelledby="experiences-title">'
        '<div class="ivm-exp-inner"><div class="ivm-exp-intro"><div>'
        '<p class="ivm-exp-eyebrow">Three ways to begin</p>'
        '<h2 id="experiences-title">Your stay. Your pace.</h2></div>'
        '<p>Start with what you have in mind. We shape the proposal around your dates, guests and preferences.</p>'
        '</div><div class="ivm-exp-grid">' + ''.join(cards) + '</div>'
        '<p class="ivm-exp-availability">Illustrative experiences. Each proposal is tailored to your dates. '
        'Services, availability, inclusions and terms are confirmed before booking.</p></div></section>'
    )


CASE = '''<section class="ivm-home-case" aria-labelledby="home-case-title"><div class="ivm-case-inner">
<div><p class="ivm-exp-eyebrow">From a published Ibiza VIP Move brief</p><h2 id="home-case-title">A weekend,<br>thoughtfully connected.</h2>
<p>Airport transfers, beach time, dinner, wellness and private transport for two guests. See how the arrangements came together around one itinerary.</p>
<a class="ivm-case-link" href="/case-studies/weekend-concierge-two-guests/">Read the anonymized case study <span aria-hidden="true">↗</span></a></div>
<div class="ivm-case-steps"><div><p class="ivm-exp-eyebrow">Arrival</p><h3>A clear starting point.</h3><p>Airport movements connected with the wider weekend plan.</p></div>
<div><p class="ivm-exp-eyebrow">During the stay</p><h3>Each part in its place.</h3><p>Beach time, wellness and evening reservations planned together.</p></div>
<div><p class="ivm-exp-eyebrow">The return</p><h3>The evening, completed.</h3><p>Private transport planned around the late return as well as the arrival.</p></div>
<p class="ivm-case-private">Client identities, precise dates and private booking details remain confidential.</p></div></div></section>'''


def audit(root=ROOT):
    manifest, assets = asset_inputs()
    html = (root / 'index.html').read_text()
    tags = Tags(html).tags
    require(html.count(MARKER) == 1 and html.count(NEW_H1) == 1 and html.count('<h1') == 1,
            'missing or duplicated experiences/heading')
    require(OLD_H1 not in html and 'data:image/' not in html and 'Visual draft' not in html,
            'prototype content leaked into production')
    require('<link rel="canonical" href="https://ibizavipmove.com/">' in html and
            'name="robots" content="index,follow' in html, 'Home indexability drift')
    require(html.count('IBIZA · PRIVATE CLIENTS &amp; TRAVEL PROFESSIONALS') == 1,
            'approved Ibiza-only tagline missing')
    ids = [a['id'] for t, a in tags if a.get('id')]
    require(len(ids) == len(set(ids)), 'duplicate page ID')
    for identity, href in SERVICES.items():
        require(sum(t == 'a' and a.get('id') == identity and a.get('href') == href
                    for t, a in tags) == 1, 'original service missing: ' + identity)
    require(html.count('class="ivm-exp-card"') == 3, 'expected three experiences')
    for name, *_rest in CARDS:
        require(html.count(f'data-experience="{name}"') == 1, 'card duplicated: ' + name)
    for href in ('/contact/?service=villas', '/contact/?service=yacht', '/contact/?service=access'):
        require(html.count('href="' + href + '"') == 1, 'missing contextual contact: ' + href)
    require('https://wa.me/34600703303' in html and 'tel:+34600703303' in html,
            'approved contact routes missing')
    css = [a['href'] for t, a in tags if t == 'link' and a.get('rel') == 'stylesheet'
           and a.get('href', '').startswith('/assets/')]
    require(len(css) == 1, 'expected one Home CSS bundle')
    require('/* Home experiences 194 */' in (root / css[0].lstrip('/')).read_text(),
            'Home-only stylesheet missing')
    for name, data in assets.items():
        require((root / 'assets/images' / name).read_bytes() == data, 'published image mismatch: ' + name)
    for t, a in tags:
        if t == 'a' and a.get('href', '').startswith('/'):
            path = a['href'].split('?', 1)[0].split('#', 1)[0]
            if path.endswith('/'):
                require((root / path.strip('/') / 'index.html').is_file(), 'broken internal link: ' + path)
        if t == 'img' and '/experience-' in a.get('src', ''):
            require(a.get('loading') == 'lazy' and a.get('width') == '960' and a.get('alt'),
                    'card image delivery/accessibility missing')
    sitemap = (root / 'sitemap.xml').read_text()
    require(sitemap.count('<loc>' + BASE + '/</loc><lastmod>2026-11-04</lastmod>') == 1,
            'Home sitemap freshness missing')
    ET.fromstring(sitemap); ET.fromstring((root / 'image-sitemap.xml').read_text())
    print('PASS: Home experiences — three linked requests, six original services, original supplied images, one CSS bundle and SEO/contact integrity')


def enhance(root=ROOT):
    manifest, assets = asset_inputs()
    path = root / 'index.html'; before = path.read_text()
    if MARKER in before:
        audit(root)
        return
    require(before.count(OLD_H1) == 1, 'unexpected source heading')
    rail_match = re.search(r'<div class="ivm-ref-service-rail">.*?</div>', before, re.S)
    require(rail_match is not None, 'original six-service rail missing')
    rail = rail_match.group()
    require(rail.count('class="ivm-ref-service"') == 6, 'unexpected original service count')
    triptych_match = re.search(r'<section class="ivm-ref-triptych">.*?</section>', before, re.S)
    require(triptych_match is not None, 'original Private Office/Black Book pathways missing')
    triptych = triptych_match.group()
    after = before.replace(rail, '', 1).replace(triptych, '', 1).replace(OLD_H1, NEW_H1, 1)
    old_sub = '<p class="ivm-ref-sub">Discretion. Access. Excellence.<br>Your time is our highest standard.</p>'
    new_sub = '<p class="ivm-ref-sub">Private villas, yachts, chauffeurs and VIP reservations. One Ibiza-based contact to arrange the details around your stay.</p>'
    require(after.count(old_sub) == 1, 'unexpected source hero summary')
    after = after.replace(old_sub, new_sub, 1)
    after = after.replace('<div class="kicker light">Luxury Concierge · Ibiza</div>',
                          '<div class="kicker light">Private concierge &amp; VIP services · Ibiza</div>', 1)
    old_actions = '<div class="ivm-ref-actions"><a class="btn gold" href="/contact/">Request Concierge</a><a class="btn ghost" href="https://wa.me/34600703303">WhatsApp 24/7</a></div>'
    require(after.count(old_actions) >= 1, 'source hero actions missing')
    new_actions = '<div class="ivm-ref-actions"><a class="btn gold" href="#experiences">Plan your Ibiza stay</a><a class="btn ghost" href="https://wa.me/34600703303">Speak to concierge</a></div><p class="ivm-home-tagline">IBIZA · PRIVATE CLIENTS &amp; TRAVEL PROFESSIONALS</p>'
    after = after.replace(old_actions, new_actions, 1)
    hero = re.search(r'<section class="ivm-ref-hero">.*?</section>', after, re.S)
    require(hero is not None, 'hero boundary missing')
    services = '<section class="ivm-home-services" aria-labelledby="home-services-title"><h2 id="home-services-title">Explore our private services</h2>' + rail + '</section>'
    after = after[:hero.end()] + experiences(manifest) + services + after[hero.end():]
    boundary = '<section class="ivm-ref-final">'
    require(after.count(boundary) == 1, 'closing boundary changed')
    after = after.replace(boundary, CASE + triptych + boundary, 1)
    css_pattern = r'<link rel="stylesheet" href="(/assets/bundles/[a-f0-9]+\.css)">'
    old_css = re.findall(css_pattern, before)
    require(len(old_css) == 1, 'unexpected source CSS bundling')
    css_data = (root / old_css[0].lstrip('/')).read_bytes() + b'\n' + (SOURCE / 'phase194_home_experiences.css').read_bytes()
    new_css = '/assets/bundles/' + hashlib.sha256(css_data).hexdigest()[:16] + '.css'
    after = after.replace(old_css[0], new_css, 1)
    require(before.split('</head>', 1)[0].replace(old_css[0], new_css) == after.split('</head>', 1)[0],
            'unexpected metadata, schema, hreflang or tracking change')
    before_scripts = re.findall(r'<script\b.*?</script>', before, re.S)
    require(before_scripts == re.findall(r'<script\b.*?</script>', after, re.S), 'script or consent drift')
    old_links = Counter(a.get('href') for t, a in Tags(before).tags if t == 'a')
    new_links = Counter(a.get('href') for t, a in Tags(after).tags if t == 'a')
    # The reviewed hero action now introduces the three experiences; header,
    # closing and footer retain the existing generic Contact destination.
    old_links.subtract({'/contact/': 1})
    require(not (old_links - new_links), 'existing destination lost')
    sitemap_path = root / 'sitemap.xml'; image_path = root / 'image-sitemap.xml'
    sitemap = sitemap_path.read_text()
    sitemap, count = re.subn(r'(<loc>https://ibizavipmove\.com/</loc><lastmod>)[^<]+(</lastmod>)',
                            r'\g<1>2026-11-04\g<2>', sitemap)
    require(count == 1, 'Home sitemap entry missing or duplicated')
    image_sitemap = image_path.read_text()
    home_images = re.search(r'<url><loc>https://ibizavipmove\.com/</loc>.*?</url>', image_sitemap, re.S)
    require(home_images is not None, 'Home image sitemap entry missing')
    additions = ''.join('<image:image><image:loc>' + BASE + '/assets/images/experience-' + name + '-960.jpg</image:loc></image:image>' for name, *_ in CARDS)
    image_sitemap = image_sitemap.replace(home_images.group(), home_images.group().replace('</url>', additions + '</url>'), 1)
    ET.fromstring(sitemap); ET.fromstring(image_sitemap)
    # Every source and invariant is checked before writing generated output.
    for name, data in assets.items():
        (root / 'assets/images' / name).write_bytes(data)
    (root / new_css.lstrip('/')).write_bytes(css_data)
    path.write_text(after); sitemap_path.write_text(sitemap); image_path.write_text(image_sitemap)
    audit(root)


if __name__ == '__main__':
    enhance()
