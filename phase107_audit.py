from pathlib import Path
import re

ROOT=Path('_site')
SCRIPT=ROOT/'assets'/'phase107.js'
CONTACTS=['/contact/','/es/contacto/','/fr/contact/','/de/kontakt/','/ar/contact/']
SCRIPT_TAG='<script src="/assets/phase107.js?v=107" defer></script>'


def page(path): return ROOT/path.strip('/')/'index.html'

if not SCRIPT.exists(): raise SystemExit('Phase 107 runtime script missing')
js=SCRIPT.read_text(encoding='utf-8')
if 'ANALYTICS_NO_PII_START' not in js or 'ANALYTICS_NO_PII_END' not in js:
    raise SystemExit('Phase 107 analytics privacy markers missing')
privacy_block=js.split('ANALYTICS_NO_PII_START',1)[1].split('ANALYTICS_NO_PII_END',1)[0]
for forbidden in ('fName','fPhone','selectedText(\'fClientType\')','selectedText(\'fArea\')'):
    if forbidden in privacy_block:
        raise SystemExit(f'Phase 107 PII/label leakage into analytics block: {forbidden}')
for required in ('ivm_qualified_lead','lead_role','stay_area','guests_bucket','lead_time_bucket','brief_present'):
    if required not in privacy_block:
        raise SystemExit(f'Phase 107 qualified-lead analytics field missing: {required}')
for required in ('fName','fPhone','fArrival','fDeparture','fGuests','fService','fBrief','fClientType','fArea'):
    if required not in js:
        raise SystemExit(f'Phase 107 WhatsApp brief field missing in runtime: {required}')
if "getElementById('localizedConciergeForm')" not in js:
    raise SystemExit('Phase 107 localized form runtime support missing')

for path in CONTACTS:
    target=page(path)
    if not target.exists(): raise SystemExit(f'Phase 107 contact page missing: {path}')
    html=target.read_text(encoding='utf-8')
    if html.count('id="fClientType"')!=1 or html.count('id="fArea"')!=1:
        raise SystemExit(f'Phase 107 qualification field cardinality mismatch: {path}')
    if html.count('data-ivm-qualified-brief="true"')!=1:
        raise SystemExit(f'Phase 107 qualified form marker mismatch: {path}')
    if html.count(SCRIPT_TAG)!=1:
        raise SystemExit(f'Phase 107 deferred script cardinality mismatch: {path}')
    if '<script src="/assets/phase107.js?v=107"></script>' in html:
        raise SystemExit(f'Phase 107 non-deferred script leaked: {path}')
    role=re.search(r'<select\s+id="fClientType"[^>]*>(.*?)</select>',html,re.I|re.S)
    area=re.search(r'<select\s+id="fArea"[^>]*>(.*?)</select>',html,re.I|re.S)
    if not role or role.group(1).count('<option')!=6:
        raise SystemExit(f'Phase 107 expected six client-role options: {path}')
    if not area or area.group(1).count('<option')!=7:
        raise SystemExit(f'Phase 107 expected seven stay-area options: {path}')
    for code in ('private_client','assistant','family_office','travel_advisor','hospitality_partner','other'):
        if f'value="{code}"' not in role.group(1):
            raise SystemExit(f'Phase 107 missing role code {code}: {path}')
    for code in ('ibiza_town','south','east','central','playa_den_bossa','west'):
        if f'value="{code}"' not in area.group(1):
            raise SystemExit(f'Phase 107 missing area code {code}: {path}')
    if len(re.findall(r'<h1\b',html,re.I))!=1:
        raise SystemExit(f'Phase 107 H1 drift: {path}')
    if '<link rel="canonical"' not in html:
        raise SystemExit(f'Phase 107 canonical missing: {path}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 107 accessibility drift: {path}')
    if '+34 613 75 62 11' in html or '34613756211' in html:
        raise SystemExit(f'Phase 107 old contact leaked: {path}')

# Conversion work must not create SEO inventory.
sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
if 'phase107' in sitemap.lower(): raise SystemExit('Phase 107 must not add sitemap URLs')

print('PASS: Phase 107 audit — five qualified private-brief forms classify buyer role and Ibiza stay area while analytics remain PII-free, runtime is deferred, and SEO/accessibility stay unchanged')

# Phase 108 separates adjacent concierge intents only after the conversion layer
# has passed. It adds no new URLs and is protected before the global final audit.
import phase108_enhance
import phase108_audit
