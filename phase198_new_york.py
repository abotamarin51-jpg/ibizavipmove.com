"""Build the origin concierge pages and connect them to the five international hubs."""
from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
from string import Template
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from phase180_enhance import BASE, ROOT, SCRIPT_RE, schema_script, set_meta, set_title
from phase199_origin_planner import add_planners, slug, without_planner

ASSETS = Path(__file__).parent / "editorial-assets"
HUB = "/international-clients/"
UPDATED = "2026-11-06"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
IMAGE_NS = "http://www.google.com/schemas/sitemap-image/1.1"


@dataclass(frozen=True)
class Market:
    city: str
    description: str
    photo: str
    requests: tuple = ()
    language: str = "en"
    path: str = ""
    page_title: str = ""

    @property
    def route(self):
        return self.path or "/" + slug(self.city) + "-to-ibiza-concierge/"

    @property
    def title(self):
        return self.page_title or f"Ibiza Concierge for Travelers from {self.city} | Ibiza VIP Move"

    @property
    def hub(self):
        return {"en": HUB, "fr": "/fr/clients-internationaux/"}[self.language]


MARKETS = (
    Market("New York",
           "Arrange a private concierge in Ibiza from New York. Request villa options, a yacht day, "
           "chauffeurs or VIP reservations through one contact on the island.",
           "/assets/images/experience-villa-960.jpg"),
    Market("Miami",
           "Plan a private Ibiza stay from Miami. Request a villa, yacht charter, marina transfers "
           "and dining reservations, or coordinate shore arrangements with your captain.",
           "/assets/images/experience-yacht-960.jpg",
           (("marina", "I’m planning from Miami and already have a yacht in Ibiza. Marina and date: __. Guests: __. Shore arrangements: __."),
            ("charter", "I’m planning from Miami and would like a yacht charter and transfers in Ibiza. Date: __. Guests: __. Preferred route: __."))),
    Market("Dubai",
           "Arrange a private concierge in Ibiza from Dubai. Plan a family villa, private staff, "
           "chauffeurs and reservations with one island contact for guests and assistants.",
           "/assets/images/experience-villa-960.jpg",
           (("family", "I’m planning a family stay in Ibiza from Dubai. Dates: __. Group size: __. Villa, staff or chauffeur needs: __."),
            ("office", "I’m coordinating an Ibiza itinerary from a Dubai office. Dates: __. Priorities: __. Approval contact: __."))),
    Market("London",
           "Plan a private Ibiza weekend from London. Arrange a chauffeur, a Formentera yacht day, "
           "dinner and late-night returns around your arrival and flight home.",
           "/assets/images/experience-nightlife-960.jpg",
           page_title="Ibiza Concierge for a Weekend from London | Ibiza VIP Move"),
    Market("Paris",
           "Organisez votre séjour à Ibiza depuis Paris. Demandez un devis en français pour un dîner "
           "en villa, un chef privé, une journée en yacht ou les trajets de vos invités.",
           "/assets/images/experience-villa-960.jpg", language="fr",
           path="/fr/conciergerie-ibiza-depuis-paris/",
           page_title="Conciergerie privée à Ibiza depuis Paris | Ibiza VIP Move"),
)


def replace_once(html, pattern, replacement):
    updated, count = re.subn(pattern, lambda _: replacement, html, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Expected one match for {pattern}, found {count}")
    return updated


def page_schema(market):
    canonical = BASE + market.route
    webpage = {
        "@type": "WebPage", "@id": canonical + "#webpage", "url": canonical,
        "name": market.title, "description": market.description, "inLanguage": market.language, "dateModified": UPDATED,
        "isPartOf": {"@id": BASE + "/#website"}, "publisher": {"@id": BASE + "/#organization"},
        "about": {"@id": canonical + "#service"}, "primaryImageOfPage": BASE + market.photo,
    }
    service = {
        "@type": "Service", "@id": canonical + "#service", "url": canonical,
        "name": f"Private concierge in Ibiza for travelers from {market.city}",
        "areaServed": {"@type": "Place", "name": "Ibiza, Spain"},
        "provider": {"@id": BASE + "/#organization"},
    }
    if market.language == "fr":
        service["name"] = f"Conciergerie privée à Ibiza depuis {market.city}"
        trail = [("Accueil", "/fr/"), ("Clients internationaux", market.hub), (market.city, market.route)]
    else:
        trail = [("Home", "/"), ("International clients", market.hub), (market.city, market.route)]
    breadcrumb = {
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": label, "item": BASE + path}
            for i, (label, path) in enumerate(trail, 1)
        ],
    }
    return "".join(schema_script({"@context": "https://schema.org", **node})
                   for node in (webpage, service, breadcrumb))


def whatsapp(message):
    return escape("https://wa.me/34600703303?" + urlencode({"text": message}), quote=True)


def render(hub, market):
    canonical = BASE + market.route
    message = (f"Hello Ibiza VIP Move, I’m planning an Ibiza stay from {market.city} and would like a quote. "
               "Stay dates: __. Guests: __. Villa or hotel area: __. Services requested: __.")
    if market.language == "fr":
        message = (f"Bonjour Ibiza VIP Move. J’organise un séjour à Ibiza depuis {market.city} et je souhaite "
                   "un devis. Dates : __. Nombre de personnes : __. Lieu du séjour : __. Services demandés : __.")
    default_wa = whatsapp(message)
    requests = {key: whatsapp("Hello Ibiza VIP Move. " + text) for key, text in market.requests}
    template = ASSETS / slug(market.city) / "main.html"
    main = Template(template.read_text(encoding="utf-8")).substitute(whatsapp=default_wa, **requests)
    css = (ASSETS / "new-york/page.css").read_text(encoding="utf-8")
    if market.requests:
        css += (ASSETS / "origin-planner/requests.css").read_text(encoding="utf-8")
    html = set_title(hub, market.title)
    for attr, key, value in (
        ("name", "description", market.description), ("property", "og:title", market.title),
        ("name", "twitter:title", market.title), ("property", "og:description", market.description),
        ("name", "twitter:description", market.description), ("property", "og:url", canonical),
        ("property", "og:image", BASE + market.photo), ("name", "twitter:image", BASE + market.photo),
        ("itemprop", "image", BASE + market.photo),
    ):
        html = set_meta(html, attr, key, value)
    html = replace_once(html, r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}">')
    html = re.sub(r'<link rel="alternate"[^>]*hreflang=[^>]+>', "", html)
    html = replace_once(html, r'<aside class="ivm-language-bar".*?</aside>', "")
    html = replace_once(html, r'<link rel="preload" as="image"[^>]*>', "")
    html = SCRIPT_RE.sub("", html)
    html = replace_once(html, r'</head>', page_schema(market) + f"<style>{css}</style></head>")
    # The shared controls use the default brief. The main section can also offer specific requests.
    html = re.sub(r'href="https://wa\.me/34600703303(?:\?[^"]*)?"', f'href="{default_wa}"', html)
    return replace_once(html, r'<main\b[^>]*>.*?</main>', main)


def linked_hub(html):
    # Retain the original contextual New York link as well as the selector's three guide links.
    link = f'<a class="text-link" href="{MARKETS[0].route}">Planning an Ibiza stay from New York</a>'
    if link in html:
        return html
    paragraph_end = "clear communication and reliable execution on the island.</p>"
    return replace_once(html, re.escape(paragraph_end), paragraph_end + f"<p>{link}</p>")


def update_sitemaps(hub_paths):
    ET.register_namespace("", SITEMAP_NS)
    ET.register_namespace("image", IMAGE_NS)
    url_tag, loc_tag, date_tag = [f"{{{SITEMAP_NS}}}{key}" for key in ("url", "loc", "lastmod")]
    photos = {market.route: market.photo for market in MARKETS}
    for name in ("sitemap.xml", "image-sitemap.xml"):
        tree = ET.parse(ROOT / name)
        root = tree.getroot()
        paths = [*hub_paths, *photos] if name == "sitemap.xml" else list(photos)
        for path in paths:
            matches = [e for e in root.findall(url_tag) if e.findtext(loc_tag) == BASE + path]
            if len(matches) > 1 or (path in hub_paths and not matches):
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
                image_url = BASE + photos[path]
                if entry.find(image_tag) is None:
                    ET.SubElement(ET.SubElement(entry, image_tag), image_loc).text = image_url
                elif entry.findtext(f"{image_tag}/{image_loc}") != image_url:
                    raise ValueError(f"Unexpected sitemap image for {path}")
        tree.write(ROOT / name, encoding="utf-8", xml_declaration=True)


def build():
    hub_file = ROOT / HUB.strip("/") / "index.html"
    hub = without_planner(hub_file.read_text(encoding="utf-8"))
    for market in MARKETS:
        target = ROOT / market.route.strip("/") / "index.html"
        if target.is_file() and 'class="ny-stay"' not in target.read_text(encoding="utf-8"):
            raise ValueError(f"Existing page at {market.route} has another owner")
        if not (ROOT / market.photo.lstrip("/")).is_file():
            raise ValueError(f"Missing approved hero image: {market.photo}")
        template = without_planner((ROOT / market.hub.strip("/") / "index.html").read_text(encoding="utf-8"))
        if f'<html lang="{market.language}"' not in template:
            raise ValueError(f"Wrong template language for {market.city}")
        html = render(template, market)
        target.parent.mkdir(exist_ok=True)
        target.write_text(html, encoding="utf-8")
    hub_file.write_text(linked_hub(hub), encoding="utf-8")
    hub_paths = add_planners(MARKETS)
    update_sitemaps(hub_paths)
    print(f"Built {len(MARKETS)} origin guides and localized planning tools on {len(hub_paths)} international hubs")


if __name__ == "__main__":
    build()
