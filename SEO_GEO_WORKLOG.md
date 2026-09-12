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
- Phase 113 is verified merged through PR #31 at `f866e7f99fea55ba605929045a78f2e98a923449`. Deployment `34690582374` completed successfully on 12 September 2026 and the exact release artifact `10297187657` matched the tested CI output. The six FR/DE/AR international-client/private-office journeys now include same-language audience and contact routes plus clearer representative briefs. Public post-release HTTP retrieval remains independently unverified because of tool-specific retrieval restrictions; this is not treated as a site outage.
- Phase 114 targets one concrete form gap found in the exact Phase 113 release artifact: English date constraints existed in `premium.js`, but the localized `localizedConciergeForm` pages did not inherit those min-date and arrival/departure ordering checks. The proposed runtime change extends today-or-later and departure-after-arrival validation to all five contact desks with site-language custom messages, without adding a new runtime asset or submitting a form. Verify its PR/CI/deployment state before treating it as published.
- Search Console, GA4 and country-specific ranking/impression/conversion data remain unverified in this workstream. Do not infer measured commercial impact from a technical deployment.

The recurring ChatGPT task is separate from GitHub Actions: Actions validate proposed changes; they do not independently invent or publish SEO content. Each execution must re-read current state, respect permissions and avoid starting another write while a related PR/deployment is unresolved.

## Phase 113 — 12 September 2026, Europe/Madrid

Evidence: the deployed FR/DE/AR international-client pages had six audience descriptions but no in-content links to the relevant Concierge, Private Office, Partners or Private Aviation journeys. All six international/private-office pages lacked a contextual route to their existing localized contact form. Private Office's two main WhatsApp CTAs had no representative-specific prefilled context. Public retrieval independently succeeded for Home and the three international pages. This is an observed navigation/briefing gap, not a measured conversion loss.

Change: add 18 contextual links within existing audience labels and one localized contact-form link to each of the six pages. Clarify the Private Office first brief with role, dates, guest count, services, timezone, approval authority and communication preference; discourage identity/bank documents in the initial message. Prefill its two main WhatsApp CTAs per language without changing the number or sending messages. Replace the international pages' generic city list (including excluded Doha) with practical Ibiza-arrival coordination copy. No new URLs, sections, stylesheets, JavaScript, schema, tracking, prices or legal-policy changes. All modifications are restricted to the six existing main-content areas.

Affected routes: `/fr/clients-internationaux/`, `/de/internationale-kunden/`, `/ar/international-clients/`, `/fr/private-office/`, `/de/private-office/`, `/ar/private-office/`.

Tests: Python compilation passed. The new read-only audit first failed on the unmodified baseline as expected, then passed after applying the change. Full artifact comparison found exactly six changed HTML files; asset/file inventory, all other HTML, sitemap, robots, heads, navigation and footers remained byte-identical. Full local HTML graph: 156/156 sitemap URLs reachable, no missing internal targets and all 13 priority URLs at depth 0–2. Canonicals, reciprocal six-entry hreflang sets, one H1, Arabic RTL, same-language routes, form fields, WhatsApp identity/context and one CSS bundle per page passed. Twelve offline Chromium render cases at 375/1440px passed without horizontal overflow; existing form required-field validation passed. No contact request was submitted. PR CI passed, merge completed at `f866e7f99fea55ba605929045a78f2e98a923449`, GitHub Pages deployment `34690582374` succeeded and the exact release artifact was revalidated.

Execution limits: direct cloning was unavailable through the container network, so connected GitHub reads plus exact deployed artifacts were used. Public post-release retrieval remained restricted by the research tool. Those restrictions do not prove an outage and are kept separate from authenticated deployment evidence.

Research: Google Search Central AI-features and crawlable-links documentation rechecked; Bing Webmaster Guidelines also state that crawlable internal links, sitemaps and clear content support both search and AI/grounding eligibility. The change improves visible routing and useful briefing content, not an AI-specific file or guaranteed ranking signal.

## Phase 114 — 12 September 2026, Europe/Madrid

Evidence: inspection of the exact Phase 113 Pages artifact found `fArrival` and `fDeparture` as date inputs on all five contact desks. `premium.js` applied today-or-later and departure-minimum logic only to the English `#conciergeForm`; the localized ES/FR/DE/AR `#localizedConciergeForm` pages were routed by `phase107.js` but had no equivalent cross-date validation. This allowed a localized brief to pass browser validity with a past date or a departure before arrival. This is a verified form-quality issue, not evidence of lost leads.

Change: extend the existing shared `phase107.js` runtime instead of adding another script. It now sets local-today minimums for arrival/departure, makes departure follow the selected arrival date, validates again immediately before the existing qualified-lead handover, and supplies localized custom validity text in EN/ES/FR/DE/AR. The date fields remain optional; no request is submitted, no personal data is added to analytics, and WhatsApp routing/number remain unchanged.

Affected routes: `/contact/`, `/es/contacto/`, `/fr/contact/`, `/de/kontakt/`, `/ar/contact/` through their existing shared qualified-brief runtime.

Tests before PR: `node --check` passed. A read-only Phase 114 gate passed against the exact Phase 113 artifact with the proposed runtime, verifying source/runtime identity, five localized message sets, date inputs, qualified-form markers and script continuity. A separate Node DOM harness executed the runtime for EN/ES/FR/DE/AR on 12 September 2026: all five initialized arrival/departure minimums to `2026-09-12`, rejected `2026-09-11` with the correct site-language message, set departure minimum to `2026-09-20` after a future arrival selection, and rejected a `2026-09-19` departure with the correct localized ordering message. Browser engine rendering was not rerun because the installed Playwright package lacked a bundled Chromium binary; this is a test-environment limitation, not a production failure.

Research: current Bing Webmaster Guidelines explicitly keep crawlability, content clarity and user experience fundamentals relevant to both search and AI grounding. Form validation itself is primarily a conversion-quality improvement rather than a direct ranking claim. No SEO/AI ranking effect is asserted.

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

1. Resolve the Phase 114 PR/check/deployment state first. Confirm the exact released runtime and contact pages before updating its publication checkpoint; do not duplicate the date-validation task.
2. Audit one remaining contact-handover issue only if evidence supports it: phone-field semantics/autocomplete, form error focus or WhatsApp handover continuity. Do not submit a real request and do not add tracking.
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
