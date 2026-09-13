"""Read-only gate for FR/DE/AR localized brand-wordmark home routing."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
LANGS = {'fr': '/fr/', 'de': '/de/', 'ar': '/ar/'}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.anchors = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.anchors.append(dict(attrs))


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 138 audit: ' + message)


def run():
    sitemap_before = (ROOT / 'sitemap.xml').read_bytes()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'sitemap inventory')

    total_wordmarks = 0
    for lang, home in LANGS.items():
        home_url = 'https://ibizavipmove.com' + home
        require(home_url in urls, 'localized home missing from sitemap ' + home)
        language_wordmarks = 0
        english_switches = 0
        for page in sorted((ROOT / lang).rglob('index.html')):
            html = page.read_text(encoding='utf-8')
            parsed = Page(html)
            wordmarks = [
                a for a in parsed.anchors
                if 'wordmark' in (a.get('class') or '').split()
            ]
            for anchor in wordmarks:
                require(anchor.get('href') == home, f'wordmark route {page}: {anchor.get("href")}')
            language_wordmarks += len(wordmarks)
            english_switches += sum(
                1 for a in parsed.anchors
                if a.get('href') == '/' and 'wordmark' not in (a.get('class') or '').split()
            )
        require(language_wordmarks == 27, f'{lang} wordmark inventory: {language_wordmarks}')
        require(english_switches > 0, f'{lang} explicit English-language route preserved')
        total_wordmarks += language_wordmarks

    require(total_wordmarks == 81, 'total localized wordmark inventory')
    require((ROOT / 'sitemap.xml').read_bytes() == sitemap_before, 'audit mutated sitemap')
    print(
        'PASS: Phase 138 audit — all 81 FR/DE/AR brand wordmarks route to the '
        'same-language homepage; explicit English routes remain available and sitemap stays at 156 URLs'
    )


if __name__ == '__main__':
    run()
