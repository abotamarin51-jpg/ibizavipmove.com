"""Read-only gate for Phase 149 priority yacht modern-format delivery."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, features
from phase149_enhance import PAGES, PRELOAD_PAGES, JPEG, AVIF, WEBP

ROOT = Path('_site')


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.stack=[]; self.pictures=[]; self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if tag=='picture': self.stack.append({'attrs':attrs,'sources':[],'imgs':[]})
        elif tag=='source' and self.stack: self.stack[-1]['sources'].append(attrs)
        elif tag=='img' and self.stack: self.stack[-1]['imgs'].append(attrs)
    def handle_endtag(self, tag):
        if tag=='picture' and self.stack: self.pictures.append(self.stack.pop())


def require(ok,msg):
    if not ok: raise SystemExit('Phase 149 audit: '+msg)


def run():
    require(features.check('avif') and features.check('webp'),'Pillow modern-format support missing')
    jpeg=ROOT/JPEG.lstrip('/'); avif=ROOT/AVIF.lstrip('/'); webp=ROOT/WEBP.lstrip('/')
    require(jpeg.is_file() and avif.is_file() and webp.is_file(),'yacht assets missing')
    require(avif.stat().st_size < jpeg.stat().st_size*.55,'AVIF no longer meets reviewed size budget')
    require(webp.stat().st_size < jpeg.stat().st_size*.60,'WebP no longer meets reviewed size budget')
    with Image.open(jpeg) as j, Image.open(avif) as a, Image.open(webp) as w:
        require(j.size==a.size==w.size==(2000,1333),'yacht dimensions changed')

    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'canonical inventory changed')

    observed=set()
    for path in ROOT.rglob('index.html'):
        parsed=Tags(path.read_text(encoding='utf-8'))
        if any(t=='img' and a.get('src')==JPEG and a.get('fetchpriority')=='high' for t,a in parsed.tags):
            rel=path.relative_to(ROOT); observed.add(str(rel.parent).replace('\\','/'))
    require(observed==set(PAGES),f'unreviewed priority yacht inventory: {sorted(observed ^ set(PAGES))}')

    for slug in PAGES:
        path=ROOT/slug/'index.html'; require(path.is_file(),f'missing target {slug}')
        parsed=Tags(path.read_text(encoding='utf-8'))
        matches=[]
        for pic in parsed.pictures:
            if pic['attrs'].get('data-ivm149')!='yacht-priority': continue
            av=[a for a in pic['sources'] if a.get('type')=='image/avif' and a.get('srcset')==AVIF]
            wp=[a for a in pic['sources'] if a.get('type')=='image/webp' and a.get('srcset')==WEBP]
            im=[a for a in pic['imgs'] if a.get('src')==JPEG and a.get('fetchpriority')=='high']
            if av and wp and im: matches.append(pic)
        require(len(matches)==1,f'{slug}: expected one reviewed yacht picture')
        require(sum(t=='h1' for t,a in parsed.tags)==1,f'{slug}: expected one H1')
        url='https://ibizavipmove.com/'+slug+'/'
        require([a.get('href') for t,a in parsed.tags if t=='link' and a.get('rel')=='canonical']==[url],f'{slug}: self canonical')
        require(url in urls,f'{slug}: canonical remains in sitemap')
        require(not any(t=='meta' and a.get('name','').lower() in {'robots','googlebot'} and 'noindex' in a.get('content','').lower() for t,a in parsed.tags),f'{slug}: indexability')
        require({a.get('hreflang') for t,a in parsed.tags if t=='link' and a.get('rel')=='alternate'}=={'en','es','fr','de','ar','x-default'},f'{slug}: language cluster')
        pre=[a for t,a in parsed.tags if t=='link' and a.get('rel')=='preload' and a.get('as')=='image']
        require(not any(a.get('href')==JPEG for a in pre),f'{slug}: JPEG preload remains')
        if slug in PRELOAD_PAGES:
            require(any(a.get('href')==AVIF and a.get('type')=='image/avif' for a in pre),f'{slug}: AVIF preload missing')
        else:
            require(not any(a.get('href')==AVIF for a in pre),f'{slug}: unexpected AVIF preload')

    print(
        f'PASS: Phase 149 audit — {len(PAGES)} priority yacht pages prefer AVIF/WebP with JPEG fallback; '
        f'{jpeg.stat().st_size} -> {avif.stat().st_size}/{webp.stat().st_size} bytes; 156 canonicals preserved'
    )


if __name__=='__main__':
    run()
