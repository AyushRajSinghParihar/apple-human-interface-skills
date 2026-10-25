# Result

Patched `interface.md` in place, replacing the short problem statement with a concrete iPadOS continuity specification. No application code was supplied or changed.

## Decisions and patch summary

- Separate durable document data, comparison workspace state and per-window context. Journal edits incrementally and restore drafts before recomputing comparisons; background callbacks alone are insufficient.
- Replace narrow-window closure with a single-editor document switcher, retaining both editors' state. The proposed 320 pt per-editor threshold is a product starting point requiring layout validation, not an Apple minimum.
- Define resize, focus loss, backgrounding, task completion, window closure, process recovery and failure behavior separately. Background work is bounded by system permission and can resume on return.
- Support independently editable document windows where available, explicit open/reuse semantics, shared revisioned document data and isolated window context. Provide an in-window fallback.
- Restore silently. Because no audio purpose was supplied, default to no audio; define a conservative explicit-resume policy if an existing read-aloud feature remains.

Guidance supports continuity, adaptation, parallel windows and respect for audio intent. The journaling model, breakpoint, duplicate-window policy and exact resume policy are design decisions added here. Official article links and applicable sections are recorded in `interface.md`.

## Worked before/after

Start comparing A and B. In A, edit paragraph 12 and leave the caret after the new sentence; in B, select a difference near paragraph 20. Narrow the window, switch to another app, then return and widen it.

Before, the supplied brief says narrowing closes the app, backgrounding clears edits and return starts audio. It provides no evidence of the exact original caret or comparison behavior.

After, narrowing shows A alone with A/B switches. A's sentence, caret and Undo remain; switching to B restores its selected difference and position. Backgrounding journals the edits and checkpoints both contexts. Return restores the same workspace silently; widening reveals both documents at their retained locations. An unfinished comparison recomputes from current revisions. Opening B in a dedicated window leaves A editable; closing B's window leaves A and B's draft intact. A later process restart recovers the latest durable checkpoint and journal, with playback paused.

## Acceptance checks

These are implementation acceptance scenarios, not executed test results.

| Scenario | Required observation |
| --- | --- |
| Repeated narrow/wide resize and rotation during editing | No closure, missing draft, reset selection/undo, or audio; both positions return |
| Layout at smallest/largest supported bounds and intermediate sizes, keyboard present/absent | Editing and A/B/difference actions remain reachable; no system-control overlap; validate proposed threshold with longer filenames and enlarged text |
| Switch apps and switch A/B windows repeatedly | Same route, drafts and positions; keystrokes and Undo affect only active document |
| Background during save/comparison; suspend before completion | Durable edits recover; interrupted task resumes/recomputes; stale result never labeled current; no routine notification |
| Terminate after a confirmed journal write, then relaunch | Latest durable edit and workspace recovered; no automatic playback |
| Simulate persistence failure or missing file | Draft retained, honest failure state and retry/relink; no silent replacement |
| Open A and B independently; repeat Open; close and reopen B | Correct document reuse, no duplicate buildup, A unaffected, B restored; same-document edits propagate through revisioned model |
| Run where separate windows are unavailable | Both documents remain independently editable through the switcher |
| Return when previously silent or paused | No sound or playback-session activation |
| If read-aloud exists: background, headphone disconnect, sustained audio, brief interruption | Position retained; sustained/route/background pauses require Play; temporary ducking never becomes an unauthorized resume |
| Touch-only and attached keyboard operation | Same essential operations available; target follows active editor; accessory changes retain state |

## Audit and evidence limits

Passed (static specification checks): the original brief was read; `interface.md` was edited; each supplied failure now has a replacement contract; independent document windows and fallback are specified; acceptance cases cover normal and interrupted paths. The installed root SKILL.md was explicitly read, then topic-index rows were searched. Routes consumed, each using a separate single-file command:

- Getting started family → Designing for iPadOS procedure → local Designing for iPadOS guide.
- Patterns family → Multitasking procedure → local Multitasking guide.
- Foundations family → routed Layout procedure → local Layout guide.
- Presentation family → routed Windows procedure → local Windows guide.
- Patterns family → routed Playing audio procedure → local Playing audio guide, including its category table.

All paths resolve under `.agents/skills/apple-hig/`. Procedures were read before their supporting guides. No web browsing occurred.

Failed checks: none observed at the specification level. The three original failures are reported by the brief, not reproduced here.

Not executed: builds, SDK/API availability checks, automated app tests, native lifecycle/background execution, file recovery fault injection, device window management, GUI rendering, audio routing, keyboard/focus behavior, accessibility or assistive-technology execution. No app implementation, deployment target, device evidence or actual audio configuration was supplied. Local guides are a dated independent HIG snapshot, not an SDK reference; official links were not fetched. Runtime acceptance and the proposed layout threshold remain unverified.
