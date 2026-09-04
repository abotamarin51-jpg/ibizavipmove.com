from pathlib import Path
from html import unescape
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
PAGES={
    '/':('Luxury Concierge Ibiza | Ibiza VIP Move','Luxury concierge in Ibiza'),
    '/private-concierge-ibiza/':('Private Concierge Ibiza | Ibiza VIP Move','Private concierge in Ibiza'),
}
SCRIPT_RE=re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',re.I|re.S)


def file_for(path):return ROOT/'index.html' if path=='/' else ROOT/path.strip('/')/'index.html'
def clean(v):return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>',' ',v or ''))).strip()
def one(pattern,html,label,path):
    ms=re.findall(pattern,html,re.I|re.S)
    if len(ms)!=1:raise SystemExit(f'Phase 85 expected one {label}: {path} -> {len(ms)}')
    return clean(ms[0])

def meta(html,attr,name,path):
    patt=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(name)}["\'])(?=[^>]*\bcontent=["\']([^"\']+)["\'])[^>]*>'
    return one(patt,html,f'{attr}={name}',path)

for path,(expected_title,h1_phrase) in PAGES.items():
    f=file_for(path)
    if not f.exists():raise SystemExit(f'Phase 85 missing page: {path}')
    html=f.read_text(encoding='utf-8')
    title=one(r'<title>(.*?)</title>',html,'title',path)
    desc=meta(html,'name','description',path)
    h1=one(r'<h1\b[^>]*>(.*?)</h1>',html,'h1',path)
    if title!=expected_title:raise SystemExit(f'Phase 85 title mismatch: {path} -> {title}')
    if h1_phrase.lower() not in h1.lower():raise SystemExit(f'Phase 85 H1 intent mismatch: {path} -> {h1}')
    if 'concierge' not in desc.lower() or 'ibiza' not in desc.lower():raise SystemExit(f'Phase 85 weak description: {path}')
    if meta(html,'property','og:title',path)!=title or meta(html,'name','twitter:title',path)!=title:
        raise SystemExit(f'Phase 85 social title mismatch: {path}')
    if meta(html,'property','og:description',path)!=desc or meta(html,'name','twitter:description',path)!=desc:
        raise SystemExit(f'Phase 85 social description mismatch: {path}')
    canonical=BASE+path
    webpage=[]
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        candidates=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else ([o] if isinstance(o,dict) else [])
        for node in candidates:
            if isinstance(node,dict) and node.get('@type')=='WebPage' and node.get('url')==canonical:
                webpage.append(node)
    if len(webpage)!=1:raise SystemExit(f'Phase 85 expected one WebPage node: {path} -> {len(webpage)}')
    if webpage[0].get('name')!=title or webpage[0].get('description')!=desc:
        raise SystemExit(f'Phase 85 WebPage metadata mismatch: {path}')

c=file_for('/private-concierge-ibiza/').read_text(encoding='utf-8')
required=(
    'Luxury concierge Ibiza','Ibiza Town & Marina Botafoch','Sant Josep & the south',
    'Santa Eulària & the east','Sant Antoni & the west',
    '/private-chauffeur-ibiza/','/luxury-villas-ibiza/','/yacht-charter-ibiza/',
    '/private-aviation-ibiza/','/restaurants-nightlife-ibiza/','/private-security-ibiza/'
)
for token in required:
    if token not in c:raise SystemExit(f'Phase 85 missing local/search-intent token: {token}')
main=re.search(r'<main\b[^>]*>(.*?)</main>',c,re.I|re.S)
if not main:raise SystemExit('Phase 85 private concierge main missing')
words=clean(main.group(1)).split()
if len(words)<600:raise SystemExit(f'Phase 85 private concierge content still too thin: {len(words)} words')
for banned in ('#1 concierge','best concierge in ibiza','guaranteed access'):
    if banned in clean(main.group(1)).lower():raise SystemExit(f'Phase 85 prohibited promotional claim: {banned}')

print(f'PASS: Phase 85 audit — head-term HOME + private-concierge intent separated; local Ibiza content and six core service pathways verified ({len(words)} words on concierge landing)')
