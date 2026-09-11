from pathlib import Path
import re

ROOT = Path('_site')
SLUGS = [
    'luxury-lifestyle-management-ibiza',
    'personal-concierge-ibiza',
    'luxury-travel-concierge-ibiza',
    'vip-services-ibiza',
    'private-client-services-ibiza',
    'destination-management-ibiza',
]

for slug in SLUGS:
    target = ROOT / slug / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 102 accessibility target missing: /{slug}/')
    html = target.read_text(encoding='utf-8')
    if 'id="main-content"' not in html:
        html, count = re.subn(r'<main\b[^>]*>', '<main id="main-content">', html, count=1, flags=re.I)
        if count != 1:
            raise SystemExit(f'Phase 102 could not restore main-content landmark: /{slug}/')
        target.write_text(html, encoding='utf-8')
    if 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 102 shared skip link missing: /{slug}/')

print('PASS: Phase 102 accessibility — main-content landmark and shared skip link preserved across six intent pages')
