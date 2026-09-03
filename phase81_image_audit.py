from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
NOINDEX=re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex',re.I)
CANON=re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"',re.I)
IMG=re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']',re.I)
CSS_HERO=re.compile(r'--hero\s*:\s*url\(\s*[\'\"]?([^\'\")\s]+)',re.I)
SM={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}

def content_paths(html):
    out=[]
    for src in IMG.findall(html):
        path=urlparse(src).path
        if path.startswith('/assets/images/') and path not in out:out.append(path)
    hm=CSS_HERO.search(html)
    if hm:
        path=urlparse(hm.group(1)).path
        if path.startswith('/assets/images/') and path not in out:out.append(path)
    return out

expected={}
for f in ROOT.rglob('*.html'):
    html=f.read_text(encoding='utf-8')
    if NOINDEX.search(html):continue
    cm=CANON.search(html)
    if not cm:continue
    paths=content_paths(html)
    if paths:expected[cm.group(1).strip()]=[BASE+p for p in paths]

sm=ROOT/'image-sitemap.xml'
if not sm.exists():raise SystemExit('Phase 81 audit image-sitemap.xml missing')
try:root=ET.parse(sm).getroot()
except Exception as exc:raise SystemExit(f'Phase 81 audit XML parse failure: {exc}')
actual={}
for u in root.findall('s:url',SM):
    loc=u.find('s:loc',SM)
    if loc is None or not loc.text:raise SystemExit('Phase 81 audit sitemap URL without loc')
    page=loc.text.strip()
    if page in actual:raise SystemExit(f'Phase 81 audit duplicate page: {page}')
    imgs=[]
    for node in u.findall('i:image',SM):
        il=node.find('i:loc',SM)
        if il is None or not il.text:raise SystemExit(f'Phase 81 audit image without loc: {page}')
        image=il.text.strip()
        if image in imgs:raise SystemExit(f'Phase 81 audit duplicate image on page: {page} -> {image}')
        if not image.startswith(BASE+'/assets/images/'):raise SystemExit(f'Phase 81 audit non-content image: {page} -> {image}')
        asset=ROOT/urlparse(image).path.lstrip('/')
        if not asset.exists():raise SystemExit(f'Phase 81 audit missing image asset: {image}')
        imgs.append(image)
    if not imgs:raise SystemExit(f'Phase 81 audit page without images: {page}')
    actual[page]=imgs

if actual!=expected:
    missing=sorted(set(expected)-set(actual)); extra=sorted(set(actual)-set(expected))
    changed=sorted(k for k in set(expected)&set(actual) if expected[k]!=actual[k])
    raise SystemExit(f'Phase 81 audit mismatch: missing={missing[:5]} extra={extra[:5]} changed={changed[:5]}')
if len(actual)<120:raise SystemExit(f'Phase 81 audit coverage too low: {len(actual)}')
print(f'PASS: Phase 81 image audit — {len(actual)} canonical pages exactly match {sum(len(v) for v in actual.values())} rendered local content-image relations')
