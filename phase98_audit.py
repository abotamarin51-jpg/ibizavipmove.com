from pathlib import Path
import re

ROOT=Path('_site')
TARGETS={
'en':'/private-concierge-ibiza/','es':'/es/concierge-privado-ibiza/','fr':'/fr/conciergerie-privee-ibiza/','de':'/de/privater-concierge-ibiza/','ar':'/ar/private-concierge-ibiza/'}
PREFIX={'es':'/es/','fr':'/fr/','de':'/de/','ar':'/ar/'}

def lang_for(path):
    for lang,prefix in PREFIX.items():
        if path.startswith(prefix): return lang
    return 'en'

def page(path): return ROOT/path.strip('/')/'index.html'

count=0
for f in ROOT.rglob('index.html'):
    html=f.read_text(encoding='utf-8')
    if 'ivm-service-faq' not in html: continue
    path='/' + str(f.relative_to(ROOT).parent).replace('\\','/').strip('/') + '/'
    lang=lang_for(path); target=TARGETS[lang]
    blocks=re.findall(r'<p\b[^>]*class="[^"]*ivm-concierge-continuity[^"]*"[^>]*>(.*?)</p>',html,re.I|re.S)
    if len(blocks)!=1: raise SystemExit(f'Phase 98 expected one continuity bridge: {path} -> {len(blocks)}')
    hrefs=re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>',blocks[0],re.I)
    if hrefs!=[target]: raise SystemExit(f'Phase 98 wrong concierge target: {path} -> {hrefs}')
    if not page(target).exists(): raise SystemExit(f'Phase 98 missing target: {target}')
    # The bridge must remain inside the conversion closing-simple section, not global navigation/footer.
    closings=re.findall(r'<section class="closing-simple">(.*?)</section>',html,re.I|re.S)
    if len(closings)!=1 or 'ivm-concierge-continuity' not in closings[0]: raise SystemExit(f'Phase 98 bridge left conversion context: {path}')
    if lang!='en' and not target.startswith(f'/{lang}/'): raise SystemExit(f'Phase 98 language leak: {path} -> {target}')
    count+=1

if count!=55: raise SystemExit(f'Phase 98 expected 55 verified bridges, found {count}')
print('PASS: Phase 98 service-to-concierge audit — 55 conversion CTAs contain exactly one same-language Private Concierge pathway for multi-service coordination')
