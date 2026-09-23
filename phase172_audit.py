from pathlib import Path
import json
import re

ROOT = Path('_site')
TARGET = ROOT / 'de' / 'private-events-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
CANONICAL = 'https://ibizavipmove.com/de/private-events-ibiza/'
TITLE = 'Eventkoordination Ibiza | Private Events | Ibiza VIP Move'
DESC = 'Private Event- und Veranstaltungskoordination auf Ibiza für Feiern und Firmenevents: Gäste, Location, Anbieter, Transport und Timing aus einem Briefing.'
H1 = 'Private Events & Eventkoordination auf Ibiza.'

text = TARGET.read_text(encoding='utf-8')
sitemap = SITEMAP.read_text(encoding='utf-8')
checks = {
    'German target language': '<html lang="de"' in text,
    'self canonical': f'<link rel="canonical" href="{CANONICAL}">' in text,
    'indexable robots': '<meta name="robots" content="index,follow,max-image-preview:large">' in text,
    'concise title': f'<title>{TITLE}</title>' in text and len(TITLE) <= 60,
    'concise meta description': f'<meta name="description" content="{DESC}">' in text and len(DESC) <= 160,
    'one H1 with Eventkoordination': text.count('<h1>') == 1 and '<h1>Private Events &amp; Eventkoordination auf Ibiza.</h1>' in text,
    'visible Veranstaltungskoordination': 'Veranstaltungskoordination' in text,
    'visible Firmenevents': 'Firmenevents' in text,
    'partner audience path': text.count('/de/partners/">Partner-Koordination ansehen') == 1 and 'Für Eventagenturen, Travel Advisors und PAs' in text,
    'contact routes preserved': 'https://wa.me/34600703303' in text and 'tel:+34600703303' in text and 'partnership@ibizavipmove.com' in text,
    'six head hreflang alternates': len(re.findall(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">', text, re.I)) == 6,
    'sitemap inventory preserved': sitemap.count('<url>') == 156,
    'truthful target lastmod': f'<loc>{CANONICAL}</loc><lastmod>2026-09-23</lastmod>' in sitemap,
}

schemas = []
for m in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.I | re.S):
    schemas.append(json.loads(m.group(1)))
webpage = next((x for x in schemas if isinstance(x, dict) and x.get('@type') == 'WebPage' and x.get('url') == CANONICAL), None)
service = next((x for x in schemas if isinstance(x, dict) and x.get('@type') == 'Service' and x.get('url') == CANONICAL), None)
checks['WebPage schema aligned'] = bool(webpage and webpage.get('name') == TITLE and webpage.get('description') == DESC)
checks['Service schema aligned'] = bool(service and service.get('name') == H1 and service.get('serviceType') == 'Private Events und Veranstaltungskoordination auf Ibiza' and service.get('description') == DESC)

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS' if ok else 'FAIL') + ': ' + name)
if failed:
    raise SystemExit('Phase 172 audit failed: ' + ', '.join(failed))
print('PASS: Phase 172 audit — one existing German event page aligned to verified German event-coordination demand; no new URL or service claim')
