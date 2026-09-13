"""Read-only gate for the reviewed A1-A8 vocabulary application."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
MARKER = 'ivm-phase140-audience-vocabulary'
EXPECTED = {
    '/private-office/': ['Family Assistant','Household Manager','Estate Manager','Director of Residences'],
    '/partners/': ['Lifestyle Coordinator','VIP Host','Artist Liaison','Tour Manager'],
    '/fr/private-office/': ['Assistant personnel de famille','Intendant de maison','Intendant de propriétés privées','Directeur de résidences privées'],
    '/fr/partners/': ['Coordinateur de voyages et de services lifestyle','Hôte VIP','Chargé de l’accueil des artistes','Responsable de tournée'],
    '/de/private-office/': ['Private Familienassistenz','Hausmanager für Privathaushalte','Verwalter privater Anwesen','Leiter privater Residenzen'],
    '/de/partners/': ['Koordinator für Reise- und Lifestyle-Services','VIP-Gästebetreuer','Künstlerbetreuer','Tourmanager für Musikproduktionen'],
    '/ar/private-office/': ['مساعد شخصي للعائلة','مدير شؤون المنزل','مدير الأملاك السكنية الخاصة','مدير المساكن الخاصة'],
    '/ar/partners/': ['منسق خدمات السفر ونمط الحياة','مضيف كبار الشخصيات','منسق شؤون الفنانين','مدير الجولات الفنية'],
    '/es/private-office/': ['Asistente personal de familias','Administrador del hogar','Gestor de propiedades residenciales privadas','Director de residencias privadas'],
    '/es/partners/': ['Coordinador de viajes y servicios lifestyle','Anfitrión VIP','Coordinador de atención a artistas','Mánager de giras musicales'],
}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))


def require(ok,msg):
    if not ok:
        raise SystemExit('Phase 140 audit: ' + msg)


def run():
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'sitemap inventory')
    seen=[]
    for path,roles in EXPECTED.items():
        file=ROOT/path.strip('/')/'index.html'
        require(file.is_file(),f'missing target {path}')
        html=file.read_text(encoding='utf-8')
        parsed=Page(html)
        require(html.count(MARKER)==1,f'one vocabulary section {path}')
        start=html.find('<section class="ivm-b2b-overview '+MARKER)
        end=html.find('</section>',start)
        require(start>=0 and end>start,f'section bounds {path}')
        section=html[start:end]
        for role in roles:
            require(section.count(role)>=1,f'missing role {role} on {path}')
            require(html.count(role)>=1,f'role not visible {role} on {path}')
            seen.append(role)
        require(sum(1 for t,a in parsed.tags if t=='h1')==1,f'one H1 {path}')
        canonical='https://ibizavipmove.com'+path
        require(canonical in urls,f'sitemap canonical {path}')
        require([a.get('href') for t,a in parsed.tags if t=='link' and a.get('rel')=='canonical']==[canonical],f'self canonical {path}')
        require({a.get('hreflang') for t,a in parsed.tags if t=='link' and a.get('rel')=='alternate'}=={'en','es','fr','de','ar','x-default'},f'hreflang cluster {path}')
        require(not any(t=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower() for t,a in parsed.tags),f'indexability {path}')
    require(len(seen)==40 and len(set(seen))==40,'40 distinct localized A1-A8 labels')
    ar=(ROOT/'ar/partners/index.html').read_text(encoding='utf-8')
    require('<html lang="ar" dir="rtl">' in ar or '<html dir="rtl" lang="ar">' in ar,'Arabic RTL preserved')
    print('PASS: Phase 140 audit — 40 reviewed A1-A8 localized role labels visible on 10 existing Partners/Private Office pages; 156 canonicals, H1/canonical/hreflang/indexability and Arabic RTL preserved')

if __name__=='__main__':
    run()
