"""Regression checks for the French Services -> Private Concierge pathway."""
from html.parser import HTMLParser
from pathlib import Path

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

    if '<h1>Conciergerie privée à Ibiza, gérée comme un seul service.</h1>' not in concierge:
        raise SystemExit('Phase 178 audit: French Concierge target identity changed')

    print('PASS: Phase 178 audit — French contextual Concierge pathway; canonicals/indexability unchanged')


if __name__ == '__main__':
    run()
