from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)

PAGES = {
    '/es/private-office/': 'Private Office Ibiza | Soporte para PAs y Family Offices | Ibiza VIP Move',
    '/es/partners/': 'Partners B2B Ibiza | Operador local para Luxury Travel | Ibiza VIP Move',
    '/fr/private-office/': 'Private Office à Ibiza | Assistants privés & Family Offices | Ibiza VIP Move',
    '/fr/partners/': 'Partenaires B2B à Ibiza | Opérateur local Luxury Travel | Ibiza VIP Move',
    '/de/private-office/': 'Private Office auf Ibiza | Assistenz für Family Offices | Ibiza VIP Move',
    '/de/partners/': 'B2B Partner auf Ibiza | Local Operator für Luxury Travel | Ibiza VIP Move',
    '/ar/private-office/': 'Private Office في إيبيزا | دعم المساعدين وFamily Offices | Ibiza VIP Move',
    '/ar/partners/': 'شركاء B2B في إيبيزا | تشغيل محلي للسفر الفاخر | Ibiza VIP Move',
}

for path, title in PAGES.items():
    file = ROOT / path.strip('/') / 'index.html'
    if not file.exists():
        raise SystemExit(f'Phase 51 metadata target missing: {path}')
    html = file.read_text(encoding='utf-8')
    html, n = re.subn(r'<title>.*?</title>', f'<title>{escape(title)}</title>', html, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f'Title missing on {path}')
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        lambda m: m.group(1) + escape(title) + m.group(2),
        html,
        count=1,
        flags=re.I,
    )

    def schema_repl(match):
        try:
            obj = json.loads(match.group(1))
        except Exception:
            return match.group(0)
        if isinstance(obj, dict) and obj.get('@type') == 'WebPage':
            obj['name'] = title
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

    html = SCRIPT_RE.sub(schema_repl, html)
    file.write_text(html, encoding='utf-8')

# Ensure the eight new titles are unique among themselves and correctly applied.
seen = set()
for path, expected in PAGES.items():
    html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
    match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    assert match and match.group(1).strip() == expected, path
    assert expected not in seen, ('duplicate Phase 51 title', expected)
    seen.add(expected)
    assert f'content="{escape(expected)}"' in html, (path, 'og:title')

print(f'PASS: Phase 51 unique localized metadata normalized on {len(PAGES)} B2B pages')
