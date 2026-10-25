# Revised task-assistant snippet

## Scope and decisions

`interface.md` supplies a behavioral brief, not code or a screenshot: the result contains the full app navigation tree and performs a bank transfer merely on display. Replace this with a compact transfer confirmation followed by a factual result. Rendering, refreshing, restoring, and opening details must never submit money movement.

This framework-agnostic contract targets source-supported visual snippets in Siri, Spotlight, or Shortcuts on iOS, iPadOS, and macOS. The installed guide excludes visual snippets on tvOS, visionOS, and watchOS; this does not establish availability of a transfer action or audio-only experience there. HIG is not an API or banking-capability guarantee. Actual deployment requires separate capability, authentication, and service validation. [Snippets — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/snippets#Platform-considerations)

| Decision | Concrete contract | Basis |
|---|---|---|
| One task per snippet | Show transfer state, amount/currency, recipient, source account identifier, and only the relevant detail/recovery action. Remove global navigation. | Compact confirmation/result and detail links: [Snippets](https://developer.apple.com/design/human-interface-guidelines/snippets#Best-practices). Field selection is a product decision. |
| Confirmation precedes submission | Require explicit confirmation of a validated transfer summary. System Cancel abandons the draft; primary label is **Transfer Money**. Display alone has zero financial side effects. | Concrete confirmation labels and system controls: [Snippets — Anatomy](https://developer.apple.com/design/human-interface-guidelines/snippets#Anatomy). Mandatory transfer confirmation is this specification's product safeguard. |
| Every invocation ends with an outcome | Return a result with system Done for completed, canceled, failed, or unresolved work. Done dismisses; it never submits or cancels an in-flight transfer. | [Snippets — Anatomy](https://developer.apple.com/design/human-interface-guidelines/snippets#Anatomy). Outcome taxonomy is a product decision. |
| Speech works independently | Speak the essential summary, confirmation question, outcome, and next step. Prefer built-in responses where sufficient. Do not say “see above.” Avoid repeating the entire spoken paragraph in the custom view; its labeled facts must still stand alone. | [Siri — Customizing](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri), [Snippets — Best practices](https://developer.apple.com/design/human-interface-guidelines/snippets#Best-practices). |
| Truthful waits | Show known summary plus current status promptly. No invented duration, percentage, or success. End an unresolved wait with a status/detail route. | [Loading — Showing progress](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress). Timeout policy requires service evidence. |

## State and action contract

Input: recipient identity, source account identity, positive amount in minor units, currency, applicable fees, and execution date. Resolve missing or ambiguous fields before confirmation: for example, “Which Alex should receive the transfer?” Never select a recipient from an ambiguous name automatically. If the service cannot securely authorize the task in the assistant context, return **Continue in App** with the draft; opening it does not authorize submission.

| State | View and complete spoken response template | Available actions / transition |
|---|---|---|
| Preparing | **Checking transfer details**; known draft facts. “I’m checking the transfer details. No transfer has been submitted.” | Cancel preparation; validation returns confirmation or a specific failure. |
| Confirmation | **Review transfer**; amount/currency, recipient, source account suffix, execution date, fee if applicable. “Transfer {amount and currency} from {source and suffix} to {recipient and disambiguator} {date}, with {fee}? Confirm to transfer, or cancel.” | System Cancel → canceled result; **Transfer Money** → submission only after authentication and unchanged validated summary. **Review in App…** on Mac, **Review in App** elsewhere opens full draft without submitting. |
| Submitting | **Submitting transfer** with the same summary. “I’m submitting your transfer of {amount and currency} to {recipient}. Completion isn’t confirmed yet.” | Disable repeat submission. Where the host exposes the initiating button during the wait, use its activity indication on iOS/iPadOS. Dismissal leaves the operation intact; do not offer misleading Cancel after submission. |
| Completed | **Transfer completed**; verified amount/currency, recipient, source suffix, completion time. “Your transfer of {amount and currency} from {source and suffix} to {recipient} completed.” | System Done; **View Transfer** → authenticated transfer record. Put reference and extended receipt in details. |
| Accepted/pending | **Transfer pending**; summary and last-checked time. “Your transfer of {amount and currency} to {recipient} was accepted but hasn’t completed. Check its status in the app.” | Done; **View Transfer**. This is the result of the request, not a claim that funds arrived. No perpetual animated progress snippet. |
| Unknown | **Transfer status unknown**; summary and last-checked time. “I couldn’t confirm the status of your transfer of {amount and currency} to {recipient}. Check its status before trying again.” | Done; **Check Transfer Status** performs a read for the existing operation. Never automatically resubmit. |
| Failed | **Transfer not submitted** only when rejection/non-submission is authoritative. “Your transfer of {amount and currency} to {recipient} wasn’t submitted: {specific reason}. {recovery instruction}.” | Done; **Review in App**. If submission might have occurred, use Unknown instead. |
| Canceled | **Transfer canceled**. “The transfer was canceled before submission. No transfer was submitted.” | Done. |

All buttons have text names matching their outcome, visible focus/enabled states, and press feedback. Detail actions navigate; none commit a transfer. Preserve system control semantics and avoid adding an implicit custom Return-to-transfer shortcut. Keyboard or assistive activation must deliberately target the confirmation action. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Content)

```text
render(state): return view(state)                 // pure: no service mutations
onConfirm(summaryVersion):
  require state == confirmation && authenticated
  require validatedSummary.version == summaryVersion
  atomically claim submission for this draftVersion
  persist operationKey and immutable confirmed summary
  state = submitting
  submitOnce(operationKey, confirmedSummary)
onServiceUpdate(key, version, outcome):
  ignore mismatched keys and older updates
  persist authoritative outcome; publish corresponding result
onTimeoutOrLostConnection(): state = unknown     // not failed or completed
onRestore(): read persisted operation; reconcile status, never submit
onDetails(): open authenticated draft/operation destination
```

Idempotency, durable operation keys, version binding, and authoritative completion are service requirements proposed here, not HIG guarantees. If these cannot be provided, keep submission in the app. Changes to amount, recipient, source, date, or fees invalidate confirmation. Delayed replies for an abandoned draft must not revive it or execute anything.

## Compact layout and localization

Custom content must stay within **400 pt high**, including enlarged text; system dialogue and controls are outside the custom content contract. Use a vertical hierarchy: state heading, amount, recipient, source, optional timing/fee, detail action. Prefer semantic text roles and readable weights. Wrap labels and stack fields; remove optional receipt details before reducing readability. Do not clip or abbreviate the amount/currency or recipient identity needed for safe confirmation. If essential confirmation content cannot fit at the current size/locale, omit inline commitment and offer **Review in App** instead. Details open the exact draft or transfer, retaining context. [Snippets](https://developer.apple.com/design/human-interface-guidelines/snippets#Best-practices), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type)

Localize whole messages with named parameters and regional currency/date formatting; distinguish language from region. Use unambiguous currency names in speech. Test long recipient/account names and expanded translations. iOS/iPadOS use supported Dynamic Type sizes; macOS has no Dynamic Type, so specify equivalent product text enlargement to at least 200%. Retain draft and operation state across orientation, narrow iPad presentation, resizing, and activation changes. [Inclusion — Languages](https://developer.apple.com/design/human-interface-guidelines/inclusion#Languages), [Typography — macOS](https://developer.apple.com/design/human-interface-guidelines/typography#macOS), [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios), [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados), [macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)

Expose heading, labeled summary, current status, and named actions in task order. Essential facts remain available visually and audibly. Do not rely on status color or require speech input. Keep results until explicit dismissal within host lifecycle constraints. Measure light/dark contrast and enlarged layouts before release. Use at least 44 × 44 pt custom action targets across this design, including Mac: this conservatively follows the general Buttons guidance where Accessibility lists a smaller macOS default (28 × 28 pt). Do not restyle system-owned controls to force custom geometry. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)

## Worked before / after

**Before — supplied behavior:** displaying the result immediately transfers money while exposing the full app navigation tree. No actual labels, amounts, or rendered geometry were supplied.

**After — illustrative fixture:** invocation requests USD 125 from Checking ending 4821 to Alex Morgan ending 9063, today, no fee.

1. Show **Review transfer / USD 125.00 / To Alex Morgan · 9063 / From Checking · 4821 / Today · No fee**. Speak: “Transfer 125 US dollars from Checking ending 4821 to Alex Morgan ending 9063 today, with no fee? Confirm to transfer, or cancel.” Show system Cancel and **Transfer Money**, plus the draft detail route. Rendering this twice submits nothing.
2. Cancel produces the canceled result and zero submissions. Alternatively, deliberate confirmation submits once and shows **Submitting transfer**; a slow response never displays “completed.”
3. Only a verified completed service response produces **Transfer completed / USD 125.00 / Alex Morgan · 9063 / Checking · 4821 / Completed {time}**, **View Transfer**, and system Done. Speak: “Your transfer of 125 US dollars from Checking ending 4821 to Alex Morgan ending 9063 completed.” View Transfer opens that record; Done dismisses.
4. If the connection drops after submission, return **Transfer status unknown**, Done, and **Check Transfer Status**, using the Unknown dialogue above. Reopening reconciles the same operation instead of transferring again.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** rendering is separated from submission; confirmation and result are distinct; every outcome has dialogue and dismissal; pending/unknown cannot claim completion; navigation is replaced by exact detail destinations; supported visual surface exclusions and the 400 pt constraint are recorded. These are document properties, not implementation results.

**Failed — supplied baseline description:** display triggers transfer; full navigation tree defeats the compact task result. Other baseline behavior is unknown.

**Not executed — implementation acceptance gates:**

- Render, refresh, resize, reopen, and open details repeatedly: zero submit calls. Cancel before confirmation: zero submit calls and canceled result. Confirm twice or restore after interruption: exactly one operation for the confirmed version.
- Change confirmed fields or authentication state: no stale submission. Deliver late/out-of-order responses: no wrong-draft result or duplicate transfer.
- Simulate slow validation, offline before submission, rejection, accepted/pending, timeout after submission, and eventual completion. Each must match the state table; status checking only reads. Service deadlines and latency remain unmeasured.
- Hide the custom view: each spoken response still identifies the relevant action, amount/currency, outcome, and next step. Mute sound: visible facts and controls still allow completion.
- At every supported iOS/iPadOS text size, Mac enlargement through 200%, narrow/wide host layouts, long translated strings, and light/dark appearance: measure custom height ≤400 pt, readable essential fields, reachable controls, and successful detail fallback. Validate regional formatting with localization review.
- On supported Apple environments, exercise keyboard, VoiceOver, and applicable assistive inputs through confirmation, cancel, details, errors, and Done. Measure target geometry and actual contrast. Confirm host dialogue suppression, system button behavior, focus, state retention, and exact deep-link routing.

Only supplied local files and installed instructions were consulted. No web, device, SDK, GUI, accessibility runtime, payment service, or executable prototype was used. Official links identify the articles behind the installed snapshot; they were not fetched. Source guidance does not prove current API availability, bank-transfer support, authentication adequacy, regulatory compliance, live service behavior, measured layout, or accessibility conformance. No ongoing Live Activity is specified; adding continuing progress would require its own routed design and platform checks.
