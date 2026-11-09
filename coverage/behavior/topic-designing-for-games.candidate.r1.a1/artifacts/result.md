# First playable minute: Match Pairs

## Scope and decisions

`interface.md` supplies iPhone and Apple TV as targets, mandatory tutorial reading, color-only tiles, universal touch dragging, purchase on loss, and short resumable sessions. It supplies no puzzle rules, screens, implementation, prices, or asset measurements. The following pair-matching rule set is a proposed concrete first level, not an inferred description of the prototype. It preserves the supplied tile-puzzle concept. No Apple SDK is assumed.

1. Open directly into a locally bundled, playable six-tile board. A one-sentence instruction sits beside play; no tutorial page, account, permission, download, rating, or purchase blocks the first move. Tips can be hidden, remembered across launches, and reopened from Pause → How to play. This applies [Games: Jump into gameplay](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Jump-into-gameplay) and [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding). The precise board and timing below are product decisions.
2. Replace dragging with two explicit activations: choose a tile, then choose its matching shape. Color remains optional decoration; circle, triangle, and square silhouettes plus visible names convey identity. This addresses the supplied color barrier using [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).
3. Use iPhone touch and Apple TV remote as complete default routes. No controller is required. Directional focus never selects a tile; Select does. This follows [Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls), [tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos), and [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection). The latter's component-focus model is not asserted for iPhone touch or VoiceOver.
4. A mismatch is recoverable, with no lives, countdown, paid retry, or automatic dismissal. No purchase screen occurs in this minute or on a failed attempt. Optional future commerce needs a separately specified voluntary store; no product type or entitlement is invented here. Showing value before shopping is source-backed; free retries and removing monetization from this minute are product decisions, not claimed universal purchase rules. See [In-App Purchase: Best practices](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase#Best-practices).
5. Save after every action that changes play. Resume exactly where the person stopped. Local resume is required; cross-device sync is outside this specification. This serves interrupted [iPhone use](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios).

## Play contract and first-minute sequence

All six tiles are face up; this tests matching rather than memory. Initial board, in stable row/column coordinates:

| | Column 1 | Column 2 | Column 3 |
|---|---|---|---|
| Row 1 | Circle A | Triangle A | Square A |
| Row 2 | Triangle B | Square B | Circle B |

Match all three pairs. There is no adjacency requirement and no time limit. Matched cells keep their place as noninteractive “Matched” markers so the board never collapses around focus.

Times below are intended pacing after the board becomes interactive, not measured launch performance or deadlines. Every step may take longer than a minute.

| Intended time | Visible state and action | Result |
|---|---|---|
| 0–10 seconds | Heading “Match Pairs”; “Match the same shapes. Choose a tile, then its partner.” Progress “0 of 3 pairs.” First tile ready to activate. Controls: Pause, Hide tips. | Immediate meaningful input, no Start gate. TV prompt: “Press Select to choose.” iPhone: “Tap to choose.” |
| 10–25 seconds | Activate Circle A; instruction becomes “Circle selected. Choose another circle.” Activate Circle B. | Both become “Circle — Matched”; progress “1 of 3 pairs.” Persistent status “Circle pair matched.” |
| 25–45 seconds | Find triangle pair. A mismatch is permitted; see worked example. | Same rules and accessible status; no new instructions required. |
| 45–60 seconds | Finish square pair, or pause at any point. | Completion says “3 of 3 pairs. Puzzle complete.” Explicit Next puzzle and Replay controls; no automatic advancement or store. If unfinished, play continues indefinitely. |

Hide tips removes optional coaching, not the goal, progress, tile names, current selection, or result messages. “How to play” from Pause shows the same short rule and “Show tips” / “Return to game”; it never resets the board. Skipping coaching persists until the player explicitly restores it. Completion remains visible until an action. Next puzzle loads a second bundled board with the same rules (row 1 Square, Circle, Triangle; row 2 Circle, Triangle, Square). Replay restores the initial board and clears pair progress only after that deliberate action.

## State and transition specification

Framework-agnostic model:

```text
save = { version, levelId, tileIdsAndShapes, matchedIds,
         selectedIdOrNull, tipsHidden, lastBoardTarget,
         resultText, phase: playing | completed }
ui = { screen: board | pause | help, previousTarget }

activateTile(id):
  if phase != playing or id is matched: no mutation
  else if selectedId is null: select id; result = "[shape] selected"
  else if selectedId == id: clear selection; result = "Selection cleared"
  else if shape(id) == shape(selectedId):
    mark both matched; clear selection
    result = "[shape] pair matched. [count] of 3 pairs"
    if count == 3: phase = completed
  else:
    clear selection
    result = "Different shapes. Choose a tile to try again"
  commit complete save atomically before publishing new state
  render values and publish one relevant accessibility status update

pause / system interruption:
  preserve board, selection, progress, tips and last target
  pause opens menu; backgrounding does not run any game actions
resume:
  validate save; restore board and context, never replay an activation
```

Actions are serialized; repeated activation events must not race or match a tile with itself. A failed persistence commit leaves the previous committed board active and shows “Progress could not be saved. Try again” with a Retry save action; keep the pending transition in memory. Retry commits it once. Do not claim unsaved changes will survive process termination. Use atomic replacement so interrupted writes retain the last valid save. Missing save starts level one; unreadable/version-incompatible save offers Retry loading or an explicit Start new game, without silently overwriting recoverable data.

Pause menu: Resume, How to play, Text size, Return to game menu. Text size offers 100%, 150%, 200% and follows a larger supported system preference when available. Return to game menu preserves the save and offers Resume and How to play there. Back at that TV root returns through system navigation. Resume never requires payment. Starting another level commits a fresh state only after Next puzzle; focus changes, scrolling, and reading never change puzzle state.

## Platform inputs and focus

| Action | iPhone | Apple TV |
|---|---|---|
| Navigate tiles | Direct touch; accessibility exploration navigates without selecting | Directional clickpad/swipe moves one visible board target; directional presses supported |
| Choose / clear chosen tile | Tap / standard assistive activation | Deliberate Select press; incidental surface contact does not activate |
| Pause | Labeled Pause button | Back during play or labeled Pause; Play/Pause also toggles pause for this game |
| Resume | Resume button | Select Resume or Back from pause |
| Help return | Return to game | Return to game or Back returns to pause |

TV initial focus is row 1 column 1. Within board: arrows follow coordinates, skip matched markers in that direction, and never wrap. If no unmatched tile exists before a horizontal edge, stay put; Up from the top edge reaches Pause. Down from the bottom edge reaches Hide/Show tips. Down from Pause returns to the last unmatched board target; Up from tips does likewise. From any row, repeated Up can reach Pause and repeated Down can reach tips. Menu controls form vertical lists, with no traps. Back from any board state opens pause without clearing selection. Holding Back and Home remain system-owned. No focus-only event changes context.

When a successful activation makes the focused tile unavailable, move to the nearest remaining unmatched tile by grid distance, breaking ties in row order; this is a deliberate-activation consequence. On completion, focus Next puzzle, with Down to Replay and Up to Pause. Restore the prior target after menu dismissal, or the nearest valid one if unavailable. Selected means an inset check and text “Selected”; focus means an external outline/platform focus treatment; pressed means immediate boundary feedback. Those meanings remain distinct when focus moves. Reserve space for TV focus treatment without obscuring neighboring names. Reduce Motion uses a static outline with no scaling/parallax. The first minute otherwise uses immediate state changes, no flashing or celebratory animation. These choices apply [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive) and the TV focus guidance; actual system integration remains untested.

Optional controller support, if implemented: D-pad moves targets; primary activation selects; cancel follows Back; Menu pauses. Prompts must use the active controller's actual glyphs. Disconnect pauses and restores remote/touch prompts without losing state. The first playable minute must work with no controller connected. These mappings follow [Game controls: Physical controllers](https://developer.apple.com/design/human-interface-guidelines/game-controls#Physical-controllers).

## Presentation and accessible semantics

Use semantic heading, body, button, and status roles. Start essential text at 17 pt on iPhone and 29 pt on TV, regular or semibold; titles are larger. These are source defaults, not universal minima. Support at least 200% text enlargement and Bold Text. Wrap instructions, grow controls, and permit scrolling without hiding essential actions. Keep tile coordinates stable: if a three-column board cannot fit enlarged names, present six full-width tile buttons in row order, each including its original coordinate. TV then uses Up/Down along that list, Up to Pause and Down to tips. No puzzle depends on spatial adjacency. Preserve selection and focus identity through orientation or layout changes. See [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

iPhone activation areas are at least 44 × 44 pt for every control; TV controls start at 66 × 66 pt. Allocate 12 pt gaps as a product starting point, enlarging where necessary for legibility and TV focus. Fit the board within safe areas; frequent iPhone tile actions occupy the middle/lower region. Both phone orientations retain state. The games source has a 28 pt iOS table minimum but 44 pt touch prose; this specification conservatively uses 44 pt, consistent with frequent game-control guidance. See [Games: Displays](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Look-stunning-on-every-display).

Use opaque backgrounds, readable text, and outlined shape silhouettes; avoid text over tile tint. Specify a product contrast target of at least 4.5:1 for all essential text and 3:1 for essential shape/state boundaries in every appearance, including focused and pressed states. These targets still require measured palette selection. They do not reproduce the local HIG contrast table as a universal conformance rule. Offer a monochrome high-contrast treatment and honor Increase Contrast. Sound is optional reinforcement; every result has persistent visible text and semantic status. No task requires hearing, speech, haptics, fast responses, or dragging.

Accessibility reading sequence: heading → goal → progress → current status → board group in row order → Pause → Hide/Show tips. Each unmatched tile is a button named, for example, “Circle, row 1, column 1”; state value is “Available” or “Selected”; hint “Choose this tile” or “Clear selection.” Matched markers expose “Circle, row 1, column 1, matched” as static content. Decoration is hidden. Progress and states update together; announce the result once without repeating the whole board or interrupting exploration for every focus move. Reading/exploring never activates. On return, restore the previous accessible element where valid. All menu and recovery actions have function names and standard activation semantics. This is the intended semantic contract under [VoiceOver: Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover); no spoken output is claimed to have executed.

## Worked before → after

**Before, supplied:** A new Apple TV player must read a long tutorial, identify tiles by color, and drag them. Losing forces shopping. The brief establishes those barriers; it gives no exact tutorial duration, geometry, or actual losing sequence.

**After, proposed TV walkthrough:** Focus Circle A and press Select: its value becomes Selected. Move Right to Triangle A: Circle remains selected while Triangle has focus. Press Select: neither matches; both remain available, selection clears, and persistent status says “Different shapes. Choose a tile to try again.” Focus remains Triangle A. Press Select again, move Down to Square B then Left to Triangle B, and Select. The triangles become matched; progress reads 1 of 3. Focus moves to the nearest unmatched tile. Pause with Back, then resume: the matched triangles, status, and target survive. Match Circle A with Circle B and Square A with Square B to complete; Next puzzle is offered without a purchase gate.

**Equivalent nonvisual iPhone route:** Navigate by the named tile buttons, activate Circle A and Circle B using standard assistive activation, hear the proposed “Circle pair matched. 1 of 3 pairs” update, and continue with triangles and squares. A touch player taps the same identities. Neither path needs color recognition or a drag. These are specification walkthroughs, not device tests.

## Acceptance checks and evidence limits

**Passed — document inspection only:** The supplied brief was read. The installed root skill, selected family skills, routed topic procedures, and supporting local guides were read in that order by explicit paths. The topic index was searched. The proposed board has exactly two of each shape; the worked triangle route and three-pair completion are consistent with its coordinates. Both platforms have a specified complete default-input route, recovery, and resume contract.

**Failed — supplied design requirements, based on the brief:** Mandatory long reading blocks play; color-only identities exclude a noncolor route; touch dragging does not provide Apple TV's remote route; losing diverts recovery to purchase. These are brief-level findings, not observed runtime failures. No revised implementation was tested or failed.

**Not executed — required implementation acceptance checks:**

| Scenario | Pass condition |
|---|---|
| Fresh install offline | First board and help work from bundled content; first activation needs no setup, purchase, or network. Measure launch-to-interactive and first-match time separately; do not count passive tutorial viewing as play. |
| Skip and return | Hide tips, terminate, relaunch: tips stay hidden; goal and status remain; How to play restores tips without resetting progress. |
| Input parity | Complete all three pairs on iPhone touch and TV remote with no controller, drag, color, or sound; repeat via supported assistive navigation and activation. |
| Error recovery | Same tile twice clears selection; mismatch consumes no progress or money; matching twice cannot double-count; result remains until superseded by an action. |
| Focus traversal | Exercise every direction, matched-cell skip, menu entry/exit, completion and return. Every action is reachable, focus is visible and distinct from selection, no clipping or unexpected activation occurs. |
| Interrupt and resume | Interrupt with a tile selected, after a mismatch, after a match, in pause and on completion; restart restores the last committed board. Failed save and corrupt-save routes preserve recoverable data and expose labeled recovery. |
| Readability | At all supported text sizes through at least 200%, Bold Text, both phone orientations and TV viewing distance around 8 feet or farther, all names/actions remain readable and reachable; verify alternate list and focus routes. |
| Sensory preferences | Measure light/dark and increased-contrast palettes against the product targets. Test monochrome, muted audio, Reduce Motion, and relevant flashing preferences; completion meaning remains. |
| Accessibility runtime | On supported Apple environments, inspect actual names/roles/values/order, then complete using VoiceOver and applicable Switch Control, Voice Control, Full Keyboard Access and AssistiveTouch routes; preserve system shortcuts. Verify real announcements and focus restoration. |
| Commercial boundary | Mismatch, replay, restart and resume never invoke shopping; no paid retry entitlement is required. Any later store requires its own offer, restore, cancellation and entitlement verification. |

Only the local brief and installed dated HIG snapshot informed this artifact. Official links above identify the locally supplied sources; they were not opened online. No SDK, engine, GUI, device, remote, controller, screen reader, Accessibility Inspector, contrast calculator, storage implementation, or transaction was executed. Geometry, contrast, comfort, real launch duration, persistence and accessibility behavior remain unverified. Local reference existence does not establish independent source review or current commercial eligibility. This file is an implementable design proposal, not a conformance certification or a claim of shipped accessibility support.
