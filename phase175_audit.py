from pathlib import Path
import re

ROOT = Path("_site")
TARGET = ROOT / "de" / "privatkoch-villa-staff-ibiza" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
CANONICAL = "https://ibizavipmove.com/de/privatkoch-villa-staff-ibiza/"
EVENT_URL = "/de/private-events-ibiza/"
HANDOFF = '<p class="ivm-concierge-continuity">Wenn Villa-Staff mit einem privaten Event oder Firmenevent verbunden ist: <a class="text-link" href="/de/private-events-ibiza/">Eventkoordination Ibiza ansehen →</a></p>'

text = TARGET.read_text(encoding="utf-8")
sitemap = SITEMAP.read_text(encoding="utf-8")

checks = {
    "German target language": '<html lang="de"' in text,
    "self canonical": f'<link rel="canonical" href="{CANONICAL}">' in text,
    "indexable robots": '<meta name="robots" content="index,follow,max-image-preview:large">' in text,
    "single event handoff": text.count(HANDOFF) == 1 and text.count(EVENT_URL) == 1,
    "existing concierge handoff preserved": '/de/privater-concierge-ibiza/">Privaten Concierge Ibiza ansehen' in text,
    "six head hreflang alternates": len(re.findall(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">', text, re.I)) == 6,
    "sitemap inventory preserved": sitemap.count("<url>") == 156,
    "truthful target lastmod": f"<loc>{CANONICAL}</loc><lastmod>2026-10-04</lastmod>" in sitemap,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Phase 175 audit failed: " + ", ".join(failed))

print("PASS: Phase 175 audit")
