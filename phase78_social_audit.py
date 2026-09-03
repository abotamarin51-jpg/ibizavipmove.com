from pathlib import Path
import json,re

ROOT=Path('_site'); LANGS=('en','es','fr','de','ar')
SLUGS=('private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning','villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)

def path_for(lang,slug):return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'
def page(path):return ROOT/path.strip('/')/'index.html'
count=0
for lang in LANGS:
  for slug in SLUGS:
    path=path_for(lang,slug); f=page(path)
    if not f.exists():raise SystemExit(f'Phase 78 audit missing: {path}')
    html=f.read_text(encoding='utf-8')
    types=re.findall(r'<meta\s+property="og:type"\s+content="([^"]+)"',html,re.I)
    if types!=['article']:raise SystemExit(f'Phase 78 audit og:type wrong: {path} -> {types}')
    mods=re.findall(r'<meta\s+property="article:modified_time"\s+content="([^"]+)"',html,re.I)
    if len(mods)!=1 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',mods[0]):raise SystemExit(f'Phase 78 audit modified time wrong: {path}')
    articles=[]
    for m in SCRIPT_RE.finditer(html):
      try:o=json.loads(m.group(1))
      except Exception:continue
      if isinstance(o,dict) and o.get('@type')=='Article':articles.append(o)
    if len(articles)!=1:raise SystemExit(f'Phase 78 audit Article count wrong: {path}')
    if articles[0].get('dateModified')!=mods[0]:raise SystemExit(f'Phase 78 audit social/schema modified-time mismatch: {path}')
    if 'datePublished' in articles[0]:raise SystemExit(f'Phase 78 audit publication date must remain unset: {path}')
    count+=1
if count!=30:raise SystemExit(f'Phase 78 audit expected 30 notes, found {count}')
print('PASS: Phase 78 social audit — 30 Black Book Article pages align og:type and modified time with structured data')
