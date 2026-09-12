"""Read-only regression gate for whitespace-safe concierge handover."""
from pathlib import Path
import re
import subprocess

ROOT = Path('_site')
RUNTIME = ROOT / 'assets' / 'phase107.js'
CONTACTS = [
    'contact/index.html',
    'es/contacto/index.html',
    'fr/contact/index.html',
    'de/kontakt/index.html',
    'ar/contact/index.html',
]


def run():
    if not RUNTIME.is_file():
        raise SystemExit('Phase 119 audit runtime missing')
    js = RUNTIME.read_text(encoding='utf-8')
    checks = {
        'trimmed getter': "const g=id=>(document.getElementById(id)?.value||'').trim();" in js,
        'name field validator': "nameField.setCustomValidity(nameField.value&&!nameField.value.trim()?c.nameBlank:'')" in js,
        'phone field validator': "phoneField.setCustomValidity(phoneField.value&&!phoneField.value.trim()?c.phoneBlank:'')" in js,
        'submit validator': "validateDates();\n    validateRequiredText();\n    if(!f.reportValidity())return;" in js,
        'English copy': 'Please enter your name, not only spaces.' in js and 'Please enter your WhatsApp or phone number, not only spaces.' in js,
        'Spanish copy': 'Introduce tu nombre, no solo espacios.' in js and 'Introduce tu WhatsApp o teléfono, no solo espacios.' in js,
        'French copy': 'Saisissez votre nom, pas uniquement des espaces.' in js and 'Saisissez votre WhatsApp ou téléphone, pas uniquement des espaces.' in js,
        'German copy': 'Bitte geben Sie Ihren Namen ein, nicht nur Leerzeichen.' in js and 'Bitte geben Sie Ihre WhatsApp- oder Telefonnummer ein, nicht nur Leerzeichen.' in js,
        'Arabic copy': 'يرجى إدخال اسمك، وليس مسافات فقط.' in js and 'يرجى إدخال رقم واتساب أو الهاتف، وليس مسافات فقط.' in js,
        'WhatsApp identity preserved': "const WA='https://wa.me/34600703303';" in js,
        'Ibiza date logic preserved': "timeZone:'Europe/Madrid'" in js,
        'analytics PII guard markers preserved': 'ANALYTICS_NO_PII_START' in js and 'ANALYTICS_NO_PII_END' in js,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(f'Phase 119 audit runtime failed: {failed}')

    result = subprocess.run(['node', '--check', str(RUNTIME)], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit('Phase 119 audit JS syntax failed: ' + (result.stderr or result.stdout))

    for rel in CONTACTS:
        html = (ROOT / rel).read_text(encoding='utf-8')
        if html.count('/assets/phase107.js?v=119') != 1 or '/assets/phase107.js?v=117' in html:
            raise SystemExit(f'Phase 119 runtime version drift: {rel}')
        for field in ('fName', 'fPhone'):
            tags = re.findall(rf'<input\b[^>]*\bid="{field}"[^>]*>', html, re.I)
            if len(tags) != 1 or not re.search(r'\brequired\b', tags[0], re.I):
                raise SystemExit(f'Phase 119 required field drift: {rel} -> {field}')
        phone = re.findall(r'<input\b[^>]*\bid="fPhone"[^>]*>', html, re.I)[0]
        for token in ('type="tel"', 'inputmode="tel"', 'autocomplete="tel"', 'aria-describedby="fPhoneHint"'):
            if token not in phone:
                raise SystemExit(f'Phase 119 phone semantics drift: {rel} -> {token}')
        if re.search(r'\bpattern\s*=', phone, re.I):
            raise SystemExit(f'Phase 119 rigid phone pattern introduced: {rel}')

    print('PASS: Phase 119 audit — whitespace-only name/phone values are guarded in five languages; trimmed handover, Ibiza date logic, phone semantics and no-PII analytics markers preserved')


if __name__ == '__main__':
    run()
