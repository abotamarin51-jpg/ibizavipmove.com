"""Regression checks for the Phase 175 Services -> Private Concierge pathway."""
from html.parser import HTMLParser
from pathlib import Path

PATH = Path('_site/services/index.html')
SNIPPET = 'Use the <a class="text-link" href="/private-concierge-ibiza/">private concierge</a> rather than managing each category separately.'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def run():
    html = PATH.read_text(encoding='utf-8')
    tags = Tags(html).tags

    if html.count(SNIPPET) != 1:
        raise SystemExit('Phase 175 audit: contextual Services pathway missing or duplicated')

    contextual = sum(
        1 for tag, attrs in tags
        if tag == 'a' and attrs.get('href') == '/private-concierge-ibiza/'
    )
    if contextual != 2:
        raise SystemExit(f'Phase 175 audit: expected contextual link plus existing footer link, got {contextual}')

    if not any(
        tag == 'link'
        and attrs.get('rel') == 'canonical'
        and attrs.get('href') == 'https://ibizavipmove.com/services/'
        for tag, attrs in tags
    ):
        raise SystemExit('Phase 175 audit: Services self-canonical changed')

    if any(
        tag == 'meta'
        and attrs.get('name', '').lower() == 'robots'
        and 'noindex' in attrs.get('content', '').lower()
        for tag, attrs in tags
    ):
        raise SystemExit('Phase 175 audit: Services became noindex')

    print('PASS: Phase 175 audit — one contextual Services pathway; footer link retained; canonical/indexability unchanged')


if __name__ == '__main__':
    run()
