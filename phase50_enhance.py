from pathlib import Path
import re

ROOT=Path('_site')
WA='https://wa.me/34600703303'

NAV={
'es':{
 'services':('/es/servicios/','Servicios'),'concierge':('/es/concierge-privado-ibiza/','Concierge'),'chauffeur':('/es/chauffeur-privado-ibiza/','Chófer'),'office':('/private-office/','Private Office'),'contact':('/es/contacto/','Contacto'),'cta':'WhatsApp 24/7','menu':'Menú'},
'fr':{
 'services':('/fr/services/','Services'),'concierge':('/fr/conciergerie-privee-ibiza/','Conciergerie'),'chauffeur':('/fr/chauffeur-prive-ibiza/','Chauffeur'),'office':('/private-office/','Private Office'),'contact':('/fr/contact/','Contact'),'cta':'WhatsApp 24/7','menu':'Menu'},
'de':{
 'services':('/de/services/','Services'),'concierge':('/de/privater-concierge-ibiza/','Concierge'),'chauffeur':('/de/privater-chauffeur-ibiza/','Chauffeur'),'office':('/private-office/','Private Office'),'contact':('/de/kontakt/','Kontakt'),'cta':'WhatsApp 24/7','menu':'Menü'},
'ar':{
 'services':('/ar/services/','الخدمات'),'concierge':('/ar/private-concierge-ibiza/','الكونسيرج'),'chauffeur':('/ar/private-chauffeur-ibiza/','السائق الخاص'),'office':('/private-office/','Private Office'),'contact':('/ar/contact/','التواصل'),'cta':'واتساب 24/7','menu':'القائمة'}
}


def nav_links(d):
    return ''.join([
      f'<a href="{d["services"][0]}">{d["services"][1]}</a>',
      f'<a href="{d["concierge"][0]}">{d["concierge"][1]}</a>',
      f'<a href="{d["chauffeur"][0]}">{d["chauffeur"][1]}</a>',
      f'<a href="{d["office"][0]}">{d["office"][1]}</a>',
      f'<a href="{d["contact"][0]}">{d["contact"][1]}</a>',
      f'<a class="nav-cta" href="{WA}">{d["cta"]}</a>'
    ])

def mobile_links(d):
    return ''.join([
      f'<a href="{d["services"][0]}">{d["services"][1]}</a>',
      f'<a href="{d["concierge"][0]}">{d["concierge"][1]}</a>',
      f'<a href="{d["chauffeur"][0]}">{d["chauffeur"][1]}</a>',
      f'<a href="{d["office"][0]}">{d["office"][1]}</a>',
      f'<a href="{d["contact"][0]}">{d["contact"][1]}</a>',
      f'<a href="{WA}">{d["cta"]}</a>'
    ])

updated={k:0 for k in NAV}
headers={k:0 for k in NAV}
for file in ROOT.rglob('*.html'):
    html=file.read_text(encoding='utf-8')
    lm=re.search(r'<html\b[^>]*\blang=["\']([a-zA-Z-]+)["\']',html,re.I)
    if not lm:continue
    lang=lm.group(1).lower().split('-')[0]
    if lang not in NAV:continue
    d=NAV[lang]

    # Replace the first primary nav while preserving any legacy attributes/classes.
    if re.search(r'<header\b[^>]*class=["\'][^"\']*site-header[^"\']*["\']',html,re.I):
        nav=re.search(r'<nav\b([^>]*)>.*?</nav>',html,re.I|re.S)
        if not nav:raise SystemExit(f'Primary nav not found: {file}')
        replacement=f'<nav{nav.group(1)}>{nav_links(d)}</nav>'
        html=html[:nav.start()]+replacement+html[nav.end():]
        headers[lang]+=1

    # Preserve mobile-menu attributes such as id and accessibility hooks.
    mm=re.search(r'<div\b([^>]*class=["\'][^"\']*mobile-menu[^"\']*["\'][^>]*)>.*?</div>',html,re.I|re.S)
    if mm:
        replacement=f'<div{mm.group(1)}>{mobile_links(d)}</div>'
        html=html[:mm.start()]+replacement+html[mm.end():]

    # Keep the existing accessible button attributes and localize only its label.
    html=re.sub(r'(<button\b[^>]*class=["\'][^"\']*menu-btn[^"\']*["\'][^>]*>)(.*?)(</button>)',lambda m:m.group(1)+d['menu']+m.group(3),html,count=1,flags=re.I|re.S)
    file.write_text(html,encoding='utf-8');updated[lang]+=1

# Validate all localized headers independent of nav attributes or quote style.
for lang,d in NAV.items():
    assert updated[lang]>0,lang
    assert headers[lang]>0,(lang,'no site headers')
    for file in ROOT.rglob('*.html'):
        html=file.read_text(encoding='utf-8')
        lm=re.search(r'<html\b[^>]*\blang=["\']([a-zA-Z-]+)["\']',html,re.I)
        if not lm or lm.group(1).lower().split('-')[0]!=lang:continue
        if not re.search(r'<header\b[^>]*class=["\'][^"\']*site-header[^"\']*["\']',html,re.I):continue
        nav=re.search(r'<nav\b[^>]*>(.*?)</nav>',html,re.I|re.S)
        assert nav,(lang,file)
        n=nav.group(1)
        assert d['services'][0] in n,(lang,file,'services')
        assert d['contact'][0] in n,(lang,file,'contact')
        assert d['concierge'][0] in n,(lang,file,'concierge')
        assert d['chauffeur'][0] in n,(lang,file,'chauffeur')
print('PASS: Phase 50 localized primary navigation aligned across ES/FR/DE/AR — '+', '.join(f'{k}:{v}' for k,v in updated.items()))
