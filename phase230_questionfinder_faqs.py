"""Two user-approved, narrowly scoped QuestionFinder FAQs.

The generated pages already explain pricing factors. This adds only one
specific customer question and its matching FAQPage JSON-LD entry to
each of the two existing pages. It does not change SEO metadata, page
identity, URLs, site architecture, or any other page.
Run after the final general build audits on both CI and deployment.
"""
from copy import deepcopy
from html import escape
from pathlib import Path
import json
import re

ROOT = Path("_site")
SCRIPT = re.compile(r'(<script\s+type="application/ld\+json">)(.*?)(</script>)', re.S | re.I)
FAQ_SECTION = re.compile(r'<section\b[^>]*class="(?:faq|ivm-service-faq)"[^>]*>.*?</section>', re.S | re.I)

CASES = (
    {
        "path": "luxury-villas-ibiza/index.html",
        "url": "https://ibizavipmove.com/luxury-villas-ibiza/",
        "q": "How much does a luxury villa in Ibiza cost?",
        "a": (
            "The cost of a luxury villa in Ibiza depends on your travel dates, "
            "preferred location, number of bedrooms, length of stay and requested services. "
            "Our Ibiza concierge team can review suitable villa options based on your "
            "group size, budget and preferences. Before confirming a reservation, "
            "we clarify the total rental price, included services, applicable deposits, "
            "additional costs and cancellation terms. Request a tailored villa proposal "
            "by sharing your dates, guest count, preferred area and budget."
        ),
        "qid": "faq-question-villa-cost",
        "aid": "faq-answer-villa-cost",
    },
    {
        "path": "hi-ibiza-vip-tables/index.html",
        "url": "https://ibizavipmove.com/hi-ibiza-vip-tables/",
        "q": "How much does a VIP table at Hï Ibiza cost?",
        "a": (
            "VIP table pricing at Hï Ibiza varies depending on the event, date, "
            "table location, number of guests and applicable minimum spend. "
            "For a personalised quotation, share your preferred event date, guest count, "
            "table preferences and approximate budget. Our concierge team can review "
            "the available options and clarify the minimum spend, deposit, entry "
            "arrangements and cancellation conditions before confirmation. "
            "Request your Hï Ibiza VIP table quotation."
        ),
        "qid": "faq-question-hi-cost",
        "aid": "faq-answer-hi-cost",
    },
)


def require(condition, message):
    if not condition:
        raise SystemExit("QuestionFinder FAQ scope validation: " + message)


def tag_list(html, pattern):
    return re.findall(pattern, html, re.S | re.I)


def schema_nodes(html):
    matches = []
    for match in SCRIPT.finditer(html):
        data = json.loads(match.group(2))
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            matches.append((match, data))
    return matches


def change(original, case):
    label = case["path"]
    require(original.count('<link rel="canonical" href="' + case["url"] + '">') == 1,
            "expected canonical missing: " + label)
    require(case["q"] not in original, "question already exists: " + label)
    require('id="' + case["qid"] + '"' not in original,
            "question ID already present: " + label)

    sections = list(FAQ_SECTION.finditer(original))
    require(len(sections) == 1, "one FAQ section expected: " + label)
    old_section = sections[0].group()
    require(old_section.count("<details") == 3, "three existing FAQ items expected: " + label)

    faqs = schema_nodes(original)
    require(len(faqs) == 1, "one JSON-LD FAQPage expected: " + label)
    original_faq = faqs[0][1]
    old_items = deepcopy(original_faq.get("mainEntity", []))
    require(len(old_items) == 3, "three existing structured FAQs expected: " + label)

    snippet = (
        '<details id="' + case["qid"] + '"><summary>' + escape(case["q"]) +
        '</summary><p id="' + case["aid"] + '">' + escape(case["a"]) +
        '</p></details>'
    )
    require(old_section.endswith("</section>"), "unexpected FAQ closing tag: " + label)
    new_section = old_section[:-len("</section>")] + snippet + "</section>"
    changed = original[:sections[0].start()] + new_section + original[sections[0].end():]

    match, faq = schema_nodes(changed)[0]
    new_faq = deepcopy(faq)
    new_faq["mainEntity"].append({
        "@type": "Question",
        "@id": case["url"] + "#" + case["qid"],
        "name": case["q"],
        "acceptedAnswer": {
            "@type": "Answer",
            "@id": case["url"] + "#" + case["aid"],
            "text": case["a"],
        },
    })
    changed = (
        changed[:match.start(2)] +
        json.dumps(new_faq, ensure_ascii=False, separators=(",", ":")) +
        changed[match.end(2):]
    )

    # SEO safety: no changed titles, headings, link targets, canonical,
    # hreflang, meta tags, images, or script files.
    for pattern in (
        r"<title>.*?</title>", r"<h1\b[^>]*>.*?</h1>",
        r"<meta\b[^>]*>", r"<link\b[^>]*>",
        r"<a\b[^>]*>", r"<img\b[^>]*>",
    ):
        require(tag_list(original, pattern) == tag_list(changed, pattern),
                "unrelated page element changed in " + label + ": " + pattern)

    new_sections = list(FAQ_SECTION.finditer(changed))
    require(len(new_sections) == 1 and
            new_sections[0].group().count("<details") == 4,
            "visible FAQ count changed unexpectedly: " + label)
    require(changed.count(case["q"]) == 2 and changed.count(case["a"]) == 2,
            "new visible/structured FAQ mismatch: " + label)
    updated_nodes = schema_nodes(changed)
    require(len(updated_nodes) == 1, "extra FAQ schema found: " + label)
    updated = updated_nodes[0][1]
    require(updated["mainEntity"][:-1] == old_items, "original FAQs changed: " + label)
    require(updated["mainEntity"][-1]["name"] == case["q"] and
            updated["mainEntity"][-1]["acceptedAnswer"]["text"] == case["a"],
            "added FAQ content mismatch: " + label)

    # Reversibility: removing only the one new visible item and the one
    # new schema entity must yield the original page exactly, including
    # every line of all other content.
    reverted = changed.replace(snippet, "", 1)
    match, json_node = schema_nodes(reverted)[0]
    json_node["mainEntity"].pop()
    reverted = (
        reverted[:match.start(2)] +
        json.dumps(json_node, ensure_ascii=False, separators=(",", ":")) +
        reverted[match.end(2):]
    )
    original_match, original_node = faqs[0]
    reference = (
        original[:original_match.start(2)] +
        json.dumps(original_node, ensure_ascii=False, separators=(",", ":")) +
        original[original_match.end(2):]
    )
    require(reverted == reference, "unexpected changes outside two FAQs: " + label)
    return changed


def main():
    results = []
    for case in CASES:
        path = ROOT / case["path"]
        require(path.is_file(), "expected page missing: " + case["path"])
        old = path.read_text(encoding="utf-8")
        results.append((path, change(old, case)))
    for path, new_html in results:
        path.write_text(new_html, encoding="utf-8")
        print("PASS: approved QuestionFinder FAQ added to " + str(path))
    print("PASS: only two pre-approved FAQ changes; all metadata and links preserved")


if __name__ == "__main__":
    main()
