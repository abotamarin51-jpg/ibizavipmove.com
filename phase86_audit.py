from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)
HUBS={
'en':'/services/','es':'/es/servicios/','fr':'/fr/services/','de':'/de/services/','ar':'/ar/services/'
}
EXPECTED_PLACES={'Eivissa / Ibiza Town','Marina Botafoch / Talamanca','Sant Josep de sa Talaia','Cala Jondal / Es Cubells','Santa Eulària des Riu','Roca Llisa / Cala Llonga','Sant Antoni de Portmany','Santa Gertrudis de Fruitera'}

for lang,path in HUBS.items():
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists():raise SystemExit(f'Phase 86 audit missing hub: {path}')
    html=f.read_text(encoding='utf-8')
    soup=BeautifulSoup(html,'html.parser')
    sections=soup.select('section.ivm-local-coverage')
    if len(sections)!=1:raise SystemExit(f'Phase 86 expected one local coverage section: {path} -> {len(sections)}')
    cards=sections[0].select('.ivm-local-area')
    if len(cards)!=8:raise SystemExit(f'Phase 86 expected eight local areas: {path} -> {len(cards)}')
    text=' '.join(sections[0].stripped_strings)
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
    if lang!='en' and not all(u.startswith(BASE+'/'+lang+'/') for u in urls):
        # Spanish hub uses /es/servicios/ but all service landings still use /es/.
        raise SystemExit(f'Phase 86 cross-language ItemList URL found: {path}')

print('PASS: Phase 86 local Ibiza audit — 5 Services hubs expose 40 visible service-area cards and eight structured Place entities per language without cross-language service links')
