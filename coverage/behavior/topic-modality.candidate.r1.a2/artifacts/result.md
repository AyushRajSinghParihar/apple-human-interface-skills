# Composer specification repair

Patched interface.md in place. The former chain `browse → composer sheet → attachment modal → settings modal` is now one titled composer sheet with internal attachment/settings navigation. Root Cancel and Done are visible; Back returns within the task. Done saves locally, while every other exit shares clean/dirty handling. Dirty dismissal offers Save Draft, Discard Changes or Cancel. Only an explicit discard removes unfinished writing. The specification also defines recovery checkpoints, failed-save behavior, asynchronous callback ownership and one decision-overlay slot. Upload failures use inline recovery instead of alerts.

## Decisions and source support

The composer remains modal for focused creation of one draft, with Browse blocked. Unrelated app settings are excluded. This preserves the requested modal task while avoiding a miniature app inside it. Clear title, exits, protection against loss and no stacked alerts are supported by [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

Large-only composition on iPhone and standard centered page/form sizing on iPad follow [Sheets — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS). Child Back and root Cancel/Done have separate meanings; three competing navigation controls are not shown together. The exit confirmation is a temporary decision, not a nested task sheet. Save/discard options follow [Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets). Routine upload status remains inline following [Alerts — Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices).

Preserving context on interruption and width changes follows [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) and [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices). The exact draft storage scheme, labels, local-save meaning of Done, and revision arbitration are product decisions. No send/publish requirement or storage implementation was supplied. Checkpoints preserve recovery work separately from explicit saves; Cancel is not silently redefined as save.

## Worked before/after

Before: From Browse, write “Meet at 4”, open an attachment modal, then settings above it. There is no attachment Back. An upload error can produce two alerts. Swipe down or Done deletes the unfinished draft.

After: Open New Draft, write “Meet at 4”, then push Attachments inside the same sheet. A failed upload retains its local file and displays inline Retry. Repeated error taps produce no alert; repeated Retry starts only one operation. Back returns to the text unchanged. Open Draft Settings and change a setting. Swipe down: the composer remains and one Save this draft? decision appears. Cancel restores Draft Settings with all edits. Back returns to root; Done saves text, attachment and settings locally, then returns to Browse. Resume opens the saved draft without an old decision overlay. If saving fails, the composer remains with its working copy and Retry. On iPad, narrowing the window during this sequence changes presentation size, not draft identity or route.

## Acceptance checks

The following are static contract traces, not executed app tests.

| Check | Static result | Required implementation observation |
| --- | --- | --- |
| Untouched new draft → Cancel / swipe / supported keyboard exit | Pass: clean close, no created work to lose | All supported exits return to the original Browse context |
| Edit → each exit, including from a child | Pass: one common dirty handler | Dismissal is intercepted before data or view disappears |
| Dirty decision → Cancel / outside dismissal / keyboard cancellation | Pass: same draft, revision and route retained | No save or discard occurs; focus returns |
| Dirty decision → Save Draft / root Done | Pass: close only after local save succeeds | Offline saving retains text and failed attachments; save failure keeps editor open |
| Dirty decision → Discard Changes | Pass: explicit new-draft removal or existing baseline restoration | Failed discard preserves working copy; late callbacks cannot resurrect discarded work |
| Attachment detail → Back → root | Pass: pop one route, keep writing | No new sheet, no task dismissal, no lost selection |
| Repeated exit/error/retry during decision or save | Pass: serialized owner and per-attachment retry guard | No duplicate task sheets, decisions, alerts or uploads |
| Background / recovery / reopen | Pass: checkpoints distinct from saves; transient overlays not restored | Test actual persistence boundary, failed writes and restart recovery |
| iPhone rotation, keyboard, enlarged text; iPad wide/narrow resize | Pass: state-preservation and reachable-action requirements specified | Verify readable controls, scroll reachability and unchanged route/draft |
| Touch, pointer, keyboard and focus restoration | Pass: shared action semantics specified | Verify native interaction, focus and supported cancellation behavior |

Failed static checks: none identified in the revised contract. The supplied original fails the stated draft-preservation, visible-exit, internal-Back and presentation-serialization requirements by its own explicit behavior.

Not executed: app/runtime tests, device or simulator interaction, SDK compilation/API availability, native sheet/confirmation anchoring, keyboard gesture handling, VoiceOver or other accessibility execution, physical reach, enlarged-text rendering, storage durability and real asynchronous races. These remain acceptance work for an implementation; the table does not establish runtime correctness.

## Evidence and audit limits

Evidence consists of the original one-paragraph interface.md and the installed local skill package. No implementation, screenshots, device recordings or test suite were supplied. No web browsing was used. Official links above identify articles referenced by the local snapshot, not independently verified current online guidance. The snapshot describes itself as derived guidance and does not establish SDK support.

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then searched its topic index. Read the getting-started, patterns and presentation family SKILL.md files, followed by the routed Designing for iOS, Designing for iPadOS, Modality, Sheets, Alerts, Entering data and Action sheets topic procedures before their corresponding reference guides. Each instruction/reference read used a separate single-file cat or rg command. No package paths were inferred from another installation.
