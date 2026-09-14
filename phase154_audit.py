"""Read-only regression gate for Phase 154 localized yacht discovery links."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
MARKER_VALUE = 'yacht'
PAGES = {
    'fr': ('yachts', '/fr/location-yacht-ibiza/'),
    'de': ('Yachten', '/de/yachtcharter-ibiza/'),
    'ar': ('يخوت', '/ar/yacht-charter-ibiza/'),
}
LANGS = {'en','es','fr','de','ar','x-default'}


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 154 audit: ' + msg)


def run(root: Path = ROOT) -> None:
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[e.text for e in ET.parse(root/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'canonical inventory changed')
    for lang, (label, href) in PAGES.items():
        source=root/lang/'index.html'; target=root/href.strip('/')/'index.html'
        require(source.is_file() and target.is_file(),f'source/destination missing: {lang}')
        html=source.read_text(encoding='utf-8'); tags=Tags(html).tags
        require(sum(1 for t,a in tags if t=='a' and a.get('href')==href and a.get('data-ivm154')==MARKER_VALUE)==1,f'exact yacht link: {lang}')
        require(label in html,f'existing visible yacht wording preserved: {lang}')
        require(sum(t=='h1' for t,a in tags)==1,f'Home H1 preserved: {lang}')
        canonical=BASE+'/'+lang+'/'
        require([a.get('href') for t,a in tags if t=='link' and a.get('rel')=='canonical']==[canonical],f'Home canonical: {lang}')
        require({a.get('hreflang') for t,a in tags if t=='link' and a.get('rel')=='alternate'}==LANGS,f'Home hreflang: {lang}')
        html_tag=next(a for t,a in tags if t=='html')
        require(html_tag.get('lang')==lang,f'Home lang: {lang}')
        if lang=='ar': require(html_tag.get('dir')=='rtl','Arabic RTL preserved')
        target_tags=Tags(target.read_text(encoding='utf-8')).tags
        target_url=BASE+href
        require(target_url in urls,f'target remains in sitemap: {lang}')
        require([a.get('href') for t,a in target_tags if t=='link' and a.get('rel')=='canonical']==[target_url],f'target self-canonical: {lang}')
        require(sum(t=='h1' for t,a in target_tags)==1,f'target H1: {lang}')
        require(not any(t=='meta' and a.get('name','').lower() in {'robots','googlebot'} and 'noindex' in a.get('content','').lower() for t,a in target_tags),f'target indexable: {lang}')
        require({a.get('hreflang') for t,a in target_tags if t=='link' and a.get('rel')=='alternate'}==LANGS,f'target hreflang: {lang}')
    print('PASS: Phase 154 audit — FR/DE/AR Home pages each expose one same-language yacht link; visible wording, RTL, canonicals, hreflang and 156-URL sitemap preserved')


if __name__=='__main__':
    run()
