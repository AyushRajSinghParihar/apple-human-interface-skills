# Result

Revised `interface.md` in place from a brief problem statement into an iOS Add Item App Shortcut specification. It now defines discovery, activation phrases, named entities, input collection, commit boundaries, spoken/visual outcomes, recovery, app-opening boundaries, and acceptance checks.

## Decisions

- Prioritize the repeated grocery add as one complete shortcut. Make it available on installation and teach it once in context; system placement remains system-controlled.
- Expose one optional List parameter, using familiar names instead of database row IDs. Collect the item afterward. Clarify the default instead of silently choosing a shared list.
- Include the actual app name once per activation phrase and omit it from app-authored dialogue. The app name is absent from the brief, so the specification explicitly defines a replacement token.
- Require explicit alternative-list selection when a list disappears. Report actual save status, including unknown outcomes, rather than failing silently or reporting premature success.
- Use built-in responses with complete speech for occupied-hands use. No custom snippet or ongoing progress surface is needed.

The contextual-tip threshold, single-item scope, duplicate policy, default selection, and retry rules are concrete product decisions. They operationalize the brief; they are not presented as universal HIG requirements.

## Worked before/after

**Before, observed in the supplied brief:** the shortcut asks for a database row ID, repeats the app name three times, and fails silently when the requested list is missing. No exact original phrase or execution transcript was supplied.

**After, specified example** (illustrative app name “Grocer,” user-selected default “Weekly groceries”):

1. User: “Add an item with Grocer.”
2. Shortcut: “Add to Weekly groceries?” User: “Yes.”
3. Shortcut: “What would you like to add to Weekly groceries?” User: “Milk.”
4. After confirmed commit: “Added milk to Weekly groceries.” The visual result identifies milk, Weekly groceries, and added status.

If the list is removed before commit: “I can’t find Weekly groceries. Which grocery list should I use for milk?” User chooses “Household.” Only after resolving and committing there: “Added milk to Household.” Canceling instead produces “Canceled. Nothing was added.” No row ID or unseen visual choice is needed.

## Acceptance audit

**Passed — static specification checks:** the revised document includes natural app-named phrase variants; one optional exposed parameter; human-readable entity resolution; omitted/ambiguous-input handling; removed-list and permission recovery; cancellation; commit-gated success; complete audio and visual outcomes; explicit opening boundaries; and contextual discovery. The before/after above traces the normal and missing-list contracts. These are checks of document coverage, not runtime passes.

**Failed:** no remaining static contract failure identified. Runtime pass/fail is undetermined.

**Not executed — required implementation checks:** installation and actual Siri/Spotlight/Shortcuts discovery; phrase recognition; default/entity disambiguation; live list deletion and revoked permissions; confirmed/failed/unknown writes and retry deduplication; cancellation; contextual-tip persistence and deep links; eyes-away comprehension on a supported client; speech-off visual results; native rendering and accessibility behavior; SDK compilation and API availability. Execute these against the acceptance contract in `interface.md` when an implementation exists.

## Evidence and limits

Read the installed root `apple-hig/SKILL.md` explicitly, then the System experiences family, its App Shortcuts procedure, and its App Shortcuts reference. Also read the Snippets procedure before its reference, and the Technologies family and Siri procedure before its Siri reference. All paths were resolved under `.agents/skills/apple-hig/`; each file was consumed with a separate `cat` command.

Material guidance comes from the installed local snapshot: [App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts), [Siri](https://developer.apple.com/design/human-interface-guidelines/siri), and [Snippets](https://developer.apple.com/design/human-interface-guidelines/snippets). These are attribution links, not claims of online verification. No web browsing occurred.

Only the short original specification and installed instructions were evidence for the design. There is no supplied implementation, app identity, deployment target, SDK, account model, or device execution evidence. The revision is a concrete design contract, not a claim of functioning App Intents integration, system suggestions, GUI rendering, accessibility execution, or device testing. Current SDK details and domain-schema fit remain implementation verification work.
