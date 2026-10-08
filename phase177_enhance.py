"""Add one contextual pathway from Private Chauffeur to the existing Luxury Car Hire page.

Phase 177 adds one useful self-drive alternative link. It changes no URL, title,
meta description, schema, sitemap, tracking, contact route, price or booking term.
"""
from pathlib import Path

PATH = Path('_site/private-chauffeur-ibiza/index.html')
OLD = 'A chauffeur booking can cover one transfer or several movements under one brief. For complex stays, transport can be coordinated alongside reservations, security, private aviation and other concierge requirements.'
NEW = OLD + ' For self-drive requests, see <a class="text-link" href="/luxury-car-rental-ibiza/">Luxury Car Hire &amp; Rental</a>.'


def enhance():
    html = PATH.read_text(encoding='utf-8')
    if NEW in html:
        if html.count(NEW) != 1:
            raise SystemExit('Phase 177: duplicate Chauffeur-to-Car-Hire pathway')
        print('PASS: Phase 177 — Chauffeur-to-Car-Hire pathway already present')
        return

    if html.count(OLD) != 1:
        raise SystemExit('Phase 177: expected one chauffeur coordination paragraph')

    if 'href="/luxury-car-rental-ibiza/"' in html:
        raise SystemExit('Phase 177: unexpected existing Car Hire link requires review')

    PATH.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 177 — one Chauffeur-to-Car-Hire contextual pathway added')


if __name__ == '__main__':
    enhance()
