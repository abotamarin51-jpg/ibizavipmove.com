from pathlib import Path
import json,re

ROOT=Path('_site');BASE='https://ibizavipmove.com';ORG=BASE+'/#organization'
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)
PATHS=['/about/','/es/sobre-nosotros/','/fr/a-propos/','/de/ueber-uns/','/ar/about/']

for path in PATHS:
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists():raise SystemExit(f'Phase 97 audit page missing: {path}')
    html=f.read_text(encoding='utf-8')
    sections=re.findall(r'<section\b[^>]*class="[^"]*ivm-official-facts[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
    if len(sections)!=1:raise SystemExit(f'Phase 97 expected one official facts section: {path} -> {len(sections)}')
    section=sections[0]
    for needle in ('Ibiza VIP Move','ibizavipmove.com','@ibizavipmove','+34 600 703 303','partnership@ibizavipmove.com'):
        if needle not in section:raise SystemExit(f'Phase 97 visible fact missing {needle}: {path}')
    if 'Avenid Isidor' in section or 'streetAddress' in section:raise SystemExit(f'Phase 97 refuses unverified address: {path}')
    about=[]
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if isinstance(o,dict) and o.get('@type')=='AboutPage' and o.get('url')==BASE+path:about.append(o)
    if len(about)!=1:raise SystemExit(f'Phase 97 expected one AboutPage schema: {path}')
    o=about[0]
    if o.get('about',{}).get('@id')!=ORG or o.get('mainEntity',{}).get('@id')!=ORG or o.get('publisher',{}).get('@id')!=ORG:
        raise SystemExit(f'Phase 97 canonical Organization refs mismatch: {path}')

print('PASS: Phase 97 official brand facts audit — 5 localized About pages expose consistent official identity and canonical Organization references without an unverified address')
