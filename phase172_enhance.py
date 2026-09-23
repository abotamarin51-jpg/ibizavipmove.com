from pathlib import Path
import html as htmllib
import json
import re

ROOT = Path('_site')
TARGET = ROOT / 'de' / 'private-events-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
CANONICAL = 'https://ibizavipmove.com/de/private-events-ibiza/'
TITLE = 'Eventkoordination Ibiza | Private Events | Ibiza VIP Move'
DESC = 'Private Event- und Veranstaltungskoordination auf Ibiza für Feiern und Firmenevents: Gäste, Location, Anbieter, Transport und Timing aus einem Briefing.'
H1 = 'Private Events & Eventkoordination auf Ibiza.'
LEAD = 'Private Feiern und ausgewählte Firmenevents brauchen klare Veranstaltungskoordination: Gäste, Location, Transport, Anbieter und Timing in einem operativen Briefing.'
H2 = 'Lokale Eventkoordination für Feiern und Firmenevents.'
LARGE = 'Wir koordinieren private Veranstaltungen und Firmenevents auf Ibiza rund um den bestätigten Umfang. Gäste, Location, Anbieter, Transport, Security und Timing werden dabei in einem gemeinsamen operativen Ablauf verbunden.'
PARTNER = '<p class="ivm-concierge-continuity">Für Eventagenturen, Travel Advisors und PAs mit bestätigten Ibiza-Abläufen: <a class="text-link" href="/de/partners/">Partner-Koordination ansehen →</a></p>'

if not TARGET.exists() or not SITEMAP.exists():
    raise SystemExit('Phase 172 target or sitemap missing')
text = TARGET.read_text(encoding='utf-8')
if f'<link rel="canonical" href="{CANONICAL}">' not in text or '<html lang="de"' not in text:
    raise SystemExit('Phase 172 canonical/language guard failed')

text = re.sub(r'<title>.*?</title>', f'<title>{htmllib.escape(TITLE)}</title>', text, count=1, flags=re.I | re.S)
for attr, key, value in [
    ('name', 'description', DESC),
    ('property', 'og:title', TITLE),
    ('property', 'og:description', DESC),
    ('name', 'twitter:title', TITLE),
    ('name', 'twitter:description', DESC),
]:
    pat = rf'(<meta\s+{attr}="{re.escape(key)}"\s+content=")[^"]*(")'
    text, n = re.subn(pat, lambda m: m.group(1) + htmllib.escape(value, quote=True) + m.group(2), text, count=1, flags=re.I)
    if n != 1:
        raise SystemExit(f'Phase 172 missing meta: {key}')

text, n = re.subn(r'<h1>.*?</h1>', f'<h1>{htmllib.escape(H1)}</h1>', text, count=1, flags=re.I | re.S)
if n != 1:
    raise SystemExit('Phase 172 H1 replacement failed')
text, n = re.subn(
    r'(<section class="page-hero">.*?<h1>.*?</h1>)<p>.*?</p>',
    lambda m: m.group(1) + f'<p>{htmllib.escape(LEAD)}</p>',
    text,
    count=1,
    flags=re.I | re.S,
)
if n != 1:
    raise SystemExit('Phase 172 hero lead replacement failed')
text, n = re.subn(
    r'(<section class="editorial">.*?<div class="kicker dark">Ibiza VIP Move</div>)<h2>.*?</h2>',
    lambda m: m.group(1) + f'<h2>{htmllib.escape(H2)}</h2>',
    text,
    count=1,
    flags=re.I | re.S,
)
if n != 1:
    raise SystemExit('Phase 172 editorial heading replacement failed')
text, n = re.subn(
    r'(<section class="editorial">.*?<div><p class="large">).*?(</p></div></section>)',
    lambda m: m.group(1) + htmllib.escape(LARGE) + m.group(2),
    text,
    count=1,
    flags=re.I | re.S,
)
if n != 1:
    raise SystemExit('Phase 172 editorial copy replacement failed')
text, n = re.subn(
    r'(<section class="process">.*?<div class="kicker dark">Private coordination</div>)<h2>.*?</h2>',
    lambda m: m.group(1) + f'<h2>{htmllib.escape(H2)}</h2>',
    text,
    count=1,
    flags=re.I | re.S,
)
if n != 1:
    raise SystemExit('Phase 172 process heading replacement failed')

if '/de/partners/">Partner-Koordination ansehen' not in text:
    marker = '<p class="ivm-concierge-continuity">Mehrere Services als einen Aufenthalt koordinieren? <a class="text-link" href="/de/privater-concierge-ibiza/">Privaten Concierge Ibiza ansehen →</a></p>'
    if marker not in text:
        raise SystemExit('Phase 172 closing marker missing')
    text = text.replace(marker, marker + PARTNER, 1)

script_re = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)
def patch_schema(match):
    try:
        obj = json.loads(match.group(1))
    except Exception:
        return match.group(0)
    if not isinstance(obj, dict):
        return match.group(0)
    typ = obj.get('@type')
    if typ == 'WebPage' and obj.get('url') == CANONICAL:
        obj['name'] = TITLE
        obj['description'] = DESC
    elif typ == 'Service' and obj.get('url') == CANONICAL:
        obj['name'] = H1
        obj['serviceType'] = 'Private Events und Veranstaltungskoordination auf Ibiza'
        obj['description'] = DESC
    elif typ == 'BreadcrumbList':
        for item in obj.get('itemListElement', []):
            if isinstance(item, dict) and item.get('item') == CANONICAL:
                item['name'] = H1
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>'

text = script_re.sub(patch_schema, text)
TARGET.write_text(text, encoding='utf-8')

sitemap = SITEMAP.read_text(encoding='utf-8')
pat = rf'(<url><loc>{re.escape(CANONICAL)}</loc><lastmod>)[^<]+(</lastmod>)'
sitemap, n = re.subn(pat, rf'\g<1>2026-09-23\g<2>', sitemap, count=1)
if n != 1:
    raise SystemExit(f'Phase 172 sitemap target replacement count: {n}')
SITEMAP.write_text(sitemap, encoding='utf-8')

print('PASS: Phase 172 German private-events intent aligned to verified Eventkoordination/Veranstaltungskoordination demand')
