"""Targeted German Partners mobile reflow; no copy or contact changes."""
from pathlib import Path

ROOT = Path('_site')
TARGET = Path('de/partners/index.html')
MARKER = 'id="ivm155-mobile-reflow"'
CSS = '@media(max-width:600px){html[lang="de"] .ivm-b2b-overview-inner>div{min-width:0;overflow-wrap:anywhere;hyphens:auto}}'
STYLE = f'<style {MARKER}>{CSS}</style>'


def enhance(root: Path = ROOT) -> None:
    path = root / TARGET
    html = path.read_text(encoding='utf-8')
    if MARKER in html:
        if html.count(MARKER) != 1 or html.count(STYLE) != 1:
            raise SystemExit('Phase 155: malformed existing mobile reflow style')
        return
    if (html.count('</head>') != 1 or '<html lang="de"' not in html
            or 'https://ibizavipmove.com/de/partners/' not in html
            or 'class="ivm-b2b-overview-inner"' not in html):
        raise SystemExit('Phase 155: German Partners baseline changed; review before writing')
    updated = html.replace('</head>', STYLE + '</head>', 1)
    if updated.replace(STYLE, '', 1) != html:
        raise SystemExit('Phase 155: unexpected non-style change')
    path.write_text(updated, encoding='utf-8')
    print('PASS: Phase 155 — German Partners mobile text may wrap without clipping')


def audit(root: Path = ROOT) -> None:
    target = root / TARGET
    html = target.read_text(encoding='utf-8')
    if html.count(STYLE) != 1 or html.count(MARKER) != 1:
        raise SystemExit('Phase 155 audit: exact scoped reflow style required')
    if STYLE not in html.split('</head>', 1)[0]:
        raise SystemExit('Phase 155 audit: style must remain in head')
    for path in root.rglob('*.html'):
        if path != target and MARKER in path.read_text(encoding='utf-8'):
            raise SystemExit(f'Phase 155 audit: unexpected style on {path}')
    print('PASS: Phase 155 audit — style isolated to German Partners; no global overflow hiding')


if __name__ == '__main__':
    enhance()
    audit()
