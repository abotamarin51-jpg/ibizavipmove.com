"""Regression checks for the French Services pathway and English conversion phases."""
from html.parser import HTMLParser
from pathlib import Path
from phase179_audit import run as audit_private_office_handoff
from phase180_audit import run as audit_vip_tables_page
from phase181_accessibility_audit import run as audit_vip_tables_language_target
from phase182_private_client_context import audit as audit_private_client_context
from phase183_travel_concierge_context import audit as audit_travel_concierge_context
from phase184_lifestyle_context import audit as audit_lifestyle_context
from phase185_personal_concierge_context import audit as audit_personal_concierge_context
from phase186_vip_services_context import audit as audit_vip_services_context
from phase178_enhance import (
    HOME, HOME_SITEMAP, HOME_NEW_LEAD, HOME_NEW_SERVICE, HOME_OLD_LEAD,
    HOME_OLD_SERVICE, HOME_NEW_LASTMOD, HOME_OLD_LASTMOD,
    FR_INTL, FR_INTL_FORM_OLD, FR_INTL_FORM_NEW,
)

SERVICES = Path('_site/fr/services/index.html')
CONCIERGE = Path('_site/fr/conciergerie-privee-ibiza/index.html')
TARGET = '/fr/conciergerie-privee-ibiza/'
SNIPPET = 'Passez par la <a class="text-link" href="/fr/conciergerie-privee-ibiza/">conciergerie privée</a> plutôt que de gérer chaque catégorie séparément.'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def canonical_is(html, url):
    return any(
        tag == 'link'
        and attrs.get('rel') == 'canonical'
        and attrs.get('href') == url
        for tag, attrs in Tags(html).tags
    )


def is_noindex(html):
    return any(
        tag == 'meta'
        and attrs.get('name', '').lower() == 'robots'
        and 'noindex' in attrs.get('content', '').lower()
        for tag, attrs in Tags(html).tags
    )


def run():
    services = SERVICES.read_text(encoding='utf-8')
    concierge = CONCIERGE.read_text(encoding='utf-8')

    if services.count(SNIPPET) != 1:
        raise SystemExit('Phase 178 audit: contextual French Concierge pathway missing or duplicated')

    target_links = sum(
        1 for tag, attrs in Tags(services).tags
        if tag == 'a' and attrs.get('href') == TARGET
    )
    if target_links != 3:
        raise SystemExit(f'Phase 178 audit: expected nav + mobile + contextual links, got {target_links}')

    if not canonical_is(services, 'https://ibizavipmove.com/fr/services/'):
        raise SystemExit('Phase 178 audit: French Services self-canonical changed')
    if not canonical_is(concierge, 'https://ibizavipmove.com/fr/conciergerie-privee-ibiza/'):
        raise SystemExit('Phase 178 audit: French Concierge self-canonical changed')
    if is_noindex(services) or is_noindex(concierge):
        raise SystemExit('Phase 178 audit: French Services or Concierge became noindex')

    if '<h1>Votre conciergerie privée à Ibiza</h1>' not in concierge:
        raise SystemExit('Phase 178 audit: French Concierge target identity changed')

    international = FR_INTL.read_text(encoding='utf-8')
    expected_international = (
        'Coordonnez votre demande à Ibiza.',
        'Envoyez-nous vos dates, le nombre d’invités et les services souhaités. Un interlocuteur à Ibiza poursuivra la conversation en privé et vous indiquera les prochaines étapes.',
        'Contacter la conciergerie sur WhatsApp',
        'E-mail pour partenaires et demandes professionnelles',
        FR_INTL_FORM_NEW,
    )
    if not all(text in international for text in expected_international):
        raise SystemExit('Phase 178 audit: approved French international contact copy missing')
    if ('Coordonnez votre brief à Ibiza.' in international
            or '>Email Partnerships</a>' in international
            or FR_INTL_FORM_OLD in international):
        raise SystemExit('Phase 178 audit: old French international contact copy still present')
    if (not canonical_is(international, 'https://ibizavipmove.com/fr/clients-internationaux/')
            or is_noindex(international)
            or 'https://wa.me/34600703303' not in international
            or 'mailto:partnership@ibizavipmove.com' not in international
            or '/fr/contact/' not in international):
        raise SystemExit('Phase 178 audit: French international routes or indexability changed')

    print('PASS: Phase 178 audit — French contextual Concierge pathway; canonicals/indexability unchanged')



def audit_home_clarity():
    html = HOME.read_text(encoding='utf-8')
    sitemap = HOME_SITEMAP.read_text(encoding='utf-8')
    if (html.count(HOME_NEW_LEAD) != 1 or html.count(HOME_NEW_SERVICE) != 1
            or HOME_OLD_LEAD in html or HOME_OLD_SERVICE in html):
        raise SystemExit('Home clarity audit: expected only the reviewed new paragraphs')
    if (html.count('<title>Luxury Concierge Ibiza | Ibiza VIP Move</title>') != 1
            or html.count('<h1>Luxury concierge in Ibiza,<br>handled privately.</h1>') != 1
            or not canonical_is(html, 'https://ibizavipmove.com/')
            or is_noindex(html)):
        raise SystemExit('Home clarity audit: Home SEO identity or indexability changed')
    if ('https://wa.me/34600703303' not in html
            or 'tel:+34600703303' not in html
            or 'partnership@ibizavipmove.com' not in html):
        raise SystemExit('Home clarity audit: existing approved contact route missing')
    if (sitemap.count(HOME_NEW_LASTMOD) != 1 or HOME_OLD_LASTMOD in sitemap
            or sitemap.count('<url>') != 157):
        raise SystemExit('Home clarity audit: unexpected sitemap inventory or Home lastmod')
    print('PASS: Home clarity audit — revised paragraphs, Home SEO and contacts, 157-URL sitemap')


if __name__ == '__main__':
    run()
    audit_private_office_handoff()
    audit_vip_tables_page()
    audit_vip_tables_language_target()
    audit_home_clarity()
    audit_private_client_context()
    audit_travel_concierge_context()
    audit_lifestyle_context()
    audit_personal_concierge_context()
    audit_vip_services_context()
