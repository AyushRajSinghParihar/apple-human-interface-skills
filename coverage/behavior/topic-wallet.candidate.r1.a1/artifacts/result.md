# Repair outcome

Patched interface.md in place from a one-sentence defect report into a concrete iPhone Wallet event-ticket specification. It now defines field hierarchy, a system-rendered credential, exact-ticket routing, add/view/retry behavior, lifecycle transitions, offline recovery and minimum-data boundaries.

## Decisions

- Replace the mutable screenshot with a nonposter event-ticket pass and system barcode facilities. Keep essential event details in fields/semantics. This follows [Wallet anatomy](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-anatomy), [event tickets](https://developer.apple.com/design/human-interface-guidelines/wallet#Event-tickets) and [images](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-images). Nonposter style is a product choice that avoids introducing poster-specific dependencies.
- Show event date/time, venue and entry information prominently; retain meaningful collapsed status and account for Watch field/crop differences. See [Designing passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Designing-passes).
- Open the exact ticket with an authenticated return route and web fallback. This applies precise entry points and preserved context from [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).
- Void canceled tickets and update visible state, while retaining a record and truthful recovery path. [Wallet passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Passes) supports accurate lifecycle, relevant updates, Add/View behavior and permission before deletion. Backend rejection and offline staffed resolution are additional product decisions.
- Remove unnecessary identity attributes throughout the pass and credential. [Privacy best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports minimum necessary data. An opaque credential and log exclusions make that decision concrete; they do not establish security certification.

## Worked before/after

Illustrative fixture only: Harbor Lights, 14 November 2026 at 19:30 America/New_York, Pier Hall, Gate B, section A / row 4 / seat 12.

Before: the supplied description reports a mutable barcode screenshot, hidden date/location, unnecessary identity details, a marketing destination and Valid after cancellation. No screenshot or actual ticket values were supplied.

After issuance: the front shows Valid, Harbor Lights, 14 Nov 2026 / 7:30 PM EST, Pier Hall, Gate B and the assigned seat, alongside a native barcode backed by an opaque issuer credential. Details contain the venue address from issuer data and this ticket's management/support destination. Holder identity attributes are absent.

After cancellation: the authoritative admission record rejects the credential immediately and queues an update to the same pass: Canceled, voided lifecycle, and “Event canceled. See ticket details for next steps.” The destination opens that canceled ticket with confirmed remedies only. An offline phone may still show the previous pass until delivery; current scanner validation rejects it, and a scanner unable to validate sends the attendee to staffed resolution. No instant synchronization is assumed.

## Acceptance checks and status

Passed — static document review:

- All five supplied defects have explicit replacement requirements in interface.md.
- The field table exposes event/time/venue/status and a system-rendered credential without relying on art.
- Lifecycle includes cancellation, revocation, redemption, expiry, changing event information, delayed delivery and offline handling.
- Add/View, refusal, retry, removal/re-add and exact-ticket recovery are specified.
- Minimum-data requirements cover front, details, artwork, payload and URLs.

Failed — supplied baseline, based only on its written assertions: screenshot credential, hidden event details, generic destination, canceled-but-valid state and unnecessary identity display. No revised runtime artifact exists to grade as passed or failed.

Not executed — implementation acceptance gates:

1. Build/sign a pass and verify SDK/schema availability, semantics/fallback fields, assets, barcode format and physical scanner compatibility.
2. Inspect collapsed/open/details rendering on supported iPhones with long names, localized dates, enlarged text, contrast and supported orientations. Essential information must remain available outside art. Inspect Watch variations if delivered there.
3. Exercise Add, cancel, failure/retry, View, removal and re-add. Verify exact-ticket context survives interruption, authentication, rotation and enlarged text in the companion page.
4. Scan issued, canceled, revoked, used and expired fixtures. Never admit the latter states by trusting the displayed label. Exercise offline phone/scanner recovery and delayed/out-of-order updates.
5. Update venue/time/gate, then cancel. Verify the same pass updates, relevance changes, cancellation removes Valid, only meaningful time-critical changes interrupt, and deletion requires permission.
6. Open the ticket destination with/without the app, signed out and offline. Require exact-ticket routing after authentication and truthful refresh failure copy.
7. Inspect generated payloads, artwork, URLs, logs and analytics for identity data or leaked credentials; test management authorization. Verify actual assistive-technology reading and operation separately.

## Evidence limits and route audit

Explicitly read installed .agents/skills/apple-hig/SKILL.md. Searched its references/topic-index.md for Wallet/pass/privacy/iOS. Read the getting-started, technologies and foundations family SKILL.md files, then routed Designing for iOS, Wallet and Privacy topic SKILL.md procedures before their corresponding source guides. All paths resolved within the installed package; every read/search used a separate single-file command. The local guides state retrieval on 2026-10-25. Official links above are attribution, not evidence of web visits.

Only interface.md and installed local instructions/guides informed the repair. No web browsing, device, SDK compilation, GUI, Pass Designer, scanner, backend integration or accessibility execution occurred. Actual rendering, supported OS minimum, delivery latency, security and refund policy remain unverified. No conflicting source rule was encountered in the selected guidance. Static review confirms specification coverage only, not implemented behavior.
