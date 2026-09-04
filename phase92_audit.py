from pathlib import Path
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'
ARTICLE='https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/'
PAGES=['/media-partners/','/es/media-partners/','/fr/media-partners/','/de/media-partners/','/ar/media-partners/']
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)
for path in PAGES:
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists(): raise SystemExit(f'Phase 92 audit missing page: {path}')
    html=f.read_text(encoding='utf-8')
    if html.count('ivm-external-reference')!=1: raise SystemExit(f'Phase 92 visible reference mismatch: {path}')
    if html.count(ARTICLE)!=1 and html.count(ARTICLE)!=2:
        raise SystemExit(f'Phase 92 article URL missing/unexpected count: {path} -> {html.count(ARTICLE)}')
    ref=re.search(r'<section\b[^>]*class="[^"]*ivm-external-reference[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
    sec=ref.group(1) if ref else ''
    if 'endorsement or partnership' not in sec: raise SystemExit(f'Phase 92 disclaimer missing: {path}')
    if not re.search(r'<a\b[^>]*href=["\']'+re.escape(ARTICLE)+r'["\'][^>]*rel=["\'][^"\']*external[^"\']*noopener[^"\']*["\']',sec,re.I):
        raise SystemExit(f'Phase 92 external-link rel missing: {path}')
    canonical=BASE+path
    citations=[]
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        for node in nodes:
            if isinstance(node,dict) and node.get('url')==canonical:
                typ=node.get('@type'); types=typ if isinstance(typ,list) else [typ]
                if 'WebPage' in types or 'AboutPage' in types:
                    citations.append(node.get('citation'))
    valid=[c for c in citations if isinstance(c,dict) and c.get('@type')=='Article' and c.get('url')==ARTICLE]
    if len(valid)!=1: raise SystemExit(f'Phase 92 structured citation mismatch: {path} -> {len(valid)}')

sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
urls=re.findall(r'<loc>(.*?)</loc>',sitemap,re.I|re.S)
if len(urls)!=138 or len(set(urls))!=138: raise SystemExit(f'Phase 92 sitemap architecture changed: {len(urls)}')
print('PASS: Phase 92 audit — five Media & Partners pages visibly and structurally cite one verified external editorial reference with explicit non-endorsement disclaimer; sitemap remains 138 URLs')
