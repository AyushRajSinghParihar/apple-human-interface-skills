# Decisions and specification changes

Edited `interface.md` in place, replacing its one-paragraph problem statement with an iOS App Shortcut contract. Add Item now has two short app-named phrases, a named List entity instead of a public row ID, one optional phrase parameter, subsequent item collection, recent-list clarification, contextual discovery, and explicit success, cancellation, ambiguity, missing-list, authentication, save, and sync responses.

The repeated task stays in context. Spoken results name the item and destination without repeating system app attribution. Complex recovery offers the relevant app destination. Retry identity and access revalidation prevent accidental duplicate or wrong-list writes. The real app name, SDK availability, and deployed implementation remain unspecified.

The installed root skill was explicitly read, followed by the topic-index search, System experiences → App Shortcuts procedure → App Shortcuts source guide, Technologies → Siri procedure → Siri source guide, and Foundations → Writing procedure → Writing source guide. Each file was consumed using a separate single-file command. No web browsing was used; official links below identify the sources represented by the local snapshot.

Source-backed decisions: prioritize a common task, expose one optional predictable parameter, ask follow-ups, teach contextually, and use natural app-named phrases ([App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts#Best-practices)); make speech sufficient by itself and explain the current failure precisely ([Siri](https://developer.apple.com/design/human-interface-guidelines/siri#Customizing-your-apps-experience-with-Siri)); provide clear remedies ([Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices)). The three-add tip threshold, last-used default, exact copy, sync semantics, and retry policy are proposed product choices, not quoted Apple requirements. No schema fit is established by the supplied files; implementation must evaluate available schemas rather than assume a grocery schema exists.

## Worked before/after

Before, as supplied: the shortcut demands a database row ID, repeats the app name three times, and silently fails if the requested list is missing. No exact original dialogue or code was supplied.

After, proposed example using “Pantry” as an illustrative app name: the person says “Add an item with Pantry.” Siri asks “Add to Weekly?” They say “Yes.” Siri asks “What item would you like to add to Weekly?” They say “Milk.” After durable shared completion, Siri says and displays “Added milk to Weekly.” No app opening is needed.

If Weekly disappears before saving, the response is “Weekly is unavailable. Nothing was added. Which grocery list should I use?” The person chooses Home; the pending milk item is saved there only after access is validated. The response becomes “Added milk to Home.” If no writable list exists, the flow offers list management and reports no add.

## Acceptance checks and evidence limits

Passed — static specification review: the revised file explicitly contains discovery surfaces, phrase variants, one optional phrase parameter, internal-only IDs, default and ambiguity rules, cancellation and removal recovery, app-opening boundaries, and audible/visual outcome copy. The worked trace is consistent with those requirements. The interface patch and this report exist as local artifacts.

Failed — no static specification check identified as failed. This does not mean a runtime release passed.

Not executed — actual installation and discovery in Siri/Shortcuts/Spotlight; phrase recognition and localized pronunciation; entity resolution; persistence, retry, cancellation races and shared sync; authentication continuation; tip rendering; SDK compilation or API availability; device, GUI, VoiceOver or other accessibility execution. Run the release acceptance matrix in `interface.md` against the implementation on supported iOS devices before release, including an eyes-away audio run and stale-list/access-loss cases.

Evidence is limited to the supplied one-paragraph specification and the installed local HIG guidance, whose source snapshots are dated 2026-10-25. No app code, device captures, SDK documentation, or runtime results were supplied or produced. HIG guidance establishes design rationale, not successful system discovery, exact system dialogue presentation, cross-device support, or accessibility behavior.
