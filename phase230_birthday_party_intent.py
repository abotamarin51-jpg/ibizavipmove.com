"""Add one helpful birthday-party planning paragraph to the existing Events page.

Search intent: private birthday party Ibiza / private parties Ibiza / luxury birthday Ibiza.
No extra landing pages, location claims, guarantees, title/H1/canonical/FAQ/schema
edits, links or layout changes. Fail closed when the approved source changes.
"""

from pathlib import Path

TARGET = Path("_site/private-events-ibiza/index.html")
ANCHOR = (
    '<p class="large">Coordinate villa dinners, celebrations, proposals and private '
    'occasions around the venue, guest count, timing, food, entertainment, '
    'production, décor and transport.</p>'
)
ADDITION = (
    '<p data-ivm230="birthday-parties">Planning a private birthday party in Ibiza? '
    'Share the date, guest count, preferred setting and whether you need a private '
    'villa dinner, entertainment, catering, guest transport or staffing. We can '
    'coordinate these requests around one event brief, subject to venue rules, '
    'supplier availability, applicable permissions and agreed terms.</p>'
)
CANONICAL = "https://ibizavipmove.com/private-events-ibiza/"


def require(condition, message):
    if not condition:
        raise SystemExit("Phase 230 birthday intent: " + message)


def enhance():
    require(TARGET.is_file(), "Events page missing")
    before = TARGET.read_text(encoding="utf-8")
    require(before.count(ANCHOR) == 1, "expected exactly one original lead paragraph")
    require(before.count('<link rel="canonical" href="' + CANONICAL + '">') == 1,
            "unexpected canonical")
    require(before.count("<h1") == 1, "unexpected H1 count")
    require(before.count('data-ivm230="birthday-parties"') <= 1,
            "duplicate birthday section")
    require('<html lang="en"' in before, "unexpected page language")
    require('name="robots" content="index,follow' in before,
            "unexpected robots status")

    if ADDITION in before:
        require(before.count(ADDITION) == 1, "duplicate or drifted birthday copy")
        require(before.count(ANCHOR + ADDITION) == 1, "birthday copy moved from approved anchor")
        print("PASS: Phase 230 — birthday-party content already present")
        return

    require('data-ivm230="birthday-parties"' not in before,
            "unexpected existing birthday copy")
    after = before.replace(ANCHOR, ANCHOR + ADDITION, 1)
    require(after.replace(ADDITION, "", 1) == before,
            "unapproved modification outside one new paragraph")
    require(after.split("</head>", 1)[0] == before.split("</head>", 1)[0],
            "SEO head must remain unchanged")
    for marker in ("<h1", "<a ", "<img ", "<details", "<script", 'hreflang="'):
        require(after.count(marker) == before.count(marker),
                "page structure changed: " + marker)
    TARGET.write_text(after, encoding="utf-8")
    print("PASS: Phase 230 — one Events planning paragraph; identity and structure preserved")


if __name__ == "__main__":
    enhance()
