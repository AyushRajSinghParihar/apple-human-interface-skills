# Result

Patched interface.md in place with an implementable macOS specification. The original brief described logo glyphs on every editing command, neon selection/alert backgrounds, and a 150-pixel wordmark displacing invoices. The revised specification removes that banner and its spacer, replaces command logos with familiar symbols or labels, restores semantic selection and alert rendering, and retains one compact identity lockup plus established app identity surfaces.

## Decisions and rationale

- Content leads: the invoice starts the document area. A maximum 20 × 20 pt logo shares an existing header row with a standard-size product name and yields before task content. This size and collapse order are design choices, not HIG requirements. [Branding, Best practices](https://developer.apple.com/design/human-interface-guidelines/branding#Best-practices) supports avoiding brand-only elements that displace useful content.
- Commands communicate outcomes: a conditional inventory maps Cut, Copy, Paste, Undo, Redo, Add Line Item and Delete Line Item to familiar glyphs and names. Existing behavior, shortcuts and recovery must be recorded and preserved. [Icons, Editing](https://developer.apple.com/design/human-interface-guidelines/icons#Editing) and [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) support familiar symbols and system controls.
- Color communicates state: semantic colors replace neon fills. The app accent can retain brand identity under Multicolor while respecting a chosen user accent. Selection, inactive selection and focus retain platform meaning. [Color, macOS](https://developer.apple.com/design/human-interface-guidelines/color#macOS) supports these choices.
- Alerts retain standard appearance and consequence-based meaning. The existing alert contracts require inspection; the brief supplies no triggers or handlers. Standard app-icon identity may remain without decorative wordmarks. [Alerts, macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS) supports app identity and restrained caution imagery.

## Worked before/after

Illustrative fixture: invoice INV-1042 for Cedar Studio, with an editable first line item. These names and command examples are proposed test data, not observed UI.

| Element | Before, from supplied brief | After specification |
|---|---|---|
| Editor top | 150-pixel wordmark pushes content below the fold | No brand banner/spacer; invoice begins the document area; compact identity shares an existing row |
| Copy / Undo, if present | Custom logo glyph for each editing command | document.on.document / arrow.uturn.backward, with Copy / Undo names and existing shortcuts |
| Selected line item | Neon brand background replaces selection color | System active/inactive content selection; selection remains apparent beyond hue |
| Alert | Neon brand background replaces alert colors | Standard Mac alert appearance and existing recorded action/default contract |
| Recognition | Oversized wordmark and pervasive command logos | Existing product name/logo, compact lockup and established app identity surfaces |

Selecting the fixture's first item and choosing Copy must copy the same content as before. Undo must reach the same prior state as before. Those are implementation acceptance conditions, not executed outcomes. Removing a banner does not prove a precise reclaimed height: “150-pixel” lacks scale and layout measurements.

## Acceptance status

Passed — static specification inspection:

- interface.md was replaced with the concrete revised specification.
- All three reported brand treatments have explicit replacements, with recognition cues retained.
- The specification provides command mappings, color/state roles, constrained-width behavior, and a 1024 × 768 pt proposed content-visibility fixture.
- It requires preserving command and alert consequences and explicitly identifies unknown inventories and behaviors.

Failed: no checks executed in this task failed. This does not imply the proposed interface passes runtime checks.

Not executed — required before shipping:

- Render the fixture and verify invoice/customer/first-item visibility, identity collapse, label expansion and glyph legibility.
- Test light/dark, Increase Contrast, user accents, active/inactive selection and non-color state cues; measure actual foreground/background contrast.
- Exercise keyboard/pointer commands, enabled/pressed states, focus, clipboard and undo equivalence; verify accessible names with VoiceOver.
- Exercise each recorded alert trigger, action, Return/Escape exit and data consequence.
- Test product recognition with representative users.

## Evidence and limits

Read the installed apple-hig root SKILL.md explicitly. Followed its installed routes in this order: Foundations family → Branding, Color and Icons topic procedures → their respective source guides; Menus and actions family → Buttons procedure → Buttons guide; Presentation family → Alerts procedure → Alerts guide. Each file was read with its own cat command. All paths resolve under .agents/skills/apple-hig/. The interface brief was read before design decisions. Official links above are attribution from the local guides; no browsing occurred.

Only a prose brief and installed instruction/reference files were available. No code, screenshots, brand assets, command inventory, alert contracts, OS support range or rendered color pairs were supplied. The local guides describe themselves as original application guidance based on a dated HIG snapshot, not SDK references or independently verified source text. No Mac/device, SDK build, GUI, accessibility, contrast measurement or user study was executed. Recognition and improved content visibility remain hypotheses with concrete acceptance checks; Linux file editing establishes only the revised documents.
