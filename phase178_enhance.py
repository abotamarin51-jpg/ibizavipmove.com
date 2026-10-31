"""Preserve the French Services pathway, then apply the English conversion phases."""
from pathlib import Path
import re
from phase179_enhance import enhance as enhance_private_office_handoff
from phase180_enhance import enhance as enhance_vip_tables_page
from phase181_accessibility_fix import enhance as enhance_vip_tables_language_target
from phase182_private_client_context import enhance as enhance_private_client_context
from phase183_travel_concierge_context import enhance as enhance_travel_concierge_context
from phase184_lifestyle_context import enhance as enhance_lifestyle_context
from phase185_personal_concierge_context import enhance as enhance_personal_concierge_context
from phase186_vip_services_context import enhance as enhance_vip_services_context
from phase187_google_maps_profile import add_google_maps_profile_links
from phase188_customer_questions import enhance as enhance_customer_questions
from phase188_audit import audit as audit_customer_questions


# One Home-only editorial refinement. Preserve SEO metadata, headings, layout and contact routes.
HOME = Path('_site/index.html')
HOME_SITEMAP = Path('_site/sitemap.xml')
HOME_OLD_LEAD = '<p class="ivm-seo-lead">Ibiza VIP Move is a luxury concierge in Ibiza for private clients and professional teams who want one discreet on-island point of coordination.</p>'
HOME_NEW_LEAD = '<p class="ivm-seo-lead">Our Ibiza concierge service helps private clients, personal assistants, family offices and luxury travel advisors plan their stay through one discreet local contact.</p>'
HOME_OLD_SERVICE = '<p>Private chauffeur, villas, yachts, aviation, access and protection are coordinated around the stay rather than treated as isolated bookings.</p>'
HOME_NEW_SERVICE = '<p>We coordinate chauffeur transport, villas, yachts, aviation, <a href="/vip-services-ibiza/" style="color:inherit;text-decoration:underline;text-underline-offset:.16em">VIP hospitality requests</a> and security around each stay.</p>'
HOME_OLD_LASTMOD = '<loc>https://ibizavipmove.com/</loc><lastmod>2026-09-03</lastmod>'
HOME_NEW_LASTMOD = '<loc>https://ibizavipmove.com/</loc><lastmod>2026-10-21</lastmod>'

PATH = Path('_site/fr/services/index.html')
OLD = 'Passez par le concierge plutôt que de gérer chaque catégorie séparément. Partagez dates, invités et priorités ; nous clarifions le brief et poursuivons en privé.'
NEW = 'Passez par la <a class="text-link" href="/fr/conciergerie-privee-ibiza/">conciergerie privée</a> plutôt que de gérer chaque catégorie séparément. Partagez dates, invités et priorités ; nous clarifions le brief et poursuivons en privé.'


def enhance():
    html = PATH.read_text(encoding='utf-8')
    if NEW in html:
        if html.count(NEW) != 1:
            raise SystemExit('Phase 178: duplicate French Services-to-Concierge pathway')
        print('PASS: Phase 178 — French Services-to-Concierge pathway already present')
        return

    if html.count(OLD) != 1:
        raise SystemExit('Phase 178: expected one French concierge coordination sentence')

    PATH.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 178 — one French Services-to-Concierge pathway added')



def enhance_home_readability():
    """Change two existing paragraphs, plus truthful Home sitemap freshness only."""
    if not HOME.is_file() or not HOME_SITEMAP.is_file():
        raise SystemExit('Home clarity: source Home or sitemap missing')
    html = HOME.read_text(encoding='utf-8')
    sitemap = HOME_SITEMAP.read_text(encoding='utf-8')
    if (html.count(HOME_NEW_LEAD) == 1 and html.count(HOME_NEW_SERVICE) == 1
            and HOME_OLD_LEAD not in html and HOME_OLD_SERVICE not in html):
        if sitemap.count(HOME_NEW_LASTMOD) != 1 or HOME_OLD_LASTMOD in sitemap:
            raise SystemExit('Home clarity: already-updated copy and sitemap disagree')
        print('PASS: Home clarity — already applied, no duplicate content')
        return
    if (html.count(HOME_OLD_LEAD) != 1 or html.count(HOME_OLD_SERVICE) != 1
            or HOME_NEW_LEAD in html or HOME_NEW_SERVICE in html):
        raise SystemExit('Home clarity: expected existing paragraphs not unique')
    if sitemap.count(HOME_OLD_LASTMOD) != 1 or HOME_NEW_LASTMOD in sitemap:
        raise SystemExit('Home clarity: expected one historical Home sitemap lastmod')
    if html.count('<link rel="canonical" href="https://ibizavipmove.com/">') != 1:
        raise SystemExit('Home clarity: wrong Home canonical')
    vip_target = Path('_site/vip-services-ibiza/index.html')
    if (not vip_target.is_file() or
            vip_target.read_text(encoding='utf-8').count('<link rel="canonical" href="https://ibizavipmove.com/vip-services-ibiza/">') != 1):
        raise SystemExit('Home VIP link: confirmed canonical destination missing')
    updated = html.replace(HOME_OLD_LEAD, HOME_NEW_LEAD, 1).replace(
        HOME_OLD_SERVICE, HOME_NEW_SERVICE, 1)
    if (updated.split('</head>', 1)[0] != html.split('</head>', 1)[0]
            or updated.count('<h1') != html.count('<h1')
            or updated.count('<a ') != html.count('<a ') + 1
            or updated.count('<script') != html.count('<script')
            or updated.count('<img ') != html.count('<img ')):
        raise SystemExit('Home clarity: unexpected structure or head drift')
    new_sitemap = sitemap.replace(HOME_OLD_LASTMOD, HOME_NEW_LASTMOD, 1)
    # All preconditions and output invariants checked before either write.
    HOME.write_text(updated, encoding='utf-8')
    HOME_SITEMAP.write_text(new_sitemap, encoding='utf-8')
    print('PASS: Home clarity — two concise paragraphs, exact Ibiza concierge wording and Home-only lastmod')


def enhance_villa_staffing_brief():
    """Explain the staffing brief beside the existing English villa overview."""
    path = Path('_site/luxury-villas-ibiza/index.html')
    target = Path('_site/private-chef-staffing-ibiza/index.html')
    sitemap_path = Path('_site/sitemap.xml')
    url = 'https://ibizavipmove.com/luxury-villas-ibiza/'
    detail = '<p>We focus on the complete stay rather than a property alone. Availability, terms and supplier details are confirmed for the specific request before any reservation is accepted.</p>'
    guidance = (
        '<p>For chef or villa-staffing requests, share the dates, guest count, meals '
        'and daily service hours. Before confirming, check the written scope for '
        'staff duties, food shopping and any additional hours.</p>'
        '<a class="text-link" href="/private-chef-staffing-ibiza/">'
        'Plan private chefs and villa staffing →</a>'
    )
    html = path.read_text(encoding='utf-8')
    target_html = target.read_text(encoding='utf-8')
    sitemap = sitemap_path.read_text(encoding='utf-8')
    if html.count(f'<link rel="canonical" href="{url}">') != 1:
        raise SystemExit('Villa staffing brief: unexpected source canonical')
    if '<link rel="canonical" href="https://ibizavipmove.com/private-chef-staffing-ibiza/">' not in target_html:
        raise SystemExit('Villa staffing brief: expected staffing destination missing')
    if html.count(detail) != 1 or html.count(guidance) > 1:
        raise SystemExit('Villa staffing brief: expected one overview and no duplicate guidance')
    updated = html if guidance in html else html.replace(detail, detail + guidance, 1)
    if updated.split('</head>', 1)[0] != html.split('</head>', 1)[0]:
        raise SystemExit('Villa staffing brief: unexpected metadata change')
    pattern = rf'(<url><loc>{re.escape(url)}</loc><lastmod>)[^<]+(</lastmod>)'
    sitemap, count = re.subn(pattern, r'\g<1>2026-10-27\g<2>', sitemap)
    if count != 1:
        raise SystemExit('Villa staffing brief: expected one existing sitemap entry')
    path.write_text(updated, encoding='utf-8')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print('PASS: Villa staffing brief — practical scope guidance and existing staffing route')


def enhance_assistant_villa_checklist():
    """Add an assistant's practical brief to the existing English villa note."""
    from phase124_enhance import MOD_META_RE, rewrite_article_schema

    article_path = Path('_site/ibiza-intelligence/villa-arrival-planning/index.html')
    office_path = Path('_site/private-office/index.html')
    sitemap_path = Path('_site/sitemap.xml')
    article_url = 'https://ibizavipmove.com/ibiza-intelligence/villa-arrival-planning/'
    office_url = 'https://ibizavipmove.com/private-office/'
    checklist = '''<section id="assistant-villa-checklist">
<h2>An executive assistant's checklist for an Ibiza villa stay.</h2>
<p>When arranging a villa stay for a principal or family, keep the property, arrivals and first reservations in one current brief. Start with these details so the local team can check the dependencies before services are confirmed.</p>
<ul class="premium-list">
<li><strong>Stay dates and guest requirements.</strong> Confirm the local check-in and check-out dates, overnight guest count and any separate arrivals. Flag practical requirements such as child seats or step-free access where relevant to the requested service.</li>
<li><strong>Property access and handover.</strong> Confirm the agreed access time, the person meeting the guests and the contact who can resolve a delayed arrival. If the villa is already booked, share the confirmed location privately with the team coordinating the arrival. Keep the written property terms with the booking record.</li>
<li><strong>Flight times, luggage and vehicles.</strong> Share flight details, passenger count, luggage volume and the onward destination when requesting <a href="/private-chauffeur-ibiza/">chauffeur coordination</a>. For travel from the United States, use the Ibiza arrival date and local time shown on the itinerary; an overnight flight may arrive on a different calendar date from departure.</li>
<li><strong>Villa readiness and staffing.</strong> List the first meal, provisioning and any <a href="/private-chef-staffing-ibiza/">private chef or villa-staffing requirements</a>. Check guest numbers, service hours, duties, shopping and additional charges in the written scope. Treat requested extras separately from services already included in the property booking.</li>
<li><strong>The first confirmed plans.</strong> Put dining, yacht departures and the next transport movement beside the villa handover time. Keep the first day realistic and identify which reservations can move if the arrival changes. Availability and applicable supplier terms still need confirmation for each request.</li>
<li><strong>Approval and communication.</strong> Name the person who may approve requests or extra costs, the preferred channel and the reply time zone. Agree whether communication stays through the assistant or includes the principal. Share only the details each supplier needs for the agreed service.</li>
<li><strong>Changes and the final handover.</strong> Keep one latest itinerary with requests marked as pending or confirmed. If flight timing, guest numbers or access changes, review the affected vehicles, property handover, staffing and reservations together. Agree who receives the updated version.</li>
</ul>
<p><strong>A useful first message:</strong> stay dates; accommodation area; guests and separate arrivals; confirmed flight times; required services; first priorities; reply time zone; and the person approving requests. Identity documents and bank details are not needed in that initial enquiry.</p>
<p>Use the checklist to prepare the brief, then explore <a href="/luxury-villas-ibiza/">private villa coordination</a> or <a href="/private-client-services-ibiza/">support for principals and their representatives</a> for the relevant service.</p>
</section>'''
    office_link = '<p id="assistant-villa-guide">Planning a villa stay? Use the <a class="text-link" href="/ibiza-intelligence/villa-arrival-planning/#assistant-villa-checklist">executive assistant\'s villa checklist</a> to prepare access, arrivals, staffing and approvals before sending the brief.</p>'
    office_anchor = '<p data-ivm179="brief">For the first message, share the dates, guest count, required services and your role. Include your time zone, who may approve requests and whether communication should stay through you. Identity documents or bank details are not needed in the first message.</p>'
    article = article_path.read_text(encoding='utf-8')
    office = office_path.read_text(encoding='utf-8')
    sitemap = sitemap_path.read_text(encoding='utf-8')
    for html, canonical in ((article, article_url), (office, office_url)):
        if html.count(f'<link rel="canonical" href="{canonical}">') != 1:
            raise SystemExit('Assistant villa guide: unexpected canonical')
    if article.count('<aside class="article-cta">') != 1 or office.count(office_anchor) != 1:
        raise SystemExit('Assistant villa guide: expected insertion point missing')
    if article.count('id="assistant-villa-checklist"') > 1 or office.count('id="assistant-villa-guide"') > 1:
        raise SystemExit('Assistant villa guide: duplicate guide content')
    if 'id="assistant-villa-checklist"' in article and checklist not in article:
        raise SystemExit('Assistant villa guide: existing checklist differs from source')
    if 'id="assistant-villa-guide"' in office and office_link not in office:
        raise SystemExit('Assistant villa guide: existing office link differs from source')
    updated_article = article if checklist in article else article.replace('<aside class="article-cta">', checklist + '<aside class="article-cta">', 1)
    updated_office = office if office_link in office else office.replace(office_anchor, office_anchor + office_link, 1)
    for route in ('private-chauffeur-ibiza', 'private-chef-staffing-ibiza', 'luxury-villas-ibiza', 'private-client-services-ibiza'):
        target = Path('_site') / route / 'index.html'
        if not target.is_file() or f'href="https://ibizavipmove.com/{route}/"' not in target.read_text(encoding='utf-8'):
            raise SystemExit(f'Assistant villa guide: missing canonical destination {route}')
    updated_article = rewrite_article_schema(updated_article, article_url, '2026-10-27')
    updated_article = MOD_META_RE.sub('', updated_article).replace('</head>', '<meta property="article:modified_time" content="2026-10-27"></head>', 1)
    if updated_office.split('</head>', 1)[0] != office.split('</head>', 1)[0]:
        raise SystemExit('Assistant villa guide: unexpected Private Office head change')
    for url in (article_url, office_url):
        pattern = rf'(<url><loc>{re.escape(url)}</loc><lastmod>)[^<]+(</lastmod>)'
        sitemap, count = re.subn(pattern, r'\g<1>2026-10-27\g<2>', sitemap)
        if count != 1:
            raise SystemExit('Assistant villa guide: expected existing sitemap entry')
    article_path.write_text(updated_article, encoding='utf-8')
    office_path.write_text(updated_office, encoding='utf-8')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print('PASS: Assistant villa checklist — existing English article, Private Office pathway and verified freshness')


if __name__ == '__main__':
    enhance()
    enhance_private_office_handoff()
    enhance_vip_tables_page()
    enhance_vip_tables_language_target()
    enhance_home_readability()
    enhance_private_client_context()
    enhance_travel_concierge_context()
    enhance_lifestyle_context()
    enhance_personal_concierge_context()
    enhance_vip_services_context()
    enhance_villa_staffing_brief()
    enhance_assistant_villa_checklist()
    add_google_maps_profile_links()
    enhance_customer_questions()
    audit_customer_questions()
