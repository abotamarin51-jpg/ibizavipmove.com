"""Read-only gate for the Phase 141 user-supplied Services-hub vocabulary bridge."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from phase142_audit import run as run_localized_home_mobile_hero_audit
from phase146_audit import run as run_localized_home_service_links_audit
from phase153_audit import run as run_french_bespoke_path_audit
from phase154_audit import run as run_localized_yacht_path_audit

ROOT = Path('_site')
PAGES = {
    'services': ['Luxury travel planning','Bespoke travel','Custom travel','Itinerary planning','Destination services','On-the-ground support','Travel coordination','Luxury travel services'],
    'fr/services': ['Organisation de voyages de luxe','Voyages sur mesure','Création d’itinéraires','Services à destination','Assistance sur place','Coordination de voyages','Services de voyage haut de gamme'],
    'de/services': ['Luxusreiseplanung','Maßgeschneiderte Reisen','Massgeschneiderte Reisen','Individuelle Reiseplanung','Services am Urlaubsort','Betreuung vor Ort','Reisekoordination','Luxusreiseservice'],
    'ar/services': ['تخطيط السفر الفاخر','رحلات مصممة حسب الطلب','تخطيط برامج الرحلات','خدمات الوجهة السياحية','مساعدة أثناء الإقامة','تنسيق السفر','خدمات السفر الفاخر'],
    'es/servicios': ['Planificación de viajes de lujo','Viajes a medida','Planificación de itinerarios','Servicios en destino','Asistencia durante la estancia','Coordinación de viajes','Servicios de viajes de lujo'],
}

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 141 audit: ' + msg)


def run():
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'canonical inventory changed')
    for slug, terms in PAGES.items():
        path=ROOT/slug/'index.html'
        require(path.is_file(),f'missing target {slug}')
        html=path.read_text(encoding='utf-8')
        tags=Tags(html).tags
        require(html.count('ivm-phase141-vocabulary')==1,f'one bridge {slug}')
        for term in terms:
            require(term in html,f'missing supplied phrase {term!r} in {slug}')
        require(sum(t=='h1' for t,a in tags)==1,f'one H1 {slug}')
        url='https://ibizavipmove.com/'+slug+'/'
        require([a.get('href') for t,a in tags if t=='link' and a.get('rel')=='canonical']==[url],f'self canonical {slug}')
        require(url in urls,f'canonical remains in sitemap {slug}')
        require(not any(t=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower() for t,a in tags),f'indexability {slug}')
        require({a.get('hreflang') for t,a in tags if t=='link' and a.get('rel')=='alternate'}=={'en','es','fr','de','ar','x-default'},f'language cluster {slug}')
        if slug == 'ar/services':
            html_tag = next((a for t,a in tags if t=='html'), {})
            require(html_tag.get('dir')=='rtl', 'Arabic RTL preserved')
    run_localized_home_mobile_hero_audit()
    run_localized_home_service_links_audit()
    run_french_bespoke_path_audit()
    run_localized_yacht_path_audit()
    print('PASS: Phase 141 audit — selected supplied travel-planning vocabulary visible on five existing Services hubs; canonicals/hreflang/indexability and 156-URL sitemap preserved')


if __name__ == '__main__':
    run()
