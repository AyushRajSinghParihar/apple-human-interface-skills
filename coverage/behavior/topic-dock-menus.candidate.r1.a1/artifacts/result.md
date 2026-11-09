# Revised Dock menu interaction specification

## Scope and decisions

Target: a macOS podcast recorder. `interface.md` says the proposed Dock menu duplicates all editing menus, puts destructive session deletion first, and must support access to the current recording and recent sessions with windows closed. No implementation, session model, or screenshots were supplied.

Replace the custom section with a few task entry points. Keep editing and session deletion out of the Dock menu. This follows the recommendation to favor a few valuable background/windowless actions, with brief labels and alternate access in the app. Removing deletion here is a product decision; the cited Dock guidance does not categorically prohibit destructive commands. Existing deletion behavior elsewhere is outside this revision. [Apple: Dock menus, Best practices](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Best-practices)

The following are explicit design assumptions, not observations: one current recording session at a time; a stable session identifier independent of its title or path; durable recent-session metadata; closing a window does not itself stop an active recording. The implementation must support these contracts or resolve the model before shipping.

## Menu artifact

Custom section, in order, while the app is running:

```text
New Recording…
Show Current Recording
────────────────────────
Recent Sessions ▸
    <most recently opened session title>
    <next session title>
    …
```

The final `…` above denotes additional entries, not a literal menu command. Preserve system-owned Dock items, window entries, and their system-managed placement; do not recreate or suppress them. Use real menu separators and a real, single-level submenu, without decorative icons or custom keyboard equivalents.

| Item | Enablement and result | Alternate access |
| --- | --- | --- |
| New Recording… | Enabled when no recording or unfinished recording setup exists. Opens setup to choose the session and input; never starts capture on selection. Disabled during an active recording or pending setup. | File > New Recording…; visible New Recording… action in the session browser |
| Show Current Recording | Enabled for a recording, paused recording, or finalizing recording. Activates its session window. Disabled when no current recording exists. | Recording > Show Current Recording; visible current-recording entry in the session browser |
| Recent Sessions | Always openable. Lists retained recent sessions by last successful open, newest first. Choosing a title opens that session without starting playback or capture. | File > Open Recent, using the same data and resolver; session browser recent list |

If history is empty, the submenu contains a disabled `No Recent Sessions` item. Known missing targets remain listed but disabled until metadata is refreshed. Keep the retained history complete and scrollable; do not truncate it solely to meet an arbitrary menu length. Use recognizable titles, adding a date or short containing-folder name only to disambiguate duplicates; do not expose full paths. No checkmarks: these commands navigate rather than apply attributes.

The short verb labels, ellipsis for required setup input, grouping, dimmed unavailable items, and shallow submenu apply the local [Menus guidance](https://developer.apple.com/design/human-interface-guidelines/menus#Labels), [Organization](https://developer.apple.com/design/human-interface-guidelines/menus#Organization), and [Submenus](https://developer.apple.com/design/human-interface-guidelines/menus#Submenus). Recent naming/order and alternate menu-bar routes follow [File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu) and [App-specific menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#App-specific-menus). The particular labels and recording-state policy are product decisions.

## State, target, and window contract

| State when invoked | Required behavior |
| --- | --- |
| Running in background, current session window open | Show Current Recording activates the app and that exact window; restore it if minimized. Preserve recording progress, edits, and selection. |
| Running, all windows closed, recording active | Show Current Recording creates a view of the same session and recorder; do not allocate a new session or restart capture. |
| Running, no current recording | Show Current Recording stays visible and disabled. New Recording… opens setup even if no windows exist. |
| Setup already pending | New Recording… is disabled; the setup remains reachable through the app's window list. A repeated invocation already queued reuses and activates the pending setup. |
| Recent session already open | Activate its existing window, restoring it if minimized. If it is the current recording, reach the same live session. |
| Recent session not open | Load it by stable identifier and open one session window. Preserve other open sessions and unsaved work. |
| Target disappeared after menu opened | Activate the session browser and display “This session is no longer available.” Refresh history and disable the unavailable entry. Do not open a blank session, silently substitute another session, or delete recorded data. |
| App not running | Do not promise custom commands. Leave system launch behavior intact. After launch, use the running-state rules. Custom closed-app Dock support requires separate implementation evidence. |

For this revision, a session has one primary window; unrelated sessions can have separate windows. Repeated commands reuse the matching window rather than the last active window. Do not close other sessions to satisfy an open request. Use normal system window controls and activation behavior. This applies the clutter/context advice in [Windows, Best practices](https://developer.apple.com/design/human-interface-guidelines/windows#Best-practices); exact native window behavior remains to be tested.

Framework-agnostic dispatch contract:

```text
onDockMenuRequested:
    build from an authoritative state snapshot
    bind recent entries to session IDs, never title/index

onCommand(command, optionalSessionID):
    serialize session creation and opens by target ID
    re-read authoritative state                 // menu may be stale
    if command == NEW_RECORDING:
        if setup exists: activate existing setup; return
        if current recording exists: return    // stale disabled action: no capture change
        activate app; open single setup
        // Cancel: discard setup only; create no recording
        // Continue: hand off to visible recording workflow
    else:
        target = currentRecordingID if SHOW_CURRENT else optionalSessionID
        if SHOW_CURRENT and target absent: return
        if target cannot resolve: show unavailable state in session browser; refresh; return
        activate app
        reuse target window, or load target and create one window
        preserve recording engine and all other session contexts
```

Loading or finalization must never turn a navigation command into a second recorder. While a target is loading, coalesce further requests for that ID. On load failure, retain the underlying session, show the failure in the session browser, and allow retry. Menu opening itself has no session or recording side effects.

## Worked before/after

**Before, from the brief:** a recording continues while its window is closed. The user opens the Dock menu and encounters deletion first, followed by the editing catalog. The supplied proposal does not specify how to return to the live recording; editing commands depend on an absent editing context. No actual invocation or deletion was observed.

**After, specified example:** “Episode 42” is recording with ID `s42`; all windows are closed. The Dock menu shows New Recording… disabled, Show Current Recording enabled, and recent sessions below. Selecting Show Current Recording activates a window bound to `s42`; elapsed recording time continues and no new recorder is created. Selecting it again reaches the same window. Selecting recent “Episode 41” opens `s41` without stopping `s42`. If `s41` vanished after menu construction, the session browser explains its unavailability and no replacement session is created.

## Acceptance checks and audit status

**Passed — static specification review only:** the custom tree contains three entry points, no editing catalog or deletion command; every custom capability has a menu-bar and visible route; labels and enabled states are explicit; current/recent IDs, no-window behavior, repeated opens, and missing targets have defined outcomes. These passes assess this document, not an implemented app.

**Failed — supplied proposal against this revised contract:** duplicating all editing menus and leading with deletion fail the focused task-entry design. This is a finding about the supplied prose, not a runtime failure or an assertion that every duplicate violates HIG.

**Not executed — implementation acceptance checks:**

1. Close all windows during recording, invoke Show Current Recording from the background, and verify the same session/engine resumes visibility with uninterrupted captured audio and no duplicate window.
2. Test idle, recording, paused, finalizing, and pending-setup states. Verify the table's labels/enablement; cancel setup and confirm no session or audio capture was created.
3. Open a recent session twice, including when minimized and with another session active. Verify correct-object reuse, preserved edits, and normal activation. Coalesce rapid repeated opens during loading.
4. Remove a recent target after opening the menu. Verify the specified unavailable state, no empty session, no data deletion, and usable retry after recovery. Also test known-missing and empty-history states.
5. Verify menu-bar and visible routes invoke the same handlers with no windows, no editing selection, and hidden editor controls. Verify unavailable parents remain openable and disabled children do not execute.
6. On a Mac, verify system Dock entries remain intact; keyboard and assistive navigation reach the submenu and correct targets. Test long/localized and duplicate titles, complete scrolling history, normal window resizing/controls, and closed-app launch behavior. Custom menu actions must not be assumed available before launch.

## Evidence limits and source audit

Only `interface.md` and installed skill instructions/references were used. No web browsing occurred; Apple links above identify the official articles behind the local snapshot and were not fetched. Local source guides are dated 2026-10-25 and are guidance summaries, not SDK documentation or proof of implementation feasibility.

Read order: installed `apple-hig/SKILL.md`; supplied interface; menus-and-actions family; relevant topic-index rows; Dock menus and Menus topic procedures; menu-bar procedure; presentation family and Windows procedure; then their corresponding source guides. Each file read used a separate shell command. Package paths were resolved under `.agents/skills/apple-hig/`.

No code, recording engine, persistence layer, Apple SDK, device, GUI, native Dock, keyboard, or accessibility execution was available or tested. Runtime, audio continuity, native rendering, localization fit, and assistive-navigation outcomes remain unverified. This deliverable is a concrete interaction contract suitable for implementation in the project's chosen framework.
