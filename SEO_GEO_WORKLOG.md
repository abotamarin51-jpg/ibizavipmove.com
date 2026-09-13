# Ibiza VIP Move — SEO / GEO worklog

Updated: 13 September 2026. Repository: `abotamarin51-jpg/ibizavipmove.com`.

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
- Phase 123: PR #41, merge `2b070ef763567b4328def623e78b5abd70028ff5`, deployment `34718471697`, release artifact `10308067566`, digest `sha256:dec797e044cb3400c00114184ffee5657cae8037b4cf27147119d3c4567d0731` — deployment completed successfully on 13 September; exact release artifact contains one `ivm-phase105-proof` block and no `ivm-phase104-authority` block on `/partners/`, with the sitemap still at 156 URLs. Direct public fetch was unavailable from the verification environment, so independent post-deploy HTML retrieval remains unconfirmed.
- Phase 124: PR #42, merge `57aa090c6053f0f2472f23d63c35933ff1b7f365`, deployment `34727014802`, release artifact `10307534868`, digest `sha256:60452d0df0778d5d617e8814fa742e4e9e67e3cecd444798569946832d87de4b` — all 30 Black Book notes now align Article/Open Graph freshness to sitemap evidence. Exact release validation confirms six English notes use verified `2026-09-03`, 24 localized notes remain intentionally undated, 156 indexable canonicals match the sitemap exactly, no internal HTML links are broken, hreflang targets resolve and `/partners/` remains consolidated.
- Phase 125: PR #44, merge `3ca0176480fa327a24d12c2bd92d5562527f053b`, deployment `34729233445`, release artifact `10308143048`, digest `sha256:b7c50d5d67208893d8dec3f88d3842e6f3cdba753b58f8ac751486d12c6d7ce4` — 44 canonical pages with a wrong image preload now point that preload at the same existing image marked `fetchpriority="high"`. Exact release validation confirms all 68 canonical pages in the deterministic one-preload/one-priority-image cohort are aligned, `/partners/` preloads its actual `private-office.jpg` hero, the sitemap remains 156 URLs and Phase 123/124 safeguards remain intact.

These are technical publication and regression checkpoints, not proof of Google indexation, rankings, traffic, conversions or Maps position.

## Phase 123 — Partners proof consolidation

Evidence: the exact Phase 122 production artifact and the previously public `/partners/` page contained two adjacent authority/proof sections that communicated substantially the same proposition and linked to the same three evidence resources: case studies, the 2026 operations report and the founder profile. `/destination-management-ibiza/` and `/private-client-services-ibiza/` each contained only one equivalent operational-evidence block. The duplication was therefore specific to the English Partners page and added repetitive copy/links without giving a professional partner a distinct next step.

Published change: remove only the older `ivm-phase104-authority` block from `/partners/`, retain the newer `ivm-phase105-proof` block and all three authority routes, and refresh only `/partners/` to truthful `lastmod=2026-09-12`. No URL, title/meta, schema, service claim, WhatsApp destination, tracking, stylesheet, price, policy or other page changes.

Validation: PR #41 CI passed; deployment `34718471697` completed successfully; exact release artifact `10308067566` contains no `ivm-phase104-authority` and exactly one `ivm-phase105-proof` block on `/partners/`; the sitemap remains exactly 156 unique canonical URLs. The public fetch tool returned a cache miss immediately after deployment, so the release artifact is the verified production-build evidence and public retrieval should be rechecked separately before claiming independent propagation.

## Phase 124 — Black Book freshness integrity

Evidence: `phase77_enhance.py` and `phase78_enhance.py` derive `Article.dateModified` and `article:modified_time` from `date.today()` at build time. In the exact Phase 123 PR artifact, all 30 Black Book planning notes therefore reported `2026-09-12` as modified even though the sitemap has verified `lastmod=2026-09-03` for the six English notes and intentionally has no `lastmod` for the 24 ES/FR/DE/AR notes. A routine deployment must not masquerade as an editorial update.

Published change: a final post-processing phase reads each of the 30 Black Book article URLs from the sitemap. When a verified sitemap `lastmod` exists, both Article schema and Open Graph modified-time metadata are aligned to it. When no verified `lastmod` exists, `dateModified` and `article:modified_time` are omitted instead of inventing a date. `datePublished` remains unset. No visible copy, URL, canonical, hreflang, service claim, contact route, tracking, price or legal content changed.

Validation: PR #42 CI `34726887779` passed before merge. Deployment `34727014802` completed successfully. Exact release artifact `10307534868` confirms six English notes use verified `2026-09-03`, 24 localized notes remain intentionally undated, all 156 indexable canonicals match the sitemap exactly, there are no broken internal HTML links in the generated site, hreflang targets resolve within the sitemap and the Phase 123 Partners consolidation remains intact. Google Search Central defines `dateModified` as the date/time the article was most recently modified and says recommended properties should be added only when they apply; this phase therefore favors truthful omission over build-time freshness inflation.

## Phase 125 — priority-image preload integrity

Evidence: the exact Phase 124 production artifact contained 68 canonical pages with exactly one `<link rel="preload" as="image">` and exactly one `<img fetchpriority="high">`. On 44 of those pages the preload pointed at a different image from the existing priority image. `/partners/`, for example, preloaded `/assets/images/aviation.jpg` while its actual priority hero was `/assets/images/private-office.jpg`. This can pull a non-LCP image into the early network queue while the real priority hero still needs to load. Chrome's current LCP-discovery guidance says image LCP should be discoverable and prioritized, and treats preload/fetch priority as mechanisms for that same critical resource.

Published change: a final post-processing phase changes only the existing preload `href` when a canonical page has exactly one image preload and one `fetchpriority="high"` image and those URLs differ. Responsive `imagesrcset` preloads are not guessed or rewritten. No image source, visible copy, URL, schema, tracking, contact route, price, policy, sitemap date or legal content changed.

Validation: PR #44 CI `34729199785` passed with preview artifact `10309107085`, digest `sha256:8f3b68f3ba04d79634854264f2537afee3d396cd41ed4d6cd5dd3b71180b69a3`. Deployment `34729233445` completed successfully, including Pages and IndexNow. Exact release artifact `10308143048`, digest `sha256:b7c50d5d67208893d8dec3f88d3842e6f3cdba753b58f8ac751486d12c6d7ce4`, confirms 68/68 eligible canonical pages aligned and zero mismatches; `/partners/` now preloads `/assets/images/private-office.jpg`, the sitemap remains 156 URLs, the Phase 123 proof consolidation remains one block and the Phase 124 EN/localized freshness behavior remains unchanged.

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

1. Recheck independent public retrieval of `/partners/` and a representative EN/FR/DE/AR Black Book note; search retrieval currently returns no result for the exact pages, so do not confuse release-artifact evidence with a separately observed public response.
2. Audit one unresolved mobile/performance, conversion/accessibility, content-clarity or information-architecture issue only if reproducible; do not add pages or tracking by default.
3. Where authorized tools allow, verify the correct Ibiza VIP Move Search Console/Analytics property before claiming indexation, country demand or lead metrics. Never reuse the other brand's property or tracking ID.
4. Keep the 13 priority commercial routes within the Phase 111 crawl-depth threshold; no orphan pages, mass country pages, synonym pages, speculative redirects/noindex changes or word-count padding.
5. Keep technical improvements separate from measured business impact.

## Primary-source reference principles

- Google crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Article structured data: https://developers.google.com/search/docs/appearance/structured-data/article
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google sitemap lastmod guidance: https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
- Google local ranking: https://support.google.com/business/answer/7091
- Chrome LCP request discovery: https://developer.chrome.com/docs/performance/insights/lcp-discovery
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/
- HTML telephone inputs: https://html.spec.whatwg.org/multipage/input.html#telephone-state-(type=tel)

Useful visible content, crawlable contextual links, accurate freshness/form semantics, matching structured data and disciplined critical-resource hints remain the basis. `llms.txt`, schema, IndexNow and more pages do not guarantee search/AI visibility, Maps rankings or leads.

## 13 September addendum — Phases 126–127

- Phase 126: PR #46, merge `14c23f5d6d9e1a08855ac24e91dbed864eeed2cc`, deployment `34734029644`, production artifact `10309969586`, digest `sha256:8c78e01d82433382ec2aab5f1d935ae16be99dcde8d0940359cb16434d43cdcb` — the existing `/luxury-car-rental-ibiza/` canonical now uses natural UK `hire` plus international/US `rental` terminology on the same URL, based on owner-provided Search Console evidence. No synonym page was created; exact private Search Console metrics are intentionally not committed to this public repository.
- Phase 127: PR #47, merge `b93c9ee6442f699ffb60ea4de66d8ca04390bdc6`, CI `34736604018`, deployment `34736647446`, production artifact `10311133324`, digest `sha256:808a62fadce880234ccce851977d3e03dadc70237bf76a249c29641061b3f6b1` — owner-provided Search Console evidence identified the historical `/services/private-jets` path as still Google-known, while the Phase 126 production artifact had no file at that route. The site now serves `/services/private-jets/` as a direct `noindex,follow` client-side alias to `/private-aviation-ibiza/`, matching the site's existing static-host fallback pattern. The alias is excluded from the sitemap; the canonical aviation page remains indexable and the sitemap stays at 156 canonical URLs.

Phase 127 is a technical URL-continuity fix, not proof that Google has recrawled the legacy URL, consolidated signals, changed rankings, or generated leads. Google recommends permanent server-side redirects where technically possible and permits client-side redirects as a fallback; GitHub Pages in this repository does not expose per-path HTTP redirect rules. Bing likewise recommends redirects for moved URLs and canonical-only sitemaps.

Next priority: use refreshed owner Search Console evidence before making further indexation changes. Prefer another reproducible legacy-URL, crawl/indexation, conversion or mobile issue over creating additional pages; keep private Search Console metrics out of the public repository.

## 13 September addendum — Phase 128

- Phase 128: PR #49, merge `2da38b591ee1650b02c6fd1aa1a92fcbf40ce357`, CI `34739068233`, deployment `34739113574`, production artifact `10312435972`, digest `sha256:c1f72ddb633ffd18b38605e4f131d76afc9dd44704f6edc532235a9eb27f3b79` — the existing `/services/` hub now replaces the search-facing “More ways clients search for this support” bridge with user-centred service-model guidance and crawlable descriptive links to all six existing service-model routes: Personal Concierge, Luxury Travel Concierge, Lifestyle Management, VIP Services, Private Client Services, and Luxury DMC & Destination Management. No new URL was created. Exact release comparison against Phase 127 changes only `services/index.html` and `sitemap.xml`; the sitemap remains 156 canonical URLs and `/services/` carries truthful `lastmod=2026-09-13`.

The GitHub Pages deployment completed successfully and the exact production artifact validates the change. An independent public reader immediately after deployment still returned its previously cached `/services/` block, so independent propagation should be rechecked separately rather than treated as proof of a live recrawl. This is an information-architecture and user-clarity improvement, not measured evidence of better rankings, traffic, conversions or leads.

Next priority: recheck independent public retrieval of `/services/`; then use refreshed owner Search Console/indexation evidence before any further indexation change. Prefer reproducible conversion, mobile/performance or legacy-URL issues over creating additional pages.
