from pathlib import Path
import re

ROOT=Path('_site')
SOURCE=Path('quintessentially-type.css')
ASSET=ROOT/'assets'/'quintessentially-type.css'
ASSET.parent.mkdir(parents=True,exist_ok=True)
ASSET.write_text(SOURCE.read_text(encoding='utf-8'),encoding='utf-8')

LINK='<link rel="stylesheet" href="/assets/quintessentially-type.css?v=27">'
count=0
for p in ROOT.rglob('*.html'):
    text=p.read_text(encoding='utf-8')
    if '<head' not in text.lower():
        continue
    text=re.sub(r'<link\s+rel="stylesheet"\s+href="/assets/quintessentially-type\.css[^>]*>','',text,flags=re.I)
    # Load last so typography scale consistently overrides every earlier visual layer.
    text=re.sub(r'</head>',LINK+'</head>',text,count=1,flags=re.I)
    p.write_text(text,encoding='utf-8')
    count+=1

home=(ROOT/'index.html').read_text(encoding='utf-8')
assert LINK in home
assert 'quintessentially-type.css?v=27' in home
assert ASSET.exists()
css=ASSET.read_text(encoding='utf-8')
assert '--ivm-display:"Cormorant Garamond"' in css
assert '--ivm-ui:"Helvetica Neue"' in css
assert 'font-size:clamp(56px,6.2vw,86px)' in css
assert 'font-size:clamp(47px,13.5vw,58px)' in css
assert count >= 43, f'Expected typography on at least 43 HTML pages, got {count}'
print(f'PASS: Phase 27 Quintessentially-inspired typography linked into {count} HTML pages')
