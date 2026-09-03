from pathlib import Path
import shutil

ROOT=Path('_site'); SRC=Path('phase72.css'); HREF='/assets/phase72.css?v=72'
if not SRC.exists(): raise SystemExit('phase72.css missing')
dst=ROOT/'assets'/'phase72.css'; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(SRC,dst)
paths=['/media-partners/','/es/media-partners/','/fr/media-partners/','/de/media-partners/','/ar/media-partners/']
for path in paths:
    p=ROOT/path.strip('/')/'index.html'
    if not p.exists(): raise SystemExit(f'media page missing: {path}')
    t=p.read_text(encoding='utf-8')
    if HREF not in t: t=t.replace('</head>',f'<link rel="stylesheet" href="{HREF}"></head>',1)
    p.write_text(t,encoding='utf-8')
for path in paths:
    t=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    assert HREF in t and 'ivm-media-links' in t,path
print('PASS: Phase 72 Media & Partners styling linked across five-language cluster')