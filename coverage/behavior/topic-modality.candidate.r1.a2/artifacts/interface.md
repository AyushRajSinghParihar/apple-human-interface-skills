# Draft composer — revised state specification

Platforms: iOS and iPadOS. This is a behavioral contract, independent of framework.

## Task and presentation

Create or revise one draft from Browse, then save it and return to the same browsing context. Done saves a draft; it does not publish or send. This scope is a product decision because the original specification defines no publishing operation.

Use one modal composer sheet to focus this short parent-related task. Browse is visible where space permits but blocked while the composer is open. Never present attachment or settings sheets above it. Attachment selection and draft-specific settings are internal navigation destinations. Unrelated app settings remain in Browse and are unavailable until the composer closes.

| Destination | Title | Visible navigation/actions |
| --- | --- | --- |
| Composer root | New Draft, or Edit Draft when reopening | Cancel at top leading; Done at top trailing; Attachments and Draft Settings in content |
| Attachment list/detail | Attachments / attachment name | Back to previous internal destination; Add/Remove in content |
| Draft settings | Draft Settings | Back to root; changes apply to the working draft |

Back never exits the composer or destroys writing. Child destinations do not also show Cancel and Done. A system swipe-back, where supported, is equivalent to Back. Root has no Back action. Root Cancel and supported vertical dismissal are exit requests, not deletion commands.

On iPhone use a large-only composer sheet so writing is not confined to half height. On iPad prefer standard centered page/form sizing, adapting to compact window widths without creating a second composer. Do not add a custom resize gesture. If the implementation permits resizing, use the system grabber. Preserve text, selection, attachment state and internal route through rotation, keyboard changes and iPad window resizing. Keep actions and editor scrollable/reachable with the keyboard and enlarged text. Touch must reach every action; pointer and attached keyboard activate the same visible actions. Supported Escape/Command-Period requests exit, except when a decision is open, when it cancels that decision.

## Draft ownership and recovery

The editor owns a stable draft ID, working revision, last explicitly saved baseline, text, ordered attachment records (including locally retained file references and upload state), draft settings, selection and internal route. The sheet's visibility never owns this data.

Dirty means meaningful text, attachment or settings changes relative to the baseline. A new untouched draft is clean. Empty text is a valid saved draft if attachments or settings contain work; Done is disabled only for a completely untouched new draft, with inline explanation: “Add writing or an attachment to save a draft.” An existing clean draft can finish without a new revision.

Persist a recovery checkpoint as edits are accepted; serialize writes by draft ID and revision so late completions cannot overwrite newer work. Checkpoints are recovery data, not explicit Done saves. Retain local attachment content until explicit deletion or successful ownership transfer. Upload success or failure must not delete text or make it impossible to save locally.

Backgrounding checkpoints the working state without treating it as Cancel. After process interruption, offer the recovered draft from Browse; resume its text and attachments, restoring a valid internal route and selection where available. Never restore an obsolete decision overlay. Unacknowledged writes during abrupt termination are not guaranteed; implementation must define and test the durability boundary. Save/checkpoint failure keeps the working copy, shows an inline error and Retry, and prevents a successful save-and-close outcome from being reported. No timer silently deletes recovery data.

## State and transition contract

Primary state: Browse or Composer(draft ID, route stack). Operation: idle, saving or discarding. Decision: none or exitDecision(draft ID, revision, return route). One owner serializes all transitions; do not use independent presentation booleans.

| Event / guard | Transition and data outcome |
| --- | --- |
| New Draft / Resume from Browse | Open one Composer; initialize or recover the same draft ID; retain Browse selection and scroll position |
| Attachments / Draft Settings | Push internal destination; preserve working state; repeated activation cannot duplicate the route |
| Back in child | Pop one destination, retaining edits and attachment operations; focus returns to the initiating control |
| Done at root, idle | Persist latest revision as saved baseline; after success clear its recovery checkpoint and close to Browse, showing that draft; failure stays open with inline Retry |
| Cancel, vertical dismissal, supported keyboard exit or app navigation away; clean | Close to previous Browse context without deletion; remove only an untouched new placeholder |
| Same exit request; dirty | Intercept before dismissal; keep composer visible and open one exitDecision; freeze draft edits while deciding |
| Repeated exit request with decision already open | No-op; retain the original draft ID, revision and return route |
| Exit decision: Save Draft | Dismiss decision, enter saving, save that revision locally; close only after success; failure returns to originating route with all work and inline Retry |
| Exit decision: Discard Changes | Dismiss decision, enter discarding; explicitly remove new draft/checkpoint or restore existing saved baseline and remove newer checkpoint; close only after success; failure keeps working copy and offers Retry |
| Exit decision: Cancel, outside dismissal or supported keyboard cancellation | Close only the decision; return to exactly the previous composer destination and working revision |
| Exit request while saving/discarding | Coalesce; do not initiate another operation, decision or dismissal |
| Background/interruption | Checkpoint and retain work; hide transient decision if necessary; resume without executing an unresolved choice |

Exit decision title: “Save this draft?” Message: “Save your changes, or discard them and close.” Actions: destructive Discard Changes first, Save Draft, and safe Cancel. No destructive keyboard default. On iPad anchor the platform-adaptive confirmation to the visible exit control, using root Cancel as the anchor for gesture/keyboard requests. Outside dismissal means Cancel. Do not implement this as a second task sheet. It is the sole temporary decision overlay over the retained composer.

## Upload errors and competing presentations

Upload failures appear inline beside the affected attachment: “Upload failed. Your draft is kept on this device.” Provide Retry and Remove; Remove affects only that attachment. Selecting an error reveals inline detail and never presents an alert. Repeated Retry starts at most one upload per attachment. Failed uploads remain resumable after saving or reopening; saving a draft does not require network success.

At most one main task sheet and one necessary decision overlay may exist. Routine upload errors cannot acquire the overlay slot. If a future genuinely critical alert is needed, route it through the same single overlay owner; dismiss the active overlay and wait for dismissal completion before presenting a replacement. Never stack alerts. Revalidate queued events against draft ID/revision and current state; drop obsolete events after save/discard/close. Late upload callbacks may update their retained draft record, but cannot reopen a sheet or alert, resurrect discarded content or replace newer edits.

On close restore Browse selection/scroll and focus to the entry control (or saved draft row after Done). On Back or decision cancellation restore the originating control/editor selection. Native focus behavior remains an implementation acceptance check.

## Guidance basis

The installed local HIG snapshot supports clear modal titles/exits, protection of created work, internal Back navigation and serialized presentations: [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). Sheet action placement, composition sizing and centered iPad styles follow [Sheets — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS). Save/discard resolution follows [Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets); inline routine failures follow [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices). These links identify the source articles; no online verification was performed. Revision persistence, exact copy, local-save semantics and event arbitration above are concrete product decisions, not Apple API guarantees.
