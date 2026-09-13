"""Read-only gate: qualified forms must not acquire obsolete competing handlers."""
from html.parser import HTMLParser
from pathlib import Path
import json
import subprocess
import xml.etree.ElementTree as ET
from phase135_audit import run as run_localized_services_routing_audit
from phase136_audit import run as run_localized_authority_footer_routing_audit
from phase137_audit import run as run_localized_contact_footer_routing_audit

ROOT = Path('_site')
CONTACTS = ('contact', 'es/contacto', 'fr/contact', 'de/kontakt', 'ar/contact')
GUARD = "const f=document.getElementById('conciergeForm');\nif(f&&!f.hasAttribute('data-ivm-qualified-brief')){"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.scripts = []
        self.current = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'script':
            self.current = [attrs, '']

    def handle_data(self, text):
        if self.current is not None:
            self.current[1] += text

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.scripts.append(self.current)
            self.current = None


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 133 audit: ' + message)


def run():
    premium = (ROOT / 'assets/premium.js').read_text(encoding='utf-8')
    require(premium.count(GUARD) == 1, 'qualified forms must bypass legacy handler')
    inline = []
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'sitemap inventory')
    for slug in CONTACTS:
        path = '/' + slug + '/'
        text = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
        page = Page(text)
        forms = [a for t, a in page.tags if t == 'form']
        require(len(forms) == 1 and forms[0].get('data-ivm-qualified-brief') == 'true', 'qualified form ' + path)
        refs = [a for a, code in page.scripts if a.get('src')]
        premium_refs = [a for a in refs if a['src'].split('?')[0] == '/assets/premium.js']
        require(len(premium_refs) == 1 and premium_refs[0]['src'] == '/assets/premium.js?v=133' and 'defer' in premium_refs[0], 'premium cache/defer ' + path)
        modern = [a for a in refs if a['src'].split('?')[0] == '/assets/phase107.js']
        require(len(modern) == 1 and 'defer' in modern[0], 'one modern form runtime ' + path)
        for attrs, code in page.scripts:
            if attrs.get('src') or attrs.get('type', '').lower() == 'application/ld+json':
                continue
            require('localizedConciergeForm' not in code and 'conciergeForm' not in code, 'obsolete inline form handler ' + path)
            inline.append({'path': path, 'code': code})
        require([a.get('href') for t, a in page.tags if t == 'link' and a.get('rel') == 'canonical'] == ['https://ibizavipmove.com' + path], 'canonical ' + path)
        require('https://ibizavipmove.com' + path in urls, 'contact discovery ' + path)
        for field in ('fName', 'fPhone', 'fClientType', 'fService'):
            matches = [a for t, a in page.tags if a.get('id') == field]
            require(len(matches) == 1 and 'required' in matches[0], 'required ' + field + ' ' + path)
    for filename in ('premium.js', 'phase63.js', 'phase107.js'):
        subprocess.run(['node', '--check', str(ROOT / 'assets' / filename)], check=True, capture_output=True, text=True)
    subprocess.run(['node', '-e', "const vm=require('node:vm');const fs=require('node:fs');for(const s of JSON.parse(fs.readFileSync(0,'utf8')))new vm.Script(s.code,{filename:s.path});"], input=json.dumps(inline), check=True, capture_output=True, text=True)
    print('PASS: Phase 133 audit — five qualified forms retain required inputs, canonical/sitemap and one modern owner; shared and inline JavaScript syntax valid; legacy handler gated')


if __name__ == '__main__':
    run()
    run_localized_services_routing_audit()
    run_localized_authority_footer_routing_audit()
    run_localized_contact_footer_routing_audit()
