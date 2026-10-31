"""Publish the 24 approved English FAQs on their existing service pages.

Copy approved by Juan from Ibiza_VIP_Move_FAQs_EN_2026-10-31.txt (31 October).
Only the customer-facing questions and answers belong in the generated site.
"""
from copy import deepcopy
from html import escape, unescape
from pathlib import Path
import json
import re

BASE = "https://ibizavipmove.com"
ORG = BASE + "/#organization"
LASTMOD = "2026-10-31"
SCRIPT = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.S | re.I)
SECTION = re.compile(r'<section\b[^>]*class="(?:faq|ivm-service-faq)"[^>]*>.*?</section>', re.S | re.I)
DETAIL = re.compile(r'<details\b[^>]*>.*?</details>', re.S | re.I)
FAQS = {
    "/private-concierge-ibiza/": [
        [
            "What does a luxury concierge in Ibiza arrange?",
            "Our Ibiza concierge services coordinate private chauffeurs, villas, yachts, restaurant reservations, beach clubs and VIP tables, alongside private aviation support, security and villa staffing. You can request one service or combine several through one local point of contact, with availability and scope confirmed for your stay."
        ],
        [
            "How do I book Ibiza VIP services for my stay?",
            "Contact our VIP concierge in Ibiza through WhatsApp on +34 600 703 303 or the contact form. Include your dates, group size, accommodation and requested services. You can message at any time; we check availability and provide pricing and terms before confirming your booking."
        ],
        [
            "How much does a luxury concierge service in Ibiza cost?",
            "Pricing depends on the services requested, travel dates, group size and coordination required. Share your itinerary and priorities for a tailored proposal. The proposal should set out the included services, any applicable concierge fees and additional costs before confirmation."
        ],
        [
            "Can I change or cancel Ibiza concierge services after booking?",
            "Changes and cancellations depend on the booked service and the terms accepted at confirmation. Contact us as soon as possible so we can review the options and any applicable charges. If a change affects several services, we will also review the connected timings and reservations."
        ]
    ],
    "/private-chauffeur-ibiza/": [
        [
            "Can I book an hourly chauffeur service in Ibiza?",
            "Yes. You can request a private chauffeur in Ibiza by the hour, for a full day or across several days. Your itinerary can include villas, hotels, marinas, restaurants and clubs. Share your schedule, passengers and luggage so we can confirm availability, minimum booking duration and pricing."
        ],
        [
            "Do you arrange a VIP airport transfer in Ibiza to a villa or hotel?",
            "Yes. Our airport chauffeur service connects Ibiza Airport with villas, hotels and other agreed destinations on the island. Send your flight number, date, passenger count, luggage details and destination address. The meeting point and waiting arrangements are clarified before travel."
        ],
        [
            "Which vehicles can I request for a luxury chauffeur service in Ibiza?",
            "You can enquire about Mercedes-Benz V-Class vehicles for private transfers and Mercedes-Benz Sprinters for groups. For an executive chauffeur service, share the passenger count, luggage and schedule so we can assess the right vehicle. The model, capacity and availability are confirmed for your booking."
        ],
        [
            "How much does a private driver or private car service in Ibiza cost?",
            "The price depends on the date, route, vehicle and service duration. For a transfer, send your pickup point, destination and time; for an hourly booking, share the planned itinerary. Your proposal should clarify taxes, waiting time and any additional hours before the service is confirmed."
        ],
        [
            "Can I book VIP transportation in Ibiza after a club?",
            "Yes. Late-night and early-morning VIP transfers can be requested, subject to availability and advance confirmation. We coordinate the meeting point, pickup time and return to your accommodation. If guests expect to leave at different times, tell us when booking so the necessary vehicles can be planned."
        ]
    ],
    "/luxury-villas-ibiza/": [
        [
            "How can a luxury villa concierge in Ibiza help me find a property?",
            "Send your dates, guest count, bedroom requirements, preferred area and budget. Include any privacy, accessibility or in-villa service needs. Our Ibiza villa concierge service reviews suitable options against your requirements, with availability and terms clarified before a reservation is made."
        ],
        [
            "Can I book luxury villas in Ibiza with concierge and private staff?",
            "Yes. Villa guest services can include the coordination of private chefs, chauffeur transport and housekeeping, subject to availability. Share the dates, guest count, meals and service hours needed. Each proposal should specify staff duties and included expenses, such as food shopping, transport and additional hours."
        ],
        [
            "Can I book villa guest services in Ibiza if I already have accommodation?",
            "Yes. We can coordinate transport, reservations, yachts and requested services around an existing villa stay. For services inside the property, access and property conditions need to be agreed with the person responsible for the accommodation. You do not also need to request villa sourcing."
        ]
    ],
    "/yacht-charter-ibiza/": [
        [
            "Can I book a private yacht charter from Ibiza to Formentera?",
            "Yes. We can help plan an Ibiza yacht charter for a day on the water with a route towards Formentera. Share your date, group size, budget and preferences. The vessel, departure port, duration and itinerary are confirmed according to availability and operating conditions."
        ],
        [
            "What is included in a luxury yacht charter in Ibiza?",
            "Inclusions depend on the vessel and proposal. Before booking, check whether crew, fuel, drinks, catering, taxes and other expenses are included. Charter offers differ, so the applicable inclusions and additional charges should be stated in your proposal."
        ],
        [
            "Can you combine Ibiza yacht rental with transfers from my villa or hotel?",
            "Yes. We can coordinate chauffeur transfers to the marina and back to your accommodation alongside the yacht booking. We confirm the port, boarding point and schedule to align the transfers. Restaurant or catering requests for the same day can also be reviewed."
        ]
    ],
    "/restaurants-nightlife-ibiza/": [
        [
            "How does VIP table booking in Ibiza work?",
            "Send the date, club or event, number of guests and approximate budget. We review your request and the available options. Table location, minimum spend, deposit and entry conditions depend on the venue and are clarified before confirmation. Chauffeur transport can be coordinated around the confirmed booking."
        ],
        [
            "Can an Ibiza concierge arrange last-minute restaurant and beach club bookings?",
            "We can review last-minute requests subject to venue availability. Send the date, preferred time, guest count and preferences, including alternatives if you are flexible. For beach clubs, specify whether you would like a restaurant table, daybed or cabana so the request can be assessed accurately."
        ],
        [
            "Does a VIP nightlife concierge in Ibiza guarantee club entry or a table?",
            "A request alone does not confirm a booking or guarantee entry. Acceptance depends on the venue, availability and its terms. We distinguish between requested and confirmed arrangements, communicate the applicable requirements and coordinate transport if needed."
        ]
    ],
    "/private-aviation-ibiza/": [
        [
            "Can you arrange ground transport for a private jet charter to Ibiza?",
            "Yes. Our private aviation concierge in Ibiza coordinates ground transport, luggage requirements and arrival at your villa, hotel or marina around your flight. Send the schedule, passenger count and authorised contact for changes. Flight operations, airport handling and access remain subject to the relevant providers and procedures."
        ],
        [
            "What happens to private jet ground transportation in Ibiza if my flight time changes?",
            "Share the revised schedule with your Ibiza VIP Move contact. Our private aviation ground coordination connects the updated flight time with your pickup, villa access and onward movements. Changes remain subject to availability and the terms of each confirmed service."
        ]
    ],
    "/private-security-ibiza/": [
        [
            "How can I request a bodyguard or close protection in Ibiza?",
            "Send your dates, locations and the support needed for your stay, event or specific movements. We assess private security and close-protection requests against the itinerary. The team and service scope are defined after reviewing the requirements and availability."
        ],
        [
            "Can private security in Ibiza be coordinated with chauffeurs, villas and events?",
            "Yes. Security requests can be coordinated with transport, accommodation, dining, events and private aviation. Confirmed services work around the same itinerary. Scope and access arrangements are reviewed for each location and type of service."
        ]
    ],
    "/private-office/": [
        [
            "How does your Ibiza concierge for family offices support private stays?",
            "Our Ibiza concierge for personal assistants, executive assistants and family-office teams provides one local contact for travel coordination. Share the dates, required services, time zone and booking approval contact. We can keep operational communication through the designated representative. This covers stay coordination, not financial or wealth-management advice."
        ],
        [
            "Can you act as an Ibiza concierge partner for luxury travel advisors?",
            "Yes. We coordinate Ibiza ground services for travel advisors and international concierges. Send the dates, traveller count and requested services to partnership@ibizavipmove.com. We agree how client communication will be handled and confirm the commercial terms for the collaboration before bookings are finalised."
        ]
    ]
}


def require(condition, message):
    if not condition:
        raise ValueError("Approved English FAQs: " + message)


def visible_items(section):
    items = []
    for detail in DETAIL.finditer(section):
        q = re.search(r"<summary\b[^>]*>(.*?)</summary>", detail.group(), re.S | re.I)
        a = re.search(r"<p\b[^>]*>(.*?)</p>", detail.group(), re.S | re.I)
        require(q is not None and a is not None, "malformed visible answer")
        clean = lambda value: re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]*>", " ", value))).strip()
        items.append([clean(q.group(1)), clean(a.group(1))])
    return items


def script(node):
    return '<script type="application/ld+json">' + json.dumps(node, ensure_ascii=False).replace("<", "\\u003c") + "</script>"


def transform(html, route):
    canonical = BASE + route
    items = FAQS[route]
    require(html.count(f'<link rel="canonical" href="{canonical}">') == 1, "canonical: " + route)
    require('<html lang="en"' in html, "English route: " + route)
    nodes = [json.loads(m.group(1)) for m in SCRIPT.finditer(html)]
    webpages = [n for n in nodes if n.get("@type") == "WebPage"]
    services = [n for n in nodes if n.get("@type") == "Service"]
    faqs = [n for n in nodes if n.get("@type") == "FAQPage"]
    require(len(webpages) == 1 and webpages[0].get("url") == canonical, "WebPage: " + route)
    require(len(services) <= 1 and len(faqs) <= 1, "duplicate entities: " + route)
    sections = list(SECTION.finditer(html))
    if len(sections) == 2 and route not in ("/private-concierge-ibiza/", "/private-office/"):
        # The core English pages also have an older, unstructured four-answer
        # block. Consolidate it into the approved service FAQ instead of leaving
        # two sections answering the same booking questions.
        legacy = [m for m in sections if 'class="faq"' in m.group()]
        primary = [m for m in sections if 'class="ivm-service-faq"' in m.group()]
        require(len(legacy) == len(primary) == 1, "legacy FAQ selection: " + route)
        require(len(visible_items(legacy[0].group())) == 4, "legacy FAQ content: " + route)
        require(not re.search(r'<(?:a|img|script)\b', legacy[0].group(), re.I),
                "legacy FAQ contains independent links/assets: " + route)
        html = html[:legacy[0].start()] + html[legacy[0].end():]
        sections = list(SECTION.finditer(html))
    require(len(sections) == len(faqs) <= 1, "FAQ section/entity count: " + route)
    if sections:
        section = sections[0].group()
        details = list(DETAIL.finditer(section))
        require(bool(details), "empty existing FAQ: " + route)
        recorded = [[q["name"], q["acceptedAnswer"]["text"]] for q in faqs[0]["mainEntity"]]
        require(visible_items(section) == recorded, "existing text/schema mismatch: " + route)
        section = section[:details[0].start()] + "APPROVED_ITEMS" + section[details[-1].end():]
        if 'id="faq"' not in section:
            section = section.replace("<section ", '<section id="faq" ', 1)
    else:
        require(route == "/private-office/", "unexpected missing FAQ: " + route)
        section = (
            '<section class="faq" id="faq" aria-label="Private Office questions">'
            '<div class="section-head"><div class="kicker dark">Private Office FAQ</div>'
            '<h2>Concierge support for your Ibiza stay.</h2></div>APPROVED_ITEMS</section>'
        )
    details_html = "".join(
        f'<details id="faq-question-{i}"><summary>{escape(q)}</summary>'
        f'<p id="faq-answer-{i}">{escape(a)}</p></details>'
        for i, (q, a) in enumerate(items, 1)
    )
    section = section.replace("APPROVED_ITEMS", details_html, 1)
    if sections:
        html = html[:sections[0].start()] + section + html[sections[0].end():]
    else:
        anchor = '<section class="ivm-b2b-cta">'
        require(html.count(anchor) == 1, "Private Office insertion point")
        html = html.replace(anchor, section + anchor, 1)

    webpage = deepcopy(webpages[0])
    webpage.setdefault("@id", canonical + "#webpage")
    faq_id = faqs[0].get("@id", canonical + "#faq") if faqs else canonical + "#faq"
    parts = webpage.get("hasPart", [])
    if isinstance(parts, dict):
        parts = [parts]
    webpage["hasPart"] = [p for p in parts if p.get("@id") != faq_id] + [{"@id": faq_id}]
    subject_id = services[0].get("@id") if services else None
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage", "@id": faq_id,
        "url": canonical + "#faq", "inLanguage": "en",
        "isPartOf": {"@id": webpage["@id"]},
        "about": {"@id": subject_id or webpage["@id"]},
        "publisher": {"@id": ORG},
        "mainEntity": [
            {"@type": "Question", "@id": canonical + f"#faq-question-{i}", "name": q,
             "acceptedAnswer": {"@type": "Answer", "@id": canonical + f"#faq-answer-{i}", "text": a}}
            for i, (q, a) in enumerate(items, 1)
        ],
    }

    def replace(match):
        node = json.loads(match.group(1))
        if node.get("@type") == "WebPage":
            return script(webpage)
        if node.get("@type") == "FAQPage":
            return script(faq)
        return match.group()
    html = SCRIPT.sub(replace, html)
    if not faqs:
        require(html.count("</head>") == 1, "head landmark: " + route)
        html = html.replace("</head>", script(faq) + "</head>", 1)
    return html


def audit(root=Path("_site")):
    total = 0
    for route, expected in FAQS.items():
        canonical = BASE + route
        html = (root / route.strip("/") / "index.html").read_text(encoding="utf-8")
        sections = list(SECTION.finditer(html))
        require(len(sections) == 1, "one visible FAQ section: " + route)
        require(visible_items(sections[0].group()) == expected, "approved visible copy: " + route)
        ids = re.findall(r'\bid="([^"]+)"', html)
        require(len(ids) == len(set(ids)), "unique HTML IDs: " + route)
        nodes = [json.loads(m.group(1)) for m in SCRIPT.finditer(html)]
        faqs = [n for n in nodes if n.get("@type") == "FAQPage"]
        require(len(faqs) == 1, "one FAQPage: " + route)
        faq = faqs[0]
        actual = [[q["name"], q["acceptedAnswer"]["text"]] for q in faq["mainEntity"]]
        require(actual == expected, "approved structured copy: " + route)
        require(faq["inLanguage"] == "en", "FAQ language: " + route)
        webpage = next(n for n in nodes if n.get("@type") == "WebPage")
        require({"@id": faq["@id"]} in webpage["hasPart"], "WebPage relationship: " + route)
        require(faq["isPartOf"] == {"@id": webpage["@id"]}, "FAQ relationship: " + route)
        for i, item in enumerate(faq["mainEntity"], 1):
            for entity, identifier in ((item, f"faq-question-{i}"), (item["acceptedAnswer"], f"faq-answer-{i}")):
                require(identifier in ids and entity["@id"] == canonical + "#" + identifier, "fragment: " + route)
        total += len(expected)
    require(total == 24 and len(FAQS) == 8, "24 answers across eight English pages")
    print("PASS: Approved English FAQs — 24 exact visible answers and matching JSON-LD across eight pages")


def enhance(root=Path("_site")):
    pending = []
    for route in FAQS:
        path = root / route.strip("/") / "index.html"
        original = path.read_text(encoding="utf-8")
        updated = transform(original, route)
        require(SCRIPT.sub("", original.split("</head>")[0]) == SCRIPT.sub("", updated.split("</head>")[0]),
                "unrelated metadata changed: " + route)
        for pattern in (r"<h1\b.*?</h1>", r"<a\b[^>]*>", r"<img\b[^>]*>",
                        r'<script\b(?!\s+type="application/ld\+json")[^>]*>.*?</script>'):
            require(re.findall(pattern, original, re.S | re.I) == re.findall(pattern, updated, re.S | re.I),
                    "unrelated page element changed: " + route)
        pending.append((path, updated))
    sitemap_path = root / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    for route in FAQS:
        pattern = rf"(<url>\s*<loc>{re.escape(BASE + route)}</loc>\s*<lastmod>)[^<]+(</lastmod>)"
        sitemap, count = re.subn(pattern, rf"\g<1>{LASTMOD}\g<2>", sitemap)
        require(count == 1, "existing sitemap entry: " + route)
    for path, updated in pending:
        path.write_text(updated, encoding="utf-8")
    sitemap_path.write_text(sitemap, encoding="utf-8")
    audit(root)


if __name__ == "__main__":
    enhance()

