"""Read-only Phase 140 gate for the user-supplied vocabulary integration."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
PAGES = {
    'partners': ['Luxury travel advisor','Travel designer','Destination specialist','Independent travel agent','Boutique travel agency','Luxury tour operator','Destination management company','Lifestyle Coordinator','VIP Host','Artist Liaison','Tour Manager'],
    'private-office': ['Private personal assistant','Executive assistant','Guest relations manager','Family Assistant','Household Manager','Estate Manager','Director of Residences'],
    'fr/partners': ['Conseiller en voyages de luxe','Créateur de voyages','Spécialiste de la destination','Agent de voyages indépendant','Agence de voyages à taille humaine','Tour-opérateur de luxe','Agence réceptive','Coordinateur de voyages et de services lifestyle','Hôte VIP','Chargé de l’accueil des artistes','Responsable de tournée'],
    'fr/private-office': ['Assistant personnel privé','Assistant de direction','Responsable des relations clients','Assistant personnel de famille','Intendant de maison','Intendant de propriétés privées','Directeur de résidences privées'],
    'de/partners': ['Luxusreiseberater','Reisedesigner','Destinationsspezialist','Selbstständiger Reiseberater','Boutique-Reisebüro','Luxusreiseveranstalter','Destinationsmanagement-Agentur','Koordinator für Reise- und Lifestyle-Services','VIP-Gästebetreuer','Künstlerbetreuer','Tourmanager für Musikproduktionen'],
    'de/private-office': ['Privatassistent','Assistenz der Geschäftsführung','Guest Relations Manager','Private Familienassistenz','Hausmanager für Privathaushalte','Verwalter privater Anwesen','Leiter privater Residenzen'],
    'ar/partners': ['مستشار سفر فاخر','مصمم رحلات','خبير وجهات سياحية','وكيل سفر مستقل','وكالة سفر متخصصة','منظم رحلات فاخرة','شركة إدارة الوجهات السياحية','منسق خدمات السفر ونمط الحياة','مضيف كبار الشخصيات','منسق شؤون الفنانين','مدير الجولات الفنية'],
    'ar/private-office': ['مساعد شخصي خاص','مساعد تنفيذي','مدير علاقات الضيوف','مساعد شخصي للعائلة','مدير شؤون المنزل','مدير الأملاك السكنية الخاصة','مدير المساكن الخاصة'],
    'es/partners': ['Asesor de viajes de lujo','Diseñador de viajes','Especialista en destinos','Agente de viajes independiente','Agencia boutique de viajes','Operador de viajes de lujo','Agencia receptiva','Coordinador de viajes y servicios lifestyle','Anfitrión VIP','Coordinador de atención a artistas','Mánager de giras musicales'],
    'es/private-office': ['Asistente personal privado','Asistente ejecutivo','Responsable de relaciones con huéspedes','Asistente personal de familias','Administrador del hogar','Gestor de propiedades residenciales privadas','Director de residencias privadas'],
}

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 140 audit: ' + msg)

def run():
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'canonical inventory changed')
    for slug, terms in PAGES.items():
        path=ROOT/slug/'index.html'
        require(path.is_file(),f'missing target {slug}')
        html=path.read_text(encoding='utf-8')
        tags=Tags(html).tags
        require(html.count('ivm-phase140-vocabulary')==1,f'one vocabulary block {slug}')
        for term in terms:
            require(term in html,f'missing supplied term {term!r} in {slug}')
        require(sum(t=='h1' for t,a in tags)==1,f'one H1 {slug}')
        url='https://ibizavipmove.com/'+slug+'/'
        require([a.get('href') for t,a in tags if t=='link' and a.get('rel')=='canonical']==[url],f'self canonical {slug}')
        require(url in urls,f'canonical remains in sitemap {slug}')
        require(not any(t=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower() for t,a in tags),f'indexability {slug}')
        require({a.get('hreflang') for t,a in tags if t=='link' and a.get('rel')=='alternate'}=={'en','es','fr','de','ar','x-default'},f'language cluster {slug}')
    print('PASS: Phase 140 audit — 90 supplied professional-role equivalences integrated across 10 existing B2B pages; 156 sitemap canonicals preserved')

if __name__ == '__main__':
    run()
