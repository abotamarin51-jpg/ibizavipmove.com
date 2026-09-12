"""Regression gate: contact pages must not imply an unauthorized membership product."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LABELS = {
    '/contact/': 'Private Client Desk · Ibiza',
    '/es/contacto/': 'Atención a clientes privados · Ibiza',
    '/fr/contact/': 'Service clients privés · Ibiza',
    '/de/kontakt/': 'Betreuung für Privatkunden · Ibiza',
    '/ar/contact/': 'خدمة العملاء الخاصين · إيبيزا',
}


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 122 audit: ' + msg)


def run():
    for route, label in LABELS.items():
        path = ROOT / route.strip('/') / 'index.html'
        require(path.is_file(), f'missing {route}')
        html = path.read_text(encoding='utf-8')
        tags = Page(html).tags
        require(html.count(label) == 1, f'localized desk label {route}')
        require('Private Members Desk' not in html, f'legacy membership wording {route}')
        require(sum(tag == 'h1' for tag, attrs in tags) == 1, f'one H1 {route}')
        require(any(tag == 'main' and attrs.get('id') == 'main-content' for tag, attrs in tags), f'main landmark {route}')
        require('ivm-skip-link' in html, f'skip link {route}')
        canonical = [attrs.get('href') for tag, attrs in tags if tag == 'link' and attrs.get('rel') == 'canonical']
        require(canonical == [BASE + route], f'canonical {route} -> {canonical}')
        css = [attrs.get('href') for tag, attrs in tags if tag == 'link' and attrs.get('rel') == 'stylesheet' and attrs.get('href', '').startswith('/assets/')]
        require(len(css) == 1 and css[0].startswith('/assets/bundles/'), f'one CSS bundle {route}')
        require((ROOT / urlparse(css[0]).path.lstrip('/')).is_file(), f'CSS exists {route}')
        for field in ('fName', 'fPhone', 'fClientType', 'fService'):
            require(any(attrs.get('id') == field for tag, attrs in tags), f'form field {field} {route}')
        require('https://wa.me/34600703303' in html, f'WhatsApp continuity {route}')
    all_html = '\n'.join(p.read_text(encoding='utf-8') for p in ROOT.rglob('*.html'))
    require('Private Members Desk' not in all_html, 'legacy membership wording remains elsewhere in generated HTML')
    print('PASS: Phase 122 audit — five localized Private Client Desk labels, no membership-product implication, canonicals/forms/accessibility/WhatsApp and one CSS bundle preserved')


if __name__ == '__main__':
    run()
