from pathlib import Path
import re

# Ensure the machine-readable discovery layer exists before auditing it.
import phase106_discovery

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PRESS = ROOT / 'press-kit.txt'
MEDIA = ROOT / 'media-partners' / 'index.html'
FOUNDER = ROOT / 'founder' / 'index.html'
REPORT = ROOT / 'ibiza-luxury-operations-report-2026' / 'index.html'
LLMS = ROOT / 'llms.txt'
SITEMAP = ROOT / 'sitemap.xml'
FORBIDDEN = [
    '+34 613 75 62 11', '34613756211',
    'Ryan Hurt', 'Ryan Huber', 'Lucinda Edwards', 'Princess Noura', 'Princesa Noura',
    'AEROAFFAIRES', 'Sahab Travel', 'Optimum Chauffeurs', 'Corporate Paris',
    'member of Ibiza Luxury Destination', 'Ibiza Luxury Destination member',
    'AggregateRating', 'PostalAddress',
]


def canonical(html):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    return m.group(1) if m else ''


for target in (PRESS, MEDIA, FOUNDER, REPORT, LLMS, SITEMAP):
    if not target.exists():
        raise SystemExit(f'Phase 106 required output missing: {target}')

press = PRESS.read_text(encoding='utf-8')
if len(press) < 1800:
    raise SystemExit(f'Phase 106 press kit unexpectedly short: {len(press)} chars')
required_press = [
    'Official brand name: Ibiza VIP Move',
    'Founder: Juan Cruz',
    'Brand structure: founder-led private concierge and luxury lifestyle coordination brand',
    'Primary service area: Ibiza, Balearic Islands, Spain',
    'Official phone / WhatsApp: +34 600 703 303',
    'Partnerships and media email: partnership@ibizavipmove.com',
    'Approved short description',
    'Operational evidence published by Ibiza VIP Move',
    'Editorial and citation guidance',
    'Verification notes',
    'Official logo (SVG): https://ibizavipmove.com/assets/brand-logo.svg',
]
for phrase in required_press:
    if phrase not in press:
        raise SystemExit(f'Phase 106 press-kit fact missing: {phrase}')
for term in FORBIDDEN:
    if term.lower() in press.lower():
        raise SystemExit(f'Phase 106 forbidden press-kit term: {term}')

media = MEDIA.read_text(encoding='utf-8')
if canonical(media) != BASE + '/media-partners/':
    raise SystemExit(f'Phase 106 media canonical drift: {canonical(media)}')
if media.count('ivm-phase106-presskit') != 1:
    raise SystemExit('Phase 106 media press-kit section cardinality mismatch')
if media.count('rel="alternate" type="text/plain" href="/press-kit.txt"') != 1:
    raise SystemExit('Phase 106 plain-text alternate link missing/duplicated')
for href in ('/press-kit.txt','/founder/','/case-studies/','/ibiza-luxury-operations-report-2026/','/assets/brand-logo.svg'):
    if f'href="{href}"' not in media:
        raise SystemExit(f'Phase 106 media source link missing: {href}')
if 'rel="author" href="/founder/"' not in media:
    raise SystemExit('Phase 106 founder author relationship missing on media page')
if '+34 600 703 303' not in media or 'partnership@ibizavipmove.com' not in media:
    raise SystemExit('Phase 106 official media contact missing')
for term in FORBIDDEN:
    if term.lower() in media.lower():
        raise SystemExit(f'Phase 106 forbidden media-page term: {term}')

for target, expected_canonical in (
    (FOUNDER, BASE + '/founder/'),
    (REPORT, BASE + '/ibiza-luxury-operations-report-2026/'),
):
    html = target.read_text(encoding='utf-8')
    if canonical(html) != expected_canonical:
        raise SystemExit(f'Phase 106 canonical drift: {target}')
    if html.count('ivm-phase106-media-link') != 1:
        raise SystemExit(f'Phase 106 media-link cardinality mismatch: {target}')
    if 'href="/media-partners/"' not in html:
        raise SystemExit(f'Phase 106 media route missing: {target}')
    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit(f'Phase 106 H1 drift: {target}')
    if 'id="main-content"' not in html or 'class="ivm-skip-link"' not in html:
        raise SystemExit(f'Phase 106 accessibility drift: {target}')

llms = LLMS.read_text(encoding='utf-8')
if llms.count('## Press and citation resources') != 1:
    raise SystemExit('Phase 106 llms press section cardinality mismatch')
for url in (
    BASE + '/media-partners/',
    BASE + '/press-kit.txt',
    BASE + '/founder/',
    BASE + '/case-studies/',
    BASE + '/ibiza-luxury-operations-report-2026/',
):
    if url not in llms:
        raise SystemExit(f'Phase 106 llms resource missing: {url}')

sitemap = SITEMAP.read_text(encoding='utf-8')
if BASE + '/press-kit.txt' in sitemap:
    raise SystemExit('Phase 106 press-kit.txt should not be added to canonical HTML sitemap')

print('PASS: Phase 106 audit — press kit facts, citation guidance, founder/report media routing and AI discovery verified without invented memberships, client leaks or sitemap pollution')

# Phase 107 runs only after the press/citation layer is verified. It changes
# conversion qualification and measurement, not the indexable SEO inventory.
import phase107_enhance
import phase107_audit
