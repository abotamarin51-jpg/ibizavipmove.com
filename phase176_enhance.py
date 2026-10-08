"""Add one reciprocal contextual link from Yacht Charter to the existing Formentera planning guide.

Phase 176 changes no URL, title, meta description, schema, sitemap, tracking,
contact route, service claim, availability statement or booking term.
"""
from pathlib import Path

PATH = Path('_site/yacht-charter-ibiza/index.html')
OLD = 'Formentera can be requested where suitable for the confirmed charter and conditions.'
NEW = '<a class="text-link" href="/ibiza-intelligence/ibiza-formentera-yacht-day/">Formentera</a> can be requested where suitable for the confirmed charter and conditions.'


def enhance():
    html = PATH.read_text(encoding='utf-8')
    if NEW in html:
        if html.count(NEW) != 1:
            raise SystemExit('Phase 176: duplicate Yacht-to-Formentera guide pathway')
        print('PASS: Phase 176 — Yacht-to-Formentera guide pathway already present')
        return

    if html.count(OLD) != 1:
        raise SystemExit('Phase 176: expected one existing Formentera charter sentence')

    if '/ibiza-intelligence/ibiza-formentera-yacht-day/' in html:
        raise SystemExit('Phase 176: unexpected existing Formentera guide link requires review')

    PATH.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 176 — one Yacht-to-Formentera guide pathway added')


if __name__ == '__main__':
    enhance()
