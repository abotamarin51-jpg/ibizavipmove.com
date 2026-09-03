from pathlib import Path
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'

ARTICLES=[
('/ibiza-intelligence/private-arrival/','The Private Arrival'),
('/ibiza-intelligence/ibiza-formentera-yacht-day/','Ibiza & Formentera by Yacht'),
('/ibiza-intelligence/ibiza-august-planning/','The August Brief'),
('/ibiza-intelligence/villa-arrival-planning/','The Villa Arrival Brief'),
('/ibiza-intelligence/nightlife-transport-planning/','The Nightlife Movement Plan'),
('/ibiza-intelligence/private-aviation-ground-coordination/','From Aircraft to Ibiza'),
]

SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)

def remove_types(html,types):
    out=[];cursor=0
    for m in SCRIPT_RE.finditer(html):
        out.append(html[cursor:m.start()])
        try:obj=json.loads(m.group(1))
        except Exception:obj=None
        if not (isinstance(obj,dict) and obj.get('@type') in types):out.append(m.group(0))
        cursor=m.end()
    out.append(html[cursor:])
    return ''.join(out)

hub=ROOT/'ibiza-intelligence'/'index.html'
if not hub.exists():raise SystemExit('Black Book hub missing')
html=hub.read_text(encoding='utf-8')
html=remove_types(html,{'CollectionPage','ItemList'})
collection={
'@context':'https://schema.org','@type':'CollectionPage','@id':BASE+'/ibiza-intelligence/#collection',
'name':'The Ibiza Black Book','url':BASE+'/ibiza-intelligence/',
'description':'Private Ibiza planning intelligence covering arrivals, yachts, peak-season operations, villa logistics, nightlife movement and private aviation ground coordination.',
'isPartOf':{'@type':'WebSite','name':'Ibiza VIP Move','url':BASE+'/'},
'about':{'@type':'Place','name':'Ibiza, Spain'},
'mainEntity':{
 '@type':'ItemList','name':'The Ibiza Black Book planning notes','numberOfItems':len(ARTICLES),
 'itemListElement':[{'@type':'ListItem','position':i,'name':title,'url':BASE+path} for i,(path,title) in enumerate(ARTICLES,1)]
}}
html=html.replace('</head>',f'<script type="application/ld+json">{json.dumps(collection,ensure_ascii=False)}</script></head>',1)
hub.write_text(html,encoding='utf-8')

for path,title in ARTICLES:
    file=ROOT/path.strip('/')/'index.html'
    if not file.exists():raise SystemExit(f'Black Book article missing: {path}')
    html=file.read_text(encoding='utf-8')
    html=remove_types(html,{'BreadcrumbList'})
    breadcrumb={
      '@context':'https://schema.org','@type':'BreadcrumbList',
      'itemListElement':[
        {'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},
        {'@type':'ListItem','position':2,'name':'The Ibiza Black Book','item':BASE+'/ibiza-intelligence/'},
        {'@type':'ListItem','position':3,'name':title,'item':BASE+path},
      ]
    }
    html=html.replace('</head>',f'<script type="application/ld+json">{json.dumps(breadcrumb,ensure_ascii=False)}</script></head>',1)
    # Strengthen any existing article-like schema without changing its factual content.
    def enrich(m):
        try:obj=json.loads(m.group(1))
        except Exception:return m.group(0)
        if isinstance(obj,dict) and obj.get('@type') in ('Article','BlogPosting'):
            obj['mainEntityOfPage']={'@type':'WebPage','@id':BASE+path}
            obj['publisher']={'@type':'Organization','name':'Ibiza VIP Move','url':BASE+'/' }
            obj['author']={'@type':'Organization','name':'Ibiza VIP Move','url':BASE+'/' }
        return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>'
    html=SCRIPT_RE.sub(enrich,html)
    file.write_text(html,encoding='utf-8')

# Validation.
h=hub.read_text(encoding='utf-8')
collection_count=0
for m in SCRIPT_RE.finditer(h):
    try:o=json.loads(m.group(1))
    except Exception:continue
    if isinstance(o,dict) and o.get('@type')=='CollectionPage':
        collection_count+=1
        assert o.get('mainEntity',{}).get('numberOfItems')==6
        assert len(o.get('mainEntity',{}).get('itemListElement',[]))==6
assert collection_count==1
for path,title in ARTICLES:
    h=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    crumbs=[]
    for m in SCRIPT_RE.finditer(h):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if isinstance(o,dict) and o.get('@type')=='BreadcrumbList':crumbs.append(o)
    assert len(crumbs)==1,path
    assert len(crumbs[0]['itemListElement'])==3,path
    assert crumbs[0]['itemListElement'][-1]['name']==title,path
print('PASS: Phase 48 Black Book CollectionPage, ItemList and article breadcrumbs structured data')
