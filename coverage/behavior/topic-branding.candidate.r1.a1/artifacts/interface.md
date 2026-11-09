# Mac invoice editor — restrained brand specification

Platform: macOS. Purpose: let people read and edit invoices while retaining a recognizable product identity. This specification replaces the supplied logo-command, neon-state, and 150-pixel wordmark treatment. No application framework or executable interface was supplied.

## Identity and content hierarchy

- Remove the 150-pixel wordmark banner and its reserved vertical space from the editor. Begin the document area with the invoice identifier, customer and editable invoice content; branding must not precede them as a separate vertical section.
- Retain the existing product name and logo artwork as recognition cues. Place a single noninteractive identity lockup in the editor's existing header row: logo at most 20 × 20 pt and product name at standard system label size. No colored panel, oversized type, duplicate wordmarks, or extra header row. At constrained widths, omit the logo first and then the product-name label before truncating invoice identification or hiding editing actions. These dimensions and priorities are product decisions, not Apple requirements.
- Retain the product's existing app icon and name on established identity surfaces. Keep invoice issuer/customer logos in invoice content distinct from the editor's product branding; do not modify invoice data or exported invoice branding as part of this change.
- Use concise, consistent product language and system typography for editor labels. Do not introduce a custom brand font.

## Editing commands

Replace every logo used as an editing-command glyph with an action-specific conventional symbol or a clear text label. Audit the actual command inventory during implementation; the examples below apply only where those commands exist.

| Command / accessible name | Preferred glyph | Outcome and scope |
|---|---|---|
| Cut | scissors | Cut selected editable content using existing behavior |
| Copy | document.on.document | Copy selected content |
| Paste | document.on.clipboard | Paste into the active editable destination |
| Undo | arrow.uturn.backward | Reverse the last eligible edit |
| Redo | arrow.uturn.forward | Reapply the last undone edit |
| Add Line Item | plus | Insert an invoice line item |
| Delete Line Item | trash | Remove the selected line item using existing recovery behavior |

Use suitable system symbols when available in the implementation's supported OS range; otherwise use a text label or simple monochrome template glyph with the same familiar metaphor. Do not assume symbol availability from this specification. Match adjacent glyph weight and size. Every icon-only control must expose its action name and a brief matching tooltip. The product logo never substitutes for an action symbol.

Use system control styles and standard Mac sizing. Preserve each command's existing location, menu equivalent, shortcut, enabled-state conditions, target and recovery semantics. Controls show normal system pressed, disabled and keyboard-focus states. Branding changes must not change default/Return activation, selection, focus restoration, clipboard contents or undo history. This brief does not establish those existing behaviors; inspect and record them before changing controls. No editing command gains prominence merely to display brand color.

## Color and state contract

| Role | Revised treatment |
|---|---|
| Document and window surfaces | Semantic document/window backgrounds; remove neon brand fills |
| Text and separators | Semantic primary/secondary text and separator roles |
| Text selection | System text-selection foreground/background, including inactive selection |
| Selected invoice rows | System content-selection foreground/background, including inactive selection |
| Focus, disabled and pressed states | System control rendering; no brand overlay |
| Interactive accent | Use the system accent mechanism. A restrained existing brand accent may be the app accent under macOS Multicolor; a user-selected accent takes precedence |
| Alerts | Standard macOS alert surface, text, buttons and consequence-based roles; no neon background, custom brand tint or decorative wordmark |

Use dynamic semantic roles through the existing framework, never copied RGB system swatches. Essential states must remain understandable through selection geometry, labels or symbols as well as color. Retain the normal app identity icon in alerts where supplied by the system; reserve caution imagery for circumstances needing extra attention. Do not add alerts for branding or routine status.

This is a visual replacement, not a redesign of alert triggers or consequences. Inventory each existing alert's trigger, copy, actions, role/default, cancellation and result before implementation; retain the contract while restoring standard presentation. If no contract can be established, resolve it before shipping. Do not infer destructive/default roles from existing neon color alone.

## Acceptance contract

1. No editing-command glyph is a logo; each command has a distinct meaningful symbol or explicit label. Test that its action, name, shortcut and enabled state agree.
2. The 150-pixel brand banner and its spacer are absent. At the same window size, invoice content begins earlier by the removed banner's actual layout allocation; the original pixel statement is not a measured point value.
3. At a product test fixture of 1024 × 768 pt, initial scroll position, the invoice identifier, customer and at least the first line item are visible. When width is reduced or labels grow, the compact identity yields first; commands and invoice identification remain usable. This fixture is a proposed product check, not a HIG minimum or a verified layout.
4. Test light/dark appearance, Increase Contrast, active/inactive selection and several user accents including Multicolor. Text selection, selected rows, focus and alerts use semantic rendering without brand overrides; states remain distinguishable without relying on hue alone.
5. Exercise all replaced commands with keyboard and pointer. Verify action names with VoiceOver, visible focus, glyph legibility at displayed size, and label expansion without overlap. Test all existing alert exits, Return/Escape behavior and data results against the recorded contract.
6. Show the revised editor to representative users and ask them to identify the product and begin editing an invoice. Record recognition and task-start results; retained branding cues alone do not establish recognition success.

## Guidance basis

Apple recommends content priority and familiar interaction conventions in [Branding, Best practices](https://developer.apple.com/design/human-interface-guidelines/branding#Best-practices); semantic colors and user-accent behavior in [Color, macOS](https://developer.apple.com/design/human-interface-guidelines/color#macOS); familiar editing metaphors in [Icons, Editing](https://developer.apple.com/design/human-interface-guidelines/icons#Editing); system styling and action labels in [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons); and standard contextual alert treatment in [Alerts, macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS). These links identify the official sources behind the installed local guidance; no web verification was performed.
