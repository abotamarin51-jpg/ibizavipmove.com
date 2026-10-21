"""Preserve the French Services pathway, then apply the English conversion phases."""
from pathlib import Path
from phase179_enhance import enhance as enhance_private_office_handoff
from phase180_enhance import enhance as enhance_vip_tables_page
from phase181_accessibility_fix import enhance as enhance_vip_tables_language_target
from phase182_private_client_context import enhance as enhance_private_client_context
from phase183_travel_concierge_context import enhance as enhance_travel_concierge_context


# One Home-only editorial refinement. Preserve SEO metadata, headings, layout and contact routes.
HOME = Path('_site/index.html')
HOME_SITEMAP = Path('_site/sitemap.xml')
HOME_OLD_LEAD = '<p class="ivm-seo-lead">Ibiza VIP Move is a luxury concierge in Ibiza for private clients and professional teams who want one discreet on-island point of coordination.</p>'
HOME_NEW_LEAD = '<p class="ivm-seo-lead">Our Ibiza concierge service helps private clients, personal assistants, family offices and luxury travel advisors plan their stay through one discreet local contact.</p>'
HOME_OLD_SERVICE = '<p>Private chauffeur, villas, yachts, aviation, access and protection are coordinated around the stay rather than treated as isolated bookings.</p>'
HOME_NEW_SERVICE = '<p>We coordinate chauffeur transport, villas, yachts, aviation, VIP hospitality requests and security around each stay.</p>'
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
    updated = html.replace(HOME_OLD_LEAD, HOME_NEW_LEAD, 1).replace(
        HOME_OLD_SERVICE, HOME_NEW_SERVICE, 1)
    if (updated.split('</head>', 1)[0] != html.split('</head>', 1)[0]
            or updated.count('<h1') != html.count('<h1')
            or updated.count('<a ') != html.count('<a ')
            or updated.count('<script') != html.count('<script')
            or updated.count('<img ') != html.count('<img ')):
        raise SystemExit('Home clarity: unexpected structure or head drift')
    new_sitemap = sitemap.replace(HOME_OLD_LASTMOD, HOME_NEW_LASTMOD, 1)
    # All preconditions and output invariants checked before either write.
    HOME.write_text(updated, encoding='utf-8')
    HOME_SITEMAP.write_text(new_sitemap, encoding='utf-8')
    print('PASS: Home clarity — two concise paragraphs, exact Ibiza concierge wording and Home-only lastmod')


if __name__ == '__main__':
    enhance()
    enhance_private_office_handoff()
    enhance_vip_tables_page()
    enhance_vip_tables_language_target()
    enhance_home_readability()
    enhance_private_client_context()
    enhance_travel_concierge_context()
