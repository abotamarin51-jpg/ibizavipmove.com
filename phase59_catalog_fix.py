from pathlib import Path
import json
import re

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG=BASE+'/#organization'
EN=BASE+'/restaurants-nightlife-ibiza/'
LOCAL={
 'es':('/es/servicios/',BASE+'/es/restaurantes-nightlife-ibiza/'),
 'fr':('/fr/services/',BASE+'/fr/restaurants-nightlife-ibiza/'),
 'de':('/de/services/',BASE+'/de/restaurants-nightlife-ibiza/'),
 'ar':('/ar/services/',BASE+'/ar/restaurants-nightlife-ibiza/'),
}
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)

for lang,(hub,local_url) in LOCAL.items():
    file=ROOT/hub.strip('/')/'index.html'
    html=file.read_text(encoding='utf-8')
    state={'org':False,'collection':False}
    def repl(m):
        try:o=json.loads(m.group(1))
        except Exception:return m.group(0)
        if not isinstance(o,dict):return m.group(0)
        if o.get('@id')==ORG:
            catalog=o.get('hasOfferCatalog')
            if isinstance(catalog,dict):
                for offer in catalog.get('itemListElement',[]):
                    if not isinstance(offer,dict):continue
                    service=offer.get('itemOffered')
                    if not isinstance(service,dict):continue
                    name=(service.get('name') or '').lower()
                    url=service.get('url')
                    if 'nightlife' in name or url in (EN,local_url):service['url']=EN
                state['org']=True
        if o.get('@type')=='CollectionPage':
            main=o.get('mainEntity')
            if isinstance(main,dict) and main.get('@type')=='ItemList':
                for item in main.get('itemListElement',[]):
                    if not isinstance(item,dict):continue
                    name=(item.get('name') or '').lower()
                    url=item.get('url')
                    if 'nightlife' in name or url in (EN,local_url):item['url']=local_url
                state['collection']=True
        return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
    html=SCRIPT_RE.sub(repl,html)
    file.write_text(html,encoding='utf-8')
    assert state['org'],(lang,'organization catalog')
    assert state['collection'],(lang,'collection')

for lang,(hub,local_url) in LOCAL.items():
    html=(ROOT/hub.strip('/')/'index.html').read_text(encoding='utf-8')
    assert f'href="{local_url.replace(BASE,"")}"' in html,(lang,'visible Access link')
    org=None;collection=None
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if not isinstance(o,dict):continue
        if o.get('@id')==ORG:org=o
        if o.get('@type')=='CollectionPage':collection=o
    assert org and collection,lang
    offers=org['hasOfferCatalog']['itemListElement']
    offer_urls={x.get('itemOffered',{}).get('url') for x in offers if isinstance(x,dict)}
    assert EN in offer_urls and local_url not in offer_urls,(lang,'canonical OfferCatalog')
    items=collection['mainEntity']['itemListElement']
    item_urls={x.get('url') for x in items if isinstance(x,dict)}
    assert local_url in item_urls and EN not in item_urls,(lang,'localized ItemList')
print('PASS: Phase 59 localized Access navigation kept separate from canonical organization OfferCatalog')
