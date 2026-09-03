from pathlib import Path
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
HOMES={'en':'/','es':'/es/','fr':'/fr/','de':'/de/','ar':'/ar/'}
ALT_TAG_RE=re.compile(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\'][^"\']+["\'])[^>]*>',re.I)
CANON_RE=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)',re.I)
LANG_RE=re.compile(r'<html\b[^>]*\blang=["\']([^"\']+)',re.I)


def file_for(path):
    return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'


def tags():
    out=[]
    for lang,path in HOMES.items():
        out.append(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{path}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    return ''.join(out)

for lang,path in HOMES.items():
    f=file_for(path)
    if not f.exists():
        raise SystemExit(f'Phase 82 homepage missing: {path}')
    html=f.read_text(encoding='utf-8')
    cm=CANON_RE.search(html)
    lm=LANG_RE.search(html)
    if not cm or cm.group(1).strip()!=BASE+path:
        raise SystemExit(f'Phase 82 canonical mismatch: {path}')
    if not lm or lm.group(1).lower().split('-')[0]!=lang:
        raise SystemExit(f'Phase 82 html lang mismatch: {path}')
    html=ALT_TAG_RE.sub('',html)
    html=html.replace('</head>',tags()+'</head>',1)
    f.write_text(html,encoding='utf-8')

# Local sanity: every homepage must expose one exact six-tag language set.
expected=set(HOMES)|{'x-default'}
for lang,path in HOMES.items():
    html=file_for(path).read_text(encoding='utf-8')
    found={}
    for tag in ALT_TAG_RE.findall(html):
        hm=re.search(r'hreflang=["\']([^"\']+)',tag,re.I)
        um=re.search(r'href=["\']([^"\']+)',tag,re.I)
        if not hm or not um:
            raise SystemExit(f'Phase 82 malformed hreflang tag: {path}')
        code=hm.group(1).lower(); href=um.group(1)
        if code in found:
            raise SystemExit(f'Phase 82 duplicate hreflang {code}: {path}')
        found[code]=href
    if set(found)!=expected:
        raise SystemExit(f'Phase 82 incomplete homepage hreflang set: {path} -> {sorted(found)}')
    if found[lang]!=BASE+path or found['x-default']!=BASE+'/':
        raise SystemExit(f'Phase 82 homepage self/x-default mismatch: {path}')

print('PASS: Phase 82 homepage hreflang — EN/ES/FR/DE/AR + x-default normalized reciprocally across all five homepages')

# Synchronize final Twitter Card metadata only after canonical/language metadata is stable.
import phase83_enhance
