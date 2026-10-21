"""Improve the existing English Private Office enquiry handoff without new URLs."""
from html import escape
from pathlib import Path
from urllib.parse import quote
import re

ROOT = Path('_site')
PAGE = ROOT / 'private-office' / 'index.html'
BASE = 'https://ibizavipmove.com'
CANONICAL = BASE + '/private-office/'
CONTACT = '/contact/'
WA = 'https://wa.me/34600703303'
MESSAGE = (
    'Hello Ibiza VIP Move, I would like to discuss Private Office coordination for a private stay in Ibiza. '
    'Before sharing the full brief, I would like to confirm the required services, approval contacts and '
    'preferred communication structure.'
)
WA_HREF = WA + '?text=' + quote(MESSAGE, safe='')
BRIEF = (
    'For the first message, share the dates, guest count, required services and your role. '
    'Include your time zone, who may approve requests and whether communication should stay through you. '
    'Identity documents or bank details are not needed in the first message.'
)
FORM_LINK = (
    '<p><a class="text-link" data-ivm179="contact" href="/contact/">'
    'Prepare the request with the private form</a></p>'
)


def enhance_html(original: str) -> str:
    if '<html lang="en"' not in original or f'<link rel="canonical" href="{CANONICAL}"' not in original:
        raise ValueError('Phase 179 English Private Office identity mismatch')

    match = re.search(r'(<main\b[^>]*>)(.*?)(</main>)', original, re.I | re.S)
    if not match:
        raise ValueError('Phase 179 main landmark missing')
    main = match.group(2)

    if 'data-ivm179=' in main:
        if (main.count('data-ivm179="office"') != 2
                or main.count('data-ivm179="contact"') != 1
                or main.count('data-ivm179="brief"') != 1
                or main.count(WA_HREF) != 2
                or main.count(FORM_LINK) != 1):
            raise ValueError('Phase 179 existing handoff is malformed or duplicated')
        return original

    cta = re.search(
        r'(<section class="ivm-b2b-cta">.*?<h2>.*?</h2>)<p>.*?</p>',
        main,
        re.S,
    )
    if not cta:
        raise ValueError('Phase 179 Private Office CTA marker missing')
    replacement = (
        cta.group(1)
        + f'<p data-ivm179="brief">{escape(BRIEF)}</p>'
        + FORM_LINK
    )
    main = main.replace(cta.group(0), replacement, 1)

    targets = (
        f'<a class="btn gold" href="{WA}">Start a private brief</a>',
        f'<a class="btn ghost" href="{WA}">WhatsApp 24/7</a>',
    )
    for old in targets:
        if main.count(old) != 1:
            raise ValueError(f'Phase 179 expected exactly one reviewed CTA: {old}')
        new = old.replace(
            f'href="{WA}"',
            f'data-ivm179="office" href="{WA_HREF}"',
        )
        main = main.replace(old, new, 1)

    if main.count(WA_HREF) != 2 or main.count(FORM_LINK) != 1:
        raise ValueError('Phase 179 generated handoff count mismatch')

    return original[:match.start(2)] + main + original[match.end(2):]


def enhance() -> None:
    if not PAGE.is_file() or not (ROOT / CONTACT.strip('/') / 'index.html').is_file():
        raise SystemExit('Phase 179 reviewed page or Contact target missing')
    original = PAGE.read_text(encoding='utf-8')
    updated = enhance_html(original)
    if updated != original:
        PAGE.write_text(updated, encoding='utf-8')
    print('PASS: Phase 179 — English Private Office adds one form route, a privacy-safe brief and two contextual WhatsApp drafts')


if __name__ == '__main__':
    enhance()
