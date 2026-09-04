from pathlib import Path
from html import unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)
SECTION_RE=re.compile(r'<section\b[^>]*class=["\'][^"\']*ivm-local-coverage[^"\']*["\'][^>]*>(.*?)</section>',re.I|re.S)
CARD_RE=re.compile(r'<div\b[^>]*class=["\'][^"\']*ivm-local-area[^"\']*["\'][^>]*>',re.I)
HUBS={
'en':'/services/','es':'/es/servicios/','fr':'/fr/services/','de':'/de/services/','ar':'/ar/services/'
}
EXPECTED_PLACES={'Eivissa / Ibiza Town','Marina Botafoch / Talamanca','Sant Josep de sa Talaia','Cala Jondal / Es Cubells','Santa Eulària des Riu','Roca Llisa / Cala Llonga','Sant Antoni de Portmany','Santa Gertrudis de Fruitera'}

def clean_text(fragment):
    text=re.sub(r'<[^>]+>',' ',fragment)
    return re.sub(r'\s+',' ',unescape(text)).strip()

for lang,path in HUBS.items():
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists():raise SystemExit(f'Phase 86 audit missing hub: {path}')
    html=f.read_text(encoding='utf-8')
    sections=SECTION_RE.findall(html)
    if len(sections)!=1:raise SystemExit(f'Phase 86 expected one local coverage section: {path} -> {len(sections)}')
    section=sections[0]
    cards=CARD_RE.findall(section)
    if len(cards)!=8:raise SystemExit(f'Phase 86 expected eight local areas: {path} -> {len(cards)}')
    text=clean_text(section)
    for needle in ('Ibiza Town','Marina Botafoch','Sant Josep','Cala Jondal','Es Cubells','Santa Eulària','Sant Antoni','Santa Gertrudis'):
        if needle.lower() not in text.lower():raise SystemExit(f'Phase 86 visible area missing {needle}: {path}')

    collections=[]
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if isinstance(o,dict) and o.get('@type')=='CollectionPage':collections.append(o)
    if len(collections)!=1:raise SystemExit(f'Phase 86 expected one CollectionPage: {path}')
    coll=collections[0]
    spatial=coll.get('spatialCoverage')
    if not isinstance(spatial,list) or len(spatial)!=8:raise SystemExit(f'Phase 86 spatialCoverage mismatch: {path}')
    names={x.get('name') for x in spatial if isinstance(x,dict) and x.get('@type')=='Place'}
    if names!=EXPECTED_PLACES:raise SystemExit(f'Phase 86 spatialCoverage place set mismatch: {path} -> {names}')
    items=(coll.get('mainEntity') or {}).get('itemListElement') or []
    if len(items)!=11:raise SystemExit(f'Phase 86 service ItemList changed: {path}')
    urls=[x.get('url','') for x in items if isinstance(x,dict)]
    if len(urls)!=11:raise SystemExit(f'Phase 86 malformed service ItemList: {path}')
    if lang!='en' and not all(u.startswith(BASE+'/'+lang+'/') for u in urls):
        raise SystemExit(f'Phase 86 cross-language ItemList URL found: {path}')
    if lang=='en' and any(re.match(rf'^{re.escape(BASE)}/(?:es|fr|de|ar)/',u) for u in urls):
        raise SystemExit(f'Phase 86 localized URL leaked into English ItemList: {path}')

print('PASS: Phase 86 local Ibiza audit — 5 Services hubs expose 40 visible service-area cards and eight structured Place entities per language without cross-language service links')
