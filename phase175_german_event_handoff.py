from pathlib import Path
import re

ROOT = Path('_site')
CANONICAL = 'https://ibizavipmove.com/de/privatkoch-villa-staff-ibiza/'
EVENT_PATH = '/de/private-events-ibiza/'
LINK = (
    '<p class="ivm-concierge-continuity">'
    'Eigenständige private Veranstaltungen oder Firmenevents koordinieren? '
    '<a class="text-link" href="/de/private-events-ibiza/">Eventkoordination Ibiza ansehen →</a>'
    '</p>'
)

def enhance(root: Path = ROOT) -> None:
    target = root / 'de' / 'privatkoch-villa-staff-ibiza' / 'index.html'
    sitemap_path = root / 'sitemap.xml'
    if not target.exists() or not sitemap_path.exists():
        raise SystemExit('Phase 175 target or sitemap missing')

    text = target.read_text(encoding='utf-8')
    if '<html lang="de"' not in text:
        raise SystemExit('Phase 175 German language guard failed')
    if f'<link rel="canonical" href="{CANONICAL}">' not in text:
        raise SystemExit('Phase 175 canonical guard failed')
    if '<meta name="robots" content="index,follow,max-image-preview:large">' not in text:
        raise SystemExit('Phase 175 indexability guard failed')

    if EVENT_PATH not in text:
        marker = re.compile(
            r'(<p class="ivm-concierge-continuity">Mehrere Services als einen Aufenthalt koordinieren\?'
            r'.*?<a class="text-link" href="/de/privater-concierge-ibiza/">Privaten Concierge Ibiza ansehen →</a></p>)',
            re.I | re.S,
        )
        text, count = marker.subn(lambda m: m.group(1) + LINK, text, count=1)
        if count != 1:
            raise SystemExit('Phase 175 continuity marker missing or ambiguous')
        target.write_text(text, encoding='utf-8')

    sitemap = sitemap_path.read_text(encoding='utf-8')
    pattern = rf'(<url><loc>{re.escape(CANONICAL)}</loc><lastmod>)[^<]+(</lastmod>)'
    sitemap, count = re.subn(pattern, r'\g<1>2026-10-02\g<2>', sitemap, count=1)
    if count != 1:
        raise SystemExit(f'Phase 175 sitemap target replacement count: {count}')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print('PASS: Phase 175 adds one German event handoff from villa staffing to the existing event-coordination page')

if __name__ == '__main__':
    enhance()
