# Contextual help for the Mac statistical-analysis workspace

This specification replaces generic document redirects with explanations and recovery steps beside the current model and data. It is framework agnostic. The only observed interface evidence is the description in `interface.md`; examples below are proposed fixtures, not findings about an implemented statistical engine.

## Decisions and source support

| Supplied behavior and effect | Revised decision | Basis |
| --- | --- | --- |
| Every disabled control opens the same 80-page PDF, taking users away from the task | Disabled controls remain inert. Show their specific reason and an enabled recovery action nearby. Never require activating a disabled control to discover the reason. | [Feedback: Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) says to explain unavailable commands and how to proceed; placement and mapping are product decisions. |
| Error text says “Consult support,” without an explanation or next step | State what failed, the known cause, and a safe next step next to the model. Preserve inputs and existing results. Support is a fallback for unresolved failures. | [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) supports nearby routine feedback and reserving alerts for critical information. |
| Tooltips obscure chart values indefinitely | Restrict help tags to brief control-action descriptions; put essential model explanations in persistent inline text. Suppress help tags over the plot and provide selected chart values in a reserved area outside it. | [Offering help: macOS, visionOS](https://developer.apple.com/design/human-interface-guidelines/offering-help#macOS-visionOS) recommends action-specific help tags, aiming for 60–75 characters maximum with localization growth. Chart placement and timing below are product choices. |
| Users need deeper help without leaving their data | An explicit “Explain Requirements” action expands an inline section beneath model settings, never an overlay. Keep the data and chart usable. Optional “Open Full Manual” is a deliberate secondary action. | [Offering help: Best practices and Creating tips](https://developer.apple.com/design/human-interface-guidelines/offering-help#Best-practices) favors concise task-specific help and inline tips when surrounding information should remain visible. |

No automatic onboarding tips are introduced. Task blockers remain visible for beginners and experienced users alike because they explain current state, rather than repeatedly teach basics. Optional detailed help opens only on request and stays closed after dismissal until requested again.

## Layout and action contract

Place the model status directly below model settings and immediately above “Run Model.” Each blocked control also has a nearby sentence explaining its own dependency; share a reason block only for controls in the same clearly labeled group. Multiple blockers appear as a stable ordered list in settings order, each with its own recovery action. The summary reads “Model cannot run — 2 requirements need attention,” using the actual count.

The detail section expands within the settings area and uses normal document scrolling; it must not cover the chart or open another application. When space is limited, retain the data view and allow settings/help to scroll. Preserve dataset identity, selection, filters, model parameters, chart viewport, and prior output when opening or closing help. Existing results carry “Previous result — settings have changed” when appropriate.

| Control | Availability, role, activation, and exit |
| --- | --- |
| Run Model | Primary analysis action when requirements are satisfied. Disabled while blocked, checking, or running. Never opens help. Return must not bypass disabled state or activate it from an unrelated help control. |
| Recovery action, e.g. Select Outcome | Enabled text button next to its reason; normal role. Moves focus to the relevant existing setting, scrolling it into view. Does not silently select a variable, change data, or start a run. |
| Explain Requirements | Enabled text button, normal role, beside the status. Expands the detail section and focuses its heading. Heading names the current model; body lists requirement, current value, and next step for each blocker. |
| Close Explanation | Enabled text button inside details. Collapses details and restores focus to Explain Requirements. Escape does the same when focus is inside details; otherwise it retains the current editor's normal meaning. |
| Open Full Manual | Secondary text action inside details. Opens the relevant model/requirement topic or exact PDF section when a verified mapping exists. If no mapping exists, label “Open Full Manual” and disclose that it opens the complete document. Requires explicit activation. |

Use text actions rather than a question-mark button beside every control. If an existing window help button is retained, keep at most one, in the view body in a lower corner for this workspace without dismissal controls; name it “Model Help” and open the same contextual section. Its tooltip can read “Explain requirements for the current model.” This follows [Buttons: macOS Help buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Help-buttons). Use familiar system styling if the chosen framework supplies it; custom buttons need enabled/disabled/focus/press feedback and meaningful accessible names. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons).

## State and event specification

The statistical engine owns validation truth. Help content maps stable reason codes to localized explanations and recovery targets; it must not infer validity from a tooltip or duplicate statistical rules in the view.

```text
state = {documentId, modelId, revision, phase, blockers, failure, helpOpen}
phase = checking | blocked | ready | running | failed | completed

on relevant settings/data change:
    revision += 1
    phase = checking
    show "Checking model requirements"; disable Run Model
    request validation(documentId, modelId, revision)

on validation result(result):
    ignore unless documentId, modelId, revision all match
    blockers = result.reasons
    phase = blocked if blockers nonempty else ready
    render reasons, counts, recovery targets, and open details from same snapshot
    do not steal focus or run automatically

on Run Model:
    accept only when phase permits and current revision is validated
    capture immutable run snapshot; phase = running
    revalidate at execution boundary; report newly discovered blockers inline

on run failure:
    accept only for matching run snapshot
    phase = failed
    preserve settings/data; show known cause and mapped next step
    offer Retry only if retry is meaningful; never claim success

on model/document switch:
    cancel pending tooltip timers; dismiss tooltip
    close details; clear obsolete reasons; validate new context
```

After failed execution, a settings change clears obsolete failure copy and revalidates. A successful result replaces the run status only when the engine confirms completion; a result from an older revision is identified as such. If the cause is unknown, say: “The model did not finish. Your data and settings are unchanged. Try again; if it fails again, contact support with error code {code}.” Only claim unchanged data/settings if the implementation guarantees that invariant. Do not invent a statistical explanation for an unknown error.

For known errors, use “{Model} could not run: {specific cause}. {next step}.” No alert is needed for these recoverable model requirements. In an open detail section, update resolved requirements in place to “Resolved” rather than removing the focused action abruptly. On collapse/reopen, show only current blockers. When the last blocker resolves, show “Ready to run”; leave focus with the user's editing task.

## Tooltips and chart values

Help tags describe the indicated action, use sentence case, generally omit final punctuation, and adapt to state. Examples: “Run the model with the current settings” and “Select an outcome before running the model.” The latter duplicates an always-visible reason; essential information never depends on hover.

Custom fallback timing, proposed for validation: show after 700 ms of uninterrupted pointer dwell; dismiss after 5 seconds, immediately on pointer departure, Escape, click, scroll, context change, or focus change. Cancel pending timers on all dismissal events. After timeout or Escape, do not reappear until the pointer leaves and re-enters. These numbers are product defaults, not Apple HIG limits; prefer platform help-tag behavior when available, subject to the no-obstruction contract.

Choose a placement outside chart bounds. If none fits, suppress the help tag; the persistent description remains available. Never show control-help tooltips on chart marks. Hovering a mark updates a reserved “Chart value” area below the chart; keyboard selection of a mark exposes the same value. Retain selected values until selection changes or is cleared. Help timeout never clears selected data values. This preserves time to read essential content while allowing incidental help tags to disappear.

## Worked before/after

Illustrative fixture: a model requires one selected outcome; none is selected. The actual engine must supply supported model requirements and validate their statistical correctness.

**Before (supplied behavior applied to fixture):** Run is disabled. Attempting to use it opens the same 80-page PDF as other controls. “Consult support” gives no repair. A tooltip remains over a chart value.

**After:** The settings area reads “Model cannot run — select an outcome variable.” “Select Outcome” focuses the outcome selector; Run Model is disabled and inert. “Explain Requirements” expands: “An outcome is the variable this model will explain. No outcome is selected. Choose an outcome in model settings.” The chart remains visible and selected values remain in the chart-value area.

The user activates Select Outcome, chooses an engine-supported variable, and validation returns no blockers. The status becomes “Ready to run,” Run Model becomes enabled, and focus remains at the selector. The user explicitly runs the model. Opening, closing, and reopening the explanation never changes the chosen variable, filters, or chart selection. A second fixture with two blockers confirms that fixing one does not enable Run prematurely.

## Accessibility and sizing contract

Provide names, button roles, disabled states, and a programmatic relationship from each blocked control to its visible reason. Keep explanation text available to assistive reading even if a disabled control is skipped by keyboard navigation. Keyboard order follows settings, reasons and their recovery actions, explanation action, and Run Model; expanded details are reached next in document order. Opening help explicitly moves focus; passive validation does not. Close returns focus as specified above.

Use persistent text as well as status symbols; color and sound are never the sole source of a blocker. At 200% text size, wrap messages and stack actions without clipping or covering data. All recovery/help actions must work with keyboard and supported assistive input, with no pointer dwell required. See [Accessibility: Vision, Mobility, Speech, Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility).

The installed references differ in sizing scope: Buttons gives a general 44 × 44 pt hit region, while Accessibility lists macOS default controls as 28 × 28 pt and minimum 20 × 20 pt. Conservatively allocate at least 44 × 44 pt for new custom help/recovery button hit regions with no overlaps; this is a product choice, not a claim that every standard Mac control must be 44 pt. Measure actual geometry in implementation.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** the supplied brief was read; each of its three reported problems has a concrete replacement above. Installed root, topic index, Patterns → Offering help and Feedback, Menus and actions → Buttons, and Foundations → Accessibility were explicitly read, with each topic procedure read before its reference. No browser or SDK was used. The result contains exact copy, anchors, eligibility, transitions, exits, later access, and recovery contracts.

**Failed — supplied baseline description:** contextual routing fails because every disabled control leads to the same PDF; actionable error explanation fails because the only supplied message is “Consult support”; nonobstructing temporary help fails because the brief explicitly reports indefinite chart obstruction. These are brief-based findings, not reproduced runtime failures.

**Not executed — implementation acceptance:**

| Scenario | Required observable result |
| --- | --- |
| Zero, one, and several blockers | Reasons match the engine snapshot; disabled controls do nothing; each recovery action reaches its setting; only zero blockers permits Run. |
| Delayed/rejected validation and rapid model changes | Old replies cannot overwrite current reasons or enable Run; checking status stays truthful. |
| Run succeeds or fails | Only confirmed completion shows success; known failures offer a specific next step; unknown failures do not fabricate a cause. Inputs and prior results survive. |
| Help open/close/reopen; experienced user; dismissed help | No automatic reopening or repeated basics; explicit access always works; selection, filters, and chart viewport survive. |
| Wrong model/document context | No stale explanation, repair target, tooltip, or result is presented as current. |
| Pointer dwell and every dismissal event | Timer cancellation works; no indefinite tag, repeated timeout loop, or chart-value obstruction. |
| Keyboard and assistive input | Every repair and help action is reachable and activatable; names/states/reasons are exposed; focus returns correctly and is not lost on resolution. |
| Long translations and 200% text | Labels wrap, full explanations remain readable, controls stay separate, and chart/data access remains available. |
| Light/dark and Increase Contrast | Text/status remain distinguishable; actual contrast is measured with a calculator; no color-only meaning. |

No device, GUI, accessibility-tool, SDK compilation, statistical-engine, localization-layout, contrast, or hit-region execution occurred. No runtime passes are claimed. No code, screenshots, model catalog, PDF content, or user-study data were supplied, so model-specific rules, verified manual anchors, native rendering, timing suitability, and learning outcomes remain unverified. Official links above identify the sources behind the installed local snapshot dated 2026-10-25; they were not opened or checked for newer guidance. Prototype testing on the user's Mac is needed to establish behavior and usability.
