"""Reject clearly incomplete phone values without imposing a country-specific phone pattern."""
from pathlib import Path

ROOT = Path('_site')
RUNTIME = ROOT / 'assets' / 'phase107.js'
CONTACTS = [
    'contact/index.html',
    'es/contacto/index.html',
    'fr/contact/index.html',
    'de/kontakt/index.html',
    'ar/contact/index.html',
]
OLD_REF = '/assets/phase107.js?v=119'
NEW_REF = '/assets/phase107.js?v=120'

MESSAGES = {
    "phoneBlank:'Please enter your WhatsApp or phone number, not only spaces.'": "phoneBlank:'Please enter your WhatsApp or phone number, not only spaces.',phoneDigits:'Please enter a complete international phone number with at least seven digits.'",
    "phoneBlank:'Introduce tu WhatsApp o teléfono, no solo espacios.'": "phoneBlank:'Introduce tu WhatsApp o teléfono, no solo espacios.',phoneDigits:'Introduce un número internacional completo con al menos siete dígitos.'",
    "phoneBlank:'Saisissez votre WhatsApp ou téléphone, pas uniquement des espaces.'": "phoneBlank:'Saisissez votre WhatsApp ou téléphone, pas uniquement des espaces.',phoneDigits:'Saisissez un numéro international complet avec au moins sept chiffres.'",
    "phoneBlank:'Bitte geben Sie Ihre WhatsApp- oder Telefonnummer ein, nicht nur Leerzeichen.'": "phoneBlank:'Bitte geben Sie Ihre WhatsApp- oder Telefonnummer ein, nicht nur Leerzeichen.',phoneDigits:'Bitte geben Sie eine vollständige internationale Telefonnummer mit mindestens sieben Ziffern ein.'",
    "phoneBlank:'يرجى إدخال رقم واتساب أو الهاتف، وليس مسافات فقط.'": "phoneBlank:'يرجى إدخال رقم واتساب أو الهاتف، وليس مسافات فقط.',phoneDigits:'يرجى إدخال رقم هاتف دولي كامل يحتوي على سبعة أرقام على الأقل.'",
}


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Phase 120 expected one {label}, found {count}')
    return text.replace(old, new, 1)


def enhance():
    if not RUNTIME.is_file():
        raise SystemExit('Phase 120 runtime missing')
    js = RUNTIME.read_text(encoding='utf-8')
    if 'phoneDigits' in js or "match(/\\p{Nd}/gu)" in js:
        raise SystemExit('Phase 120 runtime appears already enhanced')

    for old, new in MESSAGES.items():
        js = replace_once(js, old, new, 'localized phone plausibility message')

    old_validator = "    if(phoneField)phoneField.setCustomValidity(phoneField.value&&!phoneField.value.trim()?c.phoneBlank:'');"
    new_validator = (
        "    if(phoneField){\n"
        "      const phone=phoneField.value.trim();\n"
        "      const digits=(phone.match(/\\p{Nd}/gu)||[]).length;\n"
        "      phoneField.setCustomValidity(phoneField.value&&!phone?c.phoneBlank:phone&&digits<7?c.phoneDigits:'');\n"
        "    }"
    )
    js = replace_once(js, old_validator, new_validator, 'phone validator')
    RUNTIME.write_text(js, encoding='utf-8')

    for rel in CONTACTS:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 120 contact missing: {rel}')
        html = path.read_text(encoding='utf-8')
        if html.count(NEW_REF) == 1 and OLD_REF not in html:
            continue
        if html.count(OLD_REF) != 1 or NEW_REF in html:
            raise SystemExit(f'Phase 120 runtime reference drift: {rel}')
        path.write_text(html.replace(OLD_REF, NEW_REF, 1), encoding='utf-8')

    print('PASS: Phase 120 — incomplete phone values with fewer than seven Unicode decimal digits rejected across five contact desks; flexible international formatting preserved')


if __name__ == '__main__':
    enhance()
