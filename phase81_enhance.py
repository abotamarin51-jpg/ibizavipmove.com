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
SM='http://www.sitemaps.org/schemas/sitemap/0.9'
IM='http://www.google.com/schemas/sitemap-image/1.1'
ET.register_namespace('',SM)
ET.register_namespace('image',IM)


def local_content_path(url):
    path=urlparse(url).path
    return path if path.startswith('/assets/images/') else ''

pages=[]
for file in ROOT.rglob('*.html'):
    html=file.read_text(encoding='utf-8')
    if NOINDEX.search(html):continue
    cm=CANON.search(html)
    if not cm:continue
    canonical=cm.group(1).strip()
    if not canonical.startswith(BASE):raise SystemExit(f'Phase 81 external canonical: {file.relative_to(ROOT)} -> {canonical}')
    images=[]
    for src in IMG.findall(html):
        path=local_content_path(src)
        if path and path not in images:images.append(path)
    hm=CSS_HERO.search(html)
    if hm:
        path=local_content_path(hm.group(1))
        if path and path not in images:images.append(path)
    for path in images:
        asset=ROOT/path.lstrip('/')
        if not asset.exists():raise SystemExit(f'Phase 81 referenced image missing: {canonical} -> {path}')
    if images:pages.append((canonical,images))

pages.sort(key=lambda x:x[0])
urlset=ET.Element(ET.QName(SM,'urlset'))
for canonical,images in pages:
    u=ET.SubElement(urlset,ET.QName(SM,'url'))
    ET.SubElement(u,ET.QName(SM,'loc')).text=canonical
    for path in images:
        im=ET.SubElement(u,ET.QName(IM,'image'))
        ET.SubElement(im,ET.QName(IM,'loc')).text=BASE+path

out=ROOT/'image-sitemap.xml'
ET.ElementTree(urlset).write(out,encoding='utf-8',xml_declaration=True)

if len(pages)<120:raise SystemExit(f'Phase 81 image sitemap coverage unexpectedly low: {len(pages)}')
relations=sum(len(v) for _,v in pages)
if relations<len(pages):raise SystemExit('Phase 81 impossible image relation count')
print(f'PASS: Phase 81 image discovery — {len(pages)} canonical pages and {relations} real local content-image relations written to image-sitemap.xml')
