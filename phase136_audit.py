"""Read-only gate for localized authority/editorial footer routing."""
from pathlib import Path
import xml.etree.ElementTree as ET
from phase136_enhance import TARGET_PAGES, ROUTES

ROOT = Path('_site')


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 136 audit: ' + message)


def run():
    sitemap_before = (ROOT / 'sitemap.xml').read_bytes()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'sitemap inventory')

    checked = 0
    for lang, slugs in TARGET_PAGES.items():
        for slug in slugs:
            page = ROOT / slug / 'index.html'
            require(page.is_file(), 'target page ' + slug)
            html = page.read_text(encoding='utf-8')
            footer_start = html.find('<footer')
            footer_end = html.find('</footer>', footer_start)
            require(footer_start >= 0 and footer_end >= 0, 'footer ' + slug)
            footer = html[footer_start:footer_end + len('</footer>')]
            canonical = 'https://ibizavipmove.com/' + slug + '/'
            require(html.count(f'<link rel="canonical" href="{canonical}"') == 1, 'canonical ' + slug)
            require(canonical in urls, 'sitemap membership ' + slug)
            require(html.count('<h1') == 1, 'H1 ' + slug)
            require(footer.count('<a href="/privacy/">Privacy</a>') == 1, 'privacy link ' + slug)
            require(footer.count('<a href="/terms/">Terms</a>') == 1, 'terms link ' + slug)
            require(footer.count('<a href="/cookies/">Cookies</a>') == 1, 'cookies link ' + slug)
            for old, new in ROUTES[lang]:
                require(old not in footer, 'English commercial footer route ' + slug + ' ' + old)
                require(footer.count(new) == 1, 'localized footer route ' + slug + ' ' + new)
                href = new.split('href="', 1)[1].split('"', 1)[0]
                target = ROOT / href.strip('/') / 'index.html'
                require(target.is_file(), 'localized target missing ' + href)
                require('https://ibizavipmove.com' + href in urls, 'localized target outside sitemap ' + href)
            checked += 1

    require((ROOT / 'sitemap.xml').read_bytes() == sitemap_before, 'audit mutated sitemap')
    require(checked == 27, 'target page count')
    print('PASS: Phase 136 audit — 27 FR/DE/AR authority/editorial pages keep five core footer routes in-language; targets/canonical/H1/sitemap/legal links preserved')


if __name__ == '__main__':
    run()
