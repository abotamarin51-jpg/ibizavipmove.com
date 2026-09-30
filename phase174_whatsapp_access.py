from pathlib import Path
import re

ROOT = Path('_site')
APPROVED_WA = 'https://wa.me/34600703303'
APPROVED_TEL = 'tel:+34600703303'
ASSET_VERSION = '11'

js_path = ROOT / 'assets' / 'premium.js'
css_path = ROOT / 'assets' / 'premium.css'
assert js_path.is_file(), 'Missing generated premium.js'
assert css_path.is_file(), 'Missing generated premium.css'
js = js_path.read_text(encoding='utf-8')
css = css_path.read_text(encoding='utf-8')

for needle in (
    "className='ivm-whatsapp-float'",
    "IVM_WHATSAPP_ICON",
    "ivm-contact-access-hidden",
    "MutationObserver",
    APPROVED_WA,
):
    assert needle in js, f'Missing Phase 174 JS marker: {needle}'

for needle in (
    '.ivm-whatsapp-float',
    '.ivm-whatsapp-icon',
    'body.ivm-contact-access-hidden .mobile-bar',
    '@media(max-width:600px)',
):
    assert needle in css, f'Missing Phase 174 CSS marker: {needle}'

pages = []
version_errors = []
bar_errors = []
for path in ROOT.rglob('*.html'):
    html = path.read_text(encoding='utf-8')
    if '/assets/premium.js?v=' in html:
        pages.append(path)
        if f'/assets/premium.js?v={ASSET_VERSION}' not in html:
            version_errors.append(str(path))
    if 'class="mobile-bar"' in html:
        match = re.search(r'<div class="mobile-bar">(.*?)</div>', html, re.I | re.S)
        if not match:
            bar_errors.append(f'{path}: mobile bar markup not parseable')
            continue
        block = match.group(1)
        anchors = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>', block, re.I)
        if len(anchors) != 2:
            bar_errors.append(f'{path}: expected exactly two mobile actions, got {len(anchors)}')
        if not any(href.startswith(APPROVED_TEL) for href in anchors):
            bar_errors.append(f'{path}: approved telephone target missing')
        if not any(href.startswith(APPROVED_WA) for href in anchors):
            bar_errors.append(f'{path}: approved WhatsApp target missing')

assert len(pages) >= 150, f'Unexpectedly few premium pages: {len(pages)}'
assert not version_errors, 'premium.js cache version mismatch: ' + ', '.join(version_errors[:5])
assert not bar_errors, 'Mobile contact bar errors: ' + ' | '.join(bar_errors[:5])
print(f'Phase 174 static audit PASS: {len(pages)} premium pages, asset v{ASSET_VERSION}, approved contact targets preserved')
