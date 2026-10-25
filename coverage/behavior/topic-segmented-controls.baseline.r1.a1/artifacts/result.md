# iPhone account control audit

## Scope and decisions

Reviewed `interface.md`, which supplies a textual description rather than executable UI or a screenshot. “Verified” below means explicitly stated in that file; it does not mean independently reproduced. Priority reflects potential harm and task blockage, not measured frequency.

Replace the nine-action segmented control with separately labeled account actions. Retain a segmented control only if product requirements identify a small set of closely related subviews. The actual action inventory and subview names are missing, so the illustrative names below are not a proposed final information architecture.

## Ranked verified findings

| Rank | Supplied observation and effect | Source-backed decision and correction |
|---|---|---|
| 1 — Critical | Selecting Delete Account destroys data immediately. A view-selection gesture can cause irreversible loss. | Remove deletion from the segments. Give it a discoverable account action that opens an explicit consequence review and confirmation with Cancel before any deletion request. HIG distinguishes uncommon irreversible destruction from ordinary undoable deletion. [Alerts: Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices); [Managing accounts: Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts). |
| 2 — High | Keyboard/assistive users hear no selected state. They cannot reliably determine the active view. | Expose each choice’s full name, role, and selected state; make selection and activation keyboard-accessible, and publish state changes through the platform’s semantic accessibility mechanism. Exact spoken wording is implementation-dependent. [Accessibility: Vision, Mobility, Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 3 — High | Two segments remain selected for a single-view choice. The control gives contradictory feedback about the displayed view. | Store one selected view identifier and derive both visible selection and accessibility state from it. Exactly one choice is selected and its corresponding view is displayed. Multiple simultaneous choices are described for macOS, not this iPhone single-view task. [Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls). |
| 4 — High | Long labels truncate to identical prefixes. People cannot distinguish destinations reliably before activating them. | Use short, distinct title-case nouns or noun phrases for related view choices, with full accessible names. If labels cannot fit legibly at supported text sizes and widths, replace the horizontal control with a layout that shows complete labels. [Segmented controls: Content](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Content); [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 — Medium | Nine unrelated actions share the segmented control. Their relationship and interaction model are unclear, and the count compounds crowding. | Separate unrelated actions; segments on iOS switch closely related subviews. The source advises no more than about five segments on iPhone, not an absolute five-item validity rule. Do not merely split the nine unrelated actions into smaller segmented groups. [Segmented controls: Best practices and iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Best-practices). |

## Corrected behavior specification

The following is framework-agnostic. No Apple SDK types are required. Semantic roles must be mapped to the chosen runtime rather than copied as API names.

```text
Account page:
  relatedViews = product-approved closely related subviews, if any
  selectedView = one valid view ID
  accountActions = separately labeled actions outside view selection
  Delete Account = discoverable separate action

renderViewChoices():
  for each view:
    show short, distinct visible label
    expose full accessible name and appropriate selection-control role
    visibleSelected = (view.id == selectedView)
    accessibleSelected = visibleSelected
  show only the content belonging to selectedView
  if choices cannot fit with readable, distinguishable labels:
    use an alternative choice layout with full labels

activateView(id):
  require id in relatedViews
  atomically update selectedView, selected semantics, and visible content
  retain logical focus on activated choice
  never execute an account action

keyboardAndAssistiveInput:
  allow traversal and activation of every choice and action
  show keyboard focus separately from selection
  use the same activation handler for all input methods
  moving focus alone does not delete data or execute actions

activateDeleteAccount():
  open confirmation with title "Delete Account?"
  explain the actual data loss, reversibility, and completion time
  offer "Cancel" and "Delete Account"; use no default action
  move focus into confirmation and keep background controls inactive
  do not send a deletion request yet

cancelConfirmation():
  close confirmation; restore focus to Delete Account
  preserve account data and selectedView

confirmDeletion():
  require explicit activation of "Delete Account" in confirmation
  send one deletion request; prevent duplicate submissions
  expose pending status without claiming completion
  on failure: explain failure and offer recovery without claiming deletion
  on success: notify completion and leave the deleted account context
```

Choosing no default in the confirmation is a design decision supported as an option by the Alerts guidance; Cancel remains available and is not made the default. Support familiar cancellation, including Escape on an attached keyboard. In Assistive Access, the supplied accessibility guide requires two confirmations for difficult-to-reverse actions; add a second explicit confirmation in that mode before submitting deletion. [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons); [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

Keep deletion straightforward and discoverable. Disclose actual retention and completion timing; if Apple auto-renewable subscriptions apply, explain that account deletion does not cancel them and provide management instructions. These are implementation requirements to resolve, not observed omissions. [Managing accounts: Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts).

## Worked before/after

**Before, from the supplied description:** a person encounters nine long unrelated segments whose labels share truncated prefixes. Two appear selected even though only one view is intended. Assistive output omits selection state. Choosing Delete Account immediately destroys data.

**After, illustrative:** suppose the product confirms that Profile and Security are related account subviews. Profile starts selected, Security unselected, and Profile content is shown. Activating Security atomically makes Security the sole selected choice and displays Security content. Its semantics expose “Security” and selected state; the precise announcement is left to the runtime. Other account actions sit outside this group with complete labels.

The person activates the separate Delete Account action. The confirmation describes the actual loss and offers Cancel and Delete Account. No deletion request occurs. Cancel restores focus to the originating action and keeps Security selected. Reopening and explicitly confirming sends one request, exposes progress, and reports the actual outcome. Profile/Security are examples only; do not invent them if the supplied actions do not imply related views.

## Acceptance checks

These are proposed checks, not executed results.

1. Inventory all nine actions. Each has a distinct, complete label and a destination or action outside the view selector unless it is genuinely a related subview. Keep any iPhone segment group small, using the source’s “about five” guidance with fit testing.
2. For each retained view choice, activate it by touch-equivalent input, keyboard, and assistive activation. Assert one selected ID, one visible selected choice, one accessible selected choice, and matching content. Repeated activation remains consistent.
3. Traverse without activation. Focus is visible and distinguishable from selection; focus movement executes no account action. Inspect semantic name, role, and state and then verify actual spoken feedback with VoiceOver and navigation with Full Keyboard Access and Switch Control on a supported runtime.
4. At supported iPhone widths, long localized labels, and text enlargement of at least 200%, choices remain distinguishable and usable. Switch layouts if needed; do not solve identical prefixes by only adding hidden names. Check light/dark and non-color selection cues. These are adaptation checks, not verified current defects. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).
5. Activate Delete Account, cancel, and dismiss by supported cancellation input. Assert zero deletion requests and unchanged account data. Verify modal focus containment and return focus. Confirm explicitly and assert one request even after repeated activation; test pending, failure, and success states.
6. In Assistive Access, require two confirmations before submission. Verify real consequence copy, completion time, and applicable subscription/retention disclosures against product behavior.

## Evidence limits and reading trail

Only `interface.md` establishes the observed interface facts. No screenshot, code, action names beyond Delete Account, dimensions, colors, focus implementation, backend contract, or localization samples were supplied. Touch target size, contrast, actual keyboard operation beyond the stated missing state feedback, and device behavior cannot be judged. No device, simulator, SDK, GUI, accessibility service, or backend execution occurred. No web browsing occurred; official links above identify the sources referenced by the installed local guides, not newly verified web content.

Read the installed package root `.agents/skills/apple-hig/SKILL.md`, then the Selection and input family procedure, then searched `references/topic-index.md` for the exact component before reading `subskills/apple-hig-selection-and-input/references/segmented-controls.md`. Also read the Patterns, Foundations, and Presentation family procedures before their respective `managing-accounts.md`, `accessibility.md`, and `alerts.md` source guides. Each file was read in its own command. Paths resolve beneath the installed `.agents/skills/apple-hig/` package. No additional topic procedure was routed by those family instructions. The local guides identify a 2026-10-25 snapshot/retrieval date; they are derived guidance, not SDK documentation or evidence of independent review.
