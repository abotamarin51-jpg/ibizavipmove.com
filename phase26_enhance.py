from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
IMAGE_NS = 'http://www.google.com/schemas/sitemap-image/1.1'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
OG_IMAGE_RE = re.compile(r'<meta\s+property="og:image"\s+content="([^"]+)"', re.I)
IMG_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.I)
SOURCE_RE = re.compile(r'<source\b[^>]*\bsrcset="([^"]+)"', re.I)
JSONLD_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)
ROBOTS_NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)


def abs_url(value):
    value = (value or '').strip()
    if not value or value.startswith(('data:', 'javascript:')):
        return None
    return urljoin(BASE + '/', value)


def wanted_image(url):
    if not url:
        return False
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != urlparse(BASE).netloc:
        return False
    path = parsed.path.lower()
    if '/assets/images/' not in path:
        return False
    if path.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif')):
        return True
    return False


def srcset_urls(value):
    urls=[]
    for item in value.split(','):
        candidate=item.strip().split()[0] if item.strip() else ''
        u=abs_url(candidate)
        if wanted_image(u): urls.append(u)
    return urls


def enrich_jsonld(text, preferred):
    if not preferred:
        return text
    def repl(m):
        try:
            data=json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if not isinstance(data,dict):
            return m.group(0)
        typ=data.get('@type')
        img={'@type':'ImageObject','url':preferred}
        if typ in ('WebPage','AboutPage','ContactPage','CollectionPage','ProfilePage'):
            data['primaryImageOfPage']=img
        elif typ in ('Article','NewsArticle','BlogPosting'):
            data['image']=preferred
        elif typ=='Service':
            data['image']=preferred
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
    return JSONLD_RE.sub(repl,text)


entries=[]
pages_with_images=0
unique_images=set()
for path in ROOT.rglob('*.html'):
    text=path.read_text(encoding='utf-8')
    if ROBOTS_NOINDEX_RE.search(text):
        continue
    cm=CANONICAL_RE.search(text)
    if not cm:
        continue
    canonical=cm.group(1).strip()
    if not canonical.startswith(BASE):
        continue

    images=[]
    og=OG_IMAGE_RE.search(text)
    preferred=abs_url(og.group(1)) if og else None
    if wanted_image(preferred):
        images.append(preferred)

    for src in IMG_RE.findall(text):
        u=abs_url(src)
        if wanted_image(u): images.append(u)
    for srcset in SOURCE_RE.findall(text):
        images.extend(srcset_urls(srcset))

    dedup=[]; seen=set()
    for u in images:
        if u not in seen:
            dedup.append(u); seen.add(u); unique_images.add(u)

    if dedup:
        pages_with_images += 1
        entries.append((canonical,dedup))
        # Preferred image metadata uses the explicit og:image when it is a local content image.
        if wanted_image(preferred):
            updated=enrich_jsonld(text,preferred)
            if updated != text:
                path.write_text(updated,encoding='utf-8')

# Standalone Google image sitemap. Only required image:loc tags are used;
# deprecated caption/title/license sitemap tags are intentionally omitted.
ET.register_namespace('', SITEMAP_NS)
ET.register_namespace('image', IMAGE_NS)
root=ET.Element(f'{{{SITEMAP_NS}}}urlset')
for canonical,images in entries:
    url_el=ET.SubElement(root,f'{{{SITEMAP_NS}}}url')
    ET.SubElement(url_el,f'{{{SITEMAP_NS}}}loc').text=canonical
    for image in images:
        image_el=ET.SubElement(url_el,f'{{{IMAGE_NS}}}image')
        ET.SubElement(image_el,f'{{{IMAGE_NS}}}loc').text=image
ET.ElementTree(root).write(ROOT/'image-sitemap.xml',encoding='utf-8',xml_declaration=True)

# Advertise both sitemaps in robots.txt. Phase 15 rewrites robots earlier in the build,
# so this post-process is deterministic on every release.
robots=ROOT/'robots.txt'
rt=robots.read_text(encoding='utf-8') if robots.exists() else 'User-agent: *\nAllow: /\n'
main_line=f'Sitemap: {BASE}/sitemap.xml'
image_line=f'Sitemap: {BASE}/image-sitemap.xml'
lines=[line for line in rt.splitlines() if not line.lower().startswith('sitemap:')]
lines.extend([main_line,image_line])
robots.write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')

# Validation.
assert entries, 'Image sitemap has no page entries'
assert pages_with_images >= 20, f'Too few pages with discoverable content images: {pages_with_images}'
assert len(unique_images) >= 8, f'Too few unique content images: {len(unique_images)}'
xml=(ROOT/'image-sitemap.xml').read_text(encoding='utf-8')
assert 'http://www.google.com/schemas/sitemap-image/1.1' in xml
assert '<image:loc>' in xml
assert '<image:title>' not in xml and '<image:caption>' not in xml and '<image:license>' not in xml
final_robots=robots.read_text(encoding='utf-8')
assert main_line in final_robots and image_line in final_robots
print(f'PASS: Phase 26 image discovery — {pages_with_images} pages, {len(unique_images)} unique local content images, standalone image sitemap + preferred-image schema')
