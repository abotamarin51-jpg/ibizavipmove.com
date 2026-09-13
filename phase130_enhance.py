from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
TARGET = ROOT / 'de' / 'private-events-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
URL = 'https://ibizavipmove.com/de/private-events-ibiza/'
LASTMOD = '2026-09-13'

OLD_TITLE = 'Private Events auf Ibiza | Ibiza VIP Move'
NEW_TITLE = 'Private Events & Eventkoordination auf Ibiza | Ibiza VIP Move'
OLD_DESC = 'Private Events und Feiern auf Ibiza mit Koordination von Gästen, Location, Anbietern, Transport und Timing durch Ibiza VIP Move.'
NEW_DESC = 'Private Events und Eventkoordination auf Ibiza: Gäste, Location, Anbieter, Transport und Timing diskret über ein gemeinsames Briefing abgestimmt.'
OLD_H1 = 'Private Events, als ein gemeinsames Briefing koordiniert.'
NEW_H1 = 'Private Events & Eventkoordination auf Ibiza.'

if not TARGET.is_file() or not SITEMAP.is_file():
    raise SystemExit('Phase 130 target or sitemap missing')

text = TARGET.read_text(encoding='utf-8')

# Fail closed if neither the verified baseline nor the already-enhanced output is present.
if OLD_TITLE not in text and html.escape(NEW_TITLE) not in text and NEW_TITLE not in text:
    raise SystemExit('Phase 130 title baseline not found')
if OLD_DESC not in text and NEW_DESC not in text:
    raise SystemExit('Phase 130 description baseline not found')
if OLD_H1 not in text and html.escape(NEW_H1) not in text and NEW_H1 not in text:
    raise SystemExit('Phase 130 H1 baseline not found')

# Visible/search metadata. Replacements are intentionally limited to this German page.
text = text.replace(f'<title>{OLD_TITLE}</title>', f'<title>{html.escape(NEW_TITLE)}</title>')
text = text.replace(f'<meta name="description" content="{OLD_DESC}">', f'<meta name="description" content="{html.escape(NEW_DESC, quote=True)}">')
text = text.replace(f'<meta property="og:title" content="{OLD_TITLE}">', f'<meta property="og:title" content="{html.escape(NEW_TITLE, quote=True)}">')
text = text.replace(f'<meta property="og:description" content="{OLD_DESC}">', f'<meta property="og:description" content="{html.escape(NEW_DESC, quote=True)}">')
text = text.replace(f'<meta name="twitter:title" content="{OLD_TITLE}">', f'<meta name="twitter:title" content="{html.escape(NEW_TITLE, quote=True)}">')
text = text.replace(f'<meta name="twitter:description" content="{OLD_DESC}">', f'<meta name="twitter:description" content="{html.escape(NEW_DESC, quote=True)}">')
text = text.replace(OLD_H1, html.escape(NEW_H1))

# Keep structured data aligned with the visible page rather than adding new schema types.
def update_ld(match):
    raw = match.group(1)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return match.group(0)
    changed = False
    if data.get('@type') == 'WebPage' and data.get('url') == URL:
        data['name'] = NEW_TITLE
        data['description'] = NEW_DESC
        changed = True
    if data.get('@type') == 'Service' and data.get('@id') == URL + '#service':
        data['name'] = NEW_H1
        data['serviceType'] = 'Private Events und Eventkoordination auf Ibiza'
        data['description'] = NEW_DESC
        changed = True
    if not changed:
        return match.group(0)
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>'

text = re.sub(r'<script\s+type="application/ld\+json">(.*?)</script>', update_ld, text, flags=re.I | re.S)
TARGET.write_text(text, encoding='utf-8')

# Significant on-page wording changed, so update only this canonical URL's truthful lastmod.
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
tree = ET.parse(SITEMAP)
root = tree.getroot()
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
found = 0
for node in root.findall('s:url', ns):
    loc = node.find('s:loc', ns)
    if loc is not None and loc.text == URL:
        found += 1
        lastmod = node.find('s:lastmod', ns)
        if lastmod is None:
            lastmod = ET.SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        lastmod.text = LASTMOD
if found != 1:
    raise SystemExit(f'Phase 130 expected one sitemap target, found {found}')
tree.write(SITEMAP, encoding='utf-8', xml_declaration=True)
