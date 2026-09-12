# Ibiza VIP Move — SEO / GEO worklog

Updated: 12 September 2026. Repository: `abotamarin51-jpg/ibizavipmove.com`.

## Scope and safeguards

Improve the existing Ibiza website for qualified private-client and international B2B enquiries. The aspiration is international recognition for luxury concierge IN IBIZA, not a claim of a guaranteed worldwide ranking.

Only this domain/repository is in scope. Do not mix Ibiza Private Drivers, its Business Profile or its Analytics property. Google Business Profile/Maps edits, DNS/MX changes, outreach, paid links, advertising, association registrations and new membership products are outside this workstream. Local signals must describe real Ibiza service coverage, not fictional offices abroad. No invented reviews, ratings, affiliations, operating results, client identities, addresses, prices or availability guarantees.

Priority markets: USA, UK, Monaco, Switzerland, Germany, Japan, Belgium, Netherlands, France, UAE and Saudi Arabia. Priority languages: EN, FR, DE, AR. Preserve existing Spanish; do not expand Spain/Italy targeting. These are audience priorities, not verified search-volume estimates.

## Latest checkpoint

- Phase 110 was merged through PR #28 as `be6de6128907770babc8299c16a4f6633fd5a4fa`. Its recorded deployment is `34569838927`.
- Main was re-read on 12 September and still pointed to that commit; there were no open PRs at that check.
- Phase 111 introduces a READ-ONLY navigation-depth gate, not additional landing pages or a ranking claim. Verify the Phase 111 PR/check/deployment state before treating it as accepted.
- `phase111_audit.py` constructs an HTML anchor graph from the generated sitemap and pages. It requires all sitemap pages to be reachable, 13 priority URLs (including Home) within 0–2 HTML link edges of Home, and FR/DE/AR concierge pages within two links of their language home.
- It distinguishes main-content inbound sources from navigation links and does not count JSON-LD or hreflang as navigation. Its small parser/BFS self-tests run with each audit.
- Local baseline testing passed against the retained Phase 108 / build 178 artifact: 156 sitemap URLs reachable, priority depths already satisfactory. The current full build must validate subsequent Phase 109/110 changes; do not present the historical baseline as a live-site inspection.
- Public website fetches returned a cache miss in the web tool and DNS resolution failures in the local environment on 12 September. This is an access limitation observed by these tools, NOT proof that the website is down for other visitors. Recheck public availability before claiming live verification.
- Google indexation, country-specific impressions/rankings, GA4 collection and Maps rankings have NOT been verified in this iteration. Indexable does not mean indexed; a WhatsApp click is not a confirmed client or sale.

The hourly ChatGPT task is separate from GitHub Actions: Actions validate a proposed change; they do not independently invent or publish SEO content every hour. The task must re-read current state, respect permissions and maintain this checkpoint. Do not start another write while a related PR/deployment is unresolved. An execution with no justified change should say so.

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

1. Resolve the current Phase 111 PR/check/deployment state first. Run `python3 phase111_audit.py` on the FINAL `_site`, or inspect its CI log. The generated `seo_geo_audit_report.json` belongs outside `_site` and is not public page inventory.
2. Recheck public HTTPS availability. Where authorized tools allow, verify the correct Search Console/Analytics property before claiming indexing or lead metrics. Do not reuse the other brand's tracking ID or bypass approvals.
3. Review the existing Partners/Destination Management and travel-concierge copy against the intent table; identify a specific, useful B2B information gap before editing. Avoid redundant modules, broad keyword lists and word-count padding.
4. Improve a bounded, reversible change only when justified. Use a branch, meaningful tests and PR; preserve existing checks, semantic structure, accessibility, language routing and performance. Verify the diff, merge permissions, Actions and affected pages before calling anything published.
5. Update this worklog with evidence, action, PR/commit, test result, exact status and the next unresolved priority. Distinguish technical improvement from measured business impact. No automatic mass publication, speculative noindex/redirect changes, or invented case studies.

## Primary-source reference principles

- Google link guidance: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Google recrawling/indexing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Google local ranking: https://support.google.com/business/answer/7091

Useful visible content, crawlable contextual links and matching structured data remain the basis. `llms.txt`, Service schema and more pages do not guarantee search/AI visibility or Maps rankings. Repeated indexing requests do not make Google crawl a URL faster.
