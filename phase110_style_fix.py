from pathlib import Path
import re

ROOT=Path('_site')
PHASE_STYLE='<link rel="stylesheet" href="/assets/phase110.css?v=110">'
MARKER='/* Phase 110 contextual authority flow */'
TOUCHED={
'/private-chauffeur-ibiza/','/restaurants-nightlife-ibiza/','/private-aviation-ibiza/','/private-security-ibiza/','/yacht-charter-ibiza/','/private-chef-staffing-ibiza/','/wellness-ibiza/','/destination-management-ibiza/','/international-clients/',
'/case-studies/late-night-dual-vehicle-arrival/','/case-studies/multi-day-executive-chauffeur-program/','/case-studies/principal-chauffeur-security-three-days/','/case-studies/private-aviation-arrival-seven-guests/','/case-studies/weekend-concierge-two-guests/',
'/private-concierge-marina-botafoch-ibiza/','/private-concierge-cala-jondal-es-cubells-ibiza/','/private-concierge-santa-eulalia-roca-llisa-ibiza/','/private-concierge-santa-gertrudis-ibiza/'
}

def page(path): return ROOT/path.strip('/')/'index.html'

phase_asset=ROOT/'assets'/'phase110.css'
if not phase_asset.exists(): raise SystemExit('Phase 110 temporary CSS asset missing before consolidation')
css=phase_asset.read_text(encoding='utf-8')
bundles=set()

for path in TOUCHED:
    target=page(path)
    if not target.exists(): raise SystemExit(f'Phase 110 style target missing: {path}')
    html=target.read_text(encoding='utf-8')
    if html.count(PHASE_STYLE)!=1: raise SystemExit(f'Phase 110 temporary style link mismatch: {path}')
    html=html.replace(PHASE_STYLE,'',1)
    hrefs=re.findall(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',html,re.I)
    bundle_hrefs=[h for h in hrefs if h.startswith('/assets/bundles/') and h.endswith('.css')]
    if len(bundle_hrefs)!=1: raise SystemExit(f'Phase 110 expected one existing CSS bundle: {path} -> {bundle_hrefs}')
    bundles.add(bundle_hrefs[0])
    target.write_text(html,encoding='utf-8')

for href in bundles:
    bundle=ROOT/href.lstrip('/')
    if not bundle.exists(): raise SystemExit(f'Phase 110 CSS bundle missing: {href}')
    text=bundle.read_text(encoding='utf-8')
    if MARKER not in text:
        bundle.write_text(text+'\n'+MARKER+'\n'+css+'\n',encoding='utf-8')

phase_asset.unlink()
print(f'PASS: Phase 110 style consolidation — authority-flow CSS merged into {len(bundles)} existing bundles; touched pages retain exactly one stylesheet request')
