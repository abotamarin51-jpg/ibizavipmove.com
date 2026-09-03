from pathlib import Path
from datetime import date
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ORG = BASE + '/#organization'
TODAY = date.today().isoformat()

SERVICES = [
    ('Private Chauffeur Ibiza', '/private-chauffeur-ibiza/'),
    ('Luxury Villas Ibiza', '/luxury-villas-ibiza/'),
    ('Yacht Charter Ibiza', '/yacht-charter-ibiza/'),
    ('Private Aviation Ibiza', '/private-aviation-ibiza/'),
    ('Restaurants, Beach Clubs & Nightlife Ibiza', '/restaurants-nightlife-ibiza/'),
    ('Private Security Ibiza', '/private-security-ibiza/'),
    ('Private Chef & Villa Staffing Ibiza', '/private-chef-staffing-ibiza/'),
    ('Luxury Car Rental Ibiza', '/luxury-car-rental-ibiza/'),
    ('Wellness & Beauty Ibiza', '/wellness-ibiza/'),
    ('Private Events Ibiza', '/private-events-ibiza/'),
    ('Bespoke Concierge Ibiza', '/bespoke-concierge-ibiza/'),
]

PRIMARY = [
    ('Home', '/'),
    ('Private Concierge Ibiza', '/private-concierge-ibiza/'),
    ('Private Services', '/services/'),
    ('Private Office', '/private-office/'),
    ('International Clients & Partners', '/international-clients/'),
    ('Travel & Concierge Partners', '/partners/'),
    ('Media & Partner Information', '/media-partners/'),
    ('About Ibiza VIP Move', '/about/'),
    ('Request Concierge', '/contact/'),
]

LANGUAGE_HUBS = [
    ('English', '/', '/services/', '/ibiza-intelligence/', '/contact/'),
    ('Español', '/es/', '/es/servicios/', '/es/ibiza-intelligence/', '/es/contacto/'),
    ('Français', '/fr/', '/fr/services/', '/fr/ibiza-intelligence/', '/fr/contact/'),
    ('Deutsch', '/de/', '/de/services/', '/de/ibiza-intelligence/', '/de/kontakt/'),
    ('العربية', '/ar/', '/ar/services/', '/ar/ibiza-intelligence/', '/ar/contact/'),
]

BLACK_BOOK = [
    ('The Ibiza Black Book', '/ibiza-intelligence/'),
    ('Private arrival planning', '/ibiza-intelligence/private-arrival/'),
    ('Ibiza & Formentera yacht-day planning', '/ibiza-intelligence/ibiza-formentera-yacht-day/'),
    ('August peak-season planning', '/ibiza-intelligence/ibiza-august-planning/'),
    ('Villa arrival planning', '/ibiza-intelligence/villa-arrival-planning/'),
    ('Nightlife transport planning', '/ibiza-intelligence/nightlife-transport-planning/'),
    ('Private aviation ground coordination', '/ibiza-intelligence/private-aviation-ground-coordination/'),
]


def link(label, path):
    return f'- [{label}]({BASE}{path})'

for _, path in PRIMARY + SERVICES + BLACK_BOOK:
    target = ROOT / 'index.html' if path == '/' else ROOT / path.strip('/') / 'index.html'
    if not target.exists():
        raise SystemExit(f'Phase 76 referenced page missing: {path}')

for _, home, services, editorial, contact in LANGUAGE_HUBS:
    for path in (home, services, editorial, contact):
        target = ROOT / 'index.html' if path == '/' else ROOT / path.strip('/') / 'index.html'
        if not target.exists():
            raise SystemExit(f'Phase 76 language hub missing: {path}')

service_lines = '\n'.join(link(label, path) for label, path in SERVICES)
primary_lines = '\n'.join(link(label, path) for label, path in PRIMARY)
black_book_lines = '\n'.join(link(label, path) for label, path in BLACK_BOOK)
language_lines = '\n'.join(
    f'- {label}: [Home]({BASE}{home}) · [Services]({BASE}{services}) · [Black Book]({BASE}{editorial}) · [Contact]({BASE}{contact})'
    for label, home, services, editorial, contact in LANGUAGE_HUBS
)

text = f'''# Ibiza VIP Move

> Official machine-readable summary for Ibiza VIP Move, a private concierge and luxury lifestyle coordination company serving Ibiza, Balearic Islands, Spain.
> Last updated: {TODAY}.

Official website: {BASE}/
Canonical organization entity: {ORG}
Phone / WhatsApp: +34 600 703 303
Partnerships email: partnership@ibizavipmove.com
Primary service area: Ibiza, Balearic Islands, Spain
Languages published: English, Spanish, French, German and Arabic

## What Ibiza VIP Move does
Ibiza VIP Move coordinates private-client stays through one point of contact. The official service catalog covers chauffeur transportation, luxury villas, yachts, private aviation, restaurants and nightlife, private security, private chefs and villa staffing, luxury car rental, wellness, private events and bespoke concierge requests.

The company also supports principals, families, personal assistants, family offices, luxury travel advisors, concierge companies, hospitality partners and private-aviation partners that need local Ibiza execution.

## Primary official pages
{primary_lines}

## Canonical service catalog — 11 services
{service_lines}

## International discovery
Each major commercial service is published as a reciprocal five-language EN/ES/FR/DE/AR cluster using self-canonicals and hreflang. Use the language hubs below to discover the localized versions.

{language_lines}

## The Ibiza Black Book
The Ibiza Black Book is Ibiza VIP Move's evergreen planning and operational editorial collection. The hub and six planning notes are also available in English, Spanish, French, German and Arabic.

{black_book_lines}

## B2B and professional coordination
- [Private Office]({BASE}/private-office/) — for principals, families, PAs, family offices and professional representatives.
- [Travel & Concierge Partners]({BASE}/partners/) — for luxury travel advisors, concierge companies and hospitality partners.
- [International Clients & Partners]({BASE}/international-clients/) — for briefs originating outside Ibiza.
- [Media & Partner Information]({BASE}/media-partners/) — official brand and partnership information.

## Machine-readable discovery
- [XML sitemap]({BASE}/sitemap.xml)
- [Image sitemap]({BASE}/image-sitemap.xml)
- [Robots policy]({BASE}/robots.txt)

## Source-of-truth and accuracy notes
The canonical HTML pages and their structured data are the source of truth for Ibiza VIP Move services, contact details and current wording. This file is supplementary discovery metadata.

Ibiza VIP Move coordinates requests and suppliers; availability, reservations, venue access, exact vehicles, properties, practitioners, staffing, permissions and other third-party services are not guaranteed until specifically confirmed. Wellness coordination does not replace medical advice. Bespoke requests must be legal, safe and viable.
'''

llms = ROOT / 'llms.txt'
llms.write_text(text, encoding='utf-8')

# Sanity checks before later independent audit.
final = llms.read_text(encoding='utf-8')
assert f'Last updated: {TODAY}.' in final
assert f'Canonical organization entity: {ORG}' in final
assert 'Canonical service catalog — 11 services' in final
assert final.count('## The Ibiza Black Book') == 1
assert 'English, Spanish, French, German and Arabic' in final
assert 'not guaranteed until specifically confirmed' in final
assert len(set(re.findall(r'https://ibizavipmove\.com[^)\s]*', final))) >= 35
print('PASS: Phase 76 AI/GEO discovery summary refreshed from the final multilingual architecture')
