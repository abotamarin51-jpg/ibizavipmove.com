"""Keep legacy localized authority/editorial footers inside the same language journey.

Nine FR, nine DE and nine AR pages still use an older footer whose core
commercial links point to English routes even though localized equivalents
already exist. This phase changes only those five footer hrefs per page:
Services, Concierge, Partners, About and Request Concierge.

Visible copy, legal links, media route, Black Book route, schema, sitemap,
tracking, WhatsApp destination, prices and service scope are unchanged.
"""
from pathlib import Path

ROOT = Path('_site')

TARGET_PAGES = {
    'fr': (
        'fr/ibiza-intelligence',
        'fr/media-partners',
        'fr/a-propos',
        'fr/ibiza-intelligence/nightlife-transport-planning',
        'fr/ibiza-intelligence/villa-arrival-planning',
        'fr/ibiza-intelligence/ibiza-august-planning',
        'fr/ibiza-intelligence/ibiza-formentera-yacht-day',
        'fr/ibiza-intelligence/private-aviation-ground-coordination',
        'fr/ibiza-intelligence/private-arrival',
    ),
    'de': (
        'de/ueber-uns',
        'de/ibiza-intelligence',
        'de/media-partners',
        'de/ibiza-intelligence/nightlife-transport-planning',
        'de/ibiza-intelligence/villa-arrival-planning',
        'de/ibiza-intelligence/ibiza-august-planning',
        'de/ibiza-intelligence/ibiza-formentera-yacht-day',
        'de/ibiza-intelligence/private-aviation-ground-coordination',
        'de/ibiza-intelligence/private-arrival',
    ),
    'ar': (
        'ar/about',
        'ar/ibiza-intelligence',
        'ar/media-partners',
        'ar/ibiza-intelligence/nightlife-transport-planning',
        'ar/ibiza-intelligence/villa-arrival-planning',
        'ar/ibiza-intelligence/ibiza-august-planning',
        'ar/ibiza-intelligence/ibiza-formentera-yacht-day',
        'ar/ibiza-intelligence/private-aviation-ground-coordination',
        'ar/ibiza-intelligence/private-arrival',
    ),
}

ROUTES = {
    'fr': (
        ('<a href="/services/">Services</a>', '<a href="/fr/services/">Services</a>'),
        ('<a href="/private-concierge-ibiza/">Concierge</a>', '<a href="/fr/conciergerie-privee-ibiza/">Concierge</a>'),
        ('<a href="/partners/">Travel Partners</a>', '<a href="/fr/partners/">Travel Partners</a>'),
        ('<a href="/about/">About</a>', '<a href="/fr/a-propos/">About</a>'),
        ('<a href="/contact/">Request Concierge</a>', '<a href="/fr/contact/">Request Concierge</a>'),
    ),
    'de': (
        ('<a href="/services/">Services</a>', '<a href="/de/services/">Services</a>'),
        ('<a href="/private-concierge-ibiza/">Concierge</a>', '<a href="/de/privater-concierge-ibiza/">Concierge</a>'),
        ('<a href="/partners/">Travel Partners</a>', '<a href="/de/partners/">Travel Partners</a>'),
        ('<a href="/about/">About</a>', '<a href="/de/ueber-uns/">About</a>'),
        ('<a href="/contact/">Request Concierge</a>', '<a href="/de/kontakt/">Request Concierge</a>'),
    ),
    'ar': (
        ('<a href="/services/">Services</a>', '<a href="/ar/services/">Services</a>'),
        ('<a href="/private-concierge-ibiza/">Concierge</a>', '<a href="/ar/private-concierge-ibiza/">Concierge</a>'),
        ('<a href="/partners/">Travel Partners</a>', '<a href="/ar/partners/">Travel Partners</a>'),
        ('<a href="/about/">About</a>', '<a href="/ar/about/">About</a>'),
        ('<a href="/contact/">Request Concierge</a>', '<a href="/ar/contact/">Request Concierge</a>'),
    ),
}


def enhance():
    pending = {}
    changed = 0
    for lang, slugs in TARGET_PAGES.items():
        for slug in slugs:
            page = ROOT / slug / 'index.html'
            if not page.is_file():
                raise SystemExit(f'Phase 136 missing target page: {slug}')
            html = page.read_text(encoding='utf-8')
            footer_start = html.find('<footer')
            footer_end = html.find('</footer>', footer_start)
            if footer_start < 0 or footer_end < 0:
                raise SystemExit(f'Phase 136 footer missing: {slug}')
            footer_end += len('</footer>')
            footer = html[footer_start:footer_end]
            for old, new in ROUTES[lang]:
                old_count = footer.count(old)
                new_count = footer.count(new)
                if old_count == 0 and new_count == 1:
                    continue
                if old_count != 1 or new_count != 0:
                    raise SystemExit(
                        f'Phase 136 route cardinality drift on {slug}: '
                        f'{old_count=} {new_count=} {old}'
                    )
                footer = footer.replace(old, new, 1)
                changed += 1
            pending[page] = html[:footer_start] + footer + html[footer_end:]

    for page, html in pending.items():
        page.write_text(html, encoding='utf-8')
    print(f'PASS: Phase 136 localized legacy footers — {changed} commercial hrefs now remain inside FR/DE/AR journeys across 27 pages')


if __name__ == '__main__':
    enhance()
