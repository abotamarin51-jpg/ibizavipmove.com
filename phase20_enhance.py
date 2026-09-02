from pathlib import Path
import re

ROOT = Path('_site')
WA = 'https://wa.me/34600703303'
CSS_SRC = Path('editorial-inner.css')
CSS_DEST = ROOT / 'assets' / 'editorial-inner.css'
CSS_HREF = '/assets/editorial-inner.css?v=20'

PAGES = {
    '/services/': ('Services', '/assets/images/hero-desktop.jpg'),
    '/private-concierge-ibiza/': ('Concierge', '/assets/images/hero-desktop.jpg'),
    '/private-chauffeur-ibiza/': ('Move', '/assets/images/chauffeur.jpg'),
    '/luxury-villas-ibiza/': ('Stay', '/assets/images/villa.jpg'),
    '/yacht-charter-ibiza/': ('Sea', '/assets/images/yacht.jpg'),
    '/restaurants-nightlife-ibiza/': ('Access', '/assets/images/nightlife.jpg'),
    '/private-aviation-ibiza/': ('Fly', '/assets/images/aviation.jpg'),
    '/private-security-ibiza/': ('Protect', '/assets/images/security.jpg'),
    '/private-chef-staffing-ibiza/': ('Lifestyle', '/assets/images/chef.jpg'),
    '/luxury-car-rental-ibiza/': ('Move', '/assets/images/chauffeur.jpg'),
    '/wellness-ibiza/': ('Wellness', '/assets/images/wellness.jpg'),
    '/private-events-ibiza/': ('Events', '/assets/images/events.jpg'),
    '/bespoke-concierge-ibiza/': ('Bespoke', '/assets/images/bespoke.jpg'),
    '/private-office/': ('Private Office', '/assets/images/private-office.jpg'),
    '/partners/': ('Private Partners', '/assets/images/private-office.jpg'),
    '/about/': ('Ibiza VIP Move', '/assets/images/hero-desktop.jpg'),
}

NAV = (
    '<nav><a href="/private-chauffeur-ibiza/">Move</a>'
    '<a href="/luxury-villas-ibiza/">Stay</a>'
    '<a href="/yacht-charter-ibiza/">Sea</a>'
    '<a href="/restaurants-nightlife-ibiza/">Access</a>'
    '<a href="/private-aviation-ibiza/">Fly</a>'
    '<a href="/private-security-ibiza/">Protect</a>'
    '<a href="/ibiza-intelligence/">Black Book</a>'
    '<a class="nav-cta" href="/contact/">Request Concierge</a></nav>'
)
MOBILE = (
    '<div class="mobile-menu" id="mobileMenu">'
    '<a href="/private-chauffeur-ibiza/">Move</a>'
    '<a href="/luxury-villas-ibiza/">Stay</a>'
    '<a href="/yacht-charter-ibiza/">Sea</a>'
    '<a href="/restaurants-nightlife-ibiza/">Access</a>'
    '<a href="/private-aviation-ibiza/">Fly</a>'
    '<a href="/private-security-ibiza/">Protect</a>'
    '<a href="/ibiza-intelligence/">The Ibiza Black Book</a>'
    '<a href="/contact/">Request Concierge</a>'
    f'<a href="{WA}">WhatsApp 24/7</a></div>'
)

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'), encoding='utf-8')


def add_body_class(text, cls):
    m = re.search(r'<body(?:\s+class="([^"]*)")?>', text, re.I)
    if not m:
        return text
    existing = (m.group(1) or '').split()
    if cls not in existing:
        existing.append(cls)
    replacement = '<body class="' + ' '.join(x for x in existing if x) + '">'
    return text[:m.start()] + replacement + text[m.end():]


def add_hero_media(text, label, image):
    section = re.search(r'<section class="([^"]*\bpage-hero\b[^"]*)"([^>]*)>', text, re.I)
    if not section or 'page-hero-media' in text:
        return text
    alt = f'{label} — Ibiza VIP Move'
    media = f'<div class="page-hero-media"><img src="{image}" alt="{alt}" width="1800" height="1200" fetchpriority="high" decoding="async"></div>'
    insert = section.end()
    return text[:insert] + media + text[insert:]


def harmonize_kicker(text, label):
    # Only touch the first light kicker inside the page hero.
    hero = re.search(r'(<section class="[^"]*\bpage-hero\b[^"]*".*?</section>)', text, re.I | re.S)
    if not hero:
        return text
    block = hero.group(1)
    newblock = re.sub(r'<div class="kicker light">.*?</div>', f'<div class="kicker light">{label} · Ibiza</div>', block, count=1, flags=re.I | re.S)
    return text[:hero.start()] + newblock + text[hero.end():]


for url_path, (label, image) in PAGES.items():
    file = ROOT / url_path.strip('/') / 'index.html'
    if not file.exists():
        raise SystemExit(f'Missing Phase 20 target: {url_path}')
    text = file.read_text(encoding='utf-8')
    if '<html lang="en"' not in text:
        continue
    text = add_body_class(text, 'ivm-editorial-inner')
    if CSS_HREF not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{CSS_HREF}"></head>', 1)
    text = re.sub(r'<nav>.*?</nav>', NAV, text, count=1, flags=re.S)
    text = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>', MOBILE, text, count=1, flags=re.S)
    text = add_hero_media(text, label, image)
    text = harmonize_kicker(text, label)
    file.write_text(text, encoding='utf-8')

# Contact uses its existing two-column form but receives the same editorial language.
contact = ROOT / 'contact' / 'index.html'
text = contact.read_text(encoding='utf-8')
text = add_body_class(text, 'ivm-editorial-contact')
if CSS_HREF not in text:
    text = text.replace('</head>', f'<link rel="stylesheet" href="{CSS_HREF}"></head>', 1)
text = re.sub(r'<nav>.*?</nav>', NAV, text, count=1, flags=re.S)
text = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>', MOBILE, text, count=1, flags=re.S)
contact.write_text(text, encoding='utf-8')

# Keep the Black Book navigation consistent without changing its canonical URL.
book = ROOT / 'ibiza-intelligence' / 'index.html'
if book.exists():
    text = book.read_text(encoding='utf-8')
    text = re.sub(r'<nav>.*?</nav>', NAV, text, count=1, flags=re.S)
    text = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>', MOBILE, text, count=1, flags=re.S)
    if CSS_HREF not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{CSS_HREF}"></head>', 1)
    book.write_text(text, encoding='utf-8')

# Validation.
assert CSS_DEST.is_file() and CSS_DEST.stat().st_size > 5000
for url_path, (label, image) in PAGES.items():
    file = ROOT / url_path.strip('/') / 'index.html'
    html = file.read_text(encoding='utf-8')
    assert 'ivm-editorial-inner' in html, url_path
    assert CSS_HREF in html, url_path
    assert 'Black Book' in html, url_path
    if 'page-hero' in html:
        assert 'page-hero-media' in html, url_path
        assert image in html, url_path
contact_html = contact.read_text(encoding='utf-8')
assert 'ivm-editorial-contact' in contact_html and 'WhatsApp 24/7' in contact_html
print(f'PASS: Phase 20 editorial treatment applied to {len(PAGES)} English inner pages + Contact')
