# Ibiza VIP Move — SEO / GEO worklog

Updated: 13 September 2026 (Europe/Madrid). Repository: `abotamarin51-jpg/ibizavipmove.com`.

## Scope and safeguards

Improve qualified private-client and international B2B enquiries for real services IN IBIZA. International recognition is an aspiration, never a guaranteed ranking. Only this domain/repository is in scope; never mix Ibiza Private Drivers, its Google Business Profile or Analytics.

Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Languages: EN/FR/DE/AR; preserve existing Spanish without expanding Spain/Italy targeting. No fictional foreign offices, mass country/synonym pages, unauthorized membership products or word-count padding.

No GBP/Maps edits, DNS/MX changes, outreach, association registrations, paid links, ads, spending, price/commission/billing or legal-policy changes. Do not publish private client identities, identifiable itineraries, private addresses or invented reviews, awards, affiliations, operating results or availability. Do not install tracking without verified ownership/consent or send personal data to Analytics. Only link a previously verified exact Ibiza VIP Move Maps profile.

Read current main, open PRs, worklog and deployments before deciding. Use small reversible branch/PR changes, preserve existing tests, validate exact diff/head/base/checks, and verify deployment and output before calling a change published. Do not start concurrent writes or churn pages simply because another iteration runs.

## History and evidence preservation

The complete former worklog through Phase 130 is preserved BYTE-FOR-BYTE in `SEO_GEO_WORKLOG_ARCHIVE_THROUGH_130.md`, Git blob `f4600c7c049ec2e2590789c3ed9599d5d693de9a` (22,832 bytes). It was read in bounded line ranges before this compact continuation was written. Earlier implementation, PR, commit, deployment and artifact evidence remains there; no history was discarded. Its older next-step and unverified-access statements are historical, not current instructions.

Resolved work: 111 crawl depth; 112–113 multilingual B2B/audience routing; 114–120 date/phone/profile validation; 121 sitemap dates; 122 private-client rather than unauthorized membership wording; 123 Partners proof consolidation; 124 Article freshness; 125 priority-image preload alignment; 126 UK/international car terminology; 127 historical private-jets route; 128 Services model links; 129 four topic-specific Arabic articles; 130 German event terminology. Do not recreate these tasks or add synonym URLs.

## Latest publication checkpoints

- Phase 130: PR #52, merge `b604f6bb8ef507866187da25e31b23c93a3f46dc`, deployment `34744047488`, artifact `10313269080`: one existing German events page aligned with verified query wording. Full details in the archive.
- Phase 131: PR #54, merge `a70871ba741afd2e4b3c091e8b606742938458d0`: five contact forms require an explicit primary service with a localized empty placeholder plus the unchanged 12 real service choices. The current Phase 132 production artifact independently confirms this output. This entry closes the missing worklog checkpoint; it is not a new implementation.
- Phase 132: PR #55, merge `91967c87168d7881f9d8a12845bc2f80f99149bd`, successful deployment `34750310254`, artifact `10315587780`, SHA256 `656e8ab42a481dbae3b78f0567b3a4914ba78d0ebb348c6d455729a23c3da64d`. The exact artifact was downloaded and its hash checked in this execution. Independent public retrieval on 13 September now shows the new descriptive `/services/` H1 and the six Phase 128 service-model routes. Public propagation is confirmed; Google's next recrawl and performance effect are not.

## Phase 133 — single contact-form validation owner

Date: 13 September 2026, Europe/Madrid. Branch: `phase133-single-contact-form-owner`; base: the Phase 132 merge above. Initial check found no open PRs and a successful latest deployment.

Evidence: offline Chromium execution of the exact published scripts reproduced silent departure-date deletion on `/contact/`: after choosing arrival 20 December and departure 22 December, changing arrival to 24 December erased departure and left that optional field valid. The old shared-script change listener was still active beside the modern qualified-form runtime. The four localized forms also retained an obsolete inline submission script with a JavaScript syntax error; their modern runtime still worked. These are reproduced client-side defects, not an inferred conversion loss.

Change: bypass the legacy English form block only when the form has the existing `data-ivm-qualified-brief` marker. Remove only the obsolete inline form script from the four localized pages. Cache-version the existing shared-script reference on the five contact pages. Keep the modern `phase107.js` runtime, all validation messages, date rules, service/profile choices, contact destination and analytics payload code unchanged. No new JS/CSS asset, URL or tracker.

Affected HTML: `/contact/`, `/es/contacto/`, `/fr/contact/`, `/de/kontakt/`, `/ar/contact/`. Shared asset: `/assets/premium.js`; its sole code change is the legacy-handler guard. Non-form behavior is unchanged.

Local tests: the new gate rejected the unchanged baseline, then passed after enhancement; Python compilation and shared/inline JavaScript syntax passed. The enhancer is idempotent and validates expected markers before writing. Exact output comparison changed only five contact HTML files and the shared JS; all other files, sitemap/robots, CSS/images and modern form runtime remained byte-identical. Ten offline Chromium page/viewport cases at 375/1440px passed with no horizontal overflow or script errors, departure preserved, localized date error and native focus on the invalid departure field. Required role/service, whitespace/phone and optional-date checks passed. Across those cases, 120 valid service handovers produced exactly one locally captured WhatsApp destination and one existing local event each; test values were absent from the analytics payload. The navigation assignment was replaced ONLY in the test harness by a recorder; all network requests were blocked. No enquiry or message was sent. This is not a WhatsApp delivery, live browser, screen-reader or field Core Web Vitals measurement.

Research: W3C WAI forms validation/notifications recommends understandable errors and focusing the invalid field. Google/Bing continue to ground search and AI visibility in ordinary crawlability, useful visible content and truthful structured data, not additional AI files or guaranteed ranking tricks.

Status at this commit: locally validated implementation awaiting full PR CI and release verification. The PR conversation will record the exact commit/run/artifact and final publication state; read that evidence before treating Phase 133 as published. No existing audit was reduced. Both CI and deployment run the new transform and read-only gate before the existing final gates.

## Measurement and next priority

GSC Wizard currently lists the exact `https://ibizavipmove.com/` property. Prior owner exports and connected inspections are distinct evidence sources; keep private metrics outside this public repository. Do not reuse the other brand's property. This iteration does not establish fresh rankings, impressions, indexation changes, conversions or revenue, and does not claim verified GA4 attribution.

First resolve Phase 133's PR/deployment state and validate its exact output. Afterwards prioritize settled Search Console evidence and unresolved commercial-page coverage, rather than further form microchanges or editing recently changed titles before Google recrawls. Maintain 156 sitemap canonicals and the existing 13 priority routes within 0–2 crawlable HTML links from Home. Indexable is not indexed; a successful deployment or IndexNow response is not a search/AI inclusion or leads guarantee.

## Intent ownership — reuse existing pages

Home owns broad luxury concierge; `/private-concierge-ibiza/` owns connected multi-service stays. Use `/luxury-lifestyle-management-ibiza/` for ongoing stay coordination, `/personal-concierge-ibiza/` for direct assistance, `/luxury-travel-concierge-ibiza/` for private travel management/bespoke travel/planning, `/vip-services-ibiza/` for conditional hospitality/access requests, `/private-client-services-ibiza/` for principals/PAs/family offices, `/destination-management-ibiza/` for local DMC execution, and `/partners/` for professional handover. `/bespoke-concierge-ibiza/` remains for unusual individual requests. No private membership is authorized. Preserve localized routes and real Ibiza service-area information without inventing locations.

## Primary references

- https://www.w3.org/WAI/tutorials/forms/validation/
- https://www.w3.org/WAI/tutorials/forms/notifications/
- https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#the-constraint-validation-api
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a

The archive retains the additional primary references and all historical checkpoints.

## 13 September 2026 — Phase 134: commercial indexation baseline (read-only)

This checkpoint supersedes the pending Phase 133 release status above. PR #56 merged as `a517107e247bae9557914a08fee76bf589e6306c`; deployment `34752466429` and its actual Pages step are successful. The previously downloaded production archive `10315752532` was available locally and its SHA256 was reverified as `8a77319ce44488286e784c6d0b64fbf761c954da174fc77c18c3a5a68e368745`. No new browser handover tests are claimed in Phase 134. Full Phase 133 release qualifications remain in PR #56 comment `5652775930`.

At 12:48–12:49 CEST, verified the exact connected GSC property and queried Google URL Inspection for the six existing English service-model pages plus Partners and Private Concierge. Inspections were persisted by GSC Wizard; their full per-URL statuses and crawl timestamps are retained in the private owner report, not committed here. These are Google's recorded index states, not live-test crawls, and this first sample does not establish an improvement over an earlier baseline.

Follow-up live on-page checks of `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/` both returned HTTP 200, self-canonicals, one H1, no HTML noindex, mobile viewport, internal links and no critical/high findings from that auditor. Their visible copy distinguishes professional local execution from traveller-led trip planning. The auditor's missing-logo and description-length warnings do not establish the reason for an index exclusion. Google's Organization documentation does not make logo a universal required indexing field; do not add speculative schema or rewrite recently changed pages merely to satisfy that generic warning.

Independent frozen-artifact graph check: 156 unique sitemap URLs, all reachable from Home; no orphan in that inventory. All eight inspected commercial routes are within one or two crawlable HTML links of Home and have a single self-canonical and H1. This validates generated navigation, not live Googlebot fetches or field mobile performance. No content, links, schema, redirects, sitemap, dates, form code or tracking changed. No recrawl/IndexNow submission was made. A separate web-reader Services fetch failed and direct container networking could not resolve GitHub; neither is evidence of a site outage. Authorized GitHub reads and the connected live on-page audit remained available.

Decision: retain the published site unchanged and establish the commercial indexation baseline. This PR is documentation-only, appending to the completely read worklog; previous history and all runtime/workflow files are preserved. Review the exact one-file diff before merge. Existing workflow path filters exclude Markdown, so no site build/deployment is expected and no new CI-success claim is made.

Next priority: in future executions, compare these stored inspections after a meaningful processing interval (not repeated hourly checks), alongside settled per-page Search Console demand. Revisit on or after 16 September unless a new concrete failure appears earlier. Prioritize DMC and Luxury Travel Concierge review if exclusion persists; persistence alone is not proof of a technical defect. Google says crawling/processing can take days to weeks and repeated recrawl requests do not speed it up: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl . AI inclusion likewise relies on normal indexing/content requirements, without guarantees. No ranking, traffic, conversion or revenue uplift is inferred.
