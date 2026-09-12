"""Read-only gate for explicit buyer-role selection on the five concierge desks."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path('_site')
CONTACTS = {
    'contact/index.html': 'Select your profile',
    'es/contacto/index.html': 'Selecciona tu perfil',
    'fr/contact/index.html': 'Sélectionnez votre profil',
    'de/kontakt/index.html': 'Profil auswählen',
    'ar/contact/index.html': 'اختر صفتك',
}
EXPECTED = ['private_client','assistant','family_office','travel_advisor','hospitality_partner','other']


class SelectParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.in_target = False
        self.required = False
        self.options = []
        self.current = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'select' and a.get('id') == 'fClientType':
            if self.in_target or self.options:
                raise SystemExit('Phase 116 audit: duplicate fClientType select')
            self.in_target = True
            self.required = 'required' in a
        elif self.in_target and tag == 'option':
            self.current = {
                'value': a.get('value', ''),
                'selected': 'selected' in a,
                'disabled': 'disabled' in a,
                'text': '',
            }
            self.options.append(self.current)

    def handle_data(self, data):
        if self.in_target and self.current is not None:
            self.current['text'] += data

    def handle_endtag(self, tag):
        if self.in_target and tag == 'option':
            self.current = None
        elif self.in_target and tag == 'select':
            self.in_target = False


def run():
    for rel, label in CONTACTS.items():
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 116 audit: missing {rel}')
        parser = SelectParser(path.read_text(encoding='utf-8'))
        if not parser.required:
            raise SystemExit(f'Phase 116 audit: fClientType not required {rel}')
        if len(parser.options) != 7:
            raise SystemExit(f'Phase 116 audit: expected 7 options {rel} -> {len(parser.options)}')
        first = parser.options[0]
        if first['value'] != '' or not first['selected'] or not first['disabled'] or first['text'].strip() != label:
            raise SystemExit(f'Phase 116 audit: invalid placeholder {rel} -> {first}')
        if [o['value'] for o in parser.options[1:]] != EXPECTED:
            raise SystemExit(f'Phase 116 audit: role inventory/order drift {rel}')
        if any(o['selected'] for o in parser.options[1:]):
            raise SystemExit(f'Phase 116 audit: real role preselected {rel}')
    print('PASS: Phase 116 audit — five required role selects start empty with localized disabled placeholders; six buyer-role values preserved and none preselected')


if __name__ == '__main__':
    run()
