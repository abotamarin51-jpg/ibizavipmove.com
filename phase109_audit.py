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

# Phase 117 anchors date eligibility to Ibiza's calendar day rather than the
# visitor's device timezone, then cache-busts the existing qualified-brief runtime.
from phase117_enhance import enhance as enhance_ibiza_date_runtime
from phase117_audit import run as audit_ibiza_date_runtime
enhance_ibiza_date_runtime()
audit_ibiza_date_runtime()

# Phase 118 makes the required international phone field easier to hand over
# correctly without imposing a fragile country-specific validation pattern.
from phase118_enhance import enhance as enhance_phone_guidance
from phase118_audit import run as audit_phone_guidance
enhance_phone_guidance()
audit_phone_guidance()

# Phase 119 rejects whitespace-only values in the two required free-text fields,
# trims handover values and preserves the existing international phone semantics.
from phase119_enhance import enhance as enhance_required_text
from phase119_audit import run as audit_required_text
enhance_required_text()
audit_required_text()

# Phase 120 rejects clearly incomplete telephone values while keeping formatting
# flexible for international clients and preserving Unicode decimal digits.
from phase120_enhance import enhance as enhance_phone_plausibility
from phase120_audit import run as audit_phone_plausibility
enhance_phone_plausibility()
audit_phone_plausibility()

# Phase 121 keeps sitemap freshness signals truthful: only routes with verified
# significant changes on 12 September receive that lastmod date.
from phase121_enhance import enhance as enhance_sitemap_lastmod
from phase121_audit import run as audit_sitemap_lastmod
enhance_sitemap_lastmod()
audit_sitemap_lastmod()

# Phase 122 removes membership-product wording from contact desks because no
# private membership product or member-only benefit has been authorized.
from phase122_enhance import enhance as enhance_private_client_desk
from phase122_audit import run as audit_private_client_desk
enhance_private_client_desk()
audit_private_client_desk()

# Phase 123 consolidates duplicate operational-evidence blocks on the English
# Partners page while keeping the stronger proof section and authority routes.
from phase123_enhance import enhance as enhance_partner_proof
from phase123_audit import run as audit_partner_proof
enhance_partner_proof()
audit_partner_proof()

# Phase 124 prevents build time from masquerading as editorial freshness. The
# Black Book Article schema and social modified-time signal follow only verified
# sitemap lastmod values; undated entries remain intentionally undated.
from phase124_enhance import enhance as enhance_black_book_freshness
from phase124_audit import run as audit_black_book_freshness
enhance_black_book_freshness()
audit_black_book_freshness()

# Phase 111 inspects the final HTML graph after all contextual links are present.
from phase111_audit import run as audit_cornerstone_depth
audit_cornerstone_depth()
