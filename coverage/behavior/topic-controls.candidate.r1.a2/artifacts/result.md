# Revised smart-lamp Control Center interaction specification

## Scope and decisions

Input: `interface.md` specifies supported iOS control surfaces, a toggle-looking tile that opens seven setup screens, an always-On label even offline, a factory-reset long press, and guests who may lack control permission. This specification replaces that contract; no implementation was supplied.

Ship one configurable **Lamp power** control for one lamp. Its primary activation requests the opposite of the lamp's fresh, confirmed power state without opening the app. Setup and maintenance belong in the app. This follows the preference for focused actions without launching the app in [Controls — Best practices](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices) and the state/action distinction in [Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles#Best-practices).

Use the system control presentation rather than drawing an in-app switch inside Control Center. Supply a recognizable lamp symbol with distinct illuminated/unilluminated forms; color is supplementary. Supply title and state text for sizes that show text. Do not interpret a tinted symbol as device confirmation. [Controls — Anatomy](https://developer.apple.com/design/human-interface-guidelines/controls#Anatomy), [Toggles — iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/toggles#iOS-iPadOS).

No app-defined long-press command exists. Leave long press to the system's supported editing/configuration behavior; it must never reset, toggle a second time, or run setup. Remove factory reset from every control activation path. A separately designed owner-only maintenance flow in the app is outside this specification; merely moving reset is not evidence that its safeguards exist.

Target Control Center on supported iOS versions. Lock Screen and Action button variants use the same action, authorization, and state model if the eventual implementation supports them. This document does not establish minimum OS/API availability. The local Controls guide explicitly excludes watchOS, tvOS, and visionOS; absence of other platform rules does not prove implementation support. [Controls — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/controls#Platform-considerations).

## Configuration and destinations

- Gallery: title “Lamp power”, sample title “Desk lamp”, sample value “Off”, and a lamp symbol. Examples are illustrative, never a live lamp state.
- On adding: require selection of a stable lamp ID from the current account's authorized lamps; display the user-assigned name and room to disambiguate. Bind to ID, never list position or name. Do not preselect an unrelated lamp.
- With no configured lamps: explain “Set up a lamp in the app.” Offer an explicitly labeled setup destination through supported configuration UI. The power tile never silently becomes a seven-screen wizard.
- Permit later lamp selection through supported reconfiguration. Cancel preserves the previous selection. Commit invalidates cached state, cancels local pending work, and reads the new lamp before enabling power. An already-dispatched old-lamp command may still complete; it cannot update the new tile.
- Removed lamp: show “Lamp unavailable”; no power dispatch. Account changes invalidate the binding and require reselection; never reuse a different account's matching ID.
- Recovery destinations, where the surface supports them, open that lamp's status/permission page. Otherwise expose the explanation in configuration and in the app. Opening recovery must be a separate, clearly labeled action, not the power toggle's activation.

Required configuration and later editing follow [Controls — Best practices](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices). Precise destinations and preserved context follow [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

## State and action contract

Authoritative power comes from a device-confirmed reading/event, with lamp ID, revision/order token, and observation time. A transport acknowledgement only confirms receipt of a request. Reachability and account authorization are separate inputs. No default power value is On.

Product defaults, not Apple mandates: a reading is fresh for 30 seconds while its connection remains healthy; invalidate immediately on disconnection. A command has a 10-second confirmation deadline. These values require validation against the eventual lamp protocol. If ordered events or freshness cannot be established, expose unknown state rather than guess.

| Condition, in priority order | Unlocked title/value | Power activation |
| --- | --- | --- |
| Missing selection | Lamp power / Choose a lamp | No dispatch; configure through editing |
| No account or denied/revoked lamp permission | Lamp power / Access required | No dispatch; app recovery explains sign-in or owner-granted access |
| Removed lamp | Lamp power / Lamp unavailable | No dispatch; reconfigure |
| Offline/disconnected | Selected name / Offline | No dispatch; refresh on reconnect |
| No fresh reading | Selected name / State unavailable | No dispatch; request a read |
| Command awaiting confirmation | Selected name / Turning on… or Turning off… | No second dispatch; coalesce repeated activation |
| Fresh confirmed Off | Selected name / Off | Request explicit SET_POWER(true) |
| Fresh confirmed On | Selected name / On | Request explicit SET_POWER(false) |

For pending state, retain the previous confirmed appearance with a distinguishable pending treatment when supported; never show the requested value as confirmed. Completion uses the illuminated/unilluminated symbol and text. Unknown/offline/denied states use neutral unavailable treatment, not a false binary value. A target surface that cannot truthfully represent or suppress activation for these states needs a verified fallback before release; do not force unknown into false or true.

On transport failure, show “Couldn't change power” where supported, then reconcile with a fresh read. If fresh state is known, retain its truthful On/Off value with separate failure feedback; otherwise show State unavailable or Offline. Deadline expiry means unconfirmed, not proven failure: do not automatically resend. Refresh, accept later authoritative state, and allow a new explicit action only after fresh state is known. Remote changes update the control even when the app is closed, subject to actual platform update capability. Subscribe/read again when the control becomes active or connectivity returns. See [Controls — Best practices](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices).

Framework-agnostic pseudocode:

```text
activate(binding):
    reject if binding missing, removed, pending, or state not fresh/reachable
    require device unlock according to policy below
    recheck current account's lamp permission and refresh state after unlocking
    reject if authorization or freshness changed
    target = opposite(confirmedPower)
    pending = { uniqueRequestID, bindingGeneration, lampID, target, deadline }
    dispatch SET_POWER(lampID, target, uniqueRequestID)  // not blind TOGGLE
    // service must independently authorize the current principal
    // acceptance/queue receipt does not change confirmedPower

onDeviceReading(reading):
    ignore wrong account, lamp, binding generation, or older revision
    update confirmedPower and observationTime
    if reading causally confirms pending target: clear pending; show confirmed state
    if newer external change supersedes pending: reconcile; show actual state
    // a coincidental cached target value is not causal confirmation

onDeniedOrDisconnected():
    invalidate actionable state immediately; clear pending presentation
    never replay queued actions after access or connectivity returns

onDeadline():
    clear pending; mark unconfirmed; request authoritative read; never auto-retry
```

Maintain request IDs and ordering so delayed responses cannot overwrite newer state. Permission must also be checked at execution by the controlling service/device boundary: hiding or disabling UI alone does not enforce access. If the backend cannot provide causal confirmation, a read initiated after dispatch must establish actual state before declaring the target confirmed; ordering limitations remain an implementation blocker.

## Locked use, guests, and minimum data

Product security choice: require unlock before any lamp mutation, even though the guide specifically mandates authentication for security-sensitive actions and does not classify every lamp as sensitive. Unlocking proves device access; it does not grant guest permission. After unlock, a guest without lamp permission receives “You don't have permission to control this lamp. Ask the owner for access.” No command, reset, setup wizard, or automatic permission escalation follows. Cancelled authentication does nothing.

While locked, redact lamp/room/home names and On/Off values. Use generic “Lamp power” where text is present and a neutral lamp symbol; suppress the illuminated state too because it can disclose occupancy. Refresh authorized state after unlock. The same rule covers Control Center accessed while locked, symbol-only Lock Screen controls, and Action button feedback. For an Action button variant, use the hint “Hold to change lamp power”; it follows the same unlock gate, with no reset mapping. [Controls — Best practices](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices).

| Data/access | Purpose and minimum scope | Sequence |
| --- | --- | --- |
| Account principal and per-lamp control permission | Authorize one selected lamp; never infer permission from ownership of the phone | Resolve during configuration; revalidate on use and service execution |
| Lamp ID, display name, power/reachability, revision/time | Bind, label, and truthfully control that lamp | Fetch when selected; refresh/events thereafter; redact private presentation while locked |
| Platform protected resource access | Only if the actual chosen transport needs it | Request in app when the person invokes that feature, with accurate purpose copy; denial leaves setup/recovery available |

No contacts, location, camera, microphone, or tracking access is required by this design. Transport and storage are unspecified; do not invent HomeKit adoption or OS permission prompts. Use established secret storage and authentication mechanisms in the eventual stack, never tile payloads for credentials. Minimum collection and contextual permission requests follow [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) and [Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

## Worked before/after

Before, per the brief: a guest sees “On” while the lamp is offline. Tapping the apparent toggle opens seven setup screens. Holding it performs factory reset. The visible state provides no evidence of actual power.

After: an authorized user configures Desk lamp once. A fresh device reading says Off. Tapping sends SET_POWER(true), keeps the confirmed Off appearance with “Turning on…”, and stays in Control Center. Receipt of the request alone changes nothing. A matching device-confirmed event changes the value to On. A remote switch-off changes it to Off without another tap. If connectivity then drops, it shows Offline and sends no command. A long press never resets the lamp.

For the guest variant, authorization denial takes precedence over cached power: show Access required, dispatch nothing, and provide the explicit permission-recovery destination. Locking the phone redacts names and power, even for an authorized user. Unlocking as the same denied guest still grants no lamp permission.

## Acceptance checks and observed status

**Passed — specification inspection only:** the revised document defines one direct power action, explicit configuration, no destructive control gesture, authoritative/pending/unknown states, remote-change handling, reconfiguration races, locked redaction, and independent guest authorization. The worked trace is consistent with the state table. This is a manual document check, not execution.

**Failed — supplied before-contract:** the toggle/action mapping and truthful-state checks fail against the described wizard and always-On behavior. Long-press safety fails against the described factory reset. Guest access enforcement is unknown, not an observed failure.

**Not executed — implementation acceptance scenarios:**

| Check | Required outcome |
| --- | --- |
| Fresh Off → activation → confirmation; repeat from On | One explicit request in each direction; confirmed value changes only with authoritative evidence; no app launch |
| Receipt only, rejection, disconnect, timeout, late completion | Never falsely confirm; show pending/unavailable/failure appropriately; reconcile late state; no automatic replay |
| Repeated taps and out-of-order events | No duplicate mutation; stale responses cannot overwrite newer state |
| Remote change with app closed | Control reflects fresh actual state; measure real update latency and establish supported refresh behavior |
| Guest denied initially or revoked during dispatch | No unauthorized execution at service boundary; access message; authentication cannot bypass permission |
| Locked invocation, authentication cancel, unlock | No private title/value/state disclosure; no mutation before unlock; refresh and authorize afterward |
| Reconfigure during pending command; remove lamp; switch account | Old callbacks cannot affect new tile; no silent retargeting; cancellation preserves prior configuration |
| Long press on each supported surface | Only supported system behavior; zero reset/setup/power side effects |
| Control Center text sizes; symbol-only Lock Screen; Action button feedback | Recognizable lamp purpose and noncolor state distinctions; no invented text on symbol-only surface; truthful unavailable/pending fallback |
| Interrupt/resume, portrait/landscape, larger text, light/dark appearances | Binding and action identity survive; no duplicate sends; labels remain usable within system layouts |
| Assistive technology and symbol comprehension | Verify actual role/name/value/action, unavailable and pending feedback, focus behavior, and users' understanding; no color-only state meaning |

## Evidence limits and local route audit

Only local files were used. No browser, SDK, device, GUI, accessibility service, network transport, or runtime control was executed. No compilation, native rendering, permission enforcement, state-update timing, symbol recognition, contrast, or physical comfort is established. Official links identify source sections; they were not fetched. The installed package is independent guidance derived from a dated HIG snapshot, not an SDK availability reference or security certification.

Explicit reading order (paths relative to `.agents/skills/apple-hig/`; each file was read in its own shell command):

1. `SKILL.md`, then project `interface.md`; searched `references/topic-index.md` for control/lamp concepts.
2. `subskills/apple-hig-system-experiences/SKILL.md` → `.topics/apple-hig-controls/SKILL.md` → `references/controls.md` within that family.
3. Routed sensitive handling: `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-privacy/SKILL.md` → `references/privacy.md` within that family.
4. Platform qualification: `subskills/apple-hig-getting-started/SKILL.md`; searched the topic index for iOS/toggle/button/privacy; read `.topics/apple-hig-designing-for-ios/SKILL.md` → `references/designing-for-ios.md` within that family.
5. Supplied toggle candidate: `subskills/apple-hig-selection-and-input/SKILL.md` → `.topics/apple-hig-toggles/SKILL.md` → `references/toggles.md` within that family.

HomeKit was an index match but was not selected: the brief names no Apple Home integration or accessory-setup redesign. Reset confirmation and setup-screen design are outside the control revision. No general accessibility conformance claim is made. Release still requires validating surface/API support, truthful nonbinary presentation, authenticated execution, and the not-executed checks above in the chosen stack.
