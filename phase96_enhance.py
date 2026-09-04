from pathlib import Path

ROOT=Path('_site')

DATA={
'en':{
 'path':'/','concierge':'/private-concierge-ibiza/','intl':'/international-clients/',
 'anchor':'<p>Private chauffeur, villas, yachts, aviation, access and protection are coordinated around the stay rather than treated as isolated bookings.</p>',
 'links':'<p class="ivm-home-authority-pathways"><a class="text-link" href="/private-concierge-ibiza/">Explore Private Concierge Ibiza →</a> · <a class="text-link" href="/international-clients/">International private client support →</a></p>'},
'es':{
 'path':'/es/','concierge':'/es/concierge-privado-ibiza/','intl':'/es/clientes-internacionales/',
 'anchor':'<p>Chófer, villas, yates, aviación privada, restaurantes, nightlife, seguridad, chefs, wellness y peticiones especiales pueden gestionarse desde un único contacto en Ibiza.</p>',
 'links':'<p class="ivm-home-authority-pathways"><a class="text-link" href="/es/concierge-privado-ibiza/">Explorar Concierge Privado Ibiza →</a> · <a class="text-link" href="/es/clientes-internacionales/">Clientes internacionales y partners →</a></p>'},
'fr':{
 'path':'/fr/','concierge':'/fr/conciergerie-privee-ibiza/','intl':'/fr/clients-internationaux/',
 'old':'<a class="text-link" href="/international-clients/">International private client support →</a>',
 'new':'<p class="ivm-home-authority-pathways"><a class="text-link" href="/fr/conciergerie-privee-ibiza/">Découvrir la Conciergerie Privée Ibiza →</a> · <a class="text-link" href="/fr/clients-internationaux/">Clients internationaux et partenaires →</a></p>'},
'de':{
 'path':'/de/','concierge':'/de/privater-concierge-ibiza/','intl':'/de/internationale-kunden/',
 'old':'<a class="text-link" href="/international-clients/">International private client support →</a>',
 'new':'<p class="ivm-home-authority-pathways"><a class="text-link" href="/de/privater-concierge-ibiza/">Privaten Concierge Ibiza ansehen →</a> · <a class="text-link" href="/de/internationale-kunden/">Internationale Kunden und Partner →</a></p>'},
'ar':{
 'path':'/ar/','concierge':'/ar/private-concierge-ibiza/','intl':'/ar/international-clients/',
 'old':'<a class="text-link" href="/international-clients/">International private client support →</a>',
 'new':'<p class="ivm-home-authority-pathways"><a class="text-link" href="/ar/private-concierge-ibiza/">استكشف الكونسيرج الخاص في إيبيزا ←</a> · <a class="text-link" href="/ar/international-clients/">العملاء الدوليون والشركاء ←</a></p>'}}

def page(path):
    return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'

count=0
for lang,d in DATA.items():
    f=page(d['path'])
    if not f.exists(): raise SystemExit(f'Phase 96 home missing: {d["path"]}')
    if not page(d['concierge']).exists(): raise SystemExit(f'Phase 96 concierge target missing: {d["concierge"]}')
    if not page(d['intl']).exists(): raise SystemExit(f'Phase 96 international target missing: {d["intl"]}')
    html=f.read_text(encoding='utf-8')
    if 'ivm-home-authority-pathways' in html: raise SystemExit(f'Phase 96 duplicate pathways: {d["path"]}')
    if lang in ('en','es'):
        if d['anchor'] not in html: raise SystemExit(f'Phase 96 authority anchor missing: {d["path"]}')
        html=html.replace(d['anchor'],d['anchor']+d['links'],1)
    else:
        if d['old'] not in html: raise SystemExit(f'Phase 96 cross-language legacy link missing: {d["path"]}')
        html=html.replace(d['old'],d['new'],1)
    f.write_text(html,encoding='utf-8')
    count+=1

if count!=5: raise SystemExit(f'Phase 96 expected five homepages, changed {count}')
print('PASS: Phase 96 home authority pathways — five language homepages route contextually to same-language Private Concierge and International Client pages; FR/DE/AR English-link leakage removed')
