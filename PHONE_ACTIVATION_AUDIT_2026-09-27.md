# Telephone activation measurement — 27 September 2026

Status: PREPARED, NOT PUBLISHED. Preparation began at 23:10 Europe/Madrid.
Scope: Ibiza VIP Move only. Base main: `dbb4efb0ff477a3a1605ffb22a2458b1452a02da`.

## Demonstrated source behavior

The base `premium.js` blob `7b0b21642fb19765433ec0bcd16a7a04b6052611` calls `ivmTrackPhone` on `pointerdown`. The later 1,200 ms guard prevents a second count on click but cannot undo a count when initial pointer contact becomes scrolling, pointer cancellation or a secondary-button context-menu interaction. This is an event-semantics issue, distinct from the GA4 forwarding/Beacon correction in PR #125.

This finding does not establish that any historical analytics event was false or prove a completed telephone call. No private metrics or client data are recorded here.

## Minimal candidate

Use a primary `click` capture listener instead of `pointerdown`, before the native link default action. Retain the existing delegated click fallback and 1,200 ms deduplication. Preserve the event name, payload, telephone/WhatsApp/email destinations, consent layer and Beacon forwarding. No call to `preventDefault` is added. No layout, content, page URL, metadata, schema, sitemap, Google Business Profile, price, legal policy or analytics-property setting changes.

Only `premium.js`, the new offline test, additive PR-validation workflow steps and this technical note are changed. The deployment workflow is unchanged.

## Offline evidence

The local base source was matched to its Git blob hash. The exact candidate blob is `8425a9e40edf530f7487773d66abdcea299836ea`.

Commands:

```sh
node --check premium.js
node tests/phone-activation.cjs premium.js
node tests/phone-activation.cjs _site/assets/premium.js
```

Local source test: 14 cases, 14 passed. The same tests on base: 14 cases, 10 passed, 4 failed. Failing base scenarios are pointerdown without activation, pointer cancellation/scroll sequence without click, secondary-button/context-menu sequence, and a synthetic secondary-button click. The latter is defensive event-model coverage, not proof that every browser emits such a click.

Passing candidate cases also cover a completed tap sequence, keyboard-style activation, primary click, separated activations, nested elements, unchanged WhatsApp/email/request/partner events and a non-link. The test asserts that the tested application handlers do not cancel link activation.

This is an isolated Node VM event model of the exact source block, NOT a real browser, DOM integration, iOS Safari, screen-reader or end-to-end Analytics test. It cannot open a telephone link, submit a form, contact a messaging service or send an Analytics hit. Existing build/audit steps are retained, with source and generated-asset tests added before and after the build.

## Release gate — do not merge yet

The local environment has no runnable Chromium or WebKit executable and outbound DNS resolution failed. Existing deployment/preview artifact reads returned no downloadable artifact. These are testing-environment limitations, not evidence of a production outage.

Before merging, require passing PR CI, inspect the full generated diff against a verified baseline (including unexpected mutable-image drift), and test the generated pages in actual desktop/mobile browsers with all Analytics requests blocked and external contact destinations intercepted. Specifically check that a completed tap/keyboard activation is counted once, a scroll/cancel/context menu counts zero, and the consent/Beacon handoff still behaves correctly. Native iOS Safari telephone handoff remains unverified; do not generate a real call or production Analytics event as a test.

Verify the generated premium.js cache/version strategy before release; this candidate does not claim to have completed cache rollout. Recheck live main, PR head, required checks/reviews and concurrency immediately before any future merge. After an authorized release, verify deployment and affected production resources before calling it published. Do not start another change while this PR remains unresolved.

Keep the existing root worklog intact; this PR and note provide continuation evidence for the open correction. Record the eventual release or continued hold in the root worklog only through a safe complete-file update. This document deliberately contains no private GSC/GA4 metrics.

## Primary references

- https://developer.mozilla.org/en-US/docs/Web/API/Element/pointercancel_event — browsers may cancel a pointer sequence when it becomes panning/scrolling.
- https://developer.mozilla.org/en-US/docs/Web/API/Element/click_event — activation can originate from pointing devices, touch and keyboard.

No Google Business Profile/Maps changes, other-brand work, new language, outreach, expenses or live contact/analytics test submissions were made.
