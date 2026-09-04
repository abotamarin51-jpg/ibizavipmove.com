from pathlib import Path

ROOT=Path('_site'); LLMS=ROOT/'llms.txt'
if not LLMS.exists(): raise SystemExit('Phase 93 audit llms.txt missing')
text=LLMS.read_text(encoding='utf-8')
required=[
 'Primary service area: Ibiza, Balearic Islands, Spain',
 'Eivissa / Ibiza Town',
 'Marina Botafoch / Talamanca',
 'Sant Josep de sa Talaia',
 'Cala Jondal / Es Cubells',
 'Santa Eulària des Riu',
 'Roca Llisa / Cala Llonga',
 'Sant Antoni de Portmany',
 'Santa Gertrudis de Fruitera',
 'Ibiza concierge and operational support for principals, families, personal assistants, executive assistants, family offices and private teams',
 'not presented as a legal, tax, investment, fiduciary, wealth-management or formal family-office advisory service',
 'https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/',
 'does not imply endorsement or partnership',
 'https://www.instagram.com/ibizavipmove/',
 'https://ibizavipmove.com/#organization',
 'not guaranteed until specifically confirmed']
for needle in required:
    if needle not in text: raise SystemExit(f'Phase 93 missing GEO source-of-truth statement: {needle}')
if text.count('## Verified external reference')!=1: raise SystemExit('Phase 93 external reference section count mismatch')
if text.count('## Official identity')!=1: raise SystemExit('Phase 93 official identity section count mismatch')
if text.count('## Machine-readable discovery')!=1: raise SystemExit('Phase 93 machine discovery section count mismatch')
if 'Ibiza Private Drivers' in text: raise SystemExit('Phase 93 must not mix Ibiza Private Drivers into Ibiza VIP Move identity')
print('PASS: Phase 93 audit — llms.txt reflects current Ibiza VIP Move buyer scope, local service geography, official identity and verified external reference without brand mixing')
