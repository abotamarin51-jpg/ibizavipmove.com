"""Read-only audit for the English VIP Tables & Club Access page."""
from __future__ import annotations

from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import Image

from phase180_enhance import (
    BASE, CANONICAL, DESCRIPTION, FAQS, LASTMOD, SOCIAL_IMAGE,
    SOCIAL_TARGET, SOCIAL_PUBLIC, TARGET, TITLE, VISIBLE_DATE,
)

ROOT = Path('_site')
TEMPLATE = ROOT / 'private-concierge-ibiza' / 'index.html'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
SCRIPT_RE = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.I | re.S)


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit('Phase 180 audit: ' + message)


def schemas(html: str) -> list[dict]:
    out = []
    for match in SCRIPT_RE.finditer(html):
        out.append(json.loads(match.group(1)))
    return out


def node_type(node: dict, expected: str) -> bool:
    value = node.get('@type')
    return expected in value if isinstance(value, list) else value == expected


def normalize_fragment(html: str, tag: str, class_name: str | None = None) -> str:
    class_part = rf'(?=[^>]*\bclass="[^"]*\b{re.escape(class_name)}\b[^"]*")' if class_name else ''
    pattern = rf'<{tag}\b{class_part}[^>]*>.*?</{tag}>'
    match = re.search(pattern, html, re.I | re.S)
    require(match is not None, f'missing {tag}.{class_name or ""}')
    return re.sub(r'\s+', ' ', match.group(0)).strip()


def run() -> None:
    require(TARGET.is_file(), 'new page missing')
    html = TARGET.read_text(encoding='utf-8')
    template = TEMPLATE.read_text(encoding='utf-8')
    tags = Tags(html).tags

    require(f'<title>{escape(TITLE)}</title>' in html, 'title mismatch')
    require(f'<meta name="description" content="{DESCRIPTION}">' in html, 'description mismatch')
    require(f'<link rel="canonical" href="{CANONICAL}">' in html, 'canonical mismatch')
    require('<meta name="robots" content="index,follow,max-image-preview:large">' in html, 'robots mismatch')
    require(html.lower().count('<h1') == 1, 'expected exactly one H1')
    require('<h1>VIP tables and club access in Ibiza, arranged privately.</h1>' in html, 'H1 mismatch')
    # Keep public venue geography and US travel guidance factually accurate.
    require('<td>O Beach Ibiza</td><td>Sant Antoni de Portmany</td><td>Day club</td>' in html, 'O Beach public location/branding drift')
    require('<td>[UNVRS]</td><td>San Rafael (Sant Rafel)</td><td>Nightclub</td>' in html, 'UNVRS venue name/location missing')
    require('Ocean Beach Ibiza</td>' not in html, 'superseded O Beach name returned')
    require('These venues are examples for planning, not confirmed booking relationships.' in html, 'venue availability clarification missing')
    require('the gap can briefly be five hours' in html, 'US daylight-saving caveat missing')
    require('WhatsApp requires the app and an internet connection.' in html, 'WhatsApp prerequisites omitted')
    require('WhatsApp works from the US with no extra setup' not in html, 'unsupported WhatsApp setup claim')
    require('id="main-content"' in html and 'class="ivm-skip-link"' in html, 'accessibility landmarks missing')

    # Same final template chrome, styles and runtimes; only the page-specific language choices differ.
    require(normalize_fragment(html, 'header', 'site-header') == normalize_fragment(template, 'header', 'site-header'), 'header/menu drift')
    require(normalize_fragment(html, 'footer') == normalize_fragment(template, 'footer'), 'footer drift')
    styles = [a.get('href') for t, a in tags if t == 'link' and a.get('rel') == 'stylesheet']
    template_styles = [a.get('href') for t, a in Tags(template).tags if t == 'link' and a.get('rel') == 'stylesheet']
    require(styles == template_styles, 'stylesheet set differs from template')
    scripts = [a.get('src') for t, a in tags if t == 'script' and a.get('src')]
    template_scripts = [a.get('src') for t, a in Tags(template).tags if t == 'script' and a.get('src')]
    require(scripts == template_scripts, 'runtime scripts differ from template')
    language_links = [a for t, a in tags if t == 'a' and a.get('hreflang')]
    require(len(language_links) == 1 and language_links[0].get('hreflang') == 'en'
            and language_links[0].get('href') == CANONICAL and language_links[0].get('aria-current') == 'page',
            'visible language bar must keep the component without claiming translations')
    head_alts = [(a.get('hreflang'), a.get('href')) for t, a in tags
                 if t == 'link' and a.get('rel') == 'alternate' and a.get('hreflang')]
    require(head_alts == [('en', CANONICAL), ('x-default', CANONICAL)], 'head hreflang mismatch')

    require(f'<meta property="og:image" content="{SOCIAL_IMAGE}">' in html, 'licensed social image missing from Open Graph')
    require(f'<meta name="twitter:image" content="{SOCIAL_IMAGE}">' in html, 'licensed social image missing from Twitter')
    require(f'--hero:url(\'{SOCIAL_PUBLIC}\')' in html, 'reviewed editorial image not used as new hero')
    require(f'Last updated: {VISIBLE_DATE}' in html, 'visible actual update date missing')
    require(SOCIAL_TARGET.is_file() and SOCIAL_TARGET.stat().st_size > 20_000, 'generated social JPEG is absent or too small')
    with Image.open(SOCIAL_TARGET) as social:
        require(social.size == (1200, 630) and social.format == 'JPEG', 'social image must be a valid 1200x630 JPEG')
    forbidden_markers = (
        '[URL DE UNA IMAGEN PROPIA', '[MISMA IMAGEN]', '[FECHA]', '[YYYY-MM-DD]',
        '[CONFIRMAR:', '[OPCIONAL:', '[PENDIENTE:', 'data-ivm180-placeholder',
    )
    require(all(marker not in html for marker in forbidden_markers), 'unresolved owner placeholder exposed')

    data = schemas(html)
    orgs = [node for node in data if node_type(node, 'Organization') and node.get('@id') == BASE + '/#organization']
    websites = [node for node in data if node_type(node, 'WebSite') and node.get('@id') == BASE + '/#website']
    webpages = [node for node in data if node_type(node, 'WebPage') and node.get('@id') == CANONICAL + '#webpage']
    services = [node for node in data if node_type(node, 'Service') and node.get('@id') == CANONICAL + '#service']
    breadcrumbs = [node for node in data if node_type(node, 'BreadcrumbList')]
    faqs = [node for node in data if node_type(node, 'FAQPage')]
    require(len(orgs) == 1, 'Organization must be merged, never duplicated')
    require(len(websites) == 1, 'WebSite node missing or duplicated')
    require(len(webpages) == len(services) == len(breadcrumbs) == len(faqs) == 1, 'page schema node count mismatch')
    require(webpages[0].get('name') == TITLE and webpages[0].get('description') == DESCRIPTION, 'WebPage metadata mismatch')
    require(webpages[0].get('dateModified') == LASTMOD, 'schema dateModified must match actual source change')
    require(services[0].get('provider') == {'@id': BASE + '/#organization'}, 'Service provider mismatch')
    require(len(breadcrumbs[0].get('itemListElement', [])) == 3, 'breadcrumb count mismatch')
    faq_schema = faqs[0].get('mainEntity', [])
    require(len(faq_schema) == len(FAQS), 'FAQ schema count mismatch')
    for expected, item in zip(FAQS, faq_schema):
        require(item.get('name') == expected[0], 'FAQ question mismatch')
        require(item.get('acceptedAnswer', {}).get('text') == expected[1], 'FAQ answer mismatch')
        require(f'<summary>{escape(expected[0])}</summary><p>{escape(expected[1])}</p>' in html, 'visible FAQ differs from schema')

    for slug in ('restaurants-nightlife-ibiza', 'private-concierge-ibiza', 'vip-services-ibiza', 'private-chauffeur-ibiza'):
        source = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
        require(source.count('data-ivm180="vip-tables-link"') == 1, f'internal link missing or duplicated: {slug}')
        require('href="/vip-tables-club-access-ibiza/"' in source, f'internal target wrong: {slug}')

    tree = ET.parse(ROOT / 'sitemap.xml')
    urls = tree.getroot().findall(f'{{{NS}}}url')
    require(len(urls) == 157, f'expected 157 sitemap URLs, found {len(urls)}')
    matches = [node for node in urls if node.findtext(f'{{{NS}}}loc') == CANONICAL]
    require(len(matches) == 1, 'new sitemap canonical missing or duplicated')
    children = list(matches[0])
    require([child.tag.split('}', 1)[-1] for child in children] == ['loc', 'lastmod'], 'new sitemap entry has forbidden fields')
    require(matches[0].findtext(f'{{{NS}}}lastmod') == LASTMOD, 'sitemap lastmod mismatch')

    print('PASS: Phase 180 audit — existing canonical Organization, real dates, licensed social image, four inlinks, no placeholders and 157-URL sitemap verified')


if __name__ == '__main__':
    run()
