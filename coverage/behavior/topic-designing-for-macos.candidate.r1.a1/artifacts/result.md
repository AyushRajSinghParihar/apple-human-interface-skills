# Revised Mac transcript comparison specification

This is a framework-agnostic design contract, not an implementation. The supplied `interface.md` establishes macOS, a forced fullscreen single-transcript iPhone port, a hidden menu bar, and swipe-only Copy/Save. It supplies no screenshots, transcript samples, implementation, file formats, or persistence behavior. All behavior below is proposed unless explicitly described as the supplied before state.

## Decisions and source basis

| Decision | Reason and local HIG basis |
|---|---|
| One resizable comparison window contains two equal-status transcript readers. New comparisons can have independent windows. Full screen is optional. | Comparing requires simultaneous context. Mac guidance supports resizing, parallel work, menu commands and precise selection. [Designing for macOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices), [Windows — macOS](https://developer.apple.com/design/human-interface-guidelines/windows#macOS). |
| Two peer reading panes with an operable divider; independent vertical scrolling. No parent/child navigation or unnecessary sidebar. | Split arrangements can be horizontal or vertical on Mac. The peer relationship is a product decision; hierarchical primary/detail selection rules do not describe these transcripts. Prefer a 1 pt divider, with a larger interactive area. [Split views — macOS](https://developer.apple.com/design/human-interface-guidelines/split-views#macOS). |
| Source text is read-only, selectable, and copyable. Save saves the comparison, including source snapshots and reading state. | Protect research source material while supporting quotation. Read-only is our product choice, not an Apple requirement. [Text views — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-views#Best-practices). |
| Expose File and Edit commands in the Mac menu bar; use familiar shortcuts and context-sensitive availability. | Copy/Save must be discoverable without gestures. Retain system menu behavior, including user-configured hiding; do not force the bar hidden. [The menu bar — Best practices](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Best-practices), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts). |
| Use conventional filesystem opening/saving, explicit durability feedback, and autosave after the initial save. | Names, locations and formats belong under user control; a saved cue must reflect completion. [File management — Saving work and macOS](https://developer.apple.com/design/human-interface-guidelines/file-management#Saving-work). |
| Retain selections, scroll anchors, pane ratio and active target during resizing and app switching. | Window changes must preserve the task. [Layout — Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability), [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices). |
| Make all essential actions keyboard reachable, give panes meaningful names, and preserve usability at 200% text size. | Replaces gesture dependence and supports varied reading/input needs. [Accessibility — Vision, Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |

The dimensions, storage model, command subset and adaptation thresholds below are product decisions to validate, not HIG mandates. No Apple SDK or particular UI toolkit is required by this specification. Actual Mac menu/window integration remains an implementation capability to verify.

## Window and reading contract

Initial window target: 1200 × 800 logical points, clamped to the available work area. Minimum target: 640 × 480 pt. Retain standard system movement, close, minimize and zoom controls. Window > Zoom remains distinct from View > Enter Full Screen. New Comparison creates an independent untitled window; opening an already-open comparison activates its existing window. Different comparison files retain independent state. The Window menu lists comparisons with disambiguating titles.

Content order: window title; two pane headers; transcript bodies. Each header shows “Transcript A” or “Transcript B”, filename, and an Open/Replace action. Accessible names include slot and filename. Identical filenames are distinguished by slot and a secondary source-location description. Long names wrap; complete names remain available to assistive technology. An empty pane explains “Open a local transcript” and offers a labeled action. No save or copy action depends on the bottom edge of the window.

At usable content width of at least 900 pt, use side-by-side panes, initially 50/50. Each pane has a minimum width of 320 pt. Below 900 pt, stack A above B, retaining both headers and readers; each reader has a target minimum body height of 120 pt. If enlarged headers leave insufficient height, retain the focused reader and expose the other through View > Focus Transcript A/B, with a visible “Show Transcript A/B” action. Expansion restores both panes and the previous wide divider ratio. Never discard the hidden pane's content or selection. Explicit focus actions reveal their pane before focusing it.

The divider can be dragged, focused, and adjusted with arrow keys in 1 pt increments along its axis; clamp to useful pane bounds. Its semantic role is adjustable separator with orientation and percentage value. View > Equalize Panes restores 50/50 without resetting reading positions. Do not require a precision drag to recover a usable layout.

Each transcript has one vertical scroll owner, ordinary scroll bars respecting system preferences, and no surrounding same-axis page scroller. Long paragraphs wrap. Unbroken identifiers wrap visually without altering copied text. Leading alignment, comfortable line spacing and a default 15 pt body size are proposed. View > Text Size offers 100%, 125%, 150% and 200%, plus reset; controls and filenames also accommodate the user's text preferences. At 200%, reflow rather than truncate transcript content. The exact mapping to platform text preferences must be verified in the chosen stack. [Scroll views — Best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices) supports minimal reveal and avoiding nested scrolling.

Scrolling A does not move B. This design makes no claim of semantic alignment, synchronized scrolling, automated differences, or matched timestamps. Ordinary selection extension scrolls only enough to reveal the endpoint. Resizing preserves the nearest visible text anchor, rather than a raw pixel offset that could jump after reflow.

## Commands, focus and availability

Use one command dispatcher for menu items, shortcuts and in-pane actions so their targets and enabled states agree. Keep unavailable menu commands visible and dimmed. App menu supplies normal About, Services, hide/show and Quit behavior; Help describes opening two transcripts, selecting/copying and saving. Omit Format because this design has no rich-text editing.

| Menu / command | Shortcut | Scope and availability |
|---|---|---|
| File > New Comparison | Command-N | Creates an empty independent comparison. |
| File > Open… | Command-O | Chooses a comparison file or UTF-8 plain-text transcript; comparison opens in its window, transcript loads into the active slot. With no window, creates an empty comparison first. |
| File > Open Transcript A… / B… | None | Opens into the named slot; also reachable through that pane's Open/Replace action. |
| File > Close | Command-W | Closes key comparison after persistence handling below. |
| File > Save | Command-S | Saves the comparison, not the selected source transcript. Available when at least one slot is loaded; first save requests name/location. |
| Edit > Copy | Command-C | Copies the focused text control's selection. Disabled without a nonempty selection; never implicitly copies from the other pane. |
| Edit > Select All | Command-A | Selects all text in the focused reader or filename entry, never both transcripts. |
| View > Focus Transcript A / B | None | Reveals and focuses the named pane; also reaches empty pane's Open action. |
| View > Equalize Panes; Text Size | None | Window layout/reading presentation. Text Size marks its current value. |
| View > Enter/Exit Full Screen | Control-Command-F | System full-screen behavior; preserves pane state. |
| Window > Minimize; Zoom; Bring All to Front; window list | Command-M for Minimize | Standard window semantics and active-window scope. |
| App > Quit | Command-Q | Completes persistence handling for all dirty comparisons; cancellation leaves remaining work open. |

Cut, Paste and Undo are not transcript editing commands. In editable filename/location controls, preserve conventional text editing and shortcut behavior supplied by the host. Do not intercept these keys globally. No custom gesture is necessary; optional gestures must dispatch the same commands.

On initial opening, focus the first empty slot's Open action. On successful load, focus that reader at its beginning. Tab/Shift-Tab follow a logical order through pane A actions and reader, divider, then pane B actions and reader, honoring Mac keyboard navigation preferences. Full Keyboard Access must reach every action. Menu commands provide a keyboard route to either reader even when ordinary Tab navigation is restricted by preferences. Use normal text keyboard selection conventions and preserve system accessibility shortcuts.

Focus and stored selection are distinct: switching to B preserves A's selection in an inactive appearance. Returning to A restores it. App deactivation preserves both selections and anchors; reactivation restores the previous input target, without an unsolicited jump. Only the focused text control supplies Copy. Opening a file chooser temporarily owns keyboard input; cancel restores the initiating control and leaves the comparison unchanged. Failed loading keeps the previous transcript and offers an inline, persistent error with Retry/Open Another File actions. A read or decode error never installs a partly loaded transcript.

Use visible focus indicators and the “Active transcript A/B” header state alongside selection styling; color alone does not identify the command target. Readers expose actual text and read-only state; buttons expose names and enabled state; save status is textual. Validate light/dark and increased-contrast appearances with measured rendered colors, rather than assuming semantic colors prove contrast.

## Document and persistence state model

Assumption for this revision: UTF-8 plain-text input, with a versioned comparison file containing both text snapshots, filenames/source-location metadata, selection ranges, visible text anchors, active slot, text size, layout preference and divider ratios. No source write occurs. Saving a comparison makes it portable without depending on source paths. Reopening uses saved snapshots; replacement requires an explicit Open Transcript command. Unsupported format/encoding receives a readable error and format guidance. Wider format support is outside the supplied evidence.

A comparison can be saved with one slot empty. Opening/replacing either slot marks content dirty; presentation changes are persisted as session state without prompting on every scroll. Proposed comparison extension is `.transcriptcompare`; the chooser must show the format clearly and respect extension visibility preferences. It must permit name and location choice and browsing beyond a suggested folder.

```text
load(slot, file):
  read and validate into temporary storage
  on failure: retain old slot and focus; show persistent recoverable error
  on success: install snapshot; reset only that slot's range/anchor;
              focus slot; mark content dirty
save():
  if unnamed: request destination; cancel => retain dirty state and focus
  capture document revision and session state
  write safely, preserving previous saved file on failure
  on durable success: mark captured revision saved
  if edits occurred during save: remain dirty; schedule next save
  on failure: keep dirty; show "Couldn’t save" with Retry and Choose Location
```

After the first successful save, autosave content periodically (proposed two-second idle debounce) and flush on app deactivation and close. “Saving…” and “Saved” refer to actual operation state. Clear Edited only when the current content revision is durable. Do not display a dirty close dot merely because autosave is enabled; the local guide qualifies that cue for autosave being off.

For an unnamed comparison containing loaded text, Close/Quit offers Save, Discard Comparison, or Cancel. Discard affects only the comparison. If saving fails during close, retain the window and offer Retry, Discard Comparison, or Cancel; never close while claiming success. With autosave disabled, request saving on consequential exits and display unsaved cues. Named, successfully flushed comparisons close normally. Reopen restores snapshots and valid reading state, clamping ranges safely if format migration changes offsets. There is no remote sync in this design.

## Worked before/after

Illustrative fixture, not supplied research data: `Interview-A.txt` contains “The handoff took three days.” and `Interview-B.txt` contains “The handoff took one day.”

Before, the brief's forced single fullscreen transcript prevents seeing both statements together. Copy and Save require swipes, so a keyboard user has no specified completion route. Whether the current app actually loses selection or data is unknown.

After: Command-N creates a comparison. Open Transcript A… loads A; Open Transcript B… loads B. Both statements remain visible. View > Focus Transcript A targets A; keyboard selection marks “three days.” Command-C copies exactly that text. Focus Transcript B preserves A's inactive selection; selecting “one day” and Command-C copies B's phrase. Command-S names the comparison `Handoff comparison.transcriptcompare` in a chosen local folder. Resizing to 700 pt width stacks the readers while retaining their selections and anchors. Switching to another app and back retains B as target. Close and reopen restores both snapshots and reading state. No swipe or source modification is required.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** `interface.md` was read; the installed root skill, relevant family routes, topic procedures and local source guides were read. This document defines simultaneous comparison, resize adaptation, document ownership, scoped commands, keyboard completion, persistence failure/cancel paths and state preservation. All cited URLs identify official source sections from local guidance; no web pages were opened.

**Failed — brief-level requirements:** the supplied current design forces one fullscreen transcript, hides menu access and makes Copy/Save swipe-dependent. These conflict with the requested desktop workflow. This is a finding about the written brief, not a reproduced runtime defect.

**Not executed — implementation acceptance matrix:**

| Scenario | Required observable result |
|---|---|
| Keyboard-only worked example | Open A/B, reach both readers, select/copy each, save, cancel a chooser and close without a pointer; no system shortcut is intercepted. |
| Scope and multiple windows | Copy follows focused selection; Save writes the key comparison; opening an existing comparison activates its window. Closing one leaves the other intact. |
| Resize 1200 → 900 → 700 → 640 pt, then expand | No clipped essential control; both readers usable or explicit focus/reveal route available; ranges, anchors and wide ratio survive. Test short height and long filenames too. |
| Divider keyboard/pointer adjustment | Both pane bounds respected; value and orientation exposed; Equalize recovers useful proportions. |
| Long text, identifier and multiline selection | All text reachable, wrapping preserves exact copy content, one scroll owner per reader, selection extension makes minimal reveal. |
| Text at 200%, light/dark, Increase Contrast | Content and commands remain reachable; labels reflow; actual text/control contrast and activation geometry measured. |
| VoiceOver, Full Keyboard Access and Switch Control on Mac | Logical names/order, read-only text, active/inactive selection distinction, adjustable divider and complete task activation are verified independently. |
| Cancel/failed open or unsupported encoding | Existing content and comparison state remain intact; error persists until addressed; retry succeeds. |
| First save canceled, disk-full save, concurrent change during save | No false Saved cue; prior saved file preserved; dirty changes retained; closing cannot silently lose them. |
| Close/Quit/reopen and app switching | Cancel stops exit; saved snapshots and reading state restore; inactive/active window cues and input ownership remain correct. |
| Native Mac window/menu behavior | Move, resize, minimize, Zoom, optional full screen, system menu access and window switching behave conventionally, including on multiple displays. |

No GUI, Apple device, SDK compilation, filesystem durability, actual keyboard handling, assistive technology, rendered contrast, physical comfort or native integration was executed or established. The server is headless Linux; future interactive checks belong on the MacBook. The installed articles are dated local HIG-derived guidance, not SDK availability evidence or proof of independent source review. The brief provides no research corpus, so encoding coverage, transcript size/performance, researcher preferences, and adequacy of the chosen breakpoints/storage format remain to validate. No behavior was inferred from absent screenshots or code.
