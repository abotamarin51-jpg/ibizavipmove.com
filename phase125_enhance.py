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
        if (attr(tag, 'rel') or '').lower().find('preload') >= 0
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


def set_href(tag: str, href: str):
    return re.sub(
        r'\bhref\s*=\s*(["\'])(.*?)\1',
        lambda match: f'href={match.group(1)}{href}{match.group(1)}',
        tag,
        count=1,
        flags=re.I | re.S,
    )


def enhance():
    changed_pages = []
    for path in ROOT.rglob('*.html'):
        html = path.read_text(encoding='utf-8')
        if '<link rel="canonical"' not in html:
            continue
        preloads = image_preloads(html)
        highs = priority_images(html)
        if len(preloads) != 1 or len(highs) != 1:
            continue
        preload = preloads[0]
        high = highs[0]
        preload_href = attr(preload, 'href')
        high_src = attr(high, 'src')
        if not preload_href or not high_src or preload_href == high_src:
            continue
        # Keep responsive preloads untouched unless their own source model is audited.
        if attr(preload, 'imagesrcset'):
            raise SystemExit(f'Phase 125 responsive preload mismatch requires manual review: {path}')
        replacement = set_href(preload, high_src)
        if replacement == preload:
            raise SystemExit(f'Phase 125 could not update preload href: {path}')
        html = html.replace(preload, replacement, 1)
        path.write_text(html, encoding='utf-8')
        changed_pages.append((path, preload_href, high_src))

    if not changed_pages:
        raise SystemExit('Phase 125 found no mismatched single-preload/single-priority-image pages to repair')

    print(f"PASS: Phase 125 aligned {len(changed_pages)} image preloads to each page's existing fetchpriority=high image")
    for path, old, new in changed_pages:
        print(f'  {path}: {old} -> {new}')
    return changed_pages


if __name__ == '__main__':
    enhance()
