"""Connect the existing Private Office villa brief with the main Villa Concierge URL.

Single contextual link, preserving every other HTML byte, title, H1, schema,
canonical, contact form, WhatsApp and the source's other internal links.
Designed for the already-built pages; no new indexable URLs.
"""
from pathlib import Path

ROOT = Path("_site")
SOURCE = ROOT / "private-office" / "index.html"
DESTINATION = ROOT / "luxury-villas-ibiza" / "index.html"
SOURCE_CANONICAL = 'https://ibizavipmove.com/private-office/'
DEST_CANONICAL = 'https://ibizavipmove.com/luxury-villas-ibiza/'
OLD = (
    '<p id="assistant-villa-guide">Planning a villa stay? Use the '
    '<a class="text-link" href="/ibiza-intelligence/villa-arrival-planning/'
    '#assistant-villa-checklist">executive assistant\'s villa checklist</a> '
    'to prepare access, arrivals, staffing and approvals before sending the brief.</p>'
)
NEW = OLD.replace(
    'before sending the brief.</p>',
    'before sending the brief. For villa sourcing and guest services, '
    'explore <a class="text-link" href="/luxury-villas-ibiza/">'
    'luxury villa concierge in Ibiza</a>.</p>',
)


def enhance() -> None:
    if not SOURCE.is_file() or not DESTINATION.is_file():
        raise SystemExit("Phase 241: Private Office or Villa Concierge page missing")
    source_html = SOURCE.read_text(encoding="utf-8")
    destination_html = DESTINATION.read_text(encoding="utf-8")

    if source_html.count(f'<link rel="canonical" href="{SOURCE_CANONICAL}">') != 1:
        raise SystemExit("Phase 241: source canonical changed")
    if destination_html.count(f'<link rel="canonical" href="{DEST_CANONICAL}">') != 1:
        raise SystemExit("Phase 241: destination canonical changed")
    if source_html.count(NEW) == 1 and source_html.count(OLD) == 0:
        print("PASS: Phase 241 existing Villa Concierge link; no duplicate")
        return
    if source_html.count(OLD) != 1 or source_html.count('href="/luxury-villas-ibiza/"') != 0:
        raise SystemExit("Phase 241: expected one original villa brief and no existing Villa link")
    updated = source_html.replace(OLD, NEW, 1)
    if updated.replace(NEW, OLD, 1) != source_html:
        raise SystemExit("Phase 241: unrelated HTML changed")
    if updated.split("</head>", 1)[0] != source_html.split("</head>", 1)[0]:
        raise SystemExit("Phase 241: metadata drift")
    if updated.count('href="/luxury-villas-ibiza/"') != 1:
        raise SystemExit("Phase 241: villa link missing or duplicated")
    SOURCE.write_text(updated, encoding="utf-8")
    print("PASS: Phase 241 — one contextual villa link in existing Private Office brief")


if __name__ == "__main__":
    enhance()
