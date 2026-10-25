# Layout repair result

Patched `interface.md` in place from the supplied one-sentence problem statement into a concrete visionOS layout and interaction contract. The three research panels remain; panel roles are explicitly assumed because the brief did not name them.

## Decisions and patch summary

- Replace tall, surrounding panels with three bounded regions in one Shared Space window. Specify a 1200 × 680 pt proposed expanded layout, internal scrolling, and a compact one-panel arrangement that retains access to all three panels.
- Replace rigid head-follow with stable spatial anchoring, system dynamic scaling, user positioning, and system recentering. No fixed field-of-view angle or room size is assumed.
- Separate reading from model inspection. A bounded model replaces the reading body temporarily; titles, return action, and rotation controls stay outside its geometry. Returning restores reading context.
- Replace the 2 m reach requirement with indirect interaction usable with resting hands, explicit model actions, and alternative activation. Add target bounds/spacing and nonoverlapping hover requirements.
- Specify state retention, 200% text enlargement, compact reflow, and checks for Pointer Control, Zoom, and Reduce Motion.

Window dimensions, panel proportions, names, compact threshold, and the model-inspection flow are product design proposals. Apple guidance supports the underlying comfort, anchoring, scaling, separation, and input choices; it does not mandate these dashboard dimensions.

## Worked before / after

Example task: select a paper, read a finding, inspect its 3D subject, and record a note. This is a specification walkthrough, not an observed user session.

| Step | Before, based on supplied brief | Revised behavior |
|---|---|---|
| Find the finding | Tall panels extend above and behind the seated person. | Reading stays in a bounded central region; long text scrolls. If three regions feel too broad, activate Compact layout and Reading. |
| Read critical text | Text intersects 3D objects. | Reading uses a clear plane. Inspect model explicitly replaces the reading body; model bounds exclude title and controls. Return to reading restores the passage. |
| Rotate and take notes | Controls require reaching 2 m. | Activate Rotate left/right or Reset view indirectly with hands resting; activate Notes and enter the note without reaching the model. |
| Look toward the room | Content follows every head turn. | The window stays in space. Looking away leaves the room view available; returning reveals the same task state. |
| Use a smaller arrangement | Room dimensions are unknown. | Compact mode needs no room measurement; switching panels preserves source, scroll position, inspection state, and unfinished note. |

## Acceptance checks and status

**Passed — document inspection only:**

- `interface.md` was changed in place and contains explicit remedies for all five supplied defects.
- Anchor/scale/depth contracts cover the window, panels, and model. Unknown room size has a stationary fallback.
- Geometry arithmetic is internally consistent: 48 pt outer insets + 48 pt gaps + 240 + 624 + 240 = 1200 pt; height 680 − 48 = 632 pt. Two adjacent 60 pt buttons with a 16 pt gap have 76 pt center spacing.
- The worked task has selection, reading, inspection, return, and notes paths; transitions preserve useful state.

**Failed:** none found in this static specification review. This does not establish implementation conformance.

**Not executed — implementation acceptance gates:**

1. On a worn Vision Pro, complete the worked task seated at varied heights/postures with hands resting. Fail if essential work requires reaching, standing, repeated large turns, or panels above/behind the person. Check both expanded and compact arrangements; revise proposed dimensions if necessary.
2. Turn the head away and back; confirm no head lock or chasing. Move the window using system controls; confirm dynamic scaling remains readable and system recentering is preserved.
3. Rotate the model through its full range. Fail if geometry intersects critical text, action targets, or hover regions; confirm Return to reading restores the passage.
4. Resize across 1200 pt and 480 pt, switch panels, and enlarge text to 200%. Confirm all content/actions remain reachable, targets stay separated, and notes/selection/scroll/model state survive.
5. Measure actual activation and hover bounds; test eye/hand responsiveness and absence of gaze-triggered state mutations. Complete the same task with supported keyboard/assistive activation, hand/head Pointer Control, and Zoom. Test Reduce Motion without loss of state or meaning.

## Evidence and limits

Read the installed root `apple-hig/SKILL.md` explicitly, then the Getting started, Foundations, and Inputs family procedures. Read the routed Designing for visionOS, Spatial layout, Accessibility, and Eyes topic procedures before their respective local source guides. Searched the installed topic index for visionOS, spatial layout, and eye/gesture concepts before finalizing this route. Each instruction/source file was read by its own shell command.

Material source links are included in `interface.md`: [visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos), [spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout), [eyes](https://developer.apple.com/design/human-interface-guidelines/eyes), and [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). They identify the local snapshot's official source; no web browsing occurred. The platform guide's “relative to the head” placement wording is applied as comfortable initial orientation, alongside the spatial and accessibility guides' explicit advice against rigid head locking.

Only a textual brief and installed guidance were available. There is no scene, screenshot, implementation, room measurement, SDK build, GUI session, accessibility execution, or device test evidence. Source geometry and a prose walkthrough cannot establish physical comfort, actual occlusion, native rendering, gaze accuracy, or assistive behavior. Those remain pending acceptance gates above.
