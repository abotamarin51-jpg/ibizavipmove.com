"""Read-only gate for Phase 145 local concierge metadata integrity."""
from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path('_site')
PAGES = {
    'private-concierge-marina-botafoch-ibiza': (
        'Private Concierge Marina Botafoch Ibiza | Ibiza VIP Move',
        'Private concierge for Marina Botafoch, Ibiza Town and Talamanca, coordinating chauffeurs, yachts, dining, nightlife, villas and private logistics.',
        'Private concierge for Marina Botafoch, Ibiza Town and Talamanca, coordinating chauffeur transport, yachts, dining, nightlife, villas and private client logistics.',
    ),
    'private-concierge-cala-jondal-es-cubells-ibiza': (
        'Private Concierge Cala Jondal & Es Cubells | Ibiza VIP Move',
        'Private concierge for Cala Jondal, Es Cubells and south Ibiza, coordinating villas, chauffeurs, beach clubs, yachts, dining, staffing and security.',
        'Private concierge for Cala Jondal, Es Cubells and the south of Ibiza, connecting villas, chauffeur transport, beach clubs, yachts, dining, staffing and security.',
    ),
    'private-concierge-santa-eulalia-roca-llisa-ibiza': (
        'Concierge Santa Eulalia & Roca Llisa | Ibiza VIP Move',
        'Private concierge for Santa Eulalia, Roca Llisa and east Ibiza, coordinating villas, family stays, chauffeurs, dining, yachts, wellness and private support.',
        'Private concierge for Santa Eulalia, Roca Llisa and east Ibiza, coordinating villas, family stays, chauffeur transport, dining, yachts, wellness and private support.',
    ),
    'private-concierge-santa-gertrudis-ibiza': (
        'Private Concierge Santa Gertrudis | Ibiza VIP Move',
        'Private concierge for Santa Gertrudis and central Ibiza villas, coordinating chauffeurs, private chefs, family logistics, wellness, dining and yacht days.',
        'Private concierge for Santa Gertrudis and central Ibiza villas, coordinating chauffeur transport, private chefs, family logistics, wellness, dining, yachts and bespoke support.',
    ),
}


class HeadTags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.in_title=False; self.title=''; self.scripts=[]; self.current_script=None; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if tag=='title': self.in_title=True
        if tag=='script' and attrs.get('type')=='application/ld+json': self.current_script=[]
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
        if tag=='script' and self.current_script is not None:
            self.scripts.append(''.join(self.current_script)); self.current_script=None
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.current_script is not None: self.current_script.append(data)


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 145 audit: ' + msg)


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values(): yield from walk(v)
    elif isinstance(node, list):
        for v in node: yield from walk(v)


def run():
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'canonical inventory changed')

    for slug,(title,desc,visible_baseline) in PAGES.items():
        path=ROOT/slug/'index.html'; require(path.is_file(),f'missing {slug}')
        html=path.read_text(encoding='utf-8'); require('</head>' in html,f'head boundary {slug}')
        head,body=html.split('</head>',1); parsed=HeadTags(head)
        require(parsed.title==title,f'exact title {slug}')
        require(len(title)<=60,f'title length {slug}: {len(title)}')
        require(len(desc)<=160,f'description length {slug}: {len(desc)}')
        require(body.count(visible_baseline)==1,f'visible hero baseline preserved {slug}')
        require(desc not in body,f'new description remains head-only {slug}')

        def meta(name=None, prop=None):
            return [a.get('content') for t,a in parsed.tags if t=='meta' and ((name and a.get('name')==name) or (prop and a.get('property')==prop))]
        require(meta(name='description')==[desc],f'meta description {slug}')
        require(meta(prop='og:title')==[title],f'OG title {slug}')
        require(meta(prop='og:description')==[desc],f'OG description {slug}')
        require(meta(name='twitter:title')==[title],f'Twitter title {slug}')
        require(meta(name='twitter:description')==[desc],f'Twitter description {slug}')
        require(sum(t=='h1' for t,a in HeadTags(body).tags)==1,f'one H1 {slug}')

        url='https://ibizavipmove.com/'+slug+'/'
        require([a.get('href') for t,a in parsed.tags if t=='link' and a.get('rel')=='canonical']==[url],f'self canonical {slug}')
        require({a.get('hreflang') for t,a in parsed.tags if t=='link' and a.get('rel')=='alternate'}=={'en','x-default'},f'hreflang cluster {slug}')
        require(not any(t=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower() for t,a in parsed.tags),f'indexability {slug}')
        require(url in urls,f'sitemap membership {slug}')

        nodes=[]
        for raw in parsed.scripts:
            try: nodes.extend(walk(json.loads(raw)))
            except json.JSONDecodeError: pass
        require(any(n.get('@type')=='WebPage' and n.get('name')==title and n.get('description')==desc for n in nodes),f'WebPage schema metadata {slug}')
        require(any(n.get('@type')=='Service' and n.get('description')==desc for n in nodes),f'Service schema description {slug}')

    print('PASS: Phase 145 audit — four local concierge pages keep visible body/canonical/hreflang/indexability while search/social metadata stays <=60/160 chars; 156 URLs preserved')


if __name__=='__main__':
    run()
