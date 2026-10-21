"""Read-only audit for the VIP Tables page-local mobile accessibility safeguards."""
from html.parser import HTMLParser
from pathlib import Path

from phase181_accessibility_fix import CANONICAL, LINK_STYLE, MENU_FIX

PAGE = Path('_site/vip-tables-club-access-ibiza/index.html')


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
    html = PAGE.read_text(encoding='utf-8')
    links = [attrs for tag, attrs in Tags(html).tags
             if tag == 'a' and attrs.get('hreflang') == 'en' and attrs.get('href') == CANONICAL]
    if len(links) != 1:
        raise SystemExit(f'Phase 181 audit: expected one English language link, found {len(links)}')
    link = links[0]
    if link.get('aria-current') != 'page' or link.get('style') != LINK_STYLE:
        raise SystemExit('Phase 181 audit: English language target safeguard changed')
    if html.count(MENU_FIX) != 1:
        raise SystemExit('Phase 181 audit: page-local mobile menu safeguard missing or duplicated')
    if 'body.ivm-private-desk' in MENU_FIX:
        raise SystemExit('Phase 181 audit: unrelated Private Desk selector leaked into page safeguard')
    print('PASS: Phase 181 audit — current English target and page-local mobile menu close control verified')


if __name__ == '__main__':
    run()
