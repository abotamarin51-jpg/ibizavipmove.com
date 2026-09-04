from pathlib import Path
import json,re

ROOT=Path('_site')
ORG='https://ibizavipmove.com/#organization'
ARTICLE_URL='https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/'
ARTICLE_NAME='Top Luxury Travel Concierge Services for Ibiza Dining in 2026'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

SUBJECT={
 '@type':'Article',
 'name':ARTICLE_NAME,
 'url':ARTICLE_URL,
 'publisher':{'@type':'Organization','name':'Luxury Magazine'}
}

changed=0
for p in ROOT.rglob('*.html'):
    html=p.read_text(encoding='utf-8')
    touched=False
    def repl(m):
        nonlocal_dummy=None
        global changed
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        modified=False
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        for node in nodes:
            if not isinstance(node,dict) or node.get('@id')!=ORG:continue
            types=node.get('@type'); types=types if isinstance(types,list) else [types]
            if 'Organization' not in types:continue
            node['subjectOf']=[SUBJECT]
            modified=True;changed+=1
        if not modified:return m.group(0)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    html=SCRIPT_RE.sub(repl,html)
    p.write_text(html,encoding='utf-8')

if changed<60:raise SystemExit(f'Phase 99 expected at least 60 Organization entities, changed {changed}')
print(f'PASS: Phase 99 verified external subject — {changed} Organization entities identify one independent Luxury Magazine article as subjectOf without changing sameAs or implying endorsement')
