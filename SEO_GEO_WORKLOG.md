# Ibiza VIP Move — SEO / GEO worklog

Updated: 12 September 2026. Repository: `abotamarin51-jpg/ibizavipmove.com`.

## Scope and safeguards

Improve the existing Ibiza website for qualified private-client and international B2B enquiries. The aspiration is international recognition for luxury concierge IN IBIZA, not a claim of a guaranteed worldwide ranking.

Only this domain/repository is in scope. Do not mix Ibiza Private Drivers, its Business Profile or its Analytics property. Google Business Profile/Maps edits, DNS/MX changes, outreach, paid links, advertising, association registrations and new membership products are outside this workstream. Local signals must describe real Ibiza service coverage, not fictional offices abroad. No invented reviews, ratings, affiliations, operating results, client identities, addresses, prices or availability guarantees.

Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN, FR, DE, AR. Preserve existing Spanish; do not expand Spain/Italy targeting. These are audience priorities, not verified search-volume estimates.

## Latest checkpoint

- Phase 111 accepted at `16f3fcced839b31f5a2b42034d615ee83654e8d0`: final generated-HTML graph verified 156 sitemap URLs reachable, with 13 priority commercial routes within 0–2 crawlable HTML links of Home. This is not proof of Google indexation, rankings, traffic, conversions or Maps position.
- Phase 112 merged through PR #30 at `010baac97f6891c02571e2886937c79d6ebf02dd`, deployment `34689850167`: FR/DE/AR Partner pages strengthened for DMC/destination-management/private-travel intent without new URLs.
- Phase 113 merged through PR #31 at `f866e7f99fea55ba605929045a78f2e98a923449`, deployment `34690582374`: FR/DE/AR international-client/private-office journeys gained same-language audience/contact routes and clearer representative briefs.
- Phase 114 merged through PR #32 at `c5268deda041b997f21c48b578caeffcb3cc01f2`, deployment `34692434048`, release artifact `10297520685`: all five contact desks share today-or-later and departure-after-arrival validation with localized messages.
- Phase 115 merged through PR #33 at `4b85e41ba396f02ee9164f71a027a53e66d5b3fa`. Deployment `34695052164` completed successfully; exact GitHub Pages artifact `10297803160` has digest `sha256:86011c6ad35835537a86203ecb43b837abf01203f859a9f41b085f92229ce20e`. EN/ES/FR/DE/AR required phone inputs use `type="tel"`, `inputmode="tel"` and `autocomplete="tel"` without a rigid country pattern.
- Phase 116 merged through PR #34 at `68958d3315212ab3f321e35aea4ecf5782656447`. Deployment `34697823273` completed successfully; exact GitHub Pages artifact `10298674084` has digest `sha256:5a09b89514772aabf1bec174ef2f5d20f5e11466fc96673e53834af3f97cc1ef`. Five required `fClientType` selects now start from localized empty placeholders so visitors must explicitly choose their buyer profile.
- Phase 117 addresses one verified international-date defect in that exact Phase 116 release artifact: date eligibility currently uses the visitor device timezone through `getTimezoneOffset()`. Around midnight, a visitor in North America or East Asia can therefore see a different minimum arrival date from the calendar day actually in force in Ibiza. This is a form-quality issue for international travel planning, not evidence of measured lost conversions.
- Search Console, GA4 and country-specific ranking/impression/conversion data remain unverified in this workstream. Do not infer measured commercial impact from technical deployments.

The recurring task is separate from GitHub Actions: Actions validate proposed changes; they do not independently invent or publish SEO content. Each execution must re-read current state, respect permissions and avoid starting another write while a related PR/deployment is unresolved.

## Phase 116 — 12 September 2026, Europe/Madrid

Evidence: the exact Phase 115 production artifact was downloaded and inspected. On `/contact/`, `/es/contacto/`, `/fr/contact/`, `/de/kontakt/` and `/ar/contact/`, `fClientType` was marked `required` but the first option was a real `private_client` value in every language. The HTML Standard states that a required single-select of display size 1 must have a placeholder label option, and that the placeholder is the empty-value first option used by constraint validation. Source: https://html.spec.whatwg.org/multipage/form-elements.html#the-select-element

Change: prepend one localized empty option to each existing buyer-role select: English `Select your profile`, Spanish `Selecciona tu perfil`, French `Sélectionnez votre profil`, German `Profil auswählen`, Arabic `اختر صفتك`. The placeholder is `value="" selected disabled`; the existing six role codes and labels remain unchanged. No URL, CSS, JS runtime, schema, sitemap, tracking, WhatsApp number, price, legal policy, Maps/GBP or other-brand data changes.

Release: PR #34 passed the repository CI, merged at `68958d3315212ab3f321e35aea4ecf5782656447`, and deployed successfully in run `34697823273`. Exact production artifact `10298674084` was used as the Phase 117 baseline. This verifies publication mechanics and artifact content, not rankings or lead impact.

## Phase 117 — 12 September 2026, Europe/Madrid

Evidence: the exact Phase 116 production runtime calculates `localToday` from the visitor device offset (`new Date(now.getTime()-now.getTimezoneOffset()*60000)`), then uses that value for `fArrival`/`fDeparture` minimums and past-date checks. For an Ibiza-only service this can disagree with the island calendar day: for example, at `2026-09-12T22:30:00Z` Ibiza is already `2026-09-13`, while New York is still on 12 September; at `2026-09-12T21:30:00Z` Tokyo is already on 13 September while Ibiza is still on 12 September. MDN confirms `Intl.DateTimeFormat` supports an explicit IANA `timeZone` option, and Ibiza follows mainland Spain time. References: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat and https://www.timeanddate.com/time/zone/spain

Change prepared on branch `seo/phase117-ibiza-date-validation`: the existing qualified-brief runtime now derives the service calendar key with `Intl.DateTimeFormat(... timeZone: 'Europe/Madrid').formatToParts(...)`, and all arrival/departure minimum and past-date checks use that Ibiza date. The same existing JS file remains in use; contact pages are cache-busted from `phase107.js?v=107` to `phase107.js?v=117`. No new URL, stylesheet, external script, tracking event, schema, sitemap entry, WhatsApp number, price, policy, Maps/GBP change or other-brand data is introduced.

Affected routes: `/contact/`, `/es/contacto/`, `/fr/contact/`, `/de/kontakt/`, `/ar/contact/`.

Pre-PR tests: a new Phase 117 read-only gate fails on the untouched Phase 116 release because the Ibiza timezone token is absent, then passes after applying the runtime patch and five cache-busted references. `node --check` passes on the modified runtime. Date fixtures verify `Europe/Madrid` resolves `2026-09-12T22:30:00Z` to `2026-09-13`, `2026-09-12T21:30:00Z` to `2026-09-12`, and `2026-12-31T23:30:00Z` to `2027-01-01`. Full repository CI is still required before merge. No form or WhatsApp request was submitted.

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

1. Resolve the Phase 117 PR/check/deployment state first. Confirm the exact release artifact and five contact pages before calling Ibiza-time validation published; do not duplicate this date-timezone task.
2. After Phase 117, audit form → WhatsApp handover continuity only if a concrete defect can be reproduced. Do not submit a real request and do not add tracking.
3. Where authorized tools allow, verify the correct Ibiza VIP Move Search Console/Analytics property before claiming indexation, country demand or lead metrics. Never reuse the other brand's property or tracking ID.
4. Keep all high-intent commercial pages within the Phase 111 crawl-depth thresholds. No orphan pages, mass country pages, synonym pages, speculative redirects/noindex changes or word-count padding.
5. Keep technical improvements separate from measured business impact; update this file and the release PR with exact evidence.

## Primary-source reference principles

- HTML select / required constraint validation: https://html.spec.whatwg.org/multipage/form-elements.html#the-select-element
- MDN Intl.DateTimeFormat / explicit timeZone: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat
- Google crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google local ranking: https://support.google.com/business/answer/7091
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/

Useful visible content, crawlable contextual links, accurate form semantics and matching structured data remain the basis. `llms.txt`, schema, IndexNow and more pages do not guarantee search/AI visibility, Maps rankings or leads.