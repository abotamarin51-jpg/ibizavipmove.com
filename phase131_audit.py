"""Audit the Phase 131 contact-form service-selection guardrail."""
from html import unescape
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
EN_SERVICES = ['Full Concierge', 'Destination Management', 'Private Chauffeur & Transportation',
    'Luxury Villas & Private Stays', 'Yachts & Charters', 'Private Aviation',
    'Restaurants, Beach Clubs & Nightlife', 'Security & Close Protection',
    'Private Chefs & Villa Staffing', 'Luxury & Supercar Rental', 'Wellness & Beauty',
    'Private Events & Celebrations', 'Lifestyle & Bespoke Requests']
SELECT_RE = re.compile(r'(<select\b[^>]*\bid="fService"[^>]*>)(.*?)(</select>)', re.I | re.S)
OPTION_RE = re.compile(r'<option\b([^>]*)\bvalue=["\']([^"\']*)["\']([^>]*)>(.*?)</option>', re.I | re.S)

for rel, placeholder in CONTACTS.items():
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'Phase 131 audit missing contact page: {rel}')
    html = path.read_text(encoding='utf-8')
    matches = list(SELECT_RE.finditer(html))
    if len(matches) != 1:
        raise SystemExit(f'Phase 131 audit expected one fService select: {rel} -> {len(matches)}')

    opening, options, _closing = matches[0].groups()
    if not re.search(r'\brequired\b', opening, re.I):
        raise SystemExit(f'Phase 131 audit service select is not required: {rel}')

    parsed = OPTION_RE.findall(options)
    count = 13 if rel == 'contact/index.html' else 12
    if len(parsed) != count + 1:
        raise SystemExit(f'Phase 131 audit expected placeholder + {count} services: {rel} -> {len(parsed)}')

    first = parsed[0]
    attrs = (first[0] + ' ' + first[2]).lower()
    text = re.sub(r'<[^>]+>', '', first[3]).strip()
    if first[1] != '' or 'selected' not in attrs or 'disabled' not in attrs or text != placeholder:
        raise SystemExit(f'Phase 131 audit invalid placeholder: {rel}')

    real_values = [value for _a, value, _b, _text in parsed[1:]]
    if any(not value for value in real_values) or len(set(real_values)) != count:
        raise SystemExit(f'Phase 131 audit service inventory drift: {rel}')
    if rel == 'contact/index.html' and [unescape(value) for value in real_values] != EN_SERVICES:
        raise SystemExit('Phase 131 audit English inventory must preserve the original 12 services plus exactly Destination Management')

print('PASS: Phase 131 audit — five required placeholders; exact English 12-plus-DMC inventory and 12 distinct services in each other language')
