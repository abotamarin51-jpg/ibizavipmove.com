from pathlib import Path
import json,re

ROOT=Path('_site'); ORG='https://ibizavipmove.com/#organization'
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
            if not isinstance(node,dict) or node.get('@id')!=ORG or node.get('@type')!='Organization': continue
            count+=1
            if 'address' in node: raise SystemExit(f'Phase 91 Organization must not publish address: {p}')
            areas=node.get('areaServed')
            if not isinstance(areas,list) or len(areas)!=9: raise SystemExit(f'Phase 91 areaServed mismatch: {p}')
            names=[x.get('name') for x in areas if isinstance(x,dict) and x.get('@type')=='Place']
            if names!=EXPECTED: raise SystemExit(f'Phase 91 service-area set/order mismatch: {p} -> {names}')
            cps=node.get('contactPoint') or []
            if not isinstance(cps,list) or not cps: raise SystemExit(f'Phase 91 missing contact points: {p}')
            for cp in cps:
                area=cp.get('areaServed') if isinstance(cp,dict) else None
                if not isinstance(area,dict) or area.get('name')!='Ibiza, Balearic Islands, Spain': raise SystemExit(f'Phase 91 contactPoint area mismatch: {p}')
if count<50: raise SystemExit(f'Phase 91 expected at least 50 Organization entities, found {count}')
# Visible support exists on the five service hubs created in Phase 86.
for path in ['/services/','/es/servicios/','/fr/services/','/de/services/','/ar/services/']:
    f=ROOT/path.strip('/')/'index.html'
    html=f.read_text(encoding='utf-8')
    if 'ivm-local-coverage' not in html: raise SystemExit(f'Phase 91 visible service-area support missing: {path}')
print(f'PASS: Phase 91 audit — {count} Organization entities use Ibiza + 8 visible service areas and contact-point Ibiza coverage, with no physical address')
