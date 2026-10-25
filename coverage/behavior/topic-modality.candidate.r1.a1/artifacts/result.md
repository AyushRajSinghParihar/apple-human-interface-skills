# Revised composer specification

Patched interface.md in place. The one-line flow is now an implementable state and exit contract for iPhone and iPad: one modal composer, internal attachment/settings navigation, visible titles and controls, durable draft retention, explicit discard, upload recovery, and serialized presentation ownership.

## Decisions

The composer remains modal because creating one draft benefits from focused work with a clear return to Browse. Attachment selection and draft settings are steps of that task, not further modals. Global settings leave this scope. iPhone uses a large-only sheet; iPad prefers standard centered page/form sizing and adapts to compact windows without resetting state.

Close, Done, gestures and supported keyboard exits preserve writing through the same persistence gate. Done explicitly saves a draft; there is no inferred send behavior. Only confirmed Discard deletes content. Storage failure retains the editor. These persistence choices are product policy inferred from the request, not requirements attributed to Apple.

Upload errors stay inline with Retry/Remove. An exclusive decision slot prevents duplicate confirmations, and stale callbacks cannot resurrect discarded work. Back preserves the draft and returns within the task. Focus restoration is specified, not verified in a runtime.

Source support: local snapshot [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices), [Sheets — Anatomy, Best practices, iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets), and [Alerts — Best practices, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts). The sheet guide describes Cancel/Close as dismissing without saving; this design explicitly retains a separate recoverable draft and reserves Done for acknowledged completion. It does not treat Close as publishing or committing a final document.

## Worked before/after

Before: Browse → blank-titled composer → attachment modal → settings modal. A person types “Meet at noon,” encounters an upload failure and taps it twice. Two alerts can appear. There is no attachment Back action; swiping or Done deletes the unsaved writing.

After: Compose opens New Draft. “Meet at noon” becomes a stored draft revision. Attachments opens inside the same sheet; Add returns to the editor. A failed upload shows inline Retry, and two taps on its error only reveal inline details. Draft Settings opens internally and Back restores the editor. A downward swipe saves the current revision before returning to Browse. Resume reopens the writing and failed attachment in the editor. If saving fails, dismissal stops with text intact and Retry. Discard Draft is the only deletion path and requires a deliberate confirmation.

## Acceptance checks

Static specification review passed:

- Every named exit has a data consequence and destination, including clean exit, edited exit, cancelled swipe, keyboard exit, interruption and outside dismissal if offered.
- Back and Add have separate outcomes; Done saves and updates Browse once; reopening resets transient navigation.
- State ownership allows one composer and one decision; upload errors cannot present alerts, and repeated requests/callbacks are guarded.
- Both device contexts have explicit presentation choices and share draft protection.
- Failure handling distinguishes durable revisions from changes still saving.

Failed checks: none found in the revised document review. This is not a runtime test result.

Not executed; required implementation acceptance scenarios:

1. On iPhone and iPad, close an empty draft and an edited draft using each supported button, swipe, keyboard and outside-click route. Verify Browse destination, durable content and focus restoration. Cancel a swipe and verify unchanged step/text.
2. Add an attachment, change settings, use Back and resume; verify text, attachment state, settings, caret and scroll survive as specified. Resize an iPad window during editing.
3. Inject storage failure during Done and swipe: verify no dismissal, no deletion, accurate status and successful Retry. Relaunch after an acknowledged save and verify the durable revision.
4. Tap upload errors and Retry repeatedly, including during discard confirmation. Verify no stacked presentations or duplicate upload attempt; cancel confirmation and verify editor return. Confirm discard and inject stale callbacks; verify no resurrection.
5. Repeat Compose/Done/Close rapidly and verify one presentation and one Browse update. Check keyboard cancellation consumes only the top decision. Exercise VoiceOver focus transfer and visible exits with enlarged text on both platforms.

## Evidence and limits

All work used local files; no browsing occurred. Successful file reads consumed the installed root apple-hig SKILL.md, the Presentation family, the Patterns family, the routed Modality topic procedure, then its source guide. Sheets and Alerts guides were also read. The Presentation family's exact `.topics/apple-hig-sheets/SKILL.md` and `.topics/apple-hig-alerts/SKILL.md` paths were attempted but are absent from this installation; a hidden-file search found their reference guides only. The related entering-data topic procedure was also attempted and absent. Those missing procedures were not consumed or represented as available; detailed guidance uses the present guides and the available Modality procedure.

The original interface.md supplied only a prose flow. No app code, framework, deployment target, SDK, build or device runtime was supplied. No device, SDK compilation, GUI interaction, persistence fault injection, keyboard execution or accessibility execution is claimed. Static review establishes the contract's coverage, not actual native presentation, input handling, focus behavior or crash durability. Official URLs identify source sections from the local dated snapshot and were not fetched or verified online.
