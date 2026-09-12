"""Require an explicit buyer-role choice on all five concierge contact forms."""
from html import escape
from pathlib import Path
import re

ROOT = Path('_site')
CONTACTS = {
    'contact/index.html': 'Select your profile',
    'es/contacto/index.html': 'Selecciona tu perfil',
    'fr/contact/index.html': 'Sélectionnez votre profil',
    'de/kontakt/index.html': 'Profil auswählen',
    'ar/contact/index.html': 'اختر صفتك',
}
SELECT_RE = re.compile(r'(<select\b[^>]*\bid="fClientType"[^>]*>)(.*?)(</select>)', re.I | re.S)
EMPTY_OPTION_RE = re.compile(r'<option\b[^>]*\bvalue=["\']["\'][^>]*>', re.I)


def enhance():
    pending = {}
    for rel, placeholder in CONTACTS.items():
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 116 contact page missing: {rel}')
        html = path.read_text(encoding='utf-8')
        matches = list(SELECT_RE.finditer(html))
        if len(matches) != 1:
            raise SystemExit(f'Phase 116 expected one fClientType select: {rel} -> {len(matches)}')
        m = matches[0]
        opening, options, closing = m.groups()
        if not re.search(r'\brequired\b', opening, re.I):
            raise SystemExit(f'Phase 116 role select lost required: {rel}')
        if EMPTY_OPTION_RE.search(options):
            raise SystemExit(f'Phase 116 empty placeholder already exists: {rel}')
        role_values = re.findall(r'<option\b[^>]*\bvalue=["\']([^"\']*)["\']', options, re.I)
        expected = ['private_client','assistant','family_office','travel_advisor','hospitality_partner','other']
        if role_values != expected:
            raise SystemExit(f'Phase 116 role inventory drift: {rel} -> {role_values}')
        option = '<option value="" selected disabled>' + escape(placeholder) + '</option>'
        replacement = opening + option + options + closing
        pending[path] = html[:m.start()] + replacement + html[m.end():]

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print('PASS: Phase 116 — five required buyer-role selects now start with a localized empty placeholder so a real profile choice is required')


if __name__ == '__main__':
    enhance()
