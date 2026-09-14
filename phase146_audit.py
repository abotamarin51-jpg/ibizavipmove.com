"""Read-only regression gate for localized Home chef/wellness discovery."""
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET
from phase146_enhance import PAGES, linked_paragraph
from phase147_audit import run as run_structured_data_audit
from phase150_enhance import PAGES as DINING_PAGES, linked_phrase as dining_linked_phrase
from phase153_enhance import DEST as FR_BESPOKE_DEST, LABEL as FR_BESPOKE_LABEL, MARKER as FR_BESPOKE_MARKER, STYLE as FR_BESPOKE_STYLE
from phase154_enhance import PAGES as YACHT_PAGES, linked_phrase as yacht_linked_phrase

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
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
        raise SystemExit('Phase 146 audit: ' + message)


def run(root: Path = ROOT) -> None:
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(root / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')
    targets = set()
    for lang, (text, links) in PAGES.items():
        home = root / lang / 'index.html'
        html = home.read_text(encoding='utf-8')
        expected = linked_paragraph(text, links)
        if lang in DINING_PAGES:
            label, href = DINING_PAGES[lang]
            require(expected.count(label) == 1, f'Phase 150 phrase remains inside Phase 146 paragraph: {lang}')
            expected = expected.replace(label, dining_linked_phrase(label, href), 1)
        if lang == 'fr':
            require(expected.count(FR_BESPOKE_LABEL) == 1, 'Phase 153 phrase remains inside Phase 146 French paragraph')
            bespoke_link = (
                f'<a {FR_BESPOKE_MARKER} href="{FR_BESPOKE_DEST}" '
                f'style="{FR_BESPOKE_STYLE}">{FR_BESPOKE_LABEL}</a>'
            )
            expected = expected.replace(FR_BESPOKE_LABEL, bespoke_link, 1)
        if lang in YACHT_PAGES:
            label, href = YACHT_PAGES[lang]
            require(expected.count(label) == 1, f'Phase 154 yacht phrase remains inside Phase 146 paragraph: {lang}')
            expected = expected.replace(label, yacht_linked_phrase(label, href), 1)
        require(html.count(expected) == 1, f'exact linked paragraph: {lang}')
        tags = Tags(html).tags
        actual = [a.get('href') for t, a in tags if t == 'a' and a.get('data-ivm146') == 'service']
        require(actual == [href for _, href in links], f'exact two links: {lang}')
        for _, href in links:
            require(href.startswith('/' + lang + '/'), f'same-language target: {href}')
            require(sum(t == 'a' and a.get('href') == href for t, a in tags) == 1, f'one Home link: {href}')
            targets.add(BASE + href)
        for slug in [lang] + [href.strip('/') for _, href in links]:
            page_tags = Tags((root / slug / 'index.html').read_text(encoding='utf-8')).tags
            canonical = BASE + '/' + slug + '/'
            require(canonical in urls, f'sitemap membership: {slug}')
            require([a.get('href') for t, a in page_tags if t == 'link' and a.get('rel') == 'canonical'] == [canonical], f'self-canonical: {slug}')
            require(sum(t == 'h1' for t, a in page_tags) == 1, f'one H1: {slug}')
            require(not any(t == 'meta' and a.get('name', '').lower() in {'robots', 'googlebot'} and 'noindex' in a.get('content', '').lower() for t, a in page_tags), f'indexability: {slug}')
            require({a.get('hreflang') for t, a in page_tags if t == 'link' and a.get('rel') == 'alternate'} == LANGS, f'hreflang: {slug}')
            html_tag = next(a for t, a in page_tags if t == 'html')
            require(html_tag.get('lang') == lang, f'language: {slug}')
            if lang == 'ar':
                require(html_tag.get('dir') == 'rtl', f'Arabic RTL: {slug}')

    graph = {}
    for url in urls:
        slug = urlsplit(url).path.strip('/')
        tags = Tags((root / slug / 'index.html').read_text(encoding='utf-8')).tags
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
    require(all(depths.get(url, 999) <= 2 for url in targets), 'six services within two HTML links of English Home')
    run_structured_data_audit()
    print('PASS: Phase 146 audit — six existing services one link from localized Home/two from English Home; 156 reachable canonicals and FR/DE/AR SEO safeguards intact')


if __name__ == '__main__':
    run()
