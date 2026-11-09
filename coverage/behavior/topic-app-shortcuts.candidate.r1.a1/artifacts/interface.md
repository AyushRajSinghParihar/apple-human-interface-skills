# Grocery app: Add Item App Shortcut

## Scope and discovery

Target: iOS. Preserve adding groceries to a shared weekly list while hands are occupied. This is an interaction specification, not SDK implementation. The app's name is unspecified; `{AppName}` below means its actual localized display name, not literal placeholder text.

Supply one broadly useful App Shortcut, **Add Item**, first in the app's initial shortcut ordering. Make it available with installation, without requiring people to build a custom shortcut first. Use a checklist SF Symbol for the system entry. Siri, Spotlight, and Shortcuts are the intended discovery/invocation surfaces; actual placement and personalization belong to the system and are not guaranteed.

After the second successful in-app add to the same list, show one dismissible contextual tip: “Add groceries with Siri. Try ‘Add an item with {AppName}.’” Offer “View in Shortcuts” to the app's shortcut collection where supported. Record dismissal; do not repeat automatically. The two-add threshold is a product choice, not an Apple requirement. Keep the ordinary in-app add flow available.

Activation phrase variants:

- “Add an item with {AppName}.”
- “Add groceries with {AppName}.”
- “Add to {List} with {AppName}.”

Each phrase includes the app name once. Do not put the app name in app-authored follow-up or result dialogue; system attribution supplies it. Do not imply that item, quantity, and list must all be spoken in the activation phrase.

## Action and entity contract

Expose an Add Item action through App Intents. Assess existing domain schemas during implementation; no matching grocery schema or API availability is established by the supplied files.

The shortcut exposes only one optional parameter: **List**. Options are familiar writable grocery-list entities, shown and spoken by display name, for example “Weekly groceries.” Internal stable IDs resolve identity but are never requested, displayed, or read aloud. If names collide, append a human-readable owner/household qualifier and ask which list is intended. Revalidate identity and write access immediately before committing.

Required **Item** is gathered in a later step: “What would you like to add to Weekly groceries?” Accept “milk” as one item with quantity one. This first version adds a single item per invocation; ask “Which single item would you like to add?” if input is ambiguous or names several items. Do not guess extra items or quantities. Blank/unrecognized input repeats the specific item question without writing.

If List is omitted, propose the user's previously selected default writable list: “Add to Weekly groceries?” Accept yes or a different list name. Do not infer a default merely because a list is shared or named Weekly. With no valid default, ask “Which grocery list?” Name up to three writable options; for more options ask for a list name, then narrow matches. A list supplied explicitly skips this default question when unambiguous. Cancel or no response ends without a write.

## Execution and response states

Resolve list → gather item → revalidate list/access → commit → report outcome. Retain collected item during recoverable list selection. Never silently redirect to another list.

| State | Spoken dialogue and visible result | Transition |
|---|---|---|
| Missing/deleted requested list | “I can’t find Weekly groceries. Which grocery list should I use for milk?” If item is not yet known, omit “for milk.” Offer available names as above. | Select an alternative explicitly or cancel; no write until resolved. |
| Duplicate list names | “Which Weekly groceries list: Alex’s household or Sam’s household?” | Resolve one stable entity before continuing. |
| Access lost | “You no longer have permission to add to Weekly groceries. Which grocery list should I use for milk?” | Select a writable list or cancel. |
| No writable lists | “You don’t have a grocery list you can add to. Open the app to create or join one.” | Offer opening the relevant list-management screen; do not open automatically or claim an add. |
| Commit confirmed | “Added milk to Weekly groceries.” | Finish; show item, list, and added status in the built-in result, with system dismissal. |
| Same unchecked item already present | “Milk is already on Weekly groceries. Nothing was added.” | Finish without increasing quantity or creating a duplicate. A checked-off item is reactivated and reported as “Added milk to Weekly groceries.” |
| Definite save failure | “I couldn’t save milk to Weekly groceries. Try again.” | Finish with failure; retain normal retry path. |
| Save outcome unknown | “I couldn’t confirm whether milk was added to Weekly groceries. Check the list before trying again.” | Offer opening that list. Reconcile the operation before retrying; do not blindly duplicate the write. |
| Cancel at any input step | “Canceled. Nothing was added.” | End with no mutation. |

Routine adds need no additional confirmation after required inputs are resolved. Report “Added” only after the app's authoritative shared-list store confirms the write. A local pending/offline write is not confirmed shared success. Use a stable operation token for safe retries of the same execution; a deliberate later invocation is a new operation, subject to the duplicate rule.

Prefer built-in audible and visual responses; no custom snippet layout or Live Activity is required for this brief task. Speech must include the item, destination, and actual outcome wherever known. Visual output must convey the same essential result even if speech is unavailable. Do not require a visual card to complete the hands-free flow. On supported result surfaces provide “Open List” linking to the resolved list; opening it is optional after success. If it has since disappeared, show the list-management recovery destination rather than another list.

The normal valid-list add completes without opening the app. Creating/joining a list or resolving account requirements opens the relevant app content only after an explicit user choice. If authorization is required, explain “Open the app to sign in before adding groceries”; no write or success claim occurs.

## Acceptance contract

- Installed shortcut is discoverable through the supported iOS system surfaces without manual shortcut creation; verify actual behavior on a supported client.
- Each activation phrase has one app-name reference and at most the optional List parameter. No database ID appears in choices, prompts, or results.
- Omitted default, absent default, duplicate names, removed list, and revoked access follow the states above without a wrong-list write.
- “Milk” reaches the chosen shared list once; success is spoken only after commit. Duplicate, failure, unknown-outcome, and cancellation paths report their true outcomes.
- Complete the normal flow with the screen unseen; every essential prompt and result remains understandable through audio alone. Verify visual outcomes independently with speech off.
- The contextual tip appears at its specified trigger once, dismisses, and links correctly. System ranking is observed rather than asserted.
- Verify SDK availability, phrase registration, entity resolution, deep links, actual Siri recognition, and supported-client rendering during implementation. None is established by this specification.

## Design sources

Local installed HIG snapshot dated 2026-10-25, consulted without web access:

- [App Shortcuts — Best practices and Editorial guidelines](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts): important complete tasks, one optional parameter, natural app-named phrases, contextual teaching, iOS discovery and symbols.
- [Siri — Customizing your app’s experience](https://developer.apple.com/design/human-interface-guidelines/siri): specific follow-ups, complete brief speech, no repeated app attribution, precise failures; prefer built-in responses.
- [Snippets — Anatomy and Best practices](https://developer.apple.com/design/human-interface-guidelines/snippets): distinguish confirmation from completed result. This specification uses built-in responses rather than a custom view.
