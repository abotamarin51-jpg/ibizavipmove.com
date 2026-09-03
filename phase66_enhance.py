from pathlib import Path
import re
import shutil

ROOT=Path('_site')
STYLE='/assets/phase66.css?v=66'
SRC=Path('phase66.css')
DEST=ROOT/'assets'/'phase66.css'
if not SRC.exists():raise SystemExit('Phase 66 source CSS missing')
shutil.copyfile(SRC,DEST)

PAGES=[
'/private-chauffeur-ibiza/','/es/chauffeur-privado-ibiza/','/fr/chauffeur-prive-ibiza/','/de/privater-chauffeur-ibiza/','/ar/private-chauffeur-ibiza/',
'/luxury-villas-ibiza/','/es/villas-lujo-ibiza/','/fr/villas-luxe-ibiza/','/de/luxusvillen-ibiza/','/ar/luxury-villas-ibiza/',
'/yacht-charter-ibiza/','/es/yate-privado-ibiza/','/fr/location-yacht-ibiza/','/de/yachtcharter-ibiza/','/ar/yacht-charter-ibiza/',
'/private-aviation-ibiza/','/es/aviacion-privada-ibiza/','/fr/aviation-privee-ibiza/','/de/private-aviation-ibiza/','/ar/private-aviation-ibiza/',
'/restaurants-nightlife-ibiza/','/es/restaurantes-nightlife-ibiza/','/fr/restaurants-nightlife-ibiza/','/de/restaurants-nightlife-ibiza/','/ar/restaurants-nightlife-ibiza/',
'/private-security-ibiza/','/es/seguridad-privada-ibiza/','/fr/securite-privee-ibiza/','/de/private-sicherheit-ibiza/','/ar/private-security-ibiza/',
'/private-chef-staffing-ibiza/','/es/chef-privado-staffing-ibiza/','/fr/chef-prive-personnel-villa-ibiza/','/de/privatkoch-villa-staff-ibiza/','/ar/private-chef-staffing-ibiza/',
'/luxury-car-rental-ibiza/','/es/alquiler-coches-lujo-ibiza/','/fr/location-voiture-luxe-ibiza/','/de/luxusauto-mieten-ibiza/','/ar/luxury-car-rental-ibiza/',
'/wellness-ibiza/','/es/wellness-ibiza/','/fr/wellness-ibiza/','/de/wellness-ibiza/','/ar/wellness-ibiza/',
'/private-events-ibiza/','/es/eventos-privados-ibiza/','/fr/evenements-prives-ibiza/','/de/private-events-ibiza/','/ar/private-events-ibiza/',
'/bespoke-concierge-ibiza/','/es/concierge-a-medida-ibiza/','/fr/conciergerie-sur-mesure-ibiza/','/de/bespoke-concierge-ibiza/','/ar/bespoke-concierge-ibiza/'
]


def file_for(path):return ROOT/path.strip('/')/'index.html'

def add_class(html,cls):
    m=re.search(r'<body\b([^>]*)>',html,re.I)
    if not m:raise SystemExit('Phase 66 body tag missing')
    attrs=m.group(1);cm=re.search(r'class="([^"]*)"',attrs,re.I)
    if cm:
        classes=cm.group(1).split()
        if cls not in classes:classes.append(cls)
        attrs=attrs[:cm.start()]+f'class="{" ".join(classes)}"'+attrs[cm.end():]
    else:attrs+=' class="'+cls+'"'
    return html[:m.start()]+'<body'+attrs+'>'+html[m.end():]

updated=0
signature=0
for path in PAGES:
    file=file_for(path)
    if not file.exists():raise SystemExit(f'Phase 66 missing service page: {path}')
    html=file.read_text(encoding='utf-8')
    canonical_before=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
    canonical_before=canonical_before.group(1) if canonical_before else None
    html=add_class(html,'ivm-service-finished')
    if STYLE not in html:html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
    vm=re.search(r'<meta\s+name="viewport"\s+content="([^"]*)"\s*/?>',html,re.I)
    if vm and 'viewport-fit=cover' not in vm.group(1):
        content=vm.group(1).rstrip(', ')
        html=html[:vm.start()]+f'<meta name="viewport" content="{content},viewport-fit=cover">'+html[vm.end():]
    canonical_after=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
    canonical_after=canonical_after.group(1) if canonical_after else None
    if canonical_before!=canonical_after:raise SystemExit(f'Phase 66 canonical changed: {path}')
    if 'ivm-signature-inner' in html:signature+=1
    file.write_text(html,encoding='utf-8');updated+=1

assert updated==55
# Private Concierge is the seventh Phase 31 signature page, but it is not one
# of the 55 service-cluster landings. The service set therefore contains six.
assert signature==6,(signature,'expected 6 protected signature service pages')
for path in PAGES:
    html=file_for(path).read_text(encoding='utf-8')
    assert html.count('ivm-service-finished')==1,path
    assert html.count(STYLE)==1,path
    assert html.count('<h1')==1,path
    assert 'class="page-hero' in html or 'class="page-hero"' in html,path
    assert 'class="ivm-related"' in html,path
    assert html.count('class="ivm-related-card"')==3,path
    assert 'viewport-fit=cover' in html,path
    assert '<link rel="canonical"' in html,path
assert DEST.exists() and DEST.stat().st_size>3000
print(f'PASS: Phase 66 universal luxury finish applied to {updated} service landings; {signature} signature core service pages protected from heavy overrides')
