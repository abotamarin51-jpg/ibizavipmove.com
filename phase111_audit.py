"""Read-only build gate for commercial HTML link depth, not Google index status."""
from collections import Counter, deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import json
import sys
import xml.etree.ElementTree as ET

BASE = 'https://ibizavipmove.com'
PRIORITIES = (
    '/', '/private-concierge-ibiza/', '/private-chauffeur-ibiza/',
    '/luxury-villas-ibiza/', '/yacht-charter-ibiza/', '/private-aviation-ibiza/',
    '/private-client-services-ibiza/', '/destination-management-ibiza/',
    '/partners/', '/luxury-lifestyle-management-ibiza/',
    '/personal-concierge-ibiza/', '/luxury-travel-concierge-ibiza/',
    '/vip-services-ibiza/',
)
LOCALIZED = {
    '/fr/': '/fr/conciergerie-privee-ibiza/',
    '/de/': '/de/privater-concierge-ibiza/',
    '/ar/': '/ar/private-concierge-ibiza/',
}


class Page(HTMLParser):
    """Extract crawlable anchors; do not treat schema/hreflang as navigation."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = set()
        self.main_links = set()
        self.canonicals = []
        self.noindex = False
        self.main = 0
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style', 'noscript'):
            self.ignored += 1
            return
        if self.ignored:
            return
        if tag == 'main':
            self.main += 1
        if tag == 'meta' and a.get('name', '').lower() in ('robots', 'googlebot'):
            tokens = a.get('content', '').lower().replace(',', ' ').split()
            self.noindex = self.noindex or 'noindex' in tokens or 'none' in tokens
        if tag == 'link' and 'canonical' in a.get('rel', '').lower().split():
            self.canonicals.append(a.get('href', ''))
        if tag == 'a' and a.get('href') and 'hidden' not in a:
            if 'nofollow' in a.get('rel', '').lower().split():
                return
            self.links.add(a['href'])
            if self.main:
                self.main_links.add(a['href'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.ignored = max(0, self.ignored - 1)
        elif not self.ignored and tag == 'main':
            self.main = max(0, self.main - 1)


def depths(graph, start):
    result = {start: 0}
    queue = deque([start])
    while queue:
        source = queue.popleft()
        for target in sorted(graph.get(source, set())):
            if target not in result:
                result[target] = result[source] + 1
                queue.append(target)
    return result


def normalize_links(hrefs, source, inventory):
    result = set()
    for href in hrefs:
        parsed = urlsplit(urljoin(BASE + source, href))
        if parsed.scheme == 'https' and parsed.netloc == 'ibizavipmove.com':
            if parsed.path in inventory and parsed.path != source:
                result.add(parsed.path)
    return result


def self_test():
    parser = Page()
    parser.feed('<main><a href="/ok/">OK</a><a href="/no/" rel="nofollow">No</a>'
                '<script>var x="<a href=\'/fake/\'>";</script></main>'
                '<footer><a href="/footer/">Footer</a></footer>')
    assert parser.links == {'/ok/', '/footer/'}
    assert parser.main_links == {'/ok/'}
    assert depths({'/': {'/a/'}, '/a/': {'/b/'}, '/b/': {'/'}}, '/') == {
        '/': 0, '/a/': 1, '/b/': 2,
    }


def run(root=Path('_site'), report_path=Path('seo_geo_audit_report.json')):
    self_test()
    root = Path(root)
    urls = [node.text for node in ET.parse(root / 'sitemap.xml').getroot().iter()
            if node.tag.rsplit('}', 1)[-1] == 'loc']
    errors = []
    if len(urls) != len(set(urls)):
        errors.append('Duplicate sitemap URLs')
    inventory = {}
    for url in urls:
        p = urlsplit(url or '')
        if (p.scheme != 'https' or p.netloc != 'ibizavipmove.com'
                or p.query or p.fragment or '..' in p.path.split('/')):
            errors.append('Invalid canonical sitemap URL: ' + str(url))
            continue
        inventory[p.path or '/'] = url
    graph, main_graph = {}, {}
    for path, url in sorted(inventory.items()):
        target = root / path.lstrip('/') / 'index.html'
        if not target.is_file():
            errors.append('Missing sitemap page: ' + path)
            continue
        page = Page()
        page.feed(target.read_text(encoding='utf-8'))
        if page.noindex:
            errors.append('Noindex page included in sitemap: ' + path)
        if page.canonicals != [url]:
            errors.append('Canonical mismatch: ' + path)
        graph[path] = normalize_links(page.links, path, inventory)
        main_graph[path] = normalize_links(page.main_links, path, inventory)
    distance = depths(graph, '/')
    unreachable = sorted(set(inventory) - set(distance))
    if unreachable:
        errors.append('Unreachable sitemap pages: ' + ', '.join(unreachable))
    priorities = []
    for path in PRIORITIES:
        depth = distance.get(path)
        sources = sum(path in links for links in main_graph.values())
        priorities.append({'path': path, 'html_link_depth': depth,
                           'unique_main_content_sources': sources})
        if path not in inventory or depth is None or depth > 2:
            errors.append('Priority page must be within two HTML links of Home: ' + path)
        if path != '/' and sources < 1:
            errors.append('Priority page needs a contextual main-content source: ' + path)
    localized = []
    for home, path in LOCALIZED.items():
        depth = depths(graph, home).get(path)
        localized.append({'language_home': home, 'path': path, 'html_link_depth': depth})
        if home not in inventory or path not in inventory or depth is None or depth > 2:
            errors.append('Localized concierge depth regression: ' + path)
    report = {
        'scope': 'Generated HTML artifact only; no live HTTP, Search Console or rank data',
        'google_index_status': 'not_verified',
        'maps_rank_status': 'not_measured',
        'sitemap_urls': len(urls),
        'reachable_urls': len(set(inventory) & set(distance)),
        'depth_distribution': dict(sorted(Counter(distance.values()).items())),
        'unreachable': unreachable, 'priorities': priorities,
        'localized_concierge': localized, 'errors': errors,
    }
    # Keep reports outside the published _site directory.
    report_path = Path(report_path)
    if report_path.resolve().is_relative_to(root.resolve()):
        raise SystemExit('Audit report must not be written into the published site')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for item in priorities:
        print('Phase 111 depth:', item['path'], '=', item['html_link_depth'],
              '| contextual sources:', item['unique_main_content_sources'])
    if errors:
        raise SystemExit('Phase 111 audit failed: ' + '; '.join(errors))
    print(f'PASS: Phase 111 read-only crawl-depth audit — {len(urls)} sitemap URLs reachable; '
          f'{len(PRIORITIES)} priority pages within 0–2 HTML links; FR/DE/AR concierge paths protected. '
          'Google indexation, traffic, conversions and Maps rankings are not measured by this test.')
    return report


if __name__ == '__main__':
    run(Path(sys.argv[1]) if len(sys.argv) > 1 else Path('_site'))
