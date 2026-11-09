# Revised Mac document toolbar interaction specification

This is a proposed interaction contract, based on `interface.md`, not an implemented or executed interface. It preserves article reading/editing and document commands without assuming an Apple SDK.

## Evidence and decisions

The brief reports a scrollable article inside the toolbar, tiny differently styled action icons, Delete dominating Save, clipped tools at narrow widths, and essential hover-only actions. No command inventory, dimensions, screenshot, code, save model, or deletion scope is supplied. Small glyphs alone do not establish small activation regions.

1. Move the article into the document body below a stationary top-frame toolbar. The toolbar contains commands and a concise document title, never article paragraphs. The body owns vertical scrolling; reflow text to the available width, avoiding a second same-axis scroll container. Resizing preserves the reading anchor or insertion point; reveal a relevant selection only as far as necessary. This applies [Toolbars: purpose and macOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#macOS) and [Scroll views: best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices). The no-overlap layout needs no decorative scroll-edge overlay.
2. Use consistent, bezel-free toolbar items, comparable glyph weights and peer dimensions. Prefer familiar symbols; use text when meaning is uncertain. Save is a persistent text action at the trailing edge and the single emphasized task action. Delete is secondary, separated from Save by a functional group gap, never larger or primary. Do not bind ordinary Return in article editing to either toolbar action. These choices apply [Toolbars: actions and item groupings](https://developer.apple.com/design/human-interface-guidelines/toolbars#Actions) and [Buttons: style and role](https://developer.apple.com/design/human-interface-guidelines/buttons#Style); they are product decisions rather than a requirement that all Mac Save controls use accent fill.
3. Replace hover-only essential access with persistent toolbar or menu commands. Hover may supplement an icon with a tooltip; it cannot be the only way to discover or activate it. Preserve configured mouse/trackpad mappings. See [Pointing devices: best practices and macOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#macOS) and [Accessibility: mobility and speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).
4. Every toolbar action has a menu-bar command with identical scope, enablement, and handler. This remains true when the toolbar is hidden or customized. See [Toolbars: macOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#macOS) and [The menu bar: best practices](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Best-practices).

## Command contract

Assume Save writes the active document; existing storage/autosave behavior must be preserved. For this concrete proposal, Delete means irreversible deletion of the active article/document, including its unsaved edits. This is a proposed scope, not an observed fact. If the real command deletes selected text or moves a file to recoverable Trash, revise its label, menu placement, copy, and recovery contract before implementation; never silently apply whole-document deletion to a selection command.

| Command | Surface and placement | Outcome and availability |
|---|---|---|
| Save | Trailing toolbar, File > Save; Command-S | Save active writable document. Enabled for dirty or untitled documents, disabled without a document, when read-only, or while saving. Explain read-only state in document status. |
| Delete Article… | Last secondary toolbar group; File > Delete Article…; no new shortcut | Opens the confirmation below for the active article. Disabled without a deletable article or during a conflicting save/delete operation. Ellipsis reflects required further input. |
| Existing essential actions, presently unnamed | Common tools in center; corresponding File/Edit/View or existing domain menu by scope | Preserve actual labels and outcomes. Each must be inventoried and assigned a stable command ID before implementation; do not invent Export, Share, or navigation capabilities from this brief. |
| Show/Hide Toolbar | View menu; label describes next action | Toggle toolbar visibility without changing document, selection, or scroll position. |
| Customize Toolbar… / Restore Default Toolbar | View menu, if customization is supported | Customize secondary items/order only; restore defaults explicitly. Save remains pinned in the shown toolbar. |

All surfaces dispatch the same command ID against the active document. Switching windows changes the active target; an already-open deletion confirmation retains its original document ID and displayed name. Revalidate permission and existence immediately before mutation.

Save states: idle → saving → saved or failed. While saving, suppress duplicate submissions and show nonmodal “Saving…” status without changing item width. On success mark only the saved revision clean; newer edits remain dirty. On failure retain all edits, show persistent “Couldn’t save” status with a retry route through Save, and re-enable it. Save on an untitled document requests name/location; cancellation preserves edits and returns focus. No success is announced before storage acknowledges it.

Deletion confirmation: title `Delete “{article title}”?`; message `This permanently deletes this article and its unsaved changes. This cannot be undone.` Buttons: Cancel (leading, cancellation role), Delete Article (trailing, destructive role). Product choice: no default button; Return alone does not confirm, explicit focused-button activation does. Escape or Command-Period cancels. Cancel changes nothing and restores initiating focus. Successful explicit confirmation deletes only the captured target and closes its document view; failure retains the view and presents a useful error without stacking alerts. Disable repeated confirmation while pending. This conservative choice follows [Alerts: best practices and buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons). The source permits a normal default for deliberately requested destruction; it does not universally forbid destructive defaults. Routine undoable deletion would instead need a recovery contract and generally no confirmation.

## Width, overflow, and restoration

Use at most three functional regions: leading document identity (and existing navigation only if present), center common tools, trailing Save. Delete occupies a separated end of the secondary tools, not the primary position. Title names the document, not the app; prefer a short display title, retaining its full name in window identity and accessible description. Truncating the title is preferable to clipping action labels.

Width is measured usable toolbar space after window controls and insets. Breakpoints depend on measured localized labels, target geometry, and current customization, not a fixed window-width guess.

```text
layout(width, textScale, locale, customization):
    retain stable command IDs, document, selection, readingAnchor
    reserve Save's full label and target
    reserve concise identity and a single overflow affordance if needed
    fit secondary groups in frequency order; Delete has lowest retention priority
    move nonfitting secondary items into overflow, preserving their logical order
    shorten displayed title before sacrificing pinned Save
    never reduce target sizes or clip a command to force it to fit
    minimumUsableWidth = measured identity + Save + required overflow + gaps/insets
    enforce minimum window width for that locale/text scale
```

Use the platform toolbar's automatic overflow when available; do not add a second app “More” menu. If the eventual framework provides no automatic overflow, implement one equivalent labeled “More Actions” affordance for displaced commands only. Its keyboard-accessible menu lists full labels and disabled states; Escape closes it and returns focus. This fallback is a framework requirement, not a claim that native overflow has been tested. Do not put secondary commands in overflow by default when they fit. See [Toolbars: best practices and item groupings](https://developer.apple.com/design/human-interface-guidelines/toolbars#Best-practices).

| State | Direct access | Other access and preservation |
|---|---|---|
| Wide: all measured groups fit | Title, common tools, separated Delete, Save | Every action also in menu bar; no empty overflow |
| Narrow: secondary groups no longer fit | Concise title, highest-priority tools that fit, Save, one overflow | Delete moves first; displaced tools retain full menu entries; article reflows |
| Minimum supported width | Identity, Save, overflow | All secondary commands in overflow and menu bar; no toolbar scrolling or clipping |
| Toolbar hidden | Article body only | Menu bar retains all actions; View > Show Toolbar restores previous arrangement |
| Customized | Pinned identity/Save plus chosen secondary tools | Removed tools remain in menus; Restore Default Toolbar restores initial layout |
| Resize during focus/menu use | Current task state retained | If a focused item moves into overflow, close its popup safely and focus overflow; if toolbar hides, move focus to article without activation |

Do not automatically hide the toolbar on pointer exit or article scrolling. If contextual editing modes exist, exiting them restores the prior toolbar and selection; this mode is not evidenced in the brief.

## Geometry and alternative access

Use a conservative project target of at least 44 × 44 pt activation regions, nonoverlapping, with 8 pt project-defined gaps between unrelated items; grow text actions to fit. Glyphs may be smaller within those regions. This intentionally conservative choice resolves differing local guidance: Buttons gives a general 44 × 44 pt rule, while Accessibility lists macOS default 28 × 28 pt and minimum 20 × 20 pt. Do not represent 44 pt as a Mac-specific minimum or use 20 pt as the design goal. The proposed dimensions are logical points; actual framework scaling remains to be measured. Collapse tools sooner instead of shrinking them.

Give every command a button role, action name, enabled state, and visible focus treatment; names match its visible label or tooltip. Tooltips supplement semantic names. Keyboard and assistive navigation must reach visible toolbar items and overflow in visual order, without hidden duplicates. Menu commands provide a complete alternative path. Preserve article focus/selection on Save. At 200% text enlargement, measure again, reflow body text, grow targets/toolbar height as necessary, and move secondary items to overflow without clipping Save. Use sufficient contrast in light/dark and Increase Contrast appearances; no contrast measurements are available. See [Accessibility: vision, mobility, speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Worked before/after

Before, as reported: a person reading a long article scrolls within the toolbar. Delete visually outweighs Save. Narrowing the window clips tools; finding an essential command requires hover. Its exact position and command name are unknown.

After, illustrative layout fixtures (not measured runtime screenshots):

- At 1000 pt window width, assuming measured fit: `[Draft title] [existing common tools] [Delete Article…]     [Save]`. The complete article scrolls in the body below.
- At 480 pt, assuming only essentials fit: `[Draft…]                         [overflow] [Save]`. Delete and nonfitting common tools appear in the single overflow; Save remains directly visible and Command-S still works.
- A person edits, narrows the window, and saves. The same document revision is submitted, the reading position remains stable, and success clears only that revision's dirty state. Reopening the wide window restores displaced tools in their previous order. Choosing Delete opens the named confirmation; Escape returns to the unchanged draft.

These widths are test fixtures, not Apple breakpoints. If measured essentials cannot fit at 480 pt, the implementation must report/enforce its measured minimum rather than claim that fixture passes.

## Acceptance checks and evidence limits

**Passed — document inspection only:** read the supplied brief; explicitly read the installed root skill, searched its topic index, read selected family/topic procedures before their supporting guides; produced a width/state access map, shared command contract, before/after, and destructive-action policy. No web access or SDK assumptions were used.

**Failed — supplied design description:** narrow-width reachability fails because tools clip; essential discoverability fails because some actions require hover; hierarchy fails because Delete dominates Save. These are reported brief findings, not independently reproduced defects. Actual hit geometry remains unknown.

**Not executed — implementation acceptance gates:**

| Check | Pass condition |
|---|---|
| Wide → narrow → minimum → wide, including long localized title | No command clips, Save stays visible, only one overflow, order and document state survive; exact transition widths recorded |
| Article scroll, resize, offscreen selection/insertion | One vertical owner; all article content reachable; minimal reveal; no unwanted jump or toolbar scroll |
| Every command through toolbar, overflow, and menu | Same target, availability, outcome, and errors; no toolbar-only or hover-only essential actions |
| Hidden/customized toolbar, no document, read-only document, two windows | Commands remain discoverable; correct disabled reasons and active-document routing; Show/Restore works |
| Save success, failure, rapid repeated input, edits during save | No duplicate operation, no data loss, dirty state reflects revision, retry works |
| Delete confirmation, cancel, Return, explicit activation, failure | Exact scope/copy, no Return-only deletion, cancellation preserves edits, captured target only, no stacked alerts |
| Keyboard and supported assistive input | Full task completion, meaningful names/states, visible focus, safe overflow focus transfer, no inaccessible duplicates |
| 200% text, light/dark, Increase Contrast | No lost actions/content; measured targets and gaps pass; measured text/state contrast remains legible |

Only local prose and dated guidance were available. Runtime layout, native overflow, menu behavior, actual targets, contrast, focus order, VoiceOver/Full Keyboard Access, physical comfort, SDK compilation, and GUI execution are unverified. Official links above identify source articles/sections from installed references; they were not fetched or independently checked for freshness. The unnamed essential-action inventory and actual deletion/storage semantics remain implementation inputs, not evidence of existing behavior.
