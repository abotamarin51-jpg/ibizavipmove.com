from pathlib import Path
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
LANGS=('en','es','fr','de','ar')
SLUGS=(None,'private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning','villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')
errors=[]

def url(lang,slug=None):
    if lang=='en': return '/ibiza-intelligence/' if slug is None else f'/ibiza-intelligence/{slug}/'
    return f'/{lang}/ibiza-intelligence/' if slug is None else f'/{lang}/ibiza-intelligence/{slug}/'
def page(path): return ROOT/path.strip('/')/'index.html'

count=0
for slug in SLUGS:
    expected={BASE+url(lang,slug) for lang in LANGS}
    for lang in LANGS:
        p=page(url(lang,slug))
        if not p.exists(): errors.append(f'missing Black Book page: {url(lang,slug)}'); continue
        count+=1; text=p.read_text(encoding='utf-8')
        if text.lower().count('<h1')!=1: errors.append(f'bad H1 count: {url(lang,slug)}')
        alts=re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',text,re.I)
        actual={href for code,href in alts if code.lower()!='x-default'}
        x=[href for code,href in alts if code.lower()=='x-default']
        if actual!=expected: errors.append(f'hreflang mismatch: {url(lang,slug)}')
        if x!=[BASE+url('en',slug)]: errors.append(f'x-default mismatch: {url(lang,slug)}')
        if slug is None:
            links=re.findall(r'<a\s+class="intel-card"\s+href="([^"]+)"',text,re.I)
            if lang!='en' and len(links)!=6: errors.append(f'localized Black Book hub card count != 6: {url(lang)}')
        elif lang!='en':
            links=re.findall(r'<a\s+class="ivm-intelligence-related-card"\s+href="([^"]+)"',text,re.I)
            if len(links)!=3: errors.append(f'related article count != 3: {url(lang,slug)}')
            if any(not href.startswith(f'/{lang}/ibiza-intelligence/') for href in links): errors.append(f'related article changes language: {url(lang,slug)}')
            if 'ivm-intelligence-service' not in text: errors.append(f'service pathway missing: {url(lang,slug)}')

if count!=35: errors.append(f'expected 35 Black Book pages, found {count}')
if errors:
    for e in errors: print('FAIL: '+e)
    raise SystemExit(f'Phase 71 audit found {len(errors)} issue(s)')
print('PASS: Phase 71 audit — 35 Black Book pages; 7 reciprocal five-language editorial clusters; localized related notes and service pathways verified')