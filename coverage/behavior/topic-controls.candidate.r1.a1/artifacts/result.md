# Smart lamp Control Center interaction specification

This revises the behaviors reported in `interface.md`; it is a framework-agnostic design contract, not an SDK implementation. Target: supported iOS Control Center surfaces. Availability by OS version, device, and implementation stack remains to be verified. Do not infer a minimum version for ordinary controls from the guide’s separate iOS 18 locked-camera statement.

## Decisions and source basis

1. **Lamp power is a binary toggle.** Activating it requests the opposite of the latest confirmed power state without opening the app. Setup is not a toggle action. Apple recommends focused controls, preferably avoiding app launch, with accurate updates after interaction, completion, and remote changes. [Controls: Best practices](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices).
2. **Configure before use.** On adding the control, require selection of one already configured lamp that the current account may control. Offer later reconfiguration through the supported system configuration path. If none qualifies, explain “Set up a lamp in the app” and offer a clearly labeled app destination; never start a wizard by pretending to toggle power. Preserve any existing setup progress in the app. Required initial parameters and later configuration follow [Controls](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices); the eligibility and empty-state details are product decisions.
3. **Remove factory reset from every control gesture.** Long press belongs to system editing, configuration, or expansion as supported; it sends no lamp command. Reset remains an owner-authorized maintenance flow in the app, outside this control’s action model. This is a product safety decision based on the supplied destructive behavior, not an assertion that HIG prescribes a particular reset flow.
4. **Use authoritative device state.** A successful transport request is not proof that the lamp changed. Show On/Off only while a confirmed observation remains current and the lamp is reachable. Unknown, pending, offline, and denied states are distinct. This applies the truthful-state procedure and [Controls](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices).
5. **Respect authorization separately from connectivity.** Guests with current control permission can toggle; guests without it cannot. Check authorization at execution, not only at configuration. Device unlock does not grant lamp permission. Locked-device activation requires authentication under this product’s conservative policy; HIG requires authentication for security-sensitive actions but does not classify every lamp as sensitive. Redact private titles and values while locked per [Controls](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices).
6. **Keep the task brief and resumable.** No seven-screen wizard on activation. App handoffs identify their destination, and interruption preserves the selected lamp and setup progress. This follows [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

## Control and configuration contract

- Stable identity: account ID plus lamp ID; a rename changes the displayed title, never the target.
- Gallery: title “Lamp power,” recognizable lamp symbol, illustrative example title “Desk lamp” and value “Off.” Do not expose a real private room name in an unconfigured preview.
- Larger Control Center presentations: configured lamp name plus value from the state table. Use a lamp symbol with distinguishable on/off variants; tint may reinforce confirmed On but cannot establish success.
- Compact/symbol-only presentations: the lamp silhouette must communicate the task without text. Pending/unavailable appearance must not imply confirmed On. Use available system feedback for an explanation if the compact presentation cannot display a value; do not invent custom surface capabilities.
- Offer all Control Center sizes supported by the eventual integration, preserving the same lamp and action when resized. Exact sizing, symbols, animation, and layout are implementation validation items.
- Other iOS entrypoints are optional, not automatically delivered by this specification. If reused on Lock Screen, retain symbol-only meaning and locked rules; if reused for Action button, use “Hold to toggle lamp” as the verb-based hint and preserve pending/confirmed feedback. These variants derive from [Controls: Anatomy and Best practices](https://developer.apple.com/design/human-interface-guidelines/controls#Anatomy).
- Reconfiguration cancels local pending presentation, invalidates old subscriptions and callbacks, and binds fresh state to the new lamp. Already transmitted commands may finish on the old lamp; they cannot update the new tile.

Configuration sequence: choose eligible lamp → save binding → fetch fresh state → enable power action. Cancel leaves the previous binding intact, or the new control unconfigured. Deleting a lamp or signing out invalidates its binding; never silently substitute another lamp.

## State, action, and feedback contract

Product policy: a confirmed observation is current for at most 30 seconds without a successful refresh or authoritative event. Explicit disconnect invalidates it immediately. The 30-second budget is a proposed product default, not an Apple requirement; validate it against the actual transport. An observation must describe device power, not merely server receipt of a command.

Evaluate states in this order: configuration/account validity → authorization → reachability/freshness → active command → confirmed power. Locked presentation overrides visible private content in every state.

| State | Visible value when unlocked | Activation |
|---|---|---|
| No valid binding/account | Choose a lamp / Sign in in app | Clearly identified configuration or account handoff; no power request |
| Current account lacks permission | No permission | No power request; explain “You don’t have permission to control this lamp.” |
| Explicitly unreachable | Offline | No power request; retain stale observation internally, not as current On/Off |
| Reachability or power unknown/stale | Updating… during refresh, then Unavailable on failure | Refresh only; do not guess a toggle target |
| Confirmed Off | Off | Request explicit power = On |
| Confirmed On | On | Request explicit power = Off |
| Command active | Turning on… / Turning off… | Ignore repeat activation; no second command |
| Command failed/timed out | Couldn’t change lamp | Refresh; show current On/Off only after fresh confirmation; require a new deliberate activation to retry |

Execution pseudocode (abstract events and operations, not API names):

```text
activate(binding):
  if deviceLocked:
    requestSystemAuthentication()
    on cancellation: return without command
    on success: re-enter activate with current binding and fresh checks
  validate account, binding, current authorization
  if validation fails: publish corresponding unavailable reason; return
  if disconnected: publish Offline; return
  if observation is stale or unknown: refresh; return without power command
  if command is active: return
  target = opposite(latestConfirmedPower)
  operation = new unique ID bound to account, lamp, and configuration generation
  publish Pending(target)
  send explicitSetPower(target, operation) with execution-time authorization
  wait for causally matching authoritative device confirmation
  if confirmed: publish confirmed device power
  if rejected, disconnected, or 10-second deadline expires:
    clear active operation; publish failure or Offline; refresh when possible
```

The 10-second deadline is a proposed product policy. Receipt/queue acceptance never publishes success. Use explicit set-power rather than a remote “toggle” command so retries cannot invert twice. Do not queue offline actions for later surprise execution. If a command may have reached the device before timeout, report the uncertainty and reconcile; timeout does not prove the lamp stayed unchanged.

Process authoritative remote updates even when the app is closed. Apply only newer observations within the same binding generation; discard outdated responses. Remote power changes update the tile. A remote update contradicting a pending target updates the known device observation but does not falsely complete that command; resolve on correlated confirmation or timeout. After permission revocation, immediately suppress power state and stop command submission. Reject unauthorized operations at the command authority even if the tile’s cached permissions are outdated.

## Locked device, data, and access

While locked, use a generic lamp symbol and title “Lamp,” with no room name, account identity, current power, or error detail that reveals private state. Use a neutral/off symbol presentation where required to avoid revealing power; do not represent this redaction as an actual confirmed Off. Unlock/authenticate before execution, then revalidate permission and freshness. Cancellation sends nothing. Resumption preserves the binding but never replays a pre-lock pending intent automatically.

| Data/access | Purpose and minimum scope | Timing |
|---|---|---|
| Account identity and lamp permission | Authorize this account for this lamp | Configuration and every command; revocation invalidates eligibility |
| Lamp ID, display name, power, reachability | Target and truthfully display the selected lamp | Configuration, refresh, authoritative updates; redact private presentation while locked |
| Command credential | Submit authorized power changes | Protected storage and authenticated transport; never displayed |
| Optional platform network/Home access | Only if the eventual integration needs it | At the relevant setup action, with an accurate purpose; no speculative permission prompts |

Do not request location, contacts, microphone, or other unrelated access for this control. Platform permission and owner-granted lamp permission are different gates. If a guest is denied, provide an in-app explanation and owner-access instructions; no misleading OS permission alert or repeated wizard. Minimum data, contextual permission requests, and established protection mechanisms follow [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) and [Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data). The actual network/storage architecture is not supplied and remains unverified.

## Worked before → after

**Before, as reported:** “Desk lamp — On” appears even when disconnected. Tapping the toggle opens seven setup screens. Holding it factory-resets the lamp. A guest may not have command permission.

**After, worked scenario:** An authorized guest adds Lamp power, selects Desk lamp, and receives a fresh Off observation. The tile shows “Desk lamp — Off.” Tap sends explicit On and displays “Turning on…” without leaving Control Center. Request acceptance leaves it pending. Device confirmation changes it to On. A wall-switch event confirming Off changes it back to Off. When connection is lost, the tile shows Offline rather than On or Off; tapping sends nothing. Long press sends nothing to the lamp. If the owner revokes guest access, the tile changes to No permission, and the command authority rejects any raced request. While locked, private text and power are redacted; canceled authentication leaves the lamp unchanged. No part of this flow triggers setup or reset.

## Acceptance checks and evidence status

**Passed — specification inspection only:** the revised contract defines direct power action, initial/later configuration, state freshness, remote changes, failure and timeout, reconfiguration isolation, guest denial, locked redaction/authentication, symbol-only variants, and removal of reset. The worked sequence agrees with those rules. Local root → family → topic → article routing was read for iOS, Controls, and Privacy, after reading the brief and searching the topic index.

**Failed — reported baseline requirements:** the supplied toggle-to-wizard behavior fails the direct-action contract; constant On fails truthful-state reporting; long-press reset fails the revised gesture contract. These are findings about the text in `interface.md`, not observed runtime failures. Guest denial behavior was unspecified, so no baseline enforcement failure is claimed.

**Not executed — implementation acceptance scenarios:**

1. Fresh Off → one activation → one explicit On command → pending until device confirmation. A receipt-only response never produces On. Repeat taps during pending submit nothing.
2. Disconnect, stale data, rejection, and deadline expiry each avoid false confirmation; late device success reconciles without automatically issuing a second command. No offline command executes after reconnection.
3. A newer remote state updates the tile; an older response cannot overwrite it. Changing configured lamps during a command never applies the old lamp’s result to the new tile.
4. An unauthorized guest cannot configure an eligible toggle or execute a saved one. Revocation between display and command is rejected by the authority. Authentication alone never bypasses authorization.
5. Locked previews disclose no private name/value or power. Canceling authentication sends nothing; successful authentication rechecks current binding and permission.
6. Add, cancel, reconfigure, rename, delete, and sign-out preserve or invalidate the correct binding. Setup interruptions retain progress; resuming never replays a power command.
7. Supported Control Center sizes, portrait/landscape, enlarged text, and appearance changes preserve the lamp identity and action. Compact symbols communicate lamp power without labels. Long press follows supported system behavior and cannot reset.
8. On real supported iOS hardware, verify native integration, system editing/configuration, lock/authentication transitions, update delivery while the app is closed, assistive-technology semantics and activation, and symbol comprehension with people. These require implementation and execution evidence.

## Evidence limits

Only `interface.md` and the installed local guidance were used; no web browsing occurred. Official links above identify the sources named by the local snapshot, not pages fetched during this work. The guides are dated 2026-10-25 and are design guidance, not SDK availability documentation. No source conflict was found in the selected passages; absence of a platform-specific rule is not proof of support.

No app code, device, SDK, GUI, backend, credential store, lamp transport, screenshots, or assistive-technology session was supplied or exercised. No runtime acceptance check has passed. State subscriptions, correlation, authentication, authorization enforcement, timing budgets, supported presentations, symbols, and platform APIs require implementation verification. This specification does not certify security, accessibility, or device behavior.
