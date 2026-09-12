"""Cache-bust the qualified-brief runtime after Ibiza-time date validation changes."""
from pathlib import Path

ROOT = Path('_site')
CONTACTS = [
    'contact/index.html',
    'es/contacto/index.html',
    'fr/contact/index.html',
    'de/kontakt/index.html',
    'ar/contact/index.html',
]
OLD = '/assets/phase107.js?v=107'
NEW = '/assets/phase107.js?v=117'


def enhance():
    for rel in CONTACTS:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 117 missing contact page: {rel}')
        html = path.read_text(encoding='utf-8')
        if html.count(NEW) == 1 and OLD not in html:
            continue
        if html.count(OLD) != 1 or NEW in html:
            raise SystemExit(f'Phase 117 runtime reference drift: {rel}')
        path.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 117 — qualified-brief runtime cache-busted on all five contact desks after Ibiza-time validation update')


if __name__ == '__main__':
    enhance()
