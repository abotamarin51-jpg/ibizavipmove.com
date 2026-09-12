"""Read-only regression gate for native telephone input semantics."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path('_site')
CONTACTS = [
    ('en', 'contact/index.html', 'conciergeForm'),
    ('es', 'es/contacto/index.html', 'localizedConciergeForm'),
    ('fr', 'fr/contact/index.html', 'localizedConciergeForm'),
    ('de', 'de/kontakt/index.html', 'localizedConciergeForm'),
    ('ar', 'ar/contact/index.html', 'localizedConciergeForm'),
]


class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 115 audit: ' + message)


for lang, rel, form_id in CONTACTS:
    path = ROOT / rel
    require(path.is_file(), f'missing page {rel}')
    html = path.read_text(encoding='utf-8')
    tags = Tags(html).tags
    forms = [a for t, a in tags if t == 'form' and a.get('id') == form_id]
    require(len(forms) == 1, f'form identity {rel}')
    phones = [a for t, a in tags if t == 'input' and a.get('id') == 'fPhone']
    require(len(phones) == 1, f'phone cardinality {rel}')
    phone = phones[0]
    require(phone.get('type') == 'tel', f'type=tel {rel}')
    require(phone.get('inputmode') == 'tel', f'inputmode=tel {rel}')
    require(phone.get('autocomplete') == 'tel', f'autocomplete=tel {rel}')
    require('required' in phone, f'required preserved {rel}')
    require('pattern' not in phone, f'no rigid international pattern {rel}')
    require(any(t == 'html' and a.get('lang', '').split('-')[0] == lang for t, a in tags), f'language preserved {rel}')

print('PASS: Phase 115 audit — EN/ES/FR/DE/AR phone fields use native telephone semantics, preserve autofill/required behavior and do not impose a country-specific number pattern')
