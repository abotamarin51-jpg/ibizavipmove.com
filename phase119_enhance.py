"""Reject whitespace-only name/phone values and trim handover text without changing form inventory."""
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
OLD_REF = '/assets/phase107.js?v=117'
NEW_REF = '/assets/phase107.js?v=119'

MESSAGES = {
    "departureBeforeArrival:'Departure cannot be before arrival.'": "departureBeforeArrival:'Departure cannot be before arrival.',nameBlank:'Please enter your name, not only spaces.',phoneBlank:'Please enter your WhatsApp or phone number, not only spaces.'",
    "departureBeforeArrival:'La salida no puede ser anterior a la llegada.'": "departureBeforeArrival:'La salida no puede ser anterior a la llegada.',nameBlank:'Introduce tu nombre, no solo espacios.',phoneBlank:'Introduce tu WhatsApp o teléfono, no solo espacios.'",
    "departureBeforeArrival:'Le départ ne peut pas précéder l’arrivée.'": "departureBeforeArrival:'Le départ ne peut pas précéder l’arrivée.',nameBlank:'Saisissez votre nom, pas uniquement des espaces.',phoneBlank:'Saisissez votre WhatsApp ou téléphone, pas uniquement des espaces.'",
    "departureBeforeArrival:'Die Abreise darf nicht vor der Anreise liegen.'": "departureBeforeArrival:'Die Abreise darf nicht vor der Anreise liegen.',nameBlank:'Bitte geben Sie Ihren Namen ein, nicht nur Leerzeichen.',phoneBlank:'Bitte geben Sie Ihre WhatsApp- oder Telefonnummer ein, nicht nur Leerzeichen.'",
    "departureBeforeArrival:'لا يمكن أن يكون تاريخ المغادرة قبل تاريخ الوصول.'": "departureBeforeArrival:'لا يمكن أن يكون تاريخ المغادرة قبل تاريخ الوصول.',nameBlank:'يرجى إدخال اسمك، وليس مسافات فقط.',phoneBlank:'يرجى إدخال رقم واتساب أو الهاتف، وليس مسافات فقط.'",
}


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Phase 119 expected one {label}, found {count}')
    return text.replace(old, new, 1)


def enhance():
    if not RUNTIME.is_file():
        raise SystemExit('Phase 119 runtime missing')
    js = RUNTIME.read_text(encoding='utf-8')
    if 'validateRequiredText' in js or 'nameBlank' in js or 'phoneBlank' in js:
        raise SystemExit('Phase 119 runtime appears already enhanced')

    for old, new in MESSAGES.items():
        js = replace_once(js, old, new, 'localized required-text message')

    js = replace_once(
        js,
        "const g=id=>document.getElementById(id)?.value||'';",
        "const g=id=>(document.getElementById(id)?.value||'').trim();",
        'trimmed field getter',
    )

    anchor = "  const arrival=document.getElementById('fArrival');\n"
    validation = (
        "  const nameField=document.getElementById('fName');\n"
        "  const phoneField=document.getElementById('fPhone');\n"
        "  const validateRequiredText=()=>{\n"
        "    if(nameField)nameField.setCustomValidity(nameField.value&&!nameField.value.trim()?c.nameBlank:'');\n"
        "    if(phoneField)phoneField.setCustomValidity(phoneField.value&&!phoneField.value.trim()?c.phoneBlank:'');\n"
        "  };\n"
        "  [nameField,phoneField].forEach(el=>{\n"
        "    if(!el)return;\n"
        "    el.addEventListener('input',validateRequiredText);\n"
        "    el.addEventListener('change',validateRequiredText);\n"
        "  });\n"
        "  validateRequiredText();\n\n"
    )
    js = replace_once(js, anchor, validation + anchor, 'required-text validation anchor')
    js = replace_once(
        js,
        "    validateDates();\n    if(!f.reportValidity())return;",
        "    validateDates();\n    validateRequiredText();\n    if(!f.reportValidity())return;",
        'submit validation order',
    )
    RUNTIME.write_text(js, encoding='utf-8')

    for rel in CONTACTS:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 119 contact missing: {rel}')
        html = path.read_text(encoding='utf-8')
        if html.count(NEW_REF) == 1 and OLD_REF not in html:
            continue
        if html.count(OLD_REF) != 1 or NEW_REF in html:
            raise SystemExit(f'Phase 119 runtime reference drift: {rel}')
        path.write_text(html.replace(OLD_REF, NEW_REF, 1), encoding='utf-8')

    print('PASS: Phase 119 — whitespace-only required name/phone values rejected; outgoing brief text trimmed; five contact desks cache-busted to v119')


if __name__ == '__main__':
    enhance()
