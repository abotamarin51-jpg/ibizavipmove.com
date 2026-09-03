from pathlib import Path

ROOT = Path('_site')
STYLE = '/assets/phase52.css?v=52'

ROUTES = {
    'en': {'hub':'/services/','office':'/private-office/','partners':'/partners/'},
    'es': {'hub':'/es/servicios/','office':'/es/private-office/','partners':'/es/partners/'},
    'fr': {'hub':'/fr/services/','office':'/fr/private-office/','partners':'/fr/partners/'},
    'de': {'hub':'/de/services/','office':'/de/private-office/','partners':'/de/partners/'},
    'ar': {'hub':'/ar/services/','office':'/ar/private-office/','partners':'/ar/partners/'},
}

COPY = {
'en': {
 'eyebrow':'Travel Trade & Private Offices','title':'Professional Ibiza support, connected.','intro':'For assistants, family offices, luxury travel advisors, concierge companies and hospitality teams that need a dependable Ibiza operator behind the client itinerary.',
 'office':('Private Office','For principals, PAs & family offices','Explore high-touch local coordination.'),
 'partners':('B2B Partners','For travel & concierge partners','Explore the professional partner workflow.'),
 'services':('Private Services','For active client requirements','Explore the complete Ibiza service architecture.')},
'es': {
 'eyebrow':'Travel Trade & Private Offices','title':'Soporte profesional en Ibiza, conectado.','intro':'Para assistants, family offices, luxury travel advisors, empresas de concierge y hospitality teams que necesitan un operador fiable en Ibiza detrás del itinerario del cliente.',
 'office':('Private Office','Para principals, PAs y family offices','Explora coordinación local de alto nivel.'),
 'partners':('Partners B2B','Para travel y concierge partners','Explora el workflow profesional para partners.'),
 'services':('Servicios privados','Para necesidades activas del cliente','Explora toda la arquitectura de servicios en Ibiza.')},
'fr': {
 'eyebrow':'Travel Trade & Private Offices','title':'Un support professionnel Ibiza, connecté.','intro':'Pour assistants, family offices, luxury travel advisors, sociétés de conciergerie et équipes hospitality qui ont besoin d’un opérateur Ibiza fiable derrière l’itinéraire client.',
 'office':('Private Office','Pour principals, PAs & family offices','Découvrir la coordination locale high-touch.'),
 'partners':('Partenaires B2B','Pour travel & concierge partners','Découvrir le workflow professionnel partenaire.'),
 'services':('Services privés','Pour les besoins actifs du client','Découvrir l’architecture complète des services Ibiza.')},
'de': {
 'eyebrow':'Travel Trade & Private Offices','title':'Professioneller Ibiza-Support, verbunden.','intro':'Für Assistants, Family Offices, Luxury Travel Advisors, Concierge-Unternehmen und Hospitality-Teams, die hinter der Kundenroute einen verlässlichen Ibiza-Operator benötigen.',
 'office':('Private Office','Für Principals, PAs & Family Offices','High-Touch-Koordination vor Ort entdecken.'),
 'partners':('B2B Partners','Für Travel- & Concierge-Partner','Professionellen Partner-Workflow entdecken.'),
 'services':('Private Services','Für aktive Kundenanforderungen','Die komplette Ibiza-Servicearchitektur entdecken.')},
'ar': {
 'eyebrow':'Travel Trade & Private Offices','title':'دعم احترافي في إيبيزا، ضمن منظومة واحدة.','intro':'للمساعدين وFamily Offices ومستشاري السفر الفاخر وشركات الكونسيرج وفرق الضيافة التي تحتاج إلى مشغل موثوق في إيبيزا خلف برنامج العميل.',
 'office':('Private Office','للضيوف الرئيسيين والمساعدين وFamily Offices','اكتشف التنسيق المحلي عالي المستوى.'),
 'partners':('شركاء B2B','لشركاء السفر والكونسيرج','اكتشف آلية العمل المهنية للشركاء.'),
 'services':('الخدمات الخاصة','لمتطلبات العميل الحالية','اكتشف منظومة خدمات إيبيزا الكاملة.')},
}

css = Path('phase52.css')
if not css.exists():
    raise SystemExit('phase52.css missing')
asset = ROOT / 'assets' / 'phase52.css'
asset.write_text(css.read_text(encoding='utf-8'), encoding='utf-8')


def card(href, data):
    label, title, copy = data
    return f'<a class="ivm-trade-bridge-link" href="{href}"><span>{label}</span><strong>{title}</strong><small>{copy}</small></a>'


def bridge(lang, context):
    c = COPY[lang]
    r = ROUTES[lang]
    if context == 'hub':
        links = card(r['office'], c['office']) + card(r['partners'], c['partners'])
    else:
        links = card(r['partners'], c['partners']) + card(r['hub'], c['services'])
    return f'''<section class="ivm-trade-bridge" aria-label="Professional Ibiza support"><div class="ivm-trade-bridge-inner"><div><div class="eyebrow">{c['eyebrow']}</div><h2>{c['title']}</h2></div><div class="ivm-trade-bridge-copy"><p>{c['intro']}</p><div class="ivm-trade-bridge-links">{links}</div></div></div></section>'''

updated = 0
for lang, routes in ROUTES.items():
    for context, path in [('hub', routes['hub']), ('office', routes['office'])]:
        file = ROOT / path.strip('/') / 'index.html'
        if not file.exists():
            raise SystemExit(f'Phase 52 target missing: {path}')
        html = file.read_text(encoding='utf-8')
        if STYLE not in html:
            html = html.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
        if 'class="ivm-trade-bridge"' not in html:
            html = html.replace('</main>', bridge(lang, context) + '</main>', 1)
        file.write_text(html, encoding='utf-8')
        updated += 1

for lang, routes in ROUTES.items():
    for context, path in [('hub', routes['hub']), ('office', routes['office'])]:
        html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
        assert html.count('class="ivm-trade-bridge"') == 1, path
        assert STYLE in html, path
        assert routes['partners'] in html, (path, 'partners')
        if context == 'hub':
            assert routes['office'] in html, (path, 'office')
        else:
            assert routes['hub'] in html, (path, 'services')
        assert html.count('<h1') == 1, path

assert asset.exists() and asset.stat().st_size > 1000
print(f'PASS: Phase 52 B2B bridge connected {updated} international Services/Private Office pages')
