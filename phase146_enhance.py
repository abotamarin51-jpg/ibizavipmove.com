"""Link existing chef/wellness mentions on FR/DE/AR Home pages.

Navigation-only: no new copy, service, URL, tracking, schema or freshness change.
Validate every source and destination before writing any generated HTML.
"""
from pathlib import Path
import re

ROOT = Path('_site')
MARKER = 'data-ivm146="service"'
STYLE = 'text-decoration:underline;text-underline-offset:.15em'
PAGES = {
    'fr': (
        'Chauffeur privé, villas, yachts, aviation privée, restaurants, beach clubs, nightlife, sécurité, chefs privés, wellness et demandes sur mesure — coordonnés autour de votre planning et de vos préférences.',
        (('chefs privés', '/fr/chef-prive-personnel-villa-ibiza/'), ('wellness', '/fr/wellness-ibiza/')),
    ),
    'de': (
        'Privater Chauffeur, Luxusvillen, Yachten, private Aviation, Restaurants, Beach Clubs, Nightlife, Sicherheit, private Köche, Wellness und individuelle Wünsche — abgestimmt auf Ihren Zeitplan und Ihre Prioritäten.',
        (('private Köche', '/de/privatkoch-villa-staff-ibiza/'), ('Wellness', '/de/wellness-ibiza/')),
    ),
    'ar': (
        'سائق خاص، فلل فاخرة، يخوت، طيران خاص، مطاعم ونوادٍ شاطئية، حياة ليلية، أمن خاص، طهاة، عافية وطلبات مخصصة — كلها منسقة وفق جدولك وتفضيلاتك.',
        (('طهاة', '/ar/private-chef-staffing-ibiza/'), ('عافية', '/ar/wellness-ibiza/')),
    ),
}


def linked_paragraph(text: str, links: tuple) -> str:
    result = text
    for label, href in links:
        if result.count(label) != 1:
            raise SystemExit('Phase 146: ambiguous existing service wording')
        result = result.replace(label, f'<a {MARKER} href="{href}" style="{STYLE}">{label}</a>', 1)
    return '<p class="large">' + result + '</p>'


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    pending = {}
    for lang, (text, links) in PAGES.items():
        path = root / lang / 'index.html'
        html = path.read_text(encoding='utf-8')
        before = '<p class="large">' + text + '</p>'
        after = linked_paragraph(text, links)
        for _, href in links:
            target = root / href.strip('/') / 'index.html'
            if not target.is_file() or ('https://ibizavipmove.com' + href).encode() not in sitemap:
                raise SystemExit(f'Phase 146: missing canonical destination {href}')
        if MARKER in html:
            if html.count(MARKER) != 2 or html.count(after) != 1 or before in html:
                raise SystemExit(f'Phase 146: malformed existing Home links: {lang}')
            continue
        if html.count(before) != 1:
            raise SystemExit(f'Phase 146: expected one unchanged Home paragraph: {lang}')
        # Destinations must genuinely be absent from the original Home navigation.
        for _, href in links:
            if re.search(r'href=[\"\']' + re.escape(href) + r'[\"\']', html):
                raise SystemExit(f'Phase 146: destination already linked; review {lang}: {href}')
        pending[path] = html.replace(before, after, 1)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 146: unexpected sitemap change')
    print(f'PASS: Phase 146 — {len(pending)} localized Home pages updated; six contextual service links, no new copy or URLs')


if __name__ == '__main__':
    enhance()
