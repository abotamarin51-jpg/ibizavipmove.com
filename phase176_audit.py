"""Regression checks for the reciprocal Yacht Charter <-> Formentera guide pathway."""
from html.parser import HTMLParser
from pathlib import Path

YACHT = Path('_site/yacht-charter-ibiza/index.html')
GUIDE = Path('_site/ibiza-intelligence/ibiza-formentera-yacht-day/index.html')
GUIDE_PATH = '/ibiza-intelligence/ibiza-formentera-yacht-day/'
YACHT_PATH = '/yacht-charter-ibiza/'
SNIPPET = '<a class="text-link" href="/ibiza-intelligence/ibiza-formentera-yacht-day/">Formentera</a> can be requested where suitable for the confirmed charter and conditions.'


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
    yacht = YACHT.read_text(encoding='utf-8')
    guide = GUIDE.read_text(encoding='utf-8')

    if yacht.count(SNIPPET) != 1:
        raise SystemExit('Phase 176 audit: Yacht contextual guide link missing or duplicated')

    yacht_to_guide = sum(
        1 for tag, attrs in Tags(yacht).tags
        if tag == 'a' and attrs.get('href') == GUIDE_PATH
    )
    if yacht_to_guide != 1:
        raise SystemExit(f'Phase 176 audit: expected one Yacht-to-guide HTML link, got {yacht_to_guide}')

    guide_to_yacht = sum(
        1 for tag, attrs in Tags(guide).tags
        if tag == 'a' and attrs.get('href') == YACHT_PATH
    )
    if guide_to_yacht < 1:
        raise SystemExit('Phase 176 audit: existing guide-to-Yacht visible pathway missing')

    if not canonical_is(yacht, 'https://ibizavipmove.com/yacht-charter-ibiza/'):
        raise SystemExit('Phase 176 audit: Yacht self-canonical changed')
    if not canonical_is(guide, 'https://ibizavipmove.com/ibiza-intelligence/ibiza-formentera-yacht-day/'):
        raise SystemExit('Phase 176 audit: guide self-canonical changed')
    if is_noindex(yacht) or is_noindex(guide):
        raise SystemExit('Phase 176 audit: Yacht or guide became noindex')

    print('PASS: Phase 176 audit — reciprocal Yacht/Formentera pathway; canonical/indexability unchanged')


if __name__ == '__main__':
    run()
