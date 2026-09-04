from pathlib import Path
import re

ROOT=Path('_site')
TARGETS={
'en':('/private-concierge-ibiza/','Planning several services as one stay?','Explore Private Concierge Ibiza →'),
'es':('/es/concierge-privado-ibiza/','¿Necesitas coordinar varios servicios como una sola estancia?','Explorar Concierge Privado Ibiza →'),
'fr':('/fr/conciergerie-privee-ibiza/','Plusieurs services doivent fonctionner comme un seul séjour ?','Découvrir la Conciergerie Privée Ibiza →'),
'de':('/de/privater-concierge-ibiza/','Mehrere Services als einen Aufenthalt koordinieren?','Privaten Concierge Ibiza ansehen →'),
'ar':('/ar/private-concierge-ibiza/','هل تحتاج إلى تنسيق عدة خدمات ضمن إقامة واحدة؟','استكشف الكونسيرج الخاص في إيبيزا ←')}

LANG_PREFIX={'es':'/es/','fr':'/fr/','de':'/de/','ar':'/ar/'}

def lang_for(path):
    for lang,prefix in LANG_PREFIX.items():
        if path.startswith(prefix): return lang
    return 'en'

def page(path): return ROOT/path.strip('/')/'index.html'

# The 55 canonical service landings are exactly the pages protected by the FAQ layer.
service_pages=[]
for f in ROOT.rglob('index.html'):
    html=f.read_text(encoding='utf-8')
    if 'ivm-service-faq' not in html: continue
    rel='/' + str(f.relative_to(ROOT).parent).replace('\\','/').strip('/') + '/'
    service_pages.append((rel,f,html))

if len(service_pages)!=55: raise SystemExit(f'Phase 98 expected 55 service pages, found {len(service_pages)}')

changed=0
for path,f,html in service_pages:
    lang=lang_for(path); target,question,cta=TARGETS[lang]
    if not page(target).exists(): raise SystemExit(f'Phase 98 concierge target missing: {target}')
    if 'ivm-concierge-continuity' in html: raise SystemExit(f'Phase 98 duplicate bridge: {path}')
    # Every protected service landing has one conversion closing-simple section.
    # Do not require FAQ adjacency because a few localized pages have a small intermediary block.
    pattern=r'(<section class="closing-simple">.*?)(</section>)'
    m=re.search(pattern,html,re.I|re.S)
    if not m: raise SystemExit(f'Phase 98 closing section missing: {path}')
    bridge=f'<p class="ivm-concierge-continuity">{question} <a class="text-link" href="{target}">{cta}</a></p>'
    replacement=m.group(1)+bridge+m.group(2)
    html=html[:m.start()]+replacement+html[m.end():]
    f.write_text(html,encoding='utf-8');changed+=1

if changed!=55: raise SystemExit(f'Phase 98 expected 55 changes, made {changed}')
print('PASS: Phase 98 service-to-concierge authority — 55 service landings now offer one same-language contextual pathway to Private Concierge for multi-service stays')
