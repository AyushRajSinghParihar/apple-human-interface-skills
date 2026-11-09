# Result

Patched interface.md in place, replacing the one-paragraph defect description with a concrete macOS progress, worker, cancellation, and recovery specification.

## Decisions

- Replace the fake initial 90% with an indeterminate scanning bar. Reuse its geometry for measured encoding and indeterminate finalization.
- Known input bytes support an explicitly scoped encoding-byte value, not an end-to-end percentage or ETA. Require actual encoder acknowledgments; otherwise stay indeterminate. Validation and output commit determine success.
- Isolate workers from the UI and each other; show a suspected-stall message after a proposed 30-second threshold, with wait, retry, skip, pause, and cancel paths.
- Make sources read-only. Cancel preserves completed outputs and recovery state, fences late commits, and offers Resume Unfinished. Disclose when unfinished files must restart.
- Specify failures, changed inputs, empty/zero-byte jobs, retries, skipped work, button states, keyboard access, and accessible progress meaning.

Apple guidance supports honest measurable progress, stable indicator shape, useful stall recovery, safe cancellation, and pause/resume where work would otherwise be discarded: [Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators). Background responsiveness follows [Loading](https://developer.apple.com/design/human-interface-guidelines/loading); action labels/roles follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons); perceivable states and input access follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). The formula, stall threshold, manifest, and worker/commit protocol are proposed implementation decisions. The local buttons guide gives a general 44 × 44 pt target while the accessibility guide gives macOS-specific 28 × 28 pt defaults and 20 × 20 pt minima; the specification conservatively retains standard Mac controls and separation without treating the smaller minimum as a target or asserting measured geometry.

## Worked before/after

Assume two files, A = 100 MB and B = 900 MB, using decimal units for this example.

| Event | Before, from supplied brief | Revised behavior |
| --- | --- | --- |
| Start, before scanning | Fake 90% | Indeterminate “Scanning files…”; no percentage. |
| Scan finishes | No honest measurement contract supplied | Manifest freezes at 1 GB. Encoding begins at 0 measured bytes. |
| A completes; B acknowledges 300 MB | No byte accounting supplied | (100 + 300) / 1000 = 40%; “Encoding input processed: 40% · 400 MB of 1 GB”; 1 of 2 files completed. |
| B stops reporting for 30 seconds | Entire window unresponsive | Keep 40%, identify B and its phase; window and recovery actions remain usable. |
| Cancel | Deletes sources | Stop/fence workers; retain both sources, completed A output, and recovery manifest. Show “Cancelled: 1 completed, 1 unfinished.” |
| Resume without checkpoint support | Unspecified | Keep A; disclose that B restarts. Start a labeled new attempt at 100/1000 = 10%. |
| B consumes remaining input, output still validating | Unspecified | Replace encoding percentage with indeterminate “Finalizing outputs…”; never claim job success from byte consumption. |
| B output validates and commits | Unspecified | Remove progress indicator; “Completed: 2 files.” |

## Acceptance checks and status

Passed — static specification review:

- interface.md now defines unknown-to-known phase transitions without fabricated percentages, including indeterminate fallback when byte acknowledgments are unavailable.
- Formula produces 40% for the worked example; zero denominator, repeated reads, retries, skipped files, and changed inputs have explicit handling.
- Completion requires validation and commit; failure, cancellation, and partial success have distinct terminal summaries with no lingering animated indicator.
- Stalls have an identified file, unchanged measured value, usable recovery actions, and an explicit asynchronous-worker contract.
- Cancel forbids source deletion and preserves completed work; commit races, late callbacks, pause/resume, and restart limitations are specified.

Failed — supplied baseline, as described in interface.md before editing: invented 90%, whole-window blocking on a stuck file, and destructive cancellation. These are brief-level findings, not observed application execution. No unresolved contradiction was found in the revised contract during static review.

Not executed — implementation acceptance checks:

1. Inject an unknown-duration scan, unavailable encoder byte telemetry, zero-byte files, and changing source sizes; verify the specified indicator states and accounting.
2. Hang one worker; verify the stall message at the configured threshold, continued independent work, scrolling/keyboard response, and nonblocking Retry/Skip/Cancel. Confirm old attempts cannot publish outputs.
3. Exercise cancel during scanning, encoding, and output commit; compare source hashes and existing destination files, inspect retained completed outputs/checkpoints, then resume. Test a format without checkpoints.
4. Inject scan, encode, validation, destination-conflict, and write failures; verify honest per-file states, retry paths, and terminal summaries. Verify successful completion removes temporary progress.
5. On macOS, verify native controls, keyboard/default activation, focus retention, assistive names/roles/values, 200% text enlargement, light/dark contrast, and activation geometry using the implemented UI and appropriate accessibility tools.

## Evidence limits and route audit

Only the supplied local interface.md and installed instructions/guidance were used. No web browsing occurred; official links above identify the source articles from the local references and were not fetched.

Explicitly read the installed apple-hig root SKILL.md, then searched references/topic-index.md for progress/loading/accessibility/buttons. Read each selected family SKILL.md and its routed topic procedure before its supporting article: Status → Progress indicators; Patterns → Loading; Menus and actions → Buttons; Foundations → Accessibility. All paths resolved under .agents/skills/apple-hig; every read used a separate cat or rg command for one file.

The evidence is a short behavioral brief and local guidance snapshot, not app code, SDK documentation, screenshots, logs, or measured runtime behavior. The deliverable repairs the specification only. No build, SDK, device, GUI, Accessibility Inspector, or assistive-technology execution is claimed. Worker cancellation, byte telemetry, checkpoint support, and atomic publication remain implementation obligations to validate.
