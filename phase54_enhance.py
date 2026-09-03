from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)

CLUSTERS = {
 'partners': {
  'en':('/partners/','Partners'), 'es':('/es/partners/','Partners B2B'), 'fr':('/fr/partners/','Partenaires B2B'), 'de':('/de/partners/','B2B Partner'), 'ar':('/ar/partners/','شركاء B2B')},
 'office': {
  'en':('/private-office/','Private Office'), 'es':('/es/private-office/','Private Office'), 'fr':('/fr/private-office/','Private Office'), 'de':('/de/private-office/','Private Office'), 'ar':('/ar/private-office/','Private Office')},
}

PARTNER_AUDIENCE = [
 {'@type':'Audience','audienceType':'Luxury travel advisors'},
 {'@type':'Audience','audienceType':'Concierge companies'},
 {'@type':'Audience','audienceType':'Hospitality partners'},
 {'@type':'Audience','audienceType':'Personal assistants'},
 {'@type':'Audience','audienceType':'Family offices'},
]
OFFICE_AUDIENCE = [
 {'@type':'Audience','audienceType':'Principals'},
 {'@type':'Audience','audienceType':'Families'},
 {'@type':'Audience','audienceType':'Personal assistants'},
 {'@type':'Audience','audienceType':'Executive assistants'},
 {'@type':'Audience','audienceType':'Family offices'},
]


def has_type(html, target):
    for m in SCRIPT_RE.finditer(html):
        try: obj = json.loads(m.group(1))
        except Exception: continue
        if isinstance(obj, dict):
            typ = obj.get('@type')
            values = typ if isinstance(typ, list) else [typ]
            if target in values:
                return True
    return False


def enrich_webpage(html, kind, audience):
    def repl(match):
        try: obj = json.loads(match.group(1))
        except Exception: return match.group(0)
        if isinstance(obj, dict) and obj.get('@type') in ('WebPage','AboutPage','CollectionPage'):
            obj['audience'] = audience
            obj['about'] = {'@id': ORG}
        return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'
    return SCRIPT_RE.sub(repl, html)


def breadcrumb(path, label):
    return {
      '@context':'https://schema.org', '@type':'BreadcrumbList',
      'itemListElement':[
        {'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},
        {'@type':'ListItem','position':2,'name':label,'item':BASE+path},
      ]
    }


def office_service(path, lang, label):
    return {
      '@context':'https://schema.org','@type':'Service','name':label + ' · Ibiza VIP Move',
      'serviceType':'Private office and private client coordination in Ibiza',
      'url':BASE+path,'inLanguage':lang,'provider':{'@id':ORG},
      'areaServed':{'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},
      'audience':OFFICE_AUDIENCE,
    }

updated = 0
for kind, langs in CLUSTERS.items():
    for lang, (path, label) in langs.items():
        file = ROOT / path.strip('/') / 'index.html'
        if not file.exists():
            raise SystemExit(f'Phase 54 target missing: {path}')
        html = file.read_text(encoding='utf-8')
        audience = PARTNER_AUDIENCE if kind == 'partners' else OFFICE_AUDIENCE
        html = enrich_webpage(html, kind, audience)
        additions = []
        if not has_type(html, 'BreadcrumbList'):
            additions.append(breadcrumb(path, label))
        if kind == 'office' and not has_type(html, 'Service'):
            additions.append(office_service(path, lang, label))
        if additions:
            payload = ''.join('<script type="application/ld+json">'+json.dumps(obj, ensure_ascii=False)+'</script>' for obj in additions)
            html = html.replace('</head>', payload + '</head>', 1)
        file.write_text(html, encoding='utf-8')
        updated += 1

for kind, langs in CLUSTERS.items():
    for lang, (path, label) in langs.items():
        html = (ROOT / path.strip('/') / 'index.html').read_text(encoding='utf-8')
        assert has_type(html, 'BreadcrumbList'), (path, 'breadcrumb')
        assert '"audience"' in html, (path, 'audience')
        if kind == 'office':
            assert has_type(html, 'Service'), (path, 'service')
            assert 'Private office and private client coordination in Ibiza' in html, path
        assert html.count('<h1') == 1, path

print(f'PASS: Phase 54 B2B audience semantics and breadcrumbs applied to {updated} five-language Partners/Private Office pages')
