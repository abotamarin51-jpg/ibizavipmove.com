"""Phase 147: remove structured-data validation noise without inventing facts.

The verified third-party Luxury Magazine reference was encoded as Article even though the
site only stores its title and URL. Google-style Article validators then report missing
headline/image/date fields on commercial pages. Preserve the verified subject relationship
as generic CreativeWork instead, and ensure Ibiza VIP Move Organization nodes carry the
existing first-party logo. Visible copy, URLs, canonicals, hreflang and sitemap are untouched.
"""
from pathlib import Path
import json
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG_ID = BASE + '/#organization'
LOGO = BASE + '/assets/brand-mark.svg'
ARTICLE_URL = 'https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/'
ARTICLE_NAME = 'Top Luxury Travel Concierge Services for Ibiza Dining in 2026'
SCRIPT_RE = re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)', re.I | re.S)


def _types(node):
    value = node.get('@type')
    return value if isinstance(value, list) else [value]


def _walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def enhance():
    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    external_changed = 0
    logos_added = 0
    pages_changed = 0

    for path in ROOT.rglob('*.html'):
        html = path.read_text(encoding='utf-8')
        if '</head>' not in html:
            continue
        head, body = html.split('</head>', 1)
        page_changed = False

        def rewrite(match):
            nonlocal external_changed, logos_added, page_changed
            try:
                data = json.loads(match.group(2))
            except Exception:
                return match.group(0)
            changed = False
            for node in list(_walk(data)):
                if not isinstance(node, dict):
                    continue
                types = _types(node)

                # Exact verified external reference from Phase 99. Do not invent article
                # rich-result fields we do not possess; use the broader CreativeWork type.
                if (
                    'Article' in types
                    and node.get('url') == ARTICLE_URL
                    and node.get('name') == ARTICLE_NAME
                ):
                    publisher = node.get('publisher')
                    if publisher is not None and not (
                        isinstance(publisher, dict)
                        and publisher.get('@type') == 'Organization'
                        and publisher.get('name') == 'Luxury Magazine'
                    ):
                        raise SystemExit(f'Phase 147: unexpected external publisher shape in {path}')
                    node.clear()
                    node.update({'@type': 'CreativeWork', 'name': ARTICLE_NAME, 'url': ARTICLE_URL})
                    external_changed += 1
                    changed = True

                # Normalize only the site's own Organization entity. Preserve richer logos
                # already present; add the existing first-party brand mark only when absent.
                if (
                    'Organization' in _types(node)
                    and (node.get('@id') == ORG_ID or node.get('name') == 'Ibiza VIP Move')
                    and 'logo' not in node
                ):
                    node['logo'] = {'@type': 'ImageObject', 'url': LOGO}
                    logos_added += 1
                    changed = True

            if not changed:
                return match.group(0)
            page_changed = True
            return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + match.group(3)

        updated_head = SCRIPT_RE.sub(rewrite, head)
        if page_changed:
            path.write_text(updated_head + '</head>' + body, encoding='utf-8')
            pages_changed += 1

    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 147: sitemap changed unexpectedly')

    # First application should affect the established Phase 99 footprint and the later
    # authority pages; a rerun is intentionally idempotent.
    if external_changed not in (0,) and external_changed < 60:
        raise SystemExit(f'Phase 147: external relationship footprint drifted ({external_changed})')
    if logos_added not in (0,) and logos_added < 10:
        raise SystemExit(f'Phase 147: own-organization logo footprint drifted ({logos_added})')

    print(
        f'PASS: Phase 147 — structured-data cleanup on {pages_changed} pages; '
        f'{external_changed} verified external Article nodes generalized to CreativeWork and '
        f'{logos_added} Ibiza VIP Move Organization logos completed; body/sitemap unchanged'
    )


if __name__ == '__main__':
    enhance()
