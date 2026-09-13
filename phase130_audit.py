from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
TARGET = ROOT / 'de' / 'private-events-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
URL = 'https://ibizavipmove.com/de/private-events-ibiza/'
TITLE = 'Private Events & Eventkoordination auf Ibiza | Ibiza VIP Move'
DESC = 'Private Events und Eventkoordination auf Ibiza: Gäste, Location, Anbieter, Transport und Timing diskret über ein gemeinsames Briefing abgestimmt.'
H1 = 'Private Events & Eventkoordination auf Ibiza.'

text = TARGET.read_text(encoding='utf-8')

def attr(name, prop=False):
    key = 'property' if prop else 'name'
    m = re.search(rf'<meta[^>]+{key}="{re.escape(name)}"[^>]+content="([^"]*)"', text, re.I)
    return html.unescape(m.group(1)) if m else None

def tag_value(tag):
    m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', text, re.I | re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else None

canon = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', text, re.I)
robots = attr('robots') or ''
hreflangs = dict(re.findall(r'<link[^>]+rel="alternate"[^>]+hreflang="([^"]+)"[^>]+href="([^"]+)"', text, re.I))

webpage = None
service = None
for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.I | re.S):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        continue
    if data.get('@type') == 'WebPage' and data.get('url') == URL:
        webpage = data
    if data.get('@type') == 'Service' and data.get('@id') == URL + '#service':
        service = data

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
root = ET.parse(SITEMAP).getroot()
urls = root.findall('s:url', ns)
entry = None
for node in urls:
    loc = node.find('s:loc', ns)
    if loc is not None and loc.text == URL:
        entry = node
        break

checks = {
    'target exists': TARGET.is_file(),
    'title aligned': tag_value('title') == TITLE,
    'meta description aligned': attr('description') == DESC,
    'og title aligned': attr('og:title', True) == TITLE,
    'og description aligned': attr('og:description', True) == DESC,
    'twitter title aligned': attr('twitter:title') == TITLE,
    'twitter description aligned': attr('twitter:description') == DESC,
    'visible H1 aligned': tag_value('h1') == H1,
    'canonical preserved': bool(canon and canon.group(1) == URL),
    'indexing preserved': 'noindex' not in robots.lower() and 'index' in robots.lower(),
    'hreflang set preserved': all(k in hreflangs for k in ('en','es','fr','de','ar','x-default')),
    'self hreflang preserved': hreflangs.get('de') == URL,
    'WebPage schema aligned': bool(webpage and webpage.get('name') == TITLE and webpage.get('description') == DESC),
    'Service schema aligned': bool(service and service.get('name') == H1 and service.get('description') == DESC and service.get('serviceType') == 'Private Events und Eventkoordination auf Ibiza'),
    'sitemap inventory unchanged': len(urls) == 156,
    'target remains in sitemap once': sum(1 for n in urls if n.find('s:loc', ns) is not None and n.find('s:loc', ns).text == URL) == 1,
    'truthful target lastmod': bool(entry is not None and entry.find('s:lastmod', ns) is not None and entry.find('s:lastmod', ns).text == '2026-09-13'),
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('Phase 130 audit failed: ' + ', '.join(failed))
