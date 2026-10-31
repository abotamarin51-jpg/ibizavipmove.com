"""Check rendered FAQ text, entity references and existing canonical inventory."""
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

from phase188_customer_questions import BASE, ORG, ROUTES, UPDATES


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.json_buffer = None
        self.nodes = []
        self.canonicals = []
        self.language = None
        self.direction = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = attrs.get('lang')
            self.direction = attrs.get('dir', 'ltr')
        identifier = attrs.get('id')
        if identifier:
            self.ids.append(identifier)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs['href'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.json_buffer = []

    def handle_endtag(self, tag):
        if self.json_buffer is not None and tag == 'script':
            self.nodes.append(json.loads(''.join(self.json_buffer)))
            self.json_buffer = None

    def handle_data(self, value):
        if self.json_buffer is not None:
            self.json_buffer.append(value)


def audit(root=Path('_site'), routes=ROUTES):
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [u.find('s:loc', ns).text for u in ET.parse(root / 'sitemap.xml').getroot()]
    if len(urls) != 157 or len(set(urls)) != 157:
        raise ValueError('Customer questions audit: canonical inventory changed')
    for route in routes:
        canonical = BASE + route
        html = (root / route.strip('/') / 'index.html').read_text(encoding='utf-8')
        page = Page(html)
        assert page.canonicals == [canonical] and canonical in urls, route
        assert len(page.ids) == len(set(page.ids)), (route, 'duplicate HTML IDs')
        selected = {}
        for kind in ('WebPage', 'Service', 'FAQPage'):
            matches = [n for n in page.nodes if n.get('@type') == kind]
            assert len(matches) == 1, (route, kind)
            selected[kind] = matches[0]
        webpage, service, faq = (selected[k] for k in ('WebPage', 'Service', 'FAQPage'))
        assert webpage['mainEntity'] == {'@id': service['@id']}, route
        assert service['mainEntityOfPage'] == {'@id': webpage['@id']}, route
        assert service['provider'] == {'@id': ORG}, route
        assert {'@id': faq['@id']} in webpage['hasPart'], route
        assert faq['isPartOf'] == {'@id': webpage['@id']}, route
        assert faq['about'] == {'@id': service['@id']}, route
        assert faq['publisher'] == {'@id': ORG}, route
        assert len(faq['mainEntity']) == 4, route
        prefix = route.split('/')[1]
        language = prefix if prefix in ('es', 'fr', 'de', 'ar') else 'en'
        assert faq['inLanguage'] == page.language == language, route
        assert page.direction == ('rtl' if language == 'ar' else 'ltr'), route
        for index, question in enumerate(faq['mainEntity'], 1):
            answer = question['acceptedAnswer']
            question_id = 'faq-question-' + str(index)
            answer_id = 'faq-answer-' + str(index)
            assert question['@id'] == canonical + '#' + question_id, route
            assert answer['@id'] == canonical + '#' + answer_id, route
            # A <details> includes its summary and answer. Independently inspect each.
            detail = re.search(r'<details id="' + question_id + r'">(.*?)</details>', html, re.S)
            assert detail is not None, route
            summary = re.search(r'<summary>(.*?)</summary>', detail.group(1), re.S)
            assert unescape(summary.group(1)) == question['name'], route
            answer_match = re.search(r'<p id="' + answer_id + r'">(.*?)</p>', detail.group(1), re.S)
            assert answer_match is not None and unescape(answer_match.group(1)) == answer['text'], route
            assert answer_id in page.ids and question_id in page.ids, route
        # Guard two corrected booking answers against a return to "Sí." for "Cómo".
        if route in ('/es/yate-privado-ibiza/', '/es/seguridad-privada-ibiza/'):
            expected_question, expected_answer = UPDATES[route][0]
            first = faq['mainEntity'][0]
            assert (first['name'], first['acceptedAnswer']['text']) == (expected_question, expected_answer), route
            assert not expected_answer.startswith('Sí.'), (route, 'answer must explain how')
        questions = re.findall(r'<summary\b[^>]*>(.*?)</summary>', html, re.S)
        assert len(questions) == len(set(questions)), (route, 'duplicate visible question')
    print(f'PASS: Customer questions audit — {len(routes) * 4} visible Q&As match JSON-LD, languages, IDs and service/page relationships across {len(routes)} existing pages')


if __name__ == '__main__':
    audit()
