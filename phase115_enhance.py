"""Give the required phone field native telephone semantics on all five contact desks."""
from pathlib import Path
import re

ROOT = Path('_site')
CONTACTS = [
    'contact/index.html',
    'es/contacto/index.html',
    'fr/contact/index.html',
    'de/kontakt/index.html',
    'ar/contact/index.html',
]

PHONE_TAG_RE = re.compile(r'<input\b[^>]*\bid="fPhone"[^>]*>', re.I)


def enhance():
    pending = {}
    for rel in CONTACTS:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'Phase 115 contact page missing: {rel}')
        html = path.read_text(encoding='utf-8')
        matches = PHONE_TAG_RE.findall(html)
        if len(matches) != 1:
            raise SystemExit(f'Phase 115 expected exactly one phone input: {rel} -> {len(matches)}')
        tag = matches[0]
        if re.search(r'\btype\s*=\s*["\']tel["\']', tag, re.I):
            raise SystemExit(f'Phase 115 phone semantics already present: {rel}')
        if re.search(r'\btype\s*=', tag, re.I):
            raise SystemExit(f'Phase 115 unexpected existing phone type: {rel} -> {tag}')
        if not re.search(r'\bautocomplete\s*=\s*["\']tel["\']', tag, re.I):
            raise SystemExit(f'Phase 115 autocomplete tel missing before patch: {rel}')
        if re.search(r'\bpattern\s*=', tag, re.I):
            raise SystemExit(f'Phase 115 refuses rigid international phone pattern: {rel}')
        new_tag = tag[:-1] + ' type="tel" inputmode="tel">'
        pending[path] = html.replace(tag, new_tag, 1)

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print('PASS: Phase 115 — five contact phone fields now use type=tel + inputmode=tel while preserving autocomplete=tel and unrestricted international formats')


if __name__ == '__main__':
    enhance()
