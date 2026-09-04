from pathlib import Path
import re

ROOT=Path('_site')
DATA={
'en':('/','/private-concierge-ibiza/','/international-clients/'),
'es':('/es/','/es/concierge-privado-ibiza/','/es/clientes-internacionales/'),
'fr':('/fr/','/fr/conciergerie-privee-ibiza/','/fr/clients-internationaux/'),
'de':('/de/','/de/privater-concierge-ibiza/','/de/internationale-kunden/'),
'ar':('/ar/','/ar/private-concierge-ibiza/','/ar/international-clients/')}

def page(path):
    return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'

for lang,(home,concierge,intl) in DATA.items():
    f=page(home)
    if not f.exists(): raise SystemExit(f'Phase 96 audit home missing: {home}')
    html=f.read_text(encoding='utf-8')
    sections=re.findall(r'<p\b[^>]*class="[^"]*ivm-home-authority-pathways[^"]*"[^>]*>(.*?)</p>',html,re.I|re.S)
    if len(sections)!=1: raise SystemExit(f'Phase 96 expected one authority pathway block: {home} -> {len(sections)}')
    hrefs=re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>',sections[0],re.I)
    if hrefs!=[concierge,intl]: raise SystemExit(f'Phase 96 wrong same-language pathways: {home} -> {hrefs}')
    if not page(concierge).exists() or not page(intl).exists(): raise SystemExit(f'Phase 96 target missing from site: {home}')
    if lang!='en' and any(re.match(r'^/(?!'+re.escape(lang)+r'/)',u) for u in hrefs):
        raise SystemExit(f'Phase 96 language leak: {home} -> {hrefs}')
    if lang in ('fr','de','ar') and 'href="/international-clients/"' in html:
        raise SystemExit(f'Phase 96 legacy English international link remains: {home}')

print('PASS: Phase 96 home pathway audit — 5 homepages expose exactly two contextual same-language authority links with no FR/DE/AR English international-client leakage')
