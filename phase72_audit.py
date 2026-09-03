from pathlib import Path
import re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'; LANGS=('en','es','fr','de','ar'); errors=[]
def url(lang): return '/media-partners/' if lang=='en' else f'/{lang}/media-partners/'
def page(path): return ROOT/path.strip('/')/'index.html'
expected={BASE+url(l) for l in LANGS}
for lang in LANGS:
    p=page(url(lang))
    if not p.exists(): errors.append(f'missing media page: {url(lang)}'); continue
    t=p.read_text(encoding='utf-8')
    if t.lower().count('<h1')!=1: errors.append(f'bad H1: {url(lang)}')
    alts=re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',t,re.I)
    actual={href for code,href in alts if code.lower()!='x-default'}
    if actual!=expected: errors.append(f'hreflang mismatch: {url(lang)}')
    if 'partnership@ibizavipmove.com' not in t: errors.append(f'partnership email missing: {url(lang)}')
    if '/assets/phase72.css' not in t and '/assets/bundles/' not in t: errors.append(f'phase72 styling missing: {url(lang)}')
    if lang!='en':
        links=re.findall(r'<a\s+class="ivm-media-service"\s+href="([^"]+)"',t,re.I)
        if len(links)!=11: errors.append(f'expected 11 localized service links: {url(lang)}')
        if any(not href.startswith(f'/{lang}/') for href in links): errors.append(f'media service link changes language: {url(lang)}')
if errors:
    for e in errors: print('FAIL: '+e)
    raise SystemExit(f'Phase 72 audit found {len(errors)} issue(s)')
print('PASS: Phase 72 audit — five-language Media & Partners cluster, 44 localized service pathways and partnership contact verified')