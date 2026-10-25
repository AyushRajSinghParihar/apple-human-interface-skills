# Revised writing-app settings interaction specification

## Scope and decisions

This is a framework-agnostic design for iOS and macOS, based on `interface.md`. The observed specification describes an 80-row screen mixing frequent formatting and account deletion, a document font change affecting other documents, and editable switches representing system permissions. No screen, implementation, complete row inventory, permission categories, or backend contract was supplied.

The following are product decisions informed by the installed HIG snapshot; the exact grouping, persistence model, and labels are proposed design choices, not universal Apple requirements.

| Concern | Revised location and effect | Initial value and persistence |
| --- | --- | --- |
| Frequent formatting | Editor → Format; acts only on the active editing target. Label scope explicitly: “Selected text” or “Text you type next.” | Read current selection/insertion style; show “Multiple fonts” for mixed selections. Store edits in that document only. |
| Whole-document font | Editor → Document Settings → “Document font,” with “Applies to this document.” On Mac also File → Document Settings… | Read the document's stored font. Apply only to that document; never change the new-document default. |
| Default font | Settings → Writing → “Font for new documents,” with “Existing documents keep their fonts.” | Default is “App default.” Copy its resolved font into each new document at creation; existing documents never reference a mutable preference. |
| Other infrequent app preferences | Settings, grouped by effect after inventory; include only supported, useful options | Preserve existing choices; detect capabilities and respect system preferences rather than duplicating them. |
| System permission | Settings → Permissions → category name plus read-only status and relevant action | Query the OS on entry and return to the app. Never persist a supposed authorization boolean or sync it across devices. |
| Account deletion | Settings → Account → Delete Account… → review → confirmation | Account-wide operation, distinct from local preferences and document deletion. No action until explicit confirmation. |

Keep only three justified top-level destinations initially: **Writing**, **Permissions**, and **Account**. Do not redistribute the unknown remainder of the 80 rows blindly. Inventory each remaining row as command, document setting, app preference, system-owned state, or obsolete/duplicated option; record owner, frequency, default, storage, and migration before shipping. Avoid adding empty categories or speculative settings.

HIG basis: keep settings small, frequent options beside their effect, and rare app-wide preferences in settings; respect system preferences ([Settings: Best practices, General settings, Task-specific options](https://developer.apple.com/design/human-interface-guidelines/settings)). A toggle represents state rather than a command; its appearance alone cannot authorize system access ([Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles)).

## Access, navigation, and restoration

**iOS:** A labelled Settings destination in the document library opens the three-category list. Each row opens its page; Back and swipe-back return through the same hierarchy. Opening settings preserves the current document, selection, insertion style, and unsaved draft. Frequent Format access stays in the editor, reachable without visiting Settings. Closing formatting returns to the same selection. Returning from another app restores the document and route. Portrait, landscape, and enlarged text retain this hierarchy and allow content to scroll without hiding the completion or Back controls.

**macOS:** App menu → Settings… and Command-Comma open or focus one settings window. Use a stable, noncustomizable pane selector for Writing, Permissions, and Account; keep the active pane visible and use its name as the window title. Restore the last ordinary pane on reopening, never a confirmation or pending destructive operation. Follow the local settings guide's dimmed minimize/zoom convention. Closing Settings returns to the previously active document window. Settings access does not depend on a customizable editor toolbar. Format → Font… and supported formatting commands act on the active document/selection; with no editable document, keep them visible and disabled. File → Document Settings… acts on that document. Multiple document windows retain independent targets.

All settings and formatting routes must have a keyboard completion path. Switching applications, resizing, or hiding optional editor controls must preserve the target and leave commands reachable. No native menu or keyboard integration is claimed by this specification.

HIG basis: [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices), [macOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices), [Settings: macOS](https://developer.apple.com/design/human-interface-guidelines/settings#macOS), and [The menu bar: App, File, and Format menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar). The local menu-bar guide notes conflicting general/specialized custom-menu ordering language; this design uses the documented standard menu scopes and introduces no custom menu order.

## Formatting and persistence contract

Separate rich-text selection styling from a document's base font. “Document font” changes the base style and text inheriting it; explicitly formatted spans retain their overrides. Explain this on the document page: “Changes text using the document font. Individually formatted text keeps its font.” If the product uses uniform-font documents instead, omit selection-font editing and apply Document font to the entire active document. This choice must match the actual document model before implementation.

Font selection commits on explicit “Apply”; “Cancel,” Back, or dismissal discard the uncommitted candidate. The selected target document and range are captured on opening. If that document closes or becomes read-only, disable Apply and explain why; never retarget another document silently. After Apply, restore editing focus. A normal document edit may use the existing undo mechanism; this proposal does not assert one exists.

Writing preferences apply immediately after successful local persistence, without a global Save button. On persistence failure, retain the previous effective value and show an inline error with Retry. Closing a page does not discard successfully saved preferences.

```text
createDocument():
    font = resolve(preferences.newDocumentFont or AppDefault)
    document = { id: newId(), baseFont: copy(font), content: empty }
    persist(document)

applyDocumentFont(targetId, candidate):
    require targetId exists and is editable
    persistDocumentChange(targetId, baseFont = candidate)
    // No writes to other documents or preferences.

setNewDocumentFont(candidate):
    persistPreference(newDocumentFont = candidate)
    // No writes to existing documents.
```

Proposed cross-device boundary: document formatting travels with the document through whatever document transport already exists. App preferences remain device-local in this revision; Writing explicitly says “On this device.” Permission status and last visited pane are always device-local. Account deletion is account-wide. Do not add iCloud or another synchronization technology by assumption. If preference sync is later required, define conflict and offline behavior separately; never restore live links from existing documents to a shared default.

Migration: preserve each document's last stored/resolved font by materializing it into its own record before disconnecting any global font reference. Preserve the old global value as the local new-document default. If historical per-document choices were already overwritten and no versions exist, recovery cannot be promised. Do not silently reset existing documents to App default. For an unavailable font on another device, preserve its identifier, show an explicitly labelled temporary display fallback, and avoid rewriting the stored font merely on open.

## System permission state machine

The permission inventory is unknown. Create a row only for an implemented feature that actually needs protected access. Each row must map a real category to its feature, minimum access, purpose sentence, OS status reader, and supported request/settings action. No new camera, microphone, contacts, notification, or tracking feature is implied here.

| Detected state | Row presentation | Behavior |
| --- | --- | --- |
| Not requested | “Not requested” | “Use [feature]” opens that feature; request minimum access only when invoked. |
| Allowed, including limited access | Accurate scope such as “Allowed” or “Limited access” | Use only granted scope; provide management action where supported. |
| Denied | “Not allowed” | Offer “Open Settings” on iOS or “Open System Settings” on Mac when supported; otherwise provide category-specific instructions. Do not repeatedly prompt. |
| Restricted | “Restricted by system policy” | Explain that app controls cannot change it; preserve unrelated editing. |
| Unsupported / unavailable | “Unavailable on this device” | Explain the affected feature; do not offer a fake enable control. |
| Query pending / failed | “Checking…” / “Status unavailable” | Do not display assumed authorization. Offer Retry for failure. |

Entering Permissions does not request access. After a system prompt, app activation, or return from system settings, re-query before updating the label or using protected data. Canceling a request leaves ordinary writing available. Recheck authorization at feature execution, because access can change while the app is open. If opening system settings fails, retain the app route and show useful manual instructions. Do not hard-code unverified OS paths or promise a deep link for every category.

Purpose copy template, to be completed with actual data use: “Use [specific data] to [specific user-requested result].” No generic “better experience” text. Usually the feature context is sufficient; add a custom pre-permission explanation only when essential, with one Continue action leading to the real system prompt, without imitating consent choices. No protected collection before required consent.

HIG basis: [Privacy: Requesting permission and Pre-alert screens](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). These rows report system-owned facts; replacing them with disabled switches would still obscure ownership.

## Account deletion interaction

Account shows the current account identity and a distinct Delete Account… action. Signed-out users see their signed-out state; do not fabricate an account or require sign-in for otherwise available local writing.

1. Open a review page naming the account. Explain exactly which account data/documents are removed across devices, which local files survive, retention exceptions, expected completion time, and notification method. These values must come from a verified service policy. Do not ship placeholders or a false immediate-completion promise. Offer a data-preservation/export route only if supported.
2. If subscriptions exist, show separate management instructions and state that account deletion does not itself cancel Apple auto-renewable billing. Externally purchased subscriptions must not block deletion. If no billing exists, omit this section.
3. “Continue to Delete” opens the final alert: **“Delete Account?”** Message: “Delete [account identity] and the account data described on the previous page? This cannot be undone.” Actions: **Cancel** and **Delete Account**. Use no default action so Return alone cannot submit; Escape/Command-Period cancels where supported. Use platform-appropriate ordering. This is a deliberate-reading product choice: HIG also permits a normal default for explicitly requested destruction; it does not universally require Cancel to be default.
4. Cancel returns to review without mutation; Back/close before submission returns safely. Confirmation submits one idempotent deletion request, showing “Requesting deletion…” and preventing duplicate submission. Closing this view does not undo an accepted request. If authentication is necessary, use the service's existing supported method; cancellation returns without deletion.
5. Distinguish request rejection, unknown outcome after connection loss, accepted/pending, and completed. On unknown outcome, query the operation before retrying. Keep the same operation identifier for retries. Do not claim completion merely because a request was sent. Pending status survives reopening and is checked with the service. Notify completion by the disclosed supported channel; remove credentials/session on confirmed completion. Revoke Sign in with Apple tokens if that integration actually exists.

Backend deletion, timing, offline status access, retention, and completion notifications are unresolved integration requirements. The design requires a real deletion path rather than deactivation or a policy link. Destructive review must remain reachable without an active subscription-management detour.

HIG basis: [Managing accounts: Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts) and [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons). Ordinary preference changes do not trigger confirmation alerts.

## Worked before/after

Example values below are illustrative, not observations of the supplied UI.

**Before:** A writer opens document A and traverses the 80-row Settings screen to change its font to Georgia. Document B unexpectedly changes too. A permission switch appears editable even though authorization belongs to the OS. Account deletion is mixed into the same list of routine controls.

**After:** A and B each store their existing font, for example App default. In A, the writer opens Document Settings, sees “Applies to this document,” chooses Georgia, and applies. A's inherited text changes; B remains unchanged. On Mac, opening B in another window and switching focus does not retarget A's pending font edit. Settings → Writing → Font for new documents changes the local default to another font; a newly created C receives it while A stays Georgia and B stays unchanged. Opening C on another device preserves C's stored font even if that device has a different new-document default.

Settings → Permissions shows the OS-reported status as text. Invoking the relevant feature requests access only if appropriate. Returning from a denied request preserves the draft; opening system settings and returning refreshes status. Settings → Account → Delete Account… opens a separate review; Cancel at final confirmation leaves the account and documents intact.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** All three reported scope defects have explicit replacements; document and default writes have separate owners; iOS and Mac access paths are specified; permission rows cannot mutate OS status; deletion includes cancellation, pending, error, and completion states. Installed root, selected families, routed procedures, and supporting local guides were read in that order, one file per shell command. Official links above identify the local snapshot's sources; no web lookup was performed.

**Failed — supplied design contract:** The stated global effect of a document font fails per-document independence. Editable app switches for system-owned authorization fail truthful ownership. The mixed 80-row screen fails the proposed placement contract. These findings describe the supplied text, not observed runtime failures.

**Not executed — implementation acceptance gates:**

| Check | Required observable result |
| --- | --- |
| Defaults and migration | Fresh install resolves App default; existing documents retain last stored appearance after migration; setting a default only changes subsequently created documents. |
| Independent documents | Apply Georgia to A, reopen A/B, and open B in a second window: only A changes. Cancel a candidate: neither changes. A closed/read-only target never redirects to B. |
| Persistence errors | Failed preference/document storage retains prior effective state and exposes retry without false success. |
| Cross-device scope | Transfer A/C: stored font follows each document; changing one device's new-document preference leaves other preferences and existing documents unchanged; fallback does not overwrite metadata. |
| Settings restoration | Mac app menu and Command-Comma open/focus Settings and restore the last pane; closing never replays deletion. iOS Back/swipe-back restores route and draft. |
| Permissions | Exercise every supported OS state, return from settings, failed status query, unavailable capability, and revocation during use. Labels match OS facts; collection waits for consent; unrelated writing continues. |
| Deletion | Cancel at each pre-submit exit; test guest, linked sign-in, subscriptions if present, rejected request, offline/unknown outcome, repeated activation, and completion. No duplicate operation or false completion/billing claim. |
| Desktop commands | No document, multiple windows, hidden editor controls, keyboard-only use, and app reactivation preserve correct enablement and target. |
| Presentation and input | Portrait/landscape, enlarged text, narrow Mac settings panes, Return/Escape behavior, focus return, and noncolor state interpretation preserve all actions and scope labels. |

No device, SDK, GUI, backend, keyboard, assistive-technology, accessibility, or physical-comfort execution occurred. The specification is not proof of native rendering, accessible announcements or focus order, secure storage, legal compliance, synchronization, or deletion enforcement. The installed guidance is a dated derived snapshot, not SDK documentation or evidence of independent source review. Full row mapping, exact font behavior, permission categories, and deletion disclosures require the missing product inventory and service contracts before implementation can be accepted.
