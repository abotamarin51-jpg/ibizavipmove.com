"""Read-only regression gate for permissive but plausible international phone handover."""
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
MESSAGES = [
    'Please enter a complete international phone number with at least seven digits.',
    'Introduce un número internacional completo con al menos siete dígitos.',
    'Saisissez un numéro international complet avec au moins sept chiffres.',
    'Bitte geben Sie eine vollständige internationale Telefonnummer mit mindestens sieben Ziffern ein.',
    'يرجى إدخال رقم هاتف دولي كامل يحتوي على سبعة أرقام على الأقل.',
]


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 120 audit: ' + message)


def run():
    require(RUNTIME.is_file(), 'phase107 runtime missing')
    js = RUNTIME.read_text(encoding='utf-8')
    for token in (
        "const phone=phoneField.value.trim();",
        "const digits=(phone.match(/\\p{Nd}/gu)||[]).length;",
        "phoneField.setCustomValidity(phoneField.value&&!phone?c.phoneBlank:phone&&digits<7?c.phoneDigits:'');",
        "const WA='https://wa.me/34600703303';",
        "timeZone:'Europe/Madrid'",
        'ANALYTICS_NO_PII_START',
        'ANALYTICS_NO_PII_END',
    ):
        require(token in js, 'runtime token missing: ' + token)
    for message in MESSAGES:
        require(js.count(message) == 1, 'localized message missing/duplicated: ' + message)

    syntax = subprocess.run(['node', '--check', str(RUNTIME)], capture_output=True, text=True)
    require(syntax.returncode == 0, 'runtime syntax error: ' + (syntax.stderr or syntax.stdout).strip())
    fixture = subprocess.run([
        'node', '-e',
        "const n=s=>(s.match(/\\p{Nd}/gu)||[]).length;"
        "if(n('abcdefg')!==0||n('+44 20 7123 4567')<7||n('٠٥٠١٢٣٤٥٦٧')<7)process.exit(1);"
    ], capture_output=True, text=True)
    require(fixture.returncode == 0, 'Unicode digit-count fixture failed')

    for rel in CONTACTS:
        path = ROOT / rel
        require(path.is_file(), 'contact missing: ' + rel)
        html = path.read_text(encoding='utf-8')
        require(html.count('/assets/phase107.js?v=120') == 1, 'v120 runtime reference: ' + rel)
        require('/assets/phase107.js?v=119' not in html, 'stale v119 runtime reference: ' + rel)
        tags = re.findall(r'<input\b[^>]*\bid="fPhone"[^>]*>', html, re.I)
        require(len(tags) == 1, 'phone field cardinality: ' + rel)
        tag = tags[0]
        for token in ('type="tel"', 'inputmode="tel"', 'autocomplete="tel"', 'required', 'aria-describedby="fPhoneHint"'):
            require(token in tag, f'phone semantics {rel}: {token}')
        require(not re.search(r'\bpattern\s*=', tag, re.I), 'rigid HTML phone pattern introduced: ' + rel)

    print('PASS: Phase 120 audit — five contact desks reject clearly incomplete phone values while preserving type=tel, international formatting flexibility, Ibiza-date logic, WhatsApp identity and no-PII analytics guards')


if __name__ == '__main__':
    run()
