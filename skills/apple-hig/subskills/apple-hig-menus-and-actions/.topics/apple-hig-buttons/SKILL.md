---
name: apple-hig-buttons
description: Use when designing, reviewing, or adapting action buttons, including their labels, roles, emphasis, hit regions, and platform behavior.
---

# Operate on buttons

Read [the buttons guide](../../references/buttons.md) before making HIG claims. This procedure is application advice for turning that guide into an artifact; platform facts and dimensions come from the guide. Preserve the user's framework and authorized scope.

## Establish the action contract

Inspect the supplied screen, code, prototype, or brief. Identify the target platform, input methods, surrounding task, and requested mode: create, review, or adapt. For each consequential button, record its visible label or symbol, activation outcome, affected object, reversibility, current role/default status, and actual hit region if available. A screenshot can establish visible styling; it cannot establish hit geometry, keyboard behavior, or accessible names. Mark those as unknown and inspect implementation when available.

Classify the action before styling it. An immediate command fits a button. A persistent on/off setting may need a toggle; choosing one of several persistent options may need a segmented control or picker; a menu-opening control needs the corresponding menu button behavior. Retain a button when its action is to open that choice, but distinguish opening from committing a choice.

## Make and apply the consequential choices

1. Write an outcome-specific short verb phrase, or use a familiar symbol whose meaning survives its context. Give an icon-only control an accessible name that states the action. Do not assume a tooltip replaces the name. On Mac, an ellipsis indicates that another window, view, or app requires further input; add it based on the continuation, not merely because an operation takes time.
2. Assign semantic roles from consequences. Prefer one or two prominent likely actions per view and use style rather than unequal sizes to rank related choices. A primary/default action should normally be the likely nondestructive choice. If destruction is involved, consult the alerts topic before deciding confirmation and Return behavior: the guide explicitly allows a deliberate-destruction alert exception, so “destructive can never be default” is not a universal rule. Cancel abandons the current task; it is not a generic label for completing it.
3. Choose the system control/style when available, retaining its states and accessibility behavior. For a custom control, specify perceivable press feedback and preserve meaningful focus, enabled/disabled, and selected states as applicable. State the reason for a disabled action when the surrounding context does not explain it. This is application advice, not a new Apple requirement to add all states to every button.
4. Check visual and selectable geometry separately. Apply the guide's target and separation rules for the actual platform; a small glyph or small visual style does not establish a small hit region. On visionOS, retain a discernible shape/fill, use standard audible/state feedback, and inspect center spacing and hover overlap. Do not propose unsupported custom hover effects or haptics there. On watchOS, choose inline versus toolbar placement deliberately; preserve common heights for peer controls and use short labels for side-by-side actions. On Mac, distinguish view-body square/image/help buttons from toolbar items; apply the help-button placement/count rules only when designing Help.
5. Only when the command has delayed completion, define the initiating, waiting, and resolved behavior. On iOS/iPadOS, use the activating button's activity indication as described in the guide, preserving context and replacing its image when appropriate. Specify how duplicate activation is handled and what success or failure means in the product; do not promise network completion from a press animation.

Perform the authorized work: implement the controls in the supplied project for a build request; produce an annotated control specification for a design request; or report evidence-backed defects and exact corrections for a review. For adaptation, map each affected control to its destination platform rather than copying appearance alone.

## Deliver and verify

Return the changed artifact or a compact button contract containing label/name, outcome, role/default, style/placement, target region, and relevant state behavior. In review mode attach findings to identifiable controls and separate observed defects from checks requiring execution.

Verify that activation reaches the named outcome; cancellation leaves the intended prior state; keyboard/default activation cannot commit an unintended outcome; focus and accessible names identify the action; and enlarged labels do not clip or overlap adjacent targets. Measure hit regions from layout/runtime data when available. Fail the design if a destructive consequence is mislabeled, peer targets overlap, an icon has no discoverable name, or custom press feedback is absent. State separately which checks were inspected in source, exercised, or remain Apple-device checks; Linux inspection does not prove gaze, VoiceOver, haptics, or native rendering.

## Worked transformation

**Before:** A Mac photo organizer has equally prominent `Go`, `Remove`, and `Close` buttons. `Go` opens export settings; `Remove` deletes a selection with undo; `Close` finishes editing metadata.

**Decision:** The labels hide three different contracts. Export requires further input; routine reversible removal does not by itself justify a confirmation alert; finishing edits should name completion. The export task, rather than removal, is the likely action on this screen.

**After:** Specify `Export…` as the prominent action opening export settings, `Remove Photos` as a lower-emphasis command with a visible Undo path, and `Done` for finishing metadata edits. Inspect actual save semantics before changing `Close` to `Done`. Verify the Return mapping, undo restoration, and that each accessible name matches the resulting action. These product choices are an example application, not facts about the unseen implementation.

## Conditional handoffs

Load alerts for consequential confirmation/default decisions; toggles or segmented-controls for persistent selection; pop-up-buttons or pull-down-buttons for menu-opening behavior; toolbars when placement belongs to window chrome; and accessibility when naming, focus, contrast, or target access needs deeper work. Keep this button contract as the input to the next topic.
