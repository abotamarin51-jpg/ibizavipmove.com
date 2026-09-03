from pathlib import Path
import re

ROOT = Path('_site')

PAGES = [
    '/es/private-office/', '/es/partners/',
    '/fr/private-office/', '/fr/partners/',
    '/de/private-office/', '/de/partners/',
    '/ar/private-office/', '/ar/partners/',
]

for path in PAGES:
    file = ROOT / path.strip('/') / 'index.html'
    if not file.exists():
        raise SystemExit(f'Phase 51 accessibility target missing: {path}')
    html = file.read_text(encoding='utf-8')
    html, count = re.subn(r'<main\b[^>]*>', '<main id="main-content">', html, count=1, flags=re.I)
    if count != 1:
        raise SystemExit(f'Unable to normalize main landmark: {path}')
    file.write_text(html, encoding='utf-8')

for path in PAGES:
    html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
    assert html.count('id="main-content"') == 1, (path, 'main landmark')
    assert 'class="ivm-skip-link"' in html, (path, 'skip link')
    assert html.count('<h1') == 1, (path, 'h1')

print(f'PASS: Phase 51 accessibility landmarks restored on {len(PAGES)} localized B2B pages')
