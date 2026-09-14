"""Phase 151: localize residual Partners-page WhatsApp handoff messages.

Replace only the two generic English WhatsApp prefill URLs that remain on each FR/DE/AR
Partners page (footer + mobile contact bar) with the B2B partnership message already used
on that same localized page. No visible copy, phone number, URL, schema, tracking, form,
price, policy, sitemap or navigation change.
"""
from pathlib import Path
from urllib.parse import quote
from phase152_enhance import enhance as enhance_media_partner_hero
from phase155_mobile_reflow import enhance as enhance_german_partner_reflow

ROOT = Path('_site')
PHONE = '34600703303'
GENERIC_MESSAGE = "Hello Ibiza VIP Move, I'm interested in private concierge support in Ibiza. Could you please help me with availability and the next steps? Thank you."
GENERIC_HREF = f'https://wa.me/{PHONE}?text={quote(GENERIC_MESSAGE)}'
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
        generic_count = html.count(GENERIC_HREF)
        target_count = html.count(target)
        if generic_count == 0:
            if target_count != 3:
                raise SystemExit(f'Phase 151: expected three localized B2B WhatsApp handoffs on {slug}, found {target_count}')
            continue
        if generic_count != 2 or target_count != 1:
            raise SystemExit(
                f'Phase 151: unexpected WhatsApp baseline on {slug}: generic={generic_count}, localized_b2b={target_count}'
            )
        pending[path] = html.replace(GENERIC_HREF, target)

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 151: sitemap changed unexpectedly')
    print(f'PASS: Phase 151 — localized {len(pending) * 2} residual Partners WhatsApp handoffs; visible copy and contact number unchanged')
    enhance_media_partner_hero(root)
    enhance_german_partner_reflow(root)


if __name__ == '__main__':
    enhance()
