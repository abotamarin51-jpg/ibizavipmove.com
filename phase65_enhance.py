from pathlib import Path
from urllib.parse import urlparse
import hashlib
import re
import shutil

# Phases 69–70 intentionally execute here, after every visible enhancer and
# immediately before final asset bundling/gates. They improve LCP discovery and
# image layout stability without changing any page design or copy.
import phase69_enhance
import phase70_enhance

ROOT = Path('_site')
ASSETS = ROOT / 'assets'
BUNDLES = ASSETS / 'bundles'
BUNDLES.mkdir(parents=True, exist_ok=True)

# Phase 21 linked this file but did not copy it into the published artifact.
# Restore the missing asset before bundling so multilingual/editorial pages keep
# the intended cascade and no published stylesheet URL can 404.
multilingual_src = Path('editorial-multilingual.css')
multilingual_dest = ASSETS / 'editorial-multilingual.css'
if not multilingual_src.exists():
    raise SystemExit('Phase 65 missing source editorial-multilingual.css')
shutil.copyfile(multilingual_src, multilingual_dest)

STYLE_RE = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*\bhref="([^"]+)"[^>]*>', re.I)
SCRIPT_RE = re.compile(r'<script\b([^>]*)\bsrc="([^"]+)"([^>]*)></script>', re.I)
NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)


def is_local_css(href: str) -> bool:
    path = urlparse(href).path
    return path.startswith('/assets/') and path.endswith('.css')


def local_asset_path(url: str) -> Path:
    return ROOT / urlparse(url).path.lstrip('/')

bundle_signatures = {}
indexable_pages = 0
css_links_before = 0
phase46_removed = 0
first_party_script_tags = 0

for file in ROOT.rglob('*.html'):
    html = file.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html):
        continue

    # Bundle every local stylesheet in the exact order it appears. External
    # font stylesheets stay separate. CSS url() references in this project are
    # absolute /assets/... URLs, so concatenation does not change resolution.
    local = []
    for match in STYLE_RE.finditer(html):
        href = match.group(1)
        if not is_local_css(href):
            continue
        css_path = local_asset_path(href)
        if not css_path.exists():
            raise SystemExit(f'Phase 65 missing referenced CSS: {href} on {file.relative_to(ROOT)}')
        local.append((match, href, css_path))

    if local:
        pieces = []
        signature_parts = []
        for _, href, css_path in local:
            css = css_path.read_text(encoding='utf-8')
            signature_parts.extend((href, hashlib.sha256(css.encode('utf-8')).hexdigest()))
            pieces.append(f'/* {href} */\n{css.strip()}\n')
        combined = '\n'.join(pieces)
        digest = hashlib.sha256('\n'.join(signature_parts).encode('utf-8')).hexdigest()[:16]
        bundle_href = f'/assets/bundles/{digest}.css'
        bundle_path = BUNDLES / f'{digest}.css'
        if bundle_path.exists() and bundle_path.read_text(encoding='utf-8') != combined:
            raise SystemExit(f'Phase 65 bundle collision: {bundle_path.name}')
        bundle_path.write_text(combined, encoding='utf-8')
        bundle_signatures[bundle_href] = tuple(href for _, href, _ in local)

        spans = [(m.start(), m.end()) for m, _, _ in local]
        first = local[0][0]
        # Remove from the end so earlier coordinates remain valid.
        for start, end in reversed(spans[1:]):
            html = html[:start] + html[end:]
        html = html[:first.start()] + f'<link rel="stylesheet" href="{bundle_href}">' + html[first.end():]
        css_links_before += len(local)

    # Phase 63 fully supersedes Phase 46 routing across all 55 services and all
    # five contact desks. Remove the legacy runtime so it cannot overwrite the
    # localized message/context after Phase 63 executes.
    legacy_count = html.count('/assets/phase46.js?v=46')
    if legacy_count:
        html = re.sub(r'<script\b[^>]*src="/assets/phase46\.js\?v=46"[^>]*></script>', '', html, flags=re.I)
        phase46_removed += legacy_count

    # First-party scripts are at the end of body today; defer makes the intent
    # explicit and keeps them non-render-blocking if markup placement evolves.
    def defer_script(match):
        nonlocal_marker = None
        before, src, after = match.group(1), match.group(2), match.group(3)
        attrs = before + after
        if not (src.startswith('/assets/') and urlparse(src).path.endswith('.js')):
            return match.group(0)
        if re.search(r'\b(?:defer|async)\b', attrs, re.I):
            return match.group(0)
        return f'<script src="{src}" defer></script>'

    html = SCRIPT_RE.sub(defer_script, html)
    file.write_text(html, encoding='utf-8')
    indexable_pages += 1

# Validate final production request shape and every first-party asset reference.
for file in ROOT.rglob('*.html'):
    html = file.read_text(encoding='utf-8')
    if NOINDEX_RE.search(html):
        continue

    local_styles = []
    for href in STYLE_RE.findall(html):
        if is_local_css(href):
            local_styles.append(href)
            if not local_asset_path(href).exists():
                raise SystemExit(f'Phase 65 final stylesheet missing: {href} on {file.relative_to(ROOT)}')
    if len(local_styles) != 1:
        raise SystemExit(f'Phase 65 expected exactly one local CSS bundle on {file.relative_to(ROOT)}, found {len(local_styles)}')
    if not local_styles[0].startswith('/assets/bundles/'):
        raise SystemExit(f'Phase 65 non-bundled local CSS remains on {file.relative_to(ROOT)}: {local_styles[0]}')

    if '/assets/phase46.js?v=46' in html:
        raise SystemExit(f'Phase 65 legacy Phase 46 runtime remains on {file.relative_to(ROOT)}')

    for tag in re.findall(r'<script\b[^>]*src="[^"]+"[^>]*></script>', html, re.I):
        src_m = re.search(r'src="([^"]+)"', tag, re.I)
        if not src_m:
            continue
        src = src_m.group(1)
        if src.startswith('/assets/') and urlparse(src).path.endswith('.js'):
            first_party_script_tags += 1
            if not local_asset_path(src).exists():
                raise SystemExit(f'Phase 65 final script missing: {src} on {file.relative_to(ROOT)}')
            if not re.search(r'\bdefer\b', tag, re.I):
                raise SystemExit(f'Phase 65 first-party script is not deferred: {src} on {file.relative_to(ROOT)}')

if not multilingual_dest.exists() or multilingual_dest.stat().st_size < 1000:
    raise SystemExit('Phase 65 multilingual stylesheet was not restored correctly')
if not bundle_signatures or css_links_before <= indexable_pages:
    raise SystemExit('Phase 65 stylesheet bundling did not reduce requests')

print(
    f'PASS: Phase 65 performance — {indexable_pages} indexable pages, '
    f'{css_links_before} local CSS requests consolidated to {indexable_pages}, '
    f'{len(bundle_signatures)} shared bundles, {phase46_removed} legacy Phase 46 script refs removed, '
    f'{first_party_script_tags} first-party script refs verified deferred'
)
