from pathlib import Path
from collections import defaultdict
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
LANGS=('en','es','fr','de','ar')
EXPECTED=set(LANGS)|{'x-default'}
LEGAL={BASE+'/privacy/',BASE+'/terms/',BASE+'/cookies/'}
NOINDEX_RE=re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex',re.I)
CANON_RE=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)',re.I)
LANG_RE=re.compile(r'<html\b[^>]*\blang=["\']([^"\']+)',re.I)
ALT_TAG_RE=re.compile(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\'][^"\']+["\'])[^>]*>',re.I)

pages={}
for f in ROOT.rglob('*.html'):
    html=f.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html):
        continue
    cm=CANON_RE.search(html)
    if not cm:
        continue
    canonical=cm.group(1).strip()
    lm=LANG_RE.search(html)
    lang=lm.group(1).lower().split('-')[0] if lm else None
    alts={}
    for tag in ALT_TAG_RE.findall(html):
        hm=re.search(r'hreflang=["\']([^"\']+)',tag,re.I)
        um=re.search(r'href=["\']([^"\']+)',tag,re.I)
        if not hm or not um:
            raise SystemExit(f'Phase 82 malformed hreflang tag: {canonical}')
        code=hm.group(1).lower(); href=um.group(1).strip()
        if code in alts:
            raise SystemExit(f'Phase 82 duplicate hreflang {code}: {canonical}')
        alts[code]=href
    pages[canonical]={'lang':lang,'alts':alts}

if len(pages)!=138:
    raise SystemExit(f'Phase 82 expected 138 indexable canonicals, found {len(pages)}')
if set(c for c,p in pages.items() if not p['alts'])!=LEGAL:
    raise SystemExit('Phase 82 only privacy/terms/cookies may omit hreflang')

clusters=defaultdict(set)
for canonical,p in pages.items():
    if canonical in LEGAL:
        continue
    lang=p['lang']; alts=p['alts']
    if lang not in LANGS:
        raise SystemExit(f'Phase 82 unexpected page language: {canonical} -> {lang}')
    if set(alts)!=EXPECTED:
        raise SystemExit(f'Phase 82 incomplete hreflang set: {canonical} -> {sorted(alts)}')
    if alts[lang]!=canonical:
        raise SystemExit(f'Phase 82 self hreflang mismatch: {canonical}')
    if alts['x-default']!=alts['en']:
        raise SystemExit(f'Phase 82 x-default must resolve to English: {canonical}')
    for code in LANGS:
        target=alts[code]
        if target not in pages:
            raise SystemExit(f'Phase 82 hreflang target missing: {canonical} {code} -> {target}')
        target_page=pages[target]
        if target_page['lang']!=code:
            raise SystemExit(f'Phase 82 target language mismatch: {canonical} {code} -> {target}')
        if target_page['alts'].get(lang)!=canonical:
            raise SystemExit(f'Phase 82 non-reciprocal hreflang: {canonical} -> {target}')
    signature=tuple(alts[code] for code in LANGS)
    clusters[signature].add(canonical)

if len(clusters)!=27:
    raise SystemExit(f'Phase 82 expected 27 five-language clusters, found {len(clusters)}')
for signature,members in clusters.items():
    if len(members)!=5 or members!=set(signature):
        raise SystemExit(f'Phase 82 malformed five-language cluster: {signature} -> {len(members)} members')

home_signature=(BASE+'/',BASE+'/es/',BASE+'/fr/',BASE+'/de/',BASE+'/ar/')
if home_signature not in clusters:
    raise SystemExit('Phase 82 homepage cluster missing from global hreflang graph')

print('PASS: Phase 82 hreflang audit — 135 multilingual pages form 27 complete reciprocal five-language clusters; 3 English legal pages correctly remain standalone')
