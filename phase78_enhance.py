from pathlib import Path
from datetime import date
import re

ROOT=Path('_site')
TODAY=date.today().isoformat()
LANGS=('en','es','fr','de','ar')
SLUGS=(
'private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning',
'villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')


def path_for(lang,slug):
    return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'

def page(path):
    return ROOT/path.strip('/')/'index.html'

count=0
for lang in LANGS:
    for slug in SLUGS:
        path=path_for(lang,slug); f=page(path)
        if not f.exists():raise SystemExit(f'Phase 78 article missing: {path}')
        html=f.read_text(encoding='utf-8')
        if re.search(r'<meta\s+property="og:type"\s+content="[^"]*"',html,re.I):
            html=re.sub(r'(<meta\s+property="og:type"\s+content=")[^"]*(")',r'\1article\2',html,count=1,flags=re.I)
        else:
            html=html.replace('</head>','<meta property="og:type" content="article"></head>',1)
        if re.search(r'<meta\s+property="article:modified_time"\s+content="[^"]*"',html,re.I):
            html=re.sub(r'(<meta\s+property="article:modified_time"\s+content=")[^"]*(")',lambda m:m.group(1)+TODAY+m.group(2),html,count=1,flags=re.I)
        else:
            html=html.replace('</head>',f'<meta property="article:modified_time" content="{TODAY}"></head>',1)
        f.write_text(html,encoding='utf-8');count+=1

if count!=30:raise SystemExit(f'Phase 78 expected 30 articles, found {count}')
for lang in LANGS:
    for slug in SLUGS:
        path=path_for(lang,slug); html=page(path).read_text(encoding='utf-8')
        if len(re.findall(r'<meta\s+property="og:type"\s+content="article"',html,re.I))!=1:raise SystemExit(f'Phase 78 bad og:type: {path}')
        if len(re.findall(r'<meta\s+property="article:modified_time"\s+content="[^"]+"',html,re.I))!=1:raise SystemExit(f'Phase 78 bad modified time: {path}')
print('PASS: Phase 78 Black Book social metadata — 30 planning notes use og:type article with one modified-time signal')
