from pathlib import Path
from urllib.parse import urlparse
import re

ROOT=Path('_site')
NOINDEX_RE=re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex',re.I)
CANON_RE=re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"',re.I)
CSS_HERO_RE=re.compile(r'--hero\s*:\s*url\(\s*[\'\"]?([^\'\")\s]+)',re.I)
PRELOAD_RE=re.compile(r'<link\b[^>]*\brel=["\']preload["\'][^>]*\bas=["\']image["\'][^>]*>',re.I)
HREF_RE=re.compile(r'\bhref=["\']([^"\']+)["\']',re.I)
HERO_MEDIA_RE=re.compile(r'(<div\s+class=["\']page-hero-media["\'][^>]*>.*?<img\b)([^>]*)(>)',re.I|re.S)


def local_asset(url):
    path=urlparse(url).path
    return ROOT/path.lstrip('/') if path.startswith('/assets/') else None


def image_preload_paths(html):
    out=[]
    for tag in PRELOAD_RE.findall(html):
        m=HREF_RE.search(tag)
        if m: out.append(urlparse(m.group(1)).path)
    return out


def prioritize_semantic_hero(html):
    m=HERO_MEDIA_RE.search(html)
    if not m:
        return html,False
    attrs=m.group(2)
    attrs=re.sub(r'\s+loading=["\']lazy["\']','',attrs,flags=re.I)
    if not re.search(r'\bfetchpriority=["\']high["\']',attrs,re.I):
        attrs+=' fetchpriority="high"'
    if not re.search(r'\bdecoding=["\'][^"\']+["\']',attrs,re.I):
        attrs+=' decoding="async"'
    return html[:m.start()]+m.group(1)+attrs+m.group(3)+html[m.end():],True


updated=0
css_hero_pages=0
preloads_added=0
semantic_prioritized=0

for file in ROOT.rglob('*.html'):
    html=file.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html) or not CANON_RE.search(html):
        continue
    canonical_before=CANON_RE.search(html).group(1)
    hm=CSS_HERO_RE.search(html)
    if hm:
        hero=hm.group(1)
        hero_path=urlparse(hero).path
        asset=local_asset(hero)
        if asset is None:
            raise SystemExit(f'Phase 69 non-local CSS hero not supported: {file}: {hero}')
        if not asset.exists():
            raise SystemExit(f'Phase 69 CSS hero asset missing: {file}: {hero_path}')
        css_hero_pages+=1
        existing=image_preload_paths(html)
        if hero_path not in existing:
            tag=f'<link rel="preload" as="image" href="{hero}">'
            html=html.replace('</head>',tag+'</head>',1)
            preloads_added+=1
        elif existing.count(hero_path)>1:
            raise SystemExit(f'Phase 69 duplicate hero preload before normalization: {file}: {hero_path}')

    html,had_semantic=prioritize_semantic_hero(html)
    if had_semantic:
        semantic_prioritized+=1

    canonical_after=CANON_RE.search(html).group(1)
    if canonical_before!=canonical_after:
        raise SystemExit(f'Phase 69 canonical changed: {file}')
    file.write_text(html,encoding='utf-8')
    updated+=1

# Final validation across all indexable pages.
verified_css=0
for file in ROOT.rglob('*.html'):
    html=file.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html) or not CANON_RE.search(html):
        continue
    hm=CSS_HERO_RE.search(html)
    if hm:
        hero_path=urlparse(hm.group(1)).path
        matches=[x for x in image_preload_paths(html) if x==hero_path]
        if len(matches)!=1:
            raise SystemExit(f'Phase 69 expected exactly one CSS-hero preload: {file}: {hero_path} -> {len(matches)}')
        verified_css+=1
    m=HERO_MEDIA_RE.search(html)
    if m:
        attrs=m.group(2)
        if not re.search(r'\bfetchpriority=["\']high["\']',attrs,re.I):
            raise SystemExit(f'Phase 69 semantic hero lacks high fetch priority: {file}')
        if re.search(r'\bloading=["\']lazy["\']',attrs,re.I):
            raise SystemExit(f'Phase 69 semantic hero incorrectly lazy: {file}')

if verified_css<30:
    raise SystemExit(f'Phase 69 CSS hero coverage unexpectedly low: {verified_css}')
print(f'PASS: Phase 69 LCP hero discovery — {verified_css} CSS-background heroes have exact image preloads; {semantic_prioritized} semantic hero images prioritized; {preloads_added} new preload(s) added')
