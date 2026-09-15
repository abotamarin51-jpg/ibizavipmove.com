"""Page-local French Partners reflow, preserving content and contact routes."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path('_site')
TARGET = Path('fr/partners/index.html')
CANONICAL = 'https://ibizavipmove.com/fr/partners/'
MARKER = 'id="ivm156-mobile-reflow"'
CSS = ('@media(max-width:600px){html[lang="fr"] .ivm-b2b-overview-inner>div'
       '{min-width:0;overflow-wrap:anywhere;hyphens:auto}}'
       '@media(min-width:601px) and (max-width:767px){html[lang="fr"] footer .footer-grid'
       '{grid-template-columns:1fr}}')
STYLE = f'<style {MARKER}>{CSS}</style>'


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit('Phase 156: ' + message)


def validate_baseline(html: str) -> None:
    tags = Tags(html).tags
    require(html.count('</head>') == 1, 'expected one head')
    require([a.get('href') for t, a in tags if t == 'link' and a.get('rel') == 'canonical']
            == [CANONICAL], 'French Partners canonical changed')
    require(any(t == 'html' and a.get('lang') == 'fr' for t, a in tags), 'French language required')
    for cls, expected in (('ivm-b2b-overview-inner', 3), ('footer-grid', 1)):
        require(sum(t == 'div' and cls in a.get('class', '').split() for t, a in tags) == expected,
                f'expected {expected} {cls} containers')


def enhance(root: Path = ROOT) -> None:
    path = root / TARGET
    html = path.read_text(encoding='utf-8')
    validate_baseline(html)
    if MARKER in html:
        require(html.count(MARKER) == html.count(STYLE) == 1, 'malformed existing reflow style')
        require(STYLE in html.split('</head>', 1)[0], 'reflow style outside head')
        return
    updated = html.replace('</head>', STYLE + '</head>', 1)
    require(updated.replace(STYLE, '', 1) == html, 'unexpected non-style change')
    path.write_text(updated, encoding='utf-8')
    print('PASS: Phase 156 — French Partners mobile copy and footer reflow without clipping')


def audit(root: Path = ROOT) -> None:
    target = root / TARGET
    html = target.read_text(encoding='utf-8')
    validate_baseline(html)
    require(html.count(STYLE) == html.count(MARKER) == 1, 'exact scoped reflow style required')
    require(STYLE in html.split('</head>', 1)[0], 'reflow style must remain in head')
    for path in root.rglob('*.html'):
        if path != target:
            require(MARKER not in path.read_text(encoding='utf-8'), f'unexpected style on {path}')
    print('PASS: Phase 156 audit — reflow isolated to French Partners; no global CSS changes')


if __name__ == '__main__':
    enhance()
    audit()
