from pathlib import Path
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'; ORG=BASE+'/#organization'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)

DATA={
'en':{
 'path':'/about/','kicker':'Official brand information','title':'Ibiza VIP Move, verified at a glance.','labels':('Official brand','Official website','Official Instagram','Private concierge','Partnerships','Service area'),
 'values':('Ibiza VIP Move','ibizavipmove.com','@ibizavipmove','+34 600 703 303','partnership@ibizavipmove.com','Ibiza, Balearic Islands, Spain'),
 'note':'Ibiza VIP Move is a private concierge and lifestyle coordination service for Ibiza. Core requests may include chauffeur transport, villas, yachts, private aviation support, dining and nightlife, security, staffing and bespoke coordination.'},
'es':{
 'path':'/es/sobre-nosotros/','kicker':'Información oficial de la marca','title':'Ibiza VIP Move, verificado de un vistazo.','labels':('Marca oficial','Web oficial','Instagram oficial','Concierge privado','Partnerships','Área de servicio'),
 'values':('Ibiza VIP Move','ibizavipmove.com','@ibizavipmove','+34 600 703 303','partnership@ibizavipmove.com','Ibiza, Islas Baleares, España'),
 'note':'Ibiza VIP Move es un servicio de concierge privado y coordinación lifestyle en Ibiza. Las solicitudes principales pueden incluir chófer privado, villas, yates, soporte de aviación privada, dining y nightlife, seguridad, staffing y coordinación a medida.'},
'fr':{
 'path':'/fr/a-propos/','kicker':'Informations officielles de la marque','title':'Ibiza VIP Move, vérifié en un coup d’œil.','labels':('Marque officielle','Site officiel','Instagram officiel','Conciergerie privée','Partenariats','Zone de service'),
 'values':('Ibiza VIP Move','ibizavipmove.com','@ibizavipmove','+34 600 703 303','partnership@ibizavipmove.com','Ibiza, Îles Baléares, Espagne'),
 'note':'Ibiza VIP Move est un service de conciergerie privée et de coordination lifestyle à Ibiza. Les demandes principales peuvent inclure chauffeur, villas, yachts, support aviation privée, dining et nightlife, sécurité, staffing et coordination sur mesure.'},
'de':{
 'path':'/de/ueber-uns/','kicker':'Offizielle Markeninformationen','title':'Ibiza VIP Move auf einen Blick verifiziert.','labels':('Offizielle Marke','Offizielle Website','Offizielles Instagram','Privater Concierge','Partnerschaften','Servicegebiet'),
 'values':('Ibiza VIP Move','ibizavipmove.com','@ibizavipmove','+34 600 703 303','partnership@ibizavipmove.com','Ibiza, Balearen, Spanien'),
 'note':'Ibiza VIP Move ist ein privater Concierge- und Lifestyle-Koordinationsservice auf Ibiza. Zu den Kernanfragen können Chauffeur, Villen, Yachten, Private-Aviation-Support, Dining und Nightlife, Security, Staffing und individuelle Koordination gehören.'},
'ar':{
 'path':'/ar/about/','kicker':'معلومات العلامة الرسمية','title':'Ibiza VIP Move — معلومات موثقة بنظرة واحدة.','labels':('العلامة الرسمية','الموقع الرسمي','إنستغرام الرسمي','الكونسيرج الخاص','الشراكات','نطاق الخدمة'),
 'values':('Ibiza VIP Move','ibizavipmove.com','@ibizavipmove','+34 600 703 303','partnership@ibizavipmove.com','إيبيزا، جزر البليار، إسبانيا'),
 'note':'Ibiza VIP Move خدمة كونسيرج خاص وتنسيق أسلوب حياة في إيبيزا. وقد تشمل الطلبات الأساسية السائق الخاص والفلل واليخوت ودعم الطيران الخاص والمطاعم والحياة الليلية والأمن والطاقم والتنسيق المخصص.'}}

def page(path): return ROOT/path.strip('/')/'index.html'

def block(d):
    cards=[]
    for label,value in zip(d['labels'],d['values']):
        if value=='ibizavipmove.com': rendered='<a href="https://ibizavipmove.com/">ibizavipmove.com</a>'
        elif value=='@ibizavipmove': rendered='<a href="https://www.instagram.com/ibizavipmove/" rel="me external">@ibizavipmove</a>'
        elif value=='+34 600 703 303': rendered='<a href="tel:+34600703303">+34 600 703 303</a>'
        elif value=='partnership@ibizavipmove.com': rendered='<a href="mailto:partnership@ibizavipmove.com">partnership@ibizavipmove.com</a>'
        else: rendered=value
        cards.append(f'<div><span>{label}</span><strong>{rendered}</strong></div>')
    return (f'<section class="ivm-official-facts"><div class="ivm-official-facts-inner">'
            f'<div class="section-head"><div class="kicker dark">{d["kicker"]}</div><h2>{d["title"]}</h2></div>'
            f'<div class="ivm-about-role-rule">{"".join(cards)}</div><p>{d["note"]}</p></div></section>')

def patch_about(html,canonical):
    found=0
    def repl(m):
        nonlocal found
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        if not isinstance(o,dict) or o.get('@type')!='AboutPage' or o.get('url')!=canonical:return m.group(0)
        o['about']={'@id':ORG};o['mainEntity']={'@id':ORG};o['publisher']={'@id':ORG};found+=1
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    html=SCRIPT_RE.sub(repl,html)
    if found!=1:raise SystemExit(f'Phase 97 expected one AboutPage: {canonical} -> {found}')
    return html

count=0
for lang,d in DATA.items():
    f=page(d['path'])
    if not f.exists():raise SystemExit(f'Phase 97 About page missing: {d["path"]}')
    html=f.read_text(encoding='utf-8')
    if 'ivm-official-facts' in html:raise SystemExit(f'Phase 97 duplicate official facts: {d["path"]}')
    marker='<section class="closing'
    pos=html.find(marker)
    if pos<0:raise SystemExit(f'Phase 97 closing marker missing: {d["path"]}')
    html=html[:pos]+block(d)+html[pos:]
    html=patch_about(html,BASE+d['path'])
    f.write_text(html,encoding='utf-8');count+=1
if count!=5:raise SystemExit(f'Phase 97 expected 5 About pages, changed {count}')
print('PASS: Phase 97 official brand facts — five About pages expose consistent official identity, contact, service area and canonical Organization mainEntity without publishing an address')
