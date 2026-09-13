"""Keep localized contact-page Explore links inside the visitor's language journey.

The FR, DE and AR contact pages still carry three legacy Explore links to
English routes even though localized equivalents already exist: Private Office,
The Ibiza Black Book and International Clients. This phase changes only those
nine hrefs (three per page). Visible copy, form behavior, WhatsApp destination,
tracking, schema, sitemap, legal links and service scope are unchanged.
"""
from pathlib import Path

ROOT = Path('_site')

TARGETS = {
    'fr/contact': (
        ('<a href="/private-office/">Private Office</a>', '<a href="/fr/private-office/">Private Office</a>'),
        ('<a href="/ibiza-intelligence/">The Ibiza Black Book</a>', '<a href="/fr/ibiza-intelligence/">The Ibiza Black Book</a>'),
        ('<a href="/international-clients/">International Clients</a>', '<a href="/fr/clients-internationaux/">International Clients</a>'),
    ),
    'de/kontakt': (
        ('<a href="/private-office/">Private Office</a>', '<a href="/de/private-office/">Private Office</a>'),
        ('<a href="/ibiza-intelligence/">The Ibiza Black Book</a>', '<a href="/de/ibiza-intelligence/">The Ibiza Black Book</a>'),
        ('<a href="/international-clients/">International Clients</a>', '<a href="/de/internationale-kunden/">International Clients</a>'),
    ),
    'ar/contact': (
        ('<a href="/private-office/">Private Office</a>', '<a href="/ar/private-office/">Private Office</a>'),
        ('<a href="/ibiza-intelligence/">The Ibiza Black Book</a>', '<a href="/ar/ibiza-intelligence/">The Ibiza Black Book</a>'),
        ('<a href="/international-clients/">International Clients</a>', '<a href="/ar/international-clients/">International Clients</a>'),
    ),
}


def enhance():
    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    pending = {}
    changed = 0
    for slug, routes in TARGETS.items():
        page = ROOT / slug / 'index.html'
        if not page.is_file():
            raise SystemExit(f'Phase 137 missing contact page: {slug}')
        html = page.read_text(encoding='utf-8')
        footer_start = html.find('<footer')
        footer_end = html.find('</footer>', footer_start)
        if footer_start < 0 or footer_end < 0:
            raise SystemExit(f'Phase 137 footer missing: {slug}')
        footer_end += len('</footer>')
        footer = html[footer_start:footer_end]
        for old, new in routes:
            old_count = footer.count(old)
            new_count = footer.count(new)
            if old_count == 0 and new_count == 1:
                continue
            if old_count != 1 or new_count != 0:
                raise SystemExit(
                    f'Phase 137 route cardinality drift on {slug}: '
                    f'{old_count=} {new_count=} {old}'
                )
            footer = footer.replace(old, new, 1)
            changed += 1
        pending[page] = html[:footer_start] + footer + html[footer_end:]

    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 137 sitemap changed unexpectedly')
    for page, html in pending.items():
        page.write_text(html, encoding='utf-8')
    print(f'PASS: Phase 137 localized contact Explore routing — {changed} hrefs now remain inside FR/DE/AR journeys across 3 contact pages')


if __name__ == '__main__':
    enhance()
