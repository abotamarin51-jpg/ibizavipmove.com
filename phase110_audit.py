from pathlib import Path
from urllib.parse import urljoin,urlparse
import re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'
SOURCE_LINKS={
'/private-chauffeur-ibiza/':['/case-studies/principal-chauffeur-security-three-days/','/private-concierge-marina-botafoch-ibiza/','/private-concierge-cala-jondal-es-cubells-ibiza/'],
'/restaurants-nightlife-ibiza/':['/case-studies/late-night-dual-vehicle-arrival/','/private-concierge-marina-botafoch-ibiza/','/private-concierge-cala-jondal-es-cubells-ibiza/'],
'/private-aviation-ibiza/':['/case-studies/private-aviation-arrival-seven-guests/','/private-concierge-marina-botafoch-ibiza/'],
'/private-security-ibiza/':['/case-studies/principal-chauffeur-security-three-days/','/private-concierge-cala-jondal-es-cubells-ibiza/','/private-concierge-santa-eulalia-roca-llisa-ibiza/'],
'/yacht-charter-ibiza/':['/case-studies/weekend-concierge-two-guests/','/private-concierge-marina-botafoch-ibiza/','/private-concierge-cala-jondal-es-cubells-ibiza/','/private-concierge-santa-eulalia-roca-llisa-ibiza/'],
'/private-chef-staffing-ibiza/':['/case-studies/weekend-concierge-two-guests/','/private-concierge-santa-gertrudis-ibiza/','/private-concierge-santa-eulalia-roca-llisa-ibiza/'],
'/wellness-ibiza/':['/case-studies/weekend-concierge-two-guests/','/private-concierge-santa-gertrudis-ibiza/','/private-concierge-santa-eulalia-roca-llisa-ibiza/'],
'/destination-management-ibiza/':['/case-studies/multi-day-executive-chauffeur-program/','/case-studies/private-aviation-arrival-seven-guests/'],
'/international-clients/':['/case-studies/multi-day-executive-chauffeur-program/','/private-concierge-marina-botafoch-ibiza/'],
}
TARGET_BACKLINKS={
'/case-studies/late-night-dual-vehicle-arrival/':['/restaurants-nightlife-ibiza/','/private-chauffeur-ibiza/','/private-concierge-marina-botafoch-ibiza/'],
'/case-studies/multi-day-executive-chauffeur-program/':['/private-chauffeur-ibiza/','/destination-management-ibiza/','/international-clients/'],
'/case-studies/principal-chauffeur-security-three-days/':['/private-security-ibiza/','/private-chauffeur-ibiza/','/private-client-services-ibiza/'],
'/case-studies/private-aviation-arrival-seven-guests/':['/private-aviation-ibiza/','/private-chauffeur-ibiza/','/luxury-travel-concierge-ibiza/'],
'/case-studies/weekend-concierge-two-guests/':['/private-concierge-ibiza/','/luxury-villas-ibiza/','/yacht-charter-ibiza/'],
'/private-concierge-marina-botafoch-ibiza/':['/private-chauffeur-ibiza/','/restaurants-nightlife-ibiza/','/yacht-charter-ibiza/'],
'/private-concierge-cala-jondal-es-cubells-ibiza/':['/private-chauffeur-ibiza/','/restaurants-nightlife-ibiza/','/yacht-charter-ibiza/'],
'/private-concierge-santa-eulalia-roca-llisa-ibiza/':['/private-chauffeur-ibiza/','/private-security-ibiza/','/wellness-ibiza/'],
'/private-concierge-santa-gertrudis-ibiza/':['/private-chauffeur-ibiza/','/private-chef-staffing-ibiza/','/wellness-ibiza/'],
}
MIN_UNIQUE_INLINKS={
'/case-studies/late-night-dual-vehicle-arrival/':4,
'/case-studies/multi-day-executive-chauffeur-program/':4,
'/case-studies/principal-chauffeur-security-three-days/':5,
'/case-studies/private-aviation-arrival-seven-guests/':5,
'/case-studies/weekend-concierge-two-guests/':8,
'/private-concierge-marina-botafoch-ibiza/':9,
'/private-concierge-cala-jondal-es-cubells-ibiza/':8,
'/private-concierge-santa-eulalia-roca-llisa-ibiza/':8,
'/private-concierge-santa-gertrudis-ibiza/':6,
}
STYLE='<link rel="stylesheet" href="/assets/phase110.css?v=110">'

def page(path): return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'

def html(path):
    p=page(path)
    if not p.exists(): raise SystemExit(f'Phase 110 page missing: {path}')
    return p.read_text(encoding='utf-8')

if not (ROOT/'assets'/'phase110.css').exists(): raise SystemExit('Phase 110 stylesheet missing')

for path,links in SOURCE_LINKS.items():
    text=html(path)
    if text.count('ivm-phase110-flow')!=1: raise SystemExit(f'Phase 110 source module mismatch: {path}')
    section=re.search(r'<section\b[^>]*ivm-phase110-flow[^>]*>(.*?)</section>',text,re.I|re.S)
    if not section: raise SystemExit(f'Phase 110 source module malformed: {path}')
    block=section.group(0)
    for href in links:
        if f'href="{href}"' not in block: raise SystemExit(f'Phase 110 contextual target missing: {path} -> {href}')
    if block.count('ivm-phase110-card')!=len(links): raise SystemExit(f'Phase 110 card count mismatch: {path}')
    if text.count(STYLE)!=1: raise SystemExit(f'Phase 110 stylesheet link mismatch: {path}')
    if len(re.findall(r'<h1\b',text,re.I))!=1: raise SystemExit(f'Phase 110 H1 drift: {path}')
    if 'id="main-content"' not in text or 'class="ivm-skip-link"' not in text: raise SystemExit(f'Phase 110 accessibility drift: {path}')

for path,links in TARGET_BACKLINKS.items():
    text=html(path)
    if text.count('ivm-phase110-return')!=1: raise SystemExit(f'Phase 110 target module mismatch: {path}')
    section=re.search(r'<section\b[^>]*ivm-phase110-return[^>]*>(.*?)</section>',text,re.I|re.S)
    if not section: raise SystemExit(f'Phase 110 return module malformed: {path}')
    block=section.group(0)
    for href in links:
        if f'href="{href}"' not in block: raise SystemExit(f'Phase 110 commercial return link missing: {path} -> {href}')
    if text.count(STYLE)!=1: raise SystemExit(f'Phase 110 stylesheet link mismatch: {path}')
    if len(re.findall(r'<h1\b',text,re.I))!=1: raise SystemExit(f'Phase 110 H1 drift: {path}')
    if 'id="main-content"' not in text or 'class="ivm-skip-link"' not in text: raise SystemExit(f'Phase 110 accessibility drift: {path}')

# Build an actual unique-source internal-link graph over canonical sitemap URLs.
sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
urls=re.findall(r'<loc>(https://ibizavipmove\.com[^<]+)</loc>',sitemap)
urlset=set(urls)
if 'phase110' in sitemap.lower(): raise SystemExit('Phase 110 must not add sitemap inventory')
inbound={u:set() for u in urls}
for src_url in urls:
    src_path=urlparse(src_url).path or '/'
    src_file=page(src_path)
    if not src_file.exists(): continue
    text=src_file.read_text(encoding='utf-8')
    for href in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\']',text,re.I):
        if href.startswith(('mailto:','tel:','javascript:','#')): continue
        full=urljoin(src_url,href)
        parsed=urlparse(full)
        if parsed.netloc not in ('','ibizavipmove.com'): continue
        target=BASE+(parsed.path or '/')
        if target in urlset and target!=src_url: inbound[target].add(src_url)

for path,minimum in MIN_UNIQUE_INLINKS.items():
    target=BASE+path
    actual=len(inbound.get(target,set()))
    if actual<minimum: raise SystemExit(f'Phase 110 authority target underlinked: {path} -> {actual} unique sources, need {minimum}')

print('PASS: Phase 110 audit — contextual authority loops verified and all 5 case studies + 4 local concierge pages meet protected unique-source inlink thresholds without new sitemap inventory')
