from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
errors=[]
warnings=[]

HTML=list(ROOT.rglob('*.html'))
indexable=[]
canonical_to_file={}
for p in HTML:
    text=p.read_text(encoding='utf-8')
    if re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex',text,re.I): continue
    cm=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',text,re.I)
    if not cm: continue
    canonical=cm.group(1).rstrip('/')+'/'
    if canonical in canonical_to_file: errors.append(f'duplicate canonical output: {canonical} -> {canonical_to_file[canonical]} and {p}')
    canonical_to_file[canonical]=p; indexable.append((p,text,canonical))

# Keep sitemap exactly aligned with current indexable canonicals while preserving existing metadata.
sitemap=ROOT/'sitemap.xml'; NS='http://www.sitemaps.org/schemas/sitemap/0.9'; ET.register_namespace('',NS); metadata={}
if sitemap.exists():
    try:
        tree=ET.parse(sitemap)
        for u in tree.getroot().findall(f'{{{NS}}}url'):
            loc=u.find(f'{{{NS}}}loc')
            if loc is None or not loc.text: continue
            key=loc.text.rstrip('/')+'/'; metadata[key]={}
            for field in ('lastmod','changefreq','priority'):
                el=u.find(f'{{{NS}}}{field}')
                if el is not None and el.text: metadata[key][field]=el.text
    except Exception as exc: warnings.append(f'could not parse previous sitemap; rebuilding: {exc}')
root=ET.Element(f'{{{NS}}}urlset')
for canonical in sorted(canonical_to_file):
    u=ET.SubElement(root,f'{{{NS}}}url'); ET.SubElement(u,f'{{{NS}}}loc').text=canonical
    meta=metadata.get(canonical,{})
    for field in ('lastmod','changefreq','priority'):
        if meta.get(field): ET.SubElement(u,f'{{{NS}}}{field}').text=meta[field]
ET.ElementTree(root).write(sitemap,encoding='utf-8',xml_declaration=True)

def path_exists(path):
    if path=='/': return (ROOT/'index.html').exists()
    clean=path.lstrip('/'); return (ROOT/clean).exists() or (ROOT/clean/'index.html').exists()

def internal_target(href):
    if not href or href.startswith(('#','mailto:','tel:','javascript:','data:')): return None
    parsed=urlparse(href)
    if parsed.scheme and parsed.netloc and parsed.netloc!='ibizavipmove.com': return None
    path=parsed.path or '/'
    if path.startswith('/assets/') or path in ('/favicon.png','/site.webmanifest','/robots.txt','/sitemap.xml','/image-sitemap.xml','/llms.txt'): return None
    return path

for p,text,canonical in indexable:
    for href in re.findall(r'<a\b[^>]*\bhref="([^"]+)"',text,re.I):
        target=internal_target(href)
        if target and not path_exists(target): warnings.append(f'internal target from {p.relative_to(ROOT)}: {href}')

    # Validate local visual assets by URL path, ignoring cache-busting query strings such as ?v=8.
    for src in re.findall(r'<(?:img|source)\b[^>]*(?:src|srcset)="([^"]+)"',text,re.I):
        first=src.split(',')[0].strip().split()[0]
        asset_path=urlparse(first).path
        if asset_path.startswith('/assets/') and not (ROOT/asset_path.lstrip('/')).exists():
            errors.append(f'missing local image/asset in {p.relative_to(ROOT)}: {asset_path}')

    if 'id="main-content"' not in text: errors.append(f'missing main-content landmark: {p.relative_to(ROOT)}')
    if 'class="ivm-skip-link"' not in text: errors.append(f'missing skip link: {p.relative_to(ROOT)}')

# Five-language clusters introduced in Phases 36–37 must remain complete and reciprocal.
clusters=[
['/luxury-villas-ibiza/','/es/villas-lujo-ibiza/','/fr/villas-luxe-ibiza/','/de/luxusvillen-ibiza/','/ar/luxury-villas-ibiza/'],
['/yacht-charter-ibiza/','/es/yate-privado-ibiza/','/fr/location-yacht-ibiza/','/de/yachtcharter-ibiza/','/ar/yacht-charter-ibiza/'],
['/private-aviation-ibiza/','/es/aviacion-privada-ibiza/','/fr/aviation-privee-ibiza/','/de/private-aviation-ibiza/','/ar/private-aviation-ibiza/'],
['/private-security-ibiza/','/es/seguridad-privada-ibiza/','/fr/securite-privee-ibiza/','/de/private-sicherheit-ibiza/','/ar/private-security-ibiza/']]
for cluster in clusters:
    urls=[BASE+p for p in cluster]; missing=[u for u in urls if u not in canonical_to_file]
    if missing: errors.append(f'incomplete five-language cluster: {missing}'); continue
    expected=set(urls)
    for url in urls:
        text=canonical_to_file[url].read_text(encoding='utf-8')
        alts=re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',text,re.I)
        actual={href.rstrip('/')+'/' for lang,href in alts if lang.lower()!='x-default'}
        if actual!=expected: errors.append(f'hreflang cluster mismatch on {url}: expected {sorted(expected)}, found {sorted(actual)}')

critical=['/','/services/','/private-concierge-ibiza/','/private-chauffeur-ibiza/','/luxury-villas-ibiza/','/yacht-charter-ibiza/','/restaurants-nightlife-ibiza/','/private-aviation-ibiza/','/private-security-ibiza/','/private-office/','/ibiza-intelligence/','/partners/','/about/','/contact/']
for path in critical:
    if not path_exists(path): errors.append(f'critical page missing: {path}')

contacts=[('/contact/','conciergeForm'),('/es/contacto/','localizedConciergeForm'),('/fr/contact/','localizedConciergeForm'),('/de/kontakt/','localizedConciergeForm'),('/ar/contact/','localizedConciergeForm')]
for path,form_id in contacts:
    p=ROOT/path.strip('/')/'index.html'
    if not p.exists(): errors.append(f'contact page missing: {path}'); continue
    text=p.read_text(encoding='utf-8')
    if f'id="{form_id}"' not in text: errors.append(f'contact workflow form missing on {path}')
    for field in ('fName','fPhone','fArrival','fDeparture','fService','fGuests','fBrief'):
        if f'id="{field}"' not in text: errors.append(f'contact field {field} missing on {path}')

# Diagnostic file was temporary; never ship it in normal production builds.
report=ROOT/'quality-report.txt'
if report.exists(): report.unlink()

for warning in warnings[:30]: print('WARN: '+warning)
if len(warnings)>30: print(f'WARN: {len(warnings)-30} additional noncritical warning(s) suppressed')
if errors:
    print('\n'.join('FAIL: '+e for e in errors))
    raise SystemExit(f'Phase 41 quality gate found {len(errors)} critical issue(s)')
print(f'PASS: Phase 41 quality gate — {len(indexable)} indexable pages; sitemap aligned; critical assets, accessibility, multilingual clusters, navigation and forms verified; {len(warnings)} noncritical warning(s)')
