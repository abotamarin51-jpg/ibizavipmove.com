from pathlib import Path
import json,re

ROOT=Path('_site')
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)
EXPECTED=['Ibiza, Balearic Islands, Spain','Eivissa / Ibiza Town','Marina Botafoch / Talamanca','Sant Josep de sa Talaia','Cala Jondal / Es Cubells','Santa Eulària des Riu','Roca Llisa / Cala Llonga','Sant Antoni de Portmany','Santa Gertrudis de Fruitera']
count=0
for p in ROOT.rglob('*.html'):
    html=p.read_text(encoding='utf-8')
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        for node in nodes:
            if not isinstance(node,dict):continue
            typ=node.get('@type'); types=typ if isinstance(typ,list) else [typ]
            if 'Service' not in types:continue
            url=node.get('url','')
            if not isinstance(url,str) or not url.startswith('https://ibizavipmove.com/'):continue
            count+=1
            areas=node.get('areaServed')
            if not isinstance(areas,list) or len(areas)!=9:raise SystemExit(f'Phase 94 Service areaServed mismatch: {p}')
            names=[x.get('name') for x in areas if isinstance(x,dict) and x.get('@type')=='Place']
            if names!=EXPECTED:raise SystemExit(f'Phase 94 Service area set/order mismatch: {p} -> {names}')
            if 'provider' not in node or node.get('provider',{}).get('@id')!='https://ibizavipmove.com/#organization':raise SystemExit(f'Phase 94 Service provider drift: {p}')
if count<55:raise SystemExit(f'Phase 94 expected at least 55 Service entities, found {count}')
# Visible service-area support remains present on all five language hubs.
for path in ['/services/','/es/servicios/','/fr/services/','/de/services/','/ar/services/']:
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists() or 'ivm-local-coverage' not in f.read_text(encoding='utf-8'):raise SystemExit(f'Phase 94 visible GEO support missing: {path}')
print(f'PASS: Phase 94 audit — {count} Service entities use the same Ibiza + 8 visible service areas as the Organization GEO model')
