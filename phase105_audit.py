from pathlib import Path
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PAGES = {
    '/': '/case-studies/',
    '/private-concierge-ibiza/': '/case-studies/weekend-concierge-two-guests/',
    '/luxury-lifestyle-management-ibiza/': '/case-studies/weekend-concierge-two-guests/',
    '/personal-concierge-ibiza/': '/case-studies/weekend-concierge-two-guests/',
    '/luxury-travel-concierge-ibiza/': '/case-studies/private-aviation-arrival-seven-guests/',
    '/vip-services-ibiza/': '/case-studies/late-night-dual-vehicle-arrival/',
    '/private-client-services-ibiza/': '/case-studies/principal-chauffeur-security-three-days/',
    '/destination-management-ibiza/': '/case-studies/multi-day-executive-chauffeur-program/',
    '/private-chauffeur-ibiza/': '/case-studies/multi-day-executive-chauffeur-program/',
    '/private-aviation-ibiza/': '/case-studies/private-aviation-arrival-seven-guests/',
    '/private-security-ibiza/': '/case-studies/principal-chauffeur-security-three-days/',
    '/luxury-villas-ibiza/': '/case-studies/weekend-concierge-two-guests/',
    '/yacht-charter-ibiza/': '/ibiza-luxury-operations-report-2026/',
    '/partners/': '/case-studies/',
    '/private-office/': '/case-studies/principal-chauffeur-security-three-days/',
    '/international-clients/': '/case-studies/private-aviation-arrival-seven-guests/',
    '/private-concierge-marina-botafoch-ibiza/': '/case-studies/late-night-dual-vehicle-arrival/',
    '/private-concierge-cala-jondal-es-cubells-ibiza/': '/ibiza-luxury-operations-report-2026/',
    '/private-concierge-santa-eulalia-roca-llisa-ibiza/': '/ibiza-luxury-operations-report-2026/',
    '/private-concierge-santa-gertrudis-ibiza/': '/ibiza-luxury-operations-report-2026/',
}
EVIDENCE_TARGETS = [
    '/founder/',
    '/case-studies/',
    '/ibiza-luxury-operations-report-2026/',
]


def page(path):
    return ROOT / 'index.html' if path == '/' else ROOT / path.strip('/') / 'index.html'


def canonical(html):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    return m.group(1) if m else ''


for evidence in EVIDENCE_TARGETS:
    if not page(evidence).exists():
        raise SystemExit(f'Phase 105 evidence target missing: {evidence}')

for path, related in PAGES.items():
    target = page(path)
    if not target.exists():
        raise SystemExit(f'Phase 105 page missing: {path}')
    html = target.read_text(encoding='utf-8')
    expected = BASE + path if path != '/' else BASE + '/'
    if canonical(html) != expected:
        raise SystemExit(f'Phase 105 canonical drift: {path} -> {canonical(html)}')
    if html.count('ivm-phase105-proof') != 1:
        raise SystemExit(f'Phase 105 proof cardinality mismatch: {path}')
    section = re.search(r'<section\b[^>]*ivm-phase105-proof[^>]*>(.*?)</section>', html, re.I | re.S)
    if not section:
        raise SystemExit(f'Phase 105 proof section malformed: {path}')
    block = section.group(1)
    for required in ('/case-studies/', '/ibiza-luxury-operations-report-2026/', '/founder/'):
        if required not in block:
            raise SystemExit(f'Phase 105 required evidence link missing: {path} -> {required}')
    if related not in block:
        raise SystemExit(f'Phase 105 related evidence mismatch: {path} -> {related}')
    if 'rel="author" href="/founder/"' not in block:
        raise SystemExit(f'Phase 105 founder author relationship missing: {path}')
    if len(re.findall(r'<a\b', block, re.I)) != 4:
        raise SystemExit(f'Phase 105 expected four proof links: {path}')
    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit(f'Phase 105 H1 drift: {path}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 105 accessibility drift: {path}')

# Distribution should be meaningful: the three evidence hubs must now receive
# links from the entire 20-page high-intent decision set.
all_html = '\n'.join(page(path).read_text(encoding='utf-8') for path in PAGES)
if all_html.count('href="/case-studies/"') < len(PAGES):
    raise SystemExit('Phase 105 case-study hub distribution unexpectedly low')
if all_html.count('href="/ibiza-luxury-operations-report-2026/"') < len(PAGES):
    raise SystemExit('Phase 105 report distribution unexpectedly low')
if all_html.count('rel="author" href="/founder/"') != len(PAGES):
    raise SystemExit('Phase 105 founder author-link distribution mismatch')

# Do not turn evidence pages themselves into recursive commercial proof modules.
for path in EVIDENCE_TARGETS:
    html = page(path).read_text(encoding='utf-8')
    if 'ivm-phase105-proof' in html:
        raise SystemExit(f'Phase 105 recursive evidence module found: {path}')

print(f'PASS: Phase 105 audit — {len(PAGES)} high-intent pages route visibly to founder, case studies and the 2026 operations report with canonicals, H1s and accessibility preserved')
