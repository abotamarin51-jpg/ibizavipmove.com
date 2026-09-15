# Ibiza VIP Move — SEO / GEO worklog

Updated: 15 September 2026, 17:03 Europe/Madrid. Exclusive repository: `abotamarin51-jpg/ibizavipmove.com`; website: `https://ibizavipmove.com/`.

## Scope and safeguards

Improve discovery, usability and qualified enquiries for real services IN IBIZA. Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN/FR/DE/AR. Preserve Spanish without expanding Spain/Italy targeting. No invented locations, memberships, affiliations, operating outcomes, availability, testimonials or identifiable client details; no mass synonym/country pages or word-count padding.

Do not touch Ibiza Private Drivers, its website, data, Analytics or business listing. Do not mix this work with B2B contact prospecting. No Google Business Profile/Maps edits, outreach, emails, registrations, paid links, ads/spending, DNS/MX, prices, commissions, billing, legal policies or unverified tracking. Never publish a private address or identifiable itinerary.

Before every write, read live main, recent commits, open PRs, active builds/deployments and the latest user authorization. Respect pauses. Remain read-only if another execution is active or overlap cannot be excluded. Use a new branch from verified main and a small reversible PR, never a direct main write. Do not weaken existing tests. Review the complete diff, files, exact head/base, required approvals and applicable passing checks before merge; then verify production before calling a website change published. Do not send contact messages/forms or test leads. Preserve URLs, layout, contact routes and unrelated files. Revert only this iteration's own regression through the authorized PR flow, never a global rollback.

## Preserved history and intent ownership

The previous root worklog is preserved byte-for-byte in `SEO_GEO_WORKLOG_ARCHIVE_THROUGH_156.md`, Git blob `f3c6e7f82243686e10f62ebec63333a5553facfe`. Earlier archives through 130, 135, 144 and 151 are unchanged. Old PREPARED/HOLD/Next wording is historical and is superseded by the verified release state below. Detailed implementation evidence remains in the existing PRs and control documents.

Do not repeat completed multilingual routing/contact/form, service-model, freshness, aviation-route, vocabulary, schema, contextual-link or image-delivery work without a demonstrated regression.

Intent ownership: Home = broad luxury concierge; `/private-concierge-ibiza/` = connected multi-service stays; `/luxury-lifestyle-management-ibiza/` = ongoing stay coordination; `/personal-concierge-ibiza/` = direct assistance; `/luxury-travel-concierge-ibiza/` = private travel management/bespoke planning; `/vip-services-ibiza/` = conditional hospitality/access; `/private-client-services-ibiza/` = principals/PAs/family offices; `/destination-management-ibiza/` = local DMC execution; `/partners/` = professional handover; `/bespoke-concierge-ibiza/` = unusual individual requests. No paid private membership is authorized.

## Verified production state — 15 September, 14:40

Starting main: `fb7dee8fecf757b9fa8e8549897652941850c40f`. PR #100 is merged as `9d0c2415cb5c63f19e0fdee8b0ed227dcd4590d1`; its French Partners correction is no longer awaiting publication. The later mobile-hero build-ceiling correction is included in current main. Latest deployment `34961645197` completed successfully from that main commit.

Production artifact `10393387023` SHA-256 was independently matched to `0aa4813d857b8099ad3945cde48a482d0796505e98610f445ca7926e797d1cd1`. Its `/fr/partners/` HTML contains the Phase 156 style marker. This closes the stale release-status entry, not a new website release. No open PR or queued/in-progress workflow was returned before this documentation branch was created.

Important residual limitation: `build_site.sh` still downloads editorial images on each build. A successful deployment does not prove future builds are reproducible or eliminate upstream image drift. Compare actual output and preserve performance gates before future website releases. Do not silently incorporate unrelated image/date changes. Do not repeat the already-published French/German Partners fixes.

## Completed structural audit — 15 September, 14:37

Audited the exact production artifact locally, without crawling 156 live pages or repeating contact-service tests. All 156 unique sitemap canonicals have HTML output, a single self-canonical and H1, no HTML robots/googlebot noindex, no canonical-page meta refresh, valid JSON-LD syntax and existing reciprocal hreflang targets within the sitemap. The artifact robots.txt permits Googlebot for those URLs.

The canonical-page graph uses HTML anchor hrefs and excludes nofollow edges. All 156 URLs are reachable from English Home: Home at depth 0, 26 at depth 1, 98 at depth 2 and 31 at depth 3. No sitemap orphan or broken alternate was found in these checks. This does not establish that a particular exclusion was caused by content, links or anything else. No extra links, invented translations, noindex/removals or rewrites are justified solely by this audit.

Limits: this is static artifact validation, not a live HTTP/X-Robots-Tag header audit, Google's selected canonical, Google rendering, semantic rich-result validation, content-quality judgment, browser/Safari test, Core Web Vitals or full WCAG certification. JSON-LD syntax passing is not schema eligibility. The preceding four-language contact audit is a separate completed check; do not repeat its 44 service-selection cases without a change or regression.

## Indexation queue and next decision

Use only canonical Wizard property `https://ibizavipmove.com/` for tracking; do not add domain-property metrics to it. Read recent tracker/saved results first and inspect only small justified batches within quota. Pending inspection is not not-indexed; sitemap API indexed=0 and impression-derived counts are not coverage censuses. Preserve valid aliases, redirects, canonicals and deliberate exclusions. Inspections, sitemap/IndexNow submission and technical eligibility do not guarantee indexing or rankings.

This iteration read the current tracker and complete not-indexed queue without initiating fresh inspections, indexing requests, sitemap/IndexNow submissions or notification changes. Private per-URL history and metrics remain outside this public repository. No newly confirmed indexing gain or measured commercial lift is attributed to this audit.

The held commercial reassessment now concerns `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/`, from 16 September unless a new technical fault appears. German private aviation was already confirmed indexed in the earlier record; do not keep treating it as an unindexed held URL. For the remaining queue, distinguish unknown/discovered/crawled-not-indexed, then investigate a demonstrated blocker before editing. A clean static audit is not a complete exclusion diagnosis. Reuse this artifact snapshot if source/deployment stays unchanged instead of rerunning it hourly.

The tracker still exposes an enabled email digest; no legitimate digest-setting action was found in the available interface. Do not create more notifications, delete history or claim it was disabled. Request indexing only through a supported, authorized action; otherwise leave the exact manual Search Console step, avoid duplicate requests and never mark an unexecuted request as sent.

Decision: documentation-only closure and audit baseline; no website code, content, asset, contact, tracking, sitemap or configuration change. Next: read the next native tracker update and reassess the two held commercial URLs from 16 September. If a new real fault appears earlier, prioritize it. SEO/GEO monitoring is not a guaranteed finish date, number-one ranking or continuous background work.

Primary references checked in this iteration: https://developers.google.com/search/docs/crawling-indexing/links-crawlable ; https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl .


## Phase 157–159 release stability closure — 15 September, 17:03

PR #103 merged as `415b2b10e5b22aea23581075f9ce148263a29b8d`: the approved villa source is pinned and verified at build time. Its validation run `34979187777` passed. The first Pages run `34979426423` built and uploaded successfully but failed three deployment attempts: the initial Pages/OIDC timeout was followed by duplicate `github-pages` artifacts created when the single combined job was retried.

PR #104 merged as `c0a39d79164ee85f17f2e12861a8467af6c610a4` after validation `34984809003`. It follows GitHub Pages' documented build/deploy separation with `needs: build`, so retrying a failed deploy no longer re-uploads the artifact. Run `34984970083` then published Pages successfully, but the post-deploy IndexNow script failed before any submission because the separate job lacked `_site/sitemap.xml`.

PR #105 merged as `e33735d63c4adf73cead25c2b917e588ffecbbfe` after validation `34985316844`. It downloads and extracts the already-validated Pages artifact before the existing notification. Deployment `34985470178` completed successfully: build, artifact upload, Pages deployment, artifact restore and one IndexNow notification all passed. This does not prove delivery, crawling or indexing by any search engine.

Independent artifact checks: exactly one `github-pages` artifact; 156 sitemap URLs; contact HTML retains WhatsApp `34600703303`, phone `+34 600 703 303` and `partnership@ibizavipmove.com`. Villa hashes match the approved baseline: JPEG `920a2d479f869c385e47bbaf7cec73235da990c450283a75c0fb8d687de945dd`, AVIF `d396e7451eba1ebe43426b46621538c5d7c1567d4f144d2d576dbfcb32df624b`, WebP `985572087589410aa08ec4c332b171e58974cd2d566bcc55cc4b210a57e3cc82`. Production contact and villa pages returned HTTP content after release. No form or message was submitted.

Wizard remains on canonical property `https://ibizavipmove.com/`: 156 tracked, 102 indexed, 54 not indexed, 0 pending, 0 errors and 0 warnings; no new indexing change is attributed to this release. Breakdown remains 35 crawled-not-indexed, 9 discovered-not-indexed and 10 unknown. Next: from 16 September, reassess `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/` with new Google evidence. Other externally downloaded editorial assets remain a reproducibility risk, but should not displace a demonstrated commercial blocker.


## Phase 160 chauffeur source stabilization — 15 September, 18:13

A reproducibility audit compared the prior approved Pages artifact from run `34961645197` with the later release artifact from run `34985470178`. Eighteen of nineteen image files were identical. The only unexpected change was `assets/images/chauffeur.jpg`, despite no chauffeur-specific release: approved SHA-256 `4e286f6c4a91148c0beb248ca354beba7a3f281c95d3b746b17ef102d9649484` (381,377 bytes) versus mutable-upstream SHA-256 `9456394f3bb5427513d4413f1a1e2092d100f1478fd52bbc037bce5e0d9c586e` (381,328 bytes). Both are 2000×1333 JPEGs; a pixel comparison confirmed low-level changes across the image, so this was treated as release drift rather than an SEO opportunity.

PR #107 restores the previously reviewed chauffeur bytes from `editorial-assets/chauffeur.jpg` and verifies their checksum before the optimizer runs. Validation `34992565210` passed. Its Pages artifact differed from the preceding deployed artifact only in the expected chauffeur JPEG; no files were missing or added, and the sitemap remained at 156 URLs. The PR merged as `6ebf09d397df28d230ba46b035a88d42c3afcbf1`.

Deployment `34992785611` completed successfully on the first attempt. Its single Pages artifact `10406676244` (artifact digest `2bc83017b9c57414f8217cb5576c73a1d41e0d19f95d3ab8cfecdacb562f5545`) matched the validated artifact byte-for-byte excluding the expected hidden `.nojekyll` packaging difference. The deployed chauffeur resource returned the approved SHA-256 and 381,377-byte size. English, French, German and Arabic chauffeur pages and Contact returned content, and their artifact HTML retains a self-canonical, indexability and WhatsApp, telephone and email routes. No form or message was submitted.

Wizard was read on canonical property `https://ibizavipmove.com/` without repeating URL inspections: 156 tracked, 102 indexed, 54 not indexed, 0 pending, 0 errors and 0 warnings. The non-indexed breakdown remains 35 crawled-not-indexed, 9 discovered-not-indexed and 10 unknown; no new indexation is attributed to this release. The sitemap was last downloaded by Google on 15 September at 04:14 UTC with no reported error or warning; its API `indexed=0` is not used as a coverage census. The digest remains enabled because the available site-update action exposes only tags, branded keywords and sitemap URLs, not digest configuration.

Decision: Phase 160 is published and validated as a stability correction. It proves deterministic delivery of this approved asset, not ranking, AI visibility or lead impact. Other remote image sources remain monitored, but no mass rewrite is justified without demonstrated drift. Next from 16 September: read the next native tracker results and reassess `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/` before any content change.


## Phase 161 remaining-image reproducibility sample — 15 September, 19:05

No open PR or queued/in-progress workflow existed at the write gate; current main was `fb84db39f0e0ca801bf80e834495e4da9164625e` and the latest website deployment remained successful run `34992785611`. Two isolated executions of the repository's base `build_site.sh` both passed. Their 54-file intermediate outputs had no missing or extra files and differed only in the mutable 2400×1600 chauffeur download (547,482 versus 547,413 bytes; low-level pixel difference across the frame). Phase 160 already overrides that intermediate file with the checksum-pinned approved chauffeur asset later in the production sequence, so this does not reopen the completed correction.

The eight still-remote final image sources in `phase101_enhance.py` were each retrieved twice in separate rounds. All sixteen downloads completed and every pair matched exactly in size and SHA-256: hero, yacht, nightlife, events, chef, aviation, desktop hero and mobile hero. A broader local workflow replay then encountered a proxy timeout while downloading an upstream asset, so this iteration does not certify full-build determinism or interpret the timeout as a production fault. No image was frozen speculatively and no website, contact, sitemap, tracking or notification setting changed.

Wizard was read first on canonical property `https://ibizavipmove.com/` without new URL inspections: 156 tracked, 102 indexed, 54 not indexed, 0 pending, 0 errors and 0 warnings; health 79. Breakdown remains 35 crawled-not-indexed, 9 discovered-not-indexed and 10 unknown, with no newly confirmed change beyond the five earlier gains. Google last downloaded the canonical sitemap on 15 September at 04:14 UTC without reported errors or warnings. The tracker digest remains enabled because the available site-update action still exposes no digest control.

Decision: investigated and validated as a no-change stability iteration. The sample provides no demonstrated new asset regression that justifies another release. Next from 16 September: use the next native Google evidence to reassess `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/`; do not rewrite them solely for a held crawl status.


## Phase 162 car-rental performance diagnosis — 15 September, 19:55

After the live-state and overlap gate, Search Console performance was reviewed on canonical property `https://ibizavipmove.com/` for the latest settled 28-day window (16 August–12 September; data settled through 13 September). `/luxury-car-rental-ibiza/` was the highest-impression non-Home commercial URL returned: 139 impressions, 0 clicks, 0% CTR and average position 72.46. Daily visibility began on 31 August and was recorded through 8 September, followed by zero recorded impressions from 9–12 September. That cessation is a monitoring signal, not proof of deindexing, penalty or a technical fault.

The saved Indexing Tracker result still classifies the page as Submitted and indexed, PASS and INDEXING_ALLOWED, last checked 14 September 20:19 UTC and last crawled 7 September 16:30 UTC. A one-URL live Wizard audit returned HTTP 200, self-canonical, indexable, one H1, 594 words, title length 59, meta-description length 158, 36 internal links, six hreflang annotations, structured data with no schema issue, three images with alt text and zero audit issues. The visible page clearly states luxury car hire/rental, SUVs, sports cars and supercars, supplier-dependent availability/terms, and retains WhatsApp, phone and email routes. No form or message was submitted.

Query-level rows are privacy-filtered and account for only part of the page totals; no attribution or country conclusion is inferred from the missing rows. Average position around 72 means zero clicks cannot be treated as a snippet-only CTR problem. The data does not justify changing the established title, content, canonical, language routing or service claims today.

Wizard tracker totals remain 156 tracked, 102 indexed, 54 not indexed, 0 pending, 0 errors and 0 warnings. Decision: investigated, validated and queued with no website change. Recheck this page after additional settled data on or after 18 September; intervene only if the visibility loss persists with corroborating evidence. The next immediate priority remains the 16 September reassessment of `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/`.

## Phase 163 Partners performance and snippet diagnosis — 15 September, 20:56

After confirming main `74d789118f1d8593039cec577a7691f0720f70da`, no open PR and no in-progress workflow, the English B2B handover page `/partners/` was reviewed on the canonical Search Console property `https://ibizavipmove.com/`. In the latest settled 28-day window (16 August–12 September; settled through 13 September), the page recorded 9 impressions, 0 clicks, 0% CTR and average position 6.33. Impressions occurred on five dates only (31 August, 1, 5, 6 and 11 September). No query-level rows were returned for this exact page filter, so the search terms and markets behind those nine impressions cannot be diagnosed reliably.

The saved Indexing Tracker result classifies the URL as Submitted and indexed, PASS and INDEXING_ALLOWED, last checked 14 September 19:42 UTC and last crawled 13 September 23:23 UTC. A one-URL live Wizard audit returned HTTP 200, self-canonical, indexable, one H1, 656 words, 40 internal links, six hreflang annotations, three images with alt text and structured data without schema issues. The only findings were low-severity length notices: title 77 characters and meta description 172 characters. The visible page already explains local execution for luxury travel advisors, concierge companies, hospitality partners, PAs and private offices, with live-client, partnership, private-office and hospitality brief routes plus WhatsApp, telephone and partnership email. No form or message was submitted.

Decision: investigated and validated with no website change. Nine impressions across five dates are too small a sample to attribute zero clicks to snippet length, while shortening the title today could remove the differentiating Family Offices audience. Queue this URL for another performance review on or after 19 September; change the snippet only if additional settled data shows a persistent near-page-one CTR gap with enough query evidence. Wizard totals remain 156 tracked, 102 indexed and 54 not indexed (35 crawled, 9 discovered and 10 unknown), with 0 pending, 0 errors and 0 warnings; no new indexing change is confirmed. Immediate next priority from 16 September remains the held reassessment of `/destination-management-ibiza/` and `/luxury-travel-concierge-ibiza/`.
