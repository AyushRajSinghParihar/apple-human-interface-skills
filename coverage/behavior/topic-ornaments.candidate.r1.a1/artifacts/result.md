# Revised visionOS sketch-tool interaction specification

## Scope and evidence

`interface.md` states that detached, head-locked tool strips follow gaze and cover the selected drawing; contextual actions must persist on a movable, resizable window. This is a textual description, not an inspected implementation. The specification below replaces that placement model without requiring an Apple SDK.

Assumptions: this is a contained, two-dimensional sketch task in a Shared Space window. The exact command inventory, dimensions, drawing input method, and existing toolbar are unspecified. Illustrative commands below are proposed product choices, not observed controls. Preserve the existing drawing engine and document model.

## Decisions and source support

1. **Keep the canvas in a person-positioned window.** Ordinary sketch controls do not establish a need for a volume or Full Space. Keep the window anchored in surrounding space, with dynamic scaling; do not move tools or content in response to gaze or head motion. Preserve system recentering. Sources: [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [Spatial layout — Field of view and Scale](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Field-of-view).
2. **Use one bottom, window-attached tool surface.** Prefer the standard visionOS toolbar presentation when the tools are ordinary toolbar actions. Do not create a duplicate custom ornament. If persistent contextual controls cannot be represented by that surface, use one custom ornament with the same attachment contract below, replacing rather than supplementing the strip. Ornaments support persistent contextual tools without covering content; they remain parallel, slightly forward, follow the window, and stay stable during scrolling. Sources: [Ornaments — Best practices](https://developer.apple.com/design/human-interface-guidelines/ornaments#Best-practices), [Toolbars — visionOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#visionOS).
3. **Keep frequent actions visible and bounded.** The surface remains visible while sketching, selecting, panning, or scrolling. Its width never exceeds the window width; it must also clear window-management controls. No vertical tool strip or downward pull-down menu. Move infrequent options into a reserved in-window controls region that reduces the canvas viewport rather than overlaying it. This region is a product proposal; Apple recommends reducing ornament weight and relocating lower-priority tools into the window. Sources: [Ornaments](https://developer.apple.com/design/human-interface-guidelines/ornaments#Best-practices), [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars#visionOS).
4. **Protect target spacing and essential access on resize.** For regular visionOS buttons, use at least 60 pt center spacing and 16 pt gaps, with nonoverlapping targets and feedback. These are visionOS points, not Linux pixels or physical centimeters. Enforce a minimum window width derived from essential controls, localized labels, spacing, and management-control clearance; do not squeeze targets to fit. Sources: [Spatial layout — Best practices](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Best-practices), [Toolbars — visionOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#visionOS).

## Placement and state contract

The renderer receives window pose, window bounds, safe window-management regions, measured control sizes, and current canvas viewport. It must not use gaze coordinates to position the surface. Gaze targeting may highlight a control through standard platform feedback; merely looking must not execute a command or change selection.

| Object | Anchor, scale, and depth | Required behavior |
|---|---|---|
| Canvas | Window-local; inherits window dynamic scaling | Drawing content occupies an explicit viewport; no tool surface or tool hit region overlaps it |
| Tool surface | Bottom edge of parent window; parallel and slightly forward | Moves and scales with that window; independent of canvas pan/zoom/scroll; no detached dragging |
| In-window options region | Reserved layout area beside canvas, same window | Open only on explicit Options activation; reflow viewport, never cover it; close via visible Close Options action |
| System management controls | Owned by platform/runtime | Leave visible and operable; never intercept their input or introduce a competing recenter gesture |

“Bottom” means the standard bottom toolbar zone above management controls, not a strip drawn across the bottom of the artwork. For a custom renderer, validate the projected visual footprint and hit regions from the supported viewing poses. A small forward depth offset can still obscure content in projection; a local-coordinate nonintersection check alone is insufficient. Do not hard-code a depth in meters or a universal field-of-view angle: neither is established by the supplied evidence.

Proposed action contract (replace example labels with the actual product inventory before implementation):

| Action | Scope and availability | Placement and result |
|---|---|---|
| Draw / Select | Persistent mode choice; exactly one active | Always visible; explicit activation changes mode; selected state is visible |
| Selection action, e.g. Duplicate | Current selection only | Stable contextual slot; disabled with no valid selection; activation acts once, preserves original selection identity unless product semantics require otherwise |
| Options | Secondary controls for current mode/selection | Visible labeled action opens reserved region; repeat activation or Close Options closes it |

No new destructive action is introduced here. Retain existing recovery behavior for document edits. Do not assume a menu bar or an undocumented visionOS overflow mechanism supplies missing commands. At narrow widths, remove secondary inline options first; retain their Options route. If the essential surface still cannot fit, stop resizing at its measured minimum width. If the host cannot enforce that minimum, its placement adapter is incomplete: do not ship an overlapping fallback.

```text
state = {document, selectionIds, activeTool, canvasTransform, optionsOpen}

on layout(windowGeometry, platformSafeRegions):
    items = essentialTools + contextualSlot + Options
    requiredWidth = measure(items, localizedLabels, targetSpacing, safeClearance)
    require windowGeometry.width >= requiredWidth
    surface = attachToBottomToolbarZone(windowGeometry, platformSafeRegions)
    require surface.width <= windowGeometry.width
    require disjoint(surface.visualAndHitFootprint, managementRegions)
    viewport = reserveOptionsAreaIfOpen(windowContentBounds)
    require disjoint(surface.projectedFootprint, viewport)
    publishLayoutAtomically(surface, viewport)

on windowMoveOrResize:
    recompute layout using parent window transform
    preserve document, selectionIds, activeTool, canvasTransform, optionsOpen

on canvasPanZoomScroll:
    update canvasTransform only; keep surface fixed to window

on selectionChange(ids):
    update selectionIds and contextual availability in stable slots
    do not reposition surface toward selection

on activateOptions:
    toggle optionsOpen; recompute viewport without changing document coordinates

on gazeOrHeadMotion:
    no placement or document-state transition
```

These are abstract contracts, not SDK API names. Runtime adaptation must preserve window agency and use the platform's standard interaction behavior where available. Indirect activation must support resting hands; relocating sketch tools must not introduce a repeated reaching requirement. The underlying stroke-input technique remains outside the supplied brief.

Visibility: no automatic hiding, focus-only mode, or customization is introduced. On returning from an existing modal editing flow, restore this normal tool surface and its active tool/selection. If the host temporarily suppresses controls, restore them when the window becomes active; no hidden gesture may be the sole restoration route.

## Worked before / after

**Before, from the brief:** A drawing is selected. The tool strip follows the person's gaze onto that drawing and obscures it. The person then moves or resizes the window, but the supplied description gives no reliable attachment or resize behavior.

**After, specified scenario:** Select stroke group A near the lower edge. The bottom tool surface stays in its reserved zone, outside the canvas viewport; the contextual slot becomes available without jumping toward A. Activate Duplicate if that command belongs to the product. The action changes the document according to existing edit semantics; looking at it alone does nothing. Open Options: a reserved side region reduces the viewport while retaining document coordinates and selection. Close Options to recover the viewport. Move the window: the surface follows in the same transform update. Scroll the drawing: only content moves. Resize narrower: secondary inline options collapse into the explicit Options route; essential targets retain spacing. Further shrinking stops at the measured minimum. None of these operations clears A, switches tools, or moves the strip independently of the window.

## Acceptance checks and current status

**Passed — specification inspection only:** The revised contract defines a parent-window anchor, bounded width, forward/parallel relationship, stable scrolling behavior, management-control clearance, narrow-width behavior, persistent visibility, restoration, and state preservation. The worked scenario covers selection, options, movement, scrolling, and resizing. These are document-level checks, not runtime passes.

**Failed — supplied baseline description:** The described strip obscures selected content and follows gaze while head-locked. That conflicts with the intended unobscured canvas and spatial anchoring guidance. No executable baseline was available to reproduce it.

**Not executed — required implementation acceptance:**

| Check | Pass condition |
|---|---|
| Geometry at wide and minimum widths | Surface width ≤ window width; regular button spacing ≥ 60 pt center-to-center and gaps ≥ 16 pt; localized essential labels fit; no target overlap |
| Selection at every canvas edge | Selected artwork stays visible; visual and hit footprints do not cover the canvas |
| Window move and resize | Surface follows parent without independent drift or visible lag; document, selection, mode, options state, and canvas transform survive |
| Pan, zoom, scroll | Surface stays fixed to window; only canvas content changes |
| Management controls | Window move/resize controls remain visible and activatable, including with Options open |
| Narrow window | Secondary options remain reachable; essential actions stay visible; shrinking below measured minimum is prevented |
| Activation and restoration | Looking never executes actions; explicit activation works; returning from modal/host suppression restores tools and context |
| Spatial and input validation | Worn-device testing confirms projected clearance, stable depth, legibility, and resting-hand use across supported postures and window positions |

## Evidence limits and route audit

Only supplied local text and installed guidance were used; no web access occurred. Official links above identify the source articles, not pages checked live. Local references identify snapshots dated 2026-10-25 and are derived guidance, not SDK documentation or proof of independent source review. No conflicting rule was found in the selected passages.

Read order: installed `apple-hig/SKILL.md`; `interface.md`; relevant topic-index rows; Getting started family → Designing for visionOS procedure → source guide; Menus and actions family → Ornaments procedure → source guide; Toolbars procedure → source guide; Foundations family → Spatial layout procedure → source guide. Every instruction/source read used a separate single-file command under `.agents/skills/apple-hig/`.

No device, SDK, GUI, rendering, compilation, eye/hand tracking, physical comfort, accessibility, or assistive-technology execution occurred. Exact dimensions, safe regions, command inventory, localization fit, and runtime attachment remain unverified. This document specifies intended behavior; it does not establish a working implementation or accessibility conformance.
