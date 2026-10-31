"""Read-only live-site release verification for Ibiza VIP Move's VIP Tables page.

Only GET specific public Ibiza VIP Move documents/assets. No JavaScript,
tracking, cookies, submitted forms, outbound contacts or third-party requests.
The report is operational evidence, NOT evidence of indexing or bookings.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
from html.parser import HTMLParser
from io import BytesIO
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zoneinfo import ZoneInfo

from PIL import Image

ORIGIN = "https://ibizavipmove.com"
PAGE = ORIGIN + "/vip-tables-club-access-ibiza/"
SOCIAL = ORIGIN + "/assets/images/vip-tables-social.jpg"
SOURCES = (
    "restaurants-nightlife-ibiza",
    "private-concierge-ibiza",
    "vip-services-ibiza",
    "private-chauffeur-ibiza",
)
MAX_HTML = 2_000_000
MAX_IMAGE = 3_000_000


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def valid_request(url, method="GET"):
    parsed = urlsplit(url)
    if (method != "GET" or parsed.scheme != "https" or parsed.netloc != "ibizavipmove.com"
            or parsed.username or parsed.password or parsed.fragment):
        return False
    allowed = {PAGE, SOCIAL} | {ORIGIN + "/" + slug + "/" for slug in SOURCES}
    if url in allowed:
        return True
    return (parsed.path.startswith("/assets/") and
            Path(parsed.path).suffix.lower() in {".css", ".js", ".jpg", ".jpeg", ".webp",
                                                 ".avif", ".png", ".svg", ".woff", ".woff2"}
            and len(parsed.query) < 80)


def get(url, expected_content_type, limit):
    if not valid_request(url):
        raise ValueError("URL is outside the public first-party GET allowlist")
    req = Request(url, headers={"User-Agent": "IbizaVIPMove-ReadOnlyProductionReview/1.0",
                                 "Accept": expected_content_type})
    with build_opener(NoRedirect()).open(req, timeout=18) as response:
        if response.status != 200 or response.url != url:
            raise ValueError("Expected nonredirected 200 for " + url)
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if content_type != expected_content_type:
            raise ValueError("Wrong content type for " + url + ": " + content_type)
        body = response.read(limit + 1)
    if not body or len(body) > limit:
        raise ValueError("Empty or oversize resource " + url)
    return body


class PageTags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = []
        self.robots = []
        self.og = []
        self.twitter = []
        self.h1_count = 0
        self.faq_count = 0
        self.in_main = False
        self.main_wa = []
        self.static_resources = []

    def handle_starttag(self, tag, attr_list):
        a = dict(attr_list)
        if tag == "main":
            self.in_main = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "details":
            self.faq_count += 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href"))
        if tag == "meta" and a.get("name") == "robots":
            self.robots.append(a.get("content"))
        if tag == "meta" and a.get("property") == "og:image":
            self.og.append(a.get("content"))
        if tag == "meta" and a.get("name") == "twitter:image":
            self.twitter.append(a.get("content"))
        if self.in_main and tag == "a" and a.get("href", "").startswith("https://wa.me/"):
            self.main_wa.append(a["href"])
        if tag == "script" and a.get("src", "").startswith("/assets/"):
            self.static_resources.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet" and a.get("href", "").startswith("/assets/"):
            self.static_resources.append(a["href"])
        if tag == "img" and a.get("src", "").startswith("/assets/"):
            self.static_resources.append(a["src"])

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False


def parse_page(body):
    html = body.decode("utf-8")
    tags = PageTags()
    tags.feed(html)
    if tags.canonical != [PAGE]:
        raise ValueError("Canonical is not the exact new page URL")
    if tags.robots != ["index,follow,max-image-preview:large"]:
        raise ValueError("Unexpected robots directive")
    if tags.og != [SOCIAL] or tags.twitter != [SOCIAL]:
        raise ValueError("Open Graph / Twitter image URL differs from approved asset")
    if tags.h1_count != 1 or tags.faq_count != 9:
        raise ValueError("H1/FAQ structure mismatch")
    if len(tags.main_wa) != 3 or any(urlsplit(u).path != "/34600703303" for u in tags.main_wa):
        raise ValueError("Main WhatsApp CTAs do not use the approved destination")
    for literal in ("[UNVRS]", "O Beach Ibiza", "Sant Antoni de Portmany",
                    "Last updated: 31 October 2026", "Terms before confirmation",
                    "not confirmed booking relationships",
                    "Can I change or cancel an Ibiza VIP table booking?"):
        if literal not in html:
            raise ValueError("Reviewed content not served: " + literal)
    for marker in ("[FECHA]", "[CONFIRMAR:", "[OPCIONAL:", "[PENDIENTE:",
                   "data-ivm180-placeholder", "Ocean Beach Ibiza</td>"):
        if marker in html:
            raise ValueError("Unresolved or superseded editorial content: " + marker)
    schemas = []
    for match in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S):
        node = json.loads(match.group(1))
        schemas.extend(node.get("@graph", []) if isinstance(node, dict) and "@graph" in node else [node])
    values = [n.get("@type") for n in schemas if isinstance(n, dict)]
    for kind in ("Organization", "WebSite", "WebPage", "Service", "BreadcrumbList", "FAQPage"):
        if values.count(kind) != 1:
            raise ValueError("Missing or duplicate schema type: " + kind)
    webpage = next(n for n in schemas if n.get("@type") == "WebPage")
    if webpage.get("dateModified") != "2026-10-31":
        raise ValueError("Unverified page modification date")
    return {"httpStatus": 200, "htmlSha256": hashlib.sha256(body).hexdigest(),
            "h1": tags.h1_count, "visibleFaqs": tags.faq_count,
            "whatsappLinks": len(tags.main_wa), "schemaTypes": values,
            "staticResources": list(dict.fromkeys(tags.static_resources))}


def self_test():
    for url in (PAGE, SOCIAL, ORIGIN + "/private-chauffeur-ibiza/"):
        assert valid_request(url)
    for url in ("https://example.com/", ORIGIN + "/contact/", ORIGIN + "/contact/?name=test",
                "https://wa.me/34600703303", ORIGIN + "/collect.gif", "http://ibizavipmove.com/"):
        assert not valid_request(url), url
    assert not valid_request(PAGE, method="POST")
    assert NoRedirect().redirect_request(None, None, 302, "", {}, ORIGIN) is None
    print("PASS: VIP Tables release check first-party GET-only policy", flush=True)


def check_live():
    report = {"checkedAt": datetime.now(ZoneInfo("Europe/Madrid")).isoformat(),
              "sourceCommit": os.environ.get("GITHUB_SHA"), "url": PAGE,
              "mode": "production_read_only", "status": "NOT_RUN",
              "limitations": ["Not a Google crawl or proof of ranking/indexing.",
                              "No external contact, form, Analytics event or completed booking."]}
    evidence_dir = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "ivm-dmc-context-review"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    try:
        page = get(PAGE, "text/html", MAX_HTML)
        report["page"] = parse_page(page)
        picture = get(SOCIAL, "image/jpeg", MAX_IMAGE)
        with Image.open(BytesIO(picture)) as img:
            if img.format != "JPEG" or img.size != (1200, 630):
                raise ValueError("Public social JPEG invalid")
        report["social"] = {"httpStatus": 200, "size": len(picture), "dimensions": [1200, 630],
                            "sha256": hashlib.sha256(picture).hexdigest()}
        inlinks = {}
        for slug in SOURCES:
            url = ORIGIN + "/" + slug + "/"
            source = get(url, "text/html", MAX_HTML).decode("utf-8")
            if source.count('data-ivm180="vip-tables-link"') != 1:
                raise ValueError("Missing or duplicated contextual link on " + url)
            if 'href="/vip-tables-club-access-ibiza/"' not in source:
                raise ValueError("Wrong internal link on " + url)
            inlinks[slug] = {"httpStatus": 200, "links": 1}
        report["inboundSources"] = inlinks
        resources = {}
        for path in report["page"]["staticResources"]:
            url = ORIGIN + path
            typ = "text/css" if path.split("?")[0].endswith(".css") else (
                  "application/javascript" if path.split("?")[0].endswith(".js") else
                  "image/jpeg" if path.split("?")[0].endswith(".jpg") else None)
            if typ:
                data = get(url, typ, MAX_IMAGE)
                resources[path] = {"httpStatus": 200, "bytes": len(data)}
        report["staticResources"] = resources
        report["status"] = "PASS"
    except Exception as error:
        report["status"] = "FAILED_OR_BLOCKED"
        report["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (evidence_dir / "vip-tables-served-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("VIP_TABLES_PRODUCTION_REPORT " + json.dumps(report, ensure_ascii=False), flush=True)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    if args.production:
        check_live()
