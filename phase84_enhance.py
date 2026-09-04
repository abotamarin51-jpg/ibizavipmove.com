from pathlib import Path
import json
import re

ROOT=Path('_site')
TARGET=ROOT/'private-concierge-ibiza'/'index.html'
TARGET_ID='https://ibizavipmove.com/private-concierge-ibiza/#service'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

if not TARGET.exists():
    raise SystemExit('Phase 84 target page missing: /private-concierge-ibiza/')

html=TARGET.read_text(encoding='utf-8')
updated=0

def patch(match):
    global updated
    try:
        obj=json.loads(match.group(2))
    except Exception:
        return match.group(0)
    if isinstance(obj,dict) and isinstance(obj.get('@graph'),list):
        candidates=[x for x in obj['@graph'] if isinstance(x,dict)]
    elif isinstance(obj,dict):
        candidates=[obj]
    else:
        candidates=[]
    changed=False
    for node in candidates:
        typ=node.get('@type')
        types=typ if isinstance(typ,list) else [typ]
        if 'Service' in types and node.get('@id')==TARGET_ID:
            node['inLanguage']='en'
            updated+=1
            changed=True
    if not changed:
        return match.group(0)
    return match.group(1)+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+match.group(3)

html=SCRIPT_RE.sub(patch,html)
if updated!=1:
    raise SystemExit(f'Phase 84 expected exactly one Private Concierge Service node, updated {updated}')
TARGET.write_text(html,encoding='utf-8')
print('PASS: Phase 84 structured-data language — Private Concierge Service explicitly normalized to inLanguage=en')

# Separate broad Luxury Concierge Ibiza intent from the narrower Private Concierge landing.
import phase85_enhance
