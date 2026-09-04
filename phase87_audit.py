from pathlib import Path
import json
import re

ROOT=Path('_site')
HOME=ROOT/'index.html'
BASE='https://ibizavipmove.com'
ORG_ID=BASE+'/#organization'
EXPECTED=['Ibiza VIP Move Concierge','ibizavipmove.com']
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)

if not HOME.exists():
    raise SystemExit('Phase 87 audit homepage missing')
html=HOME.read_text(encoding='utf-8')

websites=[]
for m in SCRIPT_RE.finditer(html):
    try:o=json.loads(m.group(1))
    except Exception:continue
    if isinstance(o,dict) and o.get('@type')=='WebSite' and o.get('url')==BASE+'/':
        websites.append(o)

if len(websites)!=1:
    raise SystemExit(f'Phase 87 expected one canonical WebSite entity, found {len(websites)}')
ws=websites[0]
if ws.get('name')!='Ibiza VIP Move':
    raise SystemExit('Phase 87 WebSite primary name mismatch')
if ws.get('alternateName')!=EXPECTED:
    raise SystemExit(f'Phase 87 alternateName mismatch: {ws.get("alternateName")}')
if (ws.get('publisher') or {}).get('@id')!=ORG_ID:
    raise SystemExit('Phase 87 WebSite publisher mismatch')
if 'property="og:site_name" content="Ibiza VIP Move"' not in html and "property='og:site_name' content='Ibiza VIP Move'" not in html:
    raise SystemExit('Phase 87 og:site_name mismatch')
if 'name="application-name" content="Ibiza VIP Move"' not in html and "name='application-name' content='Ibiza VIP Move'" not in html:
    raise SystemExit('Phase 87 application-name mismatch')

print('PASS: Phase 87 site-name audit — one canonical WebSite uses Ibiza VIP Move with two ordered Google fallback names and consistent homepage brand signals')
