"""Align Black Book Article freshness metadata with the sitemap's verified dates."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path("_site")
BASE = "https://ibizavipmove.com"
LANGS = ("en", "es", "fr", "de", "ar")
SLUGS = (
    "private-arrival",
    "ibiza-formentera-yacht-day",
    "ibiza-august-planning",
    "villa-arrival-planning",
    "nightlife-transport-planning",
    "private-aviation-ground-coordination",
)
SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)
MOD_META_RE = re.compile(r'<meta\s+property="article:modified_time"\s+content="[^"]*"\s*/?>', re.I)


def path_for(lang, slug):
    return f"/ibiza-intelligence/{slug}/" if lang == "en" else f"/{lang}/ibiza-intelligence/{slug}/"


def page(path):
    return ROOT / path.strip("/") / "index.html"


def sitemap_lastmods():
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        raise SystemExit("Phase 124 sitemap missing")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = {}
    for entry in ET.parse(sitemap).getroot().findall("s:url", ns):
        loc = entry.find("s:loc", ns)
        lastmod = entry.find("s:lastmod", ns)
        if loc is not None and loc.text:
            out[loc.text.strip()] = lastmod.text.strip() if lastmod is not None and lastmod.text else None
    return out


def rewrite_article_schema(html, canonical, lastmod):
    found = 0
    pieces = []
    pos = 0
    for match in SCRIPT_RE.finditer(html):
        pieces.append(html[pos:match.start()])
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            data = None
        if isinstance(data, dict) and data.get("@type") == "Article" and data.get("url") == canonical:
            found += 1
            if lastmod:
                data["dateModified"] = lastmod
            else:
                data.pop("dateModified", None)
            pieces.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>")
        else:
            pieces.append(match.group(0))
        pos = match.end()
    pieces.append(html[pos:])
    if found != 1:
        raise SystemExit(f"Phase 124 expected one Article schema for {canonical}, found {found}")
    return "".join(pieces)


def enhance():
    lastmods = sitemap_lastmods()
    touched = 0
    dated = 0
    undated = 0
    for lang in LANGS:
        for slug in SLUGS:
            path = path_for(lang, slug)
            target = page(path)
            if not target.is_file():
                raise SystemExit(f"Phase 124 article missing: {path}")
            canonical = BASE + path
            if canonical not in lastmods:
                raise SystemExit(f"Phase 124 sitemap entry missing: {canonical}")
            lastmod = lastmods[canonical]
            html = target.read_text(encoding="utf-8")
            html = rewrite_article_schema(html, canonical, lastmod)
            html = MOD_META_RE.sub("", html)
            if lastmod:
                html = html.replace("</head>", f'<meta property="article:modified_time" content="{lastmod}"></head>', 1)
                dated += 1
            else:
                undated += 1
            target.write_text(html, encoding="utf-8")
            touched += 1
    if touched != 30 or dated + undated != 30:
        raise SystemExit(f"Phase 124 cardinality mismatch: touched={touched}, dated={dated}, undated={undated}")
    print(
        "PASS: Phase 124 — Black Book Article freshness now follows verified sitemap lastmod values; "
        f"{dated} dated pages aligned and {undated} pages left without invented modified dates"
    )


if __name__ == "__main__":
    enhance()
