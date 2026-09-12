"""Read-only gate for international phone guidance on the five concierge desks."""
from pathlib import Path
import re

ROOT = Path('_site')
CONTACTS = {
    'contact/index.html': ('en', 'international country code', '+44'),
    'es/contacto/index.html': ('es', 'prefijo internacional', '+34'),
    'fr/contact/index.html': ('fr', 'indicatif international', '+33'),
    'de/kontakt/index.html': ('de', 'internationale Landesvorwahl', '+49'),
    'ar/contact/index.html': ('ar', 'رمز الدولة الدولي', '+971'),
}


def run():
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    for rel, (lang, phrase, example) in CONTACTS.items():
        path = ROOT / rel
        html = path.read_text(encoding='utf-8')
        tags = re.findall(r'<input\b[^>]*\bid="fPhone"[^>]*>', html, re.I)
        if len(tags) != 1:
            raise SystemExit(f'Phase 118 audit phone input count: {rel} -> {len(tags)}')
        tag = tags[0]
        checks = {
            'required': re.search(r'\brequired\b', tag, re.I),
            'type tel': re.search(r'\btype="tel"', tag, re.I),
            'inputmode tel': re.search(r'\binputmode="tel"', tag, re.I),
            'autocomplete tel': re.search(r'\bautocomplete="tel"', tag, re.I),
            'describedby': 'aria-describedby="fPhoneHint"' in tag,
            'no rigid pattern': not re.search(r'\bpattern\s*=', tag, re.I),
            'one helper': html.count('id="fPhoneHint"') == 1,
            'localized guidance': phrase in html and example in html,
            'form exists': ('id="conciergeForm"' in html or 'id="localizedConciergeForm"' in html),
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            raise SystemExit(f'Phase 118 audit failed {rel}: {failed}')
        hm = re.search(r'<html\b[^>]*\blang="([^"]+)"', html, re.I)
        if not hm or hm.group(1).lower().split('-')[0] != lang:
            raise SystemExit(f'Phase 118 language drift: {rel}')
        cm = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
        if not cm or cm.group(1) not in sitemap:
            raise SystemExit(f'Phase 118 canonical/sitemap drift: {rel}')
    print('PASS: Phase 118 audit — EN/ES/FR/DE/AR phone fields retain flexible tel semantics and expose one localized, screen-reader-associated country-code hint each')


if __name__ == '__main__':
    run()
