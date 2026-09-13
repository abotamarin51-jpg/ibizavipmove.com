"""Give qualified contact forms one validation/submission owner, without new assets."""
from pathlib import Path
import re
from phase135_enhance import enhance as enhance_localized_services_routing

ROOT = Path('_site')
CONTACTS = ('contact', 'es/contacto', 'fr/contact', 'de/kontakt', 'ar/contact')
OLD = "const f=document.getElementById('conciergeForm');\nif(f){"
NEW = "const f=document.getElementById('conciergeForm');\nif(f&&!f.hasAttribute('data-ivm-qualified-brief')){"
LEGACY = re.compile(r"<script\b[^>]*>\(function\(\)\{const f=document.getElementById\('localizedConciergeForm'\);.*?</script>", re.S)


def enhance():
    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    runtime = ROOT / 'assets/premium.js'
    js = runtime.read_text(encoding='utf-8')
    if js.count(OLD) == 1 and NEW not in js:
        js = js.replace(OLD, NEW, 1)
    elif js.count(NEW) != 1 or OLD in js:
        raise SystemExit('Phase 133: legacy form-owner guard drift')
    pending = {runtime: js}
    removed = 0
    for slug in CONTACTS:
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        if html.count('data-ivm-qualified-brief="true"') != 1:
            raise SystemExit(f'Phase 133: qualified form missing on {slug}')
        if len(re.findall(r'<script\b[^>]*src="/assets/phase107\.js\?v=\d+"[^>]*\bdefer\b', html)) != 1:
            raise SystemExit(f'Phase 133: modern form runtime missing on {slug}')
        old_blocks = LEGACY.findall(html)
        already = '/assets/premium.js?v=133' in html
        expected = 0 if slug == 'contact' or already else 1
        if len(old_blocks) != expected:
            raise SystemExit(f'Phase 133: obsolete inline runtime drift on {slug}')
        html, count = LEGACY.subn('', html)
        removed += count
        html, count = re.subn(r'(/assets/premium\.js\?v=)\d+', r'\g<1>133', html)
        if count != 1:
            raise SystemExit(f'Phase 133: shared-runtime reference drift on {slug}')
        pending[path] = html
    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 133: sitemap changed unexpectedly')
    for path, content in pending.items():
        path.write_text(content, encoding='utf-8')
    print(f'PASS: Phase 133 single form owner; legacy English handler gated, {removed} obsolete localized inline scripts removed; five cache-versioned references; no new asset/URL')


if __name__ == '__main__':
    enhance()
    enhance_localized_services_routing()
