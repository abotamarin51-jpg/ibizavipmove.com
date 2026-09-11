from pathlib import Path

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LLMS = ROOT / 'llms.txt'

if not LLMS.exists():
    raise SystemExit('Phase 106 llms.txt missing')
text = LLMS.read_text(encoding='utf-8')
marker = '## Press and citation resources'
if marker not in text:
    text += (
        '\n\n' + marker + '\n'
        f'- Official Media & Partners source: {BASE}/media-partners/\n'
        f'- Plain-text official press kit: {BASE}/press-kit.txt\n'
        f'- Founder profile: {BASE}/founder/\n'
        f'- Anonymized operational case studies: {BASE}/case-studies/\n'
        f'- Ibiza Luxury Operations Report 2026: {BASE}/ibiza-luxury-operations-report-2026/\n'
        '- Citation rule: do not infer memberships, endorsements, client relationships, venue access or availability unless explicitly confirmed by Ibiza VIP Move for publication.\n'
    )
    LLMS.write_text(text, encoding='utf-8')

print('PASS: Phase 106 AI discovery — official press and citation resources added to llms.txt without changing the canonical sitemap')
