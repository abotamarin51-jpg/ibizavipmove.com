"""Strengthen the existing Ibiza destination-management page for professional B2B briefs.

Search Console URL Inspection currently reports the page as crawled but not indexed,
while sibling service-model pages are indexed. This phase does not create another URL.
It makes the page's primary heading explicit and adds a practical partner-handover
section so the existing canonical is more useful and more distinct for travel advisors,
concierge firms, private offices and hospitality partners.
"""
from pathlib import Path
import re

ROOT = Path('_site')
PAGE = ROOT / 'destination-management-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
URL = 'https://ibizavipmove.com/destination-management-ibiza/'
DATE = '2026-09-13'

OLD_H1 = '<h1>One Ibiza operator<br><em>behind the itinerary.</em></h1>'
NEW_H1 = '<h1>Luxury destination management in Ibiza,<br><em>behind the client itinerary.</em></h1>'
ANCHOR = '<section class="dark-panel"><div class="kicker light">Why this service exists</div>'
BLOCK = '''<section class="dark-panel ivm-phase134-brief" aria-label="Professional Ibiza handover brief"><div class="kicker light">Professional handover brief</div><h2>What your Ibiza operator needs before execution.</h2><div class="trust-grid"><div><b>Client relationship</b><p>Confirm who owns the guest relationship, who can approve changes and whether Ibiza VIP Move should be client-facing or work behind the originating partner.</p></div><div><b>Arrival & accommodation</b><p>Share confirmed arrival timing, guest and luggage requirements, accommodation details and the practical access contact for the stay.</p></div><div><b>Local dependencies</b><p>Flag vehicles, marina or yacht timings, dining, staffing, security and other confirmed services whose timing affects the wider itinerary.</p></div><div><b>Communication route</b><p>Identify the primary partner contact, escalation point and approval boundaries so operational updates reach the right person.</p></div></div></section>\n'''


def update_sitemap(text: str) -> str:
    pattern = re.compile(r'(<url>\s*<loc>' + re.escape(URL) + r'</loc>)(.*?)(</url>)', re.S)
    m = pattern.search(text)
    if not m:
        raise SystemExit('Phase 134: destination-management sitemap entry missing')
    middle = m.group(2)
    if '<lastmod>' in middle:
        middle, count = re.subn(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{DATE}</lastmod>', middle, count=1)
        if count != 1:
            raise SystemExit('Phase 134: destination-management lastmod drift')
    else:
        middle = f'\n    <lastmod>{DATE}</lastmod>' + middle
    return text[:m.start()] + m.group(1) + middle + m.group(3) + text[m.end():]


def enhance():
    if not PAGE.is_file() or not SITEMAP.is_file():
        raise SystemExit('Phase 134: required output missing')
    html = PAGE.read_text(encoding='utf-8')
    sm = SITEMAP.read_text(encoding='utf-8')

    already = NEW_H1 in html and BLOCK.strip() in html
    if already:
        if OLD_H1 in html or html.count(NEW_H1) != 1 or html.count('ivm-phase134-brief') != 1:
            raise SystemExit('Phase 134: enhanced state drift')
    else:
        if html.count(OLD_H1) != 1:
            raise SystemExit(f'Phase 134: expected one original H1, found {html.count(OLD_H1)}')
        if html.count(ANCHOR) != 1:
            raise SystemExit(f'Phase 134: insertion anchor drift, found {html.count(ANCHOR)}')
        html = html.replace(OLD_H1, NEW_H1, 1)
        html = html.replace(ANCHOR, BLOCK + ANCHOR, 1)

    sm2 = update_sitemap(sm)
    PAGE.write_text(html, encoding='utf-8')
    SITEMAP.write_text(sm2, encoding='utf-8')
    print('PASS: Phase 134 destination-management canonical strengthened with descriptive H1, professional handover brief and truthful lastmod')


if __name__ == '__main__':
    enhance()
