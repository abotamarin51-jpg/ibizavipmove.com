from pathlib import Path
import re

ROOT=Path('_site')
SLUGS=(
'private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning',
'villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')
TARGETS={
'en':'/private-concierge-ibiza/','es':'/es/concierge-privado-ibiza/','fr':'/fr/conciergerie-privee-ibiza/',
'de':'/de/privater-concierge-ibiza/','ar':'/ar/private-concierge-ibiza/'}

def path_for(lang,slug):
    return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'

def page(path):
    return ROOT/path.strip('/')/'index.html'

count=0
for lang,target in TARGETS.items():
    if not page(target).exists(): raise SystemExit(f'Phase 95 audit target missing: {target}')
    for slug in SLUGS:
        path=path_for(lang,slug); f=page(path)
        if not f.exists(): raise SystemExit(f'Phase 95 audit article missing: {path}')
        html=f.read_text(encoding='utf-8')
        sections=re.findall(r'<section\b[^>]*class="[^"]*ivm-concierge-pathway[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
        if len(sections)!=1: raise SystemExit(f'Phase 95 expected one pathway section: {path} -> {len(sections)}')
        section=sections[0]
        hrefs=re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>',section,re.I)
        if hrefs!=[target]: raise SystemExit(f'Phase 95 wrong concierge target: {path} -> {hrefs}')
        visible=re.sub(r'<[^>]+>',' ',section)
        visible=re.sub(r'\s+',' ',visible).strip()
        if len(visible)<180: raise SystemExit(f'Phase 95 pathway too thin: {path} -> {len(visible)} chars')
        if lang=='en' and re.match(r'^/(es|fr|de|ar)/',target): raise SystemExit(f'Phase 95 English language leak: {path}')
        if lang!='en' and not target.startswith(f'/{lang}/'): raise SystemExit(f'Phase 95 language leak: {path} -> {target}')
        count+=1

if count!=30: raise SystemExit(f'Phase 95 expected 30 verified pathways, found {count}')
print('PASS: Phase 95 Black Book pathway audit — 30 article-level contextual links route to the correct same-language Private Concierge landing')
