# Venue ticket pass — revised specification

Platform: iPhone Wallet (iOS). Task: identify the event, find the venue and present the correct admission credential during a brief check at the gate. Use a native PassKit event-ticket pass, with standard nonposter fields; do not build a simulated Wallet screen. Wallet owns pass layout, barcode presentation and system controls. Minimum OS/API support must be verified during implementation; no SDK availability is established by this specification.

## Field and destination contract

| Surface | Required content |
| --- | --- |
| Logo/name | Recognizable venue or issuer name; provide an icon. Branding must not carry essential ticket text. |
| Collapsed header | Event date and explicit status: “Valid”, “Canceled”, or “Expired”. |
| Primary | Event title. |
| Secondary | Event start date/time with venue time zone, and venue name. |
| Auxiliary | Gate and section/row/seat when assigned; use “General admission” when applicable. |
| Details/back | Full venue address, doors time if known, admission instructions, ticket reference, support contact and “Ticket details” link. Retain date/location on the front; details supplement them. |
| Barcode | Generate using system barcode facilities from the issuer's current admission token. Never embed a screenshot or a barcode in decorative artwork; no user editing/uploading of the credential. |

Bind fields to canonical event/ticket data, using stable field identifiers for updates. Do not invent unknown gates, seats or doors times. Include event time/location relevance metadata; supplying venue coordinates does not require collecting the person's location. Keep essential information in fields rather than images, including when a pass also appears on Watch. Inspect Watch overflow/cropping before release; iPhone scope does not establish Watch rendering success.

“Ticket details” opens the exact event and ticket in the installed app through a supported link, with an HTTPS equivalent when the app is unavailable. It shows admission status, venue/address, directions destination, and cancellation/refund information when relevant. It never opens the marketing home page. Authenticate only when needed for private management actions; preserve the ticket destination through sign-in and app interruption. Use opaque identifiers in links, with no embedded identity data or admission token. An unavailable ticket shows “Ticket unavailable” with retry/support, not a generic landing page. Do not place invented custom buttons inside the Wallet pass.

## Credential and lifecycle contract

- After confirmed purchase/registration, offer the system Add to Apple Wallet flow. Canceling addition leaves the ticket available in the app. Stop unsolicited repeat suggestions after refusal; keep a deliberate Add action available for absent or removed passes. For an existing pass, expose View in Wallet. Do not duplicate a ticket on re-add.
- The issuer is authoritative for token validity and event state. Replace the screenshot with a machine-readable credential, not a promise of screenshot resistance. Use an opaque token without personal details; scanner-side validation must reject revoked/canceled credentials. Token format, refresh and offline scanner policy require implementation verification.
- Active ticket: show “Valid” only when the issuer considers admission valid. Encode event times with a time zone and format visible dates for the user's locale. Persist the selected ticket across interruption; keep the saved pass usable without opening a marketing website.
- Changed date, time, venue or gate: update the same pass and relevance metadata from the issuer. Use an interruptive change message only when the change is time-critical; never for advertising or a minor support edit.
- Canceled event: revoke admission at the issuer, update the same pass to “Canceled”, apply supported voiding metadata, and stop presenting a usable admission barcode in the delivered canceled pass. Retain event name/date/venue for recognition. Details say “This event is canceled. This ticket cannot be used for entry.” Link to this ticket's actual refund/support state; do not promise an unconfirmed refund. A cancellation merits a time-critical change message.
- Expired ticket: set accurate expiration metadata and show “Expired”; it must not remain labeled Valid. Do not delete a canceled or expired pass without permission.
- Delivery failure/offline: retain the last received pass, retry delivery when connectivity returns, and show the last confirmed state plus update time on the app's ticket page. An issuer cancellation cannot instantly change an offline Wallet copy. The admission system must reject the canceled token even if a stale pass still says Valid. Do not describe a queued update as delivered.

## Data minimization

| Data | Purpose and handling |
| --- | --- |
| Event, venue, seat/gate, status | Needed for admission and wayfinding; expose as structured pass fields. |
| Opaque ticket reference/token | Needed for support/validation; token contains no identity attributes and is treated as a credential. |
| Full name, birth date, home address, email, phone, government ID details | Not needed by this supplied admission task. Omit from front, back, barcode payload, artwork, URLs and change messages; adding to Wallet must not newly collect these. |

No camera, contacts, tracking or user-location permission is required to add or show this ticket. No Wallet identity-verification flow is introduced. If a future venue requires identity verification, specify its actual purpose, minimum attributes and alternative process separately; do not print identity data on this pass. Review disclosures if actual data handling changes.

## Release acceptance contract

1. Inspect a generated pass: event-ticket style, structured title/date/time/venue/seat fields, meaningful collapsed header, icon and system barcode configuration; no screenshot credential or unnecessary identity data in any payload or asset.
2. On supported iPhones, add/cancel/refuse/remove/re-add/view the same ticket. Verify system UI, no duplicates or repeated unsolicited prompts, and preserved destination after interruption/sign-in.
3. Test a specific ticket link with and without the app, signed in/out, and unavailable ticket data. Each resolves to that ticket or its explicit recovery state, never marketing.
4. Exercise valid → changed → canceled and valid → expired. Check issuer rejection of revoked tokens, visible status, voiding/expiry metadata, relevance metadata, truthful refund copy and notification policy. Test delayed delivery and offline phone/scanner cases separately; do not accept stale Valid as proof of admission.
5. Inspect actual iPhone layouts in supported orientations, enlarged text and long localized date/venue/seat values. Confirm essential fields remain discoverable without image text or layout overlap. Inspect the resulting Watch pass if distributed there. Verify the barcode on venue scanners; static field inspection is insufficient.

## Guidance basis

Source-backed choices: [Wallet — Passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Passes), [Pass anatomy](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-anatomy), [Designing passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Designing-passes), [Event tickets](https://developer.apple.com/design/human-interface-guidelines/wallet#Event-tickets), and [Pass images](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-images) support the native model, field hierarchy, lifecycle and barcode correction. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) supports minimum data use. [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) supports a focused glance and preserved context.

Exact field allocation, ticket routing, status copy, issuer/scanner revocation and recovery behavior above are concrete product decisions, not quoted universal HIG requirements. Links identify the official source of the supplied local guidance; no online verification was performed.
