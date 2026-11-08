"""Phase 151: localize residual Partners-page WhatsApp handoff messages.

Replace only the two shared navigation WhatsApp handoffs that remain on each FR/DE/AR
Partners page (header CTA + mobile menu) with the B2B partnership message already used
on that same localized page. No visible copy, phone number, URL, schema, tracking, form,
price, policy, sitemap or navigation change.
"""
from pathlib import Path
from urllib.parse import quote
import re
from phase152_enhance import enhance as enhance_media_partner_hero
from phase155_mobile_reflow import enhance as enhance_german_partner_reflow
from phase156_mobile_reflow import enhance as enhance_french_partner_reflow

ROOT = Path('_site')
PHONE = '34600703303'
GENERIC_MESSAGE = "Hello Ibiza VIP Move, I'm interested in private concierge support in Ibiza. Could you please help me with availability and the next steps? Thank you."
GENERIC_HREF = f'https://wa.me/{PHONE}?text={quote(GENERIC_MESSAGE)}'
WA_LINK_RE = re.compile(r'href="https://wa\.me/34600703303(?:\?text=[^"]*)?"')
PAGES = {
    'fr/partners': "Bonjour Ibiza VIP Move, je vous contacte au sujet d’un éventuel partenariat B2B pour Ibiza. Je souhaite présenter notre société et discuter de la manière dont nous pourrions travailler ensemble.",
    'de/partners': "Hallo Ibiza VIP Move, ich kontaktiere Sie wegen einer möglichen B2B-Partnerschaft für Ibiza. Ich möchte unser Unternehmen vorstellen und besprechen, wie wir zusammenarbeiten könnten.",
    'ar/partners': "مرحباً Ibiza VIP Move، أتواصل بخصوص شراكة B2B محتملة في إيبيزا. أرغب في تقديم شركتنا ومناقشة كيفية العمل معاً.",
}


def href(message: str) -> str:
    return f'https://wa.me/{PHONE}?text={quote(message)}'


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    pending = {}
    for slug, message in PAGES.items():
        path = root / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        target = href(message)
        target_count = html.count(target)
        if target_count == 3:
            continue
        # Only the shared header CTA and mobile-menu WhatsApp link are the
        # two residual navigation handoffs covered by this phase. Preserve
        # the four route-card messages and all other service-specific CTAs.
        for label, pattern in (
            ('header', re.compile(r'<header\b.*?</header>', re.I | re.S)),
            ('mobile menu', re.compile(r'<div\b[^>]*class="[^"]*\\bmobile-menu\\b[^"]*"[^>]*>.*?</div>', re.I | re.S)),
        ):
            match = pattern.search(html)
            if not match:
                raise SystemExit(f'Phase 151: {label} missing on {slug}')
            block = match.group(0)
            if target in block:
                continue
            if len(WA_LINK_RE.findall(block)) != 1:
                raise SystemExit(f'Phase 151: expected one WhatsApp link in {label} on {slug}')
            updated = WA_LINK_RE.sub(f'href="{target}"', block, count=1)
            html = html[:match.start()] + updated + html[match.end():]
        if html.count(target) != 3:
            raise SystemExit(f'Phase 151: expected three localized B2B WhatsApp handoffs on {slug}, found {html.count(target)}')
        pending[path] = html

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 151: sitemap changed unexpectedly')
    print(f'PASS: Phase 151 — localized {len(pending) * 2} residual Partners WhatsApp handoffs; visible copy and contact number unchanged')
    enhance_media_partner_hero(root)
    enhance_german_partner_reflow(root)
    enhance_french_partner_reflow(root)


if __name__ == '__main__':
    enhance()
