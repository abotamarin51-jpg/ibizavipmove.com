"""Install the approved editorial hero and enquiry form on the French yacht page."""
import hashlib
import re
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / 'editorial-assets/fr-yacht'
URL = 'https://ibizavipmove.com/fr/location-yacht-ibiza/'
OLD_IMAGE = 'https://ibizavipmove.com/assets/images/yacht.jpg'
NEW_IMAGE = 'https://ibizavipmove.com/assets/fr-yacht/superyacht-1672.webp'
ART_DIGEST = '764389263a4b3594c8e1cea0092601a2e8e511fd7301ef0bae95bbd2de7ab5f2'
MARKER = '<section class="fr-yacht-hero"'
PUBLIC_FILES = (
    'superyacht-1672.webp', 'superyacht-768.webp', 'cormorant.woff',
    'manrope.woff', 'manrope-light.woff', 'OFL-Cormorant.txt', 'OFL-Manrope.txt',
    'enquiry.js',
)


def update_entry(xml, change):
    """Change exactly this URL's sitemap entry and preserve all other bytes."""
    pattern = r'<url>\s*<loc>' + re.escape(URL) + r'</loc>.*?</url>'
    matches = list(re.finditer(pattern, xml, re.S))
    if len(matches) != 1:
        raise ValueError('Expected exactly one French yacht sitemap entry')
    entry = matches[0]
    return xml[:entry.start()] + change(entry.group()) + xml[entry.end():]


def publish_hero(html, root, fallback_url):
    if hashlib.sha256((SOURCE / 'superyacht-1672.webp').read_bytes()).hexdigest() != ART_DIGEST:
        raise ValueError('Approved French yacht illustration differs')
    hero = (SOURCE / 'hero.html').read_text().replace('__FALLBACK_URL__', fallback_url)
    if MARKER not in html:
        old_section = r'<section class="page-hero">.*?</section>'
        old = re.findall(old_section, html, re.S)
        if len(old) != 1 or '<h1>Location de yacht privé à Ibiza, intégrée à votre séjour.</h1>' not in old[0]:
            raise ValueError('Unexpected French yacht hero')
        css_pattern = r'<link rel="stylesheet" href="(/assets/bundles/[a-f0-9]+\.css)">'
        bundles = re.findall(css_pattern, html)
        if len(bundles) != 1:
            raise ValueError('Expected one source CSS bundle')
        baseline = (root / bundles[0].lstrip('/')).read_bytes()
        css = baseline + b'\n' + (SOURCE / 'hero.css').read_bytes()
        css_url = '/assets/bundles/' + hashlib.sha256(css).hexdigest()[:16] + '.css'
        (root / css_url.lstrip('/')).write_bytes(css)
        html = html.replace(old[0], hero, 1).replace(bundles[0], css_url, 1)
        html = html.replace('<body class="', '<body class="ivm-fr-yacht ', 1)
        html = html.replace(OLD_IMAGE, NEW_IMAGE)
        html = html.replace('</body>', '<script src="/assets/fr-yacht/enquiry.js" defer></script></body>', 1)
    if html.count(hero) != 1 or html.count('<h1') != 1 or html.count(f'href="{URL}" rel="canonical"') + html.count(f'rel="canonical" href="{URL}"') != 1:
        raise ValueError('French hero or canonical verification failed')
    if html.count('href="'+fallback_url+'"') != 3 or html.count('/assets/fr-yacht/enquiry.js') != 1:
        raise ValueError('Expected one enquiry script and three contextual contact links')
    destination = root / 'assets/fr-yacht'
    destination.mkdir(parents=True, exist_ok=True)
    for filename in PUBLIC_FILES:
        shutil.copyfile(SOURCE / filename, destination / filename)
    sitemap = root / 'sitemap.xml'
    xml = update_entry(sitemap.read_text(), lambda entry: re.sub(r'<lastmod>[^<]+</lastmod>', '<lastmod>2026-11-06</lastmod>', entry))
    sitemap.write_text(xml)
    images = root / 'image-sitemap.xml'
    xml = update_entry(images.read_text(), lambda entry: entry.replace(OLD_IMAGE, NEW_IMAGE))
    images.write_text(xml)
    return html
