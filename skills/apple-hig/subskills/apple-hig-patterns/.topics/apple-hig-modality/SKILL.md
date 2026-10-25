---
name: apple-hig-modality
description: Use when choosing, reviewing, or adapting a modal task, its presentation, dismissal paths, nested flow, or protection of unfinished work.
---

# Resolve modality as a task contract

Read [the modality guide](../../references/modality.md). Use its platform facts as constraints; the decision process below is application advice. A large or fullscreen presentation does not by itself prove modality: establish whether the parent is blocked and what ends that mode.

## Inspect the interruption

Determine create, review, or adaptation mode from the request. Inspect the supplied flows, screens, implementation, or brief for the initiating action, parent context, reason to interrupt, task length, side navigation, and retained work. Identify the platform and whether the task must coexist with another document, window, or reference view. Record what is actually known: a screenshot cannot prove that the background is interactive or that dismissal discards data.

Describe the task in one outcome sentence and identify why normal navigation or an in-context control would be insufficient. If blocking the parent brings no clear decision/focus benefit, revise toward an in-context or nonmodal presentation. Do not preserve modality merely because the current mockup uses a dimmed background.

## Choose presentation and completion together

1. Separate urgent critical information, a scoped related task, an intentional choice, and substantial editing/immersion. Route urgent critical information to alerts, choices to action-sheets/confirmation-dialog guidance, and a short task attached to a parent to sheets or a suitable popover. A fullscreen editor can support substantial work without being modal; document blocking behavior explicitly.
2. Choose a platform-supported candidate and load that topic before prescribing its detailed interaction. A separate window can preserve parallel work on iPadOS, macOS, and visionOS. A popover must not be carried onto an unsupported platform or forced into a compact layout. A sheet's modality itself varies: iOS/iPadOS can support nonmodal sheets; Mac sheets block their parent while other app windows remain usable. For visionOS, distinguish a Shared Space presentation filling a window from Full Space immersion.
3. Keep a modal task narrow enough that the suspended parent remains understandable. If the flow has essential subviews, give it one understandable route and distinguish Back from exiting the task. If it becomes a miniature app with unrelated navigation, split work into ordinary navigation, a separate window, or another appropriate nonmodal workspace instead of adding layers of modal navigation.
4. Specify every available exit against the same data policy: explicit completion, Cancel/Close, interactive dismissal, platform keyboard/remote escape where supported, and any product-defined navigation away. For each exit state whether changes are committed, retained as a draft, discarded after a deliberate decision, or preserved while dismissal is cancelled. Protect created work regardless of whether the exit began with a gesture or a button. Ask about persistence only if the product contract cannot be inferred; otherwise state a reversible assumption and implement it consistently.
5. Name the task and exits so the person can predict the result. Provide a familiar visible exit, using the platform's placement conventions from the selected presentation topic. “Back” changes steps; it must not silently abandon the whole task. Keep relevant guidance close to the work rather than making a title carry instructions.
6. Resolve competing presentations. Dismiss one modal before presenting its replacement and retain only needed context. An alert may appear above modal content for a necessary decision; do not stack alerts. Define which view returns after the alert or replacement so a save/discard decision cannot strand the person or resurrect obsolete content.

Perform the requested action: implement the presentation/exit behavior in the supplied code, create a flow and state specification when designing, or produce a prioritized review grounded in identifiable transitions. Adaptation must revise the presentation and exit contract for the destination platform, not just rename a sheet.

## Deliver and verify

Provide the changed artifact plus a concise transition contract: entry → parent availability → task steps → completion → each dismissal path → resulting data and return destination. In a review, give the observed evidence, consequence, and concrete repair for each issue; list unseen behavior as an inspection question, not a defect.

Exercise or trace a clean exit and an exit after making an edit. Verify that button, gesture, and supported escape paths agree on data protection; Back preserves the task; completion updates the intended parent; reopening does not restore an obsolete transient view; and no second sheet or alert traps the flow. Inspect focus transfer and restoration in code and exercise them when a suitable runtime exists. Fail the design if there is no discoverable exit, unfinished work disappears through one route, a critical decision can be bypassed accidentally, or background blocking contradicts the task contract. Report native input, assistive technology, and Apple-device behavior as unverified when only static or Linux checks were possible.

## Worked transformation

**Before:** A tablet archive app opens “Add Collection” as a sheet. Choosing a cover presents another sheet; a downward swipe from either screen loses the entered title. A top `Back` on the first screen dismisses everything.

**Decision:** Creating a collection is a narrow related task, but cover selection belongs within it. Dismissal and back-navigation need distinct contracts; every dismissal path must protect the edited title.

**After:** Keep one collection sheet with an internal cover-selection step. The first step has `Cancel` and `Done`; the cover step has `Back` returning with its choice. Specify a shared exit handler: clean dismissal closes; edited dismissal offers keep editing or the product's explicit save/discard resolution. Completion creates one collection and returns to the archive. Verify that the swipe and Cancel paths invoke the same protection and that Back never destroys the draft. This proposed flow is application advice, not an observation of an existing app.

## Conditional handoffs

Load sheets, alerts, popovers, action-sheets, panels, or windows only for the selected presentation's detailed rules. Use entering-data or undo-and-redo when persistence/recovery is the real problem; use accessibility when focus boundaries and exit discoverability need deeper treatment. Carry the transition contract into that work.
