# Contextual Contact activation compatibility — 18 October 2026, Europe/Madrid

## Evidence and scope
Live main at the write gate: `31777e61635355398edc3e453eba041de66cdc23`. PR #141 is already merged and deployed; its service preselection is not to be duplicated or rolled back speculatively. Before this branch: no open PR and no repository-wide queued/in-progress/waiting/pending/requested workflow was returned.

The Partners review found four distinct prefilled WhatsApp routes in each EN/FR/DE/AR edition in the exact deployed artifact. The general English Private brief link is intentionally not enough to infer a visitor's role or requested service. No new Partners button, field or page is justified by that observation.

A distinct reproducible compatibility gap was found in the deployed premium.js event handler: plain `/contact/` records the existing `request_concierge_click`, but `/contact/?service=dmc` and `/contact/?service=chauffeur` do not. Contact navigation itself still works. The added DMC route in PR #141 encountered this pre-existing exact-string matching limitation. This is evidence of incomplete activation recognition, not proof of absent demand, missed messages or bookings.

## Minimal correction
Strip only query/hash from the existing contact-route matching expression, retaining the same approved same-site prefix and the five exact Contact path allowlist. Do not change anchor hrefs, existing event names/details, WhatsApp/phone/email handling, forms, consent or GA4 settings. Query values are not added to event details.

The existing final premium.js cache-key pass uses release floor 12, while future higher ASSET_VERSION values still take precedence. This invalidates only the changed premium.js reference, not unchanged logos, CSS or images. No workflow, sitemap, page copy, metadata, canonical, hreflang, schema or other property change.

## Tests and release gate
All original 26 offline activation cases are preserved. The extended 78-case suite adds contextual route checks across existing Contact paths, absolute/relative forms, query/hash, keyboard activation, non-contact/external-host negatives, unchanged destinations and no query-value payload. Before: 42 new compatibility cases fail. Candidate source and generated-handler simulation: all 78 pass. No network/Analytics/phone/email/form request is possible from this Node VM harness.

Expected complete output delta: premium.js handler plus v11-to-v12 premium.js references in 156 existing HTML files. All other output must match the previous deployed artifact byte-for-byte. Local production browser access returned ERR_BLOCKED_BY_ADMINISTRATOR; no new local browser pass is claimed. Require full existing CI, generated artifact comparison, original mobile/desktop contact and DMC checks, exact-head/base review, successful deployment and existing production checks before marking released. Final release IDs belong in the PR closure record.

No private commercial metrics, identifying client data, Maps/GBP edits, messages, notifications, indexing requests, new tracker, expense or other-brand work. Technical delivery does not establish natural GA4 reception or commercial/search/AI impact.

Reference: https://developers.google.com/tag-platform/security/guides/consent (existing consent remains unchanged).
