from pathlib import Path
from urllib.parse import urlparse
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PAGES = {
    '/fr/partners/': {
        'terms': ('DMC', 'destination management', 'private travel management'),
        'links': ('/fr/services/', '/fr/conciergerie-privee-ibiza/', '/fr/private-office/'),
        'prefix': '/fr/',
    },
    '/de/partners/': {
        'terms': ('DMC', 'Destination Management', 'Private Travel Management'),
        'links': ('/de/services/', '/de/privater-concierge-ibiza/', '/de/private-office/'),
        'prefix': '/de/',
    },
    '/ar/partners/': {
        'terms': ('DMC', 'إدارة الوجهة', 'إدارة السفر الخاص'),
        'links': ('/ar/services/', '/ar/private-concierge-ibiza/', '/ar/private-office/'),
        'prefix': '/ar/',
    },
}


def file_for(path):
    return ROOT / path.strip('/') / 'index.html'

sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
for path, data in PAGES.items():
    target = file_for(path)
    if not target.exists():
        raise SystemExit(f'Phase 112 target missing: {path}')
    html = target.read_text(encoding='utf-8')
    if html.count('ivm-phase112-b2b-intent') != 1:
        raise SystemExit(f'Phase 112 section cardinality mismatch: {path}')
    section_match = re.search(r'<section\b[^>]*ivm-phase112-b2b-intent[^>]*>(.*?)</section>', html, re.I | re.S)
    if not section_match:
        raise SystemExit(f'Phase 112 section malformed: {path}')
    block = section_match.group(0)
    for term in data['terms']:
        if term not in block:
            raise SystemExit(f'Phase 112 term missing: {path} -> {term}')
    for href in data['links']:
        if block.count(f'href="{href}"') != 1:
            raise SystemExit(f'Phase 112 localized route mismatch: {path} -> {href}')
    internal = re.findall(r'<a\b[^>]*href=["\'](/[^"\']+)["\']', block, re.I)
    if any(not href.startswith(data['prefix']) for href in internal):
        raise SystemExit(f'Phase 112 cross-language link in localized section: {path} -> {internal}')
    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit(f'Phase 112 H1 drift: {path}')
    canonical = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', html, re.I)
    if canonical != [BASE + path]:
        raise SystemExit(f'Phase 112 canonical mismatch: {path} -> {canonical}')
    local_css = [h for h in re.findall(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', html, re.I)
                 if urlparse(h).path.startswith('/assets/')]
    if len(local_css) != 1 or not urlparse(local_css[0]).path.startswith('/assets/bundles/'):
        raise SystemExit(f'Phase 112 CSS performance drift: {path} -> {local_css}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 112 accessibility drift: {path}')
    if '+34 613 75 62 11' in html or '34613756211' in html:
        raise SystemExit(f'Phase 112 old phone leaked: {path}')
    if f'<loc>{BASE + path}</loc>' not in sitemap:
        raise SystemExit(f'Phase 112 existing partner URL missing from sitemap: {path}')

print('PASS: Phase 112 audit — localized DMC/private-travel intent, same-language partner pathways, canonicals, accessibility and single-bundle performance verified on FR/DE/AR Partner pages')
