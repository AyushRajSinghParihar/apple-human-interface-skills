# Name and avatar setup: revised interaction specification

## Scope and evidence

Target: iOS and macOS, with a framework-agnostic interaction contract. The supplied `interface.md` states that First and Last name require Latin letters, one-character names are rejected, two opposite-sex parents are assumed, and avatars show only light-skinned humans. These are confirmed brief-level problems; no running interface, assets, backend, or screenshots were supplied.

The product supports chosen display identities. This specification treats the account identity separately from historical people and evidence in a family tree. The exact copy, schema, limits, catalog, and save behavior below are product decisions informed by HIG, rather than requirements quoted from Apple.

## Decisions and source basis

| Observed constraint | Revised decision | Local guidance basis and official article |
| --- | --- | --- |
| Required First/Last, Latin-only, minimum two characters | One required **Display name**; accept a single character, mononyms, all scripts, mixed scripts, punctuation, spaces, and chosen names. No legal-name verification or automatic splitting/transliteration. | Inclusion: welcoming language, languages, avoiding stereotypes; [Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion). Exact validation is a product choice. |
| Two opposite-sex parents | Remove parent questions from identity setup. Later, allow zero or multiple parent connections with no gender pairing rule. | Inclusion: avoiding stereotypes; [Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion). |
| Only light-skinned human avatars | Default to an abstract symbol. Offer nonhuman symbols and customizable human figures; no gender inference from name or appearance. | Inclusion: gender identity, people and settings; [Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion). |
| Entry and validation behavior unspecified | Persistent labels, permissive editing, actionable inline errors, predictable focus. | [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields), [Writing](https://developer.apple.com/design/human-interface-guidelines/writing). |
| Global display identities | Localize interface separately from entered content; preserve bidirectional names and artwork. | [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left), Inclusion: languages. |
| Access and privacy unspecified | Define keyboard/assistive semantics and minimize collection. Do not require photos, gender, or parent data to continue. | [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy). |

## Screen and transitions

Entry heading: **Choose how you appear**. Supporting text: **Use the name you want others to see. You can change your name and avatar later.**

Order:

1. Persistent **Display name** label, short text field, and help: **One name is enough. Use any language.** No placeholder is needed. Disable spelling correction and automatic capitalization for this field where the host supports those behaviors; allow paste, composition, and ordinary editing.
2. **Avatar (optional)** preview and **Change avatar** action. Initial preview is the abstract “Circle pattern”; it does not derive initials, gender, or ethnicity from the name.
3. Audience text: **Your name and avatar will appear to people with access to your family tree.** This specification chooses tree-scoped visibility, with no public profile or search indexing. Backend behavior must implement that scope before this copy ships.
4. **Save and continue** and **Cancel**. Cancel exits without changing the saved identity. No parent questions or permission prompts appear here.

Save remains available so an empty submission can explain what is needed. Enter from the completed name field invokes Save when no input-method composition is active; Enter during composition commits text only. iOS offers an accessible trailing **Clear display name** action; macOS supports ordinary keyboard editing and logical Tab traversal. Returning to setup loads saved values. The same fields are editable later through **Edit profile**.

States: `editing → validating → saving → saved`; validation failure returns to `editing` with the draft retained. While saving, expose persistent **Saving…**, prevent duplicate submissions, and retain the draft. On success, continue to the family tree and expose **Profile saved**. On failure, remain in setup with **Couldn’t save your profile. Try again.**, **Try again**, and **Cancel**. Retry uses an idempotent request identifier; a failed save must not leave a half-updated name/avatar pair. Exiting discards only the unsaved draft. A successful save updates display identity references, never historical names or parent records.

### Name value contract

```text
Identity = { stableId, displayName, avatarChoice }
avatarChoice = { kind: "symbol", assetId }
            or { kind: "human", styleId, skinToneId, hairId, accessoryIds }

onEdit(text):
    draft.displayName = text       // preserve partial input and IME composition
    clear stale field error       // never rewrite input as the person types

onSave():
    finish composition before attempting validation
    candidate = trimOuterUnicodeWhitespace(draft.displayName)
    if candidate has no visible grapheme:
        showNameError("Enter a display name.")
    else if candidate contains line breaks or nontext control characters:
        showNameError("Use a single line without control characters.")
    else if graphemeCount(candidate) > 200:
        showNameError("Use 200 characters or fewer.")
    else:
        atomically save(candidate, draft.avatarChoice)
```

The 200 extended-grapheme limit is a proposed operational limit, not HIG advice. Explain it when exceeded; never silently truncate. Permit combining marks and script joining characters; do not strip them using a broad “non-ASCII/control” regex. Reject explicit bidirectional override/embedding/isolate controls as nontext controls, but preserve natural Arabic/Hebrew text and joining marks. Render names as isolated text runs, never executable markup. Apply identical validation at the persistence boundary. Preserve case, internal spaces, accents, and spelling. Any normalized search key is separate from the stored display value. Duplicate display names are permitted; stable IDs identify records.

### Avatar selection

**Change avatar** expands an editor adjacent to the preview. It has labeled groups **Symbols** and **People**, plus **Use avatar** and **Cancel avatar changes**. Selection is a draft until Use avatar; the profile itself commits only on Save and continue. Cancel restores the previous preview and returns focus to Change avatar.

Initial symbol catalog: Circle pattern, Leaf, Mountain, Star, and Bird, each with a localized name. Avoid flags, religious symbols, or culturally universal claims. These choices are product proposals requiring cultural review. No photo upload or camera feature is included in this revision, so no media permissions are needed.

Human figures offer independently selectable skin tone, hair, and accessories; no male/female gate. Provide at least six labeled skin tones spanning light to dark, multiple hair textures, ages and body representations, and optional glasses, head coverings, and mobility aids. These are asset delivery requirements, not claims about existing assets. Do not lock combinations by gender or ethnicity. A person may always return to a symbol. Catalog review must include varied cultures and disabled participants; a fixed catalog cannot represent everyone.

Each option exposes its localized name and selected state, with a checkmark and outline in addition to color. Use visible labeled choices rather than a date-style wheel: this is visual identity selection, not ordered date entry. The [Pickers guidance](https://developer.apple.com/design/human-interface-guidelines/pickers) informs matching the control to the choice structure; it does not mandate a particular SDK widget. Persist stable option IDs separately from translated labels. An unavailable saved asset uses Circle pattern temporarily with **Avatar unavailable. Choose another avatar.**; do not silently overwrite the saved choice.

### Family-history continuation

Tree empty state: **Start your family tree**, with **Add a person** and **Do this later**. Adding a person does not require adding parents. Later, **Add parent connection** selects an existing person or creates one, then offers an optional **Relationship description** free-text field and **Save connection** / **Cancel**. Repeat to add more connections; no maximum of two and no required gender fields. Unknown parents may remain absent; never fabricate named people to fill slots. Historical names and source evidence belong to separate person records. A profile edit must not rewrite them. Genealogical relationship taxonomies, evidence conflicts, and authorization for editing other people's records require separate design.

## Internationalization and access contract

Localize all interface strings; never translate a person's entered name. Use leading/trailing layout. Mirror reading-order navigation for RTL interfaces, but preserve avatar artwork and the internal order of numbers. Isolate each name from adjacent UI text and use script-appropriate font fallback. Long names remain fully editable through field scrolling and readable through a wrapping profile preview, without a tooltip-only dependency.

Use semantic heading, field, action, option-group, selected-option, error, and status roles. Associate help and errors with the name field. On invalid submission, focus the field and expose its error; announce save failure without clearing the draft. Focus order follows screen order; avatar choices are keyboard reachable and activatable without dragging. Closing the editor restores its opener's focus. The adjacent named preview is decorative when its information is already supplied by the avatar control.

Design for at least 200% text enlargement without losing controls or help; allow vertical scrolling and wrapping. Use the local guide's default activation sizes as design targets: iOS 44 × 44 pt, macOS 28 × 28 pt, with adequate separation. These are platform units, not a universal CSS pixel conversion. Selected/error states include text or symbols as well as color. Contrast must be measured for final colors in light/dark appearances and Increase Contrast; no palette or measured ratio is supplied here. No motion or audio is required to complete setup.

Data-purpose contract: collect display name for recognition and avatar IDs for representation only on Save; parent connections are collected later only when requested. Collect no legal name, gender, contacts, camera, or photo-library access in this flow. Do not log draft names in analytics. Local drafts are discarded on cancel; persisted changes follow the application's deletion/retention policy, which was not supplied. These are proposed product constraints, not a privacy or security certification.

## Worked before/after

Illustrative scenario, not an executed test: a person chooses **李**, wants a Mountain avatar, and records three parent connections without supplying gender.

**Before:** First/Last fields cannot represent the chosen mononym; Latin-only and length restrictions reject 李. Available avatars cannot express the requested nonhuman identity. The two opposite-sex-parent model cannot represent the three connections.

**After:** Enter 李 in Display name, choose Symbols → Mountain → Use avatar, and Save and continue. Stored result is `{stableId: existingId, displayName: "李", avatarChoice: {kind: "symbol", assetId: "mountain"}}`. The profile preview shows 李 and Mountain. Skip tree entry now or add a person and then three independent parent connections. No surname, transliteration, gender, photo access, or parental details are required for profile completion. Editing the display name later leaves historical records unchanged.

## Acceptance checks and evidence limits

**Passed — static specification inspection:** the revised contract removes all four supplied restrictions; specifies name validation, avatar commit/cancel, failure/retry, family continuation, visibility, and independent historical records. Installed root, owning families, selected topic procedures, then their source guides were read locally. The topic index was searched for the task concepts. No web browsing was used; official links identify sources from the installed snapshot.

**Failed — supplied design against revised acceptance criteria:** its stated Latin-only/two-character rules exclude 李; mandatory First/Last excludes mononyms; its family model excludes other parent arrangements; its avatar offering lacks the specified representation choices. These findings derive from `interface.md`, not execution.

**Not executed — implementation acceptance checks:**

| Check | Required outcome |
| --- | --- |
| Name corpus: 李, Ó, أحمد, Ngũgĩ wa Thiong’o, Jean-Luc, A B, e + combining accent | Accepted, stored and displayed without script restriction, spelling changes or name splitting. |
| Empty, whitespace-only, invisible-only, newline, bidi override, 201 graphemes | Specific inline correction; draft remains; no save. Exactly 200 graphemes accepted, including composed emoji. |
| IME composition, paste, duplicates, script joiners, locale switch | No premature submit or destructive rewriting; stable identity and input survive. |
| Arabic UI with أحمد / Latin mixed name and digits | Correct navigation direction, unchanged artwork, correct digit order, usable cursor editing; native-language review required. |
| Avatar use/cancel, missing asset, profile save failure and retry | Draft/committed values follow transitions; errors actionable; atomic save; no duplicate update. |
| Zero, one, two same-gender, three, or unknown parent connections | Profile setup completes; optional later connections persist without gender pairing or two-parent cap. |
| Edit profile after tree entries exist | Only display identity changes; historical names and relationship evidence remain intact. |
| Keyboard, VoiceOver, Switch Control, Full Keyboard Access | Complete setup, selection, error recovery and cancellation; correct labels, focus return and selected states. |
| 200% text, long translations/names, light/dark and Increase Contrast | All actions and content reachable; activation geometry and actual contrast measured. |
| Fresh setup, cancel, failed save, visibility tests | No unrelated permission request; no draft analytics; tree-scoped access and atomic persistence enforced. |

No device, SDK, GUI, accessibility, rendering, contrast, backend, or runtime validation occurred. The installed guides are derived HIG snapshots dated 2026-10-25, not SDK references or proof of independent source review. Localized copy, Unicode validation details, catalog representation, cultural preferences, retention policy, and user research remain to be validated. This document specifies an implementable interaction; it does not establish universal cultural acceptance or platform compliance.
