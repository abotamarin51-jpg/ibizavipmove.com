"""Read-only gate for Phase 148 localized Private Events discovery."""
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

from phase148_enhance import BASE, EVENTS, expected_fragment

ROOT = Path('_site')
LANGS = {'en', 'es', 'fr', 'de', 'ar', 'x-default'}


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit('Phase 148 audit: ' + message)


def run(root: Path = ROOT) -> None:
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(root / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')

    targets = set()
    for lang, item in EVENTS.items():
        home = root / lang / 'index.html'
        html = home.read_text(encoding='utf-8')
        _, after = expected_fragment(lang)
        require(html.count(after) == 1, f'exact event-linked Home fragment: {lang}')

        tags = Tags(html).tags
        event_links = [
            a.get('href') for t, a in tags
            if t == 'a' and a.get('data-ivm148') == 'service'
        ]
        require(event_links == [item['href']], f'exact one event link: {lang}')
        require(item['href'].startswith('/' + lang + '/'), f'same-language target: {lang}')

        slug = item['href'].strip('/')
        target_html = (root / slug / 'index.html').read_text(encoding='utf-8')
        target_tags = Tags(target_html).tags
        canonical = BASE + item['href']
        require(canonical in urls, f'sitemap membership: {slug}')
        require(
            [a.get('href') for t, a in target_tags if t == 'link' and a.get('rel') == 'canonical'] == [canonical],
            f'self-canonical: {slug}',
        )
        require(sum(t == 'h1' for t, a in target_tags) == 1, f'one H1: {slug}')
        require(
            not any(
                t == 'meta'
                and a.get('name', '').lower() in {'robots', 'googlebot'}
                and 'noindex' in a.get('content', '').lower()
                for t, a in target_tags
            ),
            f'indexability: {slug}',
        )
        require(
            {a.get('hreflang') for t, a in target_tags if t == 'link' and a.get('rel') == 'alternate'} == LANGS,
            f'hreflang: {slug}',
        )
        html_tag = next(a for t, a in target_tags if t == 'html')
        require(html_tag.get('lang') == lang, f'language: {slug}')
        if lang == 'ar':
            require(html_tag.get('dir') == 'rtl', f'Arabic RTL: {slug}')
        targets.add(canonical)

    graph = {}
    for url in urls:
        slug = urlsplit(url).path.strip('/')
        path = root / slug / 'index.html'
        tags = Tags(path.read_text(encoding='utf-8')).tags
        edges = set()
        for tag, attrs in tags:
            if tag != 'a' or not attrs.get('href') or 'nofollow' in attrs.get('rel', '').lower().split():
                continue
            parsed = urlsplit(urljoin(url, attrs['href']))
            dest = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, '', ''))
            if dest in urls:
                edges.add(dest)
        graph[url] = edges

    depths = {BASE + '/': 0}
    queue = deque(depths)
    while queue:
        source = queue.popleft()
        for dest in graph[source]:
            if dest not in depths:
                depths[dest] = depths[source] + 1
                queue.append(dest)

    require(len(depths) == 156, 'all sitemap pages remain reachable')
    require(all(depths.get(url, 999) <= 2 for url in targets), 'event targets remain within two HTML links of English Home')

    print(
        'PASS: Phase 148 audit — FR/DE/AR Private Events pages gain one localized Home path, '
        'all three are within two HTML links of English Home, and 156 canonicals remain reachable'
    )


if __name__ == '__main__':
    run()
