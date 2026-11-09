# visionOS gallery interaction specification

Purpose: browse artwork tiles, deliberately open an image, inspect it without sustained gaze, and return to the same gallery position. Assume a two-dimensional image gallery; no immersive scene or custom hand tracking is needed.

## Presentation and action contract

Use a movable standard window in Shared Space for browsing and detail, preserving system positioning and scaling. Do not lock content to the head or move controls toward gaze. Indirect activation works with hands resting in the lap or at the sides. Prefer standard system controls and their hover, press, and audible feedback. [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices)

Each tile is one button containing its thumbnail and visible artwork title, with one containing hover region. Its accessible name is “Open [artwork title]”. Detail has a visible “Back to Gallery” button with the same accessible name, and a meaningful text description of the artwork. These are nondestructive actions. Essential labels and return controls remain visible without hover.

## State transitions

| State | Input | Result |
| --- | --- | --- |
| Gallery | Look toward a tile | System hover emphasis only; no navigation, persisted selection, app event, or analytics write. |
| Gallery | Activate a tile with a standard targeted finger-thumb tap or supported alternative | Save gallery scroll position and originating tile; open that artwork in detail. |
| Detail | Look elsewhere, stop pointing, or wait | Keep the same image open. No stare requirement, app dwell timer, timeout, or gaze-loss dismissal. |
| Detail | Activate Back to Gallery | Restore gallery scroll position and the originating tile as the logical navigation return target. |

Hover is transient system feedback, distinct from persistent app selection and keyboard/assistive focus. Focus movement alone does not open an image. The app receives supported activation actions, not pre-tap eye coordinates or gaze-dependent hover callbacks for business logic. Activation does not prove an image was viewed or understood. [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes), [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS)

## Stable targets and feedback

Specify activation regions of at least 60 × 60 pt for tiles and Back to Gallery in visionOS layout coordinates. Leave at least 16 pt clear margins between neighboring tile bounds, including their activation regions. Keep button centers at least 60 pt apart and add at least 4 pt padding around buttons 60 pt or larger. Activation regions and hover feedback must not overlap. These are requirements to measure during implementation, not measurements of existing UI.

Use discernible rounded button shapes/backgrounds. Normal tiles show thumbnail and title; hover adds only standard system emphasis. Keep artwork, title, position, depth, and target bounds stable: no jumping, target chasing, expansion into neighbors, or peripheral animation. Activation gives standard press feedback and a visible navigation result; sound is supplementary.

The local Eyes guide discusses custom hover generally, while Buttons says custom button hover is unsupported. Use standard button effects throughout; no custom-hover API is required. Accessibility lists a 60 × 60 pt visionOS default and a smaller 28 × 28 pt minimum; this gallery uses the 60 × 60 pt target required by Buttons, not the smaller minimum. Visible glyph size is separate from activation geometry. [Eyes — Making items easy to see](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see), [Eyes — Custom hover effects](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects), [Buttons — visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS)

## Privacy and data boundary

Remove the per-person gaze heatmap feature. Do not collect, infer, store, or transmit eye coordinates, fixation sequences, hover histories, or time-looking estimates. System hover remains private; no permission prompt, Full Space mode, or custom gesture is proposed as a workaround. This revision introduces no analytics, including activation telemetry. Gallery return state is local interaction state only, not gaze evidence. [Privacy — visionOS](https://developer.apple.com/design/human-interface-guidelines/privacy#visionOS)

## Alternative input and accommodation

Expose Open and Back to Gallery with standard control semantics so supported assistive activation, Switch Control, and hand/head Pointer Control can perform the same transitions without eye targeting or mandatory speech. User-configured system Dwell Control may invoke the same activation; this is distinct from the app observing gaze or imposing its own dwell trigger. Keyboard navigation must reach every tile and Back to Gallery, show focus, and provide standard activation.

Validate the complete browse → open → inspect → return path with VoiceOver and supported alternative inputs. Preserve titles and actions at 200% text enlargement by reflowing rather than clipping or shrinking targets; support Zoom. Honor Reduce Motion without losing state or navigation; this design needs no automatic spatial movement. Measure contrast in implemented appearances, including Increase Contrast. [Accessibility — Mobility, Cognitive, and visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Acceptance contract

1. Looking across tiles without activation never opens content or changes stored state. No gaze/hover-derived telemetry is produced.
2. One activation opens the intended artwork. Looking away and waiting leave it open; Back to Gallery restores saved context.
3. Measure target dimensions, spacing, and nonoverlap against the rules above; hover leaves geometry and primary visuals stable.
4. Complete the same path with resting-hand indirect input, keyboard, VoiceOver, Switch Control, and hand/head Pointer Control on supported configurations. System Dwell Control must not need app gaze access.
5. Verify 200% text, Zoom, Reduce Motion, Increase Contrast, and sound-off feedback retain content and actions.
6. On a worn Vision Pro, assess targeting responsiveness, accidental activation, distraction, comfortable viewing, and posture variation. Document review does not satisfy runtime checks.
