from pathlib import Path
import re

ROOT=Path('_site')
NOINDEX_RE=re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex',re.I)
CANON_RE=re.compile(r'<link\s+rel="canonical"',re.I)
IMG_RE=re.compile(r'<img\b[^>]*>',re.I)

DIMS={
    '/assets/brand-logo.svg':(1050,230),
    '/assets/images/nightlife.jpg':(1800,2700),
    '/assets/images/private-office.jpg':(3024,4032),
    '/assets/images/bespoke.jpg':(1900,2850),
}


def src_of(tag):
    m=re.search(r'\bsrc=["\']([^"\']+)["\']',tag,re.I)
    return m.group(1) if m else None


def url_path(src):
    return src.split('?',1)[0] if src else ''


updated_tags=0
header_lazy_removed=0
pages=0

for file in ROOT.rglob('*.html'):
    html=file.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html) or not CANON_RE.search(html):
        continue
    pages+=1
    header=re.search(r'<header\b[^>]*class=["\'][^"\']*site-header[^"\']*["\'][^>]*>.*?</header>',html,re.I|re.S)
    hs,he=(header.start(),header.end()) if header else (-1,-1)

    out=[];cursor=0
    for m in IMG_RE.finditer(html):
        out.append(html[cursor:m.start()])
        tag=m.group(0);src=src_of(tag);path=url_path(src)
        before=tag
        if path in DIMS:
            w,h=DIMS[path]
            # Intrinsic dimensions reserve layout space without changing the
            # existing responsive CSS-rendered size.
            if not re.search(r'\bwidth=["\']?\d+',tag,re.I):
                tag=tag[:-1]+f' width="{w}">'
            if not re.search(r'\bheight=["\']?\d+',tag,re.I):
                tag=tag[:-1]+f' height="{h}">'
        if path=='/assets/brand-logo.svg' and hs<=m.start()<he:
            if re.search(r'\sloading=["\']lazy["\']',tag,re.I):
                tag=re.sub(r'\sloading=["\']lazy["\']','',tag,flags=re.I)
                header_lazy_removed+=1
        if tag!=before: updated_tags+=1
        out.append(tag);cursor=m.end()
    out.append(html[cursor:])
    file.write_text(''.join(out),encoding='utf-8')

# Final layout-stability validation: every local image on every indexable page
# must expose intrinsic width/height, and header logos must never be lazy.
missing=[]
for file in ROOT.rglob('*.html'):
    html=file.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html) or not CANON_RE.search(html):
        continue
    header=re.search(r'<header\b[^>]*class=["\'][^"\']*site-header[^"\']*["\'][^>]*>.*?</header>',html,re.I|re.S)
    for tag in IMG_RE.findall(html):
        src=src_of(tag)
        if not src or not url_path(src).startswith('/assets/'):
            continue
        if not re.search(r'\bwidth=["\']?\d+',tag,re.I) or not re.search(r'\bheight=["\']?\d+',tag,re.I):
            missing.append(f'{file.relative_to(ROOT)}: {src}')
    if header:
        for tag in IMG_RE.findall(header.group(0)):
            if url_path(src_of(tag))=='/assets/brand-logo.svg' and re.search(r'\sloading=["\']lazy["\']',tag,re.I):
                raise SystemExit(f'Phase 70 header logo remains lazy: {file.relative_to(ROOT)}')
if missing:
    raise SystemExit('Phase 70 local images missing intrinsic dimensions: '+ '; '.join(missing[:12]))
if updated_tags<200:
    raise SystemExit(f'Phase 70 unexpectedly few stabilized images: {updated_tags}')
print(f'PASS: Phase 70 image layout stability — {pages} indexable pages; {updated_tags} image tags stabilized with intrinsic dimensions/loading corrections; {header_lazy_removed} above-fold logo lazy-loads removed')
