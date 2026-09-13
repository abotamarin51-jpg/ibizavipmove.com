"""Clarify the English services hub H1 around its actual Ibiza concierge intent.

Verified Search Console performance shows /services/ receiving impressions for
concierge/VIP-service queries while the existing title and description are
explicit but the visible H1 is purely editorial. This phase keeps the same URL,
title, metadata, schema, navigation and service inventory and replaces only the
H1 with a descriptive people-first heading that states the service and place.
"""
from pathlib import Path

ROOT = Path('_site')
PAGE = ROOT / 'services' / 'index.html'
OLD = '<h1>One private ecosystem.<br>Every moving part connected.</h1>'
NEW = '<h1>Luxury concierge services in Ibiza,<br>connected through one trusted contact.</h1>'


def enhance():
    if not PAGE.is_file():
        raise SystemExit('Phase 132 services page missing')
    html = PAGE.read_text(encoding='utf-8')

    # Idempotent already-enhanced state.
    if NEW in html and OLD not in html:
        if html.count(NEW) != 1:
            raise SystemExit(f'Phase 132 enhanced H1 cardinality drift: {html.count(NEW)}')
        print('PASS: Phase 132 services H1 already aligned')
        return

    if html.count(OLD) != 1:
        raise SystemExit(f'Phase 132 expected one original services H1: {html.count(OLD)}')
    html = html.replace(OLD, NEW, 1)
    PAGE.write_text(html, encoding='utf-8')
    print('PASS: Phase 132 clarified /services/ H1 without changing URL, metadata or service scope')


if __name__ == '__main__':
    enhance()
