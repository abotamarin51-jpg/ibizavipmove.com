"""Regression checks for the Private Chauffeur -> Luxury Car Hire pathway."""
from html.parser import HTMLParser
from pathlib import Path

CHAUFFEUR = Path('_site/private-chauffeur-ibiza/index.html')
CAR = Path('_site/luxury-car-rental-ibiza/index.html')
CAR_PATH = '/luxury-car-rental-ibiza/'
SNIPPET = 'For self-drive requests, see <a class="text-link" href="/luxury-car-rental-ibiza/">Luxury Car Hire &amp; Rental</a>.'


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
    chauffeur = CHAUFFEUR.read_text(encoding='utf-8')
    car = CAR.read_text(encoding='utf-8')

    if chauffeur.count(SNIPPET) != 1:
        raise SystemExit('Phase 177 audit: contextual Car Hire pathway missing or duplicated')

    target_links = sum(
        1 for tag, attrs in Tags(chauffeur).tags
        if tag == 'a' and attrs.get('href') == CAR_PATH
    )
    if target_links != 1:
        raise SystemExit(f'Phase 177 audit: expected one Chauffeur-to-Car-Hire link, got {target_links}')

    if not canonical_is(chauffeur, 'https://ibizavipmove.com/private-chauffeur-ibiza/'):
        raise SystemExit('Phase 177 audit: Chauffeur self-canonical changed')
    if not canonical_is(car, 'https://ibizavipmove.com/luxury-car-rental-ibiza/'):
        raise SystemExit('Phase 177 audit: Car Hire self-canonical changed')
    if is_noindex(chauffeur) or is_noindex(car):
        raise SystemExit('Phase 177 audit: Chauffeur or Car Hire became noindex')

    if 'Luxury Car Hire &amp; Rental Ibiza' not in car:
        raise SystemExit('Phase 177 audit: target Car Hire page identity changed')

    print('PASS: Phase 177 audit — one Chauffeur-to-Car-Hire pathway; target identity/canonicals/indexability unchanged')


if __name__ == '__main__':
    run()
