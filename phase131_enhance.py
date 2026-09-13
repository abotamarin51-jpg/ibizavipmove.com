"""Require an explicit primary-service choice on all five concierge contact forms.

The existing forms silently default to the first service option ("Full Concierge"
or its localized equivalent) when a visitor submits without interacting with the
service selector. That can misclassify qualified briefs. This phase keeps the
existing service inventory and adds a localized empty placeholder plus native
HTML required validation.
"""
from html import escape
from pathlib import Path
import re

ROOT = Path('_site')
CONTACTS = {
    'contact/index.html': 'Select primary service',
    'es/contacto/index.html': 'Selecciona el servicio principal',
    'fr/contact/index.html': 'Sélectionnez le service principal',
    'de/kontakt/index.html': 'Hauptservice auswählen',
    'ar/contact/index.html': 'اختر الخدمة الرئيسية',
}
SELECT_RE = re.compile(r'(<select\b[^>]*\bid="fService"[^>]*>)(.*?)(</select>)', re.I | re.S)
OPTION_RE = re.compile(r'<option\b([^>]*)\bvalue=["\']([^"\']*)["\']([^>]*)>(.*?)</option>', re.I | re.S)


def ensure_required(opening: str) -> str:
    if re.search(r'\brequired\b', opening, re.I):
        return opening
    return opening[:-1] + ' required>'


def enhance():
    pending = {}
    for rel, placeholder in CONTACTS.items():
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 131 contact page missing: {rel}')
        html = path.read_text(encoding='utf-8')
        matches = list(SELECT_RE.finditer(html))
        if len(matches) != 1:
            raise SystemExit(f'Phase 131 expected one fService select: {rel} -> {len(matches)}')
        m = matches[0]
        opening, options, closing = m.groups()
        parsed = OPTION_RE.findall(options)

        # Allow an exact already-enhanced state so local validation can be
        # repeated without stacking placeholders.
        if parsed and parsed[0][1] == '':
            if len(parsed) != 13:
                raise SystemExit(f'Phase 131 expected placeholder + 12 services: {rel} -> {len(parsed)}')
            first = parsed[0]
            attrs = (first[0] + ' ' + first[2]).lower()
            text = re.sub(r'<[^>]+>', '', first[3]).strip()
            if not (
                'selected' in attrs
                and 'disabled' in attrs
                and text == placeholder
                and re.search(r'\brequired\b', opening, re.I)
                and all(value for _a, value, _b, _text in parsed[1:])
            ):
                raise SystemExit(f'Phase 131 unexpected enhanced service state: {rel}')
            continue

        if len(parsed) != 12:
            raise SystemExit(f'Phase 131 expected 12 existing service options: {rel} -> {len(parsed)}')
        values = [value for _a, value, _b, _text in parsed]
        if any(not value for value in values) or len(set(values)) != 12:
            raise SystemExit(f'Phase 131 service inventory drift: {rel}')

        # Preserve every existing real service option and make the first state
        # a non-submittable placeholder so native constraint validation can
        # distinguish "not chosen" from a genuine Full Concierge request.
        opening = ensure_required(opening)
        option = '<option value="" selected disabled>' + escape(placeholder) + '</option>'
        replacement = opening + option + options + closing
        pending[path] = html[:m.start()] + replacement + html[m.end():]

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print('PASS: Phase 131 — five contact forms require an explicit localized primary-service choice without changing the service inventory')


if __name__ == '__main__':
    enhance()
