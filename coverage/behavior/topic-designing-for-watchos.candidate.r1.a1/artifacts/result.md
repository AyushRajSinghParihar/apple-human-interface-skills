# Watch-first equipment inspection — revised interaction specification

## Decisions and scope

The Watch owns identifying the assigned equipment, recording a short sequence of observations, and saving an inspection result. Replace the duplicated 40-field phone form with one check at a time. The serial number is prefilled; long explanations and administrative editing belong in a separate detail workflow. The inspection itself works without a live phone connection once its assignment and template are cached.

Evidence supplied: `interface.md` describes watchOS, a 40-field phone-form copy, required serial-number typing, a completion action below an article, gloves, and brief wrist raises. No actual fields, equipment type, inspection protocol, implementation, or screen geometry were supplied. Therefore the six checks and equipment below are illustrative fixtures, not an approved equipment procedure. Before implementation, a domain owner must map all 40 fields to prefilled metadata, required observations, conditional follow-up, or administrative detail. Never silently discard a required inspection measurement to meet the time target.

90 seconds is a usability target for a valid short inspection, including looking at the equipment. It is not a deadline, automatic pass, or permission to omit checks. If the approved protocol cannot fit, retain its requirements and revise the target.

These product choices apply the local [watchOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices): useful information and action together, shallow navigation, few gestures, and independent Watch utility. Apple does not prescribe six checks or a 90-second workflow.

## Screen and navigation contract

Use a vertical, single-column layout with a stable action area. Respect system time and safe areas. Put the task and response above optional explanations. No custom corner controls, hidden swipe commands, long press, typing, speech, or double-tap gesture is required.

| State | Visible information | Actions and transitions |
|---|---|---|
| Ready | Equipment short name, location, full prefilled serial, template name/version, “About 90 seconds” | Full-width **Start Inspection** confirms the displayed identity and creates a draft. **Change Equipment** opens cached assignments; **Equipment Not Listed** preserves context and explains how to arrange the assignment elsewhere. Never guess identity or offer a false match. |
| Check i of N | Equipment short name; “Check i of N”; concise approved criterion; current result, initially “Not checked” | Equal-height, full-width **Pass** and **Issue** buttons record an observation. **Cannot Check** records inability separately. Successful durable recording advances to the next unanswered check. **Previous** returns to the preceding check. **Details** opens optional item guidance with **Back to Check**. |
| Last check recorded / Review | “N of N recorded”; counts for pass, issue, cannot check; overall result text | **Save Inspection** appears immediately, before item history or guidance. **Review Checks** opens the recorded sequence; selecting a check allows correction. Incomplete drafts show “X checks remaining” and **Continue Inspection** instead of Save. |
| Saving | Same summary; “Saving…” | Ignore duplicate save events. Do not announce completion until durable local commit succeeds. |
| Saved | “Inspection saved on Watch”; result; equipment; completion time; “Sync pending” or “Synced” | **Done** explicitly dismisses to Ready. Pending sync remains visible on later opening. Failure to upload does not erase the saved record. |
| Save failure | “Couldn’t save. Your draft is retained.” | **Retry Save** retries the same record identity; **Review Checks** preserves all observations. No success styling. |

On Check screens, Pass and Issue receive equal visual emphasis so the design does not steer equipment judgments. Cannot Check and navigation are secondary but labeled and reachable. After recording, show the new criterion and progress immediately; retain the previous result in review. Corrections remain available throughout the draft, with no expiring recovery control. A response is an immediate command, not a persistent on/off setting.

The normal text layout should expose criterion, progress, Pass, and Issue at first glance. Secondary controls may require short scrolling. At enlarged sizes, let the criterion and controls grow and scroll rather than shrinking text or obscuring content beneath the action area. The summary always puts Save before the optional long content. Prefer inline capsule buttons; use a full-width primary action for Start and Save, short outcome labels, matching heights for peer controls, and perceivable pressed/unavailable states. This follows [Buttons: style and watchOS](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS); exact layout is this specification’s choice.

Crown rotation scrolls only the current screen; it never changes a result, marks a check passed, starts an inspection, or saves. Touch scrolling provides the equivalent navigation, and labeled buttons perform all commands. Slow rotation must allow precise positioning, while faster rotation covers content faster. Preserve Crown presses for the system. Prefer consistent linear scroll response for variable-height content; evaluate standard detents rather than introducing custom confirmation taps. See [Digital Crown: Apple Watch](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Watch).

## State, persistence, and interruption

Framework-agnostic model:

```text
Assignment = {equipmentId, displayName, serial, location, templateVersion}
Template = ordered required checks {id, criterion, optionalGuidance}
Draft = {inspectionId, assignmentSnapshot, templateSnapshot, startedAt,
         results[checkId]: UNCHECKED | PASS | ISSUE | CANNOT_CHECK,
         recordedAt[checkId], currentCheck, route, revision}
SavedRecord = immutable Draft snapshot + {completedAt, outcome, syncState}

start():
  require assignment and complete approved template available locally
  durably create draft with every result UNCHECKED
  show first check only after creation succeeds

record(checkId, value, eventRevision):
  accept only one activation from the currently rendered revision
  require value in {PASS, ISSUE, CANNOT_CHECK}
  durably persist result, timestamp, revision + 1
  on failure: remain on same check; show error and Retry; do not advance
  on success: advance to first unanswered check, or Review if none
  discard queued duplicate activations from the previous screen revision

outcome():
  if any UNCHECKED: INCOMPLETE
  else if any ISSUE: ISSUES_RECORDED
  else if any CANNOT_CHECK: NOT_FULLY_CHECKED
  else: ALL_CHECKS_PASSED

save():
  require no UNCHECKED results
  atomically commit one immutable record keyed by inspectionId
  preserve draft on failure; retry uses the same key
  queue idempotent upload; only server acknowledgement means Synced
```

“Inspection saved” means observations were recorded, not that the equipment is certified safe. Display **Issues recorded** or **Not fully checked** prominently when applicable. Do not call either a passed inspection. No automatic operational clearance or equipment lockout is specified without an approved domain policy. Optional photos, notes, or administrative details can continue elsewhere using the inspection ID; pending required follow-up must be explicit and must not be represented as completed.

Persist on every mutation, not only on exit. Wrist lowering, leaving the app, process restart, and loss of connectivity retain the draft and template version. Reopening resumes the current check or unsaved review with the same results. Never replace an in-progress template silently. A later correction to a saved record creates an amendment rather than overwriting the original; amendment editing is outside this short flow.

On supported Always On configurations, preserve the current layout, criterion, progress, and result; dim secondary fills and show controls unavailable until active. Use no ticking countdown or continuous animation. Update dimmed content only when recorded state changes and the system permits it. Wrist raise/tap restores the same context without recording an observation. Devices with Always On disabled or unavailable resume from persistence. See [Always On: best practices](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices). The illustrative equipment labels are assumed nonsensitive; real deployments need an exposure review before displaying confidential identifiers wrist-down.

Launch enters an existing draft, otherwise Ready. No complication, notification, sensor, or Action button integration is necessary for this initial design.

## Glove and accessibility behavior

Specify activation regions of at least 44 × 44 watchOS points, preferably full-width for the repeated responses; use a project starting gap of 12 pt between stacked response targets and measure actual geometry. Larger targets do not establish glove compatibility. Keep both touch and Crown navigation available; do not assume gloves operate a capacitive display or that Crown rotation can substitute for response activation. Validate the actual glove/device combination. If no supported input works safely, use an approved alternate recording workflow; keep the Watch draft incomplete.

Use semantic headline/body/action roles, regular or semibold text, and platform-equivalent scaling and Bold Text support. Start essential body text at 16 pt for the framework-independent prototype; honor platform size preferences in an implementation. Support at least 140% text enlargement for watchOS, with wrapping, growing rows, and scrolling. Never truncate criteria, serial identity, results, or action labels. The local Typography tables contain device-dependent defaults smaller and larger than 16 pt; 16 pt is a prototype choice, not a universal Watch default.

Use words and symbols alongside color for Pass, Issue, Cannot Check, save, and sync status. Success and errors remain visible until a subsequent explicit action. Do not depend on sound or haptics. Specify accessible names matching the visible action labels, button roles, and result values; every necessary control must be reachable and activatable with supported assistive input. No timed response or speech requirement. These decisions apply [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) and [Typography: Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type). Assistive behavior remains untested.

## Worked before / after

Before, the supplied proposal makes the inspector type a serial into a 40-field phone form and scroll through an article to find completion. Exact taps and completion time are unknown.

After, an illustrative cached assignment shows “Pump P-17 · Bay 2 · SN 008431.” Start confirms identity. Six illustrative criteria are Housing intact, Connections secure, Guard present, No visible leak, Indicator in approved range, and Area clear. A domain owner must replace these with approved wording and thresholds.

An all-pass walkthrough uses Start → six explicit Pass activations → Review (“6 passed”) → Save Inspection → “Inspection saved on Watch · All checks passed · Sync pending” → Done. That is nine command activations, excluding optional navigation. No serial entry or article traversal is needed.

Illustrative time budget: 10 seconds identify/start + 60 seconds physical observations and responses + 10 seconds review/save + 10 seconds allowance = 90 seconds. This is a planning allocation, not measured performance. Wrist raises may be separated by hands-on work.

Exception walkthrough: after check 2, lower the wrist. Raise it to check 3 with two observations retained. Record Issue for check 4; finish remaining checks. Review reads “5 passed · 1 issue,” and saving produces “Issues recorded,” never “All checks passed.” If check 4 cannot be examined, record Cannot Check instead; saving records a not-fully-checked outcome. If accidentally marked, revisit and correct it before saving. At 90 seconds nothing auto-submits, disappears, or changes status.

## Acceptance checks and present audit

**Passed — static specification review only:** the revised contract removes serial typing and article-gated completion; supplies explicit result commands, correction, incomplete/issue outcomes, duplicate-event protection, durable-save failure behavior, offline sync distinction, and wrist-state restoration. The required root → family → topic procedure → local source route was read from the installed package; relevant topic-index rows were searched. No web was used.

**Failed — supplied proposal against the revised design criteria:** the brief explicitly retains the broad phone form, requires serial typing, and hides completion under a long article. These are observed description-level problems; no claim about actual rendering or motor access follows from them.

**Not executed — required implementation and device acceptance:**

| Check | Pass condition |
|---|---|
| State transitions | Each result advances once; queued double taps cannot answer the next check. Changing a draft answer updates counts and outcome. Unchecked items block Save. |
| Persistence and fault injection | Interrupt after every response, at review, during commit, and during upload. Restore without lost observations or duplicate records. Local commit failure never reports Saved. Upload failure remains Sync pending and retries idempotently. |
| Independence and identity | Cached inspection completes with phone/network disconnected. Missing assignment/template never invents an identity or allows a mismatched inspection. |
| Wrist behavior | Wrist down/up and app relaunch restore the same route and data. Supported Always On stays legible, stable, and inactive without accidental results. Check devices without Always On too. |
| Layout and text | On smallest and largest supported Watches, default, 140%, and all supported text sizes plus Bold Text preserve full criteria, identity, actions, and summary. Save precedes optional content. Measure ≥44 × 44 pt regions and nonoverlap. |
| Visual access | Measure actual foreground/background contrast in supported appearances and Increase Contrast. Apply the local source table’s scope: up to 17 pt all weights 4.5:1; 18 pt all weights and bold text 3:1. Words/symbols convey every status without color. No measured conformance is claimed. |
| Input | Crown only scrolls, slow/fast response is usable, touch provides equivalent navigation, and system presses remain reserved. Verify physical separation and repeated-use comfort with actual work gloves and lighting. |
| Assistive access | On supported Apple environments, traverse and activate the complete flow with VoiceOver and applicable assistive inputs; names, values, route changes, and errors are understandable. No action requires hearing, speech, or a transient notice. |
| Timing and protocol | With domain-approved checks and representative trained inspectors, measure equipment observation time plus interaction time, errors, and interruptions. The routine path target is ≤90 seconds without skipped checks; slower completion remains usable. Validate exception paths separately. |

## Evidence limits

This is a framework-agnostic design artifact, not an app or validated inspection protocol. Only the supplied brief and installed instructions/local HIG-derived references were used. Official links above identify source articles; they were not opened. The installed references describe a dated snapshot, not verified current SDK availability. No Apple SDK, device, simulator, GUI, Accessibility Inspector, VoiceOver, glove input, haptics, contrast measurement, timing trial, build, or runtime test was executed. No sensor or hardware integration is promised. Domain completeness, real Watch fit, confidential-data handling, and physical usability remain implementation/release gates.
