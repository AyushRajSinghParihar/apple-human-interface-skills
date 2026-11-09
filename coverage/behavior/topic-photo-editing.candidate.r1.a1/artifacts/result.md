# Revised iPhone photo-editing interaction specification

Scope: framework-agnostic design for an iOS photo editor and its Photos editing extension. The only supplied product evidence is `interface.md`, a behavioral brief, not executable code. Extension hosting is requested by the task; its current implementation is unknown. Labels below describe semantic actions; a host-supplied completion label may differ.

## Decisions and source basis

1. **Opening is read-only.** Retain an immutable source reference and revision; create a private draft of editing instructions. Render previews from that source and draft. Save creates a distinct output file and keeps the source intact. This corrects the brief's immediate overwrite. The extension uses the supplied system top toolbar and the containing app's icon, without a second completion toolbar. Filter selection stays in the editor for preview. These extension decisions follow [Photo editing, Best practices](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Best-practices).
2. **Cancel never saves.** An unchanged session returns immediately. A changed session asks about losing edits, with a safe way to continue editing. Cancel includes an in-progress crop when determining whether changes exist. This follows [Photo editing](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Best-practices); exact dirty tracking is a product engineering decision.
3. **Reversible adjustments have meaningful history.** One continuous adjustment is one undo unit. Crop and filter changes are distinct units; undo/redo visibly refresh the preview. Preserve standard iOS three-finger and shake affordances where the implementation supports them, with operation wording such as “Crop” or “Filter” following system-provided Undo/Redo text. Follow [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices) and its [iOS guidance](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#iOS-iPadOS). No SDK integration is asserted here.
4. **Interruption preserves a draft, never implies Save or Cancel.** Retain selected asset, crop candidate, recipe, history cursor and editor position. Restore the same task on return, as supported by [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking#Best-practices) and [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). Durable checkpoints and termination recovery below are engineering requirements, not promises made by HIG about extension lifetime.
5. **Privacy copy describes verified output.** Default standalone export to removing location metadata, inspect the final encoded output, and block release if verification fails or is unsupported. Do not display “Location metadata removed” merely because a removal operation ran. Accurate data communication and minimal access follow [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices); the removal/inspection algorithm is our engineering choice, not supplied by HIG.

## State and data contract

Maintain:

```
source = {assetID, revision, immutableBytesReference}
entryRecipe = recipe supplied at session entry, or identity
workingRecipe = editable copy of entryRecipe
cropCandidate = none | {rectangleInSourceCoordinates, rotation, aspectRatio}
history = reversible recipe snapshots + cursor
checkpoint = {source identity/revision, entryRecipe, workingRecipe,
              cropCandidate, history, selectedTool, previewViewport}
phase = editing | confirmingDiscard | preparing | returning | closed
returnID = unique ID for this host session
```

`effectiveRecipe` includes the visible crop candidate. `dirty` means effectiveRecipe differs semantically from entryRecipe; it is not “a control was touched.” Selecting the current filter, returning a slider to its initial value, or undoing all changes leaves the session clean. Store crop coordinates independently of display orientation. Draft writes and output writes must never target source storage.

Use a durable journal/checkpoint for each accepted edit and crop update; coalesce render work rather than dropping draft state. Atomic checkpoint replacement retains the previous valid checkpoint if interrupted. Recovery guarantees apply to durably recorded state; abrupt termination before a write completes can lose the latest unrecorded input. Handle write failure visibly: “Draft couldn’t be saved. Keep this editor open to preserve your changes.” Do not silently promise recovery.

History lasts through the current editing session, including checkpoints and recoverable suspension, without an arbitrary shallow cap. Each completed slider drag, crop application, filter selection or revert is one unit with before/after values. New work after undo clears redo. Applying a crop clears the candidate and records one Crop unit. Cancel Crop drops only the candidate. Save first finalizes the visible candidate as one unit. Undo while a candidate is active drops that candidate first and retains it for Redo Crop; subsequent undo walks history. Show the restored framing immediately. A fresh session starts history from its entry recipe; saved recipe data enables future re-editing but does not imply persistent cross-session undo.

## Screen and exits

The photo preview remains central; filter/crop tools sit below it within reach. Standalone editing has Cancel and Save; the extension uses host-owned Cancel/completion actions. Choosing a tool or changing a value updates preview without dismissing. Comparison with the entry image is a clearly labeled secondary action and does not change history. Preserve preview, selection and crop across portrait/landscape and enlarged-text rearrangements; let secondary tool controls scroll rather than squeezing labels. These are design decisions applying the iOS guidance above, pending device validation.

| Event | Required transition and visible result |
|---|---|
| Open | Capture source identity/revision, load entry recipe, display preview; no asset write or automatic export. |
| Choose filter / adjust crop | Update draft and checkpoint; remain editing and preview the effective recipe. |
| Cancel, clean | Return cancellation once to the host, or close standalone editor; publish nothing. |
| Cancel, dirty | Show confirmation; no writes or return yet. |
| Dismiss editor by a supported Back/close gesture | Use the same clean/dirty cancellation path, never bypass it. Do not claim a host offers gestures it does not support. |
| Save, dirty | Freeze effective recipe and checkpoint; enter preparing. Show “Saving…” and prevent conflicting edits or duplicate Save. |
| Save, clean | Close with an unchanged result according to host contract; no derivative required. |
| Preparation fails | Return to editing with draft intact and actionable inline explanation plus Retry; no success or host return. |
| Preparation succeeds | Validate output, then enter returning. Return success only through the adapter contract below. |
| App loses activity / call / lock | Checkpoint; do not show discard confirmation, publish or cancel. Resume the same editor. |
| Process restarts | Restore matching checkpoint. If source revision changed or is inaccessible, retain draft and explain conflict; require reselect/reload or explicit discard, never apply it silently to another revision. |

Discard confirmation: title **Discard Edits?**; message **Your filter and crop changes from this editing session will be lost.** Use only relevant edit types in that message. Buttons: **Discard Edits** (destructive) and **Cancel** (cancellation, keeps editing with all work). No default action; Return does not discard. Escape/Command-Period where supported cancels the confirmation. Use platform button layout, with cancellation leading in a row or last in a stack. Only one confirmation can be open. Home/app switch preserves the pending decision. This follows [Alerts, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons); the no-default choice uses the guide's qualified advice for deliberate reading.

## Save and extension return contract

```
onSave():
  finalizeVisibleCrop()
  freeze = snapshot(source revision, effectiveRecipe, returnID)
  stage = renderToNewTemporaryFile(freeze)
  verify(stage is decodable, matches frozen revision/recipe,
         has distinct storage identity, source remains unchanged)
  persist derivative + versioned recipe/source association atomically
  if standalone: mark saved, close only after durable success
  if extension: hand off derivative + supported re-edit information
                using hostAdapter.complete(returnID, stagedResult)
```

The host adapter abstracts platform details; no Apple API names or availability are assumed. The host owns its navigation and asset adoption. Do not navigate into the containing app after completion. A successful host return dismisses to the originating Photos context with its selected photo/result. Cancellation returns no edited payload and restores the host's previous state. Keep private staging files alive until the host has accepted/copied them under its documented contract; clean orphaned staging files later.

Require the adapter to define completion/cancellation ownership, result lifetime, failure acknowledgment and idempotency. Only one terminal result per returnID is allowed. Retry after an uncertain handoff must reconcile host status, not publish a second result. If host acknowledgment cannot be established, retain the checkpoint and show a recoverable failure where the host permits; never claim “Saved.” Once accepted, close and remove the session checkpoint. Do not describe undo within the editor as undoing an already accepted external host action.

If interrupted while preparing, retain the frozen job and reconcile/restart staging safely on return. Background completion is attempted only when the runtime permits it; otherwise resume later. If the host terminates the extension, do not invent an automatic reopening ability: recovery requires a valid host session for the same asset/revision and permitted storage. No supported contract means extension readiness is unproven and must be resolved before implementation ships.

## Export and data handling

Standalone Export creates another derivative from the preview recipe; it does not commit edits or dismiss the editor. If the session remains open, Cancel still discards its draft but cannot revoke a separately completed export. Explain that boundary when an export has occurred: “Your exported copy will remain.” Extension save returns to Photos; it is not a public share operation and must not inherit a location-removal claim from standalone export.

| Data | Purpose and access boundary |
|---|---|
| Selected image and embedded metadata | Read only the supplied/selected asset for editing. Request additional library access only when the person invokes a feature that needs it; preserve editing if optional access is denied. |
| Draft, history, preview | Keep private to the session/recovery store; no network transfer required. Explicit discard removes the recoverable session draft, not the source or prior exports. |
| Location metadata in exported copy | Strip from the final supported container and embedded/sidecar representations; independently inspect the serialized output before releasing it. No current-location permission is needed to remove existing metadata. |
| Export derivative | Transfer only on explicit Export; keep source and saved editing recipe separate. |

Export statuses: **Preparing export…**, then **Location metadata removed** only when a supported output inspector reports absence. If already absent, use **No location metadata found in this export**. Unknown/failure: **Couldn’t verify location metadata removal. Export wasn’t shared.** Offer Retry and Cancel Export; retain the editing draft. Unsupported containers must be converted to a supported inspected format with the person's agreement or blocked. The claim covers metadata in those inspected bytes only; it does not promise anonymity, erase visual location clues, change the original, or control metadata a recipient adds later. Removal verification is an implementation prerequisite, not an available local capability.

## Worked before/after

Example fixture: photo A, source bytes S0, identity entry recipe, location tags present.

**Before (brief):** Open A overwrites its original. Select a filter then Cancel: filter commits despite cancellation. Export claims location removal without inspection. A call interrupts an unsaved crop, with no specified recovery.

**After, cancellation branch:** Open A leaves S0 unchanged. Choose Warm, drag crop to 4:3; preview shows both and dirty is true. Switch apps: checkpoint retains Warm and the crop candidate. Resume: same framing and tool. Cancel shows Discard Edits?; Cancel in that confirmation restores editing. Cancel again, then Discard Edits: host receives cancellation once with no derivative; A remains S0.

**After, save/export branch:** Repeat those edits. Save finalizes Crop, renders new file D1, retains S0 plus recipe, and returns D1 to the originating host only after the adapter's successful handoff. In standalone mode, Export stages E1: if inspection still finds GPS tags, it blocks release and shows the verification failure; if stripping and inspection succeed, it releases E1 with the scoped removal message. S0 still contains its original metadata. Undo Crop before Save restores the full frame while keeping Warm; Undo Filter restores entry appearance, making Cancel immediate and prompt-free.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** read the supplied brief, installed root skill, topic-index rows, owning family procedures, selected topic procedures, then their source guides. This document defines immutable originals, clean/dirty cancellation, preview, history, crop recovery, extension return and verified export copy. No web retrieval was performed; official links identify the local snapshot's sources.

**Failed — supplied behavior against this specification:** immediate overwrite, Cancel committing filters, and claiming metadata removal without checking. These are reported brief defects, not independently reproduced failures. Crop recovery is unspecified, so it is unproven rather than a reproduced loss.

**Not executed — implementation acceptance:**

| Check | Pass condition |
|---|---|
| Open/edit/cancel/save | Source bytes and metadata remain identical at every step; successful save has a distinct output identity and preserved recipe. |
| Clean vs dirty | Clean Cancel exits once with no prompt; edit then undo to baseline does likewise; candidate crop prompts; rejecting discard preserves all work. |
| Preview and host chrome | Filter/crop remain previewable; one host top toolbar and recognizable app icon; successful return restores Photos context. |
| History | Grouped drag undoes once; Crop and Filter reverse in order; redo restores; new edit clears redo; no history loss through recoverable interruption. |
| Interruptions | Switch, lock, call and termination retain durably checkpointed candidate/recipe/context; changed source triggers conflict; interrupted save never duplicates output or return. |
| Faults and return | Inject full disk, render failure, invalid output and uncertain host handoff: draft remains recoverable, source is untouched, success is not falsely reported. |
| Export | Test location-present, absent, malformed, unsupported and removal-failure fixtures; inspect the final released bytes, not just the in-memory image. No unknown result can release an export labeled as stripped. |
| Input and layout | Portrait, landscape and enlarged text preserve context and expose actions; supported Back, Escape, Return and repeated Cancel follow the stated contract; no stacked alerts. |
| Device/assistive integration | Confirm touch reach, preview quality, host dismissal, standard undo gestures/shake, focus restoration, readable labels and assistive operation in a supported implementation. |

No device, SDK, GUI, accessibility, rendering, metadata inspection or executable state-machine test was run. The local guides are dated English summaries derived from Apple guidance, not SDK contracts or independent source audits. Actual host API capabilities, storage lifetime, format coverage and re-edit serialization remain implementation validation gates. Live Photos, video and multi-resource assets are outside this still-photo specification; do not silently flatten them or claim their preservation without separately routing and validating that scope.
