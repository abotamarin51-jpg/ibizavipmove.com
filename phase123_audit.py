"""Regression gate for consolidated B2B operational evidence on /partners/."""
from html import unescape
from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ROUTE = '/partners/'
TARGET = ROOT / 'partners' / 'index.html'


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 123 audit: ' + message)


def run():
    require(TARGET.is_file(), 'partners page missing')
    html = TARGET.read_text(encoding='utf-8')
    require(html.count('ivm-phase104-authority') == 0, 'duplicate Phase 104 authority block still present')
    require(html.count('ivm-phase105-proof') == 1, 'retained evidence block count')
    proof_m = re.search(r'<section class="partners-strip ivm-phase105-proof".*?</section>', html, re.S)
    require(bool(proof_m), 'retained evidence block malformed')
    proof = proof_m.group(0)
    for href in ('/case-studies/', '/ibiza-luxury-operations-report-2026/', '/founder/'):
        require(f'href="{href}"' in proof, f'evidence route missing {href}')
    require('Operational evidence' in proof and 'travel advisors' in proof.lower(), 'B2B evidence context missing')
    require(len(re.findall(r'<h1\b', html, re.I)) == 1, 'H1 drift')
    require('id="main-content"' in html and 'class="ivm-skip-link"' in html, 'accessibility drift')
    canonical = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', html, re.I)
    require(canonical == [BASE + ROUTE], f'canonical mismatch {canonical}')
    css = [h for h in re.findall(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', html, re.I) if urlparse(h).path.startswith('/assets/')]
    require(len(css) == 1 and urlparse(css[0]).path.startswith('/assets/bundles/'), f'CSS bundle drift {css}')
    require('+34 613 75 62 11' not in html and '34613756211' not in html, 'old phone leaked')
    text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.I | re.S)
    text = unescape(re.sub(r'<[^>]+>', ' ', text))
    require(len(re.findall(r"\b[\wÀ-ÿ'’\-]+\b", text)) >= 400, 'partners content became too thin')
    alts = re.findall(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']([^"\']+)["\']\s+href=["\']([^"\']+)', html, re.I)
    require({lang.lower() for lang, href in alts} == {'en','es','fr','de','ar','x-default'}, f'hreflang set drift {alts}')

    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    tree = ET.parse(ROOT / 'sitemap.xml')
    urls = tree.getroot().findall('s:url', ns)
    locs = [u.find('s:loc', ns).text for u in urls if u.find('s:loc', ns) is not None]
    require(len(locs) == 156 and len(set(locs)) == 156, f'sitemap inventory drift {len(locs)}/{len(set(locs))}')
    matches = [u for u in urls if (u.find('s:loc', ns) is not None and u.find('s:loc', ns).text == BASE + ROUTE)]
    require(len(matches) == 1, 'partners sitemap entry count')
    lastmod = matches[0].find('s:lastmod', ns)
    require(lastmod is not None and lastmod.text == '2026-09-12', f'partners lastmod {lastmod.text if lastmod is not None else None}')
    print('PASS: Phase 123 audit — /partners/ has one concise operational-evidence block, preserved authority routes/canonical/hreflang/accessibility/CSS, and truthful 2026-09-12 lastmod across a 156-URL sitemap')


if __name__ == '__main__':
    run()
