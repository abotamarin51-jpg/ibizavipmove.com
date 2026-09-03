from pathlib import Path
from html import unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG_ID=BASE+'/#organization'
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)

PAGES={
'en':{
 'hub':('/services/','Private Services'),
 'items':[
  ('/private-chauffeur-ibiza/','Private Chauffeur & Transportation'),('/luxury-villas-ibiza/','Luxury Villas & Private Stays'),('/yacht-charter-ibiza/','Yachts & Charters'),('/restaurants-nightlife-ibiza/','Restaurants, Beach Clubs & Nightlife'),('/private-aviation-ibiza/','Private Aviation'),('/private-security-ibiza/','Security & Close Protection')]},
'es':{
 'hub':('/es/servicios/','Servicios privados'),
 'items':[
  ('/es/chauffeur-privado-ibiza/','Chófer privado'),('/es/villas-lujo-ibiza/','Villas de lujo'),('/es/yate-privado-ibiza/','Yates y charters'),('/es/aviacion-privada-ibiza/','Aviación privada'),('/es/seguridad-privada-ibiza/','Seguridad privada')]},
'fr':{
 'hub':('/fr/services/','Services privés'),
 'items':[
  ('/fr/chauffeur-prive-ibiza/','Chauffeur privé'),('/fr/villas-luxe-ibiza/','Villas de luxe'),('/fr/location-yacht-ibiza/','Yachts & charters'),('/fr/aviation-privee-ibiza/','Aviation privée'),('/fr/securite-privee-ibiza/','Sécurité privée')]},
'de':{
 'hub':('/de/services/','Private Services'),
 'items':[
  ('/de/privater-chauffeur-ibiza/','Privater Chauffeur'),('/de/luxusvillen-ibiza/','Luxusvillen'),('/de/yachtcharter-ibiza/','Yachten & Charter'),('/de/private-aviation-ibiza/','Private Aviation'),('/de/private-sicherheit-ibiza/','Private Security')]},
'ar':{
 'hub':('/ar/services/','الخدمات الخاصة'),
 'items':[
  ('/ar/private-chauffeur-ibiza/','سائق خاص'),('/ar/luxury-villas-ibiza/','فلل فاخرة'),('/ar/yacht-charter-ibiza/','يخوت وتأجير خاص'),('/ar/private-aviation-ibiza/','طيران خاص'),('/ar/private-security-ibiza/','أمن خاص')]}
}


def clean_text(value):
    return unescape(re.sub(r'<[^>]+>',' ',value or '')).replace('\n',' ').strip()

def remove_top_types(html,types):
    out=[];cursor=0
    for m in SCRIPT_RE.finditer(html):
        out.append(html[cursor:m.start()])
        try:obj=json.loads(m.group(1))
        except Exception:obj=None
        if not (isinstance(obj,dict) and obj.get('@type') in types):out.append(m.group(0))
        cursor=m.end()
    out.append(html[cursor:])
    return ''.join(out)

count=0
for lang,data in PAGES.items():
    hub_path,hub_name=data['hub']
    assert (ROOT/hub_path.strip('/')/'index.html').exists(),(lang,'hub')
    for path,fallback_name in data['items']:
        file=ROOT/path.strip('/')/'index.html'
        if not file.exists():raise SystemExit(f'Phase 49 target missing: {path}')
        html=file.read_text(encoding='utf-8')
        canonical_m=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',html,re.I)
        desc_m=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',html,re.I)
        h1_m=re.search(r'<h1\b[^>]*>(.*?)</h1>',html,re.I|re.S)
        canonical=canonical_m.group(1) if canonical_m else BASE+path
        description=unescape(desc_m.group(1)).strip() if desc_m else ''
        name=clean_text(h1_m.group(1)) if h1_m else fallback_name
        name=name or fallback_name
        html=remove_top_types(html,{'Service','BreadcrumbList'})
        service={
          '@context':'https://schema.org','@type':'Service','@id':canonical.rstrip('/')+'/#service',
          'name':name,'serviceType':fallback_name,'url':canonical,'description':description,
          'provider':{'@id':ORG_ID},
          'areaServed':{'@type':'Place','name':'Ibiza, Spain'}
        }
        crumbs={
          '@context':'https://schema.org','@type':'BreadcrumbList',
          'itemListElement':[
            {'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},
            {'@type':'ListItem','position':2,'name':hub_name,'item':BASE+hub_path},
            {'@type':'ListItem','position':3,'name':name,'item':canonical},
          ]
        }
        html=html.replace('</head>',
          '<script type="application/ld+json">'+json.dumps(service,ensure_ascii=False)+'</script>'+
          '<script type="application/ld+json">'+json.dumps(crumbs,ensure_ascii=False)+'</script></head>',1)
        file.write_text(html,encoding='utf-8');count+=1

# Validation: exactly one top-level Service and BreadcrumbList on every target.
for lang,data in PAGES.items():
    for path,_ in data['items']:
        html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
        found={'Service':0,'BreadcrumbList':0}
        for m in SCRIPT_RE.finditer(html):
            try:o=json.loads(m.group(1))
            except Exception:continue
            if isinstance(o,dict) and o.get('@type') in found:
                found[o['@type']]+=1
                if o['@type']=='Service':
                    assert o.get('provider',{}).get('@id')==ORG_ID,path
                    assert o.get('areaServed',{}).get('name')=='Ibiza, Spain',path
                else:
                    assert len(o.get('itemListElement',[]))==3,path
        assert found=={'Service':1,'BreadcrumbList':1},(path,found)
print(f'PASS: Phase 49 Service + BreadcrumbList schema added to {count} international core service pages')
