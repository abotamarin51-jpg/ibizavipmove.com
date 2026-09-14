"""Phase 154: strengthen localized yacht discovery from FR/DE/AR Home pages.

GSC currently reports the FR and AR yacht pages as unknown to Google and the DE yacht page as
crawled but not indexed, while all three targets are live, indexable, self-canonical and valid.
Wrap only the existing localized Home yacht words with same-language links to the existing yacht
service URLs. No visible copy, URL, schema, form, tracking, price, policy or sitemap change.
"""
from pathlib import Path
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
STYLE = 'text-decoration:underline;text-underline-offset:.15em'
MARKER = 'data-ivm154="yacht"'
PAGES = {
    'fr': ('yachts', '/fr/location-yacht-ibiza/'),
    'de': ('Yachten', '/de/yachtcharter-ibiza/'),
    'ar': ('يخوت', '/ar/yacht-charter-ibiza/'),
}


def linked_phrase(label: str, href: str) -> str:
    return f'<a {MARKER} href="{href}" style="{STYLE}">{label}</a>'


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    pending = {}
    for lang, (label, href) in PAGES.items():
        source = root / lang / 'index.html'
        target = root / href.strip('/') / 'index.html'
        if not source.is_file() or not target.is_file() or (BASE + href).encode() not in sitemap:
            raise SystemExit(f'Phase 154: missing reviewed source or destination: {lang}')
        html = source.read_text(encoding='utf-8')
        linked = linked_phrase(label, href)
        if MARKER in html:
            if html.count(MARKER) != 1 or html.count(linked) != 1:
                raise SystemExit(f'Phase 154: malformed existing yacht link: {lang}')
            continue
        if re.search(r'href=[\"\']' + re.escape(href) + r'[\"\']', html):
            raise SystemExit(f'Phase 154: yacht destination already linked from Home: {lang}')
        paragraphs = [m for m in re.finditer(r'<p\b[^>]*class=[\"\'][^\"\']*\blarge\b[^\"\']*[\"\'][^>]*>.*?</p>', html, re.I | re.S) if label in m.group()]
        if len(paragraphs) != 1 or paragraphs[0].group().count(label) != 1:
            raise SystemExit(f'Phase 154: expected one reviewed Home service paragraph for {lang}')
        block = paragraphs[0].group()
        updated_block = block.replace(label, linked, 1)
        pending[source] = html[:paragraphs[0].start()] + updated_block + html[paragraphs[0].end():]
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 154: sitemap changed unexpectedly')
    print(f'PASS: Phase 154 — {len(pending)} localized Home yacht mentions linked to existing same-language yacht pages; no visible copy or URL change')


if __name__ == '__main__':
    enhance()
