from pathlib import Path
import re

ROOT = Path('_site')

# Inject the phase-specific override stylesheet into every HTML page.
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if '/assets/luxury-overrides.css' not in text and '</head>' in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="/assets/luxury-overrides.css?v=1"></head>', 1)
    path.write_text(text, encoding='utf-8')

# Home hero: convert the visual from CSS-only background to a real image so
# browsers can prioritize it and search engines can understand/index it.
home = ROOT / 'index.html'
if home.exists():
    text = home.read_text(encoding='utf-8')
    old = '<section class="hero" style="--hero:url(\'/assets/images/hero.jpg\')">'
    if old in text and 'class="hero-media"' not in text:
        new = (
            '<section class="hero hero-with-media" style="--hero:url(\'/assets/images/hero.jpg\')">'
            '<img class="hero-media" src="/assets/images/hero.jpg" '
            'alt="Luxury private concierge experience overlooking the Mediterranean in Ibiza" '
            'width="2400" height="1600" fetchpriority="high" decoding="async">'
        )
        text = text.replace(old, new, 1)

    # Service cards: turn image backgrounds into semantic <img> elements.
    card_pattern = re.compile(
        r'<a class="service-card" href="(?P<href>[^"]+)">'
        r'<div class="service-card-img" style="background-image:[^"]*url\(\'(?P<src>/assets/images/[^\']+\.jpg)\'\)[^"]*"></div>'
        r'<div class="service-card-copy"><span>(?P<label>.*?)</span><h3>(?P<title>.*?)</h3>',
        re.S,
    )

    def card_repl(match):
        title = re.sub(r'<[^>]+>', '', match.group('title')).strip()
        return (
            f'<a class="service-card" href="{match.group("href")}">'
            f'<div class="service-card-img"><img src="{match.group("src")}" '
            f'alt="{title} in Ibiza — Ibiza VIP Move" loading="lazy" decoding="async" '
            f'width="1600" height="1000"></div>'
            f'<div class="service-card-copy"><span>{match.group("label")}</span><h3>{match.group("title")}</h3>'
        )

    text, count = card_pattern.subn(card_repl, text)
    home.write_text(text, encoding='utf-8')
    print(f'Image markup enhanced: {count} service cards converted')
