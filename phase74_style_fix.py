from pathlib import Path

ROOT=Path('_site')
STYLE='/assets/phase45.css?v=45'
PATHS=[
'/private-chef-staffing-ibiza/','/luxury-car-rental-ibiza/','/wellness-ibiza/','/private-events-ibiza/','/bespoke-concierge-ibiza/',
'/es/chef-privado-staffing-ibiza/','/es/alquiler-coches-lujo-ibiza/','/es/wellness-ibiza/','/es/eventos-privados-ibiza/','/es/concierge-a-medida-ibiza/',
'/fr/chef-prive-personnel-villa-ibiza/','/fr/location-voiture-luxe-ibiza/','/fr/wellness-ibiza/','/fr/evenements-prives-ibiza/','/fr/conciergerie-sur-mesure-ibiza/',
'/de/privatkoch-villa-staff-ibiza/','/de/luxusauto-mieten-ibiza/','/de/wellness-ibiza/','/de/private-events-ibiza/','/de/bespoke-concierge-ibiza/',
'/ar/private-chef-staffing-ibiza/','/ar/luxury-car-rental-ibiza/','/ar/wellness-ibiza/','/ar/private-events-ibiza/','/ar/bespoke-concierge-ibiza/'
]
asset=ROOT/'assets'/'phase45.css'
if not asset.exists(): raise SystemExit('Phase 74 requires Phase 45 FAQ CSS asset')
for path in PATHS:
    p=ROOT/path.strip('/')/'index.html'
    if not p.exists(): raise SystemExit(f'Phase 74 style page missing: {path}')
    html=p.read_text(encoding='utf-8')
    if STYLE not in html:
        html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
        p.write_text(html,encoding='utf-8')
for path in PATHS:
    html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    if STYLE not in html: raise SystemExit(f'Phase 74 FAQ CSS link missing: {path}')
print('PASS: Phase 74 shared FAQ styling linked to 25 lifestyle service pages')
