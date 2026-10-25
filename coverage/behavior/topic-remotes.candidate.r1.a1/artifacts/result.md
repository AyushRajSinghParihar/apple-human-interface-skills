# Revised Apple TV music queue interaction specification

This is a framework-agnostic design contract for tvOS. The supplied `interface.md` describes touch dragging, Menu exiting and deleting the queue, Play/Pause opening Search, disappearing focus on updates, and use of other supported remotes/controllers. No implementation or screen geometry was supplied.

## Decisions and source basis

| Supplied behavior | Revised decision | Basis |
| --- | --- | --- |
| Touch dragging is assumed | Every queue operation is reachable through directions and deliberate Select; replace required dragging with explicit move commands. | [Remotes — Gestures](https://developer.apple.com/design/human-interface-guidelines/remotes#Gestures), [Lists and tables — Best practices](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Best-practices) |
| Menu exits and deletes queue | Treat a remote's Back/legacy Menu as hierarchical Back. Leaving never deletes queue data. At app root, defer Home behavior to the system. | [Remotes — Best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices) |
| Play/Pause performs Search | Play/Pause controls active media. Search is a visible, separately activated destination. | [Remotes — Buttons](https://developer.apple.com/design/human-interface-guidelines/remotes#Buttons) |
| Focus disappears when queue updates | Preserve focus by stable queue-entry identity when that entry survives. Specify removal recovery according to input context below. | [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices) |
| Another supported input device may be used | Normalize available inputs into the same actions, show actual-device prompts, and preserve system-owned buttons. No touch capability is required. | [Game controls — Physical controllers](https://developer.apple.com/design/human-interface-guidelines/game-controls#Physical-controllers) |

The exact layout, action-page design, reorder transaction and recovery choices below are product decisions applying that guidance; Apple does not prescribe this particular queue design. Use system focus treatment when available; a custom renderer must provide equivalent clear focus and press feedback. Allow room for enlarged focused rows and imagery, and assess legibility from across the room. See [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices) and [Lists and tables — tvOS](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#tvOS).

## Screen, data and focus contract

Assumed hierarchy: Music → Queue → Track Actions. Search is another child of Music; its results are outside this specification. Back from Search returns to Music rather than whichever page happened to open it. Returning to Queue restores its saved position when possible.

Queue has a horizontal header of `Search` and `Play`/`Pause`, then a single vertical list of upcoming queue entries. Currently playing title and status are shown separately and are not an editable upcoming row. Each upcoming row shows ordinal, title, artist, and the cue “Select for actions.” An empty queue shows “No upcoming tracks”; the header remains reachable. A paused current track can exist with an empty upcoming list.

Each queue occurrence has a unique stable entry ID, separate from track ID: two occurrences of the same song remain independently targetable. Keep `currentMedia`, `playbackState`, `queueVersion`, ordered `entryIDs`, `focusedTarget`, and saved queue anchor separately. Merely focusing an entry never starts playback or changes queue order. Selecting a row opens Track Actions for that occurrence; `Play Now` explicitly starts it and consumes that occurrence from the upcoming queue after success.

Focus routes:

- First Queue entry: first upcoming row, or Search if empty. Reentry: saved surviving target and scroll position.
- Header: Left/Right moves Search ↔ playback button; outside edges stay put. Down enters the saved surviving row or first row. With an empty queue, Down stays in the header.
- List: Up/Down moves one row, scrolling it into view. Up from the first row enters the last focused header button, initially Search. Down at the last row stays there. Left/Right does not activate or reorder anything.
- Track Actions is a full-page child, not a hidden long-press menu. Its vertical buttons are `Play Now`, `Move Earlier`, `Move Later`, `Done`. Up/Down traverses available actions; boundaries stay put, Left/Right does nothing. Back and Done return to the owning queue row.

`Move Earlier` and `Move Later` move that occurrence by one adjacent position among upcoming tracks; the currently playing item is excluded. Each deliberate activation commits one move. Keep focus on the activated action while updating a visible preview and “Position N of M.” At an endpoint, show the unavailable action and reason (“Already first”/“Already last”), but exclude it from directional focus. If the focused action becomes unavailable because of the person's move, focus Done. Done is always reachable. Back leaves already committed moves intact; it does not imply rollback. No touch drag or hold gesture is needed.

Buttons use short action labels, separate targets, and immediate press feedback; focus is visibly raised/highlighted, pressed is momentary, unavailable is inactive, and playback status remains visible after focus leaves. Do not reuse the focus highlight as the playing indicator. These state distinctions follow [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS); labels and feedback follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). Exact dimensions require layout evidence and are not inferred from this brief.

## State-by-input mapping

| Logical input | Queue / Track Actions | Search / parent navigation |
| --- | --- | --- |
| Directional press, D-pad, supported stick movement | Move visible focus along the routes above; no playback or queue mutation. | Follow destination's visible navigation. |
| Remote swipe | Navigate/scroll predictably with corresponding focus feedback; stronger swipes may scroll farther. Never reorder. | Navigate visible content. |
| Deliberate Select press / controller primary activation | Activate focused row or labeled button only. Suppress duplicate dispatch from the same physical press. | Activate the focused destination action. |
| Back / legacy remote Menu / controller cancel | Track Actions → Queue; Queue → Music. Preserve queue and playback. | Search → Music; Music root → system Home. |
| Play/Pause, where present | Toggle the active media between playing and paused, in either page. No Search navigation or queue mutation. | Same while active media exists. |
| Incidental touch/contact | No activation, playback change or reorder. | No activation. |
| Hold Back; Home/logo | Preserve system behavior; never intercept for queue actions. | Same. |

With no active media, Play/Pause does nothing and the visible playback button is unavailable with “Choose a track to play.” Search opens only by Select on Search. Hardware Play/Pause and the visible playback button dispatch the same action. Do not remap a controller's Menu to remote Back: controller Menu opens a small playback/settings child page with visible Play/Pause and Done; cancel returns. This is a product application of the controller menu convention, distinct from a legacy remote's Menu button.

For conventional controllers, D-pad/stick select, A activates and B cancels; resolve equivalent semantic controls and glyphs from the actual supported profile rather than printing A/B universally. This screen has no peer sections, so shoulder navigation is unused; X/Y/triggers acquire no invented commands. Device switching retains focus, queue and playback and updates prompts. Disconnecting a controller leaves Remote navigation available without discarding state.

No electronic program guide is present. Do not capture guide/browse/page buttons for Search, queue paging, reordering or track skipping; preserve system routing to the default guide app. The source's page-button channel-change rule applies to channel playback, not an invented music-channel model. See [Remotes — Compatible remotes](https://developer.apple.com/design/human-interface-guidelines/remotes#Compatible-remotes).

The queue is a component-focus browsing surface, not a scrubber. Swipes here never seek. If a separate Now Playing seek surface is provided, press-then-swipe must enter scrubbing with a visible media-position relationship; a plain contact must not pause or seek. This specification introduces no seek UI or SDK dependency.

## Updates and operation resolution

```text
onQueueSnapshot(snapshot, inputContext):
    reconcile rows by unique entry ID, never by index or song title
    if focused target still exists and is available:
        keep that target; preserve its visible position where practicable
    else if removal occurs during discrete directional navigation:
        choose next available row at old index, else preceding row, else Search
        reveal target with visible focus
    else:
        clear stale target and hide indicator; save old index as recovery anchor
        show nonmodal "Queue updated" or "Track no longer in queue"
        on next direction: resolve nearest row at anchor, else Search
        reveal it; consume this event as recovery, without activation
        Select while no valid target performs no action
```

An asynchronous removal is not permission to jump to an arbitrary track. The conditional hide-and-recover rule preserves the source's distinction between disappearing targets during discrete navigation and other input. A routine refresh, append, or reorder that retains the focused ID must not hide focus. When the actions-page owner disappears asynchronously, show its title as unavailable, disable track commands, and retain Done (or use the same no-focus recovery if a focused command disappears). Done/Back returns to a surviving anchor or Search.

For Play Now and each move, capture entry ID and queue version. Validate against the latest order before commit. Serialize commands, commit each activation at most once, and never apply a stale index to another occurrence. If storage is delayed, show a pending label, prevent duplicate activation, and keep Back available. Back does not cancel an already submitted operation. On success publish the authoritative snapshot; on failure leave the authoritative order/playback intact and show a visible failure with a reachable Retry. Keep the pending command's stable identity across page exits. Retry revalidates it. These are product robustness decisions, not claims of a particular backend.

## Worked before/after

Illustrative fixture: song A is currently playing; upcoming entries are `[B1, C1, B2]`, where B1 and B2 are separate occurrences of song B. The user wants B2 before C1, then to leave the queue while music continues.

**Before (from the supplied brief):** the interaction assumes dragging. Menu exits and deletes the queue; Play/Pause unexpectedly performs Search. An update can remove the visible focus indicator. The brief does not establish any successful alternate-controller route.

**After (specified trace):** enter Queue focused on B1 → Down to C1 → Down to B2 → Select opens B2 actions with Play Now focused → Down to Move Earlier → Select commits `[B1, B2, C1]`. The preview reads “Position 2 of 3”; A continues playing. Back returns with B2 focused. A refresh retaining B2 preserves its focus. Back opens Music and preserves `[B1, B2, C1]`. Play/Pause pauses A without opening Search. The same trace uses directional input, primary activation and cancel on another supported controller.

If B2 is instead removed asynchronously, no different B occurrence is activated: hide stale focus, then the next direction restores C1 at the saved index (clamped to the remaining list); a subsequent deliberate Select opens C1 actions.

## Acceptance checks and evidence limits

These are implementation acceptance scenarios, not reported runtime passes.

| Check | Required observable result | Status |
| --- | --- | --- |
| Traverse header, every row, actions, endpoints and empty queue | Every enabled target reachable and escapable; no wrap surprises or focus trap. | Not executed |
| Duplicate-song reorder using fixture above | Only B2 moves; no drag required; A continues playing. | Not executed |
| Back from actions, Queue, Search, root; hold Back | Correct parent/Home behavior, queue preserved, no unintended deletion. | Not executed |
| Play/Pause playing, paused, no active media | Toggle active playback or no-op as specified; never Search. | Not executed |
| Rest/pass Remote; swipe list; deliberate Select | Incidental contact never activates; swipe navigates; press activates once. | Not executed |
| Append, reorder, refresh with focused ID retained | Same ID remains visibly focused; no playback change. | Not executed |
| Remove focused ID during discrete navigation vs asynchronous update | Nearby one-step recovery vs hidden stale indicator and explicit next-direction recovery. | Not executed |
| Remove owner on actions page; empty queue | Safe unavailable state and Done/Back route; Search remains reachable. | Not executed |
| Stale version, delayed commit, failure, repeated press, Back while pending | No wrong occurrence, duplicate mutation, or lost authoritative state; retry is reachable. | Not executed |
| Switch/disconnect actual supported remote/controller | Correct prompts and semantic actions; Remote remains usable. | Not executed |
| Guide/page/Home/logo buttons | No unrelated app interception. | Not executed |
| Television viewing and enlarged row imagery | Legible across room, focus apparent, no clipping or overlapping targets. | Not executed |

**Passed — static specification inspection:** all four supplied problem behaviors have explicit replacement contracts; controller alternatives, empty states, stable occurrence IDs, removal cases and exit routes are specified. The worked reorder yields the stated order by inspection. Required root → family → topic → source reads were completed from the installed package, including the topic-index search.

**Failed — supplied contract review:** `interface.md` explicitly assigns queue deletion to Menu, Search to Play/Pause, assumes touch dragging, and reports disappearing focus. These are brief-level findings; no runtime defect was reproduced. No execution check is reported as passed or failed.

**Not executed / unknown:** no Apple TV, Remote, controller, SDK, GUI, focus engine, accessibility traversal, television legibility, momentum or physical-comfort testing was performed. Supported controller models, exact visual layout, storage and playback implementation are unspecified. No claim of SDK compilation, native rendering, VoiceOver behavior or shipped compatibility follows from this document.

Evidence is limited to `interface.md` and installed apple-hig root, selected family/topic procedures and their local supporting guides (snapshot dated 2026-10-25). Official links identify the local guidance's source articles; no web page or media was fetched. The package contains derived guidance rather than an SDK reference or evidence of independent review. No newer-release behavior or API availability has been verified.
