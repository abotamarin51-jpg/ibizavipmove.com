# Ibiza VIP Move — SEO keyword map (17 November 2026)

**Scope:** ibizavipmove.com only. This is an editorial research/backlog file, not a request to generate hundreds of pages or alter Google Business Profile. Existing ranking pages, canonicals, URL structure, translations, tracking and content controls take precedence.

## First-party Search Console baseline

Property: `https://ibizavipmove.com/`. Search type: Web. Period: 18 Oct–14 Nov 2026, settled data.

- `villa concierge ibiza`: 44 impressions, 0 clicks, average position 13.11. Route to **/luxury-villas-ibiza/**, not a new page.
- `villa management ibiza`: 21 impressions, 0 clicks, average position 15.86. **Do not target as a core service** without evidence that property-owner management is genuinely offered.
- `eventagentur ibiza`: 147 impressions, 0 clicks, average position 25.95 across `/de/private-events-ibiza/` in query/page results. Keep language-consistent German intent.
- `event koordination ibiza`: 42 impressions, 0 clicks, average position 5.38 on German Events. Preserve its content; monitor CTR.
- `luxury concierge ibiza`: currently has homepage impressions. Preserve Home as the broad landing page.

## Intent ownership and candidate keyword groups

Keyword variations are **editorial candidates** until volume, local SERP intent and commercial fit are independently confirmed. Do not put a list of variants into a page merely to rank.

| Intent and current page | Candidate phrases | Decision |
|---|---|---|
| Broad luxury concierge — `/` and `/private-concierge-ibiza/` | luxury concierge ibiza; private concierge ibiza; vip concierge ibiza; ibiza concierge services; 24/7 concierge ibiza | Maintain existing Home / Concierge distinction, no duplicate landing page |
| Luxury stays — `/luxury-villas-ibiza/` | luxury villa rentals ibiza; luxury villas ibiza; exclusive villas ibiza; villa concierge ibiza; serviced villas ibiza; luxury villas with private chef ibiza | Existing page is indexable and already covers the main service. Monitor before further edits |
| Private events — `/private-events-ibiza/` | private events ibiza; private party ibiza; private birthday party ibiza; luxury birthday ibiza; villa celebration ibiza; private event planning ibiza | **One bounded content paragraph staged in this PR** describing how to brief a private birthday party; no new page |
| Yachts — `/yacht-charter-ibiza/` | luxury yacht charter ibiza; private yacht charter ibiza; yacht rental ibiza; ibiza formentera yacht charter | Existing route; avoid duplicating yacht intent |
| Restaurants / nightlife — `/restaurants-nightlife-ibiza/` and purpose-specific service pages | vip tables ibiza; ibiza nightlife concierge; vip restaurant reservations ibiza; luxury beach clubs ibiza | Clarify real service and booking conditions, avoid guarantees |
| Aviation / security — existing private aviation and security pages | private jet ibiza; private aviation concierge ibiza; bodyguard ibiza; private security ibiza | Existing service routes, only claims backed by operations |
| Mobility — `/private-chauffeur-ibiza/` | private chauffeur ibiza; luxury chauffeur ibiza; vip transfers ibiza; executive chauffeur ibiza | Do not copy the same target or compete unnecessarily with ibizaprivatedrivers.com |
| German private events — `/de/private-events-ibiza/` | eventagentur ibiza; event koordination ibiza; firmenevent ibiza; eventkoordination ibiza | Strong existing impression signals; preserve and monitor, editorial review separately |

## QuestionFinder import

The supplied `questionfinder-luxury-villa-ibiza.csv` has **one** row: `can verru luxury villa ibiza` (reported volume/mo 10, buyer intent 88). This is a named-property query. **Do not create a Can Verru service/booking page** or claim association without confirmed availability and rights to market the villa.

## Safeguards before any merge

1. Compare branch diff with latest main and all overlapping open PRs.
2. Require passing site build/validation and check generated Events HTML for one paragraph only. No changes to title, H1, head, canonical, hreflang, links, FAQ schema, asset delivery, contact route or Google Business.
3. Do not publish or merge automatically. Source main currently has a recent failed workflow; distinguish inherited failures from this branch.
4. If released, measure Search Console queries/pages across a comparable 28-day period; note lag, impression noise and seasonality. Do not promise top ranking.
