"""Phase 114 regression gate for localized contact-form date validation."""
from pathlib import Path
import re
import subprocess

ROOT = Path('_site')
SOURCE = Path('phase107.js')
ASSET = ROOT / 'assets' / 'phase107.js'

CONTACTS = {
    'en': '/contact/',
    'es': '/es/contacto/',
    'fr': '/fr/contact/',
    'de': '/de/kontakt/',
    'ar': '/ar/contact/',
}
MESSAGES = {
    'en': (
        'Please choose an arrival date that is today or later.',
        'Please choose a departure date that is today or later.',
        'Departure cannot be before arrival.',
    ),
    'es': (
        'Selecciona una fecha de llegada de hoy en adelante.',
        'Selecciona una fecha de salida de hoy en adelante.',
        'La salida no puede ser anterior a la llegada.',
    ),
    'fr': (
        'Choisissez une date d’arrivée à partir d’aujourd’hui.',
        'Choisissez une date de départ à partir d’aujourd’hui.',
        'Le départ ne peut pas précéder l’arrivée.',
    ),
    'de': (
        'Bitte wählen Sie ein Anreisedatum ab heute.',
        'Bitte wählen Sie ein Abreisedatum ab heute.',
        'Die Abreise darf nicht vor der Anreise liegen.',
    ),
    'ar': (
        'يرجى اختيار تاريخ وصول من اليوم فصاعداً.',
        'يرجى اختيار تاريخ مغادرة من اليوم فصاعداً.',
        'لا يمكن أن يكون تاريخ المغادرة قبل تاريخ الوصول.',
    ),
}


def fail(message):
    raise SystemExit('Phase 114 audit: ' + message)


if not SOURCE.is_file() or not ASSET.is_file():
    fail('phase107 source/runtime missing')
source = SOURCE.read_text(encoding='utf-8')
asset = ASSET.read_text(encoding='utf-8')
if source != asset:
    fail('deployed phase107 runtime drifted from source')

syntax = subprocess.run(['node', '--check', str(SOURCE)], capture_output=True, text=True)
if syntax.returncode:
    fail('phase107.js syntax error: ' + (syntax.stderr or syntax.stdout).strip())

required_runtime = (
    "const validateDates=()=>",
    "arrival.min=localToday",
    "departure.min=a||localToday",
    "arrival.setCustomValidity",
    "departure.setCustomValidity",
    "el.addEventListener('input',validateDates)",
    "el.addEventListener('change',validateDates)",
    "validateDates();\n    if(!f.reportValidity())return;",
)
for token in required_runtime:
    if token not in source:
        fail('date-validation runtime missing: ' + token)

for lang, messages in MESSAGES.items():
    for message in messages:
        if source.count(message) != 1:
            fail(f'localized validation message missing/duplicated ({lang}): {message}')

for lang, route in CONTACTS.items():
    page = ROOT / route.strip('/') / 'index.html'
    if not page.is_file():
        fail('contact page missing: ' + route)
    html = page.read_text(encoding='utf-8')
    html_lang = re.search(r'<html\b[^>]*\blang="([^"]+)"', html, re.I)
    if not html_lang or html_lang.group(1).lower().split('-')[0] != lang:
        fail('language mismatch: ' + route)
    if html.count('/assets/phase107.js?v=107') != 1:
        fail('phase107 runtime missing/duplicated: ' + route)
    for field in ('fArrival', 'fDeparture'):
        m = re.search(rf'<input\b[^>]*\bid="{field}"[^>]*>', html, re.I)
        if not m or not re.search(r'\btype="date"', m.group(0), re.I):
            fail(f'{field} is not a date input: {route}')
    if 'data-ivm-qualified-brief="true"' not in html:
        fail('qualified form marker missing: ' + route)

print(
    'PASS: Phase 114 audit — EN/ES/FR/DE/AR contact desks share one syntax-checked '
    'runtime with today-or-later arrival/departure constraints, departure-after-arrival '
    'validation and site-language custom validity messages; no form submission required'
)
