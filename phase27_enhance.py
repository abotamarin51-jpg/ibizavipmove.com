from pathlib import Path
import re

ROOT = Path('_site')
STYLE_HREF = '/assets/quintessentially-type.css?v=27'
SOURCE_CSS = Path('quintessentially-type.css')
ASSET_CSS = ROOT / 'assets' / 'quintessentially-type.css'
WA = 'https://wa.me/34600703303'

# Deploy the typography layer as a final override after all previous visual systems.
ASSET_CSS.write_text(SOURCE_CSS.read_text(encoding='utf-8'), encoding='utf-8')

html_count = 0
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if STYLE_HREF not in text and '</head>' in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{STYLE_HREF}"></head>', 1)
    path.write_text(text, encoding='utf-8')
    html_count += 1

# The reference home keeps both high-intent actions visible in the desktop header.
home_path = ROOT / 'index.html'
home = home_path.read_text(encoding='utf-8')
if 'class="ivm-header-whatsapp"' not in home:
    nav_match = re.search(r'<nav>(.*?)</nav>', home, flags=re.I | re.S)
    if nav_match:
        inner = nav_match.group(1)
        whatsapp = f'<a class="ivm-header-whatsapp" href="{WA}">WhatsApp 24/7</a>'
        # Place WhatsApp immediately before the gold concierge CTA when possible.
        if 'class="nav-cta"' in inner:
            inner = re.sub(r'(<a class="nav-cta")', whatsapp + r'\1', inner, count=1)
        else:
            inner += whatsapp
        home = home[:nav_match.start()] + '<nav>' + inner + '</nav>' + home[nav_match.end():]

home_path.write_text(home, encoding='utf-8')

# Release checks: typography should be global and the home should retain the six-service reference structure.
css = ASSET_CSS.read_text(encoding='utf-8')
assert 'Neue Haas Grotesk' in css, 'Neue Haas Grotesk typography stack missing'
assert '82px' in css and '48px' in css, 'Reference hero desktop/mobile scale missing'
assert html_count >= 40, f'Unexpectedly low HTML count: {html_count}'

linked = 0
for path in ROOT.rglob('*.html'):
    if STYLE_HREF in path.read_text(encoding='utf-8'):
        linked += 1
assert linked == html_count, f'Typography stylesheet linked on {linked}/{html_count} HTML files'

home = home_path.read_text(encoding='utf-8')
for required in ['Exceptional Ibiza.', 'id="move"', 'id="stay"', 'id="sea"', 'id="access"', 'id="fly"', 'id="protect"', 'The Ibiza Black Book', 'WhatsApp 24/7', 'Request Concierge']:
    assert required in home, f'Phase 27 home missing {required}'
assert 'ivm-header-whatsapp' in home, 'Desktop header WhatsApp CTA missing'
print(f'PASS: Phase 27 Quintessentially-scale typography on {html_count} pages + dual home CTAs')
