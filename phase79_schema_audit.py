from pathlib import Path
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'; LANGS=('en','es','fr','de','ar')
ARTICLE_SLUGS=('private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning','villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')
PAGE_TYPES={'WebPage','AboutPage','CollectionPage'}
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
NOINDEX_RE=re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex',re.I)

def article_path(lang,slug):return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'
def bb_hub(lang):return '/ibiza-intelligence/' if lang=='en' else f'/{lang}/ibiza-intelligence/'
SERVICE_HUBS={'en':'/services/','es':'/es/servicios/','fr':'/fr/services/','de':'/de/services/','ar':'/ar/services/'}
MEDIA={'en':'/media-partners/','es':'/es/media-partners/','fr':'/fr/media-partners/','de':'/de/media-partners/','ar':'/ar/media-partners/'}
OFFICE={'en':'/private-office/','es':'/es/private-office/','fr':'/fr/private-office/','de':'/de/private-office/','ar':'/ar/private-office/'}
def page(path):return ROOT/path.strip('/')/'index.html'
def objs(html):
 out=[]
 for m in SCRIPT_RE.finditer(html):
  try:o=json.loads(m.group(1))
  except Exception:continue
  if isinstance(o,dict):out.append(o)
 return out

def canonical(html):
 m=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
 return m.group(1) if m else ''

# Global rule: any top-level page-type node carrying a URL must describe the
# canonical page it is embedded on. This catches inherited source-page schemas.
checked=0
for f in ROOT.rglob('*.html'):
 html=f.read_text(encoding='utf-8')
 if NOINDEX_RE.search(html):continue
 can=canonical(html)
 if not can:continue
 for o in objs(html):
  if o.get('@type') in PAGE_TYPES and o.get('url') and o.get('url').rstrip('/')!=can.rstrip('/'):
   raise SystemExit(f'Phase 79 audit inherited page URL on {f.relative_to(ROOT)}: {o.get("@type")} -> {o.get("url")} vs {can}')
 checked+=1

# 30 notes: exactly one canonical WebPage + one Article.
for lang in LANGS:
 for slug in ARTICLE_SLUGS:
  path=article_path(lang,slug); html=page(path).read_text(encoding='utf-8'); can=BASE+path; data=objs(html)
  pages=[o for o in data if o.get('@type') in PAGE_TYPES]
  arts=[o for o in data if o.get('@type')=='Article']
  if len(pages)!=1 or pages[0].get('@type')!='WebPage':raise SystemExit(f'Phase 79 audit article page-node count: {path}')
  if pages[0].get('url')!=can or pages[0].get('@id')!=can:raise SystemExit(f'Phase 79 audit article WebPage identity: {path}')
  if len(arts)!=1 or arts[0].get('mainEntityOfPage',{}).get('@id')!=can:raise SystemExit(f'Phase 79 audit Article/WebPage link: {path}')

# Ten Collection hubs: CollectionPage only, preserving ItemList cardinality.
for paths,items in ((SERVICE_HUBS,11),({lang:bb_hub(lang) for lang in LANGS},6)):
 for lang,path in paths.items():
  html=page(path).read_text(encoding='utf-8'); can=BASE+path; data=objs(html)
  pages=[o for o in data if o.get('@type') in PAGE_TYPES]
  if len(pages)!=1 or pages[0].get('@type')!='CollectionPage':raise SystemExit(f'Phase 79 audit CollectionPage count: {path}')
  coll=pages[0]
  if coll.get('url')!=can or coll.get('@id')!=can.rstrip('/')+'/#collection':raise SystemExit(f'Phase 79 audit collection identity: {path}')
  main=coll.get('mainEntity',{})
  if main.get('@type')!='ItemList' or len(main.get('itemListElement',[]))!=items:raise SystemExit(f'Phase 79 audit collection items: {path}')

# Media and Private Office: one canonical WebPage; other non-page schemas remain allowed.
for paths in (MEDIA,OFFICE):
 for lang,path in paths.items():
  html=page(path).read_text(encoding='utf-8'); can=BASE+path
  pages=[o for o in objs(html) if o.get('@type') in PAGE_TYPES]
  if len(pages)!=1 or pages[0].get('@type')!='WebPage' or pages[0].get('url')!=can or pages[0].get('@id')!=can:
   raise SystemExit(f'Phase 79 audit canonical WebPage mismatch: {path}')

print(f'PASS: Phase 79 schema audit — {checked} indexable pages contain no inherited page URLs; 30 articles, 10 collection hubs and 10 B2B pages have canonical page identities')
