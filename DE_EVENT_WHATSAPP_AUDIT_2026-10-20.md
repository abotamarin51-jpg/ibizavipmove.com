# German event enquiry handoff — 20 October 2026, Europe/Madrid

## Scope and evidence
Continuation explicitly authorized by Juan. Base main: `e7667af4ae7d001b95f3b8742236735afa0e0752`. PRs #143 and #144 are complete; their sitemap verification is not reopened. The root SEO/GEO worklog and latest release records were read. No open PR or repository-wide in_progress/queued/waiting/pending/requested run was returned at the branch gate.

The exact deployed #143 Pages ZIP was re-read and independently matched to SHA-256 `64cde16ce12e56b99c7c0d5ff0f0bc48f1e94e8e853e593add07c0453dfef03b`. Its German event page has two existing main-content buttons labelled `Private Event anfragen`, both opening the approved WhatsApp recipient without enquiry context. This is a usability opportunity, not proof of missed enquiries or the cause of zero search clicks.

## Minimal website change
Only those two href values gain a German, editable event draft: event coordination in Ibiza; optional/open date range; guest count; occasion and requested support. No identity, wealth, role, private location, date, party size or service availability is invented. The recipient stays `34600703303`; every global/header/mobile/floating WhatsApp link remains unchanged. No new button, page, language, visible page text, SEO metadata, schema, sitemap, consent or Analytics configuration.

The existing late localized-pathway build step preserves its original French function and adds a guarded two-link replacement. Missing/duplicate/changed markers fail; re-running is idempotent. The local 262-file artifact comparison changes only `de/private-events-ibiza/index.html`, and reversing the two href changes restores its exact original bytes.

## Tests and release gate
Python syntax and offline encoding/idempotence/exact-delta tests pass, including seven ambiguous-markup negatives and eight request-policy cases. The local Chromium navigation was blocked by this environment (`ERR_BLOCKED_BY_ADMINISTRATOR`), so no local browser pass is claimed.

Add the focused test to existing full CI using its already pinned browser tools. Preserve every original test. Capture desktop/390px/360px screenshots, verify both links, target text and geometry, exercise pointer/keyboard only against the local CI artifact with outgoing navigation intercepted, and block Analytics, messages, forms and other non-allowlisted requests. On production only trial activation/focus and href checks occur. No native WhatsApp handoff or physical Safari certification is claimed.

The existing read-only post-deployment DMC review gains the same German check and retains its DMC and sitemap steps. The new production-only step does not run on a PR against the old live page; the candidate is mandatorily checked by full validation instead. Evidence remains outside website output, in existing review artifacts. No new scheduled task or external notification.

Before merge require all applicable exact-head checks, complete output/artifact and diff review, appropriate reviews/permissions and unchanged main/head with no active run. After merge require successful deployment, existing contact reviews and the German production report, with the served HTML hash equal to the reviewed output. Stop if any requirement fails. Record final IDs and verification in the PR closure; no private metrics or client information belong in this public repository.

Source for standard click-to-chat draft syntax: https://faq.whatsapp.com/5913398998672934 . A draft is not a sent message or booking. No indexing submission, Maps/GBP action, other-brand work, outreach, spending, infrastructure change or claim of SEO/AI/commercial improvement.
