# Decisions and patch summary

Patched interface.md in place with an implementable macOS presentation contract. It removes the 150-pixel wordmark banner, puts a single secondary product name beside the invoice title, replaces logo command glyphs with conventional symbols or clear labels, restores semantic selection/focus/alert colors, and honors the user's Mac accent. Recognition remains through the existing product name and app identity. Invoice issuer branding remains separate.

The patch adds a command mapping, role-to-color table, appearance/state requirements, a conditional save-failure example, and acceptance criteria. Proposed header spacing and a 1024 × 768 pt content-area fixture make content priority testable; they are project choices. The original does not say whether 150 pixels describes wordmark width or height, so no claim of exactly 150 pixels of vertical space recovered is made.

## Worked before/after

Example fixture: invoice INV-1042 for Northwind Studio, with a customer field, dates and one line item. These are illustrative values, not supplied project data.

| Before, per supplied brief | Revised behavior |
|---|---|
| A 150-pixel wordmark pushes invoice content below the fold. | A compact row shows “INV-1042” prominently and the established product name secondarily; no brand-only banner precedes customer, dates and line items. The proposed fixture requires the first item visible without scrolling. |
| Every editing command shows a custom logo. | Copy uses a conventional copy symbol or “Copy”; Add Line Item uses plus; Delete Line Item uses trash. Each keeps its existing outcome and gains an explicit name if icon-only. |
| Neon brand fills replace selections and alerts. | Selecting text uses system selected-text colors. A different user accent is honored. A save-failure alert uses the system surface and “Done”, preserving the open edits when that is the actual failure contract. |

## Acceptance checks and status

**Passed — static specification review:** interface.md was replaced with the concrete specification. All three supplied brand problems have explicit corrections; recognition has a defined location; conventional command mappings, semantic colors, user-accent precedence and alert behavior are specified. HIG guidance and project-specific choices are distinguished.

**Failed:** no revised implementation failure established. The supplied original specification does fail the revised criteria for logo command symbols, banner displacement and neon state/alert fills; that is textual evidence, not an observed app run.

**Not executed — implementation acceptance:** verify content visibility at the stated fixture; symbol legibility/availability; command outcomes, shortcuts and recovery; focus, accessible names and keyboard dismissal; save-failure edit retention; Light/Dark and increased-contrast rendering; active/inactive selections and alternate user accents. Measure rendered text/icon contrast once actual colors and backgrounds exist. No runtime or accessibility pass is implied.

## Sources and evidence limits

Read the installed apple-hig root SKILL.md explicitly, then searched its topic index. Read the Foundations family and Branding, Color and Icons topic procedures before their source guides. Also read Menus and actions → Buttons and Presentation → Alerts, each procedure before its guide. All paths resolved inside `.agents/skills/apple-hig`; each instruction/source read used one file per shell command.

Material source support: [Branding](https://developer.apple.com/design/human-interface-guidelines/branding#Best-practices) supports recognizable identity with conventional controls and content priority; [Icons](https://developer.apple.com/design/human-interface-guidelines/icons#Editing) supports familiar command metaphors; [Color](https://developer.apple.com/design/human-interface-guidelines/color#macOS) supports semantic Mac colors and user-accent precedence; [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) supports system styling; [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) supports standard, contextual alerts. These official links identify the local guides' sources; no web browsing was performed.

Evidence consists of the short original interface.md and installed local guidance, a dated independent HIG interpretation snapshot. No source code, assets, palette, screenshot, deployment target or command inventory was supplied. Command candidates and the save-failure scenario are proposed contracts, not observed features. No device, SDK build, GUI, VoiceOver or other accessibility execution occurred. Product-name recognition, native rendering, measured contrast and above-the-fold fit require later validation.
