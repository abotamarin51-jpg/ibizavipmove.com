"""Tightly scoped, owner-approved English SEO copy for three existing pages.

Run after phase192 within phase178_enhance.py. Keep the branded design, H1,
URLs, booking flows, existing FAQs, structured data and consent unchanged.
The Home introductory lead is set by HOME_NEW_LEAD in phase178_enhance.py.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import re

HOME_DMC_OLD = "<p class=\"ivm-home-authority-pathways\"><a class=\"text-link\" href=\"/private-concierge-ibiza/\">Explore Private Concierge Ibiza →</a> · <a class=\"text-link\" href=\"/international-clients/\">International private client support →</a></p>"
HOME_DMC_NEW = "<p class=\"ivm-home-authority-pathways\"><a class=\"text-link\" href=\"/private-concierge-ibiza/\">Explore Private Concierge Ibiza →</a> · <a class=\"text-link\" href=\"/international-clients/\">International private client support →</a> · <a class=\"text-link\" href=\"/destination-management-ibiza/\">Ibiza destination management for travel advisors →</a></p>"
DMC_URL = '/destination-management-ibiza/'

HOME_LEAD = ('<p class="ivm-seo-lead">Ibiza VIP Move provides luxury and VIP '
             'concierge services in Ibiza for private clients, personal assistants, '
             'family offices and luxury travel advisors through one discreet '
             'local point of contact.</p>')
VIP_OLD_SUMMARY = ('VIP services in Ibiza combining private transport, dining and '
                   'nightlife coordination, yachts, villas, security, hospitality '
                   'support and bespoke requests through one private contact.')
VIP_NEW_SUMMARY = ('VIP services in Ibiza for private clients: chauffeur transport, '
                   'dining, nightlife, yachts, villas and security, coordinated '
                   'through one discreet contact.')

# Exact reviewed source phrases: never replace unknown sections or general keywords.
CHANGES = {
    'index.html': (
        (HOME_DMC_OLD, HOME_DMC_NEW, 1),
        ('<p>From airport to villa, marina to dinner, security to last-minute changes, '
         'Ibiza VIP Move keeps confirmed services connected through one clear line of communication.</p>',
         '<p>From airport arrivals and chauffeur transport to villas, yachts, dining, '
         'private aviation and security, our Ibiza team keeps confirmed arrangements '
         'connected through one clear line of communication.</p>', 1),
    ),
    'vip-services-ibiza/index.html': (
        (VIP_OLD_SUMMARY, VIP_NEW_SUMMARY, 6),
        ('<p class="large">VIP services can involve far more than a table or a car. '
         'The quality of the experience depends on how transport, reservations, '
         'guest timing, security, accommodation and changing plans work together.</p>',
         '<p class="large">More than a single table or transfer, private hospitality '
         'in Ibiza depends on how transport, reservations, guest timing, security '
         'and accommodation work together.</p>', 1),
        ('<p>Ibiza VIP Move coordinates confirmed private services through one contact '
         'and keeps the practical handovers aligned. Venue access, tables and special '
         'requests always remain subject to actual availability and written confirmation.</p>',
         '<p>We coordinate these requests for private clients, personal assistants, '
         'family offices and luxury travel advisors through one discreet local contact. '
         'Venue access, VIP tables and special requests remain subject to '
         'availability and written confirmation.</p>', 1),
    ),
    'private-concierge-ibiza/index.html': (
        ('<p class="large">Ibiza VIP Move is a private concierge for clients who do '
         'not want to manage separate suppliers throughout their stay. We centralise '
         'communication, align timing and keep the confirmed itinerary moving.</p>',
         '<p class="large">Ibiza VIP Move provides private concierge services in Ibiza '
         'for private clients, families, personal assistants, family offices and luxury '
         'travel advisors who prefer one discreet local contact. We align timings, '
         'supplier communication and confirmed arrangements.</p>', 1),
        ('<p>From a restaurant reservation or airport movement to a complex family, '
         'executive or multi-day stay, the service scales around the brief.</p>',
         '<p>From an airport arrival or dining reservation to a multi-day private stay, '
         'we coordinate the agreed services around one clear brief and confirmed timings.</p>', 1),
    ),
}

CANONICALS = {
    'index.html': ('https://ibizavipmove.com/',
                   '<h1>Luxury concierge in Ibiza,<br>handled privately.</h1>'),
    'vip-services-ibiza/index.html': (
        'https://ibizavipmove.com/vip-services-ibiza/',
        '<h1>VIP services in Ibiza,<br><em>without fragmented planning.</em></h1>'),
    'private-concierge-ibiza/index.html': (
        'https://ibizavipmove.com/private-concierge-ibiza/',
        '<h1>Private concierge in Ibiza,<br><em>managed as one.</em></h1>'),
}


class Anchors(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.hrefs = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.hrefs.append(dict(attrs).get('href'))


def require(test, reason):
    if not test:
        raise SystemExit('Phase 193 SEO copy: ' + reason)


def inspect(relative, before, after):
    url, h1 = CANONICALS[relative]
    for html in (before, after):
        require(html.count('<link rel="canonical" href="' + url + '">') == 1,
                relative + ': self canonical')
        require(html.count(h1) == 1 and html.count('<h1') == 1,
                relative + ': branded heading')
        require('<html lang="en"' in html and 'name="robots" content="index,follow' in html,
                relative + ': language/indexability')
        for token in ('https://wa.me/34600703303', 'tel:+34600703303',
                      'partnership@ibizavipmove.com', '/assets/brand-logo.svg'):
            require(token in html, relative + ': contact or brand missing: ' + token)
    old_links, new_links = Anchors(before).hrefs, Anchors(after).hrefs
    if relative == 'index.html':
        require(new_links.count(DMC_URL) == 1,
                'Home: exactly one destination-management pathway')
        if DMC_URL not in old_links:
            require([link for link in new_links if link != DMC_URL] == old_links,
                    'Home: existing destinations or link order changed')
        else:
            require(old_links.count(DMC_URL) == 1 and new_links == old_links,
                    'Home: rerun changed approved destinations')
    else:
        require(old_links == new_links,
                relative + ': links/destinations changed')
    for token in ('<h2', '<h3', '<img', '<picture', '<form', '<script',
                  '<details', '<summary', 'data-ivm-google-maps-profile'):
        require(before.count(token) == after.count(token), relative + ': structure changed: ' + token)
    if relative != 'vip-services-ibiza/index.html':
        require(before.split('</head>', 1)[0] == after.split('</head>', 1)[0],
                relative + ': unexpected SEO head drift')
    else:
        # Meta, Open Graph, Twitter and existing JSON-LD descriptions stay in sync.
        require(after.count(VIP_NEW_SUMMARY) == 6 and VIP_OLD_SUMMARY not in after,
                'VIP: descriptions not synchronized')
        require(after.split('</head>', 1)[0].replace(VIP_NEW_SUMMARY, VIP_OLD_SUMMARY)
                == before.split('</head>', 1)[0].replace(VIP_NEW_SUMMARY, VIP_OLD_SUMMARY),
                'VIP: other SEO head changes')
        for payload in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', after, re.S):
            json.loads(payload)
    if relative == 'index.html':
        require(after.count(HOME_LEAD) == 1, 'Home: approved introductory lead missing')
        require(after.count(HOME_DMC_NEW) == 1 and HOME_DMC_OLD not in after,
                'Home: destination-management link not in approved pathway')
        target = Path('_site/destination-management-ibiza/index.html')
        require(target.is_file() and
                '<link rel="canonical" href="https://ibizavipmove.com/destination-management-ibiza/">' in
                target.read_text(encoding='utf-8'),
                'Home: verified DMC destination missing')


def enhance(root=Path('_site')):
    """Validate all three pages in memory before writing any; reruns are safe."""
    pending = []
    for relative, changes in CHANGES.items():
        path = root / relative
        require(path.is_file(), relative + ': page missing')
        before = path.read_text(encoding='utf-8')
        after = before
        for old, new, occurrences in changes:
            old_count, new_count = after.count(old), after.count(new)
            if old_count == occurrences and new_count == 0:
                after = after.replace(old, new)
            elif old_count == 0 and new_count == occurrences:
                pass  # already applied exactly once
            else:
                require(False, relative + ': unknown or duplicated source copy')
        inspect(relative, before, after)
        pending.append((path, before, after))
    for path, before, after in pending:
        if before != after:
            path.write_text(after, encoding='utf-8')
    print('PASS: Phase 193 — three approved English pages; design, FAQs, schema, links and contacts preserved')


if __name__ == '__main__':
    enhance()
