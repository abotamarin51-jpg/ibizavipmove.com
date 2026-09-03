from pathlib import Path
import re

ROOT = Path('_site')
STYLE = '/assets/phase62.css?v=62'
PAGES = [
    '/',
    '/private-concierge-ibiza/',
    '/private-chauffeur-ibiza/',
    '/luxury-villas-ibiza/',
    '/yacht-charter-ibiza/',
    '/private-aviation-ibiza/',
    '/restaurants-nightlife-ibiza/',
    '/private-security-ibiza/',
    '/contact/',
]

assets = ROOT / 'assets'
assets.mkdir(parents=True, exist_ok=True)
(assets / 'phase62.css').write_text(Path('phase62.css').read_text(encoding='utf-8'), encoding='utf-8')


def file_for(path):
    return ROOT / 'index.html' if path == '/' else ROOT / path.strip('/') / 'index.html'


def canonical_of(html):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    return m.group(1) if m else None


def add_body_class(html):
    m = re.search(r'<body\b([^>]*)>', html, re.I)
    if not m:
        raise SystemExit('Phase 62 body tag missing')
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs, re.I)
    if cm:
        classes = cm.group(1).split()
        if 'ivm-final-polish' not in classes:
            classes.append('ivm-final-polish')
        new_attrs = attrs[:cm.start()] + f'class="{" ".join(classes)}"' + attrs[cm.end():]
    else:
        new_attrs = attrs + ' class="ivm-final-polish"'
    return html[:m.start()] + '<body' + new_attrs + '>' + html[m.end():]


updated = 0
for path in PAGES:
    file = file_for(path)
    if not file.exists():
        raise SystemExit(f'Phase 62 priority page missing: {path}')
    html = file.read_text(encoding='utf-8')
    before_canonical = canonical_of(html)
    html = add_body_class(html)
    if STYLE not in html:
        html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
    # iPhone safe-area support. Preserve all existing viewport directives.
    vm = re.search(r'<meta\s+name="viewport"\s+content="([^"]*)"\s*/?>', html, re.I)
    if vm and 'viewport-fit=cover' not in vm.group(1):
        content = vm.group(1).rstrip(', ')
        replacement = f'<meta name="viewport" content="{content},viewport-fit=cover">'
        html = html[:vm.start()] + replacement + html[vm.end():]
    after_canonical = canonical_of(html)
    if before_canonical != after_canonical:
        raise SystemExit(f'Phase 62 canonical changed unexpectedly: {path}')
    file.write_text(html, encoding='utf-8')
    updated += 1

# Final assertions: no SEO/content architecture changes, only polish hooks.
for path in PAGES:
    html = file_for(path).read_text(encoding='utf-8')
    assert html.count('ivm-final-polish') == 1, path
    assert html.count(STYLE) == 1, path
    assert html.count('<h1') == 1, path
    assert 'viewport-fit=cover' in html, path
    assert canonical_of(html), path

home = file_for('/').read_text(encoding='utf-8')
assert 'ivm-editorial-home' in home
for path in PAGES[1:8]:
    html = file_for(path).read_text(encoding='utf-8')
    assert 'ivm-signature-inner' in html, path
contact = file_for('/contact/').read_text(encoding='utf-8')
assert 'ivm-private-desk' in contact
assert (assets / 'phase62.css').stat().st_size > 3000
print(f'PASS: Phase 62 final visual polish applied safely to {updated} priority journeys')
