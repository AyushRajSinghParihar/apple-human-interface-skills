# Result

Patched `interface.md` in place, replacing the original single-paragraph behavior with an implementable active/dimmed state contract, per-field exposure rules, appearance rules, refresh/failure handling, state restoration, and acceptance scenarios.

## Decisions

- Keep recorded duration useful at a glance; redact the full private heart-rate history, including derived values and chart shapes, in its existing frame. This applies Always On's contextual allowance for useful workout metrics without treating it as permission to expose all health detail.
- Remove the recurring pulse; use system-managed dimming, reduced secondary emphasis, and a stable primary metric. Apply privacy changes immediately, independently of cosmetic settling.
- Restore detail and active emphasis on wake in the same workout, history range, and viewport. Retain control positions if controls exist; the supplied artifact names none.
- Treat “summary” as a completed workout. Preserve confirmed recorded values without depending on dimmed refresh; distinguish pending reconciliation and failure from final data. This is an explicit product assumption because the brief gives no session lifecycle or data model.
- Introduce no health-data access or collection changes. No framework, API, OS minimum, exact animation duration, brightness percentage, or refresh guarantee is asserted.

Material guidance: [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices), [watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices), [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), and [Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices). These are attribution links from local snapshots, not browsed evidence. The exact retained metric and status copy are application choices, not universal Apple requirements.

## Worked before/after

Illustrative fixture, not actual workout evidence: recorded duration 32 min; private heart-rate history selected for the final 10 min; summary reconciliation pending.

| Event | Before, supplied behavior | After, revised contract |
| --- | --- | --- |
| Wrist lowers | Full private history remains at maximum brightness with a second-by-second pulse | Same viewport; “Recorded duration 32 min” remains legible; history becomes “Heart-rate history hidden”; secondary content dims and motion rests |
| No refresh is delivered | No defined freshness handling | Duration stays 32 min; status says “Updates on wrist raise”; no ticking or live implication |
| Wrist raises | No clear transition | Normal emphasis and permitted history return in place, preserving the final-10-min selection; status says “Summary updating” while pending |
| Reconciliation fails | Unspecified | Retain confirmed recorded data and show “Update unavailable” |

## Acceptance audit

**Passed — static specification review:** the patch defines both wrist states, per-field redaction, stable layout, useful primary information, no recurring pulse, refresh starvation, wake restoration, failure handling, privacy precedence, and disabled-Always-On fallback. The before/after fixture can be traced through the specified transitions without requiring a dimmed update.

**Failed — supplied baseline against the revised contract:** the original explicitly exposes private history, requests maximum brightness, repeats motion, and lacks a clear wake transition. Its refresh uncertainty has no defined presentation fallback. These are findings about supplied prose, not observed runtime defects.

**Not executed — implementation acceptance:** all hardware/runtime scenarios in `interface.md`, actual dimmed readability and energy behavior, transition-boundary privacy, system-setting behavior, Reduce Motion response, accessibility/assistive-technology behavior, sensor correctness, SDK compilation, and GUI rendering. No app implementation, simulator, device, screenshot, or measured runtime evidence was supplied or exercised.

## Evidence and routing limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, then the Getting started family and Designing for watchOS procedure before its reference. Searched relevant rows in the complete topic index. Read the Technologies family and Always On procedure before its reference; followed its Privacy and Motion routes through the Foundations family and their procedures before their references. Read the Patterns family and Workouts procedure before its reference. Each instruction/source read used a separate single-file `cat` or `rg` command.

All guidance came from this installed package and the supplied `interface.md`; no web browsing occurred. The local references describe themselves as derived guidance, with snapshot retrieval dates of 2026-10-25 and source revisions of varying ages. Their presence does not establish independent source or media review. HIG supports the design direction but is not an SDK availability reference. Supported hardware is a supplied constraint; exact OS/API eligibility and system background behavior remain implementation verification work. No conflict requiring an alternative rule was found in the passages read.
