from pathlib import Path
from html import escape
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

DATA={
'en':{'path':'/private-office/','title':'Ibiza Concierge for Family Offices & Personal Assistants | Ibiza VIP Move','desc':'Ibiza concierge support for family offices, personal assistants, principals and private teams coordinating complex stays, transport, villas, yachts, aviation and security.','kicker':'Family Offices & PAs · Ibiza','h1':'Ibiza concierge support for family offices and personal assistants.','lead':'One discreet on-island coordination point for principals, families, PAs, EAs and private teams managing complex Ibiza stays from arrival to departure.','boundary':'Ibiza VIP Move provides concierge and operational coordination for private stays. We do not present this service as legal, tax, investment, fiduciary, wealth-management or formal family-office advisory.'},
'es':{'path':'/es/private-office/','title':'Concierge Ibiza para Family Offices y Personal Assistants | Ibiza VIP Move','desc':'Concierge en Ibiza para family offices, personal assistants, principals y equipos privados que coordinan estancias complejas, transporte, villas, yates, aviación y seguridad.','kicker':'Family Offices & PAs · Ibiza','h1':'Concierge en Ibiza para family offices y personal assistants.','lead':'Un único punto de coordinación discreto en la isla para principals, familias, PAs, EAs y equipos privados que gestionan estancias complejas en Ibiza.','boundary':'Ibiza VIP Move presta servicios de concierge y coordinación operativa para estancias privadas. Este servicio no se presenta como asesoramiento legal, fiscal, de inversión, fiduciario, de gestión patrimonial ni como un family office formal.'},
'fr':{'path':'/fr/private-office/','title':'Conciergerie Ibiza pour Family Offices & Personal Assistants | Ibiza VIP Move','desc':'Conciergerie à Ibiza pour family offices, personal assistants, principals et équipes privées coordonnant séjours complexes, transport, villas, yachts, aviation et sécurité.','kicker':'Family Offices & PAs · Ibiza','h1':'Conciergerie à Ibiza pour family offices et personal assistants.','lead':'Un seul point de coordination discret sur l’île pour principals, familles, PAs, EAs et équipes privées gérant des séjours complexes à Ibiza.','boundary':'Ibiza VIP Move fournit une conciergerie et une coordination opérationnelle pour les séjours privés. Ce service n’est pas présenté comme du conseil juridique, fiscal, financier, fiduciaire, patrimonial ou comme un family office formel.'},
'de':{'path':'/de/private-office/','title':'Ibiza Concierge für Family Offices & Personal Assistants | Ibiza VIP Move','desc':'Ibiza Concierge für Family Offices, Personal Assistants, Principals und private Teams zur Koordination komplexer Aufenthalte, Transport, Villen, Yachten, Aviation und Security.','kicker':'Family Offices & PAs · Ibiza','h1':'Ibiza Concierge für Family Offices und Personal Assistants.','lead':'Ein diskreter Ansprechpartner auf Ibiza für Principals, Familien, PAs, EAs und private Teams, die komplexe Aufenthalte von Ankunft bis Abreise koordinieren.','boundary':'Ibiza VIP Move bietet Concierge- und operative Koordinationsleistungen für private Aufenthalte. Dieser Service wird nicht als Rechts-, Steuer-, Investment-, Treuhand-, Vermögensberatung oder als formelles Family Office angeboten.'},
'ar':{'path':'/ar/private-office/','title':'كونسيرج إيبيزا للمكاتب العائلية والمساعدين الشخصيين | Ibiza VIP Move','desc':'خدمة كونسيرج في إيبيزا للمكاتب العائلية والمساعدين الشخصيين والضيوف الرئيسيين والفرق الخاصة لتنسيق الإقامات المعقدة والنقل والفلل واليخوت والطيران والأمن.','kicker':'Family Offices & PAs · إيبيزا','h1':'كونسيرج في إيبيزا للمكاتب العائلية والمساعدين الشخصيين.','lead':'جهة تنسيق واحدة وسرية على الجزيرة للضيوف الرئيسيين والعائلات والمساعدين والفرق الخاصة التي تدير إقامات معقدة في إيبيزا.','boundary':'تقدم Ibiza VIP Move خدمات الكونسيرج والتنسيق التشغيلي للإقامات الخاصة. ولا يتم تقديم هذه الخدمة باعتبارها استشارة قانونية أو ضريبية أو استثمارية أو ائتمانية أو لإدارة الثروات أو كمكتب عائلي رسمي.'}}

def fpath(path): return ROOT/path.strip('/')/'index.html'

def replace_one(html,pattern,repl,label):
    new,n=re.subn(pattern,repl,html,count=1,flags=re.I|re.S)
    if n!=1: raise SystemExit(f'Phase 90 expected one {label}, found {n}')
    return new

def set_meta(html,attr,name,value):
    patt=re.compile(rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>',re.I)
    tag=f'<meta {attr}="{name}" content="{escape(value,quote=True)}">'
    if patt.search(html): return patt.sub(tag,html,count=1)
    return html.replace('</head>',tag+'</head>',1)

def patch_jsonld(html,canonical,title,desc):
    def repl(m):
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        nodes=[]
        if isinstance(o,dict) and isinstance(o.get('@graph'),list): nodes=[x for x in o['@graph'] if isinstance(x,dict)]
        elif isinstance(o,dict): nodes=[o]
        changed=False
        for node in nodes:
            typ=node.get('@type'); types=typ if isinstance(typ,list) else [typ]
            if node.get('url')==canonical and any(t in ('WebPage','AboutPage','Service') for t in types):
                if 'name' in node or any(t in ('WebPage','AboutPage') for t in types): node['name']=title
                node['description']=desc; changed=True
        if not changed:return m.group(0)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    return SCRIPT_RE.sub(repl,html)

for lang,d in DATA.items():
    f=fpath(d['path'])
    if not f.exists(): raise SystemExit(f'Phase 90 missing page: {d["path"]}')
    html=f.read_text(encoding='utf-8')
    html=replace_one(html,r'<title>.*?</title>',f'<title>{d["title"]}</title>',f'{lang} title')
    for attr,name,val in [('name','description',d['desc']),('property','og:title',d['title']),('property','og:description',d['desc']),('name','twitter:title',d['title']),('name','twitter:description',d['desc'])]:
        html=set_meta(html,attr,name,val)
    html=replace_one(html,r'<div class="kicker light">.*?</div>',f'<div class="kicker light">{d["kicker"]}</div>',f'{lang} kicker')
    html=replace_one(html,r'<h1>.*?</h1>',f'<h1>{d["h1"]}</h1>',f'{lang} h1')
    # Replace only the first hero paragraph after H1.
    h1pos=html.find(f'<h1>{d["h1"]}</h1>')
    if h1pos<0: raise SystemExit(f'Phase 90 H1 position missing: {d["path"]}')
    tail=html[h1pos:]
    tail,n=re.subn(r'(<h1>.*?</h1>)\s*<p>.*?</p>',rf'\1<p>{d["lead"]}</p>',tail,count=1,flags=re.I|re.S)
    if n!=1: raise SystemExit(f'Phase 90 hero lead missing: {d["path"]}')
    html=html[:h1pos]+tail
    if 'ivm-family-office-boundary' in html: raise SystemExit(f'Phase 90 duplicate boundary: {d["path"]}')
    boundary=f'<p class="ivm-family-office-boundary"><strong>Scope:</strong> {d["boundary"]}</p>'
    marker='<section class="ivm-b2b-cta">'
    if marker not in html: raise SystemExit(f'Phase 90 CTA marker missing: {d["path"]}')
    html=html.replace(marker,boundary+marker,1)
    html=patch_jsonld(html,BASE+d['path'],d['title'],d['desc'])
    f.write_text(html,encoding='utf-8')

print('PASS: Phase 90 family-office buyer intent — five Private Office pages aligned to concierge support for Family Offices, PAs and principals with explicit scope disambiguation')
