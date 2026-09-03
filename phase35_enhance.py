from pathlib import Path
from urllib.parse import urlparse
import re

ROOT = Path('_site')
STYLE = '/assets/phase35.css?v=35'
CSS_SRC = Path('phase35.css')
CSS_DEST = ROOT / 'assets' / 'phase35.css'
BASE = 'https://ibizavipmove.com'

CSS_DEST.write_text(CSS_SRC.read_text(encoding='utf-8'), encoding='utf-8')

CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
IMG_TAG_RE = re.compile(r'<img\b[^>]*>', re.I)


def add_attr(tag, name, value=None):
    if re.search(rf'\s{name}(?:=|\s|>)', tag, re.I):
        return tag
    insert = f' {name}' if value is None else f' {name}="{value}"'
    return tag[:-1] + insert + '>'


def improve_images(text):
    hero_seen = False
    def repl(m):
        nonlocal hero_seen
        tag = m.group(0)
        classes = re.search(r'class="([^"]*)"', tag, re.I)
        cls = classes.group(1) if classes else ''
        is_hero = any(token in cls for token in ('hero-media','page-hero-media')) or 'fetchpriority="high"' in tag
        if is_hero and not hero_seen:
            hero_seen = True
            tag = add_attr(tag, 'decoding', 'async')
            tag = add_attr(tag, 'fetchpriority', 'high')
            return tag
        tag = add_attr(tag, 'loading', 'lazy')
        tag = add_attr(tag, 'decoding', 'async')
        return tag
    return IMG_TAG_RE.sub(repl, text)


def mark_current_nav(text, canonical):
    path = urlparse(canonical).path or '/'
    def repl(m):
        tag = m.group(0)
        href_m = re.search(r'href="([^"]+)"', tag, re.I)
        if not href_m:
            return tag
        href = href_m.group(1)
        if href.startswith(('http://','https://','#','mailto:','tel:')):
            return tag
        href_path = urlparse(href).path or '/'
        if href_path.rstrip('/') == path.rstrip('/'):
            tag = add_attr(tag, 'aria-current', 'page')
        return tag
    # Header/mobile navigation only; footer can stay neutral.
    for selector in ('<nav[^>]*>.*?</nav>', '<div class="mobile-menu"[^>]*>.*?</div>'):
        match = re.search(selector, text, re.I | re.S)
        if match:
            block = re.sub(r'<a\b[^>]*>', repl, match.group(0), flags=re.I)
            text = text[:match.start()] + block + text[match.end():]
    return text


count = 0
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if '</head>' not in text or '<body' not in text:
        continue
    canonical_m = CANONICAL_RE.search(text)
    canonical = canonical_m.group(1) if canonical_m else BASE + '/'

    if STYLE not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)

    # Keyboard users can bypass repeated navigation.
    if 'class="ivm-skip-link"' not in text:
        body_end = text.find('>', text.lower().find('<body')) + 1
        text = text[:body_end] + '<a class="ivm-skip-link" href="#main-content">Skip to content</a>' + text[body_end:]

    # Give the principal content landmark a stable target.
    text = re.sub(r'<main(?![^>]*\bid=)([^>]*)>', r'<main id="main-content"\1>', text, count=1, flags=re.I)
    text = improve_images(text)
    text = mark_current_nav(text, canonical)

    # Menu button state is controlled by premium.js; expose relationship at first paint.
    text = re.sub(r'<button class="menu-btn"(?![^>]*aria-expanded)([^>]*)>', r'<button class="menu-btn" aria-expanded="false"\1>', text, count=1, flags=re.I)

    path.write_text(text, encoding='utf-8')
    count += 1

# Validation.
assert CSS_DEST.exists() and CSS_DEST.stat().st_size > 1000
indexable = []
for p in ROOT.rglob('index.html'):
    html = p.read_text(encoding='utf-8')
    if 'noindex' not in html.lower():
        indexable.append((p, html))
for p,html in indexable:
    assert STYLE in html, p
    assert 'class="ivm-skip-link"' in html, p
    assert 'id="main-content"' in html, p
    assert html.count('id="main-content"') == 1, p
    assert 'aria-expanded="false"' in html or 'menu-btn' not in html, p
# Contact controls retain iOS-friendly form IDs and the submit workflow.
contact=(ROOT/'contact'/'index.html').read_text(encoding='utf-8')
assert 'id="conciergeForm"' in contact and 'id="fPhone"' in contact
print(f'PASS: Phase 35 mobile/accessibility polish applied to {count} HTML pages')
