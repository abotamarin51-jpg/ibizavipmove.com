# Ibiza VIP Move — SEO / GEO worklog

Updated: 14 September 2026, 21:50 Europe/Madrid. Exclusive repository: `abotamarin51-jpg/ibizavipmove.com`; exclusive website: `https://ibizavipmove.com/`.

## Scope, continuity and release safeguards

Improve discovery, usability and qualified enquiries for real services IN IBIZA. Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN/FR/DE/AR. Preserve existing Spanish without expanding Spain/Italy targeting. No invented locations, memberships, affiliates, operating outcomes, availability or client details; no mass synonym/country pages or word-count padding.

Do not touch Ibiza Private Drivers, its website, data, Analytics or business listing. Do not mix this task with B2B contact prospecting. No Google Business Profile/Maps edits, outreach, emails, association registrations, paid links, ads/spending, DNS/MX, prices, commissions, billing, legal policies or unverified tracking. Never publish Juan's private address or identifiable client itineraries.

Read live main, recent commits, open PRs, active workflows/deployments and this log before any write. If another execution is active or cannot be excluded, remain read-only. Use a new branch from verified main and a small reversible PR; do not write directly to main or weaken existing gates. Review the exact diff/head/base and passing CI before merge, then verify production and relevant contact paths without submitting messages/forms. Do not publish when necessary validation is missing. Never claim zero risk, guaranteed rankings, AI inclusion or leads.

## Preserved history

The previous root worklog is preserved byte-for-byte as `SEO_GEO_WORKLOG_ARCHIVE_THROUGH_151.md`, Git blob `5181d6c596d9b4d8a266d7d15c003528654926c1`. Earlier archives through 130, 135 and 144 remain unchanged. Their historical next-step instructions do not override newer verified state. Existing detailed implementation evidence is retained in merged PRs and prior control files.

Do not repeat completed multilingual audience/footer/contact/wordmark routing, form validation, service-model, truthful-freshness, legacy aviation routing, vocabulary, schema cleanup, contextual-link or priority-image improvements unless a regression is demonstrated. The website keeps 156 sitemap canonicals; check the current inventory rather than using a historical count as evidence.

Intent ownership is unchanged: Home = broad luxury concierge; `/private-concierge-ibiza/` = connected multi-service stays; `/luxury-lifestyle-management-ibiza/` = ongoing stay coordination; `/personal-concierge-ibiza/` = direct assistance; `/luxury-travel-concierge-ibiza/` = private travel management/bespoke planning; `/vip-services-ibiza/` = conditional hospitality/access; `/private-client-services-ibiza/` = principals/PAs/family offices; `/destination-management-ibiza/` = local DMC execution; `/partners/` = professional handover; `/bespoke-concierge-ibiza/` = unusual individual requests. No private membership product is authorized.

## Verified starting state for this iteration

Main: `34312eedd1e087cd1cee8d9afb078a6dfd5af442`. Phase 154 deployment `34804314085` completed successfully; production artifact `10332911737` has independently verified SHA-256 `dd4fee09afe491fa360e1cdf845081d4c3e064eb26a7f3c64cc44fc94bfc508a`. No open PR or queued/in-progress workflow was found before this branch was created. Phase 154 links the existing FR/DE/AR Home yacht wording to the matching service pages; do not repeat it. Consult PR #94 for its detailed diff and release evidence. The archived root ends at Phase 151; PR #92/#93/#94 retain the intervening change records.

## Indexation handling

Canonical Wizard property: `https://ibizavipmove.com/` only; never add the domain-property metrics to it. Read the tracker and saved inspections before spending inspection quota. The inventory has previously been inspected; pending checks are not the same as non-indexed URLs. Preserve intentional noindex/redirect/canonical exclusions. An impression-derived count or sitemap API indexed=0 is not a complete index census. Crawled-not-indexed alone does not establish a cause.

Keep the prior reassessment hold for `/destination-management-ibiza/`, `/luxury-travel-concierge-ibiza/` and `/de/private-aviation-ibiza/` until 16 September unless a new HTTP/robots/noindex/canonical/rendering fault is demonstrated. Do not churn freshly changed pages. URL inspection is not an indexing request. Do not misuse the special-purpose Google Indexing API, repeatedly submit unchanged sitemaps, or treat IndexNow as proof of indexing. When a legitimate request requires Search Console UI, state the exact manual action and do not mark it executed without evidence.

Private tracker metrics and per-URL inspection histories stay outside this public repository. The tracker digest setting was still enabled in this iteration; no legitimate digest-toggle action was available in the discovered interface. No emails or additional notifications were sent or enabled.

## Phase 155 — German Partners mobile reflow — PUBLISHED

Opportunity: `/de/partners/` is an existing commercial B2B page. Current Wizard live audit returned HTTP 200, self-canonical, indexable, one H1, six hreflang entries and no schema errors. The reviewed defect is mobile usability, not an established indexing blockage.

The exact production artifact reproduced document scrollWidth 427 at viewport widths 320, 375 and 390. Long German words increased the intrinsic minimum width of the B2B overview grid children. A page-local style limited to max-width:600px allows those children to shrink and long words to wrap (`min-width:0; overflow-wrap:anywhere; hyphens:auto`). No global overflow hiding, clipping, reduced font size, shared-CSS change or new dependency is used.

Frozen-output validation: only `de/partners/index.html` changes; removing the one style block restores it byte-for-byte. Visible text, all links, WhatsApp/tel/email, forms, metadata, schema, hreflang and sitemap are unchanged. The new gate fails on the unpatched artifact and passes after the enhancer; rerun changes nothing. Scope is isolated from German Private Office and every other page. Integration adds one import and one call to each existing Phase 151 enhance/audit path; existing gates remain enabled.

Offline Chromium with production CSS/fonts/resources and JavaScript: after the patch, scrollWidth equals viewport width at 320/375/390/768/980/981/1440; visible body text remains identical; no JavaScript errors in fresh page contexts. Before/after mobile screenshots were reviewed. This is artifact-based offline rendering, not a live-browser or Safari certification. External navigation is unavailable in this environment; no message/form was submitted.

Release: PR #95 passed CI run `34805250041` and was merged as `dad231afd53957925e1811ebc9a437d67ba358c8`. Deployment run `34825054088` completed successfully. Production artifact `10340480600` has SHA-256 `a325cda4a495b8b8b815f6ce616030bfcc007b32bcab0974addaef5ae4c0015c`, independently matched after download. The artifact contains one exact Phase 155 marker on `/de/partners/`, retains 156 sitemap canonicals and preserves the existing WhatsApp, telephone and partnership-email routes. A post-deploy Wizard live audit returned HTTP 200, no redirect, self-canonical, indexable, one H1, six hreflang entries, valid structured data and no high/medium issues. The only reported issue is the pre-existing low-severity long-title warning. No form or message was sent.

The demonstrated benefit is mobile reflow/readability. Indexing, ranking, AI visibility, conversions, leads and revenue impact remain unmeasured. Next: keep the established 16 September reassessment hold for the three Phase 134 URLs unless a new technical failure appears; prioritize fresh Wizard evidence of a real commercial-page fault before another cosmetic or image change.

## Primary references checked for this correction

- https://www.w3.org/WAI/WCAG21/Understanding/reflow
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overflow-wrap

Do not equate a targeted reflow fix with full WCAG conformance or a Google ranking improvement.


## Indexation diagnostic — Cala Jondal & Es Cubells — 14 September 2026, 11:55 Europe/Madrid

Start state: main `d396c1a6a94f16b10ae5ea83102ae47ae14ff3e8`; no open PR or queued/in-progress workflow. The latest website deployment remained the successful Phase 155 run `34825054088`. Canonical Wizard property remained `https://ibizavipmove.com/`; the tracker had no new sweep or count change, so no URL inspection was repeated and no sitemap was resubmitted. The enabled tracker email digest remains unchanged because the available interface still exposes no legitimate digest toggle.

One local commercial page was reviewed: `/private-concierge-cala-jondal-es-cubells-ibiza/`. Private Search Console inspection details are not duplicated in this public record. Live Wizard audit returned HTTP 200, no redirect, indexable self-canonical, one H1, two intentional hreflang entries (English and x-default; no untranslated alternate is invented), 667 words, valid structured data, complete image alt coverage and zero audit issues. The indexed `/private-concierge-ibiza/` comparator was also technically clean.

Exact Phase 155 production-artifact graph analysis places the target at crawl depth 2 from Home. Eight other internal pages link to it, including the main private-concierge, luxury-lifestyle-management, villas, chauffeur, private-client-services, security, dining/nightlife and yacht pages. Five-word-shingle similarity against the three other local concierge pages was 0.275–0.279 and 0.072 against the general private-concierge page; this does not demonstrate a near-duplicate blocker. Artifact-only contact verification retained five WhatsApp links, two telephone links and one Ibiza VIP Move email route; no form or message was sent.

Decision: **no website code/content change**. A rewrite, invented translation or extra schema would be speculative. If an owner chooses to request indexing, the legitimate manual action is Search Console → URL Inspection → enter the exact canonical URL → Test Live URL → Request Indexing once; this was not executed by Wizard and is not guaranteed to produce indexing. Next: preserve the 16 September hold for the three Phase 134 URLs unless a new technical fault appears, and prioritize fresh tracker changes or a demonstrated conversion/indexability failure over cosmetic churn.


## Confirmed indexation change — German private aviation — 14 September 2026, 21:50 Europe/Madrid

Start state: main `b3f134712ed459a5ca8a2fc080ec4caa63801d3c`; no open PR or queued/in-progress workflow. The latest website deployment remains the successful Phase 155 run `34825054088`; this iteration makes no website code or content change.

On the canonical Wizard property `https://ibizavipmove.com/`, tracker `b45661cd-b57b-4a32-8ae5-8bab1cac107b` completed a fresh sweep at `2026-09-14T19:51:07Z`. `/de/private-aviation-ibiza/` changed from `Crawled - currently not indexed` to `Submitted and indexed` (PASS, indexing allowed), checked at `2026-09-14T19:42:10Z` after Google crawled it at `2026-09-13T23:49:18Z`. Tracker totals changed from 97 indexed / 59 not indexed to 98 indexed / 58 not indexed; pending, errors and warnings remain zero. This tracker is evidence for the monitored inventory, not a complete census of Google's index.

The two remaining Phase 134 URLs are unchanged: `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/` both remain `Crawled - currently not indexed`, last crawled on 12 September and rechecked in this sweep. Their established reassessment date remains 16 September. No repeat inspection, indexing request, sitemap submission, IndexNow submission, email or tracker-setting change was made. The enabled email digest remains unchanged because no legitimate toggle is exposed.

Decision: **documentation only; no website modification or deployment**. The confirmed indexation improvement is a Google status change, not proof of ranking, AI visibility, traffic or lead impact. Next: re-evaluate the two remaining held commercial URLs from 16 September, unless a new technical failure appears first.
