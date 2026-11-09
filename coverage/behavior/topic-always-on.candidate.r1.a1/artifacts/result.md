# Always On adaptation result

Patched `interface.md` in place, replacing the original single paragraph with a concrete watchOS state and field contract, privacy rules, update behavior, transitions, fallback states and acceptance scenarios. No application code was supplied or changed.

## Decisions

- Preserve a useful glance: duration stays primary while the full private heart-rate history becomes a same-frame placeholder. Workout duration is contextually useful; this does not make all health details appropriate for dimmed display. Stricter system privacy takes precedence.
- Remove the recurring pulse in both states. Settle any legacy in-flight motion when possible without delaying redaction. Use system transitions and an immediate reduced-motion path.
- Replace maximum brightness with system-managed dimming, dark background and reduced secondary fills, while requiring readable primary information.
- Preserve layout, workout identity, lifecycle, selection and scroll position. Wrist raise restores active contrast and authorized details in place.
- Treat dimmed data as a confirmed snapshot. An ongoing summary keeps an absolute last-update timestamp and coalesces permitted updates to at most once per minute. That cap is a product decision, not a promised system refresh interval. Completed summaries remain final. The original brief does not identify which lifecycle applies, so both are defined.

These decisions follow the locally read [Always On best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices), [watchOS guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), and [Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Providing-feedback). The local Always On guidance qualifies redaction by allowing expected workout context; the specification conservatively keeps duration and hides heart-rate history. No conflicting source passages were identified in the selected readings.

## Worked before/after

Illustrative ongoing workout fixture, not observed app data: at 10:20, elapsed duration is 24:36 and authorized history includes a 142 bpm sample.

| Moment | Supplied behavior | Revised contract |
| --- | --- | --- |
| Wrist lowers at 10:20 | Second-by-second pulse, full private history, maximum brightness | Static “Elapsed at last update 24:36”; “Last update 10:20”; “Heart-rate details hidden” in the history slot; dim secondary detail |
| No refresh through 10:25 | Refresh is not guaranteed; original paragraph supplies no freshness rule | Still 24:36 with last update 10:20; no invented ticks or samples |
| Wrist raises at 10:25 | No clear transition specified | Same route, frames and scroll position; normal active contrast; authorized history restored; cached timestamp retained pending refresh |
| Refresh fails | Unspecified | “Update unavailable · Last update 10:20”; cached duration retained |

A completed-workout fixture instead keeps its final duration and “Completed” label in both states, without a periodic refresh requirement.

## Acceptance checks and status

**Passed — static artifact review:** revised specification explicitly covers per-field redaction, retained useful context, stable slots, motion settling, primary legibility requirement, unavailable controls if present, stale snapshots, active restoration, authorization loss, disabled Always On, reduced motion and interrupted transitions. The required in-place patch and this decision record exist. These passes establish specification coverage only.

**Failed:** no revised-specification coverage failures identified. The original paragraph explicitly retained private history, bright presentation and repeated dimmed animation; those behaviors have been replaced in the contract.

**Not executed:** all runtime acceptance scenarios in `interface.md`, including actual dimmed readability, first-frame redaction, wrist/tap activation, update scheduling/coalescing, refresh failure recovery, control frame stability, rapid transitions, authorization changes, system privacy behavior and reduced-motion behavior. Also not executed: device, SDK compilation, GUI, accessibility/assistive-technology or energy measurements. No runtime pass is claimed.

## Audit and evidence limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly from disk before routing. Each instruction/source read used a separate `cat` command; a targeted `rg` command read the topic-index entries for Always On and Privacy.

Route consumed before supporting guides:

1. Getting started family → Designing for watchOS topic → its watchOS reference.
2. Technologies family → Always On topic → its Always On reference.
3. Foundations family → Privacy topic → its Privacy reference.
4. Foundations family → Motion topic → its Motion reference.

All paths resolve within the installed `.agents/skills/apple-hig/` package. The watchOS procedure routed this task onward to Always On; Always On routed exposure and settling decisions to Privacy and Motion. Sources identify retrieval as 2026-10-25; the Always On reference lists source revisions from 2022/2023. These are local application-guidance snapshots, not independently verified current Apple text or SDK documentation. Official links above are attribution only; no web browsing occurred.

The supplied project evidence was one paragraph, with no screenshots, implementation, framework, controls, OS version, device model or data schema. Duration and freshness slots are concrete proposed design choices; they are not claims about an existing screen. Exact rendering, supported APIs, system scheduling, native animation response, accessibility semantics and battery effects require implementation and supported-device validation. This work certifies neither security nor legal compliance.
