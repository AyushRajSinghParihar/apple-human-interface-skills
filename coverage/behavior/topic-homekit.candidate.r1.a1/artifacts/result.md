# Repair decisions and evidence

Patched `interface.md` in place, replacing the one-sentence defect description with an implementable specification. The original brief reports defects; no running implementation was supplied.

## Decisions and patch summary

- Scope Bedroom by stable home and room IDs, then filter controllable light functions. Keep a combination device’s light while excluding its fan; exclude unrelated accessories. Preserve authoritative names and external configuration changes.
- Separate confirmed power, requested power, reachability, freshness, permissions, and errors. Explicit Turn On/Turn Off buttons issue commands; a tap or delivery acknowledgment never proves physical state. Define duplicate suppression, confirmation, failure, a 10-second unconfirmed timeout, refresh, late responses, and recovery without automatic replay.
- Retain offline rows with last-known or unknown state and an explanation. Distinguish offline, empty room, and unavailable home data.
- Hide and enforce owner-only configuration boundaries. Determine guest control access from actual permissions, including permission changes during a request.
- Specify iPhone list/reflow behavior and a resizable Mac presentation with keyboard and menu command parity. Preserve valid selection on return while refreshing stale state.

The shared-home model and synchronization decisions follow [HomeKit’s terminology/layout and custom-functionality guidance](https://developer.apple.com/design/human-interface-guidelines/homekit). Command labels and waiting feedback follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons); truthful nearby results and recovery follow [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback). Platform presentation follows [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) and [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos). These links identify the official articles; only installed local snapshots were consulted. The timeout and synchronization algorithm are product choices, not HIG mandates.

## Worked before/after

Fixture: Home A has Bedroom with Bedside (Off), Ceiling (offline, last known On), a fan/light combination, and a thermostat. Kitchen has Pendant (On). Home B also has a Bedroom. The user is a guest permitted to control lights but not configure the home.

**Before, as described by the brief:** Bedroom displays every accessory in the home, including Kitchen and nonlights. Ceiling disappears. Owner configuration is visible. Tapping On for Bedside changes its UI to On even though the command fails.

**After, specified trace:** Home A → Bedroom lists Bedside, Ceiling, and the combination’s light function only. Ceiling remains labeled “Offline; Last known: On.” Configuration actions are absent. Bedside shows Off and Turn On. Activation leaves Off visible with “Turning on…” and disables duplicate activation. A rejection shows “Couldn’t turn on,” labels Off as last confirmed, and triggers a read. If that read confirms Off, Turn On becomes available again; if it finds On due to another controller, the row shows On and Turn Off. If the read fails, the state remains unknown/stale and Refresh is available. No automatic retry occurs. Home B’s Bedroom remains isolated throughout.

## Acceptance checks

The following are implementation acceptance scenarios, not executed runtime tests:

| Scenario | Required outcome |
| --- | --- |
| Home A/B have identically named rooms/lights | Stable IDs isolate selection, commands, and responses. |
| Bedroom has fan/light, thermostat, and offline light | Only light functions appear; offline light stays visible; no fan/thermostat power action. |
| Empty room versus unavailable Home data | Different messages; access failure never claims zero lights. |
| Successful, rejected, delayed, and repeated activation | Only authoritative observation yields actual state; failure remains truthful; timeout gives recovery; repeated activation sends one request. |
| Delivery acknowledgment without state confirmation | Pending remains until confirmation or the specified timeout. |
| Offline before/during a write, then reconnection | Row persists, writes stop, refresh reconciles state, old intent is not replayed. |
| Guest with/without control permission; owner loses permission | Correct control availability; owner-only configuration hidden from guests; command boundary rejects unauthorized writes. |
| Apple Home rename/move/remove or external power change | Updated labels/membership/state; no cached overwrite; obsolete callbacks cannot restore removed rows or stale state. |
| Navigate during pending request, then switch homes | Request remains bound to original IDs; new home never receives old result. |
| iPhone rotation, enlarged text, interruption and return | Controls remain reachable, labels readable, Back works, selection survives, stale state refreshes. |
| Mac keyboard-only use, resize, activation change | Same selected-light actions and availability in menu/list; no unintended Return activation; commands remain accessible. |
| Nonvisual interpretation and muted use | Light identity, actual versus pending status, reasons, and recovery remain understandable without color or sound alone. |

## Verification status and limits

**Passed — static artifact review:** `interface.md` now provides explicit contracts for all four reported defects, nonlight filtering, external synchronization, platform behavior, and failure recovery. The worked trace is consistent with those contracts. Both requested Markdown files were written and read back.

**Failed — supplied baseline:** The brief explicitly reports incorrect room scope, false command success, exposed owner configuration, and disappearing offline devices. These are reported baseline defects, not independently reproduced test failures.

**Not executed:** App/device tests, network fault injection, accessory pairing/control, multi-app synchronization, permission enforcement, SDK compilation/API availability, native rendering, target measurements, keyboard/menu operation, VoiceOver or other accessibility execution, and physical touch comfort. The project supplies only a short prose interface brief, so no executable implementation supports those claims. A Mac deployment technology must be selected and its actual integration availability verified before implementation. No web browsing, GUI interaction, or device execution was performed.

## Installed guidance audit

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then searched `references/topic-index.md`. Read owning family procedures and routed topic procedures before their supporting guides:

- Getting started → Designing for iOS and Designing for macOS → each corresponding reference.
- Technologies → HomeKit → HomeKit reference.
- Menus and actions → Buttons → Buttons reference. The existing “On” action was mapped to a candidate button; the revision uses explicit immediate commands rather than a persistent toggle.
- Patterns → Feedback → Feedback reference.

All paths were resolved inside the installed package. Each instruction/reference read used its own `cat` or `rg` command. Sources are local application guidance snapshots; their presence and citation do not establish independent review or current SDK support.
