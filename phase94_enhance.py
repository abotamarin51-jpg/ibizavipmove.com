from pathlib import Path
import json,re

ROOT=Path('_site')
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
changed=0
for p in ROOT.rglob('*.html'):
    html=p.read_text(encoding='utf-8')
    def repl(m):
        global changed
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        touched=False
        for node in nodes:
            if not isinstance(node,dict):continue
            typ=node.get('@type'); types=typ if isinstance(typ,list) else [typ]
            if 'Service' not in types:continue
            url=node.get('url','')
            if not isinstance(url,str) or not url.startswith('https://ibizavipmove.com/'):continue
            node['areaServed']=AREAS
            touched=True;changed+=1
        if not touched:return m.group(0)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    new=SCRIPT_RE.sub(repl,html)
    if new!=html:p.write_text(new,encoding='utf-8')
if changed<55:raise SystemExit(f'Phase 94 expected at least 55 Service entities, changed {changed}')
print(f'PASS: Phase 94 Service GEO consistency — {changed} Service entities aligned to Ibiza plus eight visible service areas')
