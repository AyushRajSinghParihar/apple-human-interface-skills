# Revised Mac scanner settings interaction specification

## Basis and decisions

`interface.md` supplies a text description: resolution, file destination and unrelated account deletion share six heavy nested outlined boxes; “Advanced” appears three times; the window can become narrow. It supplies no screenshot, implementation, option inventory, dimensions, or persistence behavior. The exact nesting and control types are unknown.

Use a single column of two unboxed semantic groups, in this order:

| Group heading | Contents | Reason |
| --- | --- | --- |
| Scan quality | Resolution, with its current value and existing editing control | Describes the scan property being changed. |
| Save location | File destination, with its current value and existing editing control | Describes where output goes. |

Remove all six outlined containers and all three generic “Advanced” labels. Use alignment and space to establish relationships; add no replacement outer border. This is a design choice applying Apple's preference for spacing/alignment before nested borders, rather than a rule that boxes are forbidden. With only two known settings, neither disclosure nor tabs improve the task. Keep both settings visible. [Boxes — Best practices](https://developer.apple.com/design/human-interface-guidelines/boxes#Best-practices).

Use plain section headings “Scan quality” and “Save location”, without punctuation. These are unboxed headings. If a later, evidenced inventory justifies a box, its short sentence-case settings-pane title takes a colon and sits above the box on Mac; do not apply that exception to every heading. [Boxes — Content and macOS](https://developer.apple.com/design/human-interface-guidelines/boxes#Content).

Move the existing account deletion action to the app's Account settings pane, outside the scanner panel. If no Account pane exists, add an Account destination in the app's settings navigation and put the action there. Navigating there must not trigger deletion. Retain its existing action flow; deletion confirmation, authentication and recovery behavior are not evidenced or redesigned here. This placement is a product decision grounded in the distinction between account preferences and task settings. [Settings — General settings](https://developer.apple.com/design/human-interface-guidelines/settings#General-settings).

## Scope, state and transitions

For this specification, treat this panel as app-wide **scanner defaults**, not as edits to an already running scan. That scope is a proposed product contract, not an observation. Title the pane “Scanner”; add supporting text “Defaults for new scans.” If the actual product uses current-job options, keep these groups beside the scan workflow and change that scope text before implementation; do not silently change existing setting scope. Apple recommends keeping frequent task options near their effects. [Settings — Task-specific options](https://developer.apple.com/design/human-interface-guidelines/settings#Task-specific-options).

Retain the existing supported resolution choices, destination editor, validation and commit policy. The brief gives no basis for choosing a resolution value, inventing a folder, replacing controls, or converting Apply/Cancel to automatic saving. Existing stored values win on migration; for first use, retain the product's existing valid defaults. Detect scanner capabilities through the existing capability source rather than inventing choices. If capability detection or commit semantics do not exist, that integration contract remains unresolved before implementation.

Framework-agnostic structure and transition contract:

```text
ScannerPane(title="Scanner")
  supportingText("Defaults for new scans.")
  Group(id="quality", heading="Scan quality", border=none)
    Setting(id=existingResolutionID, label="Resolution",
            editor=existingResolutionEditor, value=existingResolutionValue)
  Group(id="save", heading="Save location", border=none)
    Setting(id=existingDestinationID, label="File destination",
            editor=existingDestinationEditor, value=existingDestinationValue)

open Scanner:
  bind existing settings model; restore existing values/pending edits as applicable
edit either setting:
  delegate to existing validation and commit flow; do not mutate the other setting
resize:
  recompute layout only; retain values, pending edits, focus and scroll context
leave for Account / close / reopen:
  use existing commit-or-cancel policy; do not silently discard pending edits
  restore previously visited settings pane under the app's navigation policy
open Account:
  show existing account deletion action; opening the pane has no destructive effect
```

Keep app Settings access in the app menu with expected Command-Comma access; the scanner redesign must not remove existing access. Stable pane navigation should identify the selected pane and restore the last visited pane. These are requirements for integration, not claims about the supplied app. [Settings — macOS and Best practices](https://developer.apple.com/design/human-interface-guidelines/settings#macOS).

## Layout and semantic contract

Use these initial design tokens in logical layout units: 20 outer inset, 24 between groups, 8 between a heading and its content, and 12 between a field label and its editor. These are proposed tokens, not Apple-mandated measurements. Keep groups aligned to the same leading edge. Do not make “Resolution” or “File destination” faint to reduce visual weight.

At widths where the full label, gap and usable existing editor fit, place label and editor on one row. Otherwise stack label above editor with an 8-unit gap. Compute fit from actual localized text and editor minimum usable size, not a device name or an arbitrary fixed breakpoint. Stack destination editing actions as needed. Permit variable row heights and wrapping; keep the destination value selectable/copyable so a long location remains usable. Render labels as text with system-equivalent typography and semantic foreground roles. [Labels — Best practices](https://developer.apple.com/design/human-interface-guidelines/labels#Best-practices).

Keep a vertical scrolling content region when height is insufficient. Do not pin required controls to an unreachable bottom edge or introduce horizontal scrolling for this form. Set a minimum supported window width only if an existing editor cannot remain operable after stacking; determine that limit by measurement during implementation. A resize must not hide a group, change its scope, reset a value, or collapse it. Apple calls for adaptation to available space and cautions against relying on the Mac window's bottom edge for essential controls. [Layout — Adaptability and macOS](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability).

Expose named semantic groups introduced by their headings, and associate each field label with its own editor. Preserve the existing editor role and expose its current value, including updates. Logical reading order: pane title, scope description, Scan quality heading, Resolution editor, Save location heading, File destination editor and its associated actions. Keyboard traversal follows interactive elements in that order; headings are not extra Tab stops. Preserve the focused control's identity through reflow. Do not merge a group into a single inaccessible element that hides its editor. These are proposed semantics requiring runtime verification. [VoiceOver — Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation).

## Worked before/after

**Before, as reported:** the user seeking resolution must interpret six heavy nested boxes and repeated “Advanced” labels; account deletion sits among scan settings. The brief does not establish exact control order or the number of clicks.

**After, illustrative values only:** a user opens Scanner, changes a supported resolution from 300 dpi to 600 dpi, then checks that the file destination remains `/Users/lee/Scans`. These values demonstrate independence; they are not new defaults or claims about hardware support.

```text
Wide                                     Narrow
Scanner                                  Scanner
Defaults for new scans.                  Defaults for new scans.

Scan quality                             Scan quality
Resolution       [600 dpi]               Resolution
                                         [600 dpi]
Save location
File destination [ /Users/lee/Scans ]     Save location
                                         File destination
                                         [ /Users/lee/Scans ]
```

Both layouts expose the same two groups without borders or “Advanced” disclosures. Resizing during editing leaves 600 dpi and the destination intact. The user reaches account deletion separately through Settings → Account. A nonvisual walkthrough follows the two named groups, hears each editor's current value, edits resolution, then reaches the unchanged destination without encountering deletion.

## Acceptance checks and status

**Passed — document inspection only:** the supplied inventory is mapped: resolution → Scan quality, destination → Save location, deletion → Account. The revised structure has zero nested borders, zero repeated “Advanced” labels and explicit wide/narrow behavior. The specification defines state preservation and semantic associations. These passes concern this document, not an application.

**Failed — supplied design against this specification:** the described six nested outlined boxes, repeated generic labels and unrelated deletion action do not meet the revised grouping contract. Their presence is supported only by `interface.md`; no visual severity or runtime failure was measured.

**Not executed — implementation acceptance matrix:**

| Check | Observable pass criterion |
| --- | --- |
| Wide, narrow and intermediate resize | Both groups remain reachable; rows stack at measured fit limits; no clipping, overlap or horizontal scrolling. Record actual dimensions. |
| Short window | All editors and existing commit actions are reachable by scrolling and keyboard, without reliance on a fixed bottom edge. |
| Enlarged text and long localized strings | Headings stay with their groups; labels and values remain readable; actions remain operable. Record text settings and strings. |
| Values and reopening | Existing stored values survive migration; editing one field does not change the other; reopen/leave follows the existing commit policy. Test default and changed values. |
| Scanner changes | Existing capability handling yields valid choices or explains unavailable editing; no invented resolution or silent invalid substitution. |
| Account relocation | Deletion is absent from Scanner, reachable in Account, and never invoked by navigation; pending scanner edits follow the existing policy. |
| Keyboard and VoiceOver on Mac | Both editors are reachable, correctly named and valued in group order; reflow retains focus; no obsolete container or duplicate heading announcements. |
| Appearance and destination text | Light/dark appearance preserves readability; long destination values can be selected/copied without losing access to editing actions. |

## Evidence limits and audit trail

Used only `interface.md` and the installed package rooted at `.agents/skills/apple-hig/`. Explicitly read the root `SKILL.md`, searched relevant topic-index rows, then read each owning family and topic procedure before its supporting source guide: Layout and organization → Boxes and Labels; Patterns → Settings; Foundations → Layout; Technologies → VoiceOver. Each consumed file was read in its own shell command. Official URLs above identify the local guides' sources; they were not opened online.

The installed articles identify a 2026-10-25 snapshot/retrieval date. They are local application guidance, not SDK documentation or independent proof of current Apple behavior. The local settings guide describes pane-oriented sizing, while the brief explicitly requires narrow resizing; this specification preserves resizing and stable navigation, without imposing fixed pane dimensions.

No app code, screenshots, complete control inventory, device, SDK, GUI, scanner, keyboard interaction, or accessibility runtime was supplied or executed. No compilation, rendering, contrast measurement, VoiceOver result, actual supported resolution, commit behavior, or working Account pane is claimed. The result is an implementable grouping and state contract; final editor fit limits and integration with the existing settings model require implementation evidence.
