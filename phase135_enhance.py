"""Keep priority localized Services conversion CTAs inside the same language journey.

FR/DE/AR Services hubs already expose localized contact pages in their navigation,
but the two primary conversion CTAs on each hub still route to the English
/contact/ page. This phase changes only those six href values to the existing
localized contact routes. No visible copy, URL inventory, schema, sitemap,
tracking, WhatsApp destination, pricing or service scope changes.
"""
from pathlib import Path

ROOT = Path('_site')
TARGETS = {
    'fr/services': '/fr/contact/',
    'de/services': '/de/kontakt/',
    'ar/services': '/ar/contact/',
}


def enhance():
    pending = {}
    changed_links = 0
    for slug, local_contact in TARGETS.items():
        page = ROOT / slug / 'index.html'
        target_page = ROOT / local_contact.strip('/') / 'index.html'
        if not page.is_file() or not target_page.is_file():
            raise SystemExit(f'Phase 135 missing source/target for {slug}')
        html = page.read_text(encoding='utf-8')
        old_count = html.count('href="/contact/"')
        local_count = html.count(f'href="{local_contact}"')
        if old_count == 0 and local_count == 4:
            continue
        if old_count != 2:
            raise SystemExit(f'Phase 135 expected two English contact CTA links on {slug}: {old_count}')
        if local_count != 2:
            raise SystemExit(f'Phase 135 expected two existing localized contact routes on {slug}: {local_count}')
        html2 = html.replace('href="/contact/"', f'href="{local_contact}"')
        if html2.count(f'href="{local_contact}"') != 4 or 'href="/contact/"' in html2:
            raise SystemExit(f'Phase 135 localized contact routing validation failed on {slug}')
        pending[page] = html2
        changed_links += 2
    for page, html in pending.items():
        page.write_text(html, encoding='utf-8')
    print(f'PASS: Phase 135 localized Services conversion routing — {changed_links} CTA links now stay in FR/DE/AR contact journeys')


if __name__ == '__main__':
    enhance()
