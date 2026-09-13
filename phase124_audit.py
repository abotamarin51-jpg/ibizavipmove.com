"""Read-only audit for Black Book freshness integrity."""
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


def path_for(lang, slug):
    return f"/ibiza-intelligence/{slug}/" if lang == "en" else f"/{lang}/ibiza-intelligence/{slug}/"


def page(path):
    return ROOT / path.strip("/") / "index.html"


def sitemap_lastmods():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = {}
    for entry in ET.parse(ROOT / "sitemap.xml").getroot().findall("s:url", ns):
        loc = entry.find("s:loc", ns)
        lastmod = entry.find("s:lastmod", ns)
        if loc is not None and loc.text:
            out[loc.text.strip()] = lastmod.text.strip() if lastmod is not None and lastmod.text else None
    return out


def run():
    lastmods = sitemap_lastmods()
    checked = 0
    dated = 0
    undated = 0
    for lang in LANGS:
        for slug in SLUGS:
            path = path_for(lang, slug)
            target = page(path)
            if not target.is_file():
                raise SystemExit(f"Phase 124 audit article missing: {path}")
            canonical = BASE + path
            expected = lastmods.get(canonical)
            if canonical not in lastmods:
                raise SystemExit(f"Phase 124 audit sitemap entry missing: {canonical}")
            html = target.read_text(encoding="utf-8")
            articles = []
            for match in SCRIPT_RE.finditer(html):
                try:
                    data = json.loads(match.group(1))
                except Exception:
                    continue
                if isinstance(data, dict) and data.get("@type") == "Article" and data.get("url") == canonical:
                    articles.append(data)
            if len(articles) != 1:
                raise SystemExit(f"Phase 124 audit Article count wrong: {path} -> {len(articles)}")
            article = articles[0]
            if "datePublished" in article:
                raise SystemExit(f"Phase 124 audit must not invent publication date: {path}")
            metas = re.findall(r'<meta\s+property="article:modified_time"\s+content="([^"]+)"\s*/?>', html, re.I)
            if expected:
                if article.get("dateModified") != expected or metas != [expected]:
                    raise SystemExit(
                        f"Phase 124 audit freshness mismatch: {path} -> "
                        f"schema={article.get('dateModified')!r}, meta={metas}, sitemap={expected!r}"
                    )
                dated += 1
            else:
                if "dateModified" in article or metas:
                    raise SystemExit(
                        f"Phase 124 audit invented freshness on undated sitemap entry: {path} -> "
                        f"schema={article.get('dateModified')!r}, meta={metas}"
                    )
                undated += 1
            checked += 1
    if checked != 30:
        raise SystemExit(f"Phase 124 audit expected 30 notes, found {checked}")
    print(
        "PASS: Phase 124 audit — 30 Black Book Article pages mirror sitemap freshness exactly; "
        f"{dated} verified modified dates and {undated} intentionally undated pages"
    )


if __name__ == "__main__":
    run()
