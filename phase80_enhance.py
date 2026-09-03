from pathlib import Path
from html import unescape, escape
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
IMAGE=BASE+'/assets/images/private-office.jpg'
PATHS=(
'/media-partners/','/es/media-partners/','/fr/media-partners/','/de/media-partners/','/ar/media-partners/'
)


def file_for(path):return ROOT/path.strip('/')/'index.html'

def extract(html,pattern,label,path):
    m=re.search(pattern,html,re.I|re.S)
    if not m:raise SystemExit(f'Phase 80 missing {label}: {path}')
    return unescape(re.sub(r'<[^>]+>',' ',m.group(1))).strip()

def set_meta(html,attr,name,value):
    # Replace an existing tag regardless of whether property/name appears before
    # or after content. If missing, add one before </head>.
    patt=re.compile(rf'<meta\b(?=[^>]*\b{attr}="{re.escape(name)}")(?=[^>]*\bcontent="[^"]*")[^>]*>',re.I)
    tag=f'<meta {attr}="{name}" content="{escape(value,quote=True)}">'
    if patt.search(html):return patt.sub(tag,html,count=1)
    return html.replace('</head>',tag+'</head>',1)

for path in PATHS:
    f=file_for(path)
    if not f.exists():raise SystemExit(f'Phase 80 page missing: {path}')
    html=f.read_text(encoding='utf-8')
    canonical=extract(html,r'<link\s+rel="canonical"\s+href="([^"]+)"','canonical',path)
    expected=BASE+path
    if canonical!=expected:raise SystemExit(f'Phase 80 canonical mismatch: {path} -> {canonical}')
    title=extract(html,r'<title>(.*?)</title>','title',path)
    desc=extract(html,r'<meta\s+name="description"\s+content="([^"]+)"','description',path)
    if len(title)<20 or len(desc)<50:raise SystemExit(f'Phase 80 weak page metadata: {path}')

    html=set_meta(html,'property','og:type','website')
    html=set_meta(html,'property','og:url',canonical)
    html=set_meta(html,'property','og:title',title)
    html=set_meta(html,'property','og:description',desc)
    html=set_meta(html,'property','og:image',IMAGE)
    html=set_meta(html,'name','twitter:card','summary_large_image')
    html=set_meta(html,'name','twitter:title',title)
    html=set_meta(html,'name','twitter:description',desc)
    html=set_meta(html,'name','twitter:image',IMAGE)
    f.write_text(html,encoding='utf-8')

print('PASS: Phase 80 Media & Partners social metadata aligned across EN/ES/FR/DE/AR')
