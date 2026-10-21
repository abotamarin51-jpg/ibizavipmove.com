"""Give the single-language VIP Tables selector a minimum mobile target without adding languages."""
from pathlib import Path

PAGE = Path('_site/vip-tables-club-access-ibiza/index.html')
CANONICAL = 'https://ibizavipmove.com/vip-tables-club-access-ibiza/'
OLD = (
    f'<a href="{CANONICAL}" hreflang="en" lang="en" aria-current="page">'
    '<b>EN</b><small>English</small></a>'
)
NEW = (
    f'<a href="{CANONICAL}" hreflang="en" lang="en" aria-current="page" '
    'style="min-width:24px;min-height:44px;display:inline-flex;align-items:center;justify-content:center">'
    '<b>EN</b><small>English</small></a>'
)


def enhance() -> None:
    if not PAGE.is_file():
        raise SystemExit('Phase 181: VIP Tables page missing')
    html = PAGE.read_text(encoding='utf-8')
    if NEW in html:
        if html.count(NEW) != 1 or OLD in html:
            raise SystemExit('Phase 181: accessible language target duplicated or malformed')
        print('PASS: Phase 181 — VIP Tables language target already accessible')
        return
    if html.count(OLD) != 1:
        raise SystemExit(f'Phase 181: expected one reviewed English language target, found {html.count(OLD)}')
    PAGE.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 181 — single English language target keeps the existing component with a 24×44px minimum')


if __name__ == '__main__':
    enhance()
