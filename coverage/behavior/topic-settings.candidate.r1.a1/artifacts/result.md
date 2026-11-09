# Revised settings interaction specification

This is a framework-agnostic design for the iOS/macOS writing app described in `interface.md`. The brief establishes an 80-row mixed settings screen, global effects from document font changes, and editable switches for system permissions. It supplies no row inventory, code, screenshots, permission categories, account backend, or synchronization provider. Labels and defaults below are proposed product decisions, not observations of an existing implementation.

## Decisions and organization

Separate options by frequency and affected scope. Frequent formatting belongs beside the document; infrequent app configuration belongs in Settings; system authorization remains owned by the operating system. This follows [Settings: general settings, task-specific options, and system settings](https://developer.apple.com/design/human-interface-guidelines/settings).

| Destination | Contents and scope | Default and persistence |
| --- | --- | --- |
| Editor → Format | Everyday formatting supported by the app; active selection or insertion-point formatting only. Label the target “Selected text” or “Text you type next.” | Read from the current selection; retain document edits with that document. Mixed selections display “Multiple,” never an invented single value. |
| Document Setup → Document Font | Base font for the current document. Helper: “Changes this document only. Explicit text formatting is preserved.” | New documents copy the new-document default once; existing documents retain their own value. |
| Settings → New Documents | “Default font for new documents.” Helper: “Applies to documents you create next on this device. Existing documents keep their fonts.” | Proposed factory default: app-provided readable serif, 12 pt document size. Persist locally across launches; no implicit account sync. Document point size is distinct from interface text scaling. |
| Settings → Permissions | Read-only current authorization state for each permission actually used by an implemented feature, plus an appropriate system-settings action. | Query system state; never persist an app-owned permission boolean or copy permission state across devices. |
| Settings → Account | Signed-in identity, supported account actions, and a clearly labeled “Delete Account…” entry opening a dedicated consequence review. | Use authoritative account state. No destructive action from changing a preference. |

Do not invent replacements for the other unseen rows. Before implementation, inventory all 80 rows with frequency, scope, default, owner, persistence, and destination. Apply the table's rule to each; remove redundant system preferences rather than reproducing them. No arbitrary target row count is required. Additional categories require actual supplied options.

The device-local default policy is a deliberate conservative choice because no preference sync service is evidenced. If document synchronization exists, the document font travels as document data; changing a default on device A never rewrites an existing document on device B. Do not promise cross-device delivery without a verified transport. Preserve stored font identifiers when a font is unavailable locally: render with a disclosed fallback and do not silently rewrite the original choice. Factory defaults apply only when a value is absent. Migration must preserve current rendered document values; a new default must not retroactively reinterpret existing documents. Historical intended fonts cannot be recovered from the brief.

## Access and navigation

**iOS:** Put Settings in the library's clearly labeled app navigation. Open a Settings root with New Documents, Permissions, and Account destinations; each has a Back path. Editor formatting remains available through a labeled Format control adjacent to the editing area, including while the keyboard is shown. Document Setup is a secondary document action. Preserve document ID, selection, draft, and scroll position on a settings trip, orientation change, or app interruption. Back returns one level; returning to the editor restores its context. At narrow widths and enlarged text, allow labels to wrap and content to scroll rather than hiding completion/navigation. This applies [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices).

**macOS:** App menu → Settings… and Command-Comma open or activate one settings window, including with no document open. Use a stable, noncustomizable, always-visible pane selector for New Documents, Permissions, Account; select New Documents initially, restore the last visited pane locally thereafter, and title the window with its pane. Follow the settings guide's pane sizing and disabled minimize/zoom convention. File → Document Setup… targets the active document; disable it with no document. Format exposes supported selection formatting commands, including Font…, with toolbar equivalents using the same command handlers. Closing Settings leaves document windows intact. Switching active document windows changes the formatting target; an already-open document-setup editor stays bound to its named document. These choices follow [Settings: macOS](https://developer.apple.com/design/human-interface-guidelines/settings#macOS), [menu placement](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar), and [Mac conventions](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos).

Keep navigation and editing completion reachable as width changes. On Mac, hiding or customizing the editor toolbar must leave every toolbar action available in the menu bar; use system overflow when available, without adding a duplicate manual overflow. On iOS, preserve Format and navigation before secondary actions. See [Toolbars: grouping and platform considerations](https://developer.apple.com/design/human-interface-guidelines/toolbars).

## Control and state contracts

### Font choices and commits

Present an ordered, alphabetized font choice list near the affected value, showing the current choice and a preview. Only offer fonts supported by the implementation. The choices are single-selection values, not switches. A medium-length list can use a picker; a very large catalog needs a separately designed browsing treatment rather than an oversized wheel. This follows [Pickers: best practices](https://developer.apple.com/design/human-interface-guidelines/pickers#Best-practices).

Opening a font editor snapshots its target and committed value. A choice changes only its preview until Apply; Cancel, Back, outside dismissal where supported, or closing the editor discards that preview. Apply commits only to the captured target, then restores focus. Disable Apply when unchanged or unavailable. If the target closes, disable Apply and explain “This document is no longer open.” A persistence failure keeps the editor open with the prior committed value intact and an inline retry message; do not report success.

```text
Target = Selection(documentID, range) | Document(documentID) | NewDocumentDefault(deviceID)
openFontEditor(target): draft = copy(readCommitted(target))
chooseFont(value): validateSupported(value); draft = value; preview(target, draft)
cancel(): discardPreview(); restoreParentFocus()
apply():
  require targetStillValid() and draftIsValid()
  transaction:
    Selection -> update only captured text range / insertion attributes
    Document  -> update only document.baseFont
    Default   -> update only device.newDocumentDefaults.font
  on success: dismiss(); restoreParentFocus()
  on failure: retain committed state; show inline retry; retain draft
createDocument(): copy device defaults into independent document fields
```

Other real binary app preferences, if found in the row inventory, commit immediately and show their actual persisted state, with rollback/error feedback on failure. Use labeled row switches on iOS and established body checkboxes on Mac; state must be perceptible without color. Commands, font choices, and permission status are not binary app preferences. See [Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles).

### Permissions

Instantiate one row only after recording `{category, feature, minimum scope, data use, supported states, system destination}` from the actual implementation. The brief does not identify any category, so no camera, microphone, contacts, or notification request is assumed.

| Observed authorization | Display and allowed transition |
| --- | --- |
| Not requested | “Not requested.” Explain the specific feature that will request it; request through the OS only when that feature is invoked. |
| Granted / limited | “Allowed” or the actual limited scope. Feature uses only that scope; status row remains read-only. |
| Denied | “Not allowed.” Offer “Open System Settings” when a supported destination exists; otherwise give accurate manual instructions. Never flip an app switch to imply authorization. |
| Restricted / unavailable | Show the actual restriction or unavailable capability; explain the affected feature without promising an editable system state. |
| Query failed / unknown | “Status unavailable,” with refresh/retry. Do not equate unknown with denied or granted. |

Refresh on entering Permissions and returning to the app. A system-settings link does not mark access granted. Re-query at feature use because access may change while the app is inactive. Denial leaves ordinary writing available. If a system prompt is supported, explain purpose in a specific complete sentence naming actual use and reason; do not fabricate that sentence before the feature/data inventory exists. No startup permission batch or imitation Allow switch. These decisions apply [Privacy: requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

### Account deletion

Account → Delete Account… opens a review page identifying the account, exactly which stored content is deleted across devices, any locally retained/exported copies, expected completion time, and verified retention exceptions. These facts must come from the backend policy; unresolved fields block shipping this flow. Offer Back and any existing export route without making export a prerequisite. Signed-out users see accurate signed-out state rather than an active deletion command.

After review, Delete Account opens the final confirmation: title “Delete Account?”; message “This will permanently delete [verified data scope] for [account]. [Verified timing and retention statement].” Brackets are required integration fields, never release copy. Actions: Cancel and Delete Account. Use no default action, intentionally requiring explicit activation; Return alone does nothing. Escape/Command-Period cancels where supported. Use platform button placement, not a copied universal order. This is an uncommon irreversible action; [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) permits confirmation and considering no default for deliberate reading, while also allowing a normal default for explicitly requested destruction.

On confirmation, send one idempotent deletion request; prevent duplicate submissions. Pending is a visible state, not completion. On definitive failure preserve account and document context, explain the failure, and offer Retry. On ambiguous network failure query request status before retrying. Leaving and returning restores request status, not a fresh confirmation. Mark complete and end account access only after server confirmation; notify completion through an actual supported channel. If subscriptions exist, explain that deletion does not itself cancel Apple auto-renewable billing and offer separate management without blocking deletion. If Sign in with Apple exists, include token revocation in the backend contract. No authentication method or billing service is assumed. See [Managing accounts: deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts).

## Worked before → after

**Before, as reported:** A person editing document A traverses the mixed 80-row settings screen to change its font. Document B changes too. Permission switches imply app control over OS authorization; account deletion shares the everyday settings list.

**After, concrete scenario:** A and B both have a 12 pt serif base font. In A, open Document Setup → Document Font, choose an available sans-serif font, and Apply. A changes; B and the new-document default remain 12 pt serif. Canceling the same operation produces no change. Next, Settings → New Documents changes the default to that sans-serif font; newly created C receives it, while A and B retain their stored values. On another device the default remains its own value; a synchronized copy of A, if sync is supported, retains A's document font. Permissions displays “Not allowed” from the OS; opening system settings and returning without changing access leaves that status unchanged. Account deletion requires the separate Account review and explicit confirmation before any request is sent.

## Acceptance checks and evidence

**Passed — specification inspection:** The revised contract separates all four scopes; specifies defaults, persistence, restoration, commit/cancel/failure behavior; includes iOS and Mac access; and separates OS status from app state. The worked example predicts independent values for A, B, C, and device defaults. Installed root, owning family procedures, selected topic procedures, and supporting guides were read locally in that order; topic-index searches informed routing. No web access was used.

**Failed — supplied baseline description:** Document independence and truthful permission ownership fail according to `interface.md`. Frequent task controls are misplaced in the mixed settings screen. These are reported design defects, not reproduced runtime failures. Account deletion's backend correctness cannot be classified from its placement alone.

**Not executed — implementation acceptance scenarios:**

1. Create A and B; change A's base font, relaunch, reopen both, and confirm B/default unchanged. Change a default; create C; verify old documents remain unchanged. Cancel each font editor and inject save failure; verify no partial commits. Test mixed selection, missing font, missing default, migration, and captured document closing.
2. On each device verify device-local defaults and pane restoration. Where document sync exists, round-trip A's font without touching other documents; disconnect/reconnect and inspect actual delivery/conflict behavior. Sync transport and conflict resolution require a separate verified contract.
3. On iOS enter Settings and return to a draft; interrupt/resume, rotate, show keyboard, and enlarge text. Verify selection/draft/scroll context, reachable Format/Back/Apply, and no conflicting swipe-back behavior. Touch comfort requires device testing.
4. On Mac use Command-Comma with zero/two documents; restore the last pane; hide/customize the editor toolbar; resize and switch active windows/apps. Complete each supplied action through menus and keyboard and confirm the correct document target.
5. Exercise every supported permission state, external revocation, query failure, unsupported deep link, and return without changing permission. Verify no false grant or unrelated writing gate, and that each request is timely and minimal.
6. Cancel account review and final confirmation; verify zero requests. Exercise Return, Escape, pending, repeated submission, offline/ambiguous response, definitive failure, relaunch, and completion. Verify actual deletion, retention, billing copy, and supported completion notification against backend evidence.
7. Once controls exist, verify readable wrapped labels, meaningful names/values, focus restoration, noncolor state, keyboard operation, and assistive-technology navigation on both platforms. The written specification cannot establish those outcomes.

Only local prose and installed guidance were inspected. No application, GUI, device, SDK build, accessibility session, permission prompt, account deletion, or sync execution occurred. Official links above identify the sources recorded in the installed snapshot; they were not fetched or checked for current changes. The snapshot is derived guidance, not an SDK guarantee or legal/security certification. The 80-row inventory, actual font catalog, migration data, permission/data-purpose matrix, deletion policy/timing, and any synchronization implementation remain integration evidence needed before release. The menu guide notes conflicting custom-menu ordering wording; this design uses the named standard menus and introduces no custom ordering rule.
