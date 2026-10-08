"""Clarify the Services hub -> Private Concierge intent with one contextual link.

Phase 175 changes no URL, title, meta description, schema, sitemap, tracking or contact route.
It turns the existing "Use the concierge" wording on the English Services hub into a
contextual link to the existing Private Concierge page.
"""
from pathlib import Path

ROOT = Path('_site')
PATH = ROOT / 'services' / 'index.html'
OLD = 'Use the concierge rather than managing each category separately.'
NEW = 'Use the <a class="text-link" href="/private-concierge-ibiza/">private concierge</a> rather than managing each category separately.'


def enhance():
    html = PATH.read_text(encoding='utf-8')
    if NEW in html:
        if html.count(NEW) != 1:
            raise SystemExit('Phase 175: duplicate contextual concierge pathway')
        print('PASS: Phase 175 — contextual Services-to-Private-Concierge pathway already present')
        return

    if html.count(OLD) != 1:
        raise SystemExit('Phase 175: expected one Services-hub concierge sentence')

    PATH.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 175 — contextual Services-to-Private-Concierge pathway added')


if __name__ == '__main__':
    enhance()
