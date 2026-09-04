from pathlib import Path
from html import unescape
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'
PAGES={
'en':('/private-office/','Ibiza Concierge for Family Offices & Personal Assistants | Ibiza VIP Move','family offices and personal assistants'),
'es':('/es/private-office/','Concierge Ibiza para Family Offices y Personal Assistants | Ibiza VIP Move','family offices y personal assistants'),
'fr':('/fr/private-office/','Conciergerie Ibiza pour Family Offices & Personal Assistants | Ibiza VIP Move','family offices et personal assistants'),
'de':('/de/private-office/','Ibiza Concierge für Family Offices & Personal Assistants | Ibiza VIP Move','family offices und personal assistants'),
'ar':('/ar/private-office/','كونسيرج إيبيزا للمكاتب العائلية والمساعدين الشخصيين | Ibiza VIP Move','المكاتب العائلية والمساعدين الشخصيين')}
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)

def clean(s):
    s=re.sub(r'<script\b.*?</script>|<style\b.*?</style>',' ',s,flags=re.I|re.S)
    s=re.sub(r'<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',unescape(s)).strip()

for lang,(path,title,needle) in PAGES.items():
    f=ROOT/path.strip('/')/'index.html'
    if not f.exists(): raise SystemExit(f'Phase 90 audit missing page: {path}')
    html=f.read_text(encoding='utf-8')
    tm=re.search(r'<title>(.*?)</title>',html,re.I|re.S)
    if not tm or clean(tm.group(1))!=title: raise SystemExit(f'Phase 90 title mismatch: {path}')
    h1s=re.findall(r'<h1\b[^>]*>(.*?)</h1>',html,re.I|re.S)
    if len(h1s)!=1 or needle.lower() not in clean(h1s[0]).lower(): raise SystemExit(f'Phase 90 H1 intent mismatch: {path}')
    if html.count('ivm-family-office-boundary')!=1: raise SystemExit(f'Phase 90 scope boundary mismatch: {path}')
    text=clean(html)
    # The page must clearly define concierge/operational support and explicitly reject formal advisory positioning.
    required=['concierge'] if lang!='ar' else ['الكونسيرج']
    for n in required:
        if n.lower() not in text.lower(): raise SystemExit(f'Phase 90 concierge scope missing: {path}')
    boundary=re.search(r'<p\b[^>]*class="ivm-family-office-boundary"[^>]*>(.*?)</p>',html,re.I|re.S)
    btext=clean(boundary.group(1)) if boundary else ''
    if lang=='en' and not all(x in btext.lower() for x in ['legal','tax','investment','wealth-management','formal family-office']): raise SystemExit('Phase 90 English scope disambiguation incomplete')
    # Metadata consistency.
    for attr,name in [('property','og:title'),('name','twitter:title')]:
        m=re.search(rf'<meta\b(?=[^>]*{attr}=["\']{re.escape(name)}["\'])(?=[^>]*content=["\']([^"\']+)["\'])[^>]*>',html,re.I)
        if not m or unescape(m.group(1))!=title: raise SystemExit(f'Phase 90 social title mismatch: {path} {name}')
    canonical=BASE+path
    relevant=[]
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        for node in nodes:
            if isinstance(node,dict) and node.get('url')==canonical:
                typ=node.get('@type'); types=typ if isinstance(typ,list) else [typ]
                if any(t in ('WebPage','AboutPage','Service') for t in types): relevant.append(node)
    if relevant and not all(node.get('description') for node in relevant): raise SystemExit(f'Phase 90 structured description missing: {path}')

sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
urls=re.findall(r'<loc>(.*?)</loc>',sitemap,re.I|re.S)
if len(urls)!=138 or len(set(urls))!=138: raise SystemExit(f'Phase 90 sitemap architecture changed: {len(urls)}')
print('PASS: Phase 90 audit — 5 Private Office pages target Family Office/PA concierge intent with explicit advisory-scope disambiguation; sitemap remains 138 URLs')
