from pathlib import Path
import re

ROOT = Path('_site')
TARGET = ROOT / 'de' / 'privatkoch-villa-staff-ibiza' / 'index.html'
EVENT = ROOT / 'de' / 'private-events-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
CANONICAL = 'https://ibizavipmove.com/de/privatkoch-villa-staff-ibiza/'
EVENT_CANONICAL = 'https://ibizavipmove.com/de/private-events-ibiza/'

target = TARGET.read_text(encoding='utf-8')
event = EVENT.read_text(encoding='utf-8')
sitemap = SITEMAP.read_text(encoding='utf-8')

checks = {
    'staff page German': '<html lang="de"' in target,
    'staff page self canonical': f'<link rel="canonical" href="{CANONICAL}">' in target,
    'staff page indexable': '<meta name="robots" content="index,follow,max-image-preview:large">' in target,
    'staff page one H1': target.count('<h1>') == 1,
    'event handoff exactly once': target.count('href="/de/private-events-ibiza/"') == 1,
    'event handoff clearly scoped': 'Eigenständige private Veranstaltungen oder Firmenevents koordinieren?' in target,
    'event handoff anchor descriptive': 'Eventkoordination Ibiza ansehen →' in target,
    'event target exists and canonical': f'<link rel="canonical" href="{EVENT_CANONICAL}">' in event,
    'contact routes preserved': 'https://wa.me/34600703303' in target and 'tel:+34600703303' in target and 'partnership@ibizavipmove.com' in target,
    'six head hreflang alternates preserved': len(re.findall(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">', target, re.I)) == 6,
    'sitemap inventory preserved': sitemap.count('<url>') == 156,
    'truthful staff lastmod': f'<loc>{CANONICAL}</loc><lastmod>2026-10-02</lastmod>' in sitemap,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(('PASS' if ok else 'FAIL') + ': ' + name)
if failed:
    raise SystemExit('Phase 175 audit failed: ' + ', '.join(failed))
print('PASS: Phase 175 audit — one existing German staffing page now hands event-intent users to the existing event page; no new URL or service claim')
