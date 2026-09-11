from pathlib import Path
from html import unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
PAGES={
'private-concierge-ibiza':('whole-stay-concierge','/luxury-lifestyle-management-ibiza/','Private clients with multi-service Ibiza stays'),
'luxury-lifestyle-management-ibiza':('ongoing-lifestyle-management','/personal-concierge-ibiza/','Private clients requiring ongoing full-stay lifestyle management'),
'personal-concierge-ibiza':('direct-personal-assistance','/private-concierge-ibiza/','Individuals, couples and families seeking direct personal concierge assistance'),
'luxury-travel-concierge-ibiza':('traveller-prearrival-planning','/destination-management-ibiza/','International luxury travellers planning an Ibiza trip'),
'vip-services-ibiza':('vip-access-hospitality','/private-concierge-ibiza/','VIP guests and private groups focused on hospitality, access and mobility'),
'private-client-services-ibiza':('principal-pa-family-office','/destination-management-ibiza/','Principals, personal assistants, executive assistants and family offices'),
'destination-management-ibiza':('b2b-local-execution','/luxury-travel-concierge-ibiza/','Luxury travel advisors, concierge companies and professional hospitality partners'),
'bespoke-concierge-ibiza':('one-off-bespoke-request','/private-concierge-ibiza/','Private clients with unusual, one-off or highly specific Ibiza requests'),
}
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)

def schemas(html):
    out=[]
    for m in SCRIPT_RE.finditer(html):
        try:data=json.loads(m.group(1))
        except Exception as exc: raise SystemExit(f'Phase 108 invalid JSON-LD: {exc}')
        if isinstance(data,dict) and isinstance(data.get('@graph'),list): out.extend(data['@graph'])
        elif isinstance(data,dict): out.append(data)
    return out

sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
for slug,(key,adjacent,audience) in PAGES.items():
    target=ROOT/slug/'index.html'
    if not target.exists(): raise SystemExit(f'Phase 108 page missing: {slug}')
    html=target.read_text(encoding='utf-8')
    url=f'{BASE}/{slug}/'
    canonical=re.findall(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>',html,re.I)
    if canonical!=[url]: raise SystemExit(f'Phase 108 canonical drift: {slug} -> {canonical}')
    if len(re.findall(r'<h1\b',html,re.I))!=1: raise SystemExit(f'Phase 108 H1 drift: {slug}')
    if html.count('ivm-phase108-intent')!=1: raise SystemExit(f'Phase 108 visible intent section mismatch: {slug}')
    section=re.search(r'<section\b[^>]*ivm-phase108-intent[^>]*>(.*?)</section>',html,re.I|re.S)
    if not section: raise SystemExit(f'Phase 108 intent section malformed: {slug}')
    block=section.group(0)
    if f'data-intent-key="{key}"' not in block: raise SystemExit(f'Phase 108 intent key mismatch: {slug}')
    if 'Choose the right service model' not in block or '<strong>Different from:</strong>' not in block:
        raise SystemExit(f'Phase 108 decision language missing: {slug}')
    if f'href="{adjacent}"' not in block: raise SystemExit(f'Phase 108 adjacent pathway missing: {slug} -> {adjacent}')
    words=re.findall(r"\b[\w'-]+\b",unescape(re.sub(r'<[^>]+>',' ',section.group(1))))
    if len(words)<55: raise SystemExit(f'Phase 108 intent section too thin: {slug} -> {len(words)} words')
    services=[n for n in schemas(html) if isinstance(n,dict) and n.get('@type')=='Service' and (n.get('url')==url or str(n.get('@id','')).startswith(url))]
    if len(services)!=1: raise SystemExit(f'Phase 108 Service schema cardinality mismatch: {slug} -> {len(services)}')
    svc=services[0]
    if len(svc.get('disambiguatingDescription',''))<120: raise SystemExit(f'Phase 108 schema disambiguation too weak: {slug}')
    if (svc.get('audience') or {}).get('audienceType')!=audience: raise SystemExit(f'Phase 108 audience mismatch: {slug}')
    if sitemap.count(url)!=1: raise SystemExit(f'Phase 108 sitemap URL count changed: {slug}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 108 accessibility drift: {slug}')

# No Phase 108 URL or synthetic inventory may appear in sitemap.
if 'phase108' in sitemap.lower(): raise SystemExit('Phase 108 must not add sitemap inventory')
print('PASS: Phase 108 audit — eight concierge intents are visibly and structurally disambiguated with distinct buyer audiences, adjacent pathways and no new SEO inventory')
