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
- Phase 116 targets one verified classification defect in that exact Phase 115 artifact: every required `fClientType` select defaults immediately to the first real option (`private_client`). A visitor can therefore continue without making an explicit profile choice, and an assistant, family office or travel advisor who overlooks the control can be misclassified as a private client. This is a form-quality and B2B lead-routing issue, not evidence of measured lost conversions.
- Search Console, GA4 and country-specific ranking/impression/conversion data remain unverified in this workstream. Do not infer measured commercial impact from technical deployments.

The recurring task is separate from GitHub Actions: Actions validate proposed changes; they do not independently invent or publish SEO content. Each execution must re-read current state, respect permissions and avoid starting another write while a related PR/deployment is unresolved.

## Phase 116 — 12 September 2026, Europe/Madrid

Evidence: the exact Phase 115 production artifact was downloaded and inspected. On `/contact/`, `/es/contacto/`, `/fr/contact/`, `/de/kontakt/` and `/ar/contact/`, `fClientType` is marked `required` but the first option is a real `private_client` value in every language. The HTML Standard states that a required single-select of display size 1 must have a placeholder label option, and that the placeholder is the empty-value first option used by constraint validation. Source: https://html.spec.whatwg.org/multipage/form-elements.html#the-select-element

Change: prepend one localized empty option to each existing buyer-role select: English `Select your profile`, Spanish `Selecciona tu perfil`, French `Sélectionnez votre profil`, German `Profil auswählen`, Arabic `اختر صفتك`. The placeholder is `value="" selected disabled`; the existing six role codes and labels remain unchanged. No URL, CSS, JS runtime, schema, sitemap, tracking, WhatsApp number, price, legal policy, Maps/GBP or other-brand data changes.

Affected routes: `/contact/`, `/es/contacto/`, `/fr/contact/`, `/de/kontakt/`, `/ar/contact/`.

Pre-PR tests: the new read-only audit fails on the untouched Phase 115 artifact because only six real role options exist and no empty placeholder is present, then passes on the patched artifact. Offline Chromium constraint-validation checks on all five forms confirm the initial role value is empty, `validity.valueMissing=true`, and the form is invalid after the other required name/phone fields are filled; choosing `assistant` makes the role control valid and the otherwise-complete form valid. No request was submitted and no network handover was performed. Full repository CI remains the release gate.

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

1. Resolve the Phase 116 PR/check/deployment state first. Confirm the exact release artifact and five contact pages before calling explicit buyer-role selection published; do not duplicate this role-field task.
2. After Phase 116, audit error focus and form → WhatsApp handover continuity only if a concrete defect can be reproduced. Do not submit a real request and do not add tracking.
3. Where authorized tools allow, verify the correct Ibiza VIP Move Search Console/Analytics property before claiming indexation, country demand or lead metrics. Never reuse the other brand's property or tracking ID.
4. Keep all high-intent commercial pages within the Phase 111 crawl-depth thresholds. No orphan pages, mass country pages, synonym pages, speculative redirects/noindex changes or word-count padding.
5. Keep technical improvements separate from measured business impact; update this file and the release PR with exact evidence.

## Primary-source reference principles

- HTML select / required constraint validation: https://html.spec.whatwg.org/multipage/form-elements.html#the-select-element
- Google crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google local ranking: https://support.google.com/business/answer/7091
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/

Useful visible content, crawlable contextual links, accurate form semantics and matching structured data remain the basis. `llms.txt`, schema, IndexNow and more pages do not guarantee search/AI visibility, Maps rankings or leads.