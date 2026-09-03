from pathlib import Path
from html import unescape
import re

ROOT=Path('_site')
NOINDEX_RE=re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex',re.I)
CANON_RE=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)',re.I)


def one(html,attr,name,canonical):
    patt=re.compile(rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])(?=[^>]*\bcontent=["\']([^"\']*)["\'])[^>]*>',re.I)
    vals=[unescape(x.strip()) for x in patt.findall(html)]
    if len(vals)!=1 or not vals[0]:
        raise SystemExit(f'Phase 83 expected one non-empty {name}: {canonical} -> {len(vals)}')
    return vals[0]

count=0
for f in ROOT.rglob('*.html'):
    html=f.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html):
        continue
    cm=CANON_RE.search(html)
    if not cm:
        continue
    canonical=cm.group(1).strip()
    og_title=one(html,'property','og:title',canonical)
    og_desc=one(html,'property','og:description',canonical)
    og_image=one(html,'property','og:image',canonical)
    card=one(html,'name','twitter:card',canonical)
    tw_title=one(html,'name','twitter:title',canonical)
    tw_desc=one(html,'name','twitter:description',canonical)
    tw_image=one(html,'name','twitter:image',canonical)
    if card!='summary_large_image':
        raise SystemExit(f'Phase 83 unexpected Twitter card: {canonical} -> {card}')
    if (tw_title,tw_desc,tw_image)!=(og_title,og_desc,og_image):
        raise SystemExit(f'Phase 83 Twitter/Open Graph mismatch: {canonical}')
    if not og_image.startswith('https://ibizavipmove.com/'):
        raise SystemExit(f'Phase 83 social image is not first-party absolute URL: {canonical} -> {og_image}')
    count+=1

if count!=138:
    raise SystemExit(f'Phase 83 expected 138 indexable pages, audited {count}')
print('PASS: Phase 83 social audit — 138 indexable pages have one complete summary_large_image Twitter Card exactly aligned with Open Graph')
