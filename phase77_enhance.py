from pathlib import Path
from datetime import date
from html import unescape
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
TODAY = date.today().isoformat()
LANGS = ('en','es','fr','de','ar')
SLUGS = (
    'private-arrival',
    'ibiza-formentera-yacht-day',
    'ibiza-august-planning',
    'villa-arrival-planning',
    'nightlife-transport-planning',
    'private-aviation-ground-coordination',
)
REL = {
    'private-arrival':['private-aviation-ground-coordination','villa-arrival-planning','ibiza-august-planning'],
    'ibiza-formentera-yacht-day':['ibiza-august-planning','nightlife-transport-planning','private-arrival'],
    'ibiza-august-planning':['nightlife-transport-planning','villa-arrival-planning','ibiza-formentera-yacht-day'],
    'villa-arrival-planning':['private-arrival','private-aviation-ground-coordination','ibiza-august-planning'],
    'nightlife-transport-planning':['ibiza-august-planning','ibiza-formentera-yacht-day','villa-arrival-planning'],
    'private-aviation-ground-coordination':['private-arrival','villa-arrival-planning','ibiza-august-planning'],
}
SERVICE = {
    'en':[
        '/private-aviation-ibiza/','/yacht-charter-ibiza/','/private-concierge-ibiza/','/luxury-villas-ibiza/','/restaurants-nightlife-ibiza/','/private-aviation-ibiza/'
    ],
    'es':[
        '/es/aviacion-privada-ibiza/','/es/yate-privado-ibiza/','/es/concierge-privado-ibiza/','/es/villas-lujo-ibiza/','/es/restaurantes-nightlife-ibiza/','/es/aviacion-privada-ibiza/'
    ],
    'fr':[
        '/fr/aviation-privee-ibiza/','/fr/location-yacht-ibiza/','/fr/conciergerie-privee-ibiza/','/fr/villas-luxe-ibiza/','/fr/restaurants-nightlife-ibiza/','/fr/aviation-privee-ibiza/'
    ],
    'de':[
        '/de/private-aviation-ibiza/','/de/yachtcharter-ibiza/','/de/privater-concierge-ibiza/','/de/luxusvillen-ibiza/','/de/restaurants-nightlife-ibiza/','/de/private-aviation-ibiza/'
    ],
    'ar':[
        '/ar/private-aviation-ibiza/','/ar/yacht-charter-ibiza/','/ar/private-concierge-ibiza/','/ar/luxury-villas-ibiza/','/ar/restaurants-nightlife-ibiza/','/ar/private-aviation-ibiza/'
    ],
}
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)


def article_path(lang, slug):
    return f'/ibiza-intelligence/{slug}/' if lang == 'en' else f'/{lang}/ibiza-intelligence/{slug}/'


def hub_path(lang):
    return '/ibiza-intelligence/' if lang == 'en' else f'/{lang}/ibiza-intelligence/'


def file_for(path):
    return ROOT / path.strip('/') / 'index.html'


def clean_html(value):
    return unescape(re.sub(r'<[^>]+>', ' ', value or '')).replace('\n', ' ').strip()


def remove_article_schema(html):
    out=[]; pos=0
    for m in SCRIPT_RE.finditer(html):
        out.append(html[pos:m.start()])
        try: obj=json.loads(m.group(1))
        except Exception: obj=None
        if not (isinstance(obj,dict) and obj.get('@type') in ('Article','BlogPosting')):
            out.append(m.group(0))
        pos=m.end()
    out.append(html[pos:])
    return ''.join(out)

count=0
for lang in LANGS:
    hub = hub_path(lang)
    if not file_for(hub).exists():
        raise SystemExit(f'Phase 77 Black Book hub missing: {hub}')
    for idx, slug in enumerate(SLUGS):
        path = article_path(lang, slug)
        file = file_for(path)
        if not file.exists():
            raise SystemExit(f'Phase 77 article missing: {path}')
        html = file.read_text(encoding='utf-8')

        canonical_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
        h1_m = re.search(r'<h1\b[^>]*>(.*?)</h1>', html, re.I | re.S)
        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
        image_m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html, re.I)
        if not canonical_m or not h1_m or not desc_m or not image_m:
            raise SystemExit(f'Phase 77 article metadata incomplete: {path}')

        canonical = canonical_m.group(1).strip()
        expected = BASE + path
        if canonical != expected:
            raise SystemExit(f'Phase 77 canonical mismatch: {path}: {canonical}')
        headline = clean_html(h1_m.group(1))
        description = unescape(desc_m.group(1)).strip()
        image = image_m.group(1).strip()
        if image.startswith('/'):
            image = BASE + image
        if not headline or len(description) < 50:
            raise SystemExit(f'Phase 77 weak article metadata: {path}')

        related = [BASE + article_path(lang, s) for s in REL[slug]]
        service = BASE + SERVICE[lang][idx]
        for target in related:
            relpath = target.removeprefix(BASE)
            if not file_for(relpath).exists():
                raise SystemExit(f'Phase 77 related article missing: {path} -> {relpath}')
        if not file_for(SERVICE[lang][idx]).exists():
            raise SystemExit(f'Phase 77 service target missing: {path} -> {SERVICE[lang][idx]}')

        article = {
            '@context':'https://schema.org',
            '@type':'Article',
            '@id':canonical.rstrip('/') + '/#article',
            'headline':headline,
            'name':headline,
            'url':canonical,
            'description':description,
            'image':image,
            'inLanguage':lang,
            'dateModified':TODAY,
            'author':{'@id':ORG},
            'publisher':{'@id':ORG},
            'mainEntityOfPage':{'@type':'WebPage','@id':canonical},
            'isPartOf':{'@type':'CollectionPage','url':BASE + hub},
            'about':{'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},
            'isRelatedTo':[{'@type':'WebPage','url':u} for u in related],
            'mentions':{'@type':'Service','url':service},
        }

        html = remove_article_schema(html)
        payload = '<script type="application/ld+json">' + json.dumps(article, ensure_ascii=False) + '</script>'
        html = html.replace('</head>', payload + '</head>', 1)
        file.write_text(html, encoding='utf-8')
        count += 1

if count != 30:
    raise SystemExit(f'Phase 77 expected 30 Black Book articles, found {count}')

# Immediate validation: every article has exactly one normalized Article schema.
for lang in LANGS:
    for idx, slug in enumerate(SLUGS):
        path = article_path(lang, slug)
        html = file_for(path).read_text(encoding='utf-8')
        articles=[]
        for m in SCRIPT_RE.finditer(html):
            try:o=json.loads(m.group(1))
            except Exception:continue
            if isinstance(o,dict) and o.get('@type') in ('Article','BlogPosting'):
                articles.append(o)
        if len(articles) != 1:
            raise SystemExit(f'Phase 77 Article schema count wrong: {path} -> {len(articles)}')
        a=articles[0]
        canonical=BASE+path
        assert a.get('@type')=='Article', path
        assert a.get('@id')==canonical.rstrip('/')+'/#article', path
        assert a.get('url')==canonical, path
        assert a.get('inLanguage')==lang, path
        assert a.get('author',{}).get('@id')==ORG, path
        assert a.get('publisher',{}).get('@id')==ORG, path
        assert a.get('mainEntityOfPage',{}).get('@id')==canonical, path
        assert a.get('isPartOf',{}).get('url')==BASE+hub_path(lang), path
        assert len(a.get('isRelatedTo',[]))==3, path
        assert a.get('mentions',{}).get('url')==BASE+SERVICE[lang][idx], path
        assert 'datePublished' not in a, path

print('PASS: Phase 77 normalized Article schema across all 30 Black Book planning notes without inventing publication dates')
