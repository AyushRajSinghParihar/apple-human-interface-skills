# Revised name and avatar setup

## Scope and evidence

Design contract for the iOS/macOS family-history app in `interface.md`, independent of framework or Apple SDK. The supplied brief states that First and Last name are required in Latin letters, one-character names are rejected, two opposite-sex parents are assumed, and only light-skinned human avatars are offered. No screens, code, data schema, visibility policy, or executable app were supplied. The changes below are proposed product decisions, not claims about an existing implementation.

## Decisions and source basis

| Supplied barrier | Revised decision | Guidance and qualification |
| --- | --- | --- |
| Required Latin First/Last fields | One required **Display name** field; accept a chosen name in any script without splitting it. Historical names belong to person records, separately. | [Inclusion — Languages and Avoiding stereotypes](https://developer.apple.com/design/human-interface-guidelines/inclusion#Languages) supports internationalization and removing assumptions. The precise name model is our product decision. |
| Single-character rejection | Accept a single visible grapheme, including `李` or `Q`. No alphabet, word-count, surname, or legal-identity requirement. | Applying Inclusion to participation; Apple does not prescribe this validation algorithm. |
| Two opposite-sex parents | Remove parent entry from identity setup. In family editing, allow zero, one, two, or more parent relationships without inferring gender. | [Inclusion — Avoiding stereotypes](https://developer.apple.com/design/human-interface-guidelines/inclusion#Avoiding-stereotypes) says not to restrict family structure to one arrangement. |
| Light-skinned human avatars only | Replace the initial catalog with optional abstract and nature symbols available equally to everyone. Default to no avatar. Do not use a light-skinned or gendered person as the fallback. | [Inclusion — Gender identity and People and settings](https://developer.apple.com/design/human-interface-guidelines/inclusion#Gender-identity) supports avatar customization and varied representation. A nonhuman catalog is our bounded release choice, not an Apple mandate or a substitute for research. |

No gender, pronouns, legal name, birth date, ancestry, photograph, or parent details are needed to set up a display identity. Do not infer these from name, avatar, or language. Names need not be unique; stable internal IDs distinguish people. These decisions follow [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).

## Screen and input contract

Title: **Set up your profile**.

Persistent label: **Display name**. Helper: “Use the name you want people to see. You can use any language or a single name.” Do not put required instructions only in a placeholder. Use a general text input with international input methods, paste, selection, and undo; no forced Latin keyboard, capitalization, transliteration, or autocorrection. Offer a labeled Clear action on iOS. This follows [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices), including its iOS qualification.

Below the field: **Avatar (optional)**, preview, and **Choose Avatar** (macOS: **Choose Avatar…**, because it opens a further editing view). Helper: “Choose a symbol, or continue without one.” Primary action: **Save Profile**. Persistent scope copy: “This changes your profile, not names in your family tree.”

Proposed visibility contract: before saving, show “Your display name and avatar will be visible to members of family spaces you join. This setup does not publish them publicly.” The implementation must enforce that scope. Existing broader sharing must be reconciled before shipping this copy; do not merely assert it in the UI. No joining or publishing occurs as a side effect of Save Profile.

### Name representation and validation

- Store the entered Unicode string intact; preserve spelling, capitalization, diacritics, internal spaces, punctuation, joining characters, and order. No automatic first/last-name parsing or silent trimming.
- Product limit: 200 extended grapheme clusters, using a Unicode-aware segmentation implementation with the same version on client and server. Show the count near the limit; accept pasted text into the draft rather than silently truncating it.
- A valid committed name contains at least one visible grapheme and is within the limit. Reject line breaks, non-rendering control characters, and explicit bidi embedding/override controls. Preserve ordinary RTL text, script joiners, and combining sequences. Render names as isolated text rather than markup. Exact Unicode handling requires implementation review; “visible” must not mean ASCII or letters only.
- Allow incomplete input and IME composition. Validate on Save, never interrupt composition. If composition is active, finish composition before processing Save; Return used to choose an IME candidate must not submit.
- Empty/whitespace-only error: “Enter a display name.” Over-limit error: “Use 200 characters or fewer.” Explain that the counter treats a combined character as one. Unsupported-control error: “Remove line breaks or invisible formatting controls.” Retain the draft and offer editing; never claim the name itself is invalid.
- Errors appear next to the field, are programmatically associated with it, and persist until corrected or dismissed by a successful save. Save remains available to expose the reason for failure. Never reject duplicate display names.

### Avatar selection

Choose Avatar opens a dedicated editing view with a draft selection. Start with **No Avatar**, then named choices **Leaf**, **Flower**, **Mountain**, **Star**, **Circle**, and **Wave**. They are decorative symbols, with no gender, ancestry, religion, or personality classification. Provide four independently selectable palettes, identified by visible names and swatches; color never determines meaning. Each choice has a text label and a selected marker, not color alone.

Use one single-selection group for symbol and one for palette. Palette controls are unavailable with No Avatar, with the explanation “Choose a symbol to change its colors.” Preview changes locally. **Use Avatar** returns the staged choice to the profile draft; **Cancel** returns without changing that draft. **No Avatar** is always reversible. Neither action saves the profile. Avatar selection never changes the name. Do not require a photo, media permission, camera access, or image upload; these are outside this release. Human figures may return only after a separately reviewed, broadly representative and independently customizable catalog is specified.

## State and action model

```text
savedProfile = { id, revision, displayName, avatar: null | {symbolId, paletteId} }
profileDraft = copy(savedProfile or {displayName: "", avatar: null})

edit -> update draft only; retain it through app switching and view resizing
chooseAvatar -> avatarDraft = copy(profileDraft.avatar)
useAvatar -> profileDraft.avatar = avatarDraft; return to profile
cancelAvatar -> discard avatarDraft; return to profile
save -> validate after composition completes
  invalid -> retain draft; reveal error; focus first invalid field
  valid -> pending; submit one atomic profile update with revision + request ID
  success -> replace savedProfile; clear draft; show persistent "Profile saved"
  failure -> retain draft; show "Couldn’t save your profile. Try again."
  conflict -> retain draft; offer review of saved version; do not overwrite silently
```

Disable duplicate Save activation while pending, expose “Saving…” and a busy state, and preserve the screen context. On iOS show the activity indication inside the initiating button. On failure re-enable Save; a retry uses the same request ID until the outcome is resolved. Server validation follows the same rules. No partial name-only or avatar-only commits. [Buttons — Role and Platform considerations](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) supports clear outcomes and waiting feedback; transaction and retry semantics are product requirements.

Back exits to the previous route with a private local draft retained; reentry offers **Resume Draft** and **Discard Draft**. Discard affects only unsaved edits. Keep drafts isolated by signed-in account and clear them on sign-out. A first-time profile cannot join a family space until it has a valid saved display name; avatar and family relationships remain optional. Setup has no deadline. Reopening an existing profile begins from saved values unless a retained draft is explicitly resumed.

## Family relationships after setup

The family editor starts with an empty relationship list and **Add Parent**; no Mother/Father slots. Each relationship stores independent `childPersonId`, `parentPersonId`, optional relationship kind, and optional preferred label. Kind may be unspecified, biological, adoptive, foster, guardian, or self-described; these are application options requiring genealogy research, not universal categories. Gender is never a prerequisite. A label such as “Mother” or “Dad” is chosen explicitly and is not inferred from an avatar or name.

Allow adding an existing person or creating a person with a single name, using the same script and length rules. Do not require a parent’s parents. Distinguish people by record context and IDs, never by unique names. Unknown parents can remain absent without inventing a person. Reject self-links and cycles with a specific relationship error while preserving the entered data. An existing two-parent schema must change before this contract can ship. Editing display identity must not rewrite historical source transcriptions or relationships.

## Platform and access behavior

| Context | Required behavior |
| --- | --- |
| iOS | Scrollable single-column form; frequent actions within reach; onscreen keyboard must not obscure the only completion action. Preserve navigation Back and draft through interruption, rotation, and text enlargement. |
| macOS | Resizable profile workspace; keyboard completion and logical Tab order. Expose Save Profile in the app’s File menu and its equivalent onscreen action, with identical state. Use standard editing commands. Command-S saves when valid; candidate composition takes precedence. Switching apps preserves draft and focus context. |
| Both | Focus order follows heading, name and helper/error, avatar preview and action, visibility copy, Save. Expose labels, roles, busy/selected states, and errors to assistive technology. Avatar preview has the description “No avatar” or e.g. “Leaf avatar, Ocean palette”; omit redundant decorative images from traversal. |

These platform choices apply [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) and [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices). They require no particular SDK.

Support at least 200% text enlargement with reflow, wrapping labels and visible actions. Start with 17 pt text on iOS and 13 pt on macOS. Use 44 × 44 pt selectable regions for this form’s buttons on both platforms, with nonoverlapping separation. The local Buttons guide gives a general 44 × 44 pt rule while Accessibility gives macOS a 28 × 28 pt default and 20 × 20 pt minimum; the larger product target conservatively satisfies both, without claiming 44 pt is a universal Mac minimum. Measure actual colors in light/dark and Increase Contrast; do not claim contrast compliance without measurements. These are drawn from [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Respect language and region independently. Use leading/trailing layout, mirror reading-order navigation, preserve the natural direction of entered names, isolate mixed-direction names in surrounding sentences, and do not flip avatar art. Full saved names remain available in an expanding/wrapping profile view; the editor scrolls horizontally rather than changing stored text. Locale changes preserve the draft. Follow [Right to left — Text alignment, Controls and Images](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Text-alignment).

## Worked before/after

A person chooses the display name `李` and has two mothers, with a third guardian they may add later.

**Before, as described in the brief:** `李` fails both Latin-only and one-character rules; First/Last requires inventing another component. The two opposite-sex parent assumption cannot represent two mothers. The only avatar choices depict light-skinned humans.

**After, proposed:** Enter `李` in Display name. Leave No Avatar or choose Leaf with Ocean palette. Save Profile commits `{displayName: "李", avatar: {symbolId: "leaf", paletteId: "ocean"}}` without surname, gender, or parent data. Later, add two independent parent relationships, each optionally labeled “Mother,” and a guardian relationship if desired. The chosen profile name does not alter anyone’s historical name. If Save fails, `李` and the chosen avatar remain in the draft for retry.

## Acceptance checks and status

**Passed — specification inspection only:** This artifact explicitly removes all four supplied barriers; defines name representation, commit/cancel/error behavior and optional avatar state; separates chosen identity from genealogy; includes platform differences and source links. The installed root, selected families, topic procedures, and local source guides were read in that order. No web sources were fetched.

**Failed — supplied baseline against the revised contract:** Latin-only validation, rejection of a one-character name, fixed opposite-sex parents, and the light-skinned-only catalog each fail by the brief’s description. These are textual findings, not reproduced runtime failures.

**Not executed — implementation acceptance:**

| Scenario | Pass condition |
| --- | --- |
| Global names | `李`, `Q`, `أمل`, `山田 太郎`, `María-José`, `O’Neill`, a decomposed accented name, and mixed-direction `نور Lee` round-trip unchanged; no first/last split or forced Latin keyboard. |
| Boundaries | Empty and whitespace-only values receive actionable errors; 1 and 200 graphemes save; 201 stays editable with an error. Composition is uninterrupted; joining sequences survive. Control-character rejection does not reject ordinary RTL or combining text. |
| Avatar | No Avatar completes setup. Every symbol/palette is labeled; selection is perceivable without color. Cancel restores the prior draft, Use Avatar stages only, Save commits both fields. |
| Family diversity | Zero, one, two same-gender parents, and three parent/guardian relationships can be represented; unspecified kinds remain valid. Cycles/self-links fail without losing edits. |
| Persistence | Rotation, resize and app switching retain draft. Reentry offers resume/discard. Failed/repeated saves do not duplicate or partially update data; a revision conflict preserves edits. |
| Access | Complete by keyboard, VoiceOver and Switch Control on supported Apple systems. Focus reaches all actions; errors and pending/result states are perceivable. At 200% text, no required action or essential label clips; keyboard does not hide Save. |
| Geometry and appearance | Measure hit regions and separation, contrast in light/dark and Increase Contrast. Verify localized labels wrap. No essential information depends on sound or color. |
| Direction and localization | Arabic/Hebrew UI navigation mirrors; avatar artwork stays unchanged; mixed-script cursor, selection, paste, digits and saved rendering preserve meaning. Native-language reviewers evaluate copy and labels. |
| Privacy | Only display name and optional symbol IDs are saved; no media permissions occur; family-space visibility matches the displayed promise; draft data cannot leak across accounts. |

## Evidence limits

Only `interface.md` and installed skill guidance informed this design. Local articles are dated English summaries of HIG, not SDK documentation or independently verified current Apple pages. Official links above provide attribution and were not opened. No runtime, device, SDK, GUI, screen-reader, keyboard, accessibility-inspector, security, contrast, or geometry execution occurred. No cultural or genealogical user research occurred. Universal cultural acceptance, accurate translations, backend migration feasibility, and actual accessibility remain unproven; resolve these through implementation validation and research with people using varied scripts, chosen identities, family structures, and assistive technologies.
