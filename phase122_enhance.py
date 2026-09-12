"""Remove unauthorized membership wording from the five existing contact desks."""
from pathlib import Path

ROOT = Path('_site')
LABELS = {
    '/contact/': 'Private Client Desk · Ibiza',
    '/es/contacto/': 'Atención a clientes privados · Ibiza',
    '/fr/contact/': 'Service clients privés · Ibiza',
    '/de/kontakt/': 'Betreuung für Privatkunden · Ibiza',
    '/ar/contact/': 'خدمة العملاء الخاصين · إيبيزا',
}
OLD = 'Private Members Desk · Ibiza'


def enhance():
    pending = {}
    for route, label in LABELS.items():
        path = ROOT / route.strip('/') / 'index.html'
        if not path.is_file():
            raise SystemExit(f'Phase 122 contact page missing: {route}')
        html = path.read_text(encoding='utf-8')
        if html.count(OLD) != 1:
            raise SystemExit(f'Phase 122 expected one legacy membership label: {route} -> {html.count(OLD)}')
        if label in html:
            raise SystemExit(f'Phase 122 localized replacement already present: {route}')
        pending[path] = html.replace(OLD, label, 1)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print('PASS: Phase 122 — five contact desks use private-client service wording; unauthorized membership terminology removed without changing URLs, forms or assets')


if __name__ == '__main__':
    enhance()
