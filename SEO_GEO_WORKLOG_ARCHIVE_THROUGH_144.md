# Ibiza VIP Move — SEO / GEO worklog

Updated: 13 September 2026 (Europe/Madrid). Repository: `abotamarin51-jpg/ibizavipmove.com`.

## Scope and safeguards

Improve qualified private-client and international B2B enquiries for real services IN IBIZA. International recognition is an aspiration, never a guaranteed ranking. Only this domain/repository is in scope; never mix Ibiza Private Drivers, its Google Business Profile or Analytics.

Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN/FR/DE/AR. Preserve existing Spanish without expanding Spain/Italy targeting. No fictional foreign offices, mass country/synonym pages, unauthorized membership products, keyword stuffing or word-count padding.

No GBP/Maps edits, DNS/MX changes, outreach, memberships/association registrations, paid links, ads/spending, price/commission/billing or legal-policy changes. Do not publish private client identities, identifiable itineraries, private addresses or invented reviews, awards, affiliations, operating results or availability. Do not install tracking without verified ownership/consent or send personal data to Analytics.

Read current main, open PRs, worklog and deployments before deciding. Use small reversible branch/PR changes, preserve existing tests, validate exact diff/head/base/checks, and verify deployment/output before calling a change published. Indexable is not indexed; deployment, schema, llms.txt or IndexNow do not guarantee search/AI visibility or leads.

## Preserved history

- `SEO_GEO_WORKLOG_ARCHIVE_THROUGH_130.md` preserves the original history through Phase 130 byte-for-byte.
- `SEO_GEO_WORKLOG_ARCHIVE_THROUGH_135.md` preserves the immediately previous root worklog byte-for-byte (Git blob `44ad404c1e206f0b76d9b1188ff57ba91786fb47`). It includes Phases 131–135 and the Phase 134 commercial-indexation baseline. Older next-step statements in archives are historical, not current instructions.

Resolved work includes: Phase 111 crawl depth; 112–113 multilingual B2B/audience routing; 114–120 form/date/phone/profile validation; 121 sitemap freshness; 122 private-client wording; 123 Partners proof consolidation; 124 Article freshness; 125 priority-image preload alignment; 126 car hire/rental terminology; 127 historical private-jets route; 128 Services model links; 129 Arabic editorial specificity; 130 German event terminology; 131 explicit service choice; 132 Services H1 clarity; 133 single form-validation owner; 134 indexation baseline; 135 localized Services contact routing. Do not recreate these tasks or add synonym URLs.

## Phase 134 measurement baseline remains active

On 13 September the verified Ibiza VIP Move Search Console property was used to inspect the six English service-model pages plus Partners and Private Concierge. The per-URL private results remain outside this public repository. `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/` had recently been crawled but not selected for indexing; live on-page checks showed HTTP 200, self-canonical, one H1, no HTML noindex and no critical/high technical finding. Reassess on or after 16 September unless a new concrete defect appears earlier. Do not repeatedly rewrite these pages or request hourly recrawls.

## Phase 136 — localized authority/editorial footer routing

Published 13 September 2026. PR #61 merged as `cbe10c92e9db173ba8e21e41707e0516ff0ccda5`; production deployment `34758389618` succeeded. Exact production artifact `10318520366` has digest `sha256:a1aae766ad78ca7455b02dfe56a6c44d7c9fe17e5e724059b4b4b4aac7a2c2b3`.

Change: 27 FR/DE/AR authority/editorial pages now route five legacy footer links to their existing same-language Services, Concierge, Partners, About and Contact equivalents. This changed hrefs only; copy, legal links, schema, sitemap, tracking, WhatsApp, prices and service scope were preserved. The 156-URL sitemap and priority crawl-depth safeguards passed. This is technical navigation/localization coherence, not measured ranking, traffic or lead uplift.

## Phase 137 — localized contact Explore routing

Published 13 September 2026. Evidence from the exact Phase 136 production artifact showed `/fr/contact/`, `/de/kontakt/` and `/ar/contact/` each retaining three legacy Explore links to English destinations even though exact localized equivalents already existed. The affected routes were Private Office, The Ibiza Black Book and International Clients: nine hrefs total, six commercial and three editorial.

Change: PR #62 replaces only those nine hrefs with `/fr/...`, `/de/...` and `/ar/...` equivalents. Visible labels, form runtime/validation, WhatsApp destination, analytics behavior, canonical, H1, schema, sitemap, legal policy, prices and service scope remain unchanged. No new URL, redirect, asset, tracker or market page was created.

Validation: PR CI `34761278121` / job `103734437681` succeeded, including the new Phase 137 gate and all existing final audits. PR #62 merged as `ccaed6e26d34948a92991c08e8b65a8f94940730`. Production deployment `34761345495` / job `103734619847` succeeded, including GitHub Pages and the existing IndexNow step. Exact production artifact `10319515260` has SHA256 `3b4c33c1f5cb7a1887655838aaa51ce88992ee3da65b2ce0c40563343ffa9388`.

Production artifact verification confirms all three localized contact pages now contain the intended same-language Explore destinations, retain one self-canonical/H1, their qualified brief form and the existing official WhatsApp destination, while the sitemap remains 156 unique URLs. Comparison with the Phase 136 artifact changes the three intended contact HTML outputs plus the known clean-build JPEG encoder variance on `assets/images/villa.jpg`; no image-source code changed. A public reader immediately after release still resolved cached English destinations, so a second independent propagation check remains unconfirmed and is not treated as an outage.

Impact: technical navigation/localization and internal-link coherence only. No ranking, Google indexation, AI visibility, traffic, lead or revenue uplift is inferred from this release.

## Phase 138 — localized brand wordmark home routing

Published 13 September 2026. Exact Phase 137 production evidence showed 45 FR/DE/AR pages whose clickable Ibiza VIP Move `wordmark` still linked to the English homepage `/`, even though `/fr/`, `/de/` and `/ar/` already existed. Each language had 27 wordmark-bearing pages: 15 with the legacy English-home href and 12 already localized. Explicit English language-switch links were separate and preserved.

Change: PR #64 adds a final post-processing step that changes only those wordmark hrefs to the matching localized homepage, plus a read-only regression gate. No visible copy, URL, canonical, hreflang, schema, sitemap, form, WhatsApp destination, tracking, price, legal policy or service scope changed.

Validation: local frozen-artifact testing changed exactly 45 generated HTML files, one href per page, and was idempotent. PR CI `34763995109` succeeded; preview artifact `10320110000` has digest `sha256:86856847ec21621c84e5f327588817e995e9a4f3cdb9e6f1a74293b410b732f2`. PR #64 merged as `983e691811fbf3a141017a2ea644a40976be7c77`. Production deployment `34764056200` succeeded, including GitHub Pages and the existing IndexNow step. Exact production artifact `10319293520` has digest `sha256:6101bd68f273dff58c92344d53c7f07245ad9bbcf26b5555dbaf3a96baa37ab0`.

Production verification confirms all 81 FR/DE/AR wordmark anchors now route to the same-language homepage, explicit non-wordmark English routes remain available, and the sitemap remains 156 unique URLs. Impact is technical navigation/internal-link coherence only; no ranking, indexation, AI visibility, traffic, lead or revenue uplift is inferred.

## Intent ownership — reuse existing pages

Home owns broad luxury concierge; `/private-concierge-ibiza/` connected multi-service stays; `/luxury-lifestyle-management-ibiza/` ongoing stay coordination; `/personal-concierge-ibiza/` direct assistance; `/luxury-travel-concierge-ibiza/` private travel management/bespoke planning; `/vip-services-ibiza/` conditional hospitality/access; `/private-client-services-ibiza/` principals/PAs/family offices; `/destination-management-ibiza/` local DMC execution; `/partners/` professional handover. `/bespoke-concierge-ibiza/` remains for unusual individual requests. No private membership is authorized.

## Current primary-reference principles

Google Search Central says crawlable `<a href>` links help Google discover internal pages and that useful internal links help people and Google understand a site. Bing Webmaster Guidelines likewise name crawlable internal links as a core discovery signal and state that the same SEO foundations support Bing/Copilot grounding eligibility. These are eligibility/discovery principles, not ranking guarantees.

- https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- https://developers.google.com/search/docs/appearance/ai-features
- https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a

Next priority: audit one distinct unresolved mobile/performance, conversion/accessibility or authority-link issue; the FR/DE/AR same-language Services/footer/contact/wordmark routing layers are now covered by regression gates. Do not revisit the Phase 134 DMC/Luxury Travel Concierge indexation decision before 16 September unless a new technical failure appears.

## Phase 139 — lighter Private Office image, JPEG fallback retained

13 September 2026, Europe/Madrid. Branch `perf/phase139-private-office-image` starts from `882fb756110eecfc0e17d71d59cb9826f6d60489`, not the older Phase 137 baseline. During local research main advanced through Phase 138; its new worklog, source diff, successful deployment and exact artifact `10319293520` were read and revalidated before any branch write. No Phase 138 file or wordmark change is replaced.

Evidence: the five existing EN/ES/FR/DE/AR Private Office pages use the same 727,490-byte JPEG as their fetchpriority=high image, without an alternative format. A locally encoded WebP of the SAME 3024x4032 pixels is 357,986 bytes (50.8 percent less); it does not resize, crop or replace the subject. This measures the image payload, not total page speed or field LCP. The original JPEG remains untouched and continues to be the img src fallback, including for crawlers. No new preload is added, avoiding duplicate JPEG/WebP preloads.

Scope: `/private-office/`, `/es/private-office/`, `/fr/private-office/`, `/de/private-office/`, `/ar/private-office/`. Add one local WebP asset and a picture/source wrapper around the existing priority img on each page. All original img attributes, copy, headings, links, canonical, hreflang, structured data, sitemap, lastmod, forms, scripts and CSS remain unchanged. Existing build entrypoints call the new encoder and read-only gate after the localization steps; prior tests and workflow definitions are unchanged.

Local tests: Python compilation, idempotence and fail-before/pass-after gate; same dimensions and bounded mean pixel difference (1.256/255); side-by-side photo review. Ten offline viewport/page cases (five languages, 390/1440px) compared baseline, preferred WebP and simulated unsupported-format fallback: same page/image geometry and text, correct resource selection, no horizontal overflow or JavaScript errors. All requests were blocked and no form was submitted. This initial browser suite used the Phase 137 frozen output; reapplying the identical transform after the Phase 138 update preserves its new wordmark hrefs exactly. Rebased artifact comparison changes only five HTML files and adds the WebP. Removing the new wrappers restores each current HTML byte-for-byte. All 156 sitemap canonicals remain reachable and the 13 commercial priorities remain within two HTML links of Home.

Limits: direct container DNS and live browser navigation were unavailable; browser tests use in-memory copies, not live HTTP/field performance. Full clean PR CI and exact production output still require validation. Status at this commit is PREPARED/LOCALLY VALIDATED, not published; final release evidence will be recorded in the PR conversation. No private search metrics or personal data are published. Do not infer ranking, indexation, conversion or revenue uplift.

Primary references checked: https://developers.google.com/search/docs/appearance/google-images (picture with img src fallback, speed/quality), https://web.dev/articles/preload-responsive-images (avoid preloading multiple formats), and the Google/Bing SEO/AI guidance above. Next: verify release and public resource delivery, then assess mobile experience with real measurements when available; the 16 September indexation review interval remains unchanged.

## Phase 140 — supplied professional-role vocabulary

Published 13 September 2026. The only new vocabulary source was the user-supplied `IBIZA_VIP_MOVE_REVISAR_ANTES_DE_AGREGAR.pdf`. PR #68 integrated A1–A8 and B25–B34 as professional/client-role language on the existing Partners and Private Office pages in EN/FR/DE/AR/ES, without creating a new service or URL. PR #68 merged as `628aec9ec6e509e26ddab3fd0d1547154b91e417`; CI `34767216531` and production deployment `34767294117` succeeded. Production artifact `10320468878` has digest `sha256:90651df9065d24213e15dc316e54d1510fd212603492eb04697e12b24f4c2ed7`. Exact release comparison changed only the ten intended B2B HTML outputs; sitemap remained 156 URLs. Full term-by-term control is preserved in `PHASE140_VOCABULARY_CONTROL.md`.

Impact: broader visible buyer/partner vocabulary and clearer role recognition only. No ranking, indexation, AI visibility, traffic, lead or revenue uplift is inferred.

## Phase 141 — non-concierge travel-planning vocabulary bridge

Prepared 13 September 2026 from the same user-supplied PDF only. Exact Phase 140 production evidence showed that the selected B01/B02/B04/B06/B07/B23/B24 expressions were absent literally from each of the five existing Services hubs, even though the underlying service architecture already existed. The selected phrases describe luxury travel planning, bespoke/custom travel, itinerary planning, destination support, on-the-ground/in-stay assistance, travel coordination and luxury travel services.

Change: add one short explanatory block to `/services/`, `/fr/services/`, `/de/services/`, `/ar/services/` and `/es/servicios/` explaining that visitors do not need to know or use the word “concierge”. The block uses supplied vocabulary as alternative ways to describe a brief and explicitly says they are not separate new Ibiza VIP Move products. No new URL, service, title, H1, canonical, hreflang, schema, sitemap, form, WhatsApp destination, tracking, price or policy change.

Local validation against exact Phase 140 production: pre-change gate fails as expected; enhancement changes exactly five HTML files; rerun is idempotent; post-change gate passes with one H1, self-canonical, indexability, complete EN/ES/FR/DE/AR/x-default hreflang, Arabic RTL and unchanged 156-URL sitemap. Detailed pre-change control is in `PHASE141_VOCABULARY_CONTROL.md`.

Status at this worklog commit: **PREPARED / LOCALLY VALIDATED — PR CI and production deployment still required before calling it published.** Next: validate the exact PR diff and clean build, then merge/deploy only if all existing gates remain green. Keep the Phase 134 DMC/Luxury Travel Concierge indexation reassessment on or after 16 September.

## Current release state — Phases 141–144

This section supersedes the older prepared-only status for Phase 141 above; that earlier statement is retained as historical context.

- **Phase 141 published:** PR #70 merged as `b29f83c7dbb4f761e3a2192575a04904eded4d96`; production deployment `34767975332` succeeded; artifact `10321335103`, digest `sha256:630c21138a76d31247a5fa831b86705e4548412cd62a30bf803b3adb2e96ee75`. Five existing Services hubs gained the limited non-"concierge" vocabulary bridge, with 156 sitemap URLs preserved.
- **Phase 142 published:** localized Home pages FR/DE/AR/ES now reuse the existing mobile hero source instead of forcing the larger desktop image on narrow screens. The release passed CI and production validation; detailed evidence is retained in `PHASE142_PERFORMANCE_CONTROL.md`.
- **Phase 143 published:** PR #74 merged as `96dde62d71adf9d6b0eb83e41483136765351126`; deployment `34773091268` succeeded; artifact `10322447559`, digest `sha256:96ebcf35c196ffbb8e7bc430d2cf277d5d5a1eaaf97bd13983dd16f216d87e61`. Five Partners pages now prefer the validated 357.986-byte WebP instead of the 727.490-byte JPEG while retaining JPEG fallback; detailed evidence is in `PHASE143_PERFORMANCE_CONTROL.md`.
- **Phase 144 published:** PR #76 passed CI `34776398399` and merged as `c4f243eed1ce835168e1ffd6bd1bf18818e8b53d`; deployment `34776512394` succeeded. Exact production artifact `10323841907` has digest `sha256:85ba295391be806207aefa0d34cde642b94f19fb680af52150c0eb3fb8cdf2ae`. Fourteen reviewed priority uses of `villa.jpg` now offer AVIF then WebP while retaining JPEG fallback; nine existing JPEG preloads were replaced by AVIF preloads. In production the same-build payloads are 705.022 bytes JPEG, 348.411 bytes AVIF and 501.768 bytes WebP, with unchanged 2000×1334 dimensions. The artifact retains 156 unique sitemap URLs. Full evidence is in `PHASE144_PERFORMANCE_CONTROL.md`.

These releases demonstrate technical delivery/navigation/editorial improvements only. They do not establish field Core Web Vitals uplift, Google/Bing ranking changes, AI-answer inclusion, traffic, lead or revenue growth.

Next priority: audit the remaining `fetchpriority=high` image inventory and choose one distinct unresolved high-payload resource without modern-format delivery, while leaving lazy-loaded card imagery alone unless evidence shows it is material. Keep the Phase 134 indexation reassessment paused until 16 September unless a new concrete defect appears.
