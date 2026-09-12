"""Read-only regression gate for Ibiza-local calendar validation on international contact forms."""
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('_site')
SCRIPT = ROOT / 'assets' / 'phase107.js'
CONTACTS = [
    'contact/index.html',
    'es/contacto/index.html',
    'fr/contact/index.html',
    'de/kontakt/index.html',
    'ar/contact/index.html',
]
NEW = '/assets/phase107.js?v=117'
OLD = '/assets/phase107.js?v=107'


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 117 audit: ' + message)


def run():
    require(SCRIPT.is_file(), 'phase107 runtime missing')
    js = SCRIPT.read_text(encoding='utf-8')
    for token in (
        "timeZone:'Europe/Madrid'",
        'formatToParts',
        'const serviceToday=ibizaDateKey(new Date());',
        'arrival.min=serviceToday',
        'departure.min=a||serviceToday',
        'a&&a<serviceToday',
        'd&&d<serviceToday',
    ):
        require(token in js, f'Ibiza-time token missing: {token}')
    require('getTimezoneOffset' not in js, 'visitor-local timezone calculation still present')

    for rel in CONTACTS:
        path = ROOT / rel
        require(path.is_file(), f'missing contact page {rel}')
        html = path.read_text(encoding='utf-8')
        require(html.count(NEW) == 1, f'v117 runtime reference cardinality {rel}')
        require(OLD not in html, f'stale v107 runtime reference {rel}')

    ibiza = ZoneInfo('Europe/Madrid')
    cases = [
        ('2026-09-12T22:30:00+00:00', '2026-09-13'),
        ('2026-09-12T21:30:00+00:00', '2026-09-12'),
        ('2026-12-31T23:30:00+00:00', '2027-01-01'),
    ]
    for iso, expected in cases:
        instant = datetime.fromisoformat(iso).astimezone(timezone.utc)
        actual = instant.astimezone(ibiza).date().isoformat()
        require(actual == expected, f'Europe/Madrid date fixture {iso}: {actual} != {expected}')

    print('PASS: Phase 117 audit — five contact desks validate calendar dates against Europe/Madrid (Ibiza), cache-bust the runtime, and no longer depend on the visitor timezone')


if __name__ == '__main__':
    run()
