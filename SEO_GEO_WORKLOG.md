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
- Phase 117: PR #35, merge `219602fd3a0a023a3173cd129b808cc80342648d`, deployment `34701142012`, exact release artifact `10299928576`, digest `sha256:6b571be21d2e4d44790e69727b5cf973e4c46daf46b80aa95160bc7918905205` — contact date eligibility uses the Ibiza calendar (`Europe/Madrid`) rather than the visitor device timezone.
- Phase 118: PR #36, merge `1c89205f80befa91b3c07959e30b5114f063056d`, deployment `34703836099`, exact release artifact `10301017441`, digest `sha256:732032c131ffe96a5447d89066c7d1e8ce8187523a532eba60aae29bfd182f73` — five required phone fields expose localized international-country-code guidance via `aria-describedby` while retaining flexible `type=tel` semantics.

These are technical publication and regression checkpoints, not proof of Google indexation, rankings, traffic, conversions or Maps position.

## Phase 119 — reject whitespace-only required contact values

Evidence: the exact Phase 118 production artifact was downloaded and inspected. The EN/ES/FR/DE/AR contact forms retain required name and phone fields, but native HTML `required` treats strings containing only spaces as non-empty. Chromium reproduced this on the production English form: with `fName="   "`, `fPhone="   "` and a valid buyer profile selected, `form.checkValidity()` returned true and both required controls were considered valid. This can create an empty-looking WhatsApp handover and is a lead-quality/accessibility defect, not evidence of measured lost conversions.

Prepared change on branch `seo/phase119-reject-blank-required-text`: extend the existing shared qualified-brief runtime at build output so name and phone reject whitespace-only values with localized custom-validity messages, trim outgoing field values before the WhatsApp brief is assembled, and cache-bust the existing runtime reference from `v=117` to `v=119`. The WhatsApp destination, international phone semantics, country-code hint, Ibiza-calendar date logic, no-PII analytics payload, form inventory, URLs, CSS, schema, sitemap, tracking and Maps/GBP remain unchanged.

Pre-PR validation: the proposed runtime passes `node --check`. In a Chromium harness, whitespace-only name/phone values become invalid, the localized English message is exposed, focus moves to the first invalid required text field, and normal values with surrounding whitespace become valid while the handover getter trims them. No form or WhatsApp message was submitted. Full repository CI remains the release gate before merge.

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
| Private membership | No authorized page/product | Research term only |

## Next execution priorities

1. Resolve Phase 119 PR/check/deployment state first; verify the exact release artifact before calling the whitespace guard published.
2. After Phase 119, audit one unresolved conversion/accessibility or information-architecture issue only if reproducible; do not add pages or tracking by default.
3. Where authorized tools allow, verify the correct Ibiza VIP Move Search Console/Analytics property before claiming indexation, country demand or lead metrics. Never reuse the other brand's property or tracking ID.
4. Keep the 13 priority commercial routes within the Phase 111 crawl-depth threshold; no orphan pages, mass country pages, synonym pages, speculative redirects/noindex changes or word-count padding.
5. Keep technical improvements separate from measured business impact.

## Primary-source reference principles

- Google crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google local ranking: https://support.google.com/business/answer/7091
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/
- HTML telephone inputs: https://html.spec.whatwg.org/multipage/input.html#telephone-state-(type=tel)

Useful visible content, crawlable contextual links, accurate form semantics and matching structured data remain the basis. `llms.txt`, schema, IndexNow and more pages do not guarantee search/AI visibility, Maps rankings or leads.
