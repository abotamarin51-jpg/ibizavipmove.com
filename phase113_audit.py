"""Read-only regression gate for the localized international enquiry journeys."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PATHS = {
    'fr': ('clients-internationaux', '/fr/contact/', '/fr/conciergerie-privee-ibiza/', '/fr/aviation-privee-ibiza/'),
    'de': ('internationale-kunden', '/de/kontakt/', '/de/privater-concierge-ibiza/', '/de/private-aviation-ibiza/'),
    'ar': ('international-clients', '/ar/contact/', '/ar/private-concierge-ibiza/', '/ar/private-aviation-ibiza/'),
}


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 113 audit: ' + message)


def run():
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = {n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)}
    for lang, (slug, contact, concierge, aviation) in PATHS.items():
        for route in (slug, 'private-office'):
            path = f'/{lang}/{route}/'
            html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
            tags = Page(html).tags
            require([a.get('href') for t, a in tags if t == 'link' and a.get('rel') == 'canonical'] == [BASE + path], f'canonical {path}')
            require(BASE + path in urls, f'sitemap {path}')
            require(sum(t == 'h1' for t, a in tags) == 1, f'one H1 {path}')
            require(any(t == 'html' and a.get('lang') == lang and (lang != 'ar' or a.get('dir') == 'rtl') for t, a in tags), f'language/RTL {path}')
            require(any(t == 'main' and a.get('id') == 'main-content' for t, a in tags), f'main {path}')
            require('ivm-skip-link' in html, f'skip link {path}')
            require(not any(t == 'meta' and a.get('name', '').lower() == 'robots' and 'noindex' in a.get('content', '').lower() for t, a in tags), f'noindex {path}')
            css = [a['href'] for t, a in tags if t == 'link' and a.get('rel') == 'stylesheet' and a.get('href', '').startswith('/assets/')]
            require(len(css) == 1 and css[0].startswith('/assets/bundles/'), f'one CSS bundle {path}')
            require((ROOT / urlparse(css[0]).path.lstrip('/')).is_file(), f'CSS exists {path}')
            links = [a for t, a in tags if t == 'a' and a.get('data-ivm113')]
            form = [a for a in links if a['data-ivm113'] == 'contact']
            require(len(form) == 1 and form[0].get('href') == contact, f'contact route {path}')
            for a in links:
                href = a.get('href', '')
                if href.startswith('/'):
                    require(href.startswith(f'/{lang}/'), f'cross-language link {path}')
                    require((ROOT / href.strip('/') / 'index.html').is_file(), f'link target {path} -> {href}')
            # Every language alternate must exist and point back to this page.
            alts = [(a.get('hreflang'), a.get('href')) for t, a in tags if t == 'link' and a.get('rel') == 'alternate' and a.get('hreflang')]
            require({code for code, href in alts} == {'en', 'es', 'fr', 'de', 'ar', 'x-default'} and len(alts) == 6, f'hreflang set {path}')
            for code, href in alts:
                require(urlparse(href).netloc == 'ibizavipmove.com', f'alternate domain {path}')
                other = ROOT / urlparse(href).path.strip('/') / 'index.html'
                require(other.is_file(), f'alternate missing {href}')
                back = Page(other.read_text(encoding='utf-8')).tags
                require(any(t == 'link' and a.get('hreflang') == lang and a.get('href') == BASE + path for t, a in back), f'alternate reciprocity {path}')
            if route == slug:
                expected = Counter({concierge: 1, f'/{lang}/private-office/': 2, f'/{lang}/partners/': 2, aviation: 1})
                actual = Counter(a.get('href') for a in links if a['data-ivm113'] == 'audience')
                require(actual == expected, f'audience routing {path}')
                require('Doha' not in html and 'الدوحة' not in html, f'out-of-scope city list {path}')
            else:
                office = [a for a in links if a['data-ivm113'] == 'office']
                require(len(office) == 2, f'office CTA count {path}')
                for a in office:
                    u = urlparse(a.get('href', ''))
                    require(u.scheme == 'https' and u.netloc == 'wa.me' and u.path == '/34600703303', f'WhatsApp identity {path}')
                    q = parse_qs(u.query)
                    require(set(q) == {'text'} and len(q['text']) == 1 and 'Ibiza VIP Move' in q['text'][0], f'WhatsApp context {path}')
                    require(any(term in q['text'][0] for term in ('représentant', 'Vertreter', 'ممثلاً')), f'representative context {path}')
                require(sum(a.get('data-ivm113') == 'brief' for t, a in tags) == 1, f'brief count {path}')
                require(all(term in html for term in {'fr': ('fuseau horaire', 'valider', 'documents d’identité'), 'de': ('Zeitzone', 'freigeben', 'Ausweisdokumente'), 'ar': ('الزمنية', 'صلاحية', 'الهوية')}[lang]), f'brief essentials {path}')
            contact_html = (ROOT / contact.strip('/') / 'index.html').read_text(encoding='utf-8')
            require(all(f'id="{field}"' in contact_html for field in ('localizedConciergeForm', 'fName', 'fPhone', 'fClientType', 'fService', 'fBrief')), f'existing form fields {contact}')
    print('PASS: Phase 113 audit — six journeys; audience/contact routes, WhatsApp identity/context, approval/timezone brief, reciprocal hreflang, canonicals, sitemap, RTL, H1 and one CSS bundle verified')


if __name__ == '__main__':
    run()
