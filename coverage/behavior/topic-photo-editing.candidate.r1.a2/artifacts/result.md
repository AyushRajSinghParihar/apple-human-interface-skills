# Revised iPhone photo editing interaction specification

## Scope and decisions

The supplied `interface.md` says opening overwrites the original, Cancel commits filters, export claims location removal without checking, and interruption can strand an unsaved crop. Those statements are the observed baseline; no implementation was supplied. This specification covers a standalone iPhone editor and its Photos editing extension. Extension hosting is a requested design target, not an existing capability established by the brief.

1. **Opening is read-only.** Retain immutable source identity, bytes and metadata. Create a separate working recipe and preview. Save writes a new output file and versioned adjustment recipe; it never replaces source bytes. Keep the original available for future re-editing. This follows the new-file/original-preservation contract in [Photo editing](https://developer.apple.com/design/human-interface-guidelines/photo-editing).
2. **Preview precedes completion.** Choosing a filter or moving a crop updates the visible preview and keeps the editor open. Fit the resulting image in view after applying or undoing a crop. In the extension, use the supplied system top toolbar for cancellation and completion, without a second Done/Cancel toolbar; retain the containing app’s icon as the extension identity. These are [Photo editing best practices](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Best-practices).
3. **Cancel never commits.** With no effective changes since entry, Cancel returns immediately. With changes, explain loss and offer “Discard Changes” and “Keep Editing.” Discard removes this session’s draft and returns without an edited result; Keep Editing restores the exact preview and tool context. Undoing all changes makes the session clean again. Changed-only confirmation follows [Photo editing](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Best-practices); the exact copy and semantic dirty comparison are product decisions.
4. **Reversible adjustments have meaningful units.** One continuous crop drag or filter-strength drag is one history entry; discrete filter selection is one entry. Undo restores the prior recipe, redo restores the undone recipe, and a new edit clears redo. Keep the meaningful sequence since entry, including after draft checkpoints. Expose operation-specific labels such as “Undo Crop” and “Redo Filter”; where the system supplies Undo/Redo title text, supply only “Crop” or “Filter.” Preserve standard iPhone undo gestures/shake when integrated. These decisions apply [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices) and its [iOS guidance](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#iOS-iPadOS).
5. **Draft preservation is distinct from saving.** Checkpoint work locally without publishing an edited asset or reporting success to Photos. Preserve the recipe, unfinished crop, undo/redo history, tool, selection, zoom and viewport on interruption. This applies [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking#Best-practices); the persistence and transaction design below are engineering choices.
6. **Export claims require evidence from the final output.** Default “Remove location from exported copy” to on. Strip location fields, encode, then inspect the actual output bytes, including supported embedded metadata containers. Only a successful supported-format check permits “Location metadata removed from this copy.” Unknown or failed verification blocks delivery with removal enabled. Offer Retry or Back to Editing; never silently include location. Turning removal off requires an explicit choice and copy “Location metadata may be included.” This verification policy is a product requirement derived from truthful communication and minimization in [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), not a metadata API guarantee from HIG. Visible landmarks and location inferred from image content are outside this claim.

## State and data contract

Framework-agnostic records:

```text
Session = {sessionID, mode: app|extension, sourceID, sourceVersion,
           immutableSource, entryRecipe, workingRecipe, pendingToolState,
           undo, redo, viewport, revision, durableRevision, phase}
phase = editing | confirmingDiscard | saving | saveFailed | returned

effectiveRecipe = combine(workingRecipe, pendingToolState)
dirty = canonical(effectiveRecipe) != canonical(entryRecipe)
```

Canonical comparison includes effective crop and filters, not selection, zoom, preview caches or revision counters. A no-op adjustment creates no history entry. An unfinished crop that changes the image counts as dirty. The entry recipe may contain previously saved edits: Cancel restores that entry version, not necessarily the unedited original. “View Original” temporarily compares against immutable source without modifying recipe or history; release returns to the working preview.

| Event | Transition and visible result | Persistence / host effect |
|---|---|---|
| Open from app or Photos edit mode | Enter editing with entry preview; no automatic dismissal | Read source; initialize session; no asset write |
| Filter choice / crop movement | Show resulting preview immediately | Journal draft updates; no source or host mutation |
| End adjustment | Group increments into one named history operation | Persist recipe and inverse; clear redo for new work |
| Undo / redo | Restore recipe and show affected image region | Persist history cursor; recompute dirty |
| Cancel, clean | Return immediately | Delete session draft; extension reports cancellation once |
| Cancel, dirty | Enter confirmingDiscard with “Discard these edits? Your changes from this editing session will be lost.” | No result sent and no image saved |
| Keep Editing / dismiss confirmation | Return to editing with same context | Retain draft |
| Discard Changes | Return to invoking photo/context | Delete draft and temporary output; report cancellation once |
| Save/Done, dirty | Finalize pending adjustment, freeze revision, enter saving; show “Saving…” | Render to a separate temporary file; validate and commit as below |
| Save/Done, clean | Return unchanged without a new edited file | App closes editor; extension reports unchanged completion through host adapter |
| Render, storage or host failure | Enter saveFailed; show “Couldn’t save your edits.” with Retry and Keep Editing | Retain draft and original; no success claim |
| Successful save | Return to invoking photo with edited version visible | Publish new file/recipe; extension returns accepted edited result once |
## Save and extension return transaction

The following operations describe required semantics, not Apple API names:

```text
save(session):
  require phase in {editing, saveFailed}
  capture immutable snapshot including pending crop; assign transactionID
  phase = saving; reject duplicate completion and editing input
  output = renderToNewTemporaryFile(source, snapshot.recipe)
  validate decodable output and intended dimensions
  require output identity != source identity
  require source bytes and source metadata unchanged
  persist output + versioned recipe + transaction status atomically
  if mode == app:
    publish a new edited version linked to the original
  else:
    submit edited file + adjustment recipe via host adapter
    wait for host acceptance; keep original and recoverable draft until resolved
  mark transaction accepted; remove session draft; phase = returned
```

The extension opens from Photos edit mode and stays there while previewing. Successful completion returns control to Photos on the same asset, showing its accepted edited version. Cancellation returns to the invoking Photos editing context without applying the session’s changes. Do not open the containing app to complete the edit. Do not add extension export/share controls that compete with the host’s completion flow; standalone export is a separate operation.

Use a transaction identity to suppress double taps and duplicate return attempts. If suspended during saving, persist the phase and transaction before suspension; complete eligible input-free work only when the host/runtime permits it. If acceptance is uncertain, reconcile host status before retrying or announcing failure/success. Never blindly submit a second edited result. A host adapter must define unchanged completion, acceptance acknowledgement, cancellation and reconciliation; exact SDK calls and host capabilities remain unverified. During saving, show completion as unavailable; do not allow Discard to race an in-flight host commit.

A separate exported copy is not an edit-session save. Export snapshots the selected recipe, applies the metadata choice, validates the encoded file and passes only that exact validated file to the destination. It does not change the source, entry recipe, dirty state or undo history. A failed export leaves editing intact. Report destination completion only when delivery is acknowledged; verification alone does not prove delivery.

## Interruption and recovery

Persist draft changes during editing rather than relying solely on a final lifecycle callback. For continuous crop movement, preserve the latest durably acknowledged crop coordinates and gesture-start recipe; recovery closes that gesture as one history unit. Do not show a change as safely preserved before its journal write succeeds. If storage fails, keep the live preview but say “Changes aren’t saved on this device. Keep the editor open and try again.” No persistence design guarantees a write that never reached storage.

| Event | Required recovery |
|---|---|
| App switch, lock, transient system interruption | Checkpoint current crop/tool context; no save, discard or cancellation implied. On return restore the same preview and context without routine notifications. |
| Process termination and reopen | Restore the durable draft tied to source identity/version. Offer “Resume Editing” or “Discard Draft”; never silently publish it. |
| Extension terminated by host | Persist privately where supported. On a later invocation for the same source/version, offer recovery; do not promise that the host will reopen the extension automatically. |
| Source removed, permission revoked or version changed | Keep draft separate; explain the source is unavailable or changed. Allow retry/reselection where identity can be verified, or explicit discard. Never apply the recipe silently to a different asset/version. |
| Interruption during save/export | Reconcile transaction status; resume or retry only without duplicate delivery. Retain the draft until success or explicit discard. |

Undo history survives draft recovery. A successful save closes the session; reopening starts a new undo boundary at the saved recipe, while retaining the original and editable recipe. The original is therefore recoverable even though per-session gesture history does not span completed sessions.

## Data access and privacy

| Data | Purpose and minimum access | Retention / transfer |
|---|---|---|
| Selected source photo and existing metadata | Preview, edit and render only the selected asset | Local processing; immutable original retained; no upload specified |
| Recipe, unfinished crop and source reference | Interruption recovery and future re-editing | Private local storage; session draft deleted after confirmed save or explicit discard; saved recipe retained with edited version |
| Existing location metadata | Remove from exported copy when requested | No device-location lookup; do not request current location permission for stripping existing metadata |
| Export output | Deliver chosen copy | Only after validation and user-initiated export; temporary files deleted after delivery or abandonment |

Request access only when opening the chosen photo or choosing a protected destination requires it; a denied destination must not block continued editing. Example purpose copy, only if applicable to the actual integration: “Access this photo to preview and save your edits.” Do not infer broad library access from extension entry. Keep release privacy disclosures aligned with actual storage and transfer behavior. These decisions apply [Privacy permission guidance](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission); permission prompts and entitlements require implementation verification.

## Worked before / after

**Before, from the brief:** Opening photo A replaces its original. Selecting a filter and tapping Cancel still commits it. An interruption leaves a crop unsaved. Export asserts location removal without checking.

**After, illustrative trace:**

1. Open A, source version 7, original hash H. Entry recipe is empty; no file changes.
2. Select Warm, then drag a crop from full frame to normalized rectangle `(0.10, 0.10, 0.80, 0.70)`. Preview remains open. History contains Filter and Crop; draft contains the pending/current rectangle.
3. Switch apps mid-crop and return. Restore the durable crop and tool selection. Undo Crop visibly restores full frame with Warm retained; Redo Crop restores the rectangle.
4. Tap Cancel. Choose Keep Editing in the changed-state confirmation. Nothing is committed or returned.
5. Tap Save in the supplied extension toolbar. Create output B and recipe R; B differs in identity from A. After host acceptance, return to the same photo in Photos showing B; A still hashes to H.
6. In a separate export example from the app, export with location removal enabled. Verification finds residual GPS data: deliver nothing and offer Retry/Back to Editing. Only after a fresh encoded output passes verification may it be delivered with the scoped removal message.

Alternate exits: Cancel immediately after step 1 returns without confirmation; Discard at step 4 returns without B and removes this session’s draft; undoing Crop and Filter before Cancel also returns without confirmation.

## Acceptance checks and evidence status

**Passed — specification inspection only:** The revised contract separates immutable source, draft, output and export; defines clean/dirty cancellation, preview, history units, interruption recovery, new-file save, host return and failure paths; and scopes metadata claims to checked output. Local root, routed families, topic procedures and supporting references were read. These are document checks, not executed software tests.

**Failed — supplied baseline description:** Opening preserves the original; Cancel avoids commits; location-removal claims have verification. Each conflicts with `interface.md`. Crop recovery is unspecified and therefore unestablished, rather than a demonstrated runtime failure.

**Not executed — acceptance scenarios for implementation:**

| Check | Observable pass condition |
|---|---|
| Open, edit, cancel, save and export | Original identity, bytes and metadata stay unchanged throughout; successful save has a distinct output identity |
| Clean vs dirty cancellation | Clean returns without prompt; dirty explains loss; Keep Editing retains exact state; Discard sends no edited result |
| Effective dirty state | No-op crop/filter and undo-all are clean; unfinished effective crop is dirty; view-only changes are clean |
| Preview and extension shell | Every adjustment can be inspected before return; supplied toolbar only; correct containing-app icon; no forced containing-app launch |
| History | Filter → crop drag → undo → redo restores exact recipes; drag is one operation; new edit after undo clears redo; restored crop is visible; standard iPhone interactions work |
| Interruption | App switch, lock and process termination restore the durable crop, history and viewport without publishing; storage failure is surfaced |
| Save transaction | Rendering/storage/host failures keep draft; duplicate taps and interrupted acceptance produce at most one result; no premature success |
| Extension return | Clean cancel, changed discard, unchanged completion and accepted save each return once to the correct Photos context; host termination follows recovery contract |
| Export privacy | Known GPS fixtures are stripped and final bytes inspected; unsupported containers and verification errors block protected export; source metadata stays intact |
| Access failure | Revoked source access or denied destination preserves the draft and provides recovery without unrelated permission requests |

## Evidence limits and source route

Only local text was inspected and this specification was written. No device, SDK, build, GUI, accessibility, Photos-hosting, filesystem transaction, metadata parser or lifecycle execution occurred. No Apple API availability, metadata completeness, image fidelity, permission behavior or background-execution entitlement is established. Real implementation must prove the checks above, especially host acknowledgement/reconciliation and private draft persistence across extension termination. Live Photos, video and preservation of live frames are outside this still-photo specification; they require their own scoped design before support is claimed.

Installed package route: `apple-hig/SKILL.md` → topic-index search → technologies family → photo-editing procedure → photo-editing reference; patterns family → undo-and-redo and multitasking procedures → their references; foundations family → privacy procedure → privacy reference. All paths were resolved beneath `.agents/skills/apple-hig/`. References identify a 2026-10-25 local snapshot and describe derived application guidance. Official links above are attribution from those local files, not evidence of web retrieval or current SDK verification. Exact state schemas, copy, transaction rules, recovery policy and metadata verification are proposed product/engineering decisions; they are not asserted as literal Apple mandates.
