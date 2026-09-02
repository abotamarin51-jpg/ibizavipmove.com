from pathlib import Path
from html import escape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PHONE = '+34 600 703 303'
WA = 'https://wa.me/34600703303'
EMAIL = 'partnership@ibizavipmove.com'
CSS = '/assets/premium.css?v=8'
JS = '/assets/premium.js?v=8'
LOGO = '/assets/brand-logo.svg?v=8'

PAGES = {
    '/es/': {
        'title': 'Concierge de lujo en Ibiza | Ibiza VIP Move',
        'desc': 'Concierge privado de lujo en Ibiza para chófer, villas, yates, aviación privada, restaurantes, nightlife, seguridad y servicios a medida.',
        'h1': 'Ibiza excepcional, gestionada en privado.',
        'lead': 'Concierge privado y lifestyle management para clientes que esperan discreción, rapidez y una ejecución impecable en Ibiza.',
        'type': 'home',
        'image': '/assets/images/hero.jpg',
    },
    '/es/concierge-privado-ibiza/': {
        'title': 'Concierge privado Ibiza | Luxury Concierge | Ibiza VIP Move',
        'desc': 'Concierge privado en Ibiza para coordinar chófer, villas, yates, aviación, restaurantes, seguridad, wellness y peticiones especiales desde un solo contacto.',
        'h1': 'Concierge privado en Ibiza, sin fricción.',
        'lead': 'Un único punto de contacto para coordinar los detalles de una estancia privada, desde la llegada hasta la salida.',
        'type': 'concierge',
        'image': '/assets/images/villa.jpg',
    },
    '/es/chauffeur-privado-ibiza/': {
        'title': 'Chófer privado Ibiza | Conductor privado de lujo | Ibiza VIP Move',
        'desc': 'Servicio de chófer privado en Ibiza para aeropuerto, villas, hoteles, marinas, restaurantes, nightlife, disposiciones por horas y coordinación de varios vehículos.',
        'h1': 'Chófer privado en Ibiza, coordinado alrededor de tu agenda.',
        'lead': 'Movilidad privada para llegadas al aeropuerto, villas, hoteles, marinas, cenas, nightlife y jornadas completas en Ibiza.',
        'type': 'chauffeur',
        'image': '/assets/images/chauffeur.jpg',
    },
}


def hreflangs(en_path, es_path):
    return (
        f'<link rel="alternate" hreflang="en" href="{BASE}{en_path}">'
        f'<link rel="alternate" hreflang="es" href="{BASE}{es_path}">'
        f'<link rel="alternate" hreflang="x-default" href="{BASE}{en_path}">'
    )


def header():
    return f'''<header class="site-header"><a class="wordmark" href="/es/" aria-label="Ibiza VIP Move"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:50px;max-width:245px;object-fit:contain"></a><nav><a href="/es/concierge-privado-ibiza/">Concierge</a><a href="/es/chauffeur-privado-ibiza/">Chófer</a><a href="/private-office/">Private Office</a><a href="/ibiza-intelligence/">Ibiza Intelligence</a><a href="/contact/">Contacto</a><a class="nav-cta" href="{WA}">Solicitar concierge</a></nav><button class="menu-btn" aria-label="Abrir menú" aria-controls="mobileMenu">Menú</button></header><div class="mobile-menu" id="mobileMenu"><a href="/es/concierge-privado-ibiza/">Concierge</a><a href="/es/chauffeur-privado-ibiza/">Chófer</a><a href="/private-office/">Private Office</a><a href="/contact/">Contacto</a><a href="{WA}">WhatsApp Concierge</a></div>'''


def footer():
    return f'''<footer><div class="footer-grid"><div><div class="footer-brand"><img src="{LOGO}" alt="Ibiza VIP Move" style="display:block;width:auto;height:52px;max-width:260px;object-fit:contain"></div><p>Concierge privado, chófer y lifestyle management en Ibiza.</p></div><div><h4>Contacto</h4><a href="tel:+34600703303">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WA}">WhatsApp Concierge</a></div><div><h4>Idiomas</h4><a href="/">English</a><a href="/es/">Español</a><a href="/fr/">Français</a><a href="/de/">Deutsch</a><a href="/ar/">العربية</a></div></div><div class="footer-bottom"><span>© 2026 Ibiza VIP Move</span><span>Discreción · Precisión · Ibiza</span></div></footer><div class="mobile-bar"><a href="tel:+34600703303">Llamar</a><a href="{WA}">WhatsApp</a></div><script src="{JS}"></script>'''


def head(path, data, en_path):
    url = BASE + path
    schema = {
        '@context':'https://schema.org', '@type':'WebPage', 'name':data['title'], 'url':url,
        'description':data['desc'], 'inLanguage':'es',
        'isPartOf':{'@type':'WebSite','name':'Ibiza VIP Move','url':BASE+'/'},
        'about':{'@type':'Organization','name':'Ibiza VIP Move','url':BASE+'/'},
        'primaryImageOfPage':{'@type':'ImageObject','contentUrl':BASE+data['image']},
    }
    return f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(data['title'])}</title><meta name="description" content="{escape(data['desc'])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">{hreflangs(en_path,path)}<meta property="og:type" content="website"><meta property="og:site_name" content="Ibiza VIP Move"><meta property="og:locale" content="es_ES"><meta property="og:title" content="{escape(data['title'])}"><meta property="og:description" content="{escape(data['desc'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{data['image']}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" sizes="180x180" href="/favicon.png"><link rel="apple-touch-icon" href="/favicon.png"><meta name="theme-color" content="#090e13"><link rel="stylesheet" href="{CSS}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>'''


def page_body(data):
    common_intro = '''<section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>Un contacto. Todos los detalles alineados.</h2></div><div><p class="large">Coordinamos personas, lugares, horarios y proveedores alrededor de una sola agenda.</p><p>Chófer, villas, yates, aviación privada, restaurantes, nightlife, seguridad, chefs, wellness y peticiones especiales pueden gestionarse desde un único contacto en Ibiza.</p></div></section>'''
    if data['type'] == 'home':
        extra = '''<section class="dark-panel"><div class="kicker light">Servicios privados</div><h2>Ibiza, coordinada alrededor de ti.</h2><div class="trust-grid"><div><b>Chófer privado</b><p>Aeropuerto, villas, hoteles, marinas y nightlife.</p></div><div><b>Villas privadas</b><p>Estancias y necesidades operativas coordinadas.</p></div><div><b>Yates & Formentera</b><p>Marina, traslados, restauración y horarios alineados.</p></div><div><b>Aviación privada</b><p>Llegadas, equipaje y movilidad terrestre.</p></div><div><b>Dining & nightlife</b><p>Reservas, beach clubs y movimientos nocturnos.</p></div><div><b>Lifestyle management</b><p>Seguridad, chefs, wellness, eventos y solicitudes a medida.</p></div></div></section>'''
    elif data['type'] == 'concierge':
        extra = '''<section class="process"><div class="section-head"><div class="kicker dark">Cómo trabajamos</div><h2>Del brief a la ejecución.</h2></div><div class="process-grid"><article><span>01</span><h3>Brief</h3><p>Fechas, invitados, prioridades, privacidad y servicios necesarios.</p></article><article><span>02</span><h3>Alinear</h3><p>Conectamos movilidad, estancia, reservas y proveedores.</p></article><article><span>03</span><h3>Coordinar</h3><p>Mantenemos los detalles confirmados bajo una sola línea de comunicación.</p></article><article><span>04</span><h3>Adaptar</h3><p>Si cambian los planes, revisamos los elementos afectados.</p></article></div></section>'''
    else:
        extra = '''<section class="process"><div class="section-head"><div class="kicker dark">Movilidad privada</div><h2>Un conductor, una agenda clara.</h2></div><div class="process-grid"><article><span>01</span><h3>Aeropuerto</h3><p>Llegadas y salidas coordinadas con vuelo, equipaje y destino.</p></article><article><span>02</span><h3>Por horas</h3><p>Disponibilidad para varias paradas dentro de una agenda confirmada.</p></article><article><span>03</span><h3>Full day</h3><p>Conductor privado para jornadas completas y cambios de ubicación.</p></article><article><span>04</span><h3>Multi-vehículo</h3><p>Coordinación de grupos, equipaje y varios vehículos cuando el brief lo requiere.</p></article></div></section>'''
    return f'''<section class="page-hero" style="--hero:url('{data['image']}')"><div><div class="kicker light">Concierge privado · Ibiza</div><h1>{data['h1']}</h1><p>{data['lead']}</p><a class="btn gold" href="{WA}">Solicitar asistencia privada</a></div></section>{common_intro}{extra}<section class="closing-simple"><h2>Cuéntanos qué necesitas en Ibiza.</h2><p>Comparte fechas, número de invitados y prioridades. Continuamos la conversación de forma privada.</p><a class="btn dark" href="{WA}">Hablar por WhatsApp</a></section>'''

EN_MAP = {
    '/es/':'/',
    '/es/concierge-privado-ibiza/':'/private-concierge-ibiza/',
    '/es/chauffeur-privado-ibiza/':'/private-chauffeur-ibiza/',
}

for path, data in PAGES.items():
    dest = ROOT / path.strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    html = '<!doctype html><html lang="es">' + head(path,data,EN_MAP[path]) + f'<body>{header()}<main>{page_body(data)}</main>{footer()}</body></html>'
    dest.write_text(html, encoding='utf-8')

# Reciprocal hreflang from the English equivalents.
for es_path, en_path in EN_MAP.items():
    source = ROOT / en_path.strip('/') / 'index.html' if en_path != '/' else ROOT / 'index.html'
    if not source.exists():
        continue
    text = source.read_text(encoding='utf-8')
    es_tag = f'<link rel="alternate" hreflang="es" href="{BASE}{es_path}">'
    if es_tag not in text:
        text = text.replace('</head>', es_tag + '</head>', 1)
    source.write_text(text, encoding='utf-8')

sitemap = ROOT / 'sitemap.xml'
if sitemap.exists():
    text = sitemap.read_text(encoding='utf-8')
    additions = []
    for path in PAGES:
        url = BASE + path
        if url not in text:
            additions.append(f'<url><loc>{url}</loc></url>')
    if additions:
        text = text.replace('</urlset>', ''.join(additions) + '</urlset>')
        sitemap.write_text(text, encoding='utf-8')

checks = {
    'Spanish home': (ROOT/'es'/'index.html').is_file(),
    'Spanish concierge': (ROOT/'es'/'concierge-privado-ibiza'/'index.html').is_file(),
    'Spanish chauffeur': (ROOT/'es'/'chauffeur-privado-ibiza'/'index.html').is_file(),
    'Spanish sitemap': all((BASE+p) in (ROOT/'sitemap.xml').read_text(encoding='utf-8') for p in PAGES),
    'reciprocal home hreflang': 'hreflang="es"' in (ROOT/'index.html').read_text(encoding='utf-8'),
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if not all(checks.values()):
    raise SystemExit('Phase 14 Spanish validation failed')
print('PASS: Phase 14 Spanish local SEO')
