# Revised Mac scanner settings interaction specification

## Evidence and scope

`interface.md` supplies a macOS panel description: resolution, file destination, and unrelated account deletion share six heavy nested outlined boxes; “Advanced” repeats three times; the window resizes narrowly. No screenshot, hierarchy, control implementation, dimensions, option inventory, persistence behavior, or deletion flow was supplied. The defects established by the brief are misleading grouping and repeated nonspecific titles. Exact clipping, keyboard behavior, and accessibility defects remain unestablished.

This is a framework-agnostic design contract. It preserves the two scanner settings and access to account management. Control choices and state behavior below are proposed product decisions, not descriptions of existing software.

## Decisions and source support

1. **Remove all six outlined containers.** Use two sibling, borderless semantic groups: **Scan quality** and **Save location**. Give each one visible heading and its own controls, separated by whitespace. There is no evidence that a retained border would add meaning beyond these headings. Avoid a screen-sized replacement box. This applies [Boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/boxes#Best-practices), which recommends alignment and spacing before nested borders. It does not prohibit every box.
2. **Replace all three “Advanced” labels.** Resolution is a core setting under Scan quality; destination is under Save location. Nothing described warrants hidden advanced content or a disclosure control. These are headings, not box titles, so they have no trailing colon. If a later design retains a real settings-pane box, its brief sentence-case title goes above it on Mac and takes a colon, per [Boxes — Content and macOS](https://developer.apple.com/design/human-interface-guidelines/boxes#Content). Removing borders must preserve semantic relationships.
3. **Move account deletion to a separate Account destination in the app’s settings navigation.** Keep it out of both scanner groups and out of resolution options. The scanner panel has a low-emphasis **Account Settings…** button after the groups, opening that destination without deleting anything. The ellipsis communicates further interaction, per [Buttons — macOS](https://developer.apple.com/design/human-interface-guidelines/buttons#macOS). This relocation is a product judgment applying meaningful grouping, not an Apple mandate about scanner apps. The Account destination must expose the existing deletion entry; its confirmation, reversibility, and backend behavior require separate inspection and are outside this grouping change. Opening it must never activate deletion.
4. **Represent resolution as a labeled single-choice pop-up** displaying its current value with units. Populate only supported scanner values; do not invent capabilities. Persistent selection belongs apart from commands, following [Pop-up buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Best-practices). Use the existing valid resolution on entry; if no valid value exists, require a supported selection rather than silently fabricating a default.
5. **Show the destination as selectable, copyable location text with a “Choose Folder…” button.** It opens a folder-selection interaction; selecting a folder and accepting commits the choice, while cancellation preserves the prior destination. A location is useful portable text under [Labels — Best practices](https://developer.apple.com/design/human-interface-guidelines/labels#Best-practices). The chosen folder interaction is an abstract host capability, not an SDK assumption.
6. **Reflow from available space.** Keep group order, values, and focus stable while stacking rows when their measured content no longer fits. This applies [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability). Use a scrollable document rather than fixed bottom-positioned essential controls, respecting [Layout — macOS](https://developer.apple.com/design/human-interface-guidelines/layout#macOS).

## Worked before / after

Before, as described (not an inferred exact tree):

```text
Six heavy nested outlines
  “Advanced” repeated three times
  Resolution / file destination / unrelated account deletion mixed together
```

After, expanded layout:

```text
Scanner settings

Scan quality
  Resolution:       [300 dpi                 v]

Save location
  Destination:      /Users/lee/Documents/Scans
                    [Choose Folder…]

[Account Settings…]
```

After, narrow layout:

```text
Scanner settings

Scan quality
  Resolution:
  [300 dpi                       v]

Save location
  Destination:
  /Users/lee/Documents/
  Scans
  [Choose Folder…]

[Account Settings…]
```

Example values are fixtures, not supplied scanner capabilities or actual user paths. For a worked transition, assume supported values include 300 and 600 dpi. Start at 300 dpi and folder A. Select 600 dpi: the displayed and draft values become 600 dpi. Open Choose Folder…, select B, then cancel: folder A remains. Reopen, accept B: the draft destination becomes B. Narrow the window: 600 dpi and B persist. Open Account Settings… and return: the same scanner draft remains, with no deletion requested.

## Layout and semantic contract

Use a single leading-aligned content column. Proposed spacing tokens are 20 logical points for outer margins, 24 between groups, 8 between a heading and content, and 12 between row columns. These are project starting values, not HIG-prescribed measurements. Align wide-layout field labels together and values together. Do not indent each former box level.

For each group, measure its widest label plus column gap plus the usable width of its control/value. Use aligned rows only when this fits within the content width; otherwise stack label above value. Recalculate for resizing, text enlargement, and localization. Headings and paths wrap without fixed row heights. Long unbroken path segments may break visually without inserting characters into the copied value. Button labels wrap if necessary. Do not hide controls, replace labels with unexplained icons, or require horizontal scrolling. At large widths, keep controls near their labels rather than stretching the gaps.

Semantic order is: panel heading; Scan quality group, Resolution label and choice; Save location group, Destination label and value, Choose Folder…; Account Settings…. Each group has its visible heading as its name; each input has its own label. Borders and spacing are not the only grouping signal. Headings and static text are not extra Tab stops. Keyboard focus proceeds through Resolution, Choose Folder…, Account Settings…, with selectable path text reachable through the host’s text-navigation behavior. Pointer and keyboard activation must have equivalent outcomes. Resizing preserves the focused control and scrolls it into view when needed.

Use readable text and semantic foreground roles; keep essential labels and values legible rather than making them faint to reduce visual weight. Custom controls need visible focus, press feedback, names, roles, values, and enabled states. Verify text enlargement to 200% and complete keyboard access, following [Accessibility — Vision, Mobility, and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). No native component behavior is assumed.

## State and interaction contract

```text
state = {draftResolution, draftDestination, folderChooserOpen, focusedControl}

enter:
  load existing scanner draft, otherwise existing saved configuration
  reflect its actual values; do not reset because the layout changed

selectResolution(value):
  if value is supported: update draftResolution and its displayed value together
  otherwise: retain prior value; show a persistent explanation beside the choice

chooseFolder:
  open one chooser initialized to draftDestination
  repeated activation while open brings that chooser forward
  cancel -> close, retain prior destination, focus Choose Folder…
  accept(folder) -> validate using host capability
    valid -> update draftDestination and displayed path together; close
    invalid -> preserve prior destination; explain why; allow another choice or cancel

openAccountSettings:
  retain scanner draft; navigate to Account destination; request no deletion
  return -> restore scanner draft and focus Account Settings…

resize:
  recompute row arrangement; preserve draft, open interactions, and focus identity
```

Edits affect the scanner draft and must not initiate a scan. Preserve the host’s existing Apply/save boundary and cancellation behavior; this reorganization introduces no new persistence policy or Apply button. Integration must map draft updates to that existing boundary before release. If none exists, persistence is an unresolved product decision. Do not claim settings survive app restart until that behavior is established. Folder validation must not claim future write success; an unavailable destination gets a persistent inline explanation and a reachable Choose Folder… recovery action.

Neither new button is a default destructive action. Return within the resolution choice selects a value; it must not invoke account deletion. No new global shortcut is assigned. Button target regions must remain distinct and nonoverlapping. The local Buttons guide gives a general 44 × 44 pt hit-region recommendation while Accessibility lists macOS default controls at 28 × 28 pt, minimum 20 × 20 pt. These different scopes do not establish a universal Mac size. For these two custom button targets, conservatively allocate at least 44 × 44 pt selectable regions while retaining Mac visual styling; measure rather than infer targets from their labels.

## Acceptance checks and current status

| Check | Pass condition | Current evidence |
|---|---|---|
| Inventory | Resolution and destination retained; account management remains reachable separately | Passed: specification inspection |
| Group meaning | Two named scanner groups; no nested outlines or repeated Advanced titles | Passed: specification inspection |
| Worked transition | Selection changes draft; folder cancel retains A; acceptance selects B; resizing and navigation preserve both | Passed as a written state trace only |
| Original grouping | Unrelated deletion shares nested scanner grouping | Failed against the proposed grouping criterion, based on brief only |
| Wide/narrow/short layouts | At proposed test viewports 720 × 600, 320 × 600, and 480 × 240 logical points, all labels, values, and controls remain reachable; short height scrolls vertically | Not executed |
| Continuous resize | Repeatedly cross each measured row-fit threshold without losing focus, selection, values, or open chooser | Not executed |
| Text/localization | At 200% text, doubled label lengths, and a long unbroken path, reflow preserves meaning and full-value copying | Not executed |
| Selection model | All supported values, repeated selection, and external value changes keep display and state synchronized; no command appears as a resolution option | Not executed |
| Folder interaction | Cancel changes nothing; valid accept updates draft; invalid/unavailable folder explains recovery; duplicate activation creates no duplicate chooser | Not executed |
| Keyboard and assistive access | Complete task without pointer; correct group/name/value associations; focus returns after chooser and Account navigation | Not executed; requires implemented UI and supported environment |
| Appearance and targets | Light, dark, and Increase Contrast remain legible; measure contrast and hit regions; controls do not overlap | Not executed; no rendered colors or geometry supplied |
| Account separation | Account entry is discoverable, returning preserves scanner state, and scanner controls/default activation cannot request deletion | Not executed |
| Persistence integration | Existing save/cancel policy is preserved and explicitly verified by the implementation owner | Not executed; host policy unknown |

## Evidence limits and reading audit

Only local files and installed instructions were used; no web browsing occurred. Official links above identify source guidance, not live verification. The installed references are dated 2026-10-25 local application guidance based on Apple sources, not an SDK reference or evidence of independent review.

Auditable reads used one file per command, rooted at `.agents/skills/apple-hig/`: root `SKILL.md`; Layout and organization family, then Boxes and Labels procedures before their references; Menus and actions family, then Buttons and Pop-up buttons procedures before their references; Foundations family, then Layout and Accessibility procedures before their references. The Boxes procedure routed the additional Labels and Layout reads. Resolution’s original control type is unspecified; the pop-up is a candidate selected for this proposal. Destination’s original representation is unspecified; the revised contract uses static location text plus a button, not a new editable text field.

No application, device, scanner, SDK, GUI, accessibility tool, or automated UI test was executed. The written checks establish specification coverage only. Rendering, actual spoken order, focus behavior, keyboard interaction, folder-picker integration, scanning, deletion recovery, and persisted settings remain unverified. No claim of accessibility conformance or native appearance is made.
