from pathlib import Path
from html import unescape
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
MEDIA=(
'/media-partners/','/es/media-partners/','/fr/media-partners/','/de/media-partners/','/ar/media-partners/'
)
NOINDEX=re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex',re.I)


def value(html,attr,name):
    m=re.search(rf'<meta\b(?=[^>]*\b{attr}="{re.escape(name)}")(?=[^>]*\bcontent="([^"]*)")[^>]*>',html,re.I)
    return unescape(m.group(1)).strip() if m else ''
def canonical(html):
    m=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
    return m.group(1).strip() if m else ''
def title(html):
    m=re.search(r'<title>(.*?)</title>',html,re.I|re.S)
    return unescape(re.sub(r'<[^>]+>',' ',m.group(1))).strip() if m else ''
def desc(html):
    m=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',html,re.I)
    return unescape(m.group(1)).strip() if m else ''

checked=0
for f in ROOT.rglob('*.html'):
    html=f.read_text(encoding='utf-8')
    if NOINDEX.search(html):continue
    can=canonical(html)
    if not can:continue
    og=value(html,'property','og:url')
    if not og:raise SystemExit(f'Phase 80 audit missing og:url: {f.relative_to(ROOT)}')
    if og.rstrip('/')!=can.rstrip('/'):
        raise SystemExit(f'Phase 80 audit og:url != canonical: {f.relative_to(ROOT)} -> {og} vs {can}')
    checked+=1

if checked!=138:raise SystemExit(f'Phase 80 audit expected 138 indexable pages, found {checked}')

image=BASE+'/assets/images/private-office.jpg'
for path in MEDIA:
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists():raise SystemExit(f'Phase 80 audit missing Media page: {path}')
    html=f.read_text(encoding='utf-8'); can=canonical(html); t=title(html); d=desc(html)
    expected={
        ('property','og:type'):'website',('property','og:url'):can,('property','og:title'):t,
        ('property','og:description'):d,('property','og:image'):image,
        ('name','twitter:card'):'summary_large_image',('name','twitter:title'):t,
        ('name','twitter:description'):d,('name','twitter:image'):image,
    }
    for (attr,name),wanted in expected.items():
        got=value(html,attr,name)
        if got!=wanted:raise SystemExit(f'Phase 80 audit {name} mismatch: {path} -> {got!r} vs {wanted!r}')

print('PASS: Phase 80 social audit — 138 canonical og:url values verified and 5 Media & Partners previews fully aligned')
