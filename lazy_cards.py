from pathlib import Path
import re

ROOT = Path('_site')
ASSET = '/assets/performance.css?v=1'

CARD_PATTERN = re.compile(
    r'<div class="service-card-img" style="background-image:[^"]*?url\([\'\"]?([^\'\")]+)[\'\"]?\)"></div>',
    re.I,
)

replacements = 0
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')

    def convert(match):
        global replacements
        replacements += 1
        src = match.group(1)
        return (
            '<div class="service-card-img">'
            f'<img src="{src}" alt="" loading="lazy" decoding="async">'
            '</div>'
        )

    text = CARD_PATTERN.sub(convert, text)
    if replacements and ASSET not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{ASSET}"></head>')
    path.write_text(text, encoding='utf-8')

css = '''
.service-card-img{position:relative;overflow:hidden;background:#101820}
.service-card-img img{width:100%;height:100%;object-fit:cover;object-position:center;display:block}
.service-card-img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,12,16,.05),rgba(8,12,16,.42));pointer-events:none}
'''.strip() + '\n'
(ROOT / 'assets' / 'performance.css').write_text(css, encoding='utf-8')

print(f'Lazy-card optimization converted {replacements} service-card images')
