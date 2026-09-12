# Ibiza VIP Move — SEO / GEO worklog

Updated: 12 September 2026. Repository: `abotamarin51-jpg/ibizavipmove.com`.

## Scope and safeguards

Improve the existing Ibiza website for qualified private-client and international B2B enquiries. The aspiration is international recognition for luxury concierge IN IBIZA, not a claim of a guaranteed worldwide ranking.

Only this domain/repository is in scope. Do not mix Ibiza Private Drivers, its Business Profile or its Analytics property. Google Business Profile/Maps edits, DNS/MX changes, outreach, paid links, advertising, association registrations and new membership products are outside this workstream. Local signals must describe real Ibiza service coverage, not fictional offices abroad. No invented reviews, ratings, affiliations, operating results, client identities, addresses, prices or availability guarantees.

Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN, FR, DE, AR. Preserve existing Spanish; do not expand Spain/Italy targeting. These are audience priorities, not verified search-volume estimates.

## Latest checkpoint

- Phase 111 is accepted on `main` at commit `16f3fcced839b31f5a2b42034d615ee83654e8d0`. Deployment run `34687207716` completed successfully on 12 September 2026; GitHub Pages reported success and IndexNow returned HTTP 200 for 156 sitemap URLs.
- The Phase 111 final generated-HTML audit verified 156 sitemap URLs reachable, with 13 priority pages within 0–2 crawlable HTML links of Home. FR/DE/AR Private Concierge routes are also protected within two links of their language home. This is a crawl-depth test, not proof of Google indexation, rankings, traffic, conversions or Maps position.
- Public HTTPS retrieval through the web research tool succeeded on 12 September for Home and the English Partners/Destination Management journeys. The earlier tool-specific cache/DNS limitation is therefore not treated as an active website outage. Public retrieval still does not prove that every URL is indexed.
- The English B2B intent is already substantial: `/partners/` owns local-operator/partner intent, `/destination-management-ibiza/` owns Luxury DMC / destination-management intent, and `/luxury-travel-concierge-ibiza/` covers private travel management. Do not create English synonym pages for these terms.
- Phase 112 is verified merged through PR #30 at `010baac97f6891c02571e2886937c79d6ebf02dd`. Deployment `34689850167` completed successfully on 12 September 2026. Its exact GitHub Pages artifact `10297306287` was retrieved and inspected as the Phase 113 baseline. The existing FR/DE/AR Partner pages contain localized DMC/private-travel operating scope and same-language routes to Services, Private Concierge and Private Office. No URL, stylesheet, title/meta rewrite or new service promise was added.
- Phase 113 implementation commit: `4d6a0ae1582aa8553fd62626e14739f582671444`, branch `seo/phase113-localized-enquiry-journeys`, based on the verified Phase 112 main above. Local validation is complete; PR CI, merge and release status must be checked in GitHub before treating this checkpoint as published. The PR discussion is the release-verification record.
- Search Console, GA4 and country-specific ranking/impression/conversion data remain unverified in this workstream. Do not infer measured commercial impact from a technical deployment.

The recurring ChatGPT task is separate from GitHub Actions: Actions validate proposed changes; they do not independently invent or publish SEO content. Each execution must re-read current state, respect permissions and avoid starting another write while a related PR/deployment is unresolved.

## Phase 113 — 12 September 2026, Europe/Madrid

Evidence: the deployed FR/DE/AR international-client pages had six audience descriptions but no in-content links to the relevant Concierge, Private Office, Partners or Private Aviation journeys. All six international/private-office pages lacked a contextual route to their existing localized contact form. Private Office's two main WhatsApp CTAs had no representative-specific prefilled context. Public retrieval independently succeeded for Home and the three international pages. This is an observed navigation/briefing gap, not a measured conversion loss.

Change: add 18 contextual links within existing audience labels and one localized contact-form link to each of the six pages. Clarify the Private Office first brief with role, dates, guest count, services, timezone, approval authority and communication preference; discourage identity/bank documents in the initial message. Prefill its two main WhatsApp CTAs per language without changing the number or sending messages. Replace the international pages' generic city list (including excluded Doha) with practical Ibiza-arrival coordination copy. No new URLs, sections, stylesheets, JavaScript, schema, tracking, prices or legal-policy changes. All modifications are restricted to the six existing main-content areas.

Affected routes: `/fr/clients-internationaux/`, `/de/internationale-kunden/`, `/ar/international-clients/`, `/fr/private-office/`, `/de/private-office/`, `/ar/private-office/`.

Tests: Python compilation passed. The new read-only audit first failed on the unmodified baseline as expected, then passed after applying the change. Full artifact comparison found exactly six changed HTML files; asset/file inventory, all other HTML, sitemap, robots, heads, navigation and footers remained byte-identical. Full local HTML graph: 156/156 sitemap URLs reachable, no missing internal targets and all 13 priority URLs at depth 0–2. Canonicals, reciprocal six-entry hreflang sets, one H1, Arabic RTL, same-language routes, form fields, WhatsApp identity/context and one CSS bundle per page passed. Twelve offline Chromium render cases at 375/1440px passed without horizontal overflow; existing form required-field validation passed. No contact request was submitted.

Execution limits: direct cloning was unavailable through the container network, so connected GitHub reads plus the exact deployed artifact were used. Browser loopback navigation was denied; mobile/desktop checks used in-memory rendering with all network requests blocked, not a live HTTP or Core Web Vitals test. A clean full build and all existing gates remain required in PR CI before merge; no existing test was weakened.

Research: Google Search Central AI-features and crawlable-links documentation rechecked; Bing Webmaster Guidelines search extract also supports crawlable internal links. The change improves visible routing and useful briefing content, not an AI-specific file or guaranteed ranking signal.

## Intent ownership — reuse existing URLs

| Search intent | Existing preferred route | Scope |
| --- | --- | --- |
| Luxury concierge Ibiza | `/` | Brand and broad service overview |
| Private concierge Ibiza | `/private-concierge-ibiza/` | Connected multi-service stay |
| Lifestyle management | `/luxury-lifestyle-management-ibiza/` | Ongoing stay coordination |
| Private client services | `/private-client-services-ibiza/` | Principals, PAs, EAs, family offices |
| Personal concierge / personal assistance | `/personal-concierge-ibiza/` | Direct personal travel assistance, not recruitment |
| Luxury travel concierge / private travel management | `/luxury-travel-concierge-ibiza/` | Pre-arrival planning and local coordination |
| Bespoke travel / travel planning | `/luxury-travel-concierge-ibiza/` | Tailored travel brief; do not create synonym pages |
| VIP services / VIP hospitality / VIP access | `/vip-services-ibiza/` | Hospitality/access requests subject to actual confirmation |
| Luxury DMC / destination management | `/destination-management-ibiza/` | Local execution for professional travel partners |
| Ibiza concierge partner / local Ibiza operator | `/partners/` | Professional handover and client relationship protection |
| One-off bespoke requests | `/bespoke-concierge-ibiza/` | Unusual individual requests, distinct from full trip planning |
| Private membership | No new product/page authorized | Research term only; no invented benefits, fees or availability |

These are intended content assignments, not proof that Google ranks a URL for a query. Competing companies are terminology references, not implied partners or endorsements.

## Next execution priorities

1. Resolve the Phase 113 PR/check/deployment state first. Confirm the exact released artifact and affected pages before updating its publication checkpoint; do not repeat the international audience-link task.
2. Audit the existing localized contact-form validation and handover for a specific unresolved issue (dates, errors and language continuity), without submitting personal data or installing tracking. Required-field presence alone is not an end-to-end delivery test.
3. Where authorized tools allow, verify the correct Ibiza VIP Move Search Console/Analytics property before claiming indexation, country demand or lead metrics. Never reuse the other brand's property or tracking ID.
4. Keep all high-intent commercial pages within the Phase 111 crawl-depth thresholds. No orphan pages, mass country pages, synonym pages, speculative redirects/noindex changes or word-count padding.
5. Update this worklog with evidence, action, PR/commit, test result, exact publication state and next unresolved priority. Separate technical improvement from measured business impact.

## Primary-source reference principles

- Google link guidance: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google local ranking: https://support.google.com/business/answer/7091
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/

Useful visible content, crawlable contextual links and matching structured data remain the basis. `llms.txt`, Service schema, IndexNow and more pages do not guarantee search/AI visibility or Maps rankings. Repeated indexing requests do not create rankings or confirmed leads.
