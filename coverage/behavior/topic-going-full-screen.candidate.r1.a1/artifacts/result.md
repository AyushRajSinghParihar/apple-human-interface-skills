# Revised Mac focus-writing interaction specification

Scope: replace the behavior described in `interface.md`. That brief states that a custom overlay launches automatically, permanently hides system navigation, and discards window size on exit. These are supplied design facts, not independently observed runtime behavior. Writers must be able to concentrate, open notes, and export without losing their place.

## Decisions and source support

1. **Make entry voluntary.** A fresh launch opens an ordinary resizable document window; it never invokes fullscreen or focus mode automatically. Offer reduced chrome as **View > Start Focus Writing**, changing to **Stop Focus Writing** while active. This product decision implements optional concentration; it is not a claim that Apple prohibits all restoration of fullscreen sessions. For this revision, restore documents and ordinary window geometry across launches, but start focus writing off.
2. **Separate two choices.** Focus Writing reduces app chrome in either a normal window or fullscreen. Standard **View > Enter Full Screen / Exit Full Screen**, Control-Command-F, and the system window control all change the same window's fullscreen state. They do not toggle Focus Writing. Do not substitute a borderless overlay, maximize-to-screen operation, or custom display mode. Keep Zoom distinct. This follows [Going full screen — macOS](https://developer.apple.com/design/human-interface-guidelines/going-full-screen#macOS) and [The menu bar — View and Window](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu).
3. **Hide distractions, retain access.** Focus Writing hides secondary navigation and formatting chrome, preserves the editor and its familiar layout, and leaves commands in the menu bar. The system controls menu-bar/window-control reveal at the top edge and Dock reveal at its configured edge; do not intercept these or app switching. Honor system visibility preferences. There is no custom fullscreen exit overlay. These decisions apply [Going full screen — Best practices](https://developer.apple.com/design/human-interface-guidelines/going-full-screen#Best-practices).
4. **Keep task commands available.** File > Open… (Command-O) opens notes through the existing file-opening workflow. File > Export As… requests destination/format and exports the active document; the original stays open and the export does not open automatically. Commands remain available with app chrome hidden; disable document-dependent commands visibly when no document exists. Menu and any existing equivalent controls share action, target, and availability. See [The menu bar — File](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu) and [Designing for macOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices).
5. **Retain context and geometry.** Enter/exit changes presentation, not document identity. Preserve edits, undo history, selection/caret and visible text anchor; reflow may change a pixel scroll offset, so restore the same passage and caret visibility. Let standard fullscreen transitions manage geometry, retaining the prior normal frame as recovery state. Do not programmatically resize the window to simulate entry. On exit restore prior size and position when that display remains available; if it is gone, fit the saved frame within the current usable display bounds. Keep controls and text clear of camera housings and system regions. See [Windows — macOS](https://developer.apple.com/design/human-interface-guidelines/windows#macOS), [Layout — macOS](https://developer.apple.com/design/human-interface-guidelines/layout#macOS), and the fullscreen guidance above.

## State and transition contract

Per document window maintain independent values:

```text
presentation = windowed | entering | fullscreen | leaving
focusWriting = off | on
savedNormalFrame = frame + display identity
editorContext = document identity, live edits, undo history,
                selection/caret, visible text anchor
```

Fullscreen belongs to each window, not the application. Focus Writing is also per window. Changing either value never reloads the document. Normal editing remains enabled in both modes.

| Trigger | Required transition and result |
| --- | --- |
| Launch | Restore documents and usable normal frames; windowed, Focus Writing off. |
| Start Focus Writing | Preserve current context; hide secondary chrome; remain in current presentation. If a hidden control had input focus, return input to the editor without changing its selection. |
| Stop Focus Writing | Restore secondary chrome and its prior configuration; remain in current presentation. |
| Standard fullscreen entry | Save normal frame and text anchor; request host's standard fullscreen transition. Set fullscreen only on host confirmation. Focus Writing is unchanged. |
| Standard fullscreen exit | Request host's standard exit; confirm windowed only on host confirmation. Restore normal frame through host restoration, with display-loss recovery if needed; retain current text context and Focus Writing. |
| Entry/exit fails or is cancelled | Reconcile to host-reported presentation, retain edits/context, and update command labels. Never leave an invisible overlay or a falsely disabled exit command. |
| Repeated toggle during transition | Ignore duplicate requests until settled; do not queue alternating enter/exit requests. |
| Open a note | Retain the writing window and its full state. Open the selected note in an independent standard document window; reuse that note's existing window on repeated opens. New note windows start windowed with Focus Writing off. Commands target the currently active document window. Returning to the writing window restores its editing context. |
| Export As… | Capture the initiating document as the export target. Destination/format input, success, cancellation, or failure does not toggle fullscreen or focus mode. Cancellation changes no content; failure preserves the document and offers retry through the same command. Restore editor input after the workflow finishes. |
| Switch apps / activate another window | Retain presentation, focus mode and document state. Return to the same editing context; do not force fullscreen exit or re-entry. |
| Close | Use ordinary document close/save handling. Fullscreen exit alone never closes or discards a document. |

Framework-neutral host boundary:

```text
onFullScreenCommand(window):
    if transitionPending(window): return
    preserveLiveEditorContext(window)
    if host.isFullScreen(window): host.requestStandardExit(window)
    else:
        window.savedNormalFrame = host.normalFrame(window)
        host.requestStandardEntry(window)

onHostPresentationSettled(window, actualState):
    window.presentation = actualState
    reconcileMenuLabelAndAvailability(window)
    restoreTextAnchorAndSelectionWithoutReload(window)
```

The host operations are capability contracts, not SDK symbols. If the actual host cannot supply standard Mac fullscreen, retain usable windowed Focus Writing and disable the fullscreen command with an explanation; do not recreate the trapping overlay. No host capability has been established by this task.

## Input and command contract

Control-Command-F is reserved for fullscreen. Focus Writing has a discoverable View menu command with no new default shortcut in this revision. Export also has no new default shortcut; do not repurpose Command-E, which has established editing meaning. A keyboard-only route is: invoke the system menu-bar focus action, navigate View/File, and activate the named command; Command-O opens notes directly. Preserve normal text-editing shortcuts, app switching, and system accessibility shortcuts. These choices follow [Keyboards — standard and custom shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts).

Escape cancels an active composition, menu, or temporary workflow according to its owner. Do not globally bind it to close the document or toggle Focus Writing. Preserve the host's standard fullscreen Escape behavior when applicable; the guaranteed exit routes are the standard window control, View command, and Control-Command-F. Entering/exiting fullscreen while editing must preserve text selection. Native keyboard routing and Full Keyboard Access require Mac validation.

## Worked before → after

**Before, supplied:** The writer launches into a custom fullscreen overlay, cannot recover system navigation, and loses window size when leaving. The brief does not establish whether notes/export currently exist or how they behave.

**After, illustrative acceptance fixture:** The writer opens Draft A in a normal window at frame `(100, 80, 1000, 720)` in host logical coordinates, selects “the harbor,” and leaves paragraph 12 visible. They choose Start Focus Writing and then Control-Command-F. Secondary chrome disappears; the same document enters standard fullscreen. Moving to the top reveals the system menu bar and window controls. File > Open… opens Notes B in another window. Draft A stays intact and fullscreen. Returning to Draft A restores the selection and passage. File > Export As… exports Draft A; cancelling the destination prompt leaves it unchanged. Control-Command-F exits fullscreen to the original frame on the unchanged display, with paragraph 12 and the selection retained. Focus Writing remains on until the writer chooses Stop Focus Writing. Switching apps at any point preserves these states.

## Acceptance checks and evidence status

**Passed — specification inspection only:** the artifact defines voluntary entry, separate focus/fullscreen state, standard entry and exit, hidden-chrome command access, note/export targeting, context/geometry restoration, interruption and failure handling. Installed root, selected family routes, topic procedures and their references were read locally in that order; the topic index was searched for macOS, fullscreen, windows and keyboard concepts.

**Failed — supplied current behavior against this specification:** automatic overlay entry, permanently hidden system navigation, and discarded window size. These failures derive only from `interface.md`; no runtime reproduction was performed.

**Not executed — implementation acceptance checks:**

| Check on a Mac implementation | Pass condition |
| --- | --- |
| Launch and independent modes | No forced fullscreen/focus entry; all four windowed/fullscreen × focus off/on combinations are usable. |
| Standard entry, reveal and exit | Window control, View command and Control-Command-F agree; top-edge reveal, Dock access and system switching work without traps. |
| Keyboard-only task | Enter, open a note, return, export/cancel, and exit without a pointer; Full Keyboard Access reaches all relevant controls. Ordinary typing and editing shortcuts retain their meanings. |
| Context and interruptions | Edits, undo, selected text and visible passage survive app switching, note-window activation, repeated entry/exit and export completion/cancellation/failure. |
| Multiple documents | Export from each active document uses that document; repeated note opens reuse the correct note window. No cross-document selection or state leakage. |
| Geometry and environments | Same-display exit restores frame; disconnected-display recovery leaves a reachable window. Test small/large and intermediate window sizes, longer localized labels, increased text settings, multiple displays and a camera-housing display; essential actions never depend on a bottom edge or obstructed region. |
| Transition recovery | Rapid toggles, rejected/cancelled transitions and host state changes settle to truthful labels and reachable controls without lost edits. |
| Close/reopen | Normal save/cancel behavior remains intact; reopening restores document/normal geometry under the stated launch policy. |

Media completion, playback pause and time-sensitive content checks from the fullscreen procedure are not applicable to the supplied writing-only brief; no media behavior is inferred.

## Evidence limits

Only `interface.md` and the installed apple-hig package were used. Guidance is a local derived HIG snapshot, dated 2026-10-25 for the principal fullscreen/window/menu sources; linked official pages are provenance links and were not browsed or verified live. No conflicting source instruction affected these decisions; the menu guide's unrelated custom-menu ordering ambiguity was not used.

This is an interaction specification, not implemented code. No Mac device, GUI, Apple SDK, build, native fullscreen transition, accessibility tool, VoiceOver, Full Keyboard Access, international keyboard, camera-housing layout, or multiple-display behavior was executed or validated. Linux file inspection establishes the written contract only. Host/API feasibility and the runtime acceptance checks remain to be demonstrated in the chosen stack on the user's MacBook.
