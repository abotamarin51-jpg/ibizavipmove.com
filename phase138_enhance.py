"""Keep localized Ibiza VIP Move wordmarks inside the visitor's language journey.

A subset of FR/DE/AR pages still links the clickable brand wordmark to the
English homepage (`/`) even though `/fr/`, `/de/` and `/ar/` already exist.
This phase changes only those wordmark hrefs. Explicit language-switch links to
English, visible copy, schema, canonicals, sitemap, forms and tracking remain
untouched.
"""
from pathlib import Path
import re

ROOT = Path('_site')
LANGS = {'fr': '/fr/', 'de': '/de/', 'ar': '/ar/'}
WORDMARK = re.compile(r'<a(?P<attrs>[^>]*\bclass="[^"]*\bwordmark\b[^"]*"[^>]*)>')
EXPECTED_CHANGES = 45


def enhance():
    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    pending = {}
    changed = 0
    pages = 0

    for lang, home in LANGS.items():
        for page in sorted((ROOT / lang).rglob('index.html')):
            html = page.read_text(encoding='utf-8')
            page_changes = 0

            def replace_wordmark(match):
                nonlocal page_changes
                tag = match.group(0)
                if 'href="/"' in tag:
                    page_changes += 1
                    return tag.replace('href="/"', f'href="{home}"', 1)
                return tag

            updated = WORDMARK.sub(replace_wordmark, html)
            if page_changes:
                if page_changes != 1:
                    raise SystemExit(
                        f'Phase 138 wordmark cardinality drift on {page}: {page_changes}'
                    )
                pending[page] = updated
                changed += page_changes
                pages += 1

    if changed not in (0, EXPECTED_CHANGES) or pages not in (0, EXPECTED_CHANGES):
        raise SystemExit(
            f'Phase 138 expected {EXPECTED_CHANGES} localized wordmark routes or an '
            f'already-enhanced site, got {changed=} {pages=}'
        )
    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 138 sitemap changed unexpectedly')

    for page, html in pending.items():
        page.write_text(html, encoding='utf-8')
    print(
        f'PASS: Phase 138 localized wordmark home routing — {changed} hrefs changed '
        f'across {pages} FR/DE/AR pages; explicit language switches untouched'
    )


if __name__ == '__main__':
    enhance()
