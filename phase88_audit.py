from pathlib import Path
from html import unescape
import re

ROOT=Path('_site')
PAGE=ROOT/'private-concierge-ibiza'/'index.html'

if not PAGE.exists():
    raise SystemExit('Phase 88 audit private concierge page missing')
html=PAGE.read_text(encoding='utf-8')
sections=re.findall(r'<section\b[^>]*class="[^"]*ivm-concierge-standards[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
if len(sections)!=1:
    raise SystemExit(f'Phase 88 expected one concierge standards section, found {len(sections)}')
text=re.sub(r'<[^>]+>',' ',sections[0])
text=unescape(re.sub(r'\s+',' ',text)).strip()
for needle in ['one accountable point of contact','confirmed in writing','actually confirmed','do not promise','peak season','how Ibiza VIP Move works']:
    if needle.lower() not in text.lower():
        raise SystemExit(f'Phase 88 missing decision signal: {needle}')
if '/about/' not in sections[0] or '/contact/' not in sections[0]:
    raise SystemExit('Phase 88 missing trust/conversion internal links')
full=re.sub(r'<script\b.*?</script>|<style\b.*?</style>',' ',html,flags=re.I|re.S)
full=re.sub(r'<[^>]+>',' ',full)
words=re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9’'-]+",unescape(full))
if len(words)<850:
    raise SystemExit(f'Phase 88 private concierge page still too thin: {len(words)} words')
print(f'PASS: Phase 88 audit — private concierge decision criteria, confirmation standards and trust pathways verified ({len(words)} words)')
