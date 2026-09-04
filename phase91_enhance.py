from pathlib import Path
import json,re

ROOT=Path('_site'); ORG='https://ibizavipmove.com/#organization'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)
AREAS=[
 {'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},
 {'@type':'Place','name':'Eivissa / Ibiza Town'},
 {'@type':'Place','name':'Marina Botafoch / Talamanca'},
 {'@type':'Place','name':'Sant Josep de sa Talaia'},
 {'@type':'Place','name':'Cala Jondal / Es Cubells'},
 {'@type':'Place','name':'Santa Eulària des Riu'},
 {'@type':'Place','name':'Roca Llisa / Cala Llonga'},
 {'@type':'Place','name':'Sant Antoni de Portmany'},
 {'@type':'Place','name':'Santa Gertrudis de Fruitera'}]
changed_total=0
for p in ROOT.rglob('*.html'):
    html=p.read_text(encoding='utf-8')
    def repl(m):
        global changed_total
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        changed=False
        for node in nodes:
            if isinstance(node,dict) and node.get('@id')==ORG and node.get('@type')=='Organization':
                node['areaServed']=AREAS
                # Keep contact points geographically consistent without publishing an address.
                cps=node.get('contactPoint')
                if isinstance(cps,list):
                    for cp in cps:
                        if isinstance(cp,dict): cp['areaServed']={'@type':'Place','name':'Ibiza, Balearic Islands, Spain'}
                if 'address' in node: raise SystemExit(f'Phase 91 refuses Organization address on {p}')
                changed=True; changed_total+=1
        if not changed:return m.group(0)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    new=SCRIPT_RE.sub(repl,html)
    if new!=html:p.write_text(new,encoding='utf-8')
if changed_total<50: raise SystemExit(f'Phase 91 expected broad Organization coverage, changed only {changed_total}')
print(f'PASS: Phase 91 GEO entity coverage — {changed_total} Organization entities aligned to Ibiza plus eight visible service areas without publishing a physical address')
