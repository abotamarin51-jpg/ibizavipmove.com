from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
errors=[]

HTML=list(ROOT.rglob('*.html'))
indexable=[]
canonical_to_file={}
for p in HTML:
    text=p.read_text(encoding='utf-8')
    if re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex',text,re.I):
        continue
    cm=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',text,re.I)
    if not cm: continue
    canonical=cm.group(1)
    indexable.append((p,text,canonical))
    canonical_to_file[canonical.rstrip('/')+'/']=p

# Sitemap URLs must map to indexable canonicals, and every indexable canonical must be represented.
sitemap=ROOT/'sitemap.xml'
if not sitemap.exists():
    errors.append('sitemap.xml missing')
    sitemap_urls=set()
else:
    tree=ET.parse(sitemap);ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    sitemap_urls={u.find(f'{{{ns}}}loc').text.rstrip('/')+'/' for u in tree.getroot().findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
    for url in sorted(sitemap_urls):
        if url not in canonical_to_file:
            errors.append(f'sitemap URL has no indexable canonical page: {url}')
    for canonical,p in sorted((c,p) for c,p in canonical_to_file.items()):
        if canonical not in sitemap_urls:
            errors.append(f'indexable canonical missing from sitemap: {canonical} ({p})')

# Resolve internal absolute paths to generated targets.
def internal_target(href):
    if not href or href.startswith(('#','mailto:','tel:','javascript:','data:')):
        return None
    parsed=urlparse(href)
    if parsed.scheme and parsed.netloc and parsed.netloc!='ibizavipmove.com':
        return None
    path=parsed.path or '/'
    if path.startswith('/assets/') or path in ('/favicon.png','/site.webmanifest','/robots.txt','/sitemap.xml','/image-sitemap.xml','/llms.txt'):
        return None
    return path

def path_exists(path):
    if path=='/': return (ROOT/'index.html').exists()
    clean=path.lstrip('/')
    candidates=[ROOT/clean,ROOT/clean/'index.html']
    if Path(clean).suffix: candidates.append(ROOT/clean)
    return any(c.exists() for c in candidates)

for p,text,canonical in indexable:
    # Broken internal navigation/content links.
    for href in re.findall(r'<a\b[^>]*\bhref="([^"]+)"',text,re.I):
        target=internal_target(href)
        if target and not path_exists(target):
            errors.append(f'broken internal link in {p.relative_to(ROOT)}: {href}')

    # Local images must exist in the deploy artifact.
    for src in re.findall(r'<(?:img|source)\b[^>]*(?:src|srcset)="([^"]+)"',text,re.I):
        first=src.split(',')[0].strip().split()[0]
        if first.startswith('/assets/') and not (ROOT/first.lstrip('/')).exists():
            errors.append(f'missing local image/asset in {p.relative_to(ROOT)}: {first}')

    # Hreflang links: unique language codes, targets exist, and target links back to this canonical.
    alts=re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',text,re.I)
    if alts:
        langs=[lang.lower() for lang,_ in alts]
        if len(langs)!=len(set(langs)):
            errors.append(f'duplicate hreflang language on {p.relative_to(ROOT)}: {langs}')
        source=canonical.rstrip('/')+'/'
        for lang,href in alts:
            if lang.lower()=='x-default':
                continue
            target=href.rstrip('/')+'/'
            tp=canonical_to_file.get(target)
            if not tp:
                errors.append(f'hreflang target missing/indexability issue on {p.relative_to(ROOT)}: {lang} -> {href}')
                continue
            ttext=tp.read_text(encoding='utf-8')
            backlinks=[h.rstrip('/')+'/' for _,h in re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',ttext,re.I)]
            if source not in backlinks:
                errors.append(f'non-reciprocal hreflang: {source} -> {target} but no backlink')

    # Phase 35 accessibility landmarks must persist on indexable HTML.
    if 'id="main-content"' not in text:
        errors.append(f'missing main-content landmark: {p.relative_to(ROOT)}')
    if 'class="ivm-skip-link"' not in text:
        errors.append(f'missing skip link: {p.relative_to(ROOT)}')

# Ensure all five-language service clusters exist after Phases 36–37.
clusters=[
['/luxury-villas-ibiza/','/es/villas-lujo-ibiza/','/fr/villas-luxe-ibiza/','/de/luxusvillen-ibiza/','/ar/luxury-villas-ibiza/'],
['/yacht-charter-ibiza/','/es/yate-privado-ibiza/','/fr/location-yacht-ibiza/','/de/yachtcharter-ibiza/','/ar/yacht-charter-ibiza/'],
['/private-aviation-ibiza/','/es/aviacion-privada-ibiza/','/fr/aviation-privee-ibiza/','/de/private-aviation-ibiza/','/ar/private-aviation-ibiza/'],
['/private-security-ibiza/','/es/seguridad-privada-ibiza/','/fr/securite-privee-ibiza/','/de/private-sicherheit-ibiza/','/ar/private-security-ibiza/']]
for cluster in clusters:
    missing=[path for path in cluster if BASE+path not in canonical_to_file]
    if missing: errors.append(f'incomplete five-language cluster: {missing}')

if errors:
    print('\n'.join('FAIL: '+e for e in errors))
    raise SystemExit(f'Phase 41 quality gate found {len(errors)} issue(s)')

print(f'PASS: Phase 41 quality gate — {len(indexable)} indexable pages; sitemap parity, internal links, assets, reciprocal hreflang and accessibility landmarks verified')
