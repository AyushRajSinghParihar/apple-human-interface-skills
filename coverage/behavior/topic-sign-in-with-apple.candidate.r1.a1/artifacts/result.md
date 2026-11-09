# Sign in with Apple entry audit

Scope: iPhone volunteering app; review of `interface.md` only. “Verified” below means explicitly stated in that supplied brief, not reproduced in software. Severity is this review’s product judgment. No SDK is assumed.

## Ranked findings and decisions

| Rank | Verified observation | Effect and decision | Guidance |
| --- | --- | --- | --- |
| 1 — High | Cancel is reported as authentication success. | Misrepresents consent and session state. Treat cancellation as a separate terminal outcome: return to the prior entry context, create no account/session, and show no success message. Whether unauthorized access actually occurs is unknown. | [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) defines Cancel as abandoning the action. Session gating below is an engineering correction, not an HIG security algorithm. |
| 2 — High | A missing name on return silently creates duplicate accounts. | Fragments the volunteer’s identity and potentially their saved work. Resolve the authenticated provider identity to the existing account independently of profile name. Preserve stored data when returned fields are absent. Offer explicit, authenticated linking for an existing app account; never silently merge based on name/email. | [Sign in with Apple: Offering](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Offering-Sign-in-with-Apple) supports existing-account linking. Stable-identity lookup, atomic uniqueness, and merge safeguards are proposed engineering decisions. |
| 3 — Medium | People must retype their private relay email. | Adds unnecessary work and opportunities for mismatched identity. Use the address supplied through the authenticated flow; do not require re-entry or the underlying personal address. Display the stored relay address in account/support information when available. The brief does **not** say the app demands the underlying address. | [Collecting data](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Collecting-data), [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). |
| 4 — Medium | The sign-in button replaces Apple branding with the app mascot. | Obscures the authentication provider. Restore approved Apple artwork and an approved title. Keep the mascot elsewhere in app content. Prefer a system-provided button when available; a permitted custom button must follow the supplied-artwork rules. | [Displaying buttons](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Displaying-buttons), [Custom button](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Creating-a-custom-Sign-in-with-Apple-button). |

## Corrected entry and data contract

Use the title **Sign in with Apple** consistently. It opens authentication; pressing it alone never establishes success. Use the supported black style on a light background or white style on a dark background with sufficient contrast. Select actual appearance after inspecting the missing screen. Keep it visible without scrolling and at least as prominent/large as other sign-in methods, if any.

For a custom text button, use only Apple-supplied padded logo artwork, black/white logo and title, a rectangular shape, intact logo proportions/padding, and the source’s title/layout rules. Do not substitute a mascot or redraw the mark. Specify a 44 pt-high button with width at least 140 pt, expanding for localization; keep external clear space at least one tenth of height (4.4 pt here). Preserve at least 8% of width between title and trailing edge. The Apple-specific visual minimum is 140 × 30 pt; the general selectable region should be at least 44 × 44 pt. These are distinct constraints, not conflicting minima. See [button geometry](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Button-size-and-corner-radius), [custom text layout](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Custom-buttons-with-a-logo-and-text), and [general targets](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

Map supplied controls: the Apple entry is an immediate authentication-launch button; Cancel is an abandon-action control. The provider/system flow owns its cancellation UI when available. No extra confirmation is needed to cancel. Actual labels, roles, hit regions, focus, and rendering are not supplied.

| Data | Purpose | Corrected handling |
| --- | --- | --- |
| Verified provider identity | Resolve the volunteer account | Use a validated stable provider identifier in its appropriate identity namespace; enforce one mapping per identity. Do not use display name as a key. |
| Relay/shared email | Account contact/support | Accept the chosen relay address; store supplied data appropriately, do not require retyping, and do not solicit its underlying address. If absent on return, retain the existing value. |
| Name | Optional profile display; no mandatory purpose supplied | Preserve an existing name when absent; a new account may use a neutral display such as “Volunteer.” Offer an optional edit after useful engagement without blocking use. |

Minimize collection and explain actual uses. No volunteer-task requirement for extra personal data is evidenced. Do not add a password requirement. Review privacy disclosures if collection/use changes. These decisions follow [Collecting data](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Collecting-data) and [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Framework-agnostic behavior

The following is a behavioral contract, not token-validation or SDK implementation code. A platform/provider adapter must supply supported authentication and verified outcomes; this document does not implement that adapter.

```text
state = entry
context = prior navigation and intended volunteering task

on AppleButton.activate when state == entry:
    state = authenticating
    start one authentication attempt; ignore duplicate activation

on adapter.cancelled for current attempt:
    invalidate attempt
    state = entry
    restore context; no account write, session, or success feedback

on adapter.failed or verification failed for current attempt:
    invalidate attempt
    state = entry
    show recoverable sign-in failure with retry; preserve context
    no account creation or authenticated session

on adapter.verified(identity, optionalProfile) for current attempt:
    state = resolving
    atomically resolve unique (provider, identityNamespace, stableIdentifier)
    if mapping exists:
        select mapped account
        preserve stored profile fields absent from optionalProfile
    else if person requests linking to an existing app account:
        require proof of control of that app account
        link only after explicit confirmation; reject identity conflicts
        cancellation/failure leaves both accounts unchanged
    else:
        create one account and identity mapping atomically
        name/email absence does not trigger a second creation
    on resolution failure: return to entry with retry; no success
    on committed resolution:
        establish session for resolved account
        state = signedIn
        welcome person and resume intended task

ignore stale callbacks after an attempt is cancelled or resolved
```

Linking must be discoverable from entry/account settings; matching an email can suggest linking but cannot by itself authorize it. Account settings identify “Sign in with Apple” as the method. These implement [Offering Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Offering-Sign-in-with-Apple); concurrency and callback safeguards are proposed engineering behavior.

For delayed resolution, provide visible pending feedback and prevent repeated activation. Prefer supported button pending states; do not invent a branding alteration for an unavailable API. Exact pending rendering needs implementation review. [Buttons: iOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

## Worked before/after

Scenario: a returning volunteer already has account V17 associated with Apple identity A. The return result omits name; the stored contact is a relay address.

**Before, from the brief:** mascot entry → relay re-entry → absent name causes new account V18. Alternatively, Cancel is reported as success. Loss of specific volunteer records is a risk, not an observed fact.

**After, specified:** approved Apple entry → verified A → resolve V17 → preserve its existing name/relay address → resume the intended volunteering task. No email prompt and no V18. If the person cancels instead, return to the prior entry context with no new session, account write, or welcome. A genuinely new verified identity may create one account even without a name; subsequent returns resolve that same account.

## Acceptance checks and status

**Passed — document/static work:** read the supplied brief; all four findings trace directly to it; corrected contract distinguishes cancel/failure/success and names optional data separately. This is specification coverage, not an app test pass.

**Failed — supplied behavior:** cancellation semantics, returning-account continuity, relay-entry friction, and provider branding fail the specified criteria as described in `interface.md`.

**Not executed — implementation acceptance checks:**

| Check | Required observable result |
| --- | --- |
| Cancel, including late callback | Prior context restored; no success, new session, account creation, or stale completion. |
| Return with absent name/email | Same account identifier and volunteer records; existing profile fields retained; no redundant form. |
| New identity with absent name | Exactly one account; no mandatory name prompt; later return resolves it. |
| Repeated taps/concurrent callbacks/retry | One attempt and one committed identity mapping; failures remain retryable without duplicates. |
| Existing-account linking | Explicit proof of control and confirmation; conflict/cancel leaves mappings unchanged; no email-only merge. |
| Provider/verification/network failure | No authenticated success; understandable retry; intended task preserved. |
| Relay choice | Authentication/account use works without underlying email or retyping; stored relay is usable for support. Actual mail delivery needs separate evidence. |
| Button rendering and interaction | Approved artwork/title/style, intact padding, stated geometry and clear space, press feedback, visible prominence, localized text without clipping. |
| Account context | Explain account value and defer sign-in if useful unregistered browsing is possible; show actual method in settings. Inspect deletion route if account creation exists. |

The account-context checks follow [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices) and [Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts). Entry timing, other sign-in methods, guest access, deletion, and settings are not supplied, so their absence is **not** a verified defect.

## Evidence limits and route

Local-only audit; no web access. Official links above are citations carried by the installed guides, not pages fetched during this task. Read the installed root `apple-hig/SKILL.md`, searched `references/topic-index.md`, then read the owning family and topic procedure before each supporting guide: Technologies → Sign in with Apple; Patterns → Managing accounts; Foundations → Privacy; Menus and actions → Buttons. Paths resolve beneath `.agents/skills/apple-hig/`. References describe a 2026-10-25 snapshot and are application guidance derived from Apple, not an SDK reference or proof of current API availability.

Only a short prose brief was supplied: no screenshot, source implementation, assets, credentials, identity schema, backend logs, or test harness. No device, SDK compilation, GUI, accessibility execution, token validation, linking security, biometric behavior, relay delivery, or runtime account persistence was tested. Accessibility names/order, actual target geometry, contrast, localization, and pending rendering remain unknown; no failure is inferred from those omissions. The contract requires later implementation/security validation and visual/assistive-technology inspection before release. No actual app fix or existing-duplicate migration is claimed.
