# Result

Patched `interface.md` in place from the one-sentence brief into a concrete iPhone Wallet event-ticket specification. It replaces the mutable barcode screenshot with a system-generated credential, exposes event date/time/venue in structured fields, routes to the exact ticket, defines cancellation/expiration/update behavior, and removes unnecessary identity details from all pass surfaces and payloads.

## Decisions

- Use a standard nonposter event-ticket pass. This matches venue admission and avoids artwork-dependent essential information. Wallet owns rendering; API support remains to be verified.
- Keep event identity and admission status visible, with seat/gate and useful details behind them. Add/View, refusal, removal and re-add now have explicit behavior.
- Treat cancellation as both credential revocation and a pass update. Preserve the canceled ticket for recognition and support, rather than deleting it. Offline delivery can leave stale UI; scanner enforcement is a separate requirement.
- Remove identity data rather than moving it to the back. An opaque credential is still sensitive and does not by itself prevent screenshot reuse.
- Exact ticket routing, field placement, recovery copy and scanner policy are proposed product requirements. They extend the supplied HIG guidance; they are not asserted Apple API guarantees.

Official source links and their material recommendations are included in `interface.md`, using only the installed local snapshot.

## Worked before/after

Illustrative fixture, not supplied production event data: “Harbor Lights”, November 14, 2026, 7:30 PM America/New_York, Harbor Hall, Gate B, Section 102 / Row C / Seat 8.

Before: a mutable barcode screenshot; no visible event date/location; opening details goes to marketing; after cancellation it still says Valid; unnecessary identity details are printed.

After, while active: primary “Harbor Lights”; header date and “Valid”; structured start time with venue time zone and “Harbor Hall”; assigned gate/seat; system barcode from an opaque issuer token. Ticket details opens this ticket's app/web destination. No birth date, address, email or ID data appears in pass content.

After issuer cancellation: revoke the token, deliver an update for the same pass showing “Canceled” and supported voiding metadata, remove its usable admission barcode, retain event context, and show “This event is canceled. This ticket cannot be used for entry.” The ticket destination supplies confirmed refund/support information. If the phone is offline, its old pass may remain visible; the issuer/scanner must reject the canceled token. The specification does not promise instantaneous Wallet updates.

## Acceptance evidence

Passed — static specification inspection:

- All five supplied defects have explicit corrections in the edited artifact.
- Field hierarchy, precise destination/fallback, addition/refusal/re-add, cancellation/expiry, delayed update recovery and data-purpose handling are specified.
- Release checks cover payloads/assets, device layout, interruption, links, state transitions, notification policy, offline behavior and scanner validation.

Failed — original brief against the revised contract: screenshot credential, hidden event information, generic marketing route, canceled-as-Valid status and unnecessary identity exposure. These are reported brief defects, not independently reproduced runtime failures.

Not executed — pass generation/signing/schema validation, SDK compilation/API availability, Wallet addition/rendering or update delivery, iPhone/Watch layout, localization/text-size execution, VoiceOver or other accessibility execution, deep-link/authentication execution, barcode scanning, offline scanner enforcement and security testing. The acceptance scenarios in `interface.md` are release requirements, not passed tests.

## Evidence limits and route

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, inspected the original `interface.md`, and searched the complete topic index for Wallet/ticket/iPhone concepts. Read the Getting started, Technologies and Foundations family instructions; then the Designing for iOS, Wallet and Privacy topic procedures before their respective source guides. Each instruction/source file was consumed by a separate `cat` command. The task is a specification repair; no application implementation or runtime artifacts were supplied.

Used only project files and installed instructions. The local guides identify a dated HIG snapshot, not an SDK reference or independently established runtime result. Official links are provenance, not evidence of browsing. No web, GUI, device, SDK or accessibility execution is claimed. Watch crop/layout behavior remains a distribution check, not an assertion that all iPhone fields render identically there.
