"""Add one evidence-led German Limousinenservice FAQ to the existing chauffeur page.

Bounded SEO/GEO change:
- one visible FAQ item
- matching FAQPage JSON-LD item
- truthful sitemap lastmod for this URL only
No title, meta description, H1, canonical, links, images, hreflang, or layout changes.
"""
from pathlib import Path
import json
import re

ROOT = Path("_site")
TARGET = ROOT / "de" / "privater-chauffeur-ibiza" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
CANONICAL = "https://ibizavipmove.com/de/privater-chauffeur-ibiza/"
LASTMOD = "2026-11-11"

QUESTION = "Bieten Sie einen Limousinenservice auf Ibiza an?"
ANSWER = (
    "Ja. Sie können einen privaten Chauffeur- und Limousinenservice auf Ibiza für "
    "Flughafentransfers, Villen, Hotels, Marinas, Restaurants, Nightlife sowie stunden- "
    "oder tageweise Fahrten anfragen. Teilen Sie Datum, Fahrgastzahl, Gepäck und den "
    "gewünschten Ablauf mit. Fahrzeugtyp, Verfügbarkeit, Zeiten, Preis und Bedingungen "
    "werden vor der Buchung bestätigt."
)
QID = "faq-question-limousinenservice"
AID = "faq-answer-limousinenservice"
ANCHOR_QUESTION = "Kann ich eine Mercedes-Benz V-Klasse oder einen Sprinter auf Ibiza buchen?"

JSONLD = re.compile(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    re.S | re.I,
)


def require(ok, message):
    if not ok:
        raise SystemExit("German Limousinenservice FAQ: " + message)


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
        "hreflang": len(re.findall(r'hreflang="', html, re.I)),
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


def visible_insert(html):
    require(html.count(ANCHOR_QUESTION) == 1, "anchor FAQ question missing or duplicated")
    start = html.index(ANCHOR_QUESTION)
    details_end = html.find("</details>", start)
    require(details_end != -1, "anchor FAQ details close missing")
    details_end += len("</details>")
    detail = (
        f'<details id="{QID}"><summary>{QUESTION}</summary>'
        f'<p id="{AID}">{ANSWER}</p></details>'
    )
    return html[:details_end] + detail + html[details_end:]


def audit(html):
    require(html.count(QUESTION) == 2, "24/7 visible/schema-style occurrence count unexpected")
    require(html.count(ANSWER) == 2, "answer visible/schema-style occurrence count unexpected")
    require(html.count(f'id="{QID}"') == 1 and html.count(f'id="{AID}"') == 1,
            "visible FAQ IDs missing or duplicated")

    nodes = faq_nodes(html)
    require(len(nodes) == 1, "expected exactly one FAQPage JSON-LD entity")
    items = nodes[0][1].get("mainEntity")
    require(isinstance(items, list), "FAQPage mainEntity is not a list")
    matches = [item for item in items if item.get("name") == QUESTION]
    require(len(matches) == 1, "structured question missing or duplicated")
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
    require('<html lang="de"' in html, "target is not German")

    if QUESTION in html:
        audit(html)
        revised_sitemap = update_sitemap(sitemap)
        if revised_sitemap != sitemap:
            SITEMAP.write_text(revised_sitemap, encoding="utf-8")
        print("PASS: German Limousinenservice FAQ already installed; no duplicate")
        return

    revised = visible_insert(html)
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
    require(after == before, "title/meta/H1/canonical/link/image/hreflang identity changed")
    audit(revised)

    TARGET.write_text(revised, encoding="utf-8")
    SITEMAP.write_text(update_sitemap(sitemap), encoding="utf-8")
    print("PASS: Added German Limousinenservice FAQ with matching JSON-LD; SEO identity unchanged")


if __name__ == "__main__":
    enhance()
