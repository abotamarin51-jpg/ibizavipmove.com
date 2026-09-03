from pathlib import Path
from html import unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG=BASE+'/#organization'
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
LANGS=('en','es','fr','de','ar')
HUBS={
'en':('/services/','Private Services'),
'es':('/es/servicios/','Servicios privados'),
'fr':('/fr/services/','Services privés'),
'de':('/de/services/','Private Services'),
'ar':('/ar/services/','الخدمات الخاصة')
}
CLUSTERS={
'chauffeur':{'type':'Private chauffeur and transportation in Ibiza','en':'/private-chauffeur-ibiza/','es':'/es/chauffeur-privado-ibiza/','fr':'/fr/chauffeur-prive-ibiza/','de':'/de/privater-chauffeur-ibiza/','ar':'/ar/private-chauffeur-ibiza/'},
'villas':{'type':'Luxury villas and private stays in Ibiza','en':'/luxury-villas-ibiza/','es':'/es/villas-lujo-ibiza/','fr':'/fr/villas-luxe-ibiza/','de':'/de/luxusvillen-ibiza/','ar':'/ar/luxury-villas-ibiza/'},
'yacht':{'type':'Private yacht and charter coordination in Ibiza','en':'/yacht-charter-ibiza/','es':'/es/yate-privado-ibiza/','fr':'/fr/location-yacht-ibiza/','de':'/de/yachtcharter-ibiza/','ar':'/ar/yacht-charter-ibiza/'},
'aviation':{'type':'Private aviation coordination in Ibiza','en':'/private-aviation-ibiza/','es':'/es/aviacion-privada-ibiza/','fr':'/fr/aviation-privee-ibiza/','de':'/de/private-aviation-ibiza/','ar':'/ar/private-aviation-ibiza/'},
'access':{'type':'Restaurants, beach clubs and nightlife coordination in Ibiza','en':'/restaurants-nightlife-ibiza/','es':'/es/restaurantes-nightlife-ibiza/','fr':'/fr/restaurants-nightlife-ibiza/','de':'/de/restaurants-nightlife-ibiza/','ar':'/ar/restaurants-nightlife-ibiza/'},
'security':{'type':'Private security and close protection in Ibiza','en':'/private-security-ibiza/','es':'/es/seguridad-privada-ibiza/','fr':'/fr/securite-privee-ibiza/','de':'/de/private-sicherheit-ibiza/','ar':'/ar/private-security-ibiza/'},
'chef':{'type':'Private chef and villa staffing coordination in Ibiza','en':'/private-chef-staffing-ibiza/','es':'/es/chef-privado-staffing-ibiza/','fr':'/fr/chef-prive-personnel-villa-ibiza/','de':'/de/privatkoch-villa-staff-ibiza/','ar':'/ar/private-chef-staffing-ibiza/'},
'car':{'type':'Luxury car rental coordination in Ibiza','en':'/luxury-car-rental-ibiza/','es':'/es/alquiler-coches-lujo-ibiza/','fr':'/fr/location-voiture-luxe-ibiza/','de':'/de/luxusauto-mieten-ibiza/','ar':'/ar/luxury-car-rental-ibiza/'},
'wellness':{'type':'Private wellness and beauty coordination in Ibiza','en':'/wellness-ibiza/','es':'/es/wellness-ibiza/','fr':'/fr/wellness-ibiza/','de':'/de/wellness-ibiza/','ar':'/ar/wellness-ibiza/'},
'events':{'type':'Private event coordination in Ibiza','en':'/private-events-ibiza/','es':'/es/eventos-privados-ibiza/','fr':'/fr/evenements-prives-ibiza/','de':'/de/private-events-ibiza/','ar':'/ar/private-events-ibiza/'},
'bespoke':{'type':'Bespoke private concierge coordination in Ibiza','en':'/bespoke-concierge-ibiza/','es':'/es/concierge-a-medida-ibiza/','fr':'/fr/conciergerie-sur-mesure-ibiza/','de':'/de/bespoke-concierge-ibiza/','ar':'/ar/bespoke-concierge-ibiza/'}
}


def page_for(path):return ROOT/path.strip('/')/'index.html'
def clean(value):return unescape(re.sub(r'<[^>]+>',' ',value or '')).replace('\n',' ').strip()
def canonical_of(html):
    m=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
    return m.group(1) if m else None

def remove_schema_types(html,types):
    out=[];pos=0
    for m in SCRIPT_RE.finditer(html):
        out.append(html[pos:m.start()])
        try:o=json.loads(m.group(1))
        except Exception:o=None
        typ=o.get('@type') if isinstance(o,dict) else None
        if typ not in types:out.append(m.group(0))
        pos=m.end()
    out.append(html[pos:])
    return ''.join(out)

def alternate_tags(cluster):
    tags=''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{cluster[lang]}">' for lang in LANGS)
    return tags+f'<link rel="alternate" hreflang="x-default" href="{BASE}{cluster["en"]}">'

count=0
for key,cluster in CLUSTERS.items():
    # Refuse to normalize an incomplete cluster.
    for lang in LANGS:
        if not page_for(cluster[lang]).exists():raise SystemExit(f'Phase 64 missing {key}/{lang}: {cluster[lang]}')
    tags=alternate_tags(cluster)
    for lang in LANGS:
        path=cluster[lang];file=page_for(path);html=file.read_text(encoding='utf-8')
        canonical=canonical_of(html)
        expected=BASE+path
        if canonical!=expected:raise SystemExit(f'Phase 64 canonical mismatch {path}: {canonical} != {expected}')
        title_m=re.search(r'<h1\b[^>]*>(.*?)</h1>',html,re.I|re.S)
        desc_m=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',html,re.I)
        image_m=re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"',html,re.I)
        name=clean(title_m.group(1)) if title_m else key
        desc=unescape(desc_m.group(1)).strip() if desc_m else ''
        image=image_m.group(1) if image_m else None
        if not name or len(desc)<50:raise SystemExit(f'Phase 64 weak service metadata: {path}')
        # One complete reciprocal hreflang set per service page.
        html=re.sub(r'<link[^>]+rel="alternate"[^>]*>','',html,flags=re.I)
        html=html.replace('</head>',tags+'</head>',1)
        # Replace only the top-level Service/BreadcrumbList schemas; keep FAQ/WebPage/Organization data intact.
        html=remove_schema_types(html,{'Service','BreadcrumbList'})
        hub_path,hub_name=HUBS[lang]
        service={'@context':'https://schema.org','@type':'Service','@id':canonical.rstrip('/')+'/#service','name':name,'serviceType':cluster['type'],'url':canonical,'description':desc,'inLanguage':lang,'provider':{'@id':ORG},'areaServed':{'@type':'Place','name':'Ibiza, Balearic Islands, Spain'}}
        if image:service['image']=image
        crumbs={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},{'@type':'ListItem','position':2,'name':hub_name,'item':BASE+hub_path},{'@type':'ListItem','position':3,'name':name,'item':canonical}]}
        payload='<script type="application/ld+json">'+json.dumps(service,ensure_ascii=False)+'</script><script type="application/ld+json">'+json.dumps(crumbs,ensure_ascii=False)+'</script>'
        html=html.replace('</head>',payload+'</head>',1)
        file.write_text(html,encoding='utf-8');count+=1

# Final reciprocal + schema validation across all 55 pages.
assert count==55
for key,cluster in CLUSTERS.items():
    expected={BASE+cluster[l] for l in LANGS}
    for lang in LANGS:
        path=cluster[lang];html=page_for(path).read_text(encoding='utf-8')
        alts=re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',html,re.I)
        normal={href for code,href in alts if code.lower()!='x-default'}
        x=[href for code,href in alts if code.lower()=='x-default']
        assert normal==expected,(key,lang,'hreflang',normal,expected)
        assert x==[BASE+cluster['en']],(key,lang,'x-default',x)
        found={'Service':0,'BreadcrumbList':0}
        for m in SCRIPT_RE.finditer(html):
            try:o=json.loads(m.group(1))
            except Exception:continue
            if not isinstance(o,dict):continue
            typ=o.get('@type')
            if typ=='Service':
                found['Service']+=1
                assert o.get('url')==BASE+path,(key,lang,'service url')
                assert o.get('inLanguage')==lang,(key,lang,'language')
                assert o.get('provider',{}).get('@id')==ORG,(key,lang,'provider')
            elif typ=='BreadcrumbList':
                found['BreadcrumbList']+=1
                items=o.get('itemListElement',[])
                assert len(items)==3 and items[-1].get('item')==BASE+path,(key,lang,'breadcrumbs')
        assert found=={'Service':1,'BreadcrumbList':1},(key,lang,found)
print('PASS: Phase 64 normalized self-canonicals, reciprocal hreflang, Service schema and breadcrumbs across all 55 service landings')
