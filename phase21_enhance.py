from pathlib import Path
import re

ROOT = Path('_site')
WA = 'https://wa.me/34600703303'

LANGS = {
    'es': {'cta': 'Solicitar Concierge', 'move': '/es/chauffeur-privado-ibiza/'},
    'fr': {'cta': 'Demander Concierge', 'move': '/fr/chauffeur-prive-ibiza/'},
    'de': {'cta': 'Concierge anfragen', 'move': '/de/privater-chauffeur-ibiza/'},
    'ar': {'cta': 'اطلب الكونسيرج', 'move': '/ar/private-chauffeur-ibiza/'},
}

IMAGE_DIMS = {
    '/assets/images/hero-desktop.jpg': (2200, 1400),
    '/assets/images/villa.jpg': (2000, 1334),
    '/assets/images/chauffeur.jpg': (2000, 1333),
}


def add_body_class(text: str, cls: str) -> str:
    def repl(m):
        attrs = m.group(1)
        class_match = re.search(r'class="([^"]*)"', attrs)
        if class_match:
            classes = class_match.group(1).split()
            if cls not in classes:
                classes.append(cls)
            attrs = attrs[:class_match.start()] + f'class="{" ".join(classes)}"' + attrs[class_match.end():]
        else:
            attrs += f' class="{cls}"'
        return '<body' + attrs + '>'
    return re.sub(r'<body([^>]*)>', repl, text, count=1, flags=re.I)


def add_styles(text: str) -> str:
    tags = []
    if '/assets/editorial-inner.css?v=20' not in text:
        tags.append('<link rel="stylesheet" href="/assets/editorial-inner.css?v=20">')
    if '/assets/editorial-multilingual.css?v=21' not in text:
        tags.append('<link rel="stylesheet" href="/assets/editorial-multilingual.css?v=21">')
    if tags:
        text = text.replace('</head>', ''.join(tags) + '</head>', 1)
    return text


def replace_brand_nav(text: str, cta: str, move: str) -> str:
    nav = (
        '<nav class="editorial-nav" dir="ltr">'
        f'<a href="{move}">Move</a>'
        '<a href="/luxury-villas-ibiza/">Stay</a>'
        '<a href="/yacht-charter-ibiza/">Sea</a>'
        '<a href="/restaurants-nightlife-ibiza/">Access</a>'
        '<a href="/private-aviation-ibiza/">Fly</a>'
        '<a href="/private-security-ibiza/">Protect</a>'
        '<a href="/ibiza-intelligence/">Black Book</a>'
        f'<a class="nav-cta" href="{WA}">{cta}</a>'
        '</nav>'
    )
    text = re.sub(r'<nav(?:\s[^>]*)?>.*?</nav>', nav, text, count=1, flags=re.I | re.S)
    mobile = (
        '<div class="mobile-menu" id="mobileMenu" dir="ltr">'
        f'<a href="{move}">Move</a>'
        '<a href="/luxury-villas-ibiza/">Stay</a>'
        '<a href="/yacht-charter-ibiza/">Sea</a>'
        '<a href="/restaurants-nightlife-ibiza/">Access</a>'
        '<a href="/private-aviation-ibiza/">Fly</a>'
        '<a href="/private-security-ibiza/">Protect</a>'
        '<a href="/ibiza-intelligence/">Black Book</a>'
        f'<a href="{WA}">{cta}</a>'
        '</div>'
    )
    text = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>', mobile, text, count=1, flags=re.I | re.S)
    return text


def hero_image_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if 'chauffeur' in rel:
        return '/assets/images/chauffeur.jpg'
    if rel in {'es/index.html', 'fr/index.html', 'de/index.html', 'ar/index.html'}:
        return '/assets/images/hero-desktop.jpg'
    return '/assets/images/villa.jpg'


def inject_hero_media(text: str, image: str, alt: str) -> str:
    if 'class="page-hero-media"' in text:
        return text
    w, h = IMAGE_DIMS[image]
    media = f'<div class="page-hero-media"><img src="{image}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></div>'
    return re.sub(r'(<section class="[^"]*page-hero[^"]*"[^>]*>)', r'\1' + media, text, count=1, flags=re.I)


for lang in LANGS:
    folder = ROOT / lang
    if not folder.exists():
        continue
    for path in folder.rglob('index.html'):
        text = path.read_text(encoding='utf-8')
        text = add_body_class(text, 'ivm-editorial-inner')
        text = add_body_class(text, 'ivm-editorial-locale')
        text = add_styles(text)
        text = replace_brand_nav(text, LANGS[lang]['cta'], LANGS[lang]['move'])
        image = hero_image_for(path)
        alt = f'Ibiza VIP Move private luxury concierge experience in Ibiza — {lang.upper()}'
        text = inject_hero_media(text, image, alt)
        path.write_text(text, encoding='utf-8')

black_book = ROOT / 'ibiza-intelligence'
if black_book.exists():
    for path in black_book.rglob('index.html'):
        text = path.read_text(encoding='utf-8')
        text = add_body_class(text, 'ivm-editorial-inner')
        is_hub = path == black_book / 'index.html'
        text = add_body_class(text, 'ivm-black-book-page' if is_hub else 'ivm-black-book-article')
        text = add_styles(text)
        text = replace_brand_nav(text, 'Request Concierge', '/private-chauffeur-ibiza/')
        text = inject_hero_media(text, '/assets/images/hero-desktop.jpg', 'The Ibiza Black Book by Ibiza VIP Move — private Ibiza planning')
        text = text.replace('Ibiza Intelligence · ', 'The Ibiza Black Book · ')
        path.write_text(text, encoding='utf-8')

targets = []
for lang in LANGS:
    folder = ROOT / lang
    if folder.exists():
        targets.extend(folder.rglob('index.html'))
if black_book.exists():
    targets.extend(black_book.rglob('index.html'))
targets = list(dict.fromkeys(targets))

failed = []
for path in targets:
    text = path.read_text(encoding='utf-8')
    if '/assets/editorial-multilingual.css?v=21' not in text:
        failed.append(f'missing css: {path}')
    if 'ivm-editorial-inner' not in text:
        failed.append(f'missing editorial body class: {path}')
    if 'class="page-hero-media"' not in text:
        failed.append(f'missing semantic hero: {path}')
    if '<h1' not in text.lower():
        failed.append(f'missing h1: {path}')

ar_home = ROOT / 'ar' / 'index.html'
if ar_home.exists() and 'dir="rtl"' not in ar_home.read_text(encoding='utf-8'):
    failed.append('Arabic RTL lost')

for lang in LANGS:
    home = ROOT / lang / 'index.html'
    if home.exists():
        txt = home.read_text(encoding='utf-8')
        for label in ('Move', 'Stay', 'Sea', 'Access', 'Fly', 'Protect', 'Black Book'):
            if f'>{label}</a>' not in txt:
                failed.append(f'{lang} missing nav label {label}')

if failed:
    raise SystemExit('Phase 21 validation failed: ' + '; '.join(failed))
print(f'PASS: Phase 21 editorial multilingual + Black Book applied to {len(targets)} pages')
