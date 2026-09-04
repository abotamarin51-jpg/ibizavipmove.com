from pathlib import Path
from html import unescape
import re

ROOT=Path('_site')
HUBS={
'en':('/ibiza-intelligence/','/private-concierge-ibiza/'),
'es':('/es/ibiza-intelligence/','/es/concierge-privado-ibiza/'),
'fr':('/fr/ibiza-intelligence/','/fr/conciergerie-privee-ibiza/'),
'de':('/de/ibiza-intelligence/','/de/privater-concierge-ibiza/'),
'ar':('/ar/ibiza-intelligence/','/ar/private-concierge-ibiza/')}
NEEDLES={
'en':['accountable contact','Written confirmations','Realistic access','Change control'],
'es':['contacto responsable','Confirmaciones por escrito','Acceso realista','Control de cambios'],
'fr':['contact responsable','Confirmations écrites','Accès réaliste','Gestion des changements'],
'de':['verantwortlicher Kontakt','Schriftliche Bestätigungen','Realistischer Zugang','Änderungssteuerung'],
'ar':['جهة اتصال مسؤولة','تأكيدات مكتوبة','وصول واقعي','إدارة التغييرات']}

def clean(s):
    s=re.sub(r'<script\b.*?</script>|<style\b.*?</style>',' ',s,flags=re.I|re.S)
    s=re.sub(r'<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',unescape(s)).strip()

for lang,(path,target) in HUBS.items():
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists(): raise SystemExit(f'Phase 89 audit missing hub: {path}')
    html=f.read_text(encoding='utf-8')
    sections=re.findall(r'<section\b[^>]*class="[^"]*ivm-concierge-selection[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
    criteria=re.findall(r'<section\b[^>]*class="[^"]*ivm-concierge-criteria[^"]*"[^>]*>(.*?)</section>',html,re.I|re.S)
    if len(sections)!=1 or len(criteria)!=1: raise SystemExit(f'Phase 89 expected one guide + criteria section: {path}')
    cards=re.findall(r'<div\b[^>]*class="[^"]*intel-card[^"]*"[^>]*>(.*?)</div>',criteria[0],re.I|re.S)
    if len(cards)!=4: raise SystemExit(f'Phase 89 expected four decision cards: {path} -> {len(cards)}')
    text=clean(sections[0]+' '+criteria[0])
    for needle in NEEDLES[lang]:
        if needle.lower() not in text.lower(): raise SystemExit(f'Phase 89 missing decision concept {needle}: {path}')
    links=re.findall(r'href=["\']([^"\']+)["\']',sections[0],re.I)
    if links.count(target)!=1: raise SystemExit(f'Phase 89 same-language concierge link mismatch: {path} -> {links}')
    # Protect against accidental cross-language concierge routing in this new block.
    concierge_links=[u for u in links if 'concierge' in u or 'conciergerie' in u]
    if concierge_links!=[target]: raise SystemExit(f'Phase 89 cross-language concierge link found: {path}')
    if len(text.split())<120 and lang!='ar': raise SystemExit(f'Phase 89 guide too thin: {path} -> {len(text.split())} words')

# No new indexable URLs were introduced: sitemap remains the established 138-URL architecture.
sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
urls=re.findall(r'<loc>(.*?)</loc>',sitemap,re.I|re.S)
if len(urls)!=138 or len(set(urls))!=138: raise SystemExit(f'Phase 89 sitemap architecture changed unexpectedly: {len(urls)}')
print('PASS: Phase 89 audit — five multilingual Black Book hubs contain localized concierge-selection guidance, four decision criteria and same-language commercial pathways; sitemap remains 138 URLs')
