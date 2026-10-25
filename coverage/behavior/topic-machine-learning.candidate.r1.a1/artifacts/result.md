# Receipt categorization: revised interaction specification

## Scope and decisions

Target: iOS and macOS; framework-agnostic behavior. This is a design specification, not an implemented interface. `interface.md` supplies only a short description: every guess is labeled “Certain,” receipts move irreversibly, corrections have no explained consequence, and poor photos/unfamiliar vendors are common. There is no accuracy study, UI specimen, persistence implementation, or data-flow description.

1. Replace “Certain” with **“Suggested category: {category}”** and **“Needs review.”** These describe provenance and workflow, not measured confidence. Do not expose percentages, confidence tiers, or confidence-based ordering without validation. All new suggestions require review in this version. This conservative release decision applies [HIG Confidence](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Confidence); Apple does not prescribe this exact release policy.
2. Store categorization as reversible metadata on a stable receipt ID. Keep the original image and its storage location unchanged. Category views are filters, not physical file moves. No automatic export, accounting posting, deletion, or external move occurs. Apply [Mistakes](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Mistakes) and [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices).
3. Treat a correction as an instruction about this receipt. Persist it immediately after successful save and permit correction again. Do not equate opening a receipt with approval. Do not claim “the model learned” or apply a merchant-wide rule. Apply [Corrections](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Corrections) and [Explicit feedback](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Explicit-feedback).
4. No calibration questionnaire is required. Manual categorization remains available when recognition fails or automation is unavailable. Do not make people repeatedly fix the same receipt after model updates. Apply [Calibration](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Calibration) and [Limitations](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Limitations).

Feature classification: categorization is a core workflow; prediction is complementary because manual assignment works without it. Receipt data is private and potentially sensitive. Suggestions are proactive after import, visible, and never silently committed. Model update cadence is unknown: design for versioned offline updates without promising live learning. Category mistakes can distort reports, so only user-confirmed assignments contribute to categorized totals; pending receipts remain visible with an explicit excluded count. These are product decisions informed by [ML role dimensions](https://developer.apple.com/design/human-interface-guidelines/machine-learning#The-role-of-machine-learning-in-your-app).

## Screens and command contract

**Receipt review:** show image access, merchant text (or “Merchant not recognized”), amount/date when available, current saved category, review state, suggested category if present, and limitations before the decision controls. Keep pending and saved categories visually and semantically distinct.

Persistent copy above the first pending decision: “Categories are suggestions. Check them before using your reports. Photos that are hard to read and unfamiliar vendors can lead to mistakes.” Keep a concise reminder on subsequent pending receipts: “Review before including in reports.”

Rationale is optional and factual: show “Detected text: ‘{excerpt}’” only if that excerpt exists in extraction evidence; label it as extracted text, not a proven reason the classifier chose a category. Show “Photo may be hard to read” only if an actual input-quality signal exists. Otherwise use “No explanation is available for this suggestion.” Never invent vendor familiarity, purchase purpose, or causal explanations. This applies [Attribution](https://developer.apple.com/design/human-interface-guidelines/machine-learning#Attribution).

| Command | Outcome and scope | Role / availability |
|---|---|---|
| Use {category} | Save displayed suggestion for this receipt; mark reviewed | Primary when a suggestion exists; explicit activation only |
| Choose Category (Mac: Choose Category…) | Open category-selection view, preserving current receipt | Secondary; always available except during its save |
| Keep Uncategorized | Mark intentionally uncategorized; remove from review queue but exclude from categorized totals | Secondary; no model feedback |
| Review Later | Return to queue with pending status unchanged | Secondary; no data mutation |
| Retry Categorization | Request another suggestion without changing a saved category | Secondary on failure; optional, never required |
| Undo Category Change / Redo Category Change | Reverse/reapply latest committed category transaction | Available only when history permits |

Use outcome labels, visible focus and press feedback; one prominent action per view. A Return key must not silently accept a suggestion merely because a receipt opened; activate a focused control deliberately. iOS button save activity stays within the activating button; disable duplicate commits while saving. See [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) and [iOS delayed completion](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

**Category selection:** a full view containing labeled command rows “Set to {category},” in stable alphabetical order, plus “Set to Uncategorized” and “Cancel.” Current category has a text annotation “Current.” Rows are immediate command buttons, not a staged selection requiring a second Save. No confidence ranking, inferred alternatives, or new category-creation subsystem is required. Show before selection: “Changes this receipt’s category in your reports. It won’t change other receipts or train the model.” Cancel/back returns without changing data. On save failure retain this view and chosen value for Retry.

**After commit:** keep the receipt detail visible even if its category filter no longer matches. Show “Saved to {category}. Only this receipt changed.” Include a persistent Undo action until dismissed or superseded; history remains available after dismissal. Returning to the queue shows the updated category and count. Reopening exposes Choose Category again. Do not use a disappearing toast as the sole recovery route.

## State and persistence contract

```text
Receipt = { id, originalImageRef, revision,
            category: categoryID | null,
            review: pending | confirmed | intentionallyUncategorized,
            assignmentSource: none | user,
            suggestion: {categoryID, modelVersion, inputVersion} | null,
            predictionState: pending | ready | unavailable,
            lastCommandID }

onImport: create stable receipt; review=pending; category=null
onPrediction(result):
  attach suggestion only if inputVersion still matches
  never replace user assignment or reset review
onUseSuggestion / onSetCategory / onKeepUncategorized:
  commit(expectedRevision, uniqueCommandID, nextCategory, nextReview)
  atomically persist receipt + inverse history entry
  success -> update every category view/report from saved receipt
  failure -> keep prior saved assignment; retain draft; show Retry and Cancel
```

A null category can mean pending or intentionally uncategorized; never infer review state from category alone. Prediction unavailable copy: “Couldn’t suggest a category. Choose one yourself or try again.” No empty result blocks manual work. On app restart, restore saved state; resume an interrupted prediction or mark unavailable. An uncertain save outcome must be reconciled by command ID before retry, preventing duplicate history entries. Revision conflict: reload current state, explain “This receipt changed elsewhere,” preserve the attempted choice separately, and require a fresh explicit commit.

Each committed category/review change is one undo unit with before/after snapshots; opening a view, selecting text, or receiving a prediction creates none. Undo restores category, review state, source, and report membership; redo reapplies them. New committed edits after undo discard the redo branch. Persist history across receipt navigation and restart for retained receipts; do not clear it on autosave. Reveal the affected receipt and its restored state when undo targets an offscreen item. Conflicting newer revisions require reconciliation rather than overwriting them. Original images remain unchanged. Undo cannot reverse external actions, which this flow does not initiate. On Mac expose Undo/Redo at the top of Edit with Command-Z / Shift-Command-Z. On iOS preserve standard undo gestures where supported and retain the visible action; no gesture is essential. See [platform-specific undo guidance](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Platform-considerations).

## Data-purpose boundary

This is a proposed minimum contract, not a claim about the existing backend. Apply [Privacy best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

| Data | Purpose / boundary |
|---|---|
| Supplied receipt image and extracted text | Prediction and review; account-private; prefer processing without unnecessary transfer. Actual processing location must be established before shipping explanatory copy. |
| Category, review state, version, command history | Persist assignments and recovery within the same receipt/account boundary. Delete associated history when the receipt is permanently deleted. |
| Corrections | Functional edits only; no new training or analytics upload in this design. No implicit approval from viewing, retrying, or sharing. |

Do not introduce training collection under the correction button. Future voluntary model feedback requires a separately specified purpose, payload, retention and access controls. No new camera/library access is needed for review of already supplied images; permission flows for capture/import are outside this brief. Do not gate manual categorization on optional collection.

## Worked before / after

Illustrative fixture, not an observed receipt: an unfamiliar vendor “North Pier” has a blurry restaurant receipt; the classifier returns “Travel.”

**Before, from the brief's behavior:** “Travel — Certain”; the receipt moves irreversibly. A category correction has no explained effect. The fixture does not establish why the model erred.

**After:** receipt remains in Needs Review, with “Suggested category: Travel.” No “blurry” diagnosis appears unless input-quality evidence supports it. The person opens Choose Category, reads the scope explanation, and activates “Set to Meals.” Successful persistence shows “Saved to Meals. Only this receipt changed.” Reports now include it under Meals. Undo restores pending/uncategorized state and removes it from categorized totals, while preserving the suggestion for inspection. Redo restores Meals. Reopening and choosing Supplies saves a new correction; a later classifier result cannot replace it. If saving fails, the receipt remains pending and Retry retains the Meals choice. There is no promise that future North Pier receipts will improve.

## Acceptance checks and evidence limits

**Passed — document inspection only:** the supplied brief was read; installed root, selected families, topic procedures and supporting local guides were read in order; topic-index searches covered ML, privacy, accessibility, buttons and undo. This specification defines confidence policy, correction scope, failure recovery, inverse operations and a worked trace. Official links identify source sections; no web access was used.

**Failed — supplied behavior against this contract:** “Certain” lacks validation evidence; irreversible movement prevents recovery; missing correction explanation leaves scope unclear. These are findings from the supplied description, not observed runtime failures.

**Not executed — required implementation acceptance:**

| Test | Pass condition |
|---|---|
| Confidence and evidence | Every unreviewed prediction says Suggested/Needs review; no unvalidated certainty, confidence sorting or fabricated rationale. Missing quality signals cause no invented diagnosis. |
| Manual fallback | With prediction offline/failed, complete Choose Category or Keep Uncategorized without calibration or training consent. Review Later preserves pending state. |
| Persistence | Correct, navigate away, restart, then deliver a late prediction: saved category/review survives; all views and reports agree. |
| Save fault injection | Reject save or interrupt acknowledgment; no false Saved state, no duplicate command/history, retained draft and working retry/cancel. |
| History sequence | Confirm A, correct B, undo twice, redo twice; correct objects and report membership return. New edit clears redo; offscreen undo reveals target; restart retains history. |
| Scope and privacy | One correction changes one receipt only; no training/analytics request or unrelated permission occurs. Verify actual network/storage behavior before claiming this boundary. |
| Keyboard and assistive input | Complete review, correction, retry and undo without pointer, speech or required gesture. Focus order follows content then actions; each command exposes name, button role and availability; status is perceivable without sound/color. Verify on supported Apple environments. |
| Layout and perception | At 200% text sizing essential copy/actions remain available. Measure light/dark contrast and focus visibility. Specify 44×44 pt activation regions for these buttons on both platforms as a conservative product choice: Buttons gives general 44 pt guidance while Accessibility lists macOS default 28 pt/minimum 20 pt. Do not reinterpret those Mac figures as an Apple 44 pt mandate. |

Accessibility decisions apply [Vision, Mobility and Cognitive guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility). Actual geometry, contrast, text resizing, VoiceOver, Switch Control, Full Keyboard Access, native gestures, device comfort, SDK compilation and GUI execution have not been tested. No SDK is assumed.

Before any confidence tier or automatic commitment is proposed, run representative labeled evaluation across poor photos, unfamiliar vendors and categories, comparing held-out quality, confidence calibration, error costs and review effort for each model version. Define justified release thresholds from those results rather than inventing them here. Observe correction completion time, repeat-error rate and abandonment in usability evaluation; if correction costs exceed assistance value, reduce/suppress suggestions and retain manual mode. No dataset, accuracy, calibration, security audit or user study is supplied, so none is claimed. Local guidance is a dated snapshot, not verification of current SDK capability or live Apple documentation.
