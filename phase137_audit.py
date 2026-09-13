"""Read-only gate for FR/DE/AR contact-page Explore routing."""
from pathlib import Path
import xml.etree.ElementTree as ET
from phase137_enhance import TARGETS

ROOT = Path('_site')


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 137 audit: ' + message)


def run():
    sitemap_before = (ROOT / 'sitemap.xml').read_bytes()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'sitemap inventory')

    checked = 0
    for slug, routes in TARGETS.items():
        page = ROOT / slug / 'index.html'
        require(page.is_file(), 'contact page ' + slug)
        html = page.read_text(encoding='utf-8')
        footer_start = html.find('<footer')
        footer_end = html.find('</footer>', footer_start)
        require(footer_start >= 0 and footer_end >= 0, 'footer ' + slug)
        footer = html[footer_start:footer_end + len('</footer>')]
        canonical = 'https://ibizavipmove.com/' + slug + '/'
        require(html.count(f'<link rel="canonical" href="{canonical}"') == 1, 'canonical ' + slug)
        require(canonical in urls, 'sitemap membership ' + slug)
        require(html.count('<h1') == 1, 'H1 ' + slug)
        require(html.count('data-ivm-qualified-brief="true"') == 1, 'qualified brief form ' + slug)
        require('https://wa.me/34600703303' in html, 'WhatsApp destination ' + slug)
        for old, new in routes:
            require(old not in footer, 'English Explore route ' + slug + ' ' + old)
            require(footer.count(new) == 1, 'localized Explore route ' + slug + ' ' + new)
            href = new.split('href="', 1)[1].split('"', 1)[0]
            target = ROOT / href.strip('/') / 'index.html'
            require(target.is_file(), 'localized target missing ' + href)
            require('https://ibizavipmove.com' + href in urls, 'localized target outside sitemap ' + href)
        checked += 1

    require((ROOT / 'sitemap.xml').read_bytes() == sitemap_before, 'audit mutated sitemap')
    require(checked == 3, 'target page count')
    print('PASS: Phase 137 audit — FR/DE/AR contact footers keep Private Office, Black Book and International Clients inside the same language; form/canonical/H1/sitemap and existing footer structure preserved')


if __name__ == '__main__':
    run()
