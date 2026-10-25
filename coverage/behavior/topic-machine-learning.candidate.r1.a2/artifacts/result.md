# Receipt categorization: revised interaction specification

## Scope and decisions

The supplied `interface.md` targets iOS/macOS and reports three behaviors: every guess is labeled “Certain,” receipts move irreversibly, and correction consequences are unexplained. Low-quality photos and unfamiliar vendors are common. No accuracy study, implementation, screenshots, data-flow documentation, or category inventory was supplied.

This is a framework-agnostic design contract, not an implemented or tested Apple interface. Specific state names, copy, persistence rules, and release gates below are product decisions informed by the locally installed HIG snapshot. They are not universal Apple requirements.

1. **Replace certainty with provenance and review state.** Display “Suggested category: …” and “Needs review,” never “Certain,” a confidence percentage, or “High confidence.” “Confirmed by you” means an explicit saved choice, not model correctness. Until representative validation exists, every model suggestion requires review; no automatic filing. Apple advises validating confidence against actual quality before exposing or ranking by it. [Machine learning — Confidence](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Confidence)
2. **Make categorization reversible metadata.** Keep an immutable receipt ID and original image. Category views query metadata; categorizing never moves/deletes the original file or triggers export, payment, reimbursement, or tax submission. Save and recovery operate on the same receipt. [Machine learning — Mistakes and Corrections](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Mistakes)
3. **Explain correction scope before saving.** Always show: “This changes only this receipt’s category. It won’t change other receipts or train the model.” This is a required behavior of the proposed system, not an assertion about the existing backend. Disable training use of these correction events; verify that data path before shipping this copy. No implicit merchant rule, bulk retroactive update, or training opt-in is introduced.
4. **Offer useful fallbacks without compulsory calibration.** Manual categorization works when classification is unavailable. “Leave for later” keeps the receipt in Needs review. “Replace photo” is optional; show the new image before committing replacement and retain the prior image revision. No introductory vendor questionnaire or mandatory retake. [Machine learning — Calibration and Limitations](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Limitations)

### Role and consequences

| Dimension | Design classification and consequence |
|---|---|
| Critical/complementary | Automation is complementary; storing, inspecting, and manually categorizing receipts remain usable without it. Financial record integrity is critical. |
| Private/public | Treat images, vendors, amounts, and choices as private financial content; no receipt details in public notifications. |
| Proactive/reactive | Import is intentional, but the resulting unsolicited category is proactive assistance; keep it provisional. |
| Visible/invisible | Show the proposed category and review status; never silently relocate content. |
| Dynamic/static | Update cadence is unknown. Treat predictions as versioned snapshots; make no live-learning promise. Model updates must not overwrite saved human choices. |

These dimensions follow [Machine learning — The role of machine learning in your app](https://developer.apple.com/design/human-interface-guidelines/machine-learning#The-role-of-machine-learning-in-your-app).

## Concrete interaction

Receipt detail keeps the image, extracted merchant/date/amount (each allowed to be missing), category, and status together. Display “Check the category before using it in reports. Blurry photos and unfamiliar vendors can cause mistakes.” beside an unreviewed suggestion. Reports exclude unreviewed receipts by default and show their excluded count with a route to review them; never silently treat a suggestion as an approved category.

The category area contains:

- `Suggested category: Dining` plus `Needs review`, or `No category suggested`.
- `Use Dining` when there is a valid suggestion, `Change category` (or `Choose category`), and `Leave for later`.
- A brief factual rationale only when backed by inspectable evidence, such as `Receipt text includes “restaurant”` with the actual recognized snippet alongside the image. Label recognized text as potentially incorrect. Without evidence, say `Automatically suggested from this receipt; the reason is unavailable.` Never invent a vendor history or causal model explanation.

A low-quality-photo warning may say `Some receipt text could not be read` only if a documented detector/OCR result supports it. Otherwise use the general limitation copy above. A “new vendor” label requires an actual scoped vendor-history lookup; absence of model evidence is not proof of an unfamiliar vendor. [Machine learning — Attribution](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Attribution)

`Change category` expands a single-choice editor next to the category value. Assumption: the product supplies a finite, medium-sized category taxonomy. Show its active categories in localized alphabetical order, using stable category IDs for storage; do not rank choices by unvalidated scores. Include `Uncategorized` as a deliberate choice. Mark the existing saved value as selected; when none exists, no selection is required by default. Selecting a value edits a draft; `Save category` commits, and `Cancel` restores the prior state. A removed category remains visible as `Unavailable category` and requires a new choice rather than silently substituting another. If the real taxonomy is very large, this editor needs a separately specified searchable chooser before implementation. [Pickers — Best practices](https://developer.apple.com/design/human-interface-guidelines/pickers#Best-practices)

Successful correction reads `Saved as Travel. This receipt only.` The detail remains open and offers `Change category` again. Selecting Uncategorized is confirmed as a human choice and is distinct from leaving the receipt unreviewed. No like/dislike prompt follows. Viewing a receipt, dismissing the editor, or leaving for later is not approval. [Machine learning — Explicit feedback and Corrections](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Explicit-feedback)

## State and persistence contract

Keep processing status separate from review status:

```text
receipt = {
  id, originalImageRef, imageRevision,
  suggestion: {categoryId?, modelVersion?, evidence?},
  savedCategoryId?, review: NEEDS_REVIEW | CONFIRMED,
  revision
}
editor = {receiptId, baseRevision, draftCategoryId?, saveState}

onModelResult(id, imageRevision, result):
  ignore if imageRevision is stale
  store suggestion snapshot; never mutate saved category or confirmation

onUseSuggestion():
  commitCategory(suggestion.categoryId)  // explicit human acceptance

onSaveCategory():
  validate active category ID or explicit Uncategorized
  commitCategory(draftCategoryId)

commitCategory(category):
  persist atomically using receipt ID, base revision, idempotency key
  write category + CONFIRMED; record prior category and review state
  acknowledge success only after durable persistence
  update all views by receipt ID; leave original image unchanged

onCancel(): discard draft; no receipt mutation
onLeaveForLater(): preserve NEEDS_REVIEW; return to prior position
```

While a save is pending, keep the draft visible with `Saving category…`; prevent duplicate submission but allow navigation without losing the pending receipt identity. Do not show Saved based on a button press. On rejection or unavailable storage, retain the draft and show `Category wasn’t saved. Retry or cancel.` with those actions. On an ambiguous timeout, reconcile the idempotency key before retrying; do not create duplicate history entries. On a revision conflict, show the current saved value alongside the draft and require explicit reapplication; never overwrite silently. Preserve editor state and reconcile pending work after interruption/relaunch. Routine feedback stays near the category, without sound-only status or repeated alerts. [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices)

Each successful category change is one undo unit, including its confirmation state. Undo restores both previous category and review state through a durable inverse transaction; Redo reapplies them. A failed save adds no history. A new edit after Undo clears Redo. Keep meaningful history through the open review session, including autosaves; closing/reopening starts a new session history, while `Change category` remains available indefinitely. No disappearing banner is the only recovery path. Undo of an offscreen change reveals the affected receipt and its restored category. Concurrent changes require reconciliation, not blind reversal. Undo never claims to reverse an external submission.

On macOS use `Edit > Undo Category Change` / `Redo Category Change` with Command-Z / Shift-Command-Z. On iOS support standard undo interactions where the implementation permits and retain a visible `Undo category change` action so recovery never depends on a gesture. System-provided Undo/Redo titles receive only the operation wording. These are integration requirements to verify in the eventual stack, not assumptions that an SDK is installed. [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)

## Platform and access behavior

On iOS, use receipt detail with the editor inline near the category; keep frequent actions reachable and preserve Back. On macOS, use a resizable receipt list/detail workspace with the same selected receipt as the command target. Switching apps, rotating, resizing, or enlarging text preserves selection and drafts; narrow layouts stack content rather than hiding Save/Cancel. Provide a complete keyboard path through category selection, save, cancel, and recovery. [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices)

Status uses text rather than color alone. Controls expose names, roles, selected values, and saving/error states in task order: receipt identity, suggestion/status, rationale, category actions, editor, outcome/recovery. Return focus to the category action on cancellation; retain it near the saved value after success. Save/error status must be available to assistive technology without forcing focus away. Preserve all content/actions at 200% text enlargement. Start from activation areas of 44 × 44 pt on iOS and 28 × 28 pt on macOS; verify separation and actual geometry in implementation. These are the local guide’s platform defaults, not measured results. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)

## Data-purpose boundary

| Data | Permitted purpose in this design | Excluded behavior |
|---|---|---|
| Receipt image and recognized text | Display and categorize the selected receipt | Unannounced secondary sharing or training |
| Saved category and history | Consistent views, correction, and recovery | Inferring approval from viewing/dismissal |
| Correction event | Persist this receipt’s metadata | Automatic vendor rules or model retraining |

Processing location, storage protection, sync, retention, and current permissions are unknown. Prefer avoiding unnecessary transfers; the implementer must document actual processing and required access before release. Manual correction requires no new camera permission. Request camera access only when Capture/Replace photo is invoked, with import/manual categorization still available if denied. No collection for optional model improvement is part of this design. [Privacy — Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission)

## Worked before/after

Illustrative fixture, not an observed receipt: a blurred receipt from unfamiliar vendor “North Quay,” amount 48.20; model guesses Dining, but the purchaser knows it was a train ticket.

**Before (supplied behavior applied to fixture):** `Dining — Certain`; the receipt moves irreversibly. The interface gives no account of correction scope.

**After:** Receipt stays in Needs review. Detail shows `Suggested category: Dining`, the general limitation copy, and the image. No numerical confidence or invented rationale appears. The purchaser opens Change category, selects Travel, reads the this-receipt-only explanation, then saves. Durable acknowledgement changes the row and detail to `Travel · Confirmed by you`, with `Saved as Travel. This receipt only.` The original image and other North Quay receipts remain unchanged. Undo restores the previous unset saved category and Needs review status; Redo restores Travel and confirmation. Reopening retains Travel. A later model guess cannot overwrite it. The correction improves this record immediately; it does not claim to improve future predictions.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** the contract removes unsupported certainty; distinguishes provenance from correctness; provides manual fallback, explicit correction scope, persistent editable choices, truthful save outcomes, and a defined inverse. The worked scenario traces acceptance, correction, undo, redo, and reopening. Installed root, selected families, topic procedures, and supporting guides were read in route order, one file per command; the topic index was searched. Official links above identify source sections; no web access was used.

**Failed — supplied behavior against the revised contract:** blanket “Certain” has no supplied validation; irreversible movement prevents recovery; correction consequences are unexplained. These are findings from the brief, not runtime observations.

**Not executed — required implementation checks:**

| Scenario | Acceptance condition |
|---|---|
| Unknown vendor, blurred photo, absent evidence | Needs review; no unsupported certainty/rationale; manual choice works without retake. |
| Choose, cancel, confirm, reopen, correct again | Cancel mutates nothing; successful choices persist consistently by receipt ID across views and reopen. |
| Delayed/rejected save, offline storage, duplicate retry | No false Saved state, no duplicate command, draft retained; retry reconciles outcome. |
| Concurrent edit or stale model/image result | No silent overwrite of human choice or newer image state. |
| Multiple changes, undo/redo, new edit after undo | Correct receipt/category/review restored visibly; Redo cleared by new edit; failed writes absent from history. |
| Background/relaunch, rotation, resizing, enlarged text | Selection/draft recovered; essential actions remain reachable. |
| Keyboard, VoiceOver, Switch Control, Full Keyboard Access | Complete review/correction/recovery path; meaningful names/order/status; no gesture-only action. |
| Light/dark appearance and activation geometry | Measure actual contrast, reflow, activation areas, and spacing; no status depends on color or sound. |
| Permissions and data use | Manual flow works without camera; correction events do not enter training or leak across accounts. |

No device, GUI, accessibility, SDK, persistence, security, or model execution occurred. Local HIG articles are dated derived guidance, not SDK references or proof of independent source review. No confidence threshold, accuracy rate, vendor detector quality, or learning cadence can be justified from the supplied evidence.

Before considering confidence bands or automatic filing, evaluate labeled receipts representative of blurred/clear images, familiar/unfamiliar vendors, category imbalance, and intended users. Measure category errors and their financial consequences, abstention/review coverage, correction burden, and calibration across score ranges and model versions. Set acceptance targets with product owners before measuring; do not invent a numerical gate now. Reevaluate per-category regressions after updates. If corrections cost more effort than manual entry, improve or withdraw the suggestions rather than demanding endless fixing. The current release contract remains review-first until that evidence supports a separately approved change.
