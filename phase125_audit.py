from pathlib import Path
import re

ROOT = Path('_site')


def attr(tag: str, name: str):
    match = re.search(rf'\b{re.escape(name)}\s*=\s*(["\'])(.*?)\1', tag, flags=re.I | re.S)
    return match.group(2) if match else None


def image_preloads(html: str):
    tags = re.findall(r'<link\b[^>]*>', html, flags=re.I | re.S)
    return [
        tag for tag in tags
        if 'preload' in (attr(tag, 'rel') or '').lower().split()
        and (attr(tag, 'as') or '').lower() == 'image'
        and attr(tag, 'href')
    ]


def priority_images(html: str):
    tags = re.findall(r'<img\b[^>]*>', html, flags=re.I | re.S)
    return [
        tag for tag in tags
        if (attr(tag, 'fetchpriority') or '').lower() == 'high'
        and attr(tag, 'src')
    ]


def run():
    eligible = 0
    mismatches = []
    for path in ROOT.rglob('*.html'):
        html = path.read_text(encoding='utf-8')
        if '<link rel="canonical"' not in html:
            continue
        preloads = image_preloads(html)
        highs = priority_images(html)
        if len(preloads) != 1 or len(highs) != 1:
            continue
        eligible += 1
        preload_href = attr(preloads[0], 'href')
        high_src = attr(highs[0], 'src')
        if preload_href != high_src:
            mismatches.append((path, preload_href, high_src))

    if eligible < 20:
        raise SystemExit(f'Phase 125 audit expected a meaningful preload cohort, found only {eligible}')
    if mismatches:
        detail = '; '.join(f'{p}: {old} != {new}' for p, old, new in mismatches[:10])
        raise SystemExit(f'Phase 125 preload/priority-image mismatches remain ({len(mismatches)}): {detail}')

    partners = (ROOT / 'partners' / 'index.html').read_text(encoding='utf-8')
    preloads = image_preloads(partners)
    highs = priority_images(partners)
    if (
        len(preloads) != 1
        or len(highs) != 1
        or attr(preloads[0], 'href') != '/assets/images/private-office.jpg'
        or attr(highs[0], 'src') != '/assets/images/private-office.jpg'
    ):
        raise SystemExit('Phase 125 Partners hero/preload alignment missing')

    print(f'PASS: Phase 125 audit — {eligible} canonical pages with one image preload and one fetchpriority=high image are aligned; no wrong-image preload remains in this cohort')


if __name__ == '__main__':
    run()
