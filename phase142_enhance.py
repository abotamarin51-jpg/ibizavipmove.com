"""Phase 142: give localized homepages the existing mobile hero source used by English Home.

This is a post-build, markup-only performance change. It creates no new asset or URL.
"""
from pathlib import Path

ROOT = Path('_site')
PAGES = ('fr', 'de', 'ar', 'es')
IMG_PREFIX = '<img '
DESKTOP = 'src="/assets/images/hero-desktop.jpg"'
MOBILE_SOURCE = '<source media="(max-width:700px)" srcset="/assets/images/hero-mobile.jpg">'
PICTURE_OPEN = '<picture class="ivm-ref-hero-picture">'
PICTURE_CLOSE = '</picture>'


def enhance():
    changed = 0
    for slug in PAGES:
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')

        if MOBILE_SOURCE in html:
            if html.count(MOBILE_SOURCE) != 1 or html.count(PICTURE_OPEN) < 1:
                raise SystemExit(f'Phase 142: unexpected existing mobile hero markup in {slug}')
            continue

        marker = 'fetchpriority="high"'
        candidates = []
        start = 0
        while True:
            i = html.find(IMG_PREFIX, start)
            if i < 0:
                break
            j = html.find('>', i)
            if j < 0:
                raise SystemExit(f'Phase 142: malformed img in {slug}')
            tag = html[i:j+1]
            if DESKTOP in tag and marker in tag:
                candidates.append((i, j+1, tag))
            start = j + 1

        if len(candidates) != 1:
            raise SystemExit(f'Phase 142: expected one priority desktop hero in {slug}, found {len(candidates)}')

        i, j, tag = candidates[0]
        wrapped = PICTURE_OPEN + MOBILE_SOURCE + tag + PICTURE_CLOSE
        html = html[:i] + wrapped + html[j:]
        path.write_text(html, encoding='utf-8')
        changed += 1

    print(f'PASS: Phase 142 — responsive mobile hero added to {changed} localized homepages')


if __name__ == '__main__':
    enhance()
