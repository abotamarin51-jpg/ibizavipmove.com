from pathlib import Path
import json,re

ROOT=Path('_site')
ORG='https://ibizavipmove.com/#organization'
ARTICLE_URL='https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/'
ARTICLE_NAME='Top Luxury Travel Concierge Services for Ibiza Dining in 2026'
INSTAGRAM='https://www.instagram.com/ibizavipmove/'
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)

count=0
for p in ROOT.rglob('*.html'):
    html=p.read_text(encoding='utf-8')
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        for node in nodes:
            if not isinstance(node,dict) or node.get('@id')!=ORG:continue
            types=node.get('@type'); types=types if isinstance(types,list) else [types]
            if 'Organization' not in types:continue
            count+=1
            subject=node.get('subjectOf')
            if not isinstance(subject,list) or len(subject)!=1:raise SystemExit(f'Phase 99 subjectOf cardinality mismatch: {p}')
            article=subject[0]
            if not isinstance(article,dict) or article.get('@type')!='Article' or article.get('url')!=ARTICLE_URL or article.get('name')!=ARTICLE_NAME:
                raise SystemExit(f'Phase 99 external article mismatch: {p}')
            if (article.get('publisher') or {}).get('name')!='Luxury Magazine':raise SystemExit(f'Phase 99 publisher mismatch: {p}')
            if node.get('sameAs')!=[INSTAGRAM]:raise SystemExit(f'Phase 99 sameAs drift: {p} -> {node.get("sameAs")}')
            serialized=json.dumps(node,ensure_ascii=False).lower()
            if 'tripadvisor' in serialized:raise SystemExit(f'Phase 99 Tripadvisor must not be bound into canonical Organization: {p}')

if count<60:raise SystemExit(f'Phase 99 expected at least 60 verified Organization nodes, found {count}')
print(f'PASS: Phase 99 external subject audit — {count} canonical Organization nodes reference exactly one verified Luxury Magazine article while sameAs remains official Instagram only')
