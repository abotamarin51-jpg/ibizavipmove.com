from pathlib import Path
import re

ROOT = Path('_site')
TARGET = ROOT / 'de' / 'privatkoch-villa-staff-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
CANONICAL = 'https://ibizavipmove.com/de/privatkoch-villa-staff-ibiza/'
EVENT_URL = '/de/private-events-ibiza/'
LASTMOD = '2026-10-04'
MARKER = '<p class="ivm-concierge-continuity">Mehrere Services als einen Aufenthalt koordinieren? <a class="text-link" href="/de/privater-concierge-ibiza/">Privaten Concierge Ibiza ansehen →</a></p>'
HANDOFF = '<p class="ivm-concierge-continuity">Wenn Villa-Staff mit einem privaten Event oder Firmenevent verbunden ist: <a class="text-link" href="/de/private-events-ibiza/">Eventkoordination Ibiza ansehen →</a></p>'

if not TARGET.is_file() or not SITEMAP.is_file():
    raise SystemExit('Phase 175 target or sitemap missing')

text = TARGET.read_text(encoding='utf-8')
if f'<link rel="canonical" href="{CANONICAL}">' not in text or '<html lang="de"' not in text:
    raise SystemExit('Phase 175 canonical/language guard failed')
if text.count(EVENT_URL) > 1:
    raise SystemExit('Phase 175 refusing unexpected duplicate event links')

if HANDOFF not in text:
    if MARKER not in text:
        raise SystemExit('Phase 175 closing marker missing')
    text = text.replace(MARKER, MARKER + HANDOFF, 1)

if text.count(HANDOFF) != 1 or text.count(EVENT_URL) != 1:
    raise SystemExit('Phase 175 event handoff cardinality failed')

TARGET.write_text(text, encoding='utf-8')

sitemap = SITEMAP.read_text(encoding='utf-8')
pat = rf'(<url><loc>{re.escape(CANONICAL)}</loc><lastmod>)[^<]+(</lastmod>)'
sitemap, n = re.subn(pat, rf'\g<1>{LASTMOD}\g<2>', sitemap, count=1)
if n != 1:
    raise SystemExit(f'Phase 175 sitemap target replacement count: {n}')
SITEMAP.write_text(sitemap, encoding='utf-8')

print('PASS: Phase 175 adds one contextual handoff from German Villa Staff to the existing Eventkoordination page and updates only this page lastmod')
