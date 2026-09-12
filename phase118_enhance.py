"""Add accessible international country-code guidance to all concierge phone fields."""
from html import escape
from pathlib import Path
import re

ROOT = Path('_site')
CONTACTS = {
    'contact/index.html': 'Include the international country code so we can identify your number correctly (for example +44 or +971).',
    'es/contacto/index.html': 'Incluye el prefijo internacional para que podamos identificar correctamente tu número (por ejemplo +34 o +44).',
    'fr/contact/index.html': 'Indiquez l’indicatif international pour que nous puissions identifier correctement votre numéro (par exemple +33 ou +44).',
    'de/kontakt/index.html': 'Bitte geben Sie die internationale Landesvorwahl an, damit wir Ihre Nummer eindeutig erkennen können (z. B. +49 oder +44).',
    'ar/contact/index.html': 'أضف رمز الدولة الدولي حتى نتمكن من تحديد رقمك بشكل صحيح (مثلاً +971 أو +966).',
}
PHONE_TAG_RE = re.compile(r'<input\b[^>]*\bid="fPhone"[^>]*>', re.I)


def enhance():
    pending = {}
    for rel, hint in CONTACTS.items():
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 118 contact page missing: {rel}')
        html = path.read_text(encoding='utf-8')
        if 'id="fPhoneHint"' in html or 'aria-describedby="fPhoneHint"' in html:
            raise SystemExit(f'Phase 118 phone guidance already present: {rel}')
        matches = PHONE_TAG_RE.findall(html)
        if len(matches) != 1:
            raise SystemExit(f'Phase 118 expected one phone input: {rel} -> {len(matches)}')
        tag = matches[0]
        required = 'required' in tag.lower()
        semantics = all(token in tag.lower() for token in ('type="tel"', 'inputmode="tel"', 'autocomplete="tel"'))
        if not required or not semantics:
            raise SystemExit(f'Phase 118 phone semantics drift before hint: {rel} -> {tag}')
        if re.search(r'\bpattern\s*=', tag, re.I):
            raise SystemExit(f'Phase 118 refuses country-specific phone pattern: {rel}')
        new_tag = tag[:-1] + ' aria-describedby="fPhoneHint">'
        helper = '<small id="fPhoneHint">' + escape(hint) + '</small>'
        pending[path] = html.replace(tag, new_tag + helper, 1)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print('PASS: Phase 118 — five required tel fields now provide accessible international country-code guidance without enforcing a country-specific pattern')


if __name__ == '__main__':
    enhance()
