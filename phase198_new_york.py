"""Build the English concierge page for trips planned from New York."""
from html import escape
from pathlib import Path
import re
from string import Template
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from phase180_enhance import BASE, ROOT, SCRIPT_RE, schema_script, set_meta, set_title


SOURCE = Path(__file__).parent / "editorial-assets/new-york"
HUB = "/international-clients/"
ROUTE = "/new-york-to-ibiza-concierge/"
CANONICAL = BASE + ROUTE
TITLE = "Ibiza Concierge for Travelers from New York | Ibiza VIP Move"
DESCRIPTION = (
    "Arrange a private concierge in Ibiza from New York. Request villa options, a yacht day, "
    "chauffeurs or VIP reservations through one contact on the island."
)
PHOTO = "/assets/images/experience-villa-960.jpg"
UPDATED = "2026-11-06"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
IMAGE_NS = "http://www.google.com/schemas/sitemap-image/1.1"


def replace_once(html, pattern, replacement):
    updated, count = re.subn(pattern, lambda _: replacement, html, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Expected one match for {pattern}, found {count}")
    return updated


def page_schema():
    webpage = {
        "@type": "WebPage", "@id": CANONICAL + "#webpage", "url": CANONICAL,
        "name": TITLE, "description": DESCRIPTION, "inLanguage": "en", "dateModified": UPDATED,
        "isPartOf": {"@id": BASE + "/#website"}, "publisher": {"@id": BASE + "/#organization"},
        "about": {"@id": CANONICAL + "#service"}, "primaryImageOfPage": BASE + PHOTO,
    }
    service = {
        "@type": "Service", "@id": CANONICAL + "#service", "url": CANONICAL,
        "name": "Private concierge in Ibiza for travelers from New York",
        "areaServed": {"@type": "Place", "name": "Ibiza, Spain"},
        "provider": {"@id": BASE + "/#organization"},
    }
    trail = [("Home", "/"), ("International clients", HUB), ("New York", ROUTE)]
    breadcrumb = {
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": label, "item": BASE + path}
            for i, (label, path) in enumerate(trail, 1)
        ],
    }
    return "".join(schema_script({"@context": "https://schema.org", **node})
                   for node in (webpage, service, breadcrumb))


def render(hub):
    message = ("Hello Ibiza VIP Move, I’m planning an Ibiza stay from New York and would like a quote. "
               "Stay dates: __. Guests: __. Villa or hotel area: __. Services requested: __.")
    whatsapp = escape("https://wa.me/34600703303?" + urlencode({"text": message}), quote=True)
    main = Template((SOURCE / "main.html").read_text(encoding="utf-8")).substitute(whatsapp=whatsapp)
    css = (SOURCE / "page.css").read_text(encoding="utf-8")
    html = set_title(hub, TITLE)
    for attr, key, value in (
        ("name", "description", DESCRIPTION), ("property", "og:title", TITLE),
        ("name", "twitter:title", TITLE), ("property", "og:description", DESCRIPTION),
        ("name", "twitter:description", DESCRIPTION), ("property", "og:url", CANONICAL),
        ("property", "og:image", BASE + PHOTO), ("name", "twitter:image", BASE + PHOTO),
        ("itemprop", "image", BASE + PHOTO),
    ):
        html = set_meta(html, attr, key, value)
    html = replace_once(html, r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{CANONICAL}">')
    # Other editions of the hub are not translations of this page.
    html = re.sub(r'<link rel="alternate"[^>]*hreflang=[^>]+>', "", html)
    html = replace_once(html, r'<aside class="ivm-language-bar".*?</aside>', "")
    html = replace_once(html, r'<link rel="preload" as="image"[^>]*>', "")
    html = SCRIPT_RE.sub("", html)
    html = replace_once(html, r'</head>', page_schema() + f"<style>{css}</style></head>")
    html = replace_once(html, r'<main\b[^>]*>.*?</main>', main)
    # Use the same trip brief for the floating and mobile contacts as for the main CTA.
    return re.sub(r'href="https://wa\.me/34600703303(?:\?[^"]*)?"', f'href="{whatsapp}"', html)


def linked_hub(html):
    link = f'<a class="text-link" href="{ROUTE}">Planning an Ibiza stay from New York</a>'
    if link in html:
        return html
    paragraph_end = "clear communication and reliable execution on the island.</p>"
    return replace_once(html, re.escape(paragraph_end), paragraph_end + f"<p>{link}</p>")


def update_sitemaps():
    ET.register_namespace("", SITEMAP_NS)
    ET.register_namespace("image", IMAGE_NS)
    url_tag, loc_tag, date_tag = [f"{{{SITEMAP_NS}}}{key}" for key in ("url", "loc", "lastmod")]
    for name in ("sitemap.xml", "image-sitemap.xml"):
        tree = ET.parse(ROOT / name)
        root = tree.getroot()
        paths = (HUB, ROUTE) if name == "sitemap.xml" else (ROUTE,)
        for path in paths:
            matches = [e for e in root.findall(url_tag) if e.findtext(loc_tag) == BASE + path]
            if len(matches) > 1 or (path == HUB and not matches):
                raise ValueError(f"Unexpected {path} entries in {name}")
            if matches:
                entry = matches[0]
            else:
                entry = ET.SubElement(root, url_tag)
                ET.SubElement(entry, loc_tag).text = BASE + path
            if name == "sitemap.xml":
                date = entry.find(date_tag)
                if date is None:
                    date = ET.SubElement(entry, date_tag)
                date.text = max(date.text or "", UPDATED)
            else:
                image_tag = f"{{{IMAGE_NS}}}image"
                image_loc = f"{{{IMAGE_NS}}}loc"
                if entry.find(image_tag) is None:
                    ET.SubElement(ET.SubElement(entry, image_tag), image_loc).text = BASE + PHOTO
                elif entry.findtext(f"{image_tag}/{image_loc}") != BASE + PHOTO:
                    raise ValueError(f"Unexpected image for {CANONICAL}")
        tree.write(ROOT / name, encoding="utf-8", xml_declaration=True)


def build():
    hub_file = ROOT / HUB.strip("/") / "index.html"
    target = ROOT / ROUTE.strip("/") / "index.html"
    if target.is_file() and 'class="ny-stay"' not in target.read_text(encoding="utf-8"):
        raise ValueError(f"Existing page at {ROUTE} has another owner")
    hub = hub_file.read_text(encoding="utf-8")
    html = render(hub)
    linked = linked_hub(hub)
    if not (ROOT / PHOTO.lstrip("/")).is_file():
        raise ValueError(f"Missing approved hero image: {PHOTO}")
    target.parent.mkdir(exist_ok=True)
    target.write_text(html, encoding="utf-8")
    hub_file.write_text(linked, encoding="utf-8")
    update_sitemaps()
    print(f"Built {ROUTE} and linked it from {HUB}")


if __name__ == "__main__":
    build()
