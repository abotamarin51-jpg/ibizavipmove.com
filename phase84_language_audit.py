from pathlib import Path
from collections import Counter
import json
import re

ROOT=Path('_site')
NOINDEX_RE=re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex',re.I)
CANON_RE=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)',re.I)
LANG_RE=re.compile(r'<html\b[^>]*\blang=["\']([^"\']+)',re.I)
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)
TYPES={'WebPage','AboutPage','CollectionPage','Article','Service'}

pages=0
nodes=0
counts=Counter()
for f in ROOT.rglob('*.html'):
    html=f.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html):
        continue
    cm=CANON_RE.search(html)
    if not cm:
        continue
    canonical=cm.group(1).strip()
    lm=LANG_RE.search(html)
    if not lm:
        raise SystemExit(f'Phase 84 missing html lang: {canonical}')
    page_lang=lm.group(1).lower().split('-')[0]
    pages+=1
    for m in SCRIPT_RE.finditer(html):
        try:
            obj=json.loads(m.group(1))
        except Exception as exc:
            raise SystemExit(f'Phase 84 invalid JSON-LD: {canonical}: {exc}')
        candidates=[]
        if isinstance(obj,dict) and isinstance(obj.get('@graph'),list):
            candidates=[x for x in obj['@graph'] if isinstance(x,dict)]
        elif isinstance(obj,dict):
            candidates=[obj]
        for node in candidates:
            typ=node.get('@type')
            types=typ if isinstance(typ,list) else [typ]
            relevant=[t for t in types if t in TYPES]
            for t in relevant:
                counts[t]+=1
                nodes+=1
                value=node.get('inLanguage')
                if not value:
                    raise SystemExit(f'Phase 84 missing inLanguage: {canonical} [{t}]')
                lang=str(value).lower().split('-')[0]
                if lang!=page_lang:
                    raise SystemExit(f'Phase 84 inLanguage mismatch: {canonical} [{t}] {value} vs html {page_lang}')

if pages!=138:
    raise SystemExit(f'Phase 84 expected 138 indexable pages, audited {pages}')
if nodes<220:
    raise SystemExit(f'Phase 84 structured-language coverage unexpectedly low: {nodes}')
for required in ('WebPage','AboutPage','CollectionPage','Article','Service'):
    if counts[required]<1:
        raise SystemExit(f'Phase 84 missing structured type coverage: {required}')

print(f'PASS: Phase 84 language audit — {nodes} WebPage/AboutPage/CollectionPage/Article/Service entities across 138 indexable pages match their HTML language')
