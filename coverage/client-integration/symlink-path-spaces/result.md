# iPad editor button review

Evidence: the supplied brief states that Delete is the default, Publish and Preview have equal prominence, and repeated Publish activation starts duplicate uploads. No implementation, screenshot, or runtime was supplied. The contract below assumes Publish is the editor’s likely completion action; deletion scope and reversibility remain unspecified. No browsing or device execution was performed. This specification preserves the existing framework.

## Findings and source support

| Finding from the brief | Effect | Guidance and correction |
| --- | --- | --- |
| Delete is the editor default. | Default activation can cause unintended loss. | [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) generally assigns primary to a likely nondestructive action. Remove Delete’s editor default mapping and give it a destructive role. |
| Publish and Preview have equal prominence. | The expected completion path is unclear if Publish is the primary task. | [Buttons — Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) allows one or two prominent likely actions; equal prominence alone is not a universal violation. For this proposed hierarchy, emphasize Publish and give Preview secondary styling, without unequal peer sizes. |
| Repeated Publish starts duplicate uploads. | One publishing intent produces multiple operations. | [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS) calls for an activity indicator within the activating button during delayed completion. The single-operation guard and idempotency contract below are engineering recommendations, not a quoted HIG network requirement. |

## Corrected action contract

| Label / accessible name | Outcome and scope | Role, default, and surface | Availability and recovery |
| --- | --- | --- | --- |
| Publish | Publish a captured revision of the current document to its configured destination. | Primary, visually emphasized editor action. If a default keyboard action is supported, map it to Publish only in the appropriate command context; Return while editing text must retain text-entry behavior. | Enabled when valid, unpublished changes exist and no publish is pending. Explain unmet prerequisites nearby. Preserve the draft on failure. |
| Preview | Open a preview of the current draft without publishing or modifying it. | Normal, secondary action on the editor action surface. No default mapping. | Available when a preview can be rendered; closing returns to the draft and restores focus. During publishing, preview may remain available for the captured revision if supported. |
| Delete | Delete the current document; the shipped label must identify the actual object if context is ambiguous. | Destructive, lower emphasis and clearly separated from Publish. Never the editor default. | Block deletion of the publishing document while its operation is unresolved, with an explanation. Final recovery/confirmation policy depends on actual deletion semantics. |

Use existing platform controls/styles where available. Keep peer visual sizes consistent and distinguish emphasis through style. Each selectable region must be at least **44 × 44 pt**, with enough separation to avoid accidental selection; measure hit regions independently of glyph size. Custom controls need perceivable press feedback. Text names must identify outcomes, including for any icon-only variant. See [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and [Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content).

### Publishing state transitions

1. **Ready → Publishing:** atomically acquire a guard for the document/revision before starting work, capture the revision and destination, and assign a stable operation identity. Every activation path uses the same guarded command.
2. **Publishing:** show an activity indicator inside Publish, replacing an image if present; optionally label it “Publishing”. Make it unavailable and expose its busy/unavailable state accessibly. Ignore or coalesce touch, keyboard, accessibility, and programmatic reactivation into the existing operation. UI disabling alone is insufficient protection.
3. **Publishing → Published:** only report success after authoritative completion. Show contextual success, record the published revision, release the guard, and keep Publish unavailable until new publishable changes exist. Late callbacks must not overwrite newer state.
4. **Publishing → Failed:** preserve the draft, explain the failure in context, release the guard, and offer an explicit retry. A retry of the same intent must reuse/reconcile its operation identity so a lost response cannot create a second publication. Coordinate idempotency with the receiving service; if that service lacks it, track/reconcile uncertain results before starting another upload. Do not label an uncertain completion as a definite failure or success.

These concurrency and recovery choices are proposed product/engineering behavior. They do not prescribe an SDK or framework. Editing may continue only if the UI clearly distinguishes the captured publishing revision from newer draft changes.

### Delete decision

Determine whether Delete is reversible before implementation approval. Common undoable deletion generally needs no confirmation; uncommon irreversible destruction warrants confirmation. See [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices).

For an irreversible current-document deletion, proposed confirmation copy is **Delete This Document?**, with **This permanently deletes this document.**, **Delete**, and **Cancel**. Verify the statement against actual storage and publication behavior before shipping. Cancel leaves the document intact and restores focus. Choose no default in this confirmation to require deliberate selection; support Escape or Command-Period on an attached keyboard. This is a conservative product choice: the [Alerts — Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) guidance explicitly permits a normal default for confirmation of deliberately requested destruction, so destructive actions are not universally forbidden as alert defaults. That exception does not justify Delete as this editor’s default.

## Proposed checks and evidence status

**Passed — document inspection only:** installed root → menus-and-actions family → buttons topic procedure → buttons guide read in order, one cat command per file. The conditional confirmation decision also followed presentation → alerts procedure → alerts guide. All paths came from installed links under `.agents/skills/apple-hig`; no source-package sibling path was used. The written contract covers outcomes, roles, surfaces, keyboard behavior, geometry, and pending/resolved states.

**Failed — reported behavior, not independently reproduced:** Delete is the editor default; repeated Publish creates duplicate uploads. Equal Publish/Preview emphasis is a mismatch with the proposed primary-task hierarchy, not a proven standalone HIG violation.

**Not executed — acceptance checks:**

| Check | Acceptance condition | Verification method |
| --- | --- | --- |
| Activation and defaults | Publish targets the captured document/revision; Preview has no publication side effect; Delete targets only the named object. Return in text entry does not delete or publish. | Command/handler checks, then attached-keyboard iPad checks. |
| Repeated activation | Rapid mixed input and concurrent command calls start one operation; retries after timeout/lost response create at most one publication. | Instrumented concurrency and receiving-service integration checks, including uncertain completion. |
| Pending and resolution | In-button activity indication appears promptly; repeat activation is blocked; authoritative success, failure, and late callbacks produce the specified state. Draft content survives failure. | State-transition checks with delayed, failed, and reordered responses; visual iPad verification. |
| Delete and cancellation | Actual reversibility matches the chosen policy; confirmation Cancel and keyboard cancellation leave data intact. Any supported recovery restores the affected document. | Storage/handler checks and iPad interaction checks after deletion semantics are established. |
| Accessibility and feedback | Names match outcomes; focus order is meaningful; busy/disabled reasons are understandable; focus returns after Preview or cancellation; custom press feedback is perceivable. | Inspect semantics and perform VoiceOver, keyboard, and touch checks on iPad. |
| Geometry and enlarged text | All targets measure at least 44 × 44 pt, remain separate, and labels neither clip nor overlap at enlarged text sizes and supported iPad layouts. | Layout measurements plus iPad rendering checks. |

No code, service integration, SDK compilation, assistive-technology behavior, or physical-device behavior has been verified. Proposed checks are not test passes.
