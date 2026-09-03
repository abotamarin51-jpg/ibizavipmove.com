from pathlib import Path

ROOT=Path('_site')
SCRIPT='/assets/phase46.js?v=46'
source=Path('phase46.js')
if not source.exists():raise SystemExit('phase46.js missing')
dest=ROOT/'assets'/'phase46.js';dest.write_text(source.read_text(encoding='utf-8'),encoding='utf-8')

SERVICE_PAGES=[
'/private-chauffeur-ibiza/','/luxury-villas-ibiza/','/yacht-charter-ibiza/','/private-aviation-ibiza/','/restaurants-nightlife-ibiza/','/private-security-ibiza/',
'/es/chauffeur-privado-ibiza/','/es/villas-lujo-ibiza/','/es/yate-privado-ibiza/','/es/aviacion-privada-ibiza/','/es/seguridad-privada-ibiza/',
'/fr/chauffeur-prive-ibiza/','/fr/villas-luxe-ibiza/','/fr/location-yacht-ibiza/','/fr/aviation-privee-ibiza/','/fr/securite-privee-ibiza/',
'/de/privater-chauffeur-ibiza/','/de/luxusvillen-ibiza/','/de/yachtcharter-ibiza/','/de/private-aviation-ibiza/','/de/private-sicherheit-ibiza/',
'/ar/private-chauffeur-ibiza/','/ar/luxury-villas-ibiza/','/ar/yacht-charter-ibiza/','/ar/private-aviation-ibiza/','/ar/private-security-ibiza/'
]
CONTACT_PAGES=['/contact/','/es/contacto/','/fr/contact/','/de/kontakt/','/ar/contact/']

for path in SERVICE_PAGES+CONTACT_PAGES:
    file=ROOT/path.strip('/')/'index.html'
    if not file.exists():raise SystemExit(f'Phase 46 target missing: {path}')
    html=file.read_text(encoding='utf-8')
    tag=f'<script src="{SCRIPT}"></script>'
    if tag not in html:
        html=html.replace('</body>',tag+'</body>',1)
    file.write_text(html,encoding='utf-8')

for path in SERVICE_PAGES+CONTACT_PAGES:
    html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    assert SCRIPT in html,path
assert dest.exists() and dest.stat().st_size>1500
assert 'service=' in source.read_text(encoding='utf-8')
assert 'fService' in source.read_text(encoding='utf-8')
print(f'PASS: Phase 46 contextual service routing added to {len(SERVICE_PAGES)} service pages and {len(CONTACT_PAGES)} private desks')
