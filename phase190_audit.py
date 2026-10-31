"""Check the final club-page inventory, identity, discovery and enquiry handoffs."""
from html import unescape
from html.parser import HTMLParser
import json
import re
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET

from phase190_club_guides import BASE, CLUBS, DATE, HUB, ACCESS, IMAGE, IM, ROOT, SM, page, route


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.tags = []
        self.text = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'a':
            self.links.append(attrs)

    def handle_data(self, data):
        self.text.append(data)


def audit():
    sitemap = ET.parse(ROOT / 'sitemap.xml').getroot()
    urls = [node.findtext(f'{{{SM}}}loc') for node in sitemap.findall(f'{{{SM}}}url')]
    assert len(urls) == len(set(urls)) == 160, 'Expected the original 157 canonicals plus three club pages'
    images = ET.parse(ROOT / 'image-sitemap.xml').getroot()
    hub = page(HUB).read_text(encoding='utf-8')
    access = page(ACCESS).read_text(encoding='utf-8')
    template_nodes = [json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', hub, re.S)]
    identity = {node['@id']: node for node in template_nodes if node.get('@id') in (BASE + '/#organization', BASE + '/#website')}
    for club in CLUBS:
        canonical = BASE + route(club)
        html = page(route(club)).read_text(encoding='utf-8')
        doc = Document(html)
        assert urls.count(canonical) == 1
        assert re.search(r'<html\b[^>]*lang="en"', html), canonical
        assert html.count('<h1>') == 1 and f'<h1>{club["name"]} VIP tables.</h1>' in html
        assert html.count('data-ivm190="club-layout"') == 1
        assert html.count('<main ') == 1 and html.count('</main>') == 1
        canonicals = [a.get('href') for tag, a in doc.tags if tag == 'link' and a.get('rel') == 'canonical']
        assert canonicals == [canonical], canonicals
        alternates = [(a.get('hreflang'), a.get('href')) for tag, a in doc.tags if tag == 'link' and a.get('hreflang')]
        assert alternates == [('en', canonical), ('x-default', canonical)], alternates
        meta = {a.get('name', a.get('property')): a.get('content') for tag, a in doc.tags if tag == 'meta'}
        assert 'noindex' not in meta.get('robots', '')
        assert meta['description'] == meta['og:description'] == meta['twitter:description'] == club['description']
        assert meta['og:url'] == canonical and meta['og:title'] == meta['twitter:title'] == club['title']
        title = unescape(re.search(r'<title>(.*?)</title>', html).group(1))
        assert title == club['title']
        nodes = [json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
        types = [n['@type'] for n in nodes]
        for node_type in ('Organization', 'WebSite', 'WebPage', 'Service', 'BreadcrumbList', 'FAQPage'):
            assert types.count(node_type) == 1, (canonical, node_type)
        for node in nodes:
            if node.get('@id') in identity:
                assert node == identity[node['@id']], 'Shared business identity changed'
        service = next(n for n in nodes if n['@type'] == 'Service')
        assert service['url'] == canonical and service['provider']['@id'] == BASE + '/#organization'
        assert not any(key in service for key in ('offers', 'aggregateRating', 'review')), 'Unverified offers or ratings'
        webpage = next(n for n in nodes if n['@type'] == 'WebPage')
        assert webpage['about']['@id'] == service['@id'] and webpage['dateModified'] == DATE
        faq = next(n for n in nodes if n['@type'] == 'FAQPage')
        visible = Document(re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S).group(1))
        for question in faq['mainEntity']:
            assert question['name'] in visible.text and question['acceptedAnswer']['text'] in visible.text
        assert len(faq['mainEntity']) == html.count('<details>') == 3
        brief_links = [a for a in doc.links if a.get('data-ivm190') == 'brief']
        assert len(brief_links) == 3
        for a in brief_links:
            url = urlsplit(a['href'])
            assert url.scheme == 'https' and url.netloc == 'wa.me' and url.path == '/34600703303'
            assert club['name'] in parse_qs(url.query)['text'][0]
        assert any(a.get('href') == club['source'] for a in visible.links), 'Official source missing'
        for a in doc.links:
            href = a.get('href', '')
            url = urlsplit(href)
            if url.netloc and url.netloc != 'ibizavipmove.com':
                continue
            if url.scheme not in ('', 'https'):
                continue
            if url.path.startswith('/'):
                target = ROOT / url.path.lstrip('/')
                target = target / 'index.html' if url.path.endswith('/') else target
                assert target.is_file(), (canonical, href)
        for source in (hub, access):
            assert f'href="{route(club)}"' in source, 'Missing contextual incoming link'
        image_nodes = [node for node in images.findall(f'{{{SM}}}url') if node.findtext(f'{{{SM}}}loc') == canonical]
        assert len(image_nodes) == 1 and image_nodes[0].findtext(f'{{{IM}}}image/{{{IM}}}loc') == BASE + IMAGE
    print('PASS: Phase 190 audit — 160 unique canonicals; three source-linked, independently described club pages; matching visible FAQ/schema; valid internal links and venue-specific WhatsApp briefs')


if __name__ == '__main__':
    audit()
