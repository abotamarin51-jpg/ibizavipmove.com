"""Use verified Search Console demand to clarify the existing luxury-car page for UK/US wording.

This phase does not create a synonym URL. It keeps the established canonical and adds
natural "hire" + "rental" language to the same service page, then records a truthful
lastmod for the significant 2026-09-13 copy/metadata change.
"""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
URL = BASE + '/luxury-car-rental-ibiza/'
PAGE = ROOT / 'luxury-car-rental-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
LASTMOD = '2026-09-13'

TITLE = 'Luxury Car Hire & Rental Ibiza | Supercars | Ibiza VIP Move'
DESCRIPTION = (
    'Luxury car hire and rental in Ibiza, including executive cars, luxury SUVs, '
    'sports cars and supercars, with delivery coordinated to villas, hotels or marinas.'
)
H1 = 'Luxury Car Hire & Rental'
H2 = 'Luxury car hire and rental selected around the client and itinerary.'
LEAD = (
    'Request luxury car hire or rental in Ibiza across executive cars, luxury SUVs, '
    'sports cars and supercars, with delivery details, dates, driver requirements and '
    'preferred model category clarified in advance.'
)


def replace_meta(text, attr, key, value):
    pattern = rf'(<meta\s+{attr}="{re.escape(key)}"\s+content=")[^"]*(")'
    updated, count = re.subn(
        pattern,
        lambda m: m.group(1) + escape(value, quote=True) + m.group(2),
        text,
        count=1,
        flags=re.I,
    )
    if count != 1:
        raise SystemExit(f'Phase 126 metadata target missing: {attr}={key}')
    return updated


def rewrite_jsonld(text):
    pattern = re.compile(r'(<script\s+type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.I | re.S)
    changed = {'webpage': 0, 'service': 0, 'breadcrumb': 0, 'organization': 0}

    def exact_replace(value):
        if isinstance(value, dict):
            return {k: exact_replace(v) for k, v in value.items()}
        if isinstance(value, list):
            return [exact_replace(v) for v in value]
        if value == 'Luxury Car Rental Ibiza':
            return 'Luxury Car Hire & Rental Ibiza'
        if value == 'Luxury & Supercar Rental':
            return 'Luxury Car Hire & Rental'
        if value == 'Luxury car rental coordination in Ibiza':
            return 'Luxury car hire and rental coordination in Ibiza'
        return value

    def repl(match):
        raw = match.group(2).strip()
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)

        obj_type = obj.get('@type') if isinstance(obj, dict) else None
        obj_id = obj.get('@id') if isinstance(obj, dict) else None

        if obj_type == 'WebPage' and obj_id == URL + '#webpage':
            obj['name'] = 'Luxury Car Hire & Rental Ibiza'
            obj['description'] = DESCRIPTION
            changed['webpage'] += 1
        elif obj_type == 'Service' and obj_id == URL + '#service':
            obj['name'] = H1
            obj['serviceType'] = 'Luxury car hire and rental coordination in Ibiza'
            obj['description'] = DESCRIPTION
            changed['service'] += 1
        elif obj_type == 'BreadcrumbList':
            items = obj.get('itemListElement', [])
            if any(isinstance(item, dict) and item.get('item') == URL for item in items):
                obj = exact_replace(obj)
                changed['breadcrumb'] += 1
        elif obj_type == 'Organization' and obj.get('@id') == BASE + '/#organization':
            obj = exact_replace(obj)
            changed['organization'] += 1

        return match.group(1) + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + match.group(3)

    updated = pattern.sub(repl, text)
    missing = [name for name, count in changed.items() if count != 1]
    if missing:
        raise SystemExit(f'Phase 126 JSON-LD target mismatch: {changed}')
    return updated


def update_sitemap():
    if not SITEMAP.is_file():
        raise SystemExit('Phase 126 sitemap missing')
    ET.register_namespace('', NS)
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    matches = 0
    for url in root.findall(f'{{{NS}}}url'):
        loc = url.find(f'{{{NS}}}loc')
        if loc is None or loc.text != URL:
            continue
        matches += 1
        lastmod = url.find(f'{{{NS}}}lastmod')
        if lastmod is None:
            lastmod = ET.Element(f'{{{NS}}}lastmod')
            url.insert(1, lastmod)
        lastmod.text = LASTMOD
    if matches != 1:
        raise SystemExit(f'Phase 126 sitemap target cardinality mismatch: {matches}')
    tree.write(SITEMAP, encoding='utf-8', xml_declaration=True)


def enhance():
    if not PAGE.is_file():
        raise SystemExit('Phase 126 luxury car page missing')
    text = PAGE.read_text(encoding='utf-8')

    if f'<link rel="canonical" href="{URL}">' not in text:
        raise SystemExit('Phase 126 canonical drift before update')

    text, count = re.subn(r'<title>.*?</title>', f'<title>{escape(TITLE)}</title>', text, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit('Phase 126 title target missing')

    text = replace_meta(text, 'name', 'description', DESCRIPTION)
    text = replace_meta(text, 'property', 'og:title', TITLE)
    text = replace_meta(text, 'property', 'og:description', DESCRIPTION)
    text = replace_meta(text, 'name', 'twitter:title', TITLE)
    text = replace_meta(text, 'name', 'twitter:description', DESCRIPTION)

    replacements = {
        '<h1>Luxury &amp; Supercar Rental</h1>': f'<h1>{escape(H1)}</h1>',
        '<h1>Luxury & Supercar Rental</h1>': f'<h1>{escape(H1)}</h1>',
        '<h2>Luxury car rental selected around the client and itinerary.</h2>': f'<h2>{escape(H2)}</h2>',
        '<p class="large">Request executive cars, luxury SUVs, sports cars or supercars with delivery details, dates, driver requirements and preferred model category clarified in advance.</p>': f'<p class="large">{escape(LEAD)}</p>',
        '<h2>Request Luxury &amp; Supercar Rental</h2>': f'<h2>Request {escape(H1)}</h2>',
        '<h2>Request Luxury & Supercar Rental</h2>': f'<h2>Request {escape(H1)}</h2>',
    }

    # The H1 may be HTML-escaped or literal depending on the earlier renderer;
    # require exactly one representation to exist before replacement.
    h1_hits = sum(old in text for old in list(replacements)[:2])
    if h1_hits != 1:
        raise SystemExit(f'Phase 126 H1 source mismatch: {h1_hits}')

    required_exact = [
        '<h2>Luxury car rental selected around the client and itinerary.</h2>',
        '<p class="large">Request executive cars, luxury SUVs, sports cars or supercars with delivery details, dates, driver requirements and preferred model category clarified in advance.</p>',
    ]
    for old in required_exact:
        if text.count(old) != 1:
            raise SystemExit(f'Phase 126 expected source copy mismatch: {old[:72]}')

    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new, 1)

    text = rewrite_jsonld(text)
    PAGE.write_text(text, encoding='utf-8')
    update_sitemap()
    print('PASS: Phase 126 GSC-led luxury-car intent alignment — existing canonical now covers natural UK hire + US rental language without creating a synonym page')


if __name__ == '__main__':
    enhance()
