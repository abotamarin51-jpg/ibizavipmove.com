from pathlib import Path
import json
import re

ROOT=Path('_site')
HOME=ROOT/'index.html'
BASE='https://ibizavipmove.com'
WEBSITE_ID=BASE+'/#website'
ORG_ID=BASE+'/#organization'
ALTERNATES=['Ibiza VIP Move Concierge','ibizavipmove.com']
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

if not HOME.exists():
    raise SystemExit('Phase 87 homepage missing')

html=HOME.read_text(encoding='utf-8')
found=0

def patch(match):
    global found
    try:
        obj=json.loads(match.group(2))
    except Exception:
        return match.group(0)
    if not isinstance(obj,dict) or obj.get('@type')!='WebSite':
        return match.group(0)
    if obj.get('url')!=BASE+'/':
        return match.group(0)
    obj['@id']=WEBSITE_ID
    obj['name']='Ibiza VIP Move'
    obj['alternateName']=ALTERNATES
    obj['publisher']={'@id':ORG_ID}
    found+=1
    return match.group(1)+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+match.group(3)

html=SCRIPT_RE.sub(patch,html)
if found!=1:
    raise SystemExit(f'Phase 87 expected one canonical WebSite entity, found {found}')
HOME.write_text(html,encoding='utf-8')

print('PASS: Phase 87 Google site name — Ibiza VIP Move WebSite enriched with ordered alternateName fallbacks')
