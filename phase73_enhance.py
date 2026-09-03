from pathlib import Path
import re
import shutil

ROOT = Path('_site')
HOME = ROOT / 'index.html'
CSS_SRC = Path('phase73.css')
CSS_HREF = '/assets/phase73.css?v=73'

if not HOME.exists():
    raise SystemExit('Phase 73 homepage missing')
if not CSS_SRC.exists():
    raise SystemExit('Phase 73 stylesheet missing')

css_dest = ROOT / 'assets' / 'phase73.css'
css_dest.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(CSS_SRC, css_dest)

html = HOME.read_text(encoding='utf-8')
if CSS_HREF not in html:
    html = html.replace('</head>', f'<link rel="stylesheet" href="{CSS_HREF}"></head>', 1)

anchors = {
    'move': '/private-chauffeur-ibiza/',
    'stay': '/luxury-villas-ibiza/',
    'sea': '/yacht-charter-ibiza/',
    'access': '/restaurants-nightlife-ibiza/',
    'fly': '/private-aviation-ibiza/',
    'protect': '/private-security-ibiza/',
}

for anchor_id, href in anchors.items():
    # Keep the approved service-card markup intact; only add the missing target id.
    pattern = re.compile(
        rf'<a\s+class="ivm-ref-service"\s+href="{re.escape(href)}"(?![^>]*\bid=)([^>]*)>',
        re.I,
    )
    replacement = f'<a class="ivm-ref-service" id="{anchor_id}" href="{href}"\\1>'
    html, count = pattern.subn(replacement, html, count=1)
    if count == 0 and f'id="{anchor_id}"' not in html:
        raise SystemExit(f'Phase 73 could not attach #{anchor_id} to {href}')

HOME.write_text(html, encoding='utf-8')

# Validate both desktop and mobile navigation targets and ensure every target is unique.
final = HOME.read_text(encoding='utf-8')
for anchor_id, href in anchors.items():
    if final.count(f'id="{anchor_id}"') != 1:
        raise SystemExit(f'Phase 73 expected one #{anchor_id} target')
    if final.count(f'href="#{anchor_id}"') < 2:
        raise SystemExit(f'Phase 73 expected desktop + mobile links to #{anchor_id}')
    target = re.search(rf'<a\b[^>]*\bid="{anchor_id}"[^>]*>', final, re.I)
    if not target or f'href="{href}"' not in target.group(0):
        raise SystemExit(f'Phase 73 #{anchor_id} is not attached to {href}')

if CSS_HREF not in final or not css_dest.exists():
    raise SystemExit('Phase 73 scroll-offset styling missing')

print('PASS: Phase 73 homepage chapter navigation — 6 desktop/mobile anchors resolve to the correct service cards')
