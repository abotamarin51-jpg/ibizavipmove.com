"""Add a localized origin selector to each existing international hub."""
import csv
from html import escape
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from zoneinfo import ZoneInfo

from phase180_enhance import ROOT

ASSETS = Path(__file__).parent / "editorial-assets/origin-planner"
WA = "https://wa.me/34600703303"
START = "<!-- origin planner start -->"
END = "<!-- origin planner end -->"


def slug(city):
    letters = unicodedata.normalize("NFKD", city).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", letters).strip("-")


def read_cities():
    groups = {}
    with (ASSETS / "regions.tsv").open(encoding="utf-8", newline="") as source:
        regions = {r["code"]: r for r in csv.DictReader(source, delimiter="\t")}
    with (ASSETS / "cities.tsv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            code, country, city, zone = (row[k] for k in ("country_code", "country", "city", "timezone"))
            ZoneInfo(zone)
            group = groups.setdefault(code, {"names": {"en": country, **regions[code]}, "cities": {}})
            key = slug(city)
            if group["names"]["en"] != country or not key or key in group["cities"]:
                raise ValueError(f"Ambiguous origin in {country}: {city}")
            names = {"en": city, **{lang: row[lang] for lang in ("es", "fr", "de", "ar")}}
            if not all(names.values()):
                raise ValueError(f"Missing city name for {city}")
            group["cities"][key] = (names, zone)
    if groups.keys() != regions.keys():
        raise ValueError("Country inventory and localized names disagree")
    return groups


def without_planner(html):
    html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)
    html = re.sub(r'<style data-origin-planner>.*?</style>', "", html, flags=re.S)
    return re.sub(r'<script defer data-origin-planner src="[^"]+"></script>', "", html)


def planner_html(language, copy, groups, markets):
    countries = []
    cities = []
    for code, group in sorted(groups.items(), key=lambda pair: pair[1]["names"][language]):
        name = escape(group["names"][language])
        countries.append(f'<option value="{code}">{name}</option>')
        options = "".join(f'<option value="{key}" data-zone="{escape(zone)}">{escape(names[language])}</option>'
                          for key, (names, zone) in sorted(group["cities"].items(), key=lambda pair: pair[1][0][language]))
        cities.append(f'<optgroup data-country="{code}" label="{name}">{options}</optgroup>')
    service_options = "".join(f'<option>{escape(name)}</option>' for name in copy["services"])
    city_names = {key: names[language] for group in groups.values() for key, (names, _) in group["cities"].items()}
    guides = "".join(f'<a hreflang="{m.language}" href="{m.route}">{escape(city_names[slug(m.city)])} '
                     f'<small aria-hidden="true">{m.language.upper()}</small></a>' for m in markets)
    t = {k: escape(v, quote=True) for k, v in copy.items() if isinstance(v, str)}
    return f"""{START}<section id="origin-planner" aria-labelledby="origin-title" data-message="{t['message']}">
<div class="origin-layout"><div><h2 id="origin-title">{t['heading']}</h2><p>{t['intro']}</p>
<nav class="origin-guides" aria-label="{t['guides']}"><span>{t['guides']}</span>{guides}</nav></div>
<div><div class="origin-fields" hidden>
<label>{t['country']}<select id="origin-country"><option value="">{t['choose']}</option>{''.join(countries)}<option value="other">{t['otherCountry']}</option></select></label>
<label>{t['city']}<select id="origin-city" disabled><option value="">{t['whole']}</option><option value="other">{t['otherCity']}</option>{''.join(cities)}</select></label>
<label class="origin-wide" hidden>{t['custom']}<input id="origin-custom" type="text" maxlength="100" dir="auto"></label>
<label class="origin-wide">{t['service']}<select id="origin-service">{service_options}</select></label>
<div class="origin-clocks"><span id="origin-local-clock" hidden>{t['local']}<strong></strong></span><span>{t['ibiza']}<strong id="origin-ibiza-time"></strong></span></div>
</div><div class="origin-actions"><a class="origin-primary" id="origin-whatsapp" href="{WA}">{t['action']}</a>
<a href="{t['contact']}">{t['form']}</a></div>
<div class="origin-share" hidden><button id="origin-share" type="button" data-copied="{t['copied']}">{t['share']}</button>
<span id="origin-share-status" role="status"></span>
<label hidden>{t['copyManually']}<input id="origin-share-url" type="text" dir="ltr" readonly></label></div></div></div></section>{END}"""


def add_planners(markets):
    groups = read_cities()
    translations = json.loads((ASSETS / "languages.json").read_text(encoding="utf-8"))
    css = (ASSETS / "planner.css").read_text(encoding="utf-8")
    js = (ASSETS / "planner.js").read_bytes()
    digest = hashlib.sha256(js).hexdigest()[:12]
    asset = f"/assets/origin-planner-{digest}.js"
    (ROOT / asset.lstrip("/")).write_bytes(js)
    paths = []
    for language, copy in translations.items():
        path = ROOT / copy["path"] / "index.html"
        html = without_planner(path.read_text(encoding="utf-8"))
        if f'<html lang="{language}"' not in html or not (ROOT / copy["contact"].strip("/") / "index.html").is_file():
            raise ValueError(f"Unexpected hub or contact destination for {language}")
        start = html.index("<main")
        boundary = html.index("</section>", start) + len("</section>")
        html = html[:boundary] + planner_html(language, copy, groups, markets) + html[boundary:]
        html = html.replace("</head>", f"<style data-origin-planner>{css}</style></head>", 1)
        html = html.replace("</body>", f'<script defer data-origin-planner src="{asset}"></script></body>', 1)
        path.write_text(html, encoding="utf-8")
        paths.append("/" + copy["path"] + "/")
    return paths
