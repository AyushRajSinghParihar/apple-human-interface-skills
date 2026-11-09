# Action icon repair

Patched `interface.md` in place into a concrete macOS specification. The supplied evidence was one sentence, with no code, screenshots, asset inventory, deployment target or backend contract.

## Decisions and changes

- Reserved the star for Favorite, with outline/filled state and visible next-action labels. Replaced the toolbar's Delete star with trash plus Delete. Removed the Publish star in favor of text. Unfamiliar custom actions require outcome-specific labels.
- Added consistent baseline metrics, symbol weight/scale, optical padding, template rendering and text fallbacks for unavailable symbols.
- Defined shared validation, native disabled visuals and semantics, blocked activation, explanations, pending/error behavior, focus, menu access, overflow and recovery.
- Chose reversible library deletion and preconfigured single-asset publication as explicit product assumptions. These require implementation verification; they are not discovered capabilities or Apple-prescribed product behavior. Favorite's star, the 8 pt gap and text-only Publish are project choices. Standard trash and consistent metaphors come from local HIG guidance linked in the revised specification.

## Worked before/after

Before: `Poster.png` has a Favorite star in its row, while an identical toolbar star deletes it and an identical menu star publishes it. The brief reports unlabeled unfamiliar pictograms and active-looking disabled icons. The star does not predict a stable outcome.

After: select editable, unpublished `Poster.png` with a configured destination. The row shows outline star + Add to Favorites. Activation commits Favorite, then shows filled star + Remove from Favorites; a second activation restores off. Trash + Delete removes the selected asset from the library; Edit > Undo Delete restores it. Asset > Publish is a text command publishing it to the configured destination with pending/result status. Clearing selection leaves Delete and Publish visible but dimmed and inoperable, with selection guidance. This is a specification trace, not an executed scenario.

## Acceptance checks

| Check | Status and evidence |
| --- | --- |
| Required specification patch and result report | Passed: written and read back locally. |
| Original three star meanings separated | Passed by document inspection: only Favorite retains the star. |
| Unlabeled actions, alignment and disabled appearance addressed | Passed at specification level: explicit label, baseline and disabled-state contracts. Artwork and runtime behavior remain unverified. |
| Scope, availability, pending/failure and recovery defined | Passed at specification level: row versus selection scope, deletion recovery and remote publication limits are explicit. |
| Installed skill routing | Passed: read installed root, searched topic index, then read owning families and topic procedures before source guides. Topics: Icons, SF Symbols, Buttons, Toolbars, Menus, The menu bar, Accessibility, Toggles, Undo and redo. Each file read used a separate single-file command. |
| Favorite twice; Delete/Undo/Redo; failures and duplicate publication | Not executed. Accept only correct persisted state, restored asset identities/selection, truthful failure and no duplicate publication. |
| Empty/multiple/read-only selection, multiple windows, narrow/hidden/customized toolbar | Not executed. Accept only frontmost-window validation and reachable menu equivalents. |
| Actual symbols, baseline alignment, appearance, contrast, localized and 200% enlarged labels | Not executed. Reject missing glyphs, clipping, overlap, indistinguishable disabled states or lost metaphors. No contrast or target measurements exist. |
| Keyboard, VoiceOver, Accessibility Inspector, focus restoration | Not executed. Verify names, roles, values, states, reachability and disabled activation blocking on macOS. |
| Deployment SDK, symbol availability and restrictions | Not executed. Confirm before using symbols; text-only fallbacks are specified. |

Failed checks: none among completed static document checks. The original brief reports defects; no repaired runtime behavior has passed testing.

## Evidence limits

Used only supplied local files and installed instructions. No browsing, device, GUI, SDK compilation, accessibility execution, image inspection or user testing occurred. Official article links in `interface.md` identify guidance read through local dated application-guidance snapshots; these are not SDK documentation or independently verified current Apple pages.

The local Buttons guide's general 44 × 44 pt hit-region statement differs from Accessibility's macOS 28 × 28 pt default / 20 × 20 pt minimum. The patch explicitly uses the Mac-specific default for custom rows, retains native menu/toolbar geometry, and leaves actual geometry and comfort to runtime verification. The menu-bar source also flags inconsistent general-versus-specialized ordering wording; the patch uses concrete app-specific placement between View and Window without inventing a universal hierarchy rule.

Actual Delete recovery, Publish destination and external effects, remaining custom pictogram meanings, symbol support and framework behavior remain evidence limits. The deliverable repairs the specification; the concrete contracts must be implemented and checked before release.
