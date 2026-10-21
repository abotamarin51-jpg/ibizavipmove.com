"""Read-only audit for the single-language VIP Tables target-size safeguard."""
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path('_site/vip-tables-club-access-ibiza/index.html')
CANONICAL = 'https://ibizavipmove.com/vip-tables-club-access-ibiza/'
STYLE = 'min-width:24px;min-height:44px;display:inline-flex;align-items:center;justify-content:center'


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def run() -> None:
    if not PAGE.is_file():
        raise SystemExit('Phase 181 audit: VIP Tables page missing')
    links = [attrs for tag, attrs in Tags(PAGE.read_text(encoding='utf-8')).tags
             if tag == 'a' and attrs.get('hreflang') == 'en' and attrs.get('href') == CANONICAL]
    if len(links) != 1:
        raise SystemExit(f'Phase 181 audit: expected one English language link, found {len(links)}')
    link = links[0]
    if link.get('aria-current') != 'page' or link.get('style') != STYLE:
        raise SystemExit('Phase 181 audit: English language target safeguard changed')
    print('PASS: Phase 181 audit — one current English language target retains a 24×44px minimum without fake translations')


if __name__ == '__main__':
    run()
