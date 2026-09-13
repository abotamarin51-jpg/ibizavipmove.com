"""Read-only regression gate for Phase 134 destination-management differentiation."""
from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path('_site')
PAGE = ROOT / 'destination-management-ibiza' / 'index.html'
URL = 'https://ibizavipmove.com/destination-management-ibiza/'
DATE = '2026-09-13'
EXPECTED_H1 = 'Luxury destination management in Ibiza, behind the client itinerary.'
TOKENS = (
    'Professional handover brief',
    'What your Ibiza operator needs before execution.',
    'Client relationship',
    'Arrival & accommodation',
    'Local dependencies',
    'Communication route',
    'work behind the originating partner',
    'approval boundaries',
)

class Doc(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.h1=[]; self._h1=False; self._buf=[]; self.scripts=[]; self._script=None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if tag=='h1': self._h1=True; self._buf=[]
        elif tag=='br' and self._h1: self._buf.append(' ')
        if tag=='script': self._script=[a,'']
    def handle_data(self, data):
        if self._h1: self._buf.append(data)
        if self._script is not None: self._script[1]+=data
    def handle_endtag(self, tag):
        if tag=='h1' and self._h1:
            self.h1.append(' '.join(''.join(self._buf).split())); self._h1=False
        if tag=='script' and self._script is not None:
            self.scripts.append(self._script); self._script=None

def req(ok,msg):
    if not ok: raise SystemExit('Phase 134 audit: '+msg)

def run():
    text=PAGE.read_text(encoding='utf-8'); doc=Doc(text)
    req(doc.h1==[EXPECTED_H1], 'descriptive single H1')
    req(text.count('ivm-phase134-brief')==1, 'one handover brief')
    for t in TOKENS: req(t in text, 'missing '+t)
    canon=[a.get('href') for tag,a in doc.tags if tag=='link' and a.get('rel')=='canonical']
    req(canon==[URL], 'self canonical')
    robots=[a.get('content','').lower() for tag,a in doc.tags if tag=='meta' and a.get('name','').lower()=='robots']
    req(not any('noindex' in x for x in robots), 'page unexpectedly noindex')
    for href in ('/partners/','/luxury-travel-concierge-ibiza/','/private-client-services-ibiza/','/case-studies/multi-day-executive-chauffeur-program/','/ibiza-luxury-operations-report-2026/','/founder/'):
        req(any(tag=='a' and a.get('href')==href for tag,a in doc.tags), 'missing pathway '+href)
    objs=[]
    for attrs,code in doc.scripts:
        if attrs.get('type','').lower()=='application/ld+json':
            try: objs.append(json.loads(code))
            except Exception as e: raise SystemExit('Phase 134 audit: invalid JSON-LD: '+str(e))
    blob=json.dumps(objs,ensure_ascii=False)
    req(URL in blob and 'Luxury destination management company services in Ibiza' in blob, 'canonical service schema preserved')
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    root=ET.parse(ROOT/'sitemap.xml')
    urls=[]; lastmod=None
    for u in root.findall('s:url',ns):
        loc=u.find('s:loc',ns).text; urls.append(loc)
        if loc==URL:
            lm=u.find('s:lastmod',ns); lastmod=lm.text if lm is not None else None
    req(len(urls)==len(set(urls))==156, 'sitemap inventory')
    req(urls.count(URL)==1 and lastmod==DATE, 'destination lastmod')
    print('PASS: Phase 134 audit — destination-management page is distinct, canonical/indexable, B2B pathways/schema preserved, sitemap remains 156 URLs')

if __name__=='__main__': run()
