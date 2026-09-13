"""Read-only gate for Phase 147 structured-data cleanup."""
from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG_ID = BASE + '/#organization'
ARTICLE_URL = 'https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/'
ARTICLE_NAME = 'Top Luxury Travel Concierge Services for Ibiza Dining in 2026'
PRIORITY = (
    'private-events-ibiza',
    'private-chef-staffing-ibiza',
    'private-concierge-cala-jondal-es-cubells-ibiza',
    'private-concierge-santa-eulalia-roca-llisa-ibiza',
)


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 147 audit: ' + msg)


def types(node):
    value = node.get('@type')
    return value if isinstance(value, list) else [value]


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def run():
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')

    external_creativeworks = 0
    own_orgs = 0
    for path in ROOT.rglob('*.html'):
        html = path.read_text(encoding='utf-8')
        if '</head>' not in html:
            continue
        head = html.split('</head>', 1)[0]
        pos = 0
        marker = '<script type="application/ld+json">'
        while True:
            start = head.find(marker, pos)
            if start < 0:
                break
            start += len(marker)
            end = head.find('</script>', start)
            require(end >= 0, f'unclosed JSON-LD in {path}')
            raw = head[start:end]
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SystemExit(f'Phase 147 audit: invalid JSON-LD in {path}: {exc}')
            for node in walk(data):
                node_types = types(node)
                if node.get('url') == ARTICLE_URL and node.get('name') == ARTICLE_NAME:
                    require('Article' not in node_types, f'external reference still typed Article in {path}')
                    require('CreativeWork' in node_types, f'external reference not CreativeWork in {path}')
                    require('publisher' not in node, f'external reference retains incomplete publisher entity in {path}')
                    external_creativeworks += 1
                if (
                    'Organization' in node_types
                    and (node.get('@id') == ORG_ID or node.get('name') == 'Ibiza VIP Move')
                ):
                    require(node.get('logo') is not None, f'Ibiza VIP Move Organization missing logo in {path}')
                    own_orgs += 1
            pos = end + len('</script>')

    require(external_creativeworks >= 60, f'expected established external CreativeWork footprint, found {external_creativeworks}')
    require(own_orgs >= 60, f'expected established own Organization footprint, found {own_orgs}')

    for slug in PRIORITY:
        path = ROOT / slug / 'index.html'
        require(path.is_file(), f'missing priority page {slug}')
        html = path.read_text(encoding='utf-8')
        tags = Tags(html).tags
        url = BASE + '/' + slug + '/'
        require(sum(t == 'h1' for t, a in tags) == 1, f'one H1 {slug}')
        require([a.get('href') for t, a in tags if t == 'link' and a.get('rel') == 'canonical'] == [url], f'self canonical {slug}')
        require(url in urls, f'sitemap membership {slug}')
        require(not any(t == 'meta' and a.get('name','').lower() == 'robots' and 'noindex' in a.get('content','').lower() for t,a in tags), f'indexability {slug}')

    # Preserve the site's own field-report Article facts while cleaning only the
    # exact third-party subject relationship.
    report = (ROOT / 'ibiza-luxury-operations-report-2026' / 'index.html').read_text(encoding='utf-8')
    require('"headline":"Ibiza Luxury Operations Report 2026"' in report or '"headline": "Ibiza Luxury Operations Report 2026"' in report, 'owned report Article headline preserved')
    require('"datePublished"' in report, 'owned report publication date preserved')

    print(
        f'PASS: Phase 147 audit — {external_creativeworks} exact external references use CreativeWork, '
        f'{own_orgs} Ibiza VIP Move Organization nodes carry a logo, priority canonicals/indexability and 156 URLs preserved'
    )


if __name__ == '__main__':
    run()
