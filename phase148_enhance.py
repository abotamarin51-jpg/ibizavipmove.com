"""Phase 148: reduce crawl depth for localized Private Events pages.

Adds one truthful, same-language event-service pathway near the existing FR/DE/AR Home
service summary. No URL, tracking, schema, form, price or policy changes.
"""
from pathlib import Path
from phase150_enhance import enhance as enhance_localized_dining_paths

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
MARKER = 'data-ivm148="service"'
AUTHORITY_MARKER = 'class="ivm-home-authority-pathways"'
EVENTS = {
    'fr': {
        'label': 'Événements privés à Ibiza →',
        'href': '/fr/evenements-prives-ibiza/',
    },
    'de': {
        'label': 'Private Events auf Ibiza →',
        'href': '/de/private-events-ibiza/',
    },
    'ar': {
        'label': 'الفعاليات الخاصة في إيبيزا ←',
        'href': '/ar/private-events-ibiza/',
    },
}


def event_block(lang: str) -> str:
    item = EVENTS[lang]
    return (
        '<p class="ivm-home-event-pathway">'
        f'<a class="text-link" {MARKER} href="{item["href"]}">{item["label"]}</a>'
        '</p>'
    )


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    pending = {}

    for lang, item in EVENTS.items():
        path = root / lang / 'index.html'
        html = path.read_text(encoding='utf-8')
        target = root / item['href'].strip('/') / 'index.html'
        canonical = (BASE + item['href']).encode()
        block = event_block(lang)

        if not target.is_file() or canonical not in sitemap:
            raise SystemExit(f'Phase 148: missing canonical destination {item["href"]}')

        if MARKER in html:
            if html.count(MARKER) != 1 or html.count(block) != 1:
                raise SystemExit(f'Phase 148: malformed existing event pathway: {lang}')
            continue

        if html.count(AUTHORITY_MARKER) != 1:
            raise SystemExit(f'Phase 148: expected one Home authority-pathways paragraph: {lang}')
        if f'href="{item["href"]}"' in html or f"href='{item['href']}'" in html:
            raise SystemExit(f'Phase 148: event destination already linked from Home: {lang}')

        marker_at = html.index(AUTHORITY_MARKER)
        close_at = html.find('</p>', marker_at)
        if close_at < 0:
            raise SystemExit(f'Phase 148: malformed Home authority-pathways paragraph: {lang}')
        insert_at = close_at + len('</p>')
        pending[path] = html[:insert_at] + block + html[insert_at:]

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')

    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 148: unexpected sitemap change')

    print(
        f'PASS: Phase 148 — {len(pending)} localized Home pages gain one same-language '
        'Private Events pathway; no URL, schema, form or sitemap change'
    )
    enhance_localized_dining_paths(root)


if __name__ == '__main__':
    enhance()
