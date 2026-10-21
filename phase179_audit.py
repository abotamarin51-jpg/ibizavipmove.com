"""Read-only regression gate for the English Private Office enquiry handoff."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET

from phase179_enhance import BRIEF, CANONICAL, CONTACT, MESSAGE, WA_HREF

ROOT = Path('_site')
PAGE = ROOT / 'private-office' / 'index.html'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
EXPECTED_TITLE = 'Ibiza Concierge for Family Offices & Personal Assistants | Ibiza VIP Move'
EXPECTED_H1 = 'Ibiza concierge support for family offices and personal assistants.'


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 179 audit: ' + message)


def run() -> None:
    html = PAGE.read_text(encoding='utf-8')
    tags = Tags(html).tags
    main_start = html.find('<main')
    main_end = html.find('</main>')
    require(main_start >= 0 and main_end > main_start, 'main landmark missing')
    main = html[main_start:main_end + len('</main>')]

    require(f'<title>{EXPECTED_TITLE}</title>' in html, 'title changed')
    require(f'<h1>{EXPECTED_H1}</h1>' in main, 'H1 changed')
    require(
        [a.get('href') for t, a in tags if t == 'link' and a.get('rel') == 'canonical'] == [CANONICAL],
        'canonical changed',
    )
    require(not any(
        t == 'meta' and a.get('name', '').lower() == 'robots' and 'noindex' in a.get('content', '').lower()
        for t, a in tags
    ), 'page became noindex')
    require(main.count('data-ivm179="office"') == 2, 'contextual WhatsApp CTA count')
    require(main.count('data-ivm179="contact"') == 1, 'form route count')
    require(main.count('data-ivm179="brief"') == 1, 'brief count')
    require(main.count(WA_HREF) == 2, 'WhatsApp href count')
    require(all(term in main for term in (
        'guest count', 'time zone', 'approve requests', 'Identity documents', 'bank details'
    )), 'brief essentials missing')

    office_links = [
        a for t, a in tags
        if t == 'a' and a.get('data-ivm179') == 'office'
    ]
    require(len(office_links) == 2, 'two office links required')
    for anchor in office_links:
        parsed = urlsplit(anchor.get('href', ''))
        require(
            parsed.scheme == 'https' and parsed.netloc == 'wa.me' and parsed.path == '/34600703303',
            'approved WhatsApp identity changed',
        )
        query = parse_qs(parsed.query)
        require(query == {'text': [MESSAGE]}, 'WhatsApp draft changed')

    contact_links = [
        a for t, a in tags
        if t == 'a' and a.get('data-ivm179') == 'contact'
    ]
    require(len(contact_links) == 1 and contact_links[0].get('href') == CONTACT, 'Contact route changed')
    require(contact_links[0].get('style') == 'min-height:24px;display:inline-flex;align-items:center', 'Contact target size safeguard changed')
    contact = ROOT / CONTACT.strip('/') / 'index.html'
    require(contact.is_file(), 'Contact target missing')
    contact_html = contact.read_text(encoding='utf-8')
    require(all(f'id="{field}"' in contact_html for field in (
        'conciergeForm', 'fName', 'fPhone', 'fClientType', 'fService', 'fBrief'
    )), 'existing Contact fields missing')

    for lang in ('fr', 'de', 'ar'):
        localized = (ROOT / lang / 'private-office' / 'index.html').read_text(encoding='utf-8')
        require(localized.count('data-ivm113="office"') == 2, f'{lang} contextual handoff changed')
        require(localized.count('data-ivm113="contact"') == 1, f'{lang} Contact route changed')

    values = {}
    for node in ET.parse(ROOT / 'sitemap.xml').getroot().findall(f'{{{NS}}}url'):
        loc = node.findtext(f'{{{NS}}}loc')
        if loc:
            values[loc.rstrip('/') + '/'] = node.findtext(f'{{{NS}}}lastmod')
    require(len(values) == 156, f'sitemap inventory drift: {len(values)}')
    require(values.get(CANONICAL) == '2026-10-21', 'Private Office lastmod is not the verified change date')

    print('PASS: Phase 179 audit — English Private Office handoff, privacy guidance, Contact route, localized isolation and truthful lastmod')


if __name__ == '__main__':
    run()
