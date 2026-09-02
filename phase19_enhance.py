from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
WA = 'https://wa.me/34600703303'

# Real Ibiza sunset photograph — Federico Di Dio / Unsplash, Ibiza, Spain.
# Source page: https://unsplash.com/photos/boat-on-sea-during-sunset-b77qz_-lf3A
IBIZA_HERO = 'https://images.unsplash.com/photo-1631193722492-9eee3ca45896'
variants = {
    'hero-desktop.jpg': IBIZA_HERO + '?auto=format&fit=crop&w=2200&h=1400&q=84&fm=jpg',
    'hero-mobile.jpg': IBIZA_HERO + '?auto=format&fit=crop&w=900&h=1250&q=82&fm=jpg',
}
img_dir = ROOT / 'assets' / 'images'
for name, url in variants.items():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 IbizaVIPMoveBuild/1.0'})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    if len(data) < 50_000:
        raise SystemExit(f'Phase 19 hero {name} unexpectedly small: {len(data)} bytes')
    (img_dir / name).write_bytes(data)
    print(f'Phase 19 Ibiza hero {name}: {len(data):,} bytes')

# Publish the new editorial design system on every page while keeping all URLs/canonicals.
style_src = '/assets/editorial-black.css?v=19'
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if style_src not in text and '</head>' in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{style_src}"></head>', 1)
    if '<html lang="en"' in text:
        text = text.replace('>Ibiza Intelligence<', '>Black Book<')
    path.write_text(text, encoding='utf-8')


def chapter(section_id, number, label, title, copy, href, image, alt):
    return f'''<section class="ivm-chapter" id="{section_id}">
      <div class="ivm-chapter-media"><img src="{image}" alt="{alt}" loading="lazy" decoding="async" width="1800" height="1200"></div>
      <div class="ivm-chapter-copy">
        <div class="ivm-chapter-number">{number} / {label}</div>
        <h2><small>{label}</small>{title}</h2>
        <p>{copy}</p>
        <a class="ivm-chapter-link" href="{href}">Discover {label} →</a>
      </div>
    </section>'''

chapters = ''.join([
    chapter('move','01','Move','Private Chauffeur','Airport arrivals, villa movements, dinner, nightlife and full-day mobility — coordinated around one confirmed itinerary.','/private-chauffeur-ibiza/','/assets/images/chauffeur.jpg','Private chauffeur and luxury mobility in Ibiza'),
    chapter('stay','02','Stay','Private Villas','Exceptional stays aligned around privacy, location, guest requirements and the rhythm of the island.','/luxury-villas-ibiza/','/assets/images/villa.jpg','Luxury villa and private stay in Ibiza'),
    chapter('sea','03','Sea','Yachts & Formentera','A day at sea planned as part of the stay — marina timing, chauffeur movements, dining and the evening that follows.','/yacht-charter-ibiza/','/assets/images/yacht.jpg','Private yacht experience in Ibiza and Formentera'),
    chapter('access','04','Access','Dining & Nightlife','Restaurants, beach clubs, celebrations and nightlife coordinated with timing, transport and the rest of your private brief.','/restaurants-nightlife-ibiza/','/assets/images/nightlife.jpg','Private dining and nightlife coordination in Ibiza'),
    chapter('fly','05','Fly','Private Aviation','Ground coordination around private and commercial arrivals: luggage, chauffeur, villa readiness and onward movement.','/private-aviation-ibiza/','/assets/images/aviation.jpg','Private aviation ground coordination in Ibiza'),
    chapter('protect','06','Protect','Discreet Security','Close-protection and private-security requirements coordinated discreetly around the principal, venue and itinerary.','/private-security-ibiza/','/assets/images/security.jpg','Discreet private security and close protection in Ibiza'),
])

home_main = f'''<section class="hero editorial-hero">
  <picture class="hero-picture">
    <source media="(max-width:700px)" srcset="/assets/images/hero-mobile.jpg">
    <img class="hero-media" src="/assets/images/hero-desktop.jpg" alt="Cinematic Ibiza sunset over the Mediterranean" width="2200" height="1400" fetchpriority="high" decoding="async">
  </picture>
  <div class="hero-content">
    <div class="kicker light">Ibiza · Private Concierge</div>
    <h1>Exceptional Ibiza.<br><em>Handled privately.</em></h1>
    <p>Private concierge, chauffeur and lifestyle management for clients who expect discretion, access and precise local execution.</p>
    <div class="hero-actions">
      <a class="btn gold" href="/contact/">Request Concierge</a>
      <a class="btn ghost" href="{WA}">WhatsApp 24/7</a>
    </div>
    <nav class="hero-index" aria-label="Private services">
      <a href="#move">Move</a><a href="#stay">Stay</a><a href="#sea">Sea</a><a href="#access">Access</a><a href="#fly">Fly</a><a href="#protect">Protect</a>
    </nav>
  </div>
</section>
<section class="ivm-manifesto">
  <div class="ivm-manifesto-inner">
    <div><div class="kicker dark">Private by design</div><h2>One trusted contact for the island.</h2></div>
    <div><p>Ibiza moves fast. Your private office on the island should move faster — quietly aligning the details behind the stay.</p><div class="manifesto-note">From airport to villa, marina to dinner, security to last-minute changes: Ibiza VIP Move keeps confirmed services connected through one line of communication.</div></div>
  </div>
</section>
<section class="ivm-chapters">{chapters}</section>
<section class="ivm-private-office">
  <div class="ivm-private-office-inner">
    <div><div class="kicker light">Private Office</div><h2>For stays that go beyond reservations.</h2></div>
    <div><p>High-touch Ibiza support for principals, families, personal assistants, family offices and travel professionals who need dependable local coordination behind a complex itinerary.</p><div class="office-rule"><span>Principals & Families</span><span>Personal Assistants</span><span>Family Offices</span></div><a class="ivm-chapter-link" href="/private-office/">Explore Private Office →</a></div>
  </div>
</section>
<section class="ivm-black-book" id="black-book">
  <div class="ivm-black-book-head">
    <div><div class="kicker dark">Curated Ibiza Intelligence</div><h2>The Ibiza<br>Black Book.</h2></div>
    <p class="black-book-intro">Not another guide to Ibiza. A private edit of how to move through the island well — arrivals, sea days, peak-season planning and the details that shape the stay.</p>
  </div>
  <div class="ivm-black-book-grid">
    <a class="ivm-book-card" href="/ibiza-intelligence/private-arrival/"><span>01 / Arrival</span><h3>The Private Arrival</h3><p>How aviation, luggage, chauffeur and villa readiness should connect before the principal lands.</p><b>Open the Black Book →</b></a>
    <a class="ivm-book-card" href="/ibiza-intelligence/ibiza-formentera-yacht-day/"><span>02 / Sea</span><h3>Ibiza by Sea</h3><p>Planning Ibiza and Formentera around marina timings, transport, dining and the evening that follows.</p><b>Open the Black Book →</b></a>
    <a class="ivm-book-card" href="/ibiza-intelligence/ibiza-august-planning/"><span>03 / Peak Season</span><h3>The August Brief</h3><p>What deserves to be arranged early when demand, traffic and availability are at their highest.</p><b>Open the Black Book →</b></a>
  </div>
  <div style="width:min(1240px,92vw);margin:42px auto 0"><a class="ivm-chapter-link" href="/ibiza-intelligence/">Enter The Ibiza Black Book →</a></div>
</section>
<section class="ivm-final-request">
  <div class="ivm-final-request-inner">
    <div class="kicker light">Private request</div>
    <h2>Tell us what Ibiza needs to look like.</h2>
    <p>You do not need every detail finalised. Share dates, guests and priorities; we will continue the conversation privately.</p>
    <div class="hero-actions"><a class="btn gold" href="/contact/">Request Concierge</a><a class="btn ghost" href="{WA}">WhatsApp 24/7</a></div>
  </div>
</section>'''

home_path = ROOT / 'index.html'
home = home_path.read_text(encoding='utf-8')
# Distinct home body hook.
if 'ivm-editorial-home' not in home:
    home = home.replace('<body>', '<body class="ivm-editorial-home">', 1)
# Minimal editorial navigation on home.
nav = (
    '<nav><a href="#move">Move</a><a href="#stay">Stay</a><a href="#sea">Sea</a>'
    '<a href="#access">Access</a><a href="#fly">Fly</a><a href="#protect">Protect</a>'
    '<a href="/ibiza-intelligence/">Black Book</a><a class="nav-cta" href="/contact/">Request Concierge</a></nav>'
)
home = re.sub(r'<nav>.*?</nav>', nav, home, count=1, flags=re.S)
mobile = (
    '<div class="mobile-menu" id="mobileMenu"><a href="#move">Move</a><a href="#stay">Stay</a><a href="#sea">Sea</a>'
    '<a href="#access">Access</a><a href="#fly">Fly</a><a href="#protect">Protect</a>'
    '<a href="/ibiza-intelligence/">The Ibiza Black Book</a><a href="/contact/">Request Concierge</a>'
    f'<a href="{WA}">WhatsApp 24/7</a></div>'
)
home = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>', mobile, home, count=1, flags=re.S)
home = re.sub(r'<main>.*?</main>', f'<main>{home_main}</main>', home, count=1, flags=re.S)
# Phase 18 preload stays valid because Phase 19 overwrites those same responsive files.
home = home.replace('Luxury private concierge experience overlooking the Mediterranean in Ibiza','Cinematic Ibiza sunset over the Mediterranean')
home_path.write_text(home, encoding='utf-8')

# Rebrand the existing /ibiza-intelligence/ hub visually as The Ibiza Black Book without changing URL/canonical.
book_path = ROOT / 'ibiza-intelligence' / 'index.html'
if book_path.exists():
    book = book_path.read_text(encoding='utf-8')
    if '<body class=' in book:
        book = re.sub(r'<body class="([^"]*)">', lambda m: f'<body class="{m.group(1)} ivm-black-book-page">', book, count=1)
    else:
        book = book.replace('<body>', '<body class="ivm-black-book-page">', 1)
    book = re.sub(r'<title>.*?</title>', '<title>The Ibiza Black Book | Ibiza VIP Move</title>', book, count=1, flags=re.S)
    book = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="The Ibiza Black Book by Ibiza VIP Move: private planning intelligence for arrivals, yachts, peak season and exceptional stays in Ibiza.">', book, count=1)
    book = re.sub(r'<h1>.*?</h1>', '<h1>The Ibiza Black Book</h1>', book, count=1, flags=re.S)
    book = book.replace('Ibiza Intelligence', 'The Ibiza Black Book')
    book_path.write_text(book, encoding='utf-8')

# Ensure the generated stylesheet is deployed.
asset_css = ROOT / 'assets' / 'editorial-black.css'
source_css = Path('editorial-black.css')
asset_css.write_text(source_css.read_text(encoding='utf-8'), encoding='utf-8')

# Validation of the requested direction.
home = home_path.read_text(encoding='utf-8')
required = [
    'Exceptional Ibiza.', 'WhatsApp 24/7', 'id="move"', 'id="stay"', 'id="sea"',
    'id="access"', 'id="fly"', 'id="protect"', 'The Ibiza Black Book', style_src,
]
missing = [x for x in required if x not in home]
if missing:
    raise SystemExit('Phase 19 home missing: ' + ', '.join(missing))
assert asset_css.is_file() and asset_css.stat().st_size > 5000
assert (img_dir / 'hero-desktop.jpg').stat().st_size < 1_000_000
assert (img_dir / 'hero-mobile.jpg').stat().st_size < 650_000
assert book_path.exists() and 'The Ibiza Black Book' in book_path.read_text(encoding='utf-8')
print('PASS: Phase 19 editorial luxury homepage + six chapters + Ibiza Black Book')
