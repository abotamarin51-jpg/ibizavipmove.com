from pathlib import Path

ROOT=Path('_site')
LLMS=ROOT/'llms.txt'
if not LLMS.exists(): raise SystemExit('Phase 93 llms.txt missing')
text=LLMS.read_text(encoding='utf-8')

# Replace the older general service-area line with the same service geography
# that is visible on the website and present in Organization structured data.
old='Primary service area: Ibiza, Balearic Islands, Spain\n'
new='''Primary service area: Ibiza, Balearic Islands, Spain
Service areas include: Eivissa / Ibiza Town; Marina Botafoch / Talamanca; Sant Josep de sa Talaia; Cala Jondal / Es Cubells; Santa Eulària des Riu; Roca Llisa / Cala Llonga; Sant Antoni de Portmany; Santa Gertrudis de Fruitera.
'''
if old not in text: raise SystemExit('Phase 93 primary service-area marker missing')
text=text.replace(old,new,1)

old_b2b='''## B2B and professional coordination
- [Private Office](https://ibizavipmove.com/private-office/) — for principals, families, PAs, family offices and professional representatives.
- [Travel & Concierge Partners](https://ibizavipmove.com/partners/) — for luxury travel advisors, concierge companies and hospitality partners.
- [International Clients & Partners](https://ibizavipmove.com/international-clients/) — for briefs originating outside Ibiza.
- [Media & Partner Information](https://ibizavipmove.com/media-partners/) — official brand and partnership information.
'''
new_b2b='''## B2B and professional coordination
- [Private Office](https://ibizavipmove.com/private-office/) — Ibiza concierge and operational support for principals, families, personal assistants, executive assistants, family offices and private teams coordinating complex stays.
- [Travel & Concierge Partners](https://ibizavipmove.com/partners/) — for luxury travel advisors, concierge companies and hospitality partners.
- [International Clients & Partners](https://ibizavipmove.com/international-clients/) — for briefs originating outside Ibiza.
- [Media & Partner Information](https://ibizavipmove.com/media-partners/) — official brand, factual verification and partnership information.

Private Office scope clarification: Ibiza VIP Move is not presented as a legal, tax, investment, fiduciary, wealth-management or formal family-office advisory service. It provides concierge and on-island operational coordination for private stays.
'''
if old_b2b not in text: raise SystemExit('Phase 93 B2B marker missing')
text=text.replace(old_b2b,new_b2b,1)

machine='''## Machine-readable discovery
- [XML sitemap](https://ibizavipmove.com/sitemap.xml)
- [Image sitemap](https://ibizavipmove.com/image-sitemap.xml)
- [Robots policy](https://ibizavipmove.com/robots.txt)
'''
replacement='''## Verified external reference
Luxury Magazine published the 2026 editorial article “Top Luxury Travel Concierge Services for Ibiza Dining,” which includes a section about Ibiza VIP Move and its coordination-led approach to complex dining logistics. This is an independent external editorial reference and does not imply endorsement or partnership.
- [Luxury Magazine editorial reference](https://www.luxury-magazine.eu/luxury-travel-concierge-services-ibiza-dining/)

## Official identity
- Official website: https://ibizavipmove.com/
- Official Instagram: https://www.instagram.com/ibizavipmove/
- Canonical organization entity: https://ibizavipmove.com/#organization

## Machine-readable discovery
- [XML sitemap](https://ibizavipmove.com/sitemap.xml)
- [Image sitemap](https://ibizavipmove.com/image-sitemap.xml)
- [Robots policy](https://ibizavipmove.com/robots.txt)
'''
if machine not in text: raise SystemExit('Phase 93 machine-discovery marker missing')
text=text.replace(machine,replacement,1)

LLMS.write_text(text,encoding='utf-8')
print('PASS: Phase 93 AI/GEO source of truth — llms.txt aligned to Family Office concierge scope, eight Ibiza service areas, official Instagram and verified external editorial reference')
