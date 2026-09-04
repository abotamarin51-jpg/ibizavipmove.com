from pathlib import Path
from html import escape
import json,re

ROOT=Path('_site'); BASE='https://ibizavipmove.com'
ARTICLE_URL='https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/'
ARTICLE_TITLE='Top Luxury Travel Concierge Services for Ibiza Dining'
SCRIPT_RE=re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',re.I|re.S)
DATA={
'en':('/media-partners/','External editorial reference','Luxury Magazine referenced Ibiza VIP Move in a 2026 editorial comparison of Ibiza dining concierge services, discussing our coordination-led approach when restaurant plans depend on transport, villas, yachts, staff and changing schedules.','Read the external article →'),
'es':('/es/media-partners/','Referencia editorial externa','Luxury Magazine mencionó a Ibiza VIP Move en una comparativa editorial de 2026 sobre servicios de concierge para dining en Ibiza, destacando nuestro enfoque de coordinación cuando los planes dependen de transporte, villas, yates, staff y cambios de horario.','Leer el artículo externo →'),
'fr':('/fr/media-partners/','Référence éditoriale externe','Luxury Magazine a cité Ibiza VIP Move dans une comparaison éditoriale 2026 des services de conciergerie dining à Ibiza, en décrivant notre approche de coordination lorsque restaurants, transport, villas, yachts, staff et changements d’horaires sont liés.','Lire l’article externe →'),
'de':('/de/media-partners/','Externe redaktionelle Referenz','Luxury Magazine erwähnte Ibiza VIP Move in einem redaktionellen Vergleich 2026 zu Dining-Concierge-Services auf Ibiza und beschrieb unseren koordinationsorientierten Ansatz, wenn Restaurants, Transport, Villen, Yachten, Staff und Zeitänderungen zusammenhängen.','Externen Artikel lesen →'),
'ar':('/ar/media-partners/','مرجع تحريري خارجي','ذكرت Luxury Magazine شركة Ibiza VIP Move في مقارنة تحريرية لعام 2026 حول خدمات كونسيرج المطاعم في إيبيزا، مع وصف نهجنا القائم على التنسيق عندما ترتبط المطاعم بالنقل والفلل واليخوت والطاقم وتغييرات المواعيد.','قراءة المقال الخارجي ←')}

def fpath(path):return ROOT/path.strip('/')/'index.html'
def block(head,copy,cta):
    return f'<section class="editorial ivm-external-reference"><div><div class="kicker dark">Media reference</div><h2>{escape(head)}</h2></div><div><p class="large">{escape(copy)}</p><p><a href="{ARTICLE_URL}" rel="external noopener" target="_blank">{escape(cta)}</a></p><p class="ivm-source-note">External source: Luxury Magazine. Reference is listed for verification; it does not imply endorsement or partnership.</p></div></section>'

def patch_schema(html,canonical):
    def repl(m):
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        nodes=o.get('@graph',[]) if isinstance(o,dict) and isinstance(o.get('@graph'),list) else [o]
        changed=False
        for node in nodes:
            if not isinstance(node,dict) or node.get('url')!=canonical: continue
            typ=node.get('@type'); types=typ if isinstance(typ,list) else [typ]
            if 'WebPage' in types or 'AboutPage' in types:
                node['citation']={'@type':'Article','name':ARTICLE_TITLE,'url':ARTICLE_URL}
                changed=True
        if not changed:return m.group(0)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    return SCRIPT_RE.sub(repl,html)

for lang,(path,head,copy,cta) in DATA.items():
    f=fpath(path)
    if not f.exists(): raise SystemExit(f'Phase 92 missing Media & Partners page: {path}')
    html=f.read_text(encoding='utf-8')
    if 'ivm-external-reference' in html: raise SystemExit(f'Phase 92 duplicate external reference: {path}')
    marker='<section class="ivm-media-cta"'
    if marker not in html:
        marker='<section class="closing'
    pos=html.find(marker)
    if pos<0: raise SystemExit(f'Phase 92 insertion marker missing: {path}')
    html=html[:pos]+block(head,copy,cta)+html[pos:]
    html=patch_schema(html,BASE+path)
    f.write_text(html,encoding='utf-8')
print('PASS: Phase 92 external editorial reference — five Media & Partners pages cite one verified 2026 Luxury Magazine article without implying endorsement or partnership')
