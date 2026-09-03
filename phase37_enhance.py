from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
WA='https://wa.me/34600703303'
TODAY='2026-09-03'
SOURCE=ROOT/'es'/'concierge-privado-ibiza'/'index.html'

SERVICES={
'villas':{
'en':'/luxury-villas-ibiza/','es':'/es/villas-lujo-ibiza/','fr':'/fr/villas-luxe-ibiza/','de':'/de/luxusvillen-ibiza/','ar':'/ar/luxury-villas-ibiza/','image':'/assets/images/villa.jpg',
'title':'Villas de lujo en Ibiza | Concierge privado | Ibiza VIP Move',
'desc':'Villas de lujo en Ibiza con coordinación privada de llegada, estancia, personal, chófer y servicios lifestyle a través de Ibiza VIP Move.',
'kicker':'Estancia privada · Ibiza','h1':'Villas de lujo en Ibiza, coordinadas alrededor de tu estancia.','lead':'Una villa privada no es solo un alojamiento. Llegada, acceso, transporte, personal y ritmo de la estancia deben funcionar como una sola experiencia.','section':'La estancia empieza antes de llegar.','large':'Coordinamos los detalles prácticos alrededor de la villa para que la llegada y los días posteriores sean más fluidos.','items':[('01','Brief de villa','Fechas, huéspedes, ubicación, acceso y prioridades de la estancia.'),('02','Pre-arrival','Horarios, llegada, chófer y necesidades prácticas alineadas antes de aterrizar.'),('03','Durante la estancia','Chófer, personal, wellness, dining y peticiones lifestyle pueden coordinarse en conjunto.'),('04','Adaptar','Si cambia el planning, revisamos los elementos afectados alrededor del nuevo brief.')], 'cta':'Solicitar villa privada'},
'yacht':{
'en':'/yacht-charter-ibiza/','es':'/es/yate-privado-ibiza/','fr':'/fr/location-yacht-ibiza/','de':'/de/yachtcharter-ibiza/','ar':'/ar/yacht-charter-ibiza/','image':'/assets/images/yacht.jpg',
'title':'Yate privado Ibiza y Formentera | Ibiza VIP Move','desc':'Yate privado y charter en Ibiza y Formentera con coordinación de marina, chófer, catering y planning por Ibiza VIP Move.',
'kicker':'Yate privado · Ibiza & Formentera','h1':'Un día de yate integrado en tu itinerario.','lead':'Yate, marina, transporte terrestre y el resto del día se coordinan alrededor del mismo planning.','section':'De la villa a bordo, sin fricción.','large':'Un buen día en el mar también depende de lo que ocurre antes de embarcar y después de volver a tierra.','items':[('01','Brief de mar','Fecha, huéspedes, preferencias, timing y tipo de día deseado.'),('02','Marina','Punto de salida, horario y detalles prácticos confirmados previamente.'),('03','A bordo','Catering y necesidades confirmadas alineadas con el charter.'),('04','Regreso','Chófer, cena o programa nocturno pueden coordinarse alrededor de la hora de regreso.')], 'cta':'Solicitar yate privado'},
'aviation':{
'en':'/private-aviation-ibiza/','es':'/es/aviacion-privada-ibiza/','fr':'/fr/aviation-privee-ibiza/','de':'/de/private-aviation-ibiza/','ar':'/ar/private-aviation-ibiza/','image':'/assets/images/aviation.jpg',
'title':'Aviación privada Ibiza | Coordinación en tierra | Ibiza VIP Move','desc':'Aviación privada en Ibiza con coordinación de vuelo, equipaje, chófer y traslado a villa u hotel a través de Ibiza VIP Move.',
'kicker':'Aviación privada · Ibiza','h1':'Del vuelo al transporte terrestre, bajo un solo brief.','lead':'Conectamos llegada o salida con equipaje, vehículos, destino y timing para que la operación terrestre continúe sin fricción.','section':'El vuelo es solo una parte de la llegada.','large':'Coordinamos la aviación privada con el movimiento terrestre para reducir conversaciones separadas y mantener el itinerario alineado.','items':[('01','Vuelo','Timing, pasajeros, equipaje y destino claramente definidos.'),('02','Llegada','Necesidades operativas alrededor de la llegada coordinadas con antelación.'),('03','Vehículos','Capacidad de pasajeros y equipaje considerados dentro del mismo plan.'),('04','Continuación','Villa, hotel, seguridad u otros servicios pueden alinearse alrededor de la llegada.')], 'cta':'Solicitar coordinación de aviación'},
'security':{
'en':'/private-security-ibiza/','es':'/es/seguridad-privada-ibiza/','fr':'/fr/securite-privee-ibiza/','de':'/de/private-sicherheit-ibiza/','ar':'/ar/private-security-ibiza/','image':'/assets/images/security.jpg',
'title':'Seguridad privada Ibiza | Close Protection | Ibiza VIP Move','desc':'Seguridad privada y close protection en Ibiza con coordinación discreta de movimientos, ubicaciones y horarios alrededor del cliente.',
'kicker':'Seguridad privada · Ibiza','h1':'Seguridad privada integrada discretamente en la estancia.','lead':'Las necesidades de protección se coordinan alrededor del cliente, sus movimientos, ubicaciones y el planning confirmado.','section':'La protección funciona mejor dentro del contexto correcto.','large':'Transporte, lugares, horarios y requisitos privados pueden considerarse juntos para evitar una coordinación fragmentada.','items':[('01','Brief de seguridad','Principal, huéspedes, planning y contexto operativo.'),('02','Movimientos','Los trayectos confirmados pueden alinearse con las necesidades de protección.'),('03','Ubicaciones','Se aclaran los detalles relevantes de villas, eventos o nightlife según necesidad.'),('04','Discreción','La información sensible se limita a las personas necesarias para ejecutar el servicio confirmado.')], 'cta':'Solicitar seguridad privada'}
}


def hreflangs(s):
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{s[lang]}">' for lang in ('en','es','fr','de','ar')) + f'<link rel="alternate" hreflang="x-default" href="{BASE}{s["en"]}">'


def main(s):
    cards=''.join(f'<article><span>{n}</span><h3>{escape(t)}</h3><p>{escape(c)}</p></article>' for n,t,c in s['items'])
    return f'''<main id="main-content"><section class="page-hero"><div class="page-hero-media"><img src="{s['image']}" alt="{escape(s['h1'])} — Ibiza VIP Move" width="1800" height="1200" fetchpriority="high" decoding="async"></div><div><div class="kicker light">{escape(s['kicker'])}</div><h1>{escape(s['h1'])}</h1><p>{escape(s['lead'])}</p><a class="btn gold" href="{WA}">{escape(s['cta'])}</a></div></section><section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>{escape(s['section'])}</h2></div><div><p class="large">{escape(s['large'])}</p></div></section><section class="process"><div class="section-head"><div class="kicker dark">Coordinación privada</div><h2>{escape(s['section'])}</h2></div><div class="process-grid">{cards}</div></section><section class="closing-simple"><h2>{escape(s['cta'])}</h2><p>Ibiza VIP Move · Atención privada · Ibiza</p><a class="btn dark" href="{WA}">{escape(s['cta'])}</a></section></main>'''


def update_jsonld(html,canonical,s):
    patt=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
    def repl(m):
        try:o=json.loads(m.group(1))
        except:return m.group(0)
        if not isinstance(o,dict):return m.group(0)
        if o.get('@type')=='WebPage':
            o['name']=s['title'];o['url']=canonical;o['description']=s['desc'];o['inLanguage']='es';o['primaryImageOfPage']={'@type':'ImageObject','url':BASE+s['image']}
        elif o.get('@type')=='Service':
            o['url']=canonical;o['areaServed']={'@type':'Place','name':'Ibiza, Spain'};o['image']=BASE+s['image']
        return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
    return patt.sub(repl,html)

if not SOURCE.exists():raise SystemExit('Spanish Phase 37 source page missing')
source=SOURCE.read_text(encoding='utf-8')
created=[]
for key,s in SERVICES.items():
    canonical=BASE+s['es'];html=source
    html=re.sub(r'<title>.*?</title>',f'<title>{escape(s["title"])}</title>',html,count=1,flags=re.I|re.S)
    html=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(s['desc'])+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<link[^>]+rel="alternate"[^>]*>','',html,flags=re.I)
    html=re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")',lambda m:m.group(1)+canonical+m.group(2),html,count=1,flags=re.I)
    for prop,val in [('og:title',s['title']),('og:description',s['desc']),('og:url',canonical),('og:image',BASE+s['image'])]:
        html=re.sub(rf'(<meta\s+property="{re.escape(prop)}"\s+content=")[^"]*(")',lambda m,v=val:m.group(1)+escape(v)+m.group(2),html,count=1,flags=re.I)
    html=re.sub(r'<main\b[^>]*>.*?</main>',main(s),html,count=1,flags=re.I|re.S)
    html=update_jsonld(html,canonical,s)
    html=html.replace('</head>',hreflangs(s)+'</head>',1)
    dest=ROOT/s['es'].strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8');created.append((key,s))

# Refresh reciprocal hreflang on all five language versions now that Spanish exists.
for key,s in SERVICES.items():
    tags=hreflangs(s)
    for lang in ('en','es','fr','de','ar'):
        p=ROOT/s[lang].strip('/')/'index.html'
        if not p.exists():raise SystemExit(f'Missing language sibling {lang} for {key}')
        html=p.read_text(encoding='utf-8');html=re.sub(r'<link[^>]+rel="alternate"[^>]*>','',html,flags=re.I);html=html.replace('</head>',tags+'</head>',1);p.write_text(html,encoding='utf-8')

# Sitemap.
sitemap=ROOT/'sitemap.xml';ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9');tree=ET.parse(sitemap);root=tree.getroot();ns='http://www.sitemaps.org/schemas/sitemap/0.9';existing={u.find(f'{{{ns}}}loc').text for u in root.findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for _,s in created:
    url=BASE+s['es']
    if url not in existing:
        u=ET.SubElement(root,f'{{{ns}}}url');ET.SubElement(u,f'{{{ns}}}loc').text=url;ET.SubElement(u,f'{{{ns}}}lastmod').text=TODAY;ET.SubElement(u,f'{{{ns}}}changefreq').text='monthly';ET.SubElement(u,f'{{{ns}}}priority').text='0.8'
tree.write(sitemap,encoding='utf-8',xml_declaration=True)

# Image sitemap.
imgmap=ROOT/'image-sitemap.xml'
if imgmap.exists():
    SM='http://www.sitemaps.org/schemas/sitemap/0.9';IMG='http://www.google.com/schemas/sitemap-image/1.1';ET.register_namespace('',SM);ET.register_namespace('image',IMG);it=ET.parse(imgmap);ir=it.getroot();ex={u.find(f'{{{SM}}}loc').text for u in ir.findall(f'{{{SM}}}url') if u.find(f'{{{SM}}}loc') is not None}
    for _,s in created:
        url=BASE+s['es']
        if url not in ex:
            u=ET.SubElement(ir,f'{{{SM}}}url');ET.SubElement(u,f'{{{SM}}}loc').text=url;im=ET.SubElement(u,f'{{{IMG}}}image');ET.SubElement(im,f'{{{IMG}}}loc').text=BASE+s['image']
    it.write(imgmap,encoding='utf-8',xml_declaration=True)

llms=ROOT/'llms.txt'
if llms.exists():
    text=llms.read_text(encoding='utf-8')
    if '/es/villas-lujo-ibiza/' not in text:
        text+='\n## Servicios principales en español\n'+ '\n'.join(f'- [{s["h1"]}]({BASE}{s["es"]})' for _,s in created)+'\n';llms.write_text(text,encoding='utf-8')

assert len(created)==4
for key,s in created:
    html=(ROOT/s['es'].strip('/')/'index.html').read_text(encoding='utf-8');assert html.count('<h1')==1;assert BASE+s['es'] in html;assert 'hreflang="fr"' in html and 'hreflang="de"' in html and 'hreflang="ar"' in html;assert 'id="main-content"' in html and 'ivm-skip-link' in html
print('PASS: Phase 37 created 4 Spanish core-service pages and completed five-language hreflang clusters')
