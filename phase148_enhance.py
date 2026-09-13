"""Phase 148: reduce crawl depth for localized Private Events pages.

Adds one truthful, same-language event-service link to the existing FR/DE/AR Home
service summary. No URL, tracking, schema, form, price or policy changes.
"""
from pathlib import Path

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
MARKER = 'data-ivm148="service"'
STYLE = 'text-decoration:underline;text-underline-offset:.15em'
EVENTS = {
    'fr': {
        'before': 'nightlife, sécurité,',
        'label': 'événements privés',
        'href': '/fr/evenements-prives-ibiza/',
    },
    'de': {
        'before': 'Nightlife, Sicherheit,',
        'label': 'Private Events',
        'href': '/de/private-events-ibiza/',
    },
    'ar': {
        'before': 'حياة ليلية، أمن خاص،',
        'label': 'فعاليات خاصة',
        'href': '/ar/private-events-ibiza/',
    },
}


def expected_fragment(lang: str) -> tuple[str, str]:
    item = EVENTS[lang]
    before = item['before']
    first, second = before.split(', ', 1) if lang != 'ar' else before.split('، ', 1)
    sep = ', ' if lang != 'ar' else '، '
    after = (
        first + sep
        + f'<a {MARKER} href="{item["href"]}" style="{STYLE}">{item["label"]}</a>'
        + sep + second
    )
    return before, after


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    pending = {}

    for lang, item in EVENTS.items():
        path = root / lang / 'index.html'
        html = path.read_text(encoding='utf-8')
        target = root / item['href'].strip('/') / 'index.html'
        canonical = (BASE + item['href']).encode()

        if not target.is_file() or canonical not in sitemap:
            raise SystemExit(f'Phase 148: missing canonical destination {item["href"]}')

        before, after = expected_fragment(lang)
        if MARKER in html:
            if html.count(MARKER) != 1 or html.count(after) != 1 or before in html:
                raise SystemExit(f'Phase 148: malformed existing event link: {lang}')
            continue

        if html.count(before) != 1:
            raise SystemExit(f'Phase 148: expected one unchanged Home service fragment: {lang}')
        if f'href="{item["href"]}"' in html or f"href='{item['href']}'" in html:
            raise SystemExit(f'Phase 148: event destination already linked from Home: {lang}')

        pending[path] = html.replace(before, after, 1)

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')

    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 148: unexpected sitemap change')

    print(
        f'PASS: Phase 148 — {len(pending)} localized Home pages gain one same-language '
        'Private Events pathway; no URL, schema, form or sitemap change'
    )


if __name__ == '__main__':
    enhance()
