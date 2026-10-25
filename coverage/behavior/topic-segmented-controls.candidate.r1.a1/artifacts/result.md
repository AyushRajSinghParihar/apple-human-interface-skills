# iPhone account-page control audit

## Scope and evidence

Reviewed `interface.md`, a behavioral description, against the installed apple-hig package. “Verified” below means explicitly stated in that supplied description, not reproduced in an application. No screenshot, dimensions, implementation, actual accessibility tree, full action inventory, or backend contract was supplied. This is a framework-agnostic correction specification, not an implemented interface.

## Ranked verified findings

Priority is this review's assessment of consequence, not an Apple severity scale.

| Rank | Observed evidence and effect | Decision and source |
| --- | --- | --- |
| 1 — Critical | Selecting Delete Account immediately destroys data. A view-choice interaction can cause irreversible loss without a deliberate confirmation boundary. | Remove deletion from the segmented control. A separate Delete Account button opens a consequential confirmation; only explicit confirmation may request deletion. Uncommon irreversible destruction warrants confirmation; this is not a rule to confirm every routine, undoable deletion. [Alerts: Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices), [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 2 — High | Two segments remain selected for a single-view choice. The control contradicts the displayed-view contract. | Represent the choice with one selected identifier, not independent booleans. Selection and visible content change together; activating the selected choice is a no-op. macOS multiple-selection support does not justify this iPhone single-view behavior. [Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls). |
| 3 — High | Keyboard/assistive users receive no selected-state feedback. They cannot reliably determine the current view. | Expose each choice's unique name, selection-control role, selected state, group relationship, and affected content. Synchronize semantic and visual state; make navigation and activation available through supported keyboard and assistive input. [Accessibility: Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [VoiceOver: Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Descriptions). This evidence does not establish that controls are unreachable. |
| 4 — High | Labels truncate to identical prefixes, hiding which outcome activation will produce. | Use distinct concise labels; show complete action names on vertically arranged buttons when needed. Do not rely on tooltips or accessible names to repair indistinguishable visible labels. [Segmented controls: Content](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Content), [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 — Medium | Nine long unrelated actions occupy one segmented control. The grouping implies a shared choice model and exceeds practical iPhone capacity. | Separate commands from persistent view choice. Use segments only for a small set of closely related local views; retain every existing command as an individually named action outside that group. The guide says no more than **about five** segments on iPhone, not an absolute numeric validation rule. Nine unrelated commands remain unsuitable even if they fit. [Segmented controls: Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Best-practices). |

## Corrected contract and decisions

Inventory all nine existing entries before implementation: identifier, complete label, command versus view choice, effect, affected data, reversibility, and availability. Only Delete Account is named in the evidence. No claim is made that the other eight have been individually classified. Preserve their functionality; do not silently remove them to reduce the segment count.

Use a vertically arranged set of separately labeled action buttons for unrelated commands. Keep Delete Account discoverable on the account page, visually separated from ordinary commands, with destructive meaning conveyed by wording as well as styling. Provide press and focus feedback. Use at least 44 × 44 pt activation regions with nonoverlapping separation as the design target. The local Buttons guide recommends that general target; the Accessibility guide separately lists a 44 × 44 pt iOS default and a 28 × 28 pt minimum. Use the conservative 44 pt target here; no measured size violation is established. [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

Retain a segmented control only if inventory establishes two or more closely related local views. Every segment then has the same single-choice behavior, text-only short noun labels, comparable content footprints, and one selected view. Do not invent top-level destinations or compress unrelated actions into five segments. If no related views exist, remove the segmented control entirely. If labels cannot remain distinguishable at the available width or enlarged text, use a vertically arranged single-choice presentation with the same state contract instead of shrinking or clipping essential text. Preserve at least 200% text enlargement. [Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls), [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Semantic order: Account page title → view-choice group, if present → current view heading/content → ordinary commands → Delete Account. Use actual locale reading order. Each choice exposes its complete visible name, selected=true/false, and relation to the current content. Keep focus on the activated choice after a view change; publish the content/state change through the implementation's accessibility mechanism without redundant announcements. Focus movement alone must not execute commands. Exact platform role mappings and speech require implementation verification. [VoiceOver: Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation).

### Deletion confirmation

Activation of Delete Account opens a confirmation without mutating data. Proposed title: **Delete Account?** Proposed message: **This will delete your account and its data. This cannot be undone.** Use this message only if the actual deletion/retention contract supports it; replace it with accurate scope, retention, and completion timing before shipping. Do not promise that subscription billing stops. If Apple auto-renewable subscriptions exist, provide separate management guidance; if Sign in with Apple is used, account deletion also needs token revocation. These capabilities are unknown, not additional verified defects. [Managing accounts: Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts).

Provide **Delete Account** (destructive action) and **Cancel** (cancel action). For an iPhone vertical button stack, place the action above Cancel. Product decision: use **no default action**, so Return alone cannot commit deletion; focused explicit activation still works. The alert guide permits a normal default for deliberately requested destruction, so this conservative choice is not a universal ban on destructive defaults. Escape/Command-Period cancel on a supported attached keyboard. Cancel or precommit interruption closes the confirmation, makes zero deletion requests, preserves the selected view, and restores focus to Delete Account on return. If Assistive Access is supported, use its documented two-confirmation treatment for difficult-to-reverse actions; do not impose that mode-specific rule on ordinary iOS. [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

## Framework-agnostic state model

```text
state:
  selectedView = one valid view ID, if related views exist
  deletion = idle | confirming | submitting | failed | complete

activateView(id):
  require id belongs to relatedViews
  if id == selectedView: return
  atomically:
    selectedView = id
    visibleContent = contentFor(id)
    selectedSemantics = (choice.id == id) for every choice
  retain focus on activated choice; publish relevant state/content change

activateDelete():
  if deletion in {idle, failed}: deletion = confirming
  // Present confirmation; no destructive request.

cancelConfirmationOrInterruptBeforeCommit():
  if deletion == confirming:
    deletion = idle
    close confirmation; restore initiating focus when page resumes

confirmDeleteByExplicitActivation():
  require deletion == confirming
  deletion = submitting
  disable duplicate submission; show labeled activity in initiating action
  request deletion once with operation identity
  // Backend must enforce duplicate protection; UI alone cannot guarantee it.
  on confirmed success:
    deletion = complete
    show accurate completion status; leave deleted account context
  on confirmed failure:
    deletion = failed
    show actionable error; allow a new explicit confirmation
  on uncertain outcome or interruption after submission:
    reconcile operation status before offering another destructive request
    never describe cancellation as undoing a committed request
```

Pending-state indication follows [Buttons: iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). Duplicate protection and reconciliation are engineering decisions, not quoted HIG mandates. External view-state changes must use the same atomic selection/content update; an invalid stored ID falls back to one valid view, never zero or two selections when choices exist.

## Worked before/after

**Before, supplied:** Nine unrelated long labels share one control; two selections persist; labels collapse to identical prefixes. Choosing Delete Account destroys data immediately; assistive users hear no selection state.

**After, illustrative:** If inventory supports related local views called Profile and Security (example names, not supplied features), the page shows `Profile [selected] | Security`. Activating Security changes both content and selected semantics to Security; Profile becomes unselected. Repeating Security does nothing. The semantic equivalent is “Security, selected, choice in Account view”; this is not a promised VoiceOver transcript.

The person then activates the separate Delete Account button. Security remains the selected view, data is unchanged, and the confirmation appears. Cancel restores the account page and initiating focus with zero deletion requests. Reopening and explicitly activating Delete Account submits one request; repeated activation while pending submits none. Success shows completion; failure or uncertain completion follows the recovery contract above. If inventory finds no actual view choices, the corrected page contains action buttons and no segmented control.

## Acceptance checks and status

**Passed — document inspection:** Platform and all five findings are directly supported by `interface.md`; installed root, family, topic, and source guidance were read in that order per route. The correction separates selection from commands and defines precommit cancellation and destructive commit boundaries. These are specification checks, not runtime passes.

**Failed — supplied interface contract:** Immediate destruction on segment selection; exactly-one selection; selected-state feedback; distinguishable labels; related grouping and practical iPhone segment count.

**Not executed — implementation acceptance:**

| Check | Required result |
| --- | --- |
| Inventory each of nine entries | Every original outcome is retained and mapped to a suitable control; no unnamed action is assumed to be a view. |
| Activate each view, repeat, restore/external change | Exactly one selected ID and matching content; repeat is a no-op; invalid IDs recover deterministically. |
| Activate each command | Only its named outcome occurs; no retained view-selection styling on commands. |
| Open deletion, Cancel, Escape, interruption before commit | No data mutation/request; previous view retained; initiating focus restored on return. |
| Return with no explicit target; explicit confirm; repeat | Return alone does not delete; explicit confirm submits once; pending repeats cannot duplicate. |
| Success, failure, timeout, interruption after commit | Accurate status; reconcile unknown result before retry; no false completion or false undo promise. |
| Keyboard, VoiceOver, Switch Control | Entire task reachable and activatable; unique names, current selection and grouping exposed; confirmation focus contained and restored; no activation from mere focus. |
| Narrow supported iPhone widths, 200% text, longer translations | Complete distinguishable names; no overlapping targets; usable vertical alternative when needed. |
| Geometry and appearance inspection | Targets meet the specified 44 × 44 pt design target; measured separation and selection distinguishability; selection does not rely solely on color. |
| Account integrations, if present | Actual timing/retention disclosed, subscriptions handled separately, linked tokens revoked, completion confirmed. |
| Assistive Access, if supported | Difficult-to-reverse deletion uses that mode's two confirmations. |

## Evidence limits and route record

No web access was used. Official links identify the sources represented by the installed snapshot (2026-10-25); they were not fetched or checked for later revisions. No device, GUI, SDK, accessibility tool, runtime test, deletion request, build, or backend execution occurred. Contrast, target geometry, native rendering, spoken output, focus order, localization layout, and recovery behavior remain unverified. No screenshot-specific media route applies because no image or animation was supplied.

Installed package root: `.agents/skills/apple-hig/`. Read root `SKILL.md` and searched `references/topic-index.md` for the relevant concepts. Routes read (each family SKILL.md, then `.topics/apple-hig-<topic>/SKILL.md`, then its `references/<topic>.md`):

- `subskills/apple-hig-selection-and-input/` → segmented-controls.
- `subskills/apple-hig-menus-and-actions/` → buttons (routed by segmented-controls).
- `subskills/apple-hig-presentation/` → alerts (routed by buttons).
- `subskills/apple-hig-patterns/` → managing-accounts.
- `subskills/apple-hig-foundations/` → accessibility.
- `subskills/apple-hig-technologies/` → voiceover (routed by accessibility).

Every consumed file was read or searched in a separate shell command. No SDK or platform feasibility claim is needed for this review of an explicitly supplied iOS control.
