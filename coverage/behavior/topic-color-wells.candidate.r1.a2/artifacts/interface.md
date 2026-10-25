# Accent-color selection — revised macOS specification

## Control and targets

Accent color means the existing shape color property, not the macOS system accent preference. Preserve its existing color representation and precision. Replace the randomizing square with a standard macOS color well and persistent label “Accent color”. Start with a 28 × 28 pt activation area, the local guide's macOS default, and separate adjacent actions. The visible swatch may be smaller. Evaluate and prefer the system picker and its saved colors; preserve the project's framework. Opening or focusing the well never changes content.

Only selected editable shapes in the active document are targets. With no selection, disable the well and show “Select editable shapes”. If any selected shape is locked/noneditable, disable it and show “Selection includes locked shapes”; do not silently edit a subset.

## Display states

| State | Display and accessible value |
| --- | --- |
| Uniform selection | Actual color swatch and readable color value, including color space where needed to distinguish values |
| Mixed selection | Neutral swatch with a dash and text “Multiple colors”; never black or the first object's color |
| Actual black | Black swatch and its value, distinct from mixed |
| Unavailable | Disabled well and the relevant explanation above |

Refresh on selection, document, and underlying color changes. Use adaptive system labels and a visible swatch boundary. Distinguish keyboard focus, well activation highlighting, and persistent shape selection. User-selected content colors must not recolor essential control labels.

## Picker transaction

Maintain a session token, document identity, target shape identities, and each target's original color. Preview is a rendering overlay separate from saved data and undo history. Application-owned Apply and Cancel actions accompany the system picker; do not assume the native panel provides these semantics.

1. Click, Space on the focused well, or assistive activation opens the picker, highlights the well, and snapshots targets. Initial picker synchronization is not a color choice. Mixed colors remain unchanged until an explicit choice.
2. Each explicit valid choice previews one color on every session target and the well; mark the value “Preview”. Repeated choices replace that candidate. Unselected shapes and other properties stay unchanged. Invalid or unsupported input leaves the last valid preview intact, explains the problem inline, and disables Apply until corrected. Never silently substitute black or lose precision.
3. Apply requires a valid explicit choice. Atomically commit the final color, close/deactivate the session, and create one “Change Accent Color” undo operation. A choice identical to all originals creates no history entry.
4. Cancel, Escape, Command-Period, and picker close discard the overlay and restore the exact original display, including mixed colors. They create no history, dirty-state, or saved-data change. Closing never implies Apply. Nested native picker editing may consume Escape first; once that interaction ends, Escape cancels the session.
5. Before a selection change, target deletion/locking, document switch/close, or another edit to target colors, cancel the preview and invalidate its token, then process the new action and refresh the well. Ignore callbacks from invalidated sessions. Reopening captures fresh targets. No callback may modify a stale selection or another document.
6. Save/autosave serializes committed data only. Undo during preview cancels that preview without consuming history. After Apply, Command-Z restores each original per-shape color and Shift-Command-Z reapplies the final color. Use standard Edit Undo/Redo entries with the operation name. New committed edits after Undo clear that redo branch. Preserve existing save/open history policy and avoid adding an arbitrary history limit. Reveal affected content when reversal would otherwise be invisible.

## Color transfer

Preserve macOS dragging between wells and from the picker. Export a concrete color only; mixed/disabled wells export no fabricated value. Copy the color property without changing/deleting the source, including within this editor: property copying is the deliberate exception to container move defaults. Option never changes this into destructive movement.

Accept a single supported native color representation. Reject noncolor, multiple-color, unsupported, or unavailable-target drops without mutation. Highlight only eligible destinations and clear feedback on exit, cancel, or failure. Use native drag representation/copy feedback. A valid drop onto an idle well snapshots the current targets and opens the same transaction with the color staged; during a session it replaces the candidate. Apply/Cancel still governs persistence. Revalidate targets at drop time. Picker selection supplies a non-drag alternative.

## Keyboard and accessibility

With macOS keyboard navigation and Full Keyboard Access enabled, Tab/Shift-Tab reaches and exits the well in inspector reading order without changing shape selection. Space activates it. All picker choices and Apply/Cancel must be reachable without a pointer. Preserve native picker editing keys; Return in a field must not accidentally Apply the whole session. Activate Apply explicitly. Return focus to the initiating well on completion if available; after a user context change, honor the new destination instead of stealing focus.

Expose the native well role, name “Accent color”, matching color value or “Multiple colors”, disabled state, and activation action. Expose Preview state text and labeled Apply/Cancel actions. A tooltip or hue alone cannot convey meaning. Use standard system focus effects. Start with macOS default 13 pt text; at 200% text enlargement reflow labels, values, explanations, and actions so they remain readable and reachable. Evaluate actual label/boundary/focus/mixed-marker contrast in Light, Dark, and Increase Contrast appearances. Arbitrary shape colors do not determine control text colors.

## Basis and scope

The installed local snapshot supports system-picker preference, synchronization, activation highlighting, and Mac color transfer: [Color wells](https://developer.apple.com/design/human-interface-guidelines/color-wells#macOS). Labels, noncolor cues, sizing, and access follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Keyboard paths and separate focus/selection follow [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices) and [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices). Transfer and recovery follow [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop) and [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS).

Selection scope, mixed-state dash, locked-selection policy, Apply/Cancel staging including drops, session invalidation, and overlay persistence are product decisions for this repair, not universal Apple mandates. Native integration and API availability require implementation and SDK verification. Acceptance scenarios and evidence limits are in result.md.
