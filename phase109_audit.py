from pathlib import Path
from html import unescape
import re

ROOT=Path('_site')
PAGES={
'fr/conciergerie-privee-ibiza':['/fr/chauffeur-prive-ibiza/','/fr/villas-luxe-ibiza/','/fr/location-yacht-ibiza/','/fr/aviation-privee-ibiza/','/fr/restaurants-nightlife-ibiza/','/fr/securite-privee-ibiza/','/fr/contact/'],
'de/privater-concierge-ibiza':['/de/privater-chauffeur-ibiza/','/de/luxusvillen-ibiza/','/de/yachtcharter-ibiza/','/de/private-aviation-ibiza/','/de/restaurants-nightlife-ibiza/','/de/private-sicherheit-ibiza/','/de/kontakt/'],
'ar/private-concierge-ibiza':['/ar/private-chauffeur-ibiza/','/ar/luxury-villas-ibiza/','/ar/yacht-charter-ibiza/','/ar/private-aviation-ibiza/','/ar/restaurants-nightlife-ibiza/','/ar/private-security-ibiza/','/ar/contact/'],
}
for slug,links in PAGES.items():
    target=ROOT/slug/'index.html'
    if not target.exists(): raise SystemExit(f'Phase 109 page missing: {slug}')
    html=target.read_text(encoding='utf-8')
    if html.count('ivm-phase109-depth')!=1 or html.count('ivm-phase109-process')!=1:
        raise SystemExit(f'Phase 109 section cardinality mismatch: {slug}')
    if len(re.findall(r'<h1\b',html,re.I))!=1: raise SystemExit(f'Phase 109 H1 drift: {slug}')
    if '<link rel="canonical"' not in html: raise SystemExit(f'Phase 109 canonical missing: {slug}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 109 accessibility drift: {slug}')
    text=re.sub(r'<script.*?</script>|<style.*?</style>',' ',html,flags=re.I|re.S)
    text=unescape(re.sub(r'<[^>]+>',' ',text))
    words=re.findall(r"\b[\wÀ-ÿ'’\-]+\b",text)
    if len(words)<450: raise SystemExit(f'Phase 109 cornerstone still too thin: {slug} -> {len(words)} words')
    for href in links:
        if f'href="{href}"' not in html: raise SystemExit(f'Phase 109 same-language pathway missing: {slug} -> {href}')
    for place in ('Ibiza Town','Marina Botafoch','Cala Jondal','Es Cubells','Santa Eulària','Roca Llisa','Santa Gertrudis','Sant Josep'):
        if place not in html: raise SystemExit(f'Phase 109 local Ibiza place missing: {slug} -> {place}')
    if '+34 613 75 62 11' in html or '34613756211' in html: raise SystemExit(f'Phase 109 old phone leaked: {slug}')
print('PASS: Phase 109 audit — FR/DE/AR Private Concierge cornerstone pages exceed 450 visible words, expose real Ibiza service areas and route to seven same-language conversion/service paths')

# Phase 110 strengthens internal authority distribution only after the
# multilingual cornerstone layer has passed its own quality gate.
import phase110_enhance
import phase110_audit

# Phase 112 strengthens existing FR/DE/AR Partner pages for international
# DMC/private-travel briefs without adding landing pages or new stylesheets.
import phase112_enhance
import phase112_audit

# Phase 113 connects existing international audience cards to the matching
# local-language service/partner journey and makes representative briefs clearer.
from phase113_enhance import enhance as enhance_enquiry_journeys
from phase113_audit import run as audit_enquiry_journeys
enhance_enquiry_journeys()
audit_enquiry_journeys()

# Phase 114 protects date and validation continuity across all five contact desks.
import phase114_audit

# Phase 115 gives every required phone field native telephone semantics without
# imposing a country-specific pattern on international private-client enquiries.
from phase115_enhance import enhance as enhance_phone_semantics
enhance_phone_semantics()
import phase115_audit

# Phase 116 makes the required buyer-role field genuinely required by starting
# from a localized empty placeholder instead of silently defaulting to private client.
from phase116_enhance import enhance as enhance_buyer_role
from phase116_audit import run as audit_buyer_role
enhance_buyer_role()
audit_buyer_role()

# Phase 111 inspects the final HTML graph after all contextual links are present.
from phase111_audit import run as audit_cornerstone_depth
audit_cornerstone_depth()
