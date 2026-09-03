from pathlib import Path
from html import unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG=BASE+'/#organization'
WEBSITE=BASE+'/#website'
LANGS=('en','es','fr','de','ar')
ARTICLE_SLUGS=('private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning','villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')
PAGE_TYPES={'WebPage','AboutPage','CollectionPage'}
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)


def article_path(lang,slug):return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'
def bb_hub(lang):return '/ibiza-intelligence/' if lang=='en' else f'/{lang}/ibiza-intelligence/'
SERVICE_HUBS={'en':'/services/','es':'/es/servicios/','fr':'/fr/services/','de':'/de/services/','ar':'/ar/services/'}
MEDIA={'en':'/media-partners/','es':'/es/media-partners/','fr':'/fr/media-partners/','de':'/de/media-partners/','ar':'/ar/media-partners/'}
OFFICE={'en':'/private-office/','es':'/es/private-office/','fr':'/fr/private-office/','de':'/de/private-office/','ar':'/ar/private-office/'}

def file_for(path):return ROOT/path.strip('/')/'index.html'

def clean(value):return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>',' ',value or ''))).strip()

def metadata(html,path):
    cm=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
    tm=re.search(r'<title>(.*?)</title>',html,re.I|re.S)
    dm=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',html,re.I)
    lm=re.search(r'<html\b[^>]*\blang="([^"]+)"',html,re.I)
    im=re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"',html,re.I)
    if not cm or not tm or not dm:raise SystemExit(f'Phase 79 metadata incomplete: {path}')
    canonical=cm.group(1).strip(); expected=BASE+path
    if canonical!=expected:raise SystemExit(f'Phase 79 canonical mismatch: {path} -> {canonical}')
    image=im.group(1).strip() if im else ''
    if image.startswith('/'):image=BASE+image
    return canonical,clean(tm.group(1)),unescape(dm.group(1)).strip(),(lm.group(1).lower().split('-')[0] if lm else 'en'),image

def strip_page_nodes(html):
    kept=[]; page_nodes=[]; pos=0
    for m in SCRIPT_RE.finditer(html):
        kept.append(html[pos:m.start()])
        try:o=json.loads(m.group(1))
        except Exception:o=None
        if isinstance(o,dict) and o.get('@type') in PAGE_TYPES:
            page_nodes.append(o)
        else:
            kept.append(m.group(0))
        pos=m.end()
    kept.append(html[pos:])
    return ''.join(kept),page_nodes

def insert_node(html,node):
    payload='<script type="application/ld+json">'+json.dumps(node,ensure_ascii=False)+'</script>'
    return html.replace('</head>',payload+'</head>',1)

def web_node(canonical,title,desc,lang,image):
    node={'@context':'https://schema.org','@type':'WebPage','@id':canonical,'url':canonical,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':WEBSITE},'about':{'@id':ORG},'publisher':{'@id':ORG}}
    if image:node['primaryImageOfPage']={'@type':'ImageObject','url':image}
    return node

def collection_node(existing,canonical,title,desc,lang,image):
    node=dict(existing)
    node.update({'@context':'https://schema.org','@type':'CollectionPage','@id':canonical.rstrip('/')+'/#collection','url':canonical,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':WEBSITE},'about':{'@id':ORG},'publisher':{'@id':ORG}})
    if image:node['primaryImageOfPage']={'@type':'ImageObject','url':image}
    return node

# 30 editorial notes: one canonical WebPage node + one Article node.
for lang in LANGS:
    for slug in ARTICLE_SLUGS:
        path=article_path(lang,slug); f=file_for(path)
        if not f.exists():raise SystemExit(f'Phase 79 article missing: {path}')
        html=f.read_text(encoding='utf-8'); canonical,title,desc,page_lang,image=metadata(html,path)
        html,_=strip_page_nodes(html)
        html=insert_node(html,web_node(canonical,title,desc,page_lang,image))
        f.write_text(html,encoding='utf-8')

# Collection hubs: preserve their ItemList but remove inherited/redundant page nodes.
for family,paths,expected_items in (
    ('services',SERVICE_HUBS,11),
    ('black-book',{lang:bb_hub(lang) for lang in LANGS},6),
):
    for lang,path in paths.items():
        f=file_for(path)
        if not f.exists():raise SystemExit(f'Phase 79 {family} hub missing: {path}')
        html=f.read_text(encoding='utf-8'); canonical,title,desc,page_lang,image=metadata(html,path)
        html,nodes=strip_page_nodes(html)
        collections=[o for o in nodes if o.get('@type')=='CollectionPage']
        if len(collections)!=1:raise SystemExit(f'Phase 79 expected one source CollectionPage: {path} -> {len(collections)}')
        main=collections[0].get('mainEntity',{})
        if main.get('@type')!='ItemList' or len(main.get('itemListElement',[]))!=expected_items:raise SystemExit(f'Phase 79 {family} ItemList mismatch: {path}')
        html=insert_node(html,collection_node(collections[0],canonical,title,desc,page_lang,image))
        f.write_text(html,encoding='utf-8')

# Media & Partners and Private Office: one canonical WebPage node; preserve all
# non-page schemas such as Service, BreadcrumbList and Organization.
for paths in (MEDIA,OFFICE):
    for lang,path in paths.items():
        f=file_for(path)
        if not f.exists():raise SystemExit(f'Phase 79 page missing: {path}')
        html=f.read_text(encoding='utf-8'); canonical,title,desc,page_lang,image=metadata(html,path)
        html,_=strip_page_nodes(html)
        html=insert_node(html,web_node(canonical,title,desc,page_lang,image))
        f.write_text(html,encoding='utf-8')

print('PASS: Phase 79 structured-data hygiene — 50 targeted pages consolidated to canonical page entities without inherited page-schema drift')
