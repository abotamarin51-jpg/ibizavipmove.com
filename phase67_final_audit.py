from pathlib import Path
from urllib.parse import urlparse
from html import unescape
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG=BASE+'/#organization'
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
NOINDEX_RE=re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex',re.I)
errors=[]


def fail(msg):errors.append(msg)
def asset(url):return ROOT/urlparse(url).path.lstrip('/')
def page(path):return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'
def schemas(text):
    out=[]
    for m in SCRIPT_RE.finditer(text):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if isinstance(o,dict):out.append(o)
    return out

# 1) Global indexable-page integrity and production request shape.
indexable=[];canonicals={};titles={}
for p in ROOT.rglob('*.html'):
    text=p.read_text(encoding='utf-8')
    if NOINDEX_RE.search(text):continue
    cm=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',text,re.I)
    if not cm:continue
    canonical=cm.group(1).rstrip('/')+'/'
    rel=p.relative_to(ROOT)
    if canonical in canonicals:fail(f'duplicate canonical {canonical}: {canonicals[canonical]} / {rel}')
    canonicals[canonical]=rel
    tm=re.search(r'<title>(.*?)</title>',text,re.I|re.S)
    title=unescape(re.sub(r'<[^>]+>',' ',tm.group(1))).strip() if tm else ''
    if not title:fail(f'missing title: {rel}')
    elif title in titles:fail(f'duplicate title: {title} on {titles[title]} / {rel}')
    titles[title]=rel
    if text.lower().count('<h1')!=1:fail(f'expected one H1: {rel}')
    dm=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',text,re.I)
    if not dm or len(unescape(dm.group(1)).strip())<50:fail(f'weak meta description: {rel}')
    if 'id="main-content"' not in text:fail(f'missing main-content: {rel}')
    if 'class="ivm-skip-link"' not in text:fail(f'missing skip-link: {rel}')

    local_css=[h for h in re.findall(r'<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"',text,re.I) if urlparse(h).path.startswith('/assets/')]
    if len(local_css)!=1 or not urlparse(local_css[0]).path.startswith('/assets/bundles/'):
        fail(f'expected one CSS bundle: {rel} -> {local_css}')
    for href in local_css:
        if not asset(href).exists():fail(f'missing CSS bundle {href}: {rel}')

    if '/assets/phase46.js?v=46' in text:fail(f'obsolete phase46 runtime: {rel}')
    for tag in re.findall(r'<script\b[^>]*src="[^"]+"[^>]*></script>',text,re.I):
        sm=re.search(r'src="([^"]+)"',tag,re.I)
        if not sm:continue
        src=sm.group(1)
        if urlparse(src).path.startswith('/assets/'):
            if not asset(src).exists():fail(f'missing script {src}: {rel}')
            if urlparse(src).path.endswith('.js') and not re.search(r'\bdefer\b',tag,re.I):fail(f'non-deferred first-party script {src}: {rel}')

    for tag in re.findall(r'<img\b[^>]*>',text,re.I):
        am=re.search(r'\balt="([^"]*)"',tag,re.I)
        if not am or not am.group(1).strip():fail(f'image without alt: {rel}')
        sm=re.search(r'\bsrc="([^"]+)"',tag,re.I)
        if sm and urlparse(sm.group(1)).path.startswith('/assets/') and not asset(sm.group(1)).exists():fail(f'missing image {sm.group(1)}: {rel}')
    indexable.append((p,text,canonical))

if len(indexable)<90:fail(f'indexable page count unexpectedly low: {len(indexable)}')

# 2) Sitemap must exactly represent every indexable canonical.
sitemap=ROOT/'sitemap.xml'
if not sitemap.exists():fail('sitemap.xml missing')
else:
    try:
        ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sm_urls={x.text.rstrip('/')+'/' for x in ET.parse(sitemap).getroot().findall('s:url/s:loc',ns) if x.text}
        if sm_urls!=set(canonicals):fail(f'sitemap mismatch: sitemap={len(sm_urls)} canonicals={len(canonicals)}')
    except Exception as exc:fail(f'sitemap parse failure: {exc}')

# 3) Exactly 55 service-cluster pages with 11 reciprocal five-language clusters.
service_pages=[];clusters={}
langs={'en','es','fr','de','ar'}
for p,text,canonical in indexable:
    if 'ivm-service-finished' not in text:continue
    service_pages.append((p,text,canonical))
    alts=re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',text,re.I)
    normal={code.lower():href.rstrip('/')+'/' for code,href in alts if code.lower()!='x-default'}
    x=[href.rstrip('/')+'/' for code,href in alts if code.lower()=='x-default']
    if set(normal)!=langs or len(set(normal.values()))!=5:fail(f'incomplete service hreflang set: {p.relative_to(ROOT)}')
    if len(x)!=1 or x[0]!=normal.get('en'):fail(f'bad x-default: {p.relative_to(ROOT)}')
    key=frozenset(normal.values());clusters.setdefault(key,[]).append(canonical)

    ss=schemas(text);svc=[o for o in ss if o.get('@type')=='Service'];bread=[o for o in ss if o.get('@type')=='BreadcrumbList']
    if len(svc)!=1 or svc[0].get('url','').rstrip('/')+'/'!=canonical:fail(f'bad Service schema: {p.relative_to(ROOT)}')
    if len(bread)!=1:fail(f'bad BreadcrumbList count: {p.relative_to(ROOT)}')
    if text.count('class="ivm-related-card"')!=3:fail(f'bad related-service count: {p.relative_to(ROOT)}')
    if text.count('/assets/phase63.js?v=63')!=1:fail(f'Phase63 routing missing/duplicated: {p.relative_to(ROOT)}')
    if 'viewport-fit=cover' not in text:fail(f'mobile safe-area missing: {p.relative_to(ROOT)}')

    html_lang_m=re.search(r'<html\b[^>]*\blang="([^"]+)"',text,re.I);lang=(html_lang_m.group(1).lower().split('-')[0] if html_lang_m else 'en')
    related=re.findall(r'<a\s+class="ivm-related-card"\s+href="([^"]+)"',text,re.I)
    for href in related:
        if lang=='en':
            if re.match(r'^/(es|fr|de|ar)/',href):fail(f'English related link changes language: {p.relative_to(ROOT)} -> {href}')
        elif not href.startswith(f'/{lang}/'):fail(f'localized related link changes language: {p.relative_to(ROOT)} -> {href}')
        if not page(href).exists():fail(f'related link target missing: {p.relative_to(ROOT)} -> {href}')

if len(service_pages)!=55:fail(f'expected 55 finished service pages, found {len(service_pages)}')
if len(clusters)!=11:fail(f'expected 11 service clusters, found {len(clusters)}')
for key,members in clusters.items():
    if len(members)!=5:fail(f'cluster does not have five reciprocal pages: {sorted(members)}')

# 4) Five Private Members Desks: exact 12-option catalog and conversion routing.
contacts=['/contact/','/es/contacto/','/fr/contact/','/de/kontakt/','/ar/contact/']
for path in contacts:
    p=page(path)
    if not p.exists():fail(f'contact desk missing: {path}');continue
    text=p.read_text(encoding='utf-8')
    fm=re.search(r'<select\s+id="fService"[^>]*>(.*?)</select>',text,re.I|re.S)
    if not fm or fm.group(1).count('<option')!=12:fail(f'contact service catalog != 12: {path}')
    if text.count('/assets/phase63.js?v=63')!=1:fail(f'contact Phase63 routing missing/duplicated: {path}')
    for field in ('fName','fPhone','fArrival','fDeparture','fService','fGuests','fBrief'):
        if f'id="{field}"' not in text:fail(f'contact field missing {field}: {path}')

# 5) Five service hubs must expose an 11-item CollectionPage/ItemList.
hubs=['/services/','/es/servicios/','/fr/services/','/de/services/','/ar/services/']
for path in hubs:
    p=page(path)
    if not p.exists():fail(f'service hub missing: {path}');continue
    coll=[o for o in schemas(p.read_text(encoding='utf-8')) if o.get('@type')=='CollectionPage']
    if len(coll)!=1:fail(f'CollectionPage missing/duplicated: {path}');continue
    main=coll[0].get('mainEntity',{})
    if main.get('@type')!='ItemList' or len(main.get('itemListElement',[]))!=11:fail(f'hub ItemList != 11: {path}')

# 6) Official entity: identity, contacts and canonical 11-service OfferCatalog.
home=(ROOT/'index.html').read_text(encoding='utf-8')
orgs=[o for o in schemas(home) if o.get('@id')==ORG]
if len(orgs)!=1:fail(f'homepage organization entity count: {len(orgs)}')
else:
    org=orgs[0]
    if 'https://www.instagram.com/ibizavipmove/' not in org.get('sameAs',[]):fail('official Instagram sameAs missing')
    cps=org.get('contactPoint',[]);types={x.get('contactType') for x in cps if isinstance(x,dict)}
    if types!={'private concierge','partnerships'}:fail(f'organization contactPoint types wrong: {types}')
    catalog=org.get('hasOfferCatalog',{}).get('itemListElement',[])
    if len(catalog)!=11:fail(f'OfferCatalog != 11: {len(catalog)}')

# 7) Editorial authority/discovery resources.
bb=list((ROOT/'ibiza-intelligence').rglob('index.html')) if (ROOT/'ibiza-intelligence').exists() else []
bb=[p for p in bb if not NOINDEX_RE.search(p.read_text(encoding='utf-8'))]
if len(bb)!=7:fail(f'expected Black Book hub + 6 notes, found {len(bb)}')
robots=(ROOT/'robots.txt').read_text(encoding='utf-8') if (ROOT/'robots.txt').exists() else ''
if BASE+'/sitemap.xml' not in robots or BASE+'/image-sitemap.xml' not in robots:fail('robots sitemap discovery incomplete')
if not (ROOT/'image-sitemap.xml').exists():fail('image-sitemap.xml missing')
if not (ROOT/'llms.txt').exists():fail('llms.txt missing')

if errors:
    for e in errors:print('FAIL: '+e)
    raise SystemExit(f'Phase 67 final audit found {len(errors)} issue(s)')
print(
    f'PASS: Phase 67 FINAL AUDIT — {len(indexable)} indexable pages; 55 service landings; '
    f'11 five-language service clusters; 5 Private Members Desks; 5 eleven-service hubs; '
    f'one CSS bundle/page; first-party JS deferred; assets, sitemap, entity, Black Book and conversion paths verified.'
)
