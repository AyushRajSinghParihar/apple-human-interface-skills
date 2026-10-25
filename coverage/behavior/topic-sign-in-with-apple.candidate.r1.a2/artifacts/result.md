# Sign in with Apple entry audit

Scope: iPhone volunteering app, iOS. Evidence is the single paragraph in `interface.md:1`, not a running interface. “Verified” below means explicitly stated in that supplied specification. Severity ranks are review judgments, not Apple severity classifications.

## Ranked findings and decisions

| Rank | Verified observation | Effect and correction | Basis |
| --- | --- | --- | --- |
| 1 — Critical | “Cancel is reported as authentication success.” | The result misrepresents the person's choice; downstream access consequences are unknown. Cancel must return to the entry context without a new session, account mutation, or success event. Only a verified successful result may complete authentication. | [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role): Cancel abandons the current action. The success gate is an engineering correction, not a token-validation algorithm supplied by HIG. |
| 2 — High | Missing name on return silently creates duplicate accounts. | This fragments volunteer identity and may separate existing commitments/history. Resolve the established identity independently of optional profile fields; preserve the existing account and stored name when a return result omits it. Offer an explicit, authenticated linking route for a separate existing account. | [Sign in with Apple — Offering](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Offering-Sign-in-with-Apple) supports linking rather than duplicate identity. Stable identity resolution, uniqueness, and idempotency below are proposed engineering decisions. The brief does not establish when Apple supplies names. |
| 3 — Medium | Users must retype their private relay email. | Adds redundant entry and typo risk. Consume the verified supplied email when present, retain an existing stored address when absent, and show the relay address in account/support details. Never substitute a demand for the underlying personal address. | [Sign in with Apple — Collecting data](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Collecting-data), [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). Retyping a relay address alone does **not** prove relay rejection or collection of the underlying address. |
| 4 — Medium | The sign-in button replaces Apple branding with the app mascot. | Obscures the authentication provider. Restore recognizable Apple identity and an approved title. Keep the mascot outside the authentication control if desired. | [Sign in with Apple — Displaying buttons](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Displaying-buttons) and [custom button rules](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Creating-a-custom-Sign-in-with-Apple-button). |

## Corrected entry and data contract

Use the consistent visible title **Sign in with Apple**. Activation starts authentication; it does not itself signal success. Prefer a system-provided button when available. No Apple SDK is assumed here: a custom implementation must use Apple-supplied padded logo artwork, approved black/white logo and title, and the documented proportions. Do not redraw the logo or ship a mascot substitute while assets are unavailable.

For a proposed light entry background, use the supported black button with white title/logo; verify actual contrast. Use a rectangular text button, matching neighboring corner treatment. Proposed size: at least 140 × 44 pt, expanding for localization, with at least 4.4 pt outside clear space at that height. The specific Sign in with Apple visual minimum is 140 × 30 pt with one-tenth-height clear margins; the general [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) recommends at least 44 × 44 pt hit regions. These describe different constraints; the proposed 44 pt height satisfies both. Keep it at least as prominent/large as other sign-in methods and visible without scrolling. Actual geometry, other methods, title, and placement are not supplied and are not findings.

Control inventory: the entry command maps to Buttons plus Sign in with Apple; the implied relay re-entry control maps to Text fields and is removed from this flow; the reported cancellation outcome maps to the Cancel action contract. Its visual surface and owner are unknown. No missing label, keyboard, target-size, or focus defect can be inferred. [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) informed inspection of the implied input, rather than justification for retaining it.

| Data | Purpose and handling decision |
| --- | --- |
| Verified provider identity | Resolve the volunteer account; never use name or typed email as its identity key. |
| Chosen relay/shared email | Contact/support where actually needed; retain supplied choice, display it in account details, no re-entry or underlying-address requirement. Actual contact delivery remains untested. |
| Name | Display profile information, separate from identity. Preserve an existing value when absent; use a neutral welcome if unavailable. Any later optional profile request must explain its benefit and permit decline without blocking account use. |
| Additional password | Do not request one for Sign in with Apple. No such request is alleged in the supplied interface. |

Account necessity and entry timing are unknown. As a design recommendation, allow browsing opportunities without an account if feasible, and explain why an account is needed at a commitment step such as saving a volunteering registration. This is conditional on product requirements, not a verified gating defect. See [Managing accounts — Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices). Account deletion and authentication-method identification in settings need inspection in the wider account flow; absence from this paragraph is not evidence they are missing.

## Framework-agnostic state specification

The authentication adapter and verifier are abstract dependencies. Their secure implementation, provider identity scope, credential lifecycle, and available platform APIs require separate implementation documentation and security validation.

```text
state = ENTRY
on activateApple:
  if state != ENTRY: ignore duplicate activation
  remember entry context and intended volunteering action
  state = AUTHORIZING
  request adapter authentication with fresh attempt identifier

on adapterResult(attempt, outcome):
  if attempt is stale or already completed: ignore
  if outcome == CANCEL:
    finish attempt; state = ENTRY
    restore prior context; emit no authentication-success event
    perform no account/session write
  else if outcome == FAILURE:
    finish attempt; state = ENTRY
    show recoverable failure with retry; retain context
  else:
    state = VERIFYING
    verified = verifier.validate(outcome, attempt)
    if validation fails: return recoverable failure; no account/session write
    else:
      transaction:
        account = lookupByVerifiedProviderIdentity(verified.identity)
        if found:
          preserve stored name/email when result fields are absent
        else if person explicitly requests linking to an existing account:
          require proof of control of that account before linking
          if proof is absent or fails: do not link or silently create duplicate
        else:
          create once under a unique verified-provider-identity constraint
        persist only supplied, permitted profile values
      create session only after resolution succeeds
      finish attempt; state = SIGNED_IN
      emit success once; welcome and resume intended volunteering action
```

During authorization/verification, prevent repeated activation and retain the entry context. Represent delayed work visibly; for an app-controlled activating button follow the iOS activity-indicator guidance in [Buttons — iOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), while retaining approved provider branding in its idle state. Verification/network failure returns to retry without claiming success. A late callback after cancellation must not create an account. Concurrency-safe resolution and authenticated linking are engineering recommendations, not security guarantees from the HIG snapshot. Never merge accounts solely because email strings match.

## Worked before/after

Illustrative fixture: volunteer account V17 already has a verified Apple identity I17, a stored relay address, and an upcoming shift. The fixture is proposed, not observed user data.

**Before:** The volunteer taps the mascot sign-in button and must retype the relay address. A return result without a name silently creates V18. The existing shift may consequently appear missing. On a separate attempt, choosing Cancel is reported as success.

**After:** The volunteer taps **Sign in with Apple**, using approved Apple branding. A verified return result with identity I17 and no name resolves V17, preserves its stored profile and shift, and resumes the intended task without email typing. If the person instead cancels, they return to the same entry context; V17 and its shifts are unchanged, no new session is created, and no success is reported. A successful first-time identity creates one account; lack of optional name does not block useful work.

## Acceptance checks and results

**Failed in the supplied specification:** Cancel abandons authentication; returning identity retains one account despite missing name; relay email needs no re-entry; provider branding remains recognizable. All four checks fail based on `interface.md:1` only.

**Passed by static document review:** Each reported defect has a ranked correction; the proposed contract separates cancel, failure, verification, and success; it preserves missing profile values and removes relay re-entry. These are specification checks, not implementation passes.

**Not executed — required implementation acceptance checks:**

| Scenario | Expected observable result |
| --- | --- |
| Cancel, including a late success callback | Same entry context; zero new sessions/accounts/profile writes/success events. |
| Return as I17 with name and email absent | V17 retained; stored profile and volunteering records intact; no duplicate. |
| First verified identity, no name | One usable account; neutral welcome; no required name/password/relay re-entry. |
| Retry, repeated tap, duplicate callback, concurrent successful requests | At most one account per verified identity and one completion per attempt. |
| Invalid credential, verifier failure, network interruption | No authenticated success; understandable recovery and retry. |
| Explicit existing-account linking, with/without account-control proof | Successful authorized link preserves existing records; absent/failed proof never merges accounts. |
| Relay chosen | Same address accepted and displayed for support; no underlying-address demand; separately verify actual mail delivery. |
| Button at supported sizes/locales/appearances | Approved artwork/title, documented margins, at least 44 × 44 pt hit region, no overlap/clipping, sufficient contrast, equal prominence and no-scroll visibility relative to other methods. |

## Evidence limits and reading trail

Only `interface.md` supplies interface evidence. No screenshot, implementation, layout measurements, backend records, assets, or executable prototype was supplied or run. No device, SDK compilation, GUI, accessibility, biometric, relay-delivery, or security execution is claimed. Accessible naming/order and native rendering remain unverified; this audit establishes no accessibility violation or conformance result.

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, searched its `references/topic-index.md`, then read each selected family and topic procedure before its reference. Routes used: Technologies → Sign in with Apple; Menus and actions → Buttons; Patterns → Managing accounts; Foundations → Privacy; Selection and input → Text fields. Paths were resolved within that installed package, with one file per shell read command.

Guidance came exclusively from those installed local references, dated 2026-10-25; the Sign in with Apple reference records a source revision of September 14, 2022. Official links above identify the material guidance but were not opened. No web browsing, independent source review, current API verification, or App Review approval is implied. The pseudocode is a proposed behavior contract, not a deployable authentication implementation.
