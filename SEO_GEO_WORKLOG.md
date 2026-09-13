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

Date: 13 September 2026. Evidence from the exact Phase 136 production artifact: `/fr/contact/`, `/de/kontakt/` and `/ar/contact/` each retain a legacy Explore footer with three English destinations even though exact localized equivalents already exist. The affected routes are Private Office, The Ibiza Black Book and International Clients: nine hrefs total, six commercial and three editorial.

Prepared change: replace only those nine hrefs with `/fr/...`, `/de/...` and `/ar/...` equivalents. Keep visible labels, form runtime/validation, WhatsApp destination, analytics behavior, canonical, H1, schema, sitemap, legal policy, prices and service scope unchanged. No new URL or asset.

Local validation against the exact Phase 136 artifact: Python compilation passes; the transform changes exactly three HTML files and is idempotent; the read-only gate confirms all nine localized targets exist and are present in the unchanged 156-URL sitemap, each contact page retains one self-canonical/H1 and its qualified brief form, and the official WhatsApp destination remains present.

Status at this commit: prepared for PR CI and production verification. The final PR conversation must record the exact CI run, merge commit, deployment and production artifact before Phase 137 is treated as published. Do not infer ranking, indexation, conversion or revenue impact from this technical change.

## Intent ownership — reuse existing pages

Home owns broad luxury concierge; `/private-concierge-ibiza/` connected multi-service stays; `/luxury-lifestyle-management-ibiza/` ongoing stay coordination; `/personal-concierge-ibiza/` direct assistance; `/luxury-travel-concierge-ibiza/` private travel management/bespoke planning; `/vip-services-ibiza/` conditional hospitality/access; `/private-client-services-ibiza/` principals/PAs/family offices; `/destination-management-ibiza/` local DMC execution; `/partners/` professional handover. `/bespoke-concierge-ibiza/` remains for unusual individual requests. No private membership is authorized.

## Current primary-reference principles

Google Search Central says crawlable `<a href>` links help Google discover internal pages and that useful internal links help people and Google understand a site. Bing Webmaster Guidelines likewise name crawlable internal links as a core discovery signal and state that the same SEO foundations support Bing/Copilot grounding eligibility. These are eligibility/discovery principles, not ranking guarantees.

- https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- https://developers.google.com/search/docs/appearance/ai-features
- https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a

Next priority after Phase 137 release verification: audit one distinct unresolved FR/DE/AR conversion or authority-link issue, mobile/performance defect or Search Console signal. Do not revisit the Phase 134 DMC/Luxury Travel Concierge indexation decision before 16 September unless a new technical failure appears.
