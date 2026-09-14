"""Read-only gate for Phase 151 localized Partners WhatsApp handoffs."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from phase151_enhance import GENERIC_HREF, PAGES, href
from phase152_audit import run as run_media_partner_hero_audit
from phase155_mobile_reflow import audit as run_german_partner_reflow_audit

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LANGS = {'en', 'es', 'fr', 'de', 'ar', 'x-default'}


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit('Phase 151 audit: ' + message)


def run(root: Path = ROOT) -> None:
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(root / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')
    for slug, message in PAGES.items():
        path = root / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        tags = Tags(html).tags
        target = href(message)
        require(html.count(GENERIC_HREF) == 0, f'generic English WhatsApp prefill removed: {slug}')
        require(html.count(target) == 3, f'three localized B2B WhatsApp handoffs: {slug}')
        canonical = BASE + '/' + slug + '/'
        require(canonical in urls, f'sitemap membership: {slug}')
        require([a.get('href') for t,a in tags if t == 'link' and a.get('rel') == 'canonical'] == [canonical], f'self canonical: {slug}')
        require(sum(t == 'h1' for t,a in tags) == 1, f'one H1: {slug}')
        require(not any(t == 'meta' and a.get('name','').lower() in {'robots','googlebot'} and 'noindex' in a.get('content','').lower() for t,a in tags), f'indexable: {slug}')
        require({a.get('hreflang') for t,a in tags if t == 'link' and a.get('rel') == 'alternate'} == LANGS, f'hreflang: {slug}')
        html_tag = next(a for t,a in tags if t == 'html')
        lang = slug.split('/',1)[0]
        require(html_tag.get('lang') == lang, f'language: {slug}')
        if lang == 'ar':
            require(html_tag.get('dir') == 'rtl', 'Arabic RTL preserved')
    run_media_partner_hero_audit(root)
    run_german_partner_reflow_audit(root)
    print('PASS: Phase 151 audit — FR/DE/AR Partners residual WhatsApp handoffs are localized B2B; canonicals/hreflang/indexability and 156-URL sitemap preserved')


if __name__ == '__main__':
    run()
