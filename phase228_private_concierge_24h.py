"""Add one evidence-led 24/7 concierge FAQ to the existing English concierge page.

Bounded SEO/GEO change:
- one visible FAQ item
- matching FAQPage JSON-LD item
- truthful sitemap lastmod for this URL only
No title, meta description, H1, canonical, links, images, or layout changes.
"""
from pathlib import Path
import json
import re

ROOT = Path("_site")
TARGET = ROOT / "private-concierge-ibiza" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
CANONICAL = "https://ibizavipmove.com/private-concierge-ibiza/"
LASTMOD = "2026-11-11"

QUESTION = "What should I expect from a 24/7 dedicated concierge service in Ibiza?"
ANSWER = (
    "You can message your Ibiza VIP Move contact at any time during your stay. "
    "We use one local point of contact to coordinate confirmed transport, reservations, "
    "villas, yachts, staffing and itinerary changes as plans evolve. New, urgent or "
    "same-day requests are checked against availability and supplier terms before they "
    "are treated as confirmed."
)
QID = "faq-question-24-7"
AID = "faq-answer-24-7"

FAQ_SECTION = re.compile(
    r'<section\b[^>]*class="(?:faq|ivm-service-faq)"[^>]*>.*?</section>',
    re.S | re.I,
)
JSONLD = re.compile(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    re.S | re.I,
)


def require(ok, message):
    if not ok:
        raise SystemExit("Private Concierge 24/7 FAQ: " + message)


def scalar(pattern, html, label):
    match = re.search(pattern, html, re.S | re.I)
    require(match is not None, "missing " + label)
    return match.group(1)


def identity(html):
    return {
        "title": scalar(r"<title>(.*?)</title>", html, "title"),
        "description": scalar(r'<meta\s+name="description"\s+content="([^"]*)"', html, "meta description"),
        "canonical": scalar(r'<link\s+rel="canonical"\s+href="([^"]*)"', html, "canonical"),
        "h1": re.sub(r"\s+", " ", scalar(r"<h1\b[^>]*>(.*?)</h1>", html, "H1")).strip(),
        "links": len(re.findall(r"<a\b", html, re.I)),
        "images": len(re.findall(r"<img\b", html, re.I)),
    }


def faq_nodes(html):
    found = []
    for match in JSONLD.finditer(html):
        try:
            node = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(node, dict) and node.get("@type") == "FAQPage":
            found.append((match, node))
    return found


def audit(html):
    sections = list(FAQ_SECTION.finditer(html))
    require(len(sections) == 1, "expected exactly one visible FAQ section")
    section = sections[0].group()
    require(section.count(QUESTION) == 1, "visible 24/7 question missing or duplicated")
    require(section.count(ANSWER) == 1, "visible 24/7 answer missing or duplicated")
    require(html.count(f'id="{QID}"') == 1 and html.count(f'id="{AID}"') == 1,
            "visible FAQ fragment IDs missing or duplicated")

    nodes = faq_nodes(html)
    require(len(nodes) == 1, "expected exactly one FAQPage JSON-LD entity")
    items = nodes[0][1].get("mainEntity")
    require(isinstance(items, list), "FAQPage mainEntity is not a list")
    matches = [item for item in items if item.get("name") == QUESTION]
    require(len(matches) == 1, "structured 24/7 question missing or duplicated")
    answer = matches[0].get("acceptedAnswer", {})
    require(answer.get("text") == ANSWER, "structured answer mismatch")
    require(matches[0].get("@id") == CANONICAL + "#" + QID, "structured question ID mismatch")
    require(answer.get("@id") == CANONICAL + "#" + AID, "structured answer ID mismatch")


def update_sitemap(text):
    block_re = re.compile(
        r'(<url>\s*<loc>' + re.escape(CANONICAL) + r'</loc>)(.*?)(</url>)',
        re.S,
    )
    matches = list(block_re.finditer(text))
    require(len(matches) == 1, "target sitemap URL missing or duplicated")
    match = matches[0]
    body = match.group(2)
    if re.search(r"<lastmod>[^<]*</lastmod>", body):
        body = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", body, count=1)
    else:
        body = f"<lastmod>{LASTMOD}</lastmod>" + body
    replacement = match.group(1) + body + match.group(3)
    return text[:match.start()] + replacement + text[match.end():]


def enhance():
    require(TARGET.is_file() and SITEMAP.is_file(), "target page or sitemap missing")
    html = TARGET.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    before = identity(html)
    require(before["canonical"] == CANONICAL, "unexpected canonical")
    require('<html lang="en"' in html, "target is not the English page")

    if QUESTION in html:
        audit(html)
        updated_sitemap = update_sitemap(sitemap)
        if updated_sitemap != sitemap:
            SITEMAP.write_text(updated_sitemap, encoding="utf-8")
        print("PASS: Private Concierge 24/7 FAQ already installed; no duplicate")
        return

    sections = list(FAQ_SECTION.finditer(html))
    require(len(sections) == 1, "expected exactly one visible FAQ section before change")
    section = sections[0].group()
    require(QID not in html and AID not in html, "reserved FAQ IDs already exist")

    detail = (
        f'<details id="{QID}"><summary>{QUESTION}</summary>'
        f'<p id="{AID}">{ANSWER}</p></details>'
    )
    revised_section = section[:-10] + detail + "</section>"
    revised = html[:sections[0].start()] + revised_section + html[sections[0].end():]

    nodes = faq_nodes(revised)
    require(len(nodes) == 1, "expected exactly one FAQPage JSON-LD entity before schema update")
    script_match, faq = nodes[0]
    items = faq.get("mainEntity")
    require(isinstance(items, list), "FAQPage mainEntity is not a list")
    require(all(item.get("name") != QUESTION for item in items), "structured question already exists")
    items.append({
        "@type": "Question",
        "@id": CANONICAL + "#" + QID,
        "name": QUESTION,
        "acceptedAnswer": {
            "@type": "Answer",
            "@id": CANONICAL + "#" + AID,
            "text": ANSWER,
        },
    })
    encoded = json.dumps(faq, ensure_ascii=False).replace("<", "\\u003c")
    replacement = '<script type="application/ld+json">' + encoded + "</script>"
    revised = revised[:script_match.start()] + replacement + revised[script_match.end():]

    after = identity(revised)
    require(after == before, "title/meta/H1/canonical/link/image identity changed")
    audit(revised)

    TARGET.write_text(revised, encoding="utf-8")
    SITEMAP.write_text(update_sitemap(sitemap), encoding="utf-8")
    print("PASS: Added one 24/7 concierge FAQ with matching JSON-LD; SEO identity unchanged")


if __name__ == "__main__":
    enhance()
