from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
FOUNDER = BASE + '/#juan-cruz'
SCRIPT_RE = re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)', re.I | re.S)

ABOUT = {
    'en': {
        'path': '/about/',
        'kicker': 'Founder-led concierge',
        'title': 'Personal accountability. One trusted contact.',
        'lead': 'Ibiza VIP Move is a personal concierge brand founded and led by Juan Cruz.',
        'body': 'Every brief begins with direct communication. Juan coordinates each request through a carefully selected network of independent Ibiza specialists, keeping transport, hospitality and lifestyle details aligned through one point of contact.',
    },
    'es': {
        'path': '/es/sobre-nosotros/',
        'kicker': 'Concierge dirigido por su fundador',
        'title': 'Responsabilidad personal. Un contacto de confianza.',
        'lead': 'Ibiza VIP Move es una marca personal de concierge fundada y dirigida por Juan Cruz.',
        'body': 'Cada solicitud comienza con una comunicación directa. Juan coordina cada petición mediante una red cuidadosamente seleccionada de especialistas independientes de Ibiza, manteniendo transporte, hospitalidad y lifestyle alineados desde un único punto de contacto.',
    },
    'fr': {
        'path': '/fr/a-propos/',
        'kicker': 'Conciergerie dirigée par son fondateur',
        'title': 'Responsabilité personnelle. Un contact de confiance.',
        'lead': 'Ibiza VIP Move est une marque personnelle de conciergerie fondée et dirigée par Juan Cruz.',
        'body': 'Chaque demande commence par une communication directe. Juan coordonne chaque mission avec un réseau soigneusement sélectionné de spécialistes indépendants à Ibiza, en alignant transport, hospitalité et lifestyle autour d’un seul point de contact.',
    },
    'de': {
        'path': '/de/ueber-uns/',
        'kicker': 'Vom Gründer persönlich geführt',
        'title': 'Persönliche Verantwortung. Ein verlässlicher Kontakt.',
        'lead': 'Ibiza VIP Move ist eine persönliche Concierge-Marke, gegründet und geführt von Juan Cruz.',
        'body': 'Jede Anfrage beginnt mit direkter Kommunikation. Juan koordiniert die einzelnen Anforderungen über ein sorgfältig ausgewähltes Netzwerk unabhängiger Ibiza-Spezialisten und hält Transport, Hospitality und Lifestyle über einen Ansprechpartner abgestimmt.',
    },
    'ar': {
        'path': '/ar/about/',
        'kicker': 'كونسيرج بإدارة المؤسس',
        'title': 'مسؤولية شخصية. جهة اتصال واحدة موثوقة.',
        'lead': 'Ibiza VIP Move علامة كونسيرج شخصية أسسها ويديرها Juan Cruz.',
        'body': 'يبدأ كل طلب بتواصل مباشر. ينسّق Juan كل متطلبات الإقامة عبر شبكة مختارة بعناية من المتخصصين المستقلين في إيبيزا، مع مواءمة النقل والضيافة وخدمات أسلوب الحياة من خلال جهة اتصال واحدة.',
    },
}

PERSON_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': FOUNDER,
    'name': 'Juan Cruz',
    'jobTitle': 'Founder',
    'url': BASE + '/about/',
    'worksFor': {'@id': ORG},
    'knowsAbout': [
        'Private concierge Ibiza',
        'Luxury lifestyle coordination Ibiza',
        'Private chauffeur coordination Ibiza',
        'Luxury villas Ibiza',
        'Yacht charter coordination Ibiza',
        'Private aviation ground coordination Ibiza',
    ],
}


def page(path):
    return ROOT / path.strip('/') / 'index.html'


def founder_section(data):
    return (
        '<section class="editorial ivm-founder-identity">'
        f'<div><div class="kicker dark">{data["kicker"]}</div><h2>{data["title"]}</h2></div>'
        f'<div><p class="large">{data["lead"]}</p><p>{data["body"]}</p></div>'
        '</section>'
    )


# Place the founder directly beside the factual brand information on every About page.
for data in ABOUT.values():
    target = page(data['path'])
    if not target.exists():
        raise SystemExit(f'Phase 100 About page missing: {data["path"]}')
    html = target.read_text(encoding='utf-8')
    if 'ivm-founder-identity' in html:
        raise SystemExit(f'Phase 100 duplicate founder section: {data["path"]}')
    marker = '<section class="ivm-official-facts">'
    if marker not in html:
        raise SystemExit(f'Phase 100 official facts marker missing: {data["path"]}')
    html = html.replace(marker, founder_section(data) + marker, 1)
    if data['path'] == '/about/':
        html = html.replace('Official company facts', 'Official brand facts', 1)
    target.write_text(html, encoding='utf-8')


organization_count = 0
person_pages = {BASE + '/', *(BASE + data['path'] for data in ABOUT.values())}

for target in ROOT.rglob('*.html'):
    html = target.read_text(encoding='utf-8')
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    canonical = canonical_match.group(1) if canonical_match else ''

    def enrich(match):
        global organization_count
        try:
            data = json.loads(match.group(2))
        except Exception:
            return match.group(0)
        nodes = data.get('@graph', []) if isinstance(data, dict) and isinstance(data.get('@graph'), list) else [data]
        changed = False
        for node in nodes:
            if not isinstance(node, dict) or node.get('@id') != ORG:
                continue
            types = node.get('@type')
            types = types if isinstance(types, list) else [types]
            if 'Organization' not in types:
                continue
            node['founder'] = {'@id': FOUNDER}
            organization_count += 1
            changed = True
        if not changed:
            return match.group(0)
        return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + match.group(3)

    html = SCRIPT_RE.sub(enrich, html)
    if canonical in person_pages:
        if FOUNDER in html and '"@type":"Person"' in html:
            raise SystemExit(f'Phase 100 duplicate Person entity: {canonical}')
        tag = '<script type="application/ld+json">' + json.dumps(PERSON_SCHEMA, ensure_ascii=False, separators=(',', ':')) + '</script>'
        if '</head>' not in html:
            raise SystemExit(f'Phase 100 head closing marker missing: {canonical}')
        html = html.replace('</head>', tag + '</head>', 1)
    target.write_text(html, encoding='utf-8')

if organization_count < 60:
    raise SystemExit(f'Phase 100 expected at least 60 canonical Organization entities, changed {organization_count}')

llms = ROOT / 'llms.txt'
if not llms.exists():
    raise SystemExit('Phase 100 llms.txt missing')
text = llms.read_text(encoding='utf-8')
text = text.replace(
    'Official website: https://ibizavipmove.com/\n',
    'Official website: https://ibizavipmove.com/\nFounder: Juan Cruz\nBusiness structure: founder-led personal concierge brand\n',
    1,
)
text = text.replace('a private concierge and luxury lifestyle coordination company serving Ibiza', 'a founder-led private concierge and luxury lifestyle coordination brand serving Ibiza')
text = text.replace('The company also supports principals', 'The brand also supports principals')
llms.write_text(text, encoding='utf-8')

print(f'PASS: Phase 100 founder identity — five localized About pages, six Person entity pages and {organization_count} Organization founder references aligned to the founder-led personal brand')
