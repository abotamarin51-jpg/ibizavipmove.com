from pathlib import Path
from html import escape, unescape
import re

ROOT=Path('_site')
NOINDEX_RE=re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex',re.I)
CANON_RE=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)',re.I)


def extract_meta(html,attr,name,label,canonical):
    patt=re.compile(rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])(?=[^>]*\bcontent=["\']([^"\']*)["\'])[^>]*>',re.I)
    matches=patt.findall(html)
    if len(matches)!=1 or not matches[0].strip():
        raise SystemExit(f'Phase 83 expected one non-empty {label}: {canonical} -> {len(matches)}')
    return unescape(matches[0].strip())


def set_meta(html,attr,name,value):
    patt=re.compile(rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])(?=[^>]*\bcontent=["\'][^"\']*["\'])[^>]*>',re.I)
    tag=f'<meta {attr}="{name}" content="{escape(value,quote=True)}">'
    if patt.search(html):
        return patt.sub(tag,html,count=1)
    return html.replace('</head>',tag+'</head>',1)

count=0
for f in ROOT.rglob('*.html'):
    html=f.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html):
        continue
    cm=CANON_RE.search(html)
    if not cm:
        continue
    canonical=cm.group(1).strip()
    og_title=extract_meta(html,'property','og:title','og:title',canonical)
    og_desc=extract_meta(html,'property','og:description','og:description',canonical)
    og_image=extract_meta(html,'property','og:image','og:image',canonical)
    html=set_meta(html,'name','twitter:card','summary_large_image')
    html=set_meta(html,'name','twitter:title',og_title)
    html=set_meta(html,'name','twitter:description',og_desc)
    html=set_meta(html,'name','twitter:image',og_image)
    f.write_text(html,encoding='utf-8')
    count+=1

if count!=138:
    raise SystemExit(f'Phase 83 expected 138 indexable pages, updated {count}')
print('PASS: Phase 83 social sharing — Twitter Cards synchronized with verified Open Graph metadata across all 138 indexable pages')
