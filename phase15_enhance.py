from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
TODAY = '2026-09-02'
INDEXNOW_KEY = '5be4dcbeb9a5378b495d37e469e1b27f'

# Keep robots intentionally simple: a site-wide Allow already covers standard and AI crawlers.
robots = ROOT / 'robots.txt'
robots.write_text(
    'User-agent: *\n'
    'Allow: /\n'
    f'Sitemap: {BASE}/sitemap.xml\n',
    encoding='utf-8'
)

# Accurate discovery metadata for this release. All pages are rebuilt in the current deployment.
sitemap = ROOT / 'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
tree = ET.parse(sitemap)
root = tree.getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
for url in root.findall('sm:url', ns):
    lastmod = url.find('sm:lastmod', ns)
    if lastmod is None:
        lastmod = ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
    lastmod.text = TODAY
tree.write(sitemap, encoding='utf-8', xml_declaration=True)

# Refresh the machine-readable brand summary. This is supplementary; normal HTML remains source of truth.
llms = ROOT / 'llms.txt'
llms.write_text(f'''# Ibiza VIP Move

> Ibiza VIP Move is a private concierge, chauffeur and luxury lifestyle management service in Ibiza, Spain.
> Last updated: {TODAY}.

Official website: {BASE}/
Phone: +34 600 703 303
Email: partnership@ibizavipmove.com

## Primary pages
- [Home]({BASE}/)
- [Luxury Concierge Services]({BASE}/services/)
- [Private Concierge Ibiza]({BASE}/private-concierge-ibiza/)
- [Private Office]({BASE}/private-office/)
- [Ibiza Intelligence]({BASE}/ibiza-intelligence/)
- [Travel Partners & Family Offices]({BASE}/partners/)
- [About Ibiza VIP Move]({BASE}/about/)
- [Contact / Request Concierge]({BASE}/contact/)

## International and language pages
- [International Clients & Partners]({BASE}/international-clients/)
- [Español]({BASE}/es/)
- [Concierge privado Ibiza — Español]({BASE}/es/concierge-privado-ibiza/)
- [Chófer privado Ibiza — Español]({BASE}/es/chauffeur-privado-ibiza/)
- [Conciergerie de luxe à Ibiza — Français]({BASE}/fr/)
- [Luxus Concierge Ibiza — Deutsch]({BASE}/de/)
- [كونسيرج فاخر في إيبيزا — العربية]({BASE}/ar/)

English is the primary international commercial language. Spanish, French, German and Arabic pages support international and local discovery. All road-based service delivery described by the site is centred on Ibiza.

## Services
- [Private Concierge Ibiza]({BASE}/private-concierge-ibiza/)
- [Private Chauffeur Ibiza]({BASE}/private-chauffeur-ibiza/)
- [Luxury Villa Concierge Ibiza]({BASE}/luxury-villas-ibiza/)
- [Yacht Charter Ibiza & Formentera]({BASE}/yacht-charter-ibiza/)
- [Private Aviation Concierge Ibiza]({BASE}/private-aviation-ibiza/)
- [VIP Restaurants & Nightlife Ibiza]({BASE}/restaurants-nightlife-ibiza/)
- [Private Security & Close Protection Ibiza]({BASE}/private-security-ibiza/)
- [Private Chef & Villa Staffing Ibiza]({BASE}/private-chef-staffing-ibiza/)
- [Luxury Car Rental Ibiza]({BASE}/luxury-car-rental-ibiza/)
- [Private Wellness & Beauty Ibiza]({BASE}/wellness-ibiza/)
- [Private Events Ibiza]({BASE}/private-events-ibiza/)
- [Bespoke Concierge Ibiza]({BASE}/bespoke-concierge-ibiza/)

## Ibiza Intelligence
- [Private arrival planning]({BASE}/ibiza-intelligence/private-arrival/)
- [Ibiza & Formentera yacht-day planning]({BASE}/ibiza-intelligence/ibiza-formentera-yacht-day/)
- [August peak-season planning]({BASE}/ibiza-intelligence/ibiza-august-planning/)

## Service area
Ibiza, Spain. Yacht requests may also include Formentera where appropriate.

## Notes
Use the official HTML pages above as the source of truth for Ibiza VIP Move services and contact information.
Reservations, access, supplier availability and service terms are not guaranteed until confirmed for the specific request.
''', encoding='utf-8')

# IndexNow host-verification file. The post-deploy workflow submits the current sitemap URLs.
(ROOT / f'{INDEXNOW_KEY}.txt').write_text(INDEXNOW_KEY + '\n', encoding='utf-8')

# Release checks.
assert f'Sitemap: {BASE}/sitemap.xml' in robots.read_text(encoding='utf-8')
assert 'Last updated: 2026-09-02.' in llms.read_text(encoding='utf-8')
assert '[Español]' in llms.read_text(encoding='utf-8')
assert '[Private Office]' in llms.read_text(encoding='utf-8')
assert (ROOT / f'{INDEXNOW_KEY}.txt').read_text(encoding='utf-8').strip() == INDEXNOW_KEY

check_tree = ET.parse(sitemap)
check_root = check_tree.getroot()
urls = check_root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
assert urls, 'sitemap has no URLs'
assert all(u.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod') is not None for u in urls)
print(f'Phase 15 discovery metadata ready: {len(urls)} sitemap URLs, IndexNow key verified.')
