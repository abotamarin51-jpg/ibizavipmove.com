from pathlib import Path
from html import escape
import re

ROOT = Path('_site')

PAGES = {
    '/': ('Operational proof before the brief.', '/case-studies/', 'Browse real operating cases'),
    '/private-concierge-ibiza/': ('See how private coordination works in practice.', '/case-studies/weekend-concierge-two-guests/', 'Weekend concierge case'),
    '/luxury-lifestyle-management-ibiza/': ('See a multi-service stay translated into one operating brief.', '/case-studies/weekend-concierge-two-guests/', 'Lifestyle coordination case'),
    '/personal-concierge-ibiza/': ('See the difference between requests and connected execution.', '/case-studies/weekend-concierge-two-guests/', 'Personal concierge case'),
    '/luxury-travel-concierge-ibiza/': ('See how arrival and on-island logistics are connected.', '/case-studies/private-aviation-arrival-seven-guests/', 'Private aviation arrival case'),
    '/vip-services-ibiza/': ('See how VIP hospitality depends on the operating detail.', '/case-studies/late-night-dual-vehicle-arrival/', 'Late-night VIP logistics case'),
    '/private-client-services-ibiza/': ('See the operating model behind principal-level support.', '/case-studies/principal-chauffeur-security-three-days/', 'Principal support case'),
    '/destination-management-ibiza/': ('See the local operating layer behind a professional client brief.', '/case-studies/multi-day-executive-chauffeur-program/', 'Professional client case'),
    '/private-chauffeur-ibiza/': ('See how a chauffeur program is coordinated beyond a single transfer.', '/case-studies/multi-day-executive-chauffeur-program/', 'Multi-day chauffeur case'),
    '/private-aviation-ibiza/': ('See how flight timing, luggage and vehicles become one arrival plan.', '/case-studies/private-aviation-arrival-seven-guests/', 'Private aviation arrival case'),
    '/private-security-ibiza/': ('See how chauffeur and licensed security can be aligned around one principal.', '/case-studies/principal-chauffeur-security-three-days/', 'Chauffeur + security case'),
    '/luxury-villas-ibiza/': ('See how villa timing connects with transport and the wider stay.', '/case-studies/weekend-concierge-two-guests/', 'Private stay case'),
    '/yacht-charter-ibiza/': ('See the operational principles used to connect sea days with the rest of the itinerary.', '/ibiza-luxury-operations-report-2026/', 'Read the 2026 field report'),
    '/partners/': ('Evidence for travel advisors, concierge firms and professional partners.', '/case-studies/', 'Review operating cases'),
    '/private-office/': ('Operational evidence for PAs, family offices and principals.', '/case-studies/principal-chauffeur-security-three-days/', 'Principal support case'),
    '/international-clients/': ('See how international travel briefs translate into local Ibiza execution.', '/case-studies/private-aviation-arrival-seven-guests/', 'International arrival case'),
    '/private-concierge-marina-botafoch-ibiza/': ('See the evidence behind marina, city and late-night coordination.', '/case-studies/late-night-dual-vehicle-arrival/', 'Late-night logistics case'),
    '/private-concierge-cala-jondal-es-cubells-ibiza/': ('See the field principles behind south-Ibiza private stays.', '/ibiza-luxury-operations-report-2026/', '2026 operations report'),
    '/private-concierge-santa-eulalia-roca-llisa-ibiza/': ('See the field principles behind multi-day private stays.', '/ibiza-luxury-operations-report-2026/', '2026 operations report'),
    '/private-concierge-santa-gertrudis-ibiza/': ('See the field principles behind central-Ibiza villa logistics.', '/ibiza-luxury-operations-report-2026/', '2026 operations report'),
}


def page(path):
    if path == '/':
        return ROOT / 'index.html'
    return ROOT / path.strip('/') / 'index.html'


def evidence_section(title, case_url, case_label):
    return (
        '<section class="partners-strip ivm-phase105-proof" aria-label="Operational evidence">'
        '<div><div class="kicker dark">Operational evidence</div>'
        f'<h2>{escape(title)}</h2>'
        '<p>Ibiza VIP Move publishes anonymized operating cases and field observations so private clients and professional partners can evaluate how the coordination model works before sending a brief.</p>'
        '<p>'
        f'<a class="text-link" href="{escape(case_url, quote=True)}">{escape(case_label)}</a> · '
        '<a class="text-link" href="/ibiza-luxury-operations-report-2026/">Ibiza Luxury Operations Report 2026</a> · '
        '<a class="text-link" rel="author" href="/founder/">Founder: Juan Cruz</a>'
        '</p></div>'
        '<a class="btn dark" href="/case-studies/">View operational evidence</a>'
        '</section>'
    )


for path, (title, case_url, case_label) in PAGES.items():
    target = page(path)
    if not target.exists():
        raise SystemExit(f'Phase 105 target missing: {path}')
    html = target.read_text(encoding='utf-8')
    if 'ivm-phase105-proof' in html:
        raise SystemExit(f'Phase 105 duplicate proof section: {path}')
    section = evidence_section(title, case_url, case_label)

    # Keep operational evidence close to the decision point: immediately before
    # the page's final closing CTA when one exists, otherwise before </main>.
    closings = list(re.finditer(r'<section\b[^>]*class="[^"]*closing[^\"]*"', html, re.I))
    if closings:
        pos = closings[-1].start()
        html = html[:pos] + section + html[pos:]
    elif '</main>' in html:
        html = html.replace('</main>', section + '</main>', 1)
    else:
        raise SystemExit(f'Phase 105 no insertion point: {path}')
    target.write_text(html, encoding='utf-8')

print(f'PASS: Phase 105 authority distribution — operational evidence connected to {len(PAGES)} high-intent commercial and local pages without creating new indexable URLs')
