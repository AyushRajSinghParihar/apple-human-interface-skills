# Decisions and patch

Replaced interface.md's defect paragraph with a concrete iPadOS/macOS specification covering explicit copy versus collaboration modes, invited-only view defaults, owner/editor/viewer capabilities, invitation lifecycle, persistent management, removal acknowledgment, stale access, specific link destinations, and durable offline conflict recovery. Added exact state copy, cancellation, retry, confirmation, and control contracts.

HIG supports the interaction principles and platform distinctions; owner-only management, seven-day expiry, revision guards, and offline policy are product decisions. Official article links are in interface.md, sourced from installed local guidance rather than live browsing.

## Worked before/after

Before: Morgan shares a link that silently grants edit access. Alex appears active before acceptance, can trigger destructive edits as a viewer, and keeps seeing access after removal. Offline changes may overwrite another writer.

After: Morgan sees “Only invited people · Can view · Only owner can invite” before Send Invitation. Server acknowledgment puts Alex under Invitations as Invited · Can view. Forwarding the link grants no access to another account. Alex's authenticated acceptance moves Alex to People as a viewer, with editing unavailable and server mutations refused. Presence remains separate. If Morgan later grants editing, Alex may write a provisional offline draft. Removal stays pending until acknowledged. On reconnect, authorization precedes upload: removal rejects the shared write, shows access ended, and retains unsent authored text separately. If access remains valid but revisions conflict, both versions survive for review before a guarded commit.

## Acceptance checks and outcomes

Passed — static specification review: copy versus access, recipient scope, capability matrix, pending versus accepted people, management after sharing, changed/revoked access, copy payload, update links, and offline recovery all have explicit contracts. Files were revised as requested. These are document checks, not runtime passes.

| Implementation check | Required result | Execution |
| --- | --- | --- |
| Copy / cancel / unsupported destination | Copy has text without membership metadata; no grant; pre-send cancellation commits nothing; unsupported destinations do not receive misleading payloads | Not executed |
| Forwarded and wrong-account links | No content or implicit membership; account correction or unavailable state | Not executed |
| Pending / expiry / resend / cancel race | Separate invitation group; no false presence; old tokens fail; race resolves to authoritative membership | Not executed |
| Viewer command paths and direct requests | Toolbar, keyboard, context menu, drag, batch, and server mutation all refuse edits/destruction | Not executed |
| Removal/downgrade during queued edit | Stale write rejected; correct role shown; unsent authored draft survives separately; no false Saved | Not executed |
| Failed or uncertain removal / duplicate taps | No premature success; reconciliation and idempotent retry; no offline permission queue | Not executed |
| Foreground/reconnect/update links | Revalidate access and open exact object; revoked person sees access ended | Not executed |
| Offline restart / repeated conflict | Durable draft survives; authorization precedes upload; both versions and reviewed work survive new conflicts | Not executed |
| Confirmations and native controls | Cancel/keyboard dismissal commits nothing; no accidental default removal; actual iPad hit regions and enlarged labels pass | Not executed |
| Apple-device and accessibility behavior | Native sharing, focus restoration, keyboard navigation, and assistive state announcements verified on iPad/Mac | Not executed |

Failed — none established by execution. Original failures are reported facts from the brief, not independently reproduced defects.

## Evidence limits and routing audit

Explicitly read the installed apple-hig root SKILL.md and searched references/topic-index.md. Read owning family, selected topic procedure, then supporting guide for each route: Patterns → Collaboration and sharing; Menus and actions → Activity views and Buttons; Foundations → Privacy; Presentation → Alerts. Every instruction/source file was consumed with its own cat command from this project's installed package.

Used only supplied local files and installed instructions; no web browsing. Source snapshots are dated 2026-10-25; official links are local-source citations, not live verification. No material source conflict was identified. Preserved the distinction between Mac sharing extensions and unsupported Mac activity-view components.

No app code, backend, device, SDK compilation, GUI, delivery, universal-link integration, accessibility, or conflict execution was available or performed. Native rendering, focus order, actual target geometry, server enforcement, and revocation timing remain unverified. Authentication/identity matching, retention implementation, minimum OS versions, and API availability require implementation evidence. This specification establishes no security or platform-integration certification.
