# Furniture placement: revised specification

Platform: iOS/iPadOS handheld camera AR. Preserve furniture selection and dimensions in the existing prototype stack. Treat AR as an optional preview; product images and dimensions remain usable without a camera. No visionOS or Mac camera support is implied.

## Entry and permission

Opening a product must not start capture. Show its image and verified width/depth/height. On capable devices with a dimensioned model, offer “View in Your Room” with context: “Preview at actual size. Choose a well-lit, clear floor area. Stay aware of people and obstacles. Adjust from where you are.” Omit AR entry on unsupported devices or models without verified physical dimensions; never invent scale.

This is ordinary product context, not a custom permission pre-alert. Tapping View in Your Room requests system camera permission if undetermined. Purpose string: “The camera shows your room so you can preview furniture at actual size.” Begin capture only after authorization. Do not imitate the system alert. If denied or restricted, return to details with “Camera access is unavailable. You can still view furniture dimensions.” After denial offer Open Settings and Back to Details without repeated permission requests. Restricted access must not suggest Settings can necessarily resolve it.

Data contract: process camera frames and transient surface/pose estimates locally for this session; no recording, uploads, room analytics, or persisted room maps. Stop capture and release room data on Close. Retain product metadata only. No microphone, location, contacts or photo-library permission is needed. These are requirements for implementation, not claims about existing code.

## State and transition contract

| State | Presentation | Actions and transition |
|---|---|---|
| Finding floor | Live camera and system discovery coaching; no chair. “Find a clear floor area. Move the device slowly while staying in a safe spot.” | Close exits; Restart restarts discovery. Hide unrelated editing UI while coaching. |
| Ready | An indicator aligned to the current usable horizontal floor estimate; no floating chair. “Preview position — not yet placed.” Dimensions remain in screen space. | Place Chair commits only while tracking and the candidate remain usable; otherwise return to Finding floor. Use current estimates without waiting for exact floor edges. |
| Placed | Actual-size chair attached to the floor; “Placed — approximate preview.” | Adjust Position enters Adjusting. Rotate Left/Right changes yaw by 15° per activation. Close exits. |
| Adjusting | Immediate feedback on a floor-constrained draft; “Adjusting — confirm position.” | Move Left/Right/Nearer/Farther changes position 5 cm per activation on camera-relative floor axes. Rotate Left/Right changes yaw. Confirm Position commits; Cancel Adjustment restores the last committed transform. Invalid moves are disabled with “No floor estimate here”; never float the chair. |
| Recovering | On uncertain anchor or limited/unavailable tracking, hide chair and indicator and remove Placed immediately. “Placement paused. Finding your room again.” Use system relocalization coaching. | Disable placement/editing; Close and Restart remain available immediately. Stable tracking plus a recovered old anchor restores the committed placement. Tracking restored without the old anchor returns to Finding floor for fresh placement. Never trust tracking alone to restore the old location. |
| Inactive | On backgrounding/camera interruption, suspend capture and edits. Preserve selected product and last committed transform as unverified session state; discard any uncommitted adjustment. | Foregrounding enters Recovering, never directly Placed. |

Restart clears the transient map and anchor, retains product, dimensions and yaw preference, and enters Finding floor. Close is a persistent labeled screen-space button in every camera state, including coaching/recovery: stop capture, discard room placement and return to the same product details without movement or confirmation. A later AR entry starts new discovery. Close must remain available above coaching if needed.

No timeout blocks Restart or Close. If discovery/recovery fails to progress, show a relevant remedy: “Try more light or a floor area with visible detail,” or “Move the device more slowly.” Do not instruct backward walking, expansive sweeps or moving into another room. Encourage short sessions and taking a rest through an always available exit. The app does not detect all obstacles or certify safety/clearance. Product details say “Check real measurements and clearances before buying.”

## Grounding and input

Render at fixed 1:1 physical scale from verified dimensions. No pinch scaling or enlarging distant furniture to imply proximity. Where supported, floor classification may restrict placement; otherwise guide selection of a horizontal floor without claiming automatic classification. Surface detection does not certify free space.

Refine estimates gently, retaining surface contact, perspective, plausible lighting and diffuse shadow. If a correction would cause a visible jump or detachment, enter Recovering rather than teleporting. Target 60 scene updates per second as performance guidance, pending measurement on supported devices.

Optional shortcuts: tap the chair to select; one-finger drag repositions on valid floor; two-finger rotation changes yaw. Drag/rotation enter Adjusting and share its Confirm/Cancel contract. Expand reasonable hit proximity for thin/distant chair parts without stealing control taps. Visible controls cover placement, movement, rotation, confirmation and exit; no gesture or locomotion is essential. Provide an offscreen directional hint while retaining indirect controls. Preserve system Back/edge gestures, three-finger editing gestures and iPad four-finger multitasking; no movement gesture closes AR.

## Controls and adaptation

Use native buttons with action labels, semantic roles, enabled states and press feedback. Place Chair and Confirm Position are prominent in their respective states; other commands are secondary. Move/rotate affect only the selected chair in discrete steps. Require at least 44 × 44 pt activation regions and nonoverlapping separation for every session button. Keep frequent controls in the middle/lower safe region and Close always visible within safe areas. Status and critical instructions stay in screen space, paired with text/symbols rather than color or sound alone.

Support native text enlargement to at least 200% without losing actions or status. Expose product name, dimensions and placement state as accessible content. Names match button labels; expose roles, disabled states and reasons. Task access order: Close, status, chair summary, current primary action, then adjustment/recovery controls. All commands must support assistive activation and Full Keyboard Access, with no accessory required for touch. This does not establish nonvisual spatial usability: retain non-AR dimensions and validate AR with assistive-technology users.

Use most of the display for the scene. At wide iPad widths, adjustment controls sit alongside it; at compact widths, stack controls below status in a bounded scrolling area, keeping Close and the primary action visible. Adapt iPhone portrait/landscape, iPad resizing/multitasking and enlarged text without shrinking targets. Preserve selection, committed pose and draft across resizing; interruptions follow Inactive/Recovering. If camera availability changes, do not assume multitasking capture support. Respect safe areas and measure contrast of actual control/status backing against bright/dark camera imagery in light/dark appearances.

## Design basis

Local sources: [AR coaching, placement and recovery](https://developer.apple.com/design/human-interface-guidelines/augmented-reality), [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) and [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados). Links identify official articles; no online verification occurred. Step sizes, labels, immediate hiding, confirmation and the no-upload contract are product decisions applying this guidance, not universal Apple mandates.
