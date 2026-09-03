from pathlib import Path
import re

ROOT=Path('_site')
STYLE='/assets/phase42.css?v=42'
CSS_SRC=Path('phase42.css')
CSS_DEST=ROOT/'assets'/'phase42.css'

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'),encoding='utf-8')

LABELS={
'en':('EN','English'),
'es':('ES','Español'),
'fr':('FR','Français'),
'de':('DE','Deutsch'),
'ar':('AR','العربية'),
}
ORDER=('en','es','fr','de','ar')
ALT_RE=re.compile(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',re.I)
CANON_RE=re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"',re.I)

count=0
for page in ROOT.rglob('*.html'):
    html=page.read_text(encoding='utf-8')
    if '<footer' not in html or re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex',html,re.I):
        continue
    alts={lang.lower():href for lang,href in ALT_RE.findall(html) if lang.lower() in LABELS}
    if len(alts)<2:
        continue
    canonical_m=CANON_RE.search(html)
    canonical=canonical_m.group(1).rstrip('/')+'/' if canonical_m else ''
    links=[]
    for lang in ORDER:
        href=alts.get(lang)
        if not href:
            continue
        short,name=LABELS[lang]
        current=' aria-current="page"' if href.rstrip('/')+'/'==canonical else ''
        direction=' dir="rtl"' if lang=='ar' else ''
        links.append(f'<a href="{href}" hreflang="{lang}" lang="{lang}"{direction}{current}><b>{short}</b><small>{name}</small></a>')
    bar='<aside class="ivm-language-bar" aria-label="Language versions"><div class="ivm-language-inner"><div class="ivm-language-label">International editions</div><nav class="ivm-language-links" aria-label="Choose language">'+''.join(links)+'</nav></div></aside>'
    if 'class="ivm-language-bar"' not in html:
        html=html.replace('<footer',bar+'<footer',1)
    if STYLE not in html:
        html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
    page.write_text(html,encoding='utf-8')
    count+=1

# Validation: core five-language clusters must expose all five choices.
clusters=[
'/luxury-villas-ibiza/','/es/villas-lujo-ibiza/','/fr/villas-luxe-ibiza/','/de/luxusvillen-ibiza/','/ar/luxury-villas-ibiza/',
'/yacht-charter-ibiza/','/es/yate-privado-ibiza/','/fr/location-yacht-ibiza/','/de/yachtcharter-ibiza/','/ar/yacht-charter-ibiza/',
'/private-aviation-ibiza/','/es/aviacion-privada-ibiza/','/fr/aviation-privee-ibiza/','/de/private-aviation-ibiza/','/ar/private-aviation-ibiza/',
'/private-security-ibiza/','/es/seguridad-privada-ibiza/','/fr/securite-privee-ibiza/','/de/private-sicherheit-ibiza/','/ar/private-security-ibiza/'
]
for rel in clusters:
    p=ROOT/rel.strip('/')/'index.html'
    html=p.read_text(encoding='utf-8')
    assert STYLE in html,rel
    assert html.count('class="ivm-language-bar"')==1,rel
    for lang in ORDER:
        assert f'hreflang="{lang}"' in html,(rel,lang)
    assert 'aria-current="page"' in html,rel
assert CSS_DEST.exists() and CSS_DEST.stat().st_size>1500
assert count>=20,f'Unexpectedly few pages with language navigation: {count}'
print(f'PASS: Phase 42 premium language navigation added to {count} multilingual pages')
