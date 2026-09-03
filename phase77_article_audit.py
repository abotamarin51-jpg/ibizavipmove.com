from pathlib import Path
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG=BASE+'/#organization'
LANGS=('en','es','fr','de','ar')
SLUGS=(
'private-arrival','ibiza-formentera-yacht-day','ibiza-august-planning',
'villa-arrival-planning','nightlife-transport-planning','private-aviation-ground-coordination')
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)


def path_for(lang,slug):
    return f'/ibiza-intelligence/{slug}/' if lang=='en' else f'/{lang}/ibiza-intelligence/{slug}/'

def hub_for(lang):
    return '/ibiza-intelligence/' if lang=='en' else f'/{lang}/ibiza-intelligence/'

def page(path):
    return ROOT/path.strip('/')/'index.html'

count=0
for lang in LANGS:
    for slug in SLUGS:
        path=path_for(lang,slug); f=page(path)
        if not f.exists():raise SystemExit(f'Phase 77 audit missing article: {path}')
        html=f.read_text(encoding='utf-8')
        canonical=BASE+path
        articles=[]
        for m in SCRIPT_RE.finditer(html):
            try:o=json.loads(m.group(1))
            except Exception:continue
            if isinstance(o,dict) and o.get('@type') in ('Article','BlogPosting'):articles.append(o)
        if len(articles)!=1:raise SystemExit(f'Phase 77 audit expected one Article: {path} -> {len(articles)}')
        a=articles[0]
        required=('headline','description','image','dateModified','author','publisher','mainEntityOfPage','isPartOf','about','isRelatedTo','mentions')
        missing=[k for k in required if not a.get(k)]
        if missing:raise SystemExit(f'Phase 77 audit missing fields {missing}: {path}')
        if a.get('@type')!='Article':raise SystemExit(f'Phase 77 audit wrong type: {path}')
        if a.get('@id')!=canonical.rstrip('/')+'/#article':raise SystemExit(f'Phase 77 audit bad id: {path}')
        if a.get('url')!=canonical:raise SystemExit(f'Phase 77 audit bad url: {path}')
        if a.get('inLanguage')!=lang:raise SystemExit(f'Phase 77 audit bad language: {path}')
        if a.get('author',{}).get('@id')!=ORG or a.get('publisher',{}).get('@id')!=ORG:raise SystemExit(f'Phase 77 audit bad authority refs: {path}')
        if a.get('mainEntityOfPage',{}).get('@id')!=canonical:raise SystemExit(f'Phase 77 audit bad mainEntityOfPage: {path}')
        if a.get('isPartOf',{}).get('url')!=BASE+hub_for(lang):raise SystemExit(f'Phase 77 audit bad collection: {path}')
        rel=a.get('isRelatedTo',[])
        if not isinstance(rel,list) or len(rel)!=3:raise SystemExit(f'Phase 77 audit related count: {path}')
        for item in rel:
            u=item.get('url','') if isinstance(item,dict) else ''
            if not u.startswith(BASE):raise SystemExit(f'Phase 77 audit external related URL: {path} -> {u}')
            rp=u.removeprefix(BASE)
            if not page(rp).exists():raise SystemExit(f'Phase 77 audit missing related URL: {path} -> {rp}')
            if lang=='en' and re.match(r'^/(es|fr|de|ar)/',rp):raise SystemExit(f'Phase 77 audit language leak: {path} -> {rp}')
            if lang!='en' and not rp.startswith(f'/{lang}/'):raise SystemExit(f'Phase 77 audit language leak: {path} -> {rp}')
        mention=a.get('mentions',{}).get('url','')
        if not mention.startswith(BASE) or not page(mention.removeprefix(BASE)).exists():raise SystemExit(f'Phase 77 audit bad service mention: {path}')
        if 'datePublished' in a:raise SystemExit(f'Phase 77 audit must not invent publication date: {path}')
        count+=1

if count!=30:raise SystemExit(f'Phase 77 audit expected 30 articles, found {count}')
print('PASS: Phase 77 Article audit — 30 Black Book planning notes across 5 languages have one normalized Article schema each')
