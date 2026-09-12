# Ibiza VIP Move — SEO / GEO worklog

Updated: 12 September 2026. Repository: `abotamarin51-jpg/ibizavipmove.com`.

## Scope and safeguards

Improve the existing Ibiza website for qualified private-client and international B2B enquiries. The aspiration is international recognition for luxury concierge IN IBIZA, not a guaranteed worldwide ranking. Only this domain/repository is in scope. Do not mix Ibiza Private Drivers, its Business Profile or its Analytics property. Google Business Profile/Maps edits, DNS/MX changes, outreach, paid links, advertising, association registrations and new membership products remain outside this workstream. No invented reviews, ratings, affiliations, offices, client identities, prices or availability guarantees.

Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN, FR, DE, AR. Preserve existing Spanish without expanding Spain/Italy targeting. Search Console, GA4 and country-specific ranking/impression/conversion data remain unverified; do not infer commercial impact from technical deployment alone.

## Latest verified checkpoints

- Phase 111: `16f3fcced839b31f5a2b42034d615ee83654e8d0` — 156 sitemap URLs reachable in the generated HTML graph; 13 priority commercial routes within 0–2 crawlable links of Home.
- Phase 112: PR #30, merge `010baac97f6891c02571e2886937c79d6ebf02dd`, deployment `34689850167` — FR/DE/AR Partner pages strengthened for DMC/destination-management/private-travel intent without new URLs.
- Phase 113: PR #31, merge `f866e7f99fea55ba605929045a78f2e98a923449`, deployment `34690582374` — FR/DE/AR international-client/private-office journeys gained same-language audience/contact routes and clearer representative briefs.
- Phase 114: PR #32, merge `c5268deda041b997f21c48b578caeffcb3cc01f2`, deployment `34692434048` — five contact desks share localized today-or-later and departure-after-arrival validation.
- Phase 115: PR #33, merge `4b85e41ba396f02ee9164f71a027a53e66d5b3fa`, deployment `34695052164` — five required phone inputs use `type="tel"`, `inputmode="tel"` and `autocomplete="tel"` without a rigid country pattern.
- Phase 116: PR #34, merge `68958d3315212ab3f321e35aea4ecf5782656447`, deployment `34697823273` — required buyer-role selects start from localized empty placeholders instead of silently defaulting to private client.
- Phase 117: PR #35, merge `219602fd3a0a023a3173cd129b808cc80342648d`, deployment `34701142012`, artifact `10299928576` — contact date eligibility uses the Ibiza calendar (`Europe/Madrid`) rather than the visitor device timezone.
- Phase 118: PR #36, merge `1c89205f80befa91b3c07959e30b5114f063056d`, deployment `34703836099`, artifact `10301017441` — localized international-country-code guidance added without rigid country validation.
- Phase 119: PR #37, merge `526650a427465785265f3b1251745a359c1a1312`, deployment `34706772578`, artifact `10300879821` — whitespace-only required name/phone values rejected; outgoing WhatsApp values trimmed.
- Phase 120: PR #38, merge `15d9025914ae6959cc6a9b18f843b0b90911eeda`, deployment `34709598540`, artifact `10302363132` — clearly incomplete phone values rejected while international formatting remains flexible.
- Phase 121: PR #39, merge `b774abae7df8168a555bf78d36eed552b544e8ff`, deployment `34712575664`, exact release artifact `10303518957`, digest `sha256:2f5723a9be48dbe70fdebfb2e9e362ccb2a282e29efe16ade28903bf88a26b08` — 14 routes with verified significant 12 September changes carry truthful `lastmod=2026-09-12`; sitemap inventory remains 156 URLs.
- Phase 122: PR #40, merge `d12b14ad322d571ef4c357637025c3f83abda8bc`, deployment `34715611730`, exact release artifact `10304588267`, digest `sha256:2cf033e231479c35419bc055904e970e017b024a2379e458f2796c6a3456aa76` — five contact desks use localized private-client service wording instead of implying an unauthorized membership product. Public EN/FR/DE/AR contact retrieval on 12 September now shows the new labels.

These are technical publication and regression checkpoints, not proof of Google indexation, rankings, traffic, conversions or Maps position.

## Phase 123 — Partners proof consolidation

Evidence: the exact Phase 122 production artifact and the public `/partners/` page contain two adjacent authority/proof sections that communicate substantially the same proposition and link to the same three evidence resources: case studies, the 2026 operations report and the founder profile. `/destination-management-ibiza/` and `/private-client-services-ibiza/` each contain only one equivalent operational-evidence block. The duplication is therefore specific to the English Partners page and adds repetitive copy/links without giving a professional partner a distinct next step.

Prepared change on branch `seo/phase123-partners-proof-consolidation`: remove only the older `ivm-phase104-authority` block from `/partners/`, retain the newer `ivm-phase105-proof` block and all three authority routes, and refresh only `/partners/` to truthful `lastmod=2026-09-12`. No URL, title/meta, schema, service claim, WhatsApp destination, tracking, stylesheet, price, policy or other page changes.

Pre-PR validation against the exact Phase 122 release artifact: enhancer and read-only audit pass; `/partners/` retains 466 visible main-content words, one H1, canonical, six-entry EN/ES/FR/DE/AR/x-default hreflang set, one CSS bundle, accessibility landmarks and links to case studies/report/founder. The sitemap remains exactly 156 unique canonical URLs. Google states that internal links should be crawlable and contextually useful; Bing’s current Webmaster Guidelines likewise emphasize crawlable internal links, content clarity and accurate freshness signals for search and grounding experiences. Consolidation is a clarity change, not a ranking guarantee.

## Intent ownership — reuse existing URLs

| Search intent | Existing preferred route | Scope |
| --- | --- | --- |
| Luxury concierge Ibiza | `/` | Brand and broad service overview |
| Private concierge Ibiza | `/private-concierge-ibiza/` | Connected multi-service stay |
| Lifestyle management | `/luxury-lifestyle-management-ibiza/` | Ongoing stay coordination |
| Private client services | `/private-client-services-ibiza/` | Principals, PAs, EAs, family offices |
| Personal concierge / personal assistance | `/personal-concierge-ibiza/` | Direct personal travel assistance, not recruitment |
| Luxury travel concierge / private travel management | `/luxury-travel-concierge-ibiza/` | Pre-arrival planning and local coordination |
| Bespoke travel / travel planning | `/luxury-travel-concierge-ibiza/` | Tailored travel brief; no synonym page |
| VIP services / VIP hospitality / VIP access | `/vip-services-ibiza/` | Hospitality/access requests subject to confirmation |
| Luxury DMC / destination management | `/destination-management-ibiza/` | Local execution for professional travel partners |
| Ibiza concierge partner / local Ibiza operator | `/partners/` | Professional handover and client relationship protection |
| One-off bespoke requests | `/bespoke-concierge-ibiza/` | Unusual individual requests |
| Private membership | No authorized page/product | Research term only; do not imply membership in visible service UI |

## Next execution priorities

1. Resolve Phase 123 PR/check/deployment state first; verify the final `/partners/` artifact contains one operational-evidence block and the 156-URL crawl-depth gate remains green before calling it published.
2. After Phase 123, audit one unresolved conversion/accessibility, content-clarity or information-architecture issue only if reproducible; do not add pages or tracking by default.
3. Where authorized tools allow, verify the correct Ibiza VIP Move Search Console/Analytics property before claiming indexation, country demand or lead metrics. Never reuse the other brand's property or tracking ID.
4. Keep the 13 priority commercial routes within the Phase 111 crawl-depth threshold; no orphan pages, mass country pages, synonym pages, speculative redirects/noindex changes or word-count padding.
5. Keep technical improvements separate from measured business impact.

## Primary-source reference principles

- Google crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google sitemap lastmod guidance: https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
- Google local ranking: https://support.google.com/business/answer/7091
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/
- HTML telephone inputs: https://html.spec.whatwg.org/multipage/input.html#telephone-state-(type=tel)

Useful visible content, crawlable contextual links, accurate freshness/form semantics and matching structured data remain the basis. `llms.txt`, schema, IndexNow and more pages do not guarantee search/AI visibility, Maps rankings or leads.
