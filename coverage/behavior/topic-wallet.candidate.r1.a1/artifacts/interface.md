# Venue ticket pass — revised specification

Platform: iOS, iPhone Wallet. Task: identify the event and present admission quickly. This is a design contract; no implementation or supported OS range was supplied.

## Pass and field contract

Use a PassKit nonposter event-ticket pass with Wallet-owned rendering and navigation. Essential information must be structured fields, never solely artwork. Supply appropriate event semantics where supported and retain visible fallback fields. Verify exact schema and SDK availability during implementation.

| Area | Content |
| --- | --- |
| Logo/name | Recognizable issuer or venue |
| Collapsed header | Explicit status: Valid, Canceled, Used or Expired |
| Primary | Event name |
| Secondary | Event date and start time, including venue time zone |
| Auxiliary | Venue name, gate and assigned section/row/seat; otherwise General admission |
| Barcode | System-rendered barcode using an issuer-controlled opaque admission credential and a scanner-compatible format |
| Details/back | Full venue address, doors time if known, ticket reference, status explanation, exact-ticket management/support link and essential terms |

Unknown date/location reads “Date to be confirmed” or “Venue to be confirmed”; do not hide it. Omit unknown gates/seats rather than inventing them. Use locale-appropriate dates and explicit time-zone information. Keep status as text, not color alone. Provide known event time/location as relevance metadata; no user-location permission is needed to display the venue.

Never embed a screenshot barcode or offer a barcode editor. Authorized issuer updates change credentials. System rendering does not itself prevent copying/replay: admission validation must check current event/ticket status and redemption state.

Supply an icon and efficient @2x/@3x PNG branding assets. The local guide specifies icon.png at 38 × 38 pt and the chosen style's logo.png at 50–160 pt wide × 50 pt high. Omit optional background artwork until legibility is verified. Keep essential information available in Watch fields/details if the pass appears there; do not assume identical cropping or placement.

## Add, view and destination

After purchase/registration offer system Add to Apple Wallet. Existing passes get View in Wallet; absent/removed passes retain Add. Canceling addition preserves the ticket page and stops repeated suggestions. Failed delivery offers Retry and support.

The pass's app/website destination opens this exact event and ticket with current status, entry details and management/support options. Supply an equivalent HTTPS destination when the app is absent. Preserve the ticket route through authentication and interruptions. Never route to a marketing homepage, put the admission token or personal details in a URL, or authorize account changes merely from URL possession.

Wallet owns its orientation/navigation behavior. The companion ticket page must preserve the selected ticket and usable actions through rotation, enlarged text and returning from Wallet.

## Lifecycle contract

The issuer record is authoritative. Maintain a stable pass identity for updates and order updates by source revision so delayed delivery cannot restore stale state.

| Trigger | Result |
| --- | --- |
| Issued for active event | Valid; display event details and credential |
| Date/time, venue or gate changes | Update fields, semantics and relevance on the same pass; reflect the same information at the ticket destination |
| Event canceled | Void using supported Wallet lifecycle facilities; status Canceled; “Event canceled. See ticket details for next steps.” Backend immediately rejects admission |
| Ticket revoked | Void; explain “Ticket no longer valid. Contact ticket support.” Backend rejects admission |
| Redeemed | Used; update the pass and redemption record to prevent reuse under venue policy |
| Admission window ends | Expired; set expiry to the issuer's actual admission window, not an invented duration |

Cancellation overrides prior valid/used/expired presentation. Ordinary event edits never reactivate canceled tickets; reinstatement needs a separately authorized issuer decision and credential policy. Do not promise refunds until confirmed; the ticket destination gives known next steps and support.

Send updates promptly and retry failures. Interruptive change messages are reserved for time-critical changes such as cancellation or imminent venue/time changes, never marketing or minor terms edits. Obtain permission before deleting a pass; cancellation must not silently remove the record.

An offline Wallet pass may retain its last delivered state. Do not call it live or promise immediate synchronization. Cached credentials remain presentable offline, but admission eligibility requires current issuer validation. A scanner without current validation sends the attendee to staffed resolution rather than accepting a cached Valid label. If the companion page cannot fetch status, show “Unable to refresh ticket status” with Retry/support; do not claim current validity.

## Minimum data

| Data | Purpose and boundary |
| --- | --- |
| Event/time/venue, gate/seat, status | Identify event and support entry; visible fields and appropriate semantics |
| Opaque credential and ticket reference | Admission/support; no identity attributes embedded; exclude credential from logs/analytics |
| Holder name, birth date, home address, email, phone, government ID | Omit from artwork, fields, back/details, barcode and URLs; no demonstrated admission need |

Keep existing purchase-account records outside the pass. No new identity verification, tracking, contacts or location permissions are part of this repair. A future identity requirement needs separate justification. Existing authenticated ticket management remains required; this specification does not certify security.

## Guidance basis

Applied local guidance, without browsing: [Wallet passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Passes), [anatomy](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-anatomy), [designing passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Designing-passes), [event tickets](https://developer.apple.com/design/human-interface-guidelines/wallet#Event-tickets), [images](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-images), [watchOS](https://developer.apple.com/design/human-interface-guidelines/wallet#watchOS), [Privacy best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), and [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

Nonposter style, exact copy, opaque tokens, backend validation, revision ordering and offline staffed resolution are concrete product decisions. HIG does not define this venue's security protocol or delivery guarantees.
