"""Apply two page-local mobile accessibility safeguards without adding languages or global CSS."""
from pathlib import Path

PAGE = Path('_site/vip-tables-club-access-ibiza/index.html')
CANONICAL = 'https://ibizavipmove.com/vip-tables-club-access-ibiza/'
LINK_STYLE = 'min-width:24px;min-height:44px;display:inline-flex;align-items:center;justify-content:center'
OLD = (
    f'<a href="{CANONICAL}" hreflang="en" lang="en" aria-current="page">'
    '<b>EN</b><small>English</small></a>'
)
NEW = (
    f'<a href="{CANONICAL}" hreflang="en" lang="en" aria-current="page" '
    f'style="{LINK_STYLE}"><b>EN</b><small>English</small></a>'
)
MENU_FIX = (
    '<style data-ivm181="menu-close">'
    '@media(max-width:900px){body.menu-open .site-header{position:fixed!important;z-index:100!important}}'
    '</style>'
)


def enhance() -> None:
    if not PAGE.is_file():
        raise SystemExit('Phase 181: VIP Tables page missing')
    html = PAGE.read_text(encoding='utf-8')
    changed = False

    if NEW in html:
        if html.count(NEW) != 1 or OLD in html:
            raise SystemExit('Phase 181: accessible language target duplicated or malformed')
    else:
        if html.count(OLD) != 1:
            raise SystemExit(f'Phase 181: expected one reviewed English language target, found {html.count(OLD)}')
        html = html.replace(OLD, NEW, 1)
        changed = True

    if MENU_FIX in html:
        if html.count(MENU_FIX) != 1:
            raise SystemExit('Phase 181: page-local menu safeguard duplicated')
    else:
        if html.count('</head>') != 1:
            raise SystemExit('Phase 181: head closing marker missing or duplicated')
        html = html.replace('</head>', MENU_FIX + '</head>', 1)
        changed = True

    if changed:
        PAGE.write_text(html, encoding='utf-8')
    print('PASS: Phase 181 — 24×44px English selector and page-local mobile menu close control preserved')


if __name__ == '__main__':
    enhance()
