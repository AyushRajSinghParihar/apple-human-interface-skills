# Always On adaptation result

Patched interface.md in place, replacing its single paragraph with an active/dimmed specification, transitions, per-field rules, fallbacks and acceptance checks.

## Decisions

- Replace maximum brightness with system-managed dimming, preserving primary legibility and reducing secondary detail.
- Remove the repeating pulse; settle in-flight motion without delaying privacy redaction.
- Hide all private heart-rate history at wrist down while retaining a static recorded duration and status as useful workout context. Duration is a proposed field, not an observed existing metric.
- Preserve layout, viewport and workout identity; restore permitted details and active appearance on wake. Existing actions retain positions with unavailable appearances while dimmed; waking cannot invoke them.
- Use a timestamped recorded snapshot because dimmed refresh is not guaranteed. No live claim, ticking counter or fabricated value. Meaningful delivered corrections update in place.
- Interpret summary as a completed-workout surface. Save confirmation is separate from workout completion; no new session controls or sensor assumptions are introduced.

## Worked before/after

Illustrative data: a completed 32-minute workout, private heart-rate samples, confirmed save and last update at 10:42. These are example values, not measured data.

**Before:** Wrist down exposes full heart-rate history at maximum brightness with a second-by-second pulse. Refresh is not guaranteed, and no freshness or wrist-raise contract is defined.

**After:** Wrist down shows Workout summary, Workout ended / Saved, 32 min, Heart-rate details hidden, and Recorded summary · updated 10:42 in stable regions with no pulse. At 10:47 without new data, the timestamp remains 10:42. Wrist raise restores permitted history in the same region and normal active appearance. A failed refresh preserves the snapshot with Couldn’t update · last updated 10:42. Wake triggers no save or underlying action.

## Acceptance results

**Passed — static specification review:** The revised artifact contains active/dimmed pairs, complete heart-rate redaction, stable positions, motion settling, truthful snapshot handling, missing-data and save-status rules, restoration, rapid-transition handling, revoked-access behavior and Always On availability fallback. The worked scenario agrees with those requirements.

**Failed:** No static specification check identified as failed. Runtime conformance is unestablished.

**Not executed:** All runtime acceptance checks in interface.md, including device dimming/readability, privacy during transitions, tap/wrist wake, animation interruption, scheduling/energy behavior, refresh and persistence, sensors and permission revocation. No device, SDK compilation, GUI or accessibility execution occurred. These are pending implementation checks, not passes inferred from prose.

## Sources and evidence limits

Explicitly read the installed apple-hig root SKILL.md, searched its topic index, then followed family → topic procedure → supporting reference for Designing for watchOS, Always On, Privacy, Motion and Workouts. Paths resolved beneath .agents/skills/apple-hig/. Each instruction/reference read used a separate file command. No web browsing occurred.

Material provenance links from the local articles: [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices), [watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices), [Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts#Best-practices), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), and [Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices). These links were not fetched. The installed sources are dated derived guidance, not SDK documentation or independent certification. No conflict was identified in the selected passages.

The only product evidence supplied was one paragraph, with no implementation, screenshot, metric schema, device/OS version or measurements. Hardware support comes from the brief, not verification. Actual luminance, energy use, native transitions, physical readability, assistive-technology behavior and API availability remain unverified. An active workout session would require a separate recording-state contract.
