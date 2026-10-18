# English Destination Management contact context — 18 October 2026

## Verified starting point
Main: `791bfb5b29ae881d965942b7d51379a13c7ca58d`. Successful Pages run: `39097087396`. Its artifact `12124119771` has independently matched ZIP SHA-256 `22a6b49ed6436109e206a3f4aa2b58f9a4938b753cd33c017da9d1cb089e6940`.

PR #140 and its unmodified-production browser check `39097139047` already closed the WhatsApp/menu verification. Do not reopen that resolved issue without a regression. This iteration concerns a distinct form-context opportunity. Main, open PRs and repository-wide queued/in-progress/waiting/pending/requested runs were checked before writing; no other work was returned.

The two English DMC contextual form links previously pointed to `/contact/`. The English service selector did not offer Destination Management. Direct DMC WhatsApp already preserved the service, and the profile selector already existed. This is not a total contact failure or proof of lost customers.

## Minimal candidate
Only English DMC and English Contact website HTML change. Keep the two existing anchor labels, add `?service=dmc` to their Contact destinations, and add one Destination Management option to the existing service selector. A small first-party inline script preselects it only for that single allowlisted parameter on English Contact, only if the selector is empty. It neither infers a client profile nor overwrites an existing selection, dispatches an event, stores data or submits anything.

No other language, field, title, description, H1, canonical, hreflang, schema, phone/WhatsApp/email destination, consent, Analytics configuration, sitemap inventory or search submission changes. No Maps/Google Business Profile, other brand, outreach, private client information or spending is involved. Contact remains canonical to `/contact/`; the query is a form state, not an additional landing page.

## Local evidence and release gates
The isolated transform applied to the exact deployed artifact changes only `contact/index.html` and `destination-management-ibiza/index.html`. A second application is byte-identical. Head metadata/H1, contact anchors, profile choices and all other output files match the baseline. JavaScript syntax passes; six offline preselection cases and twelve browser request-policy cases pass.

Local Chromium cannot navigate to localhost (`ERR_BLOCKED_BY_ADMINISTRATOR`). That is a test-environment limitation, not a website fault or a passing browser result. Full-build CI runs the original snippet review unchanged, then the new DMC form-context review against generated output. It checks both links in desktop/mobile, selection, editable service/profile, clean/unknown/repeated parameters, existing chauffeur routing, canonical, targets, geometry and script/resource errors. No name, phone, brief or form submission is generated. Screenshots stay outside website output.

A separate read-only post-deploy workflow checks unmodified production. It has only contents:read, no credentials persisted, no deployment, schedule, secrets, contact messages or Analytics traffic. Production GETs are allowlisted to the two relevant documents and existing static assets/fonts. Native iPhone/Safari, search impact and commercial impact are not certified.

Status at preparation: candidate only; not merged or published. Require the exact head's complete CI, output diff against the deployed artifact, review/head/base checks, successful deployment and passing unmodified-production evidence before calling it published. Final release IDs and outcome belong in this PR's closure comment; no private commercial metrics are stored here.

References checked: Google Search Central — consolidate duplicate URLs; W3C WAI — labeling controls.
https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
https://www.w3.org/WAI/tutorials/forms/labels/
