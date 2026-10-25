# Shared gallery: Apple TV and Vision Pro contracts

## Scope and evidence

`interface.md` supplies 20 objects with details and describes five problematic behaviors. This is a replacement interaction specification, not an implemented or device-tested interface. No framework, assets, object dimensions, SDK version, or runtime was supplied. “Shared” is interpreted as the same gallery dataset across platforms, not simultaneous collaboration. Objects are treated as ordinary gallery content; genuine 3D inspection is not established.

The installed apple-hig root, Getting started and Inputs families, their tvOS, visionOS, Focus and selection, Eyes, Remotes, and Gestures procedures were read before their source guides. The Foundations family and Accessibility and Spatial layout procedures were likewise read before their guides. All evidence came from local files; official links below identify the locally supplied source guidance and were not browsed.

## Shared task and state

Both contracts implement `Gallery → deliberate activation of object → Detail(objectID) → return to Gallery` with identical object identity and detail content. Browsing alone never opens detail or changes committed selection.

Persist `orderedObjectIDs`, `route`, `selectedObjectID` (last deliberately opened object), `returnAnchorID`, and `galleryScrollAnchor` (object ID plus viewport offset). Save return context before entering detail. Keep transient TV focus, system gaze hover, and committed selection separate. A subtle “Last opened” label can express committed selection independently of the current interaction target; it must not resemble focus or hover.

On return, resolve the saved ID before drawing the gallery, restore the viewport, and expose the returned object. If data changed, use the nearest surviving object in the prior order, preferring the successor then predecessor; if empty, show “No objects” with no phantom card. A load failure stays in detail with a labeled Retry and the platform return action; return remains usable. No timers or automatic route changes. These fallback and persistence rules are product decisions, not quoted HIG mandates.

## Contract 1 — Apple TV / tvOS

**Presentation.** One gallery screen with a four-column, five-row logical grid, vertically scrollable as needed. Each card combines artwork and title into one focusable action. Use large recognizable images and legible titles for across-room viewing; reserve space around cards so the system focus enlargement does not clip or cover neighbors. Four columns is an initial design choice pending actual television layout checks. Prefer native focusable components and system focus effects. [Designing for tvOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Focus and selection, tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS).

| State/input | Required transition and feedback |
|---|---|
| First gallery entry | Focus object 1; show a clearly raised/highlighted target. Do not open detail. |
| Left / Right | Move to the adjacent card in the same row. At an outer edge, remain there; no wrapping. |
| Up / Down | Move one row in the same column. Scroll enough to reveal the focused card. At the first/last row, remain there. |
| Siri Remote swipe | Directional navigation with platform scrolling/momentum feedback; never a pinpoint free cursor. Each settled target is visible. |
| Select press on a card | Show pressed feedback, save return context, commit its ID, and open that object's detail. Merely resting a finger or moving focus does not open it. |
| Detail entry | Focus a visible “Back to Gallery” action; show object title, image and detail text. Scroll long content through ordinary remote input. |
| Back button or “Back to Gallery” | Navigate to the gallery parent, restore scroll and focus to `returnAnchorID`, even if that card was offscreen before restoration. |
| Back at gallery root | Allow the system Home behavior. Holding Back retains system Home behavior. |

Focus route: every card is reachable from object 1 by row/column movement and can return by the reverse route. Detail has one return action plus its scrollable content, with no isolated interactive region. No playback exists in the supplied brief, so Play/Pause receives no gallery-specific action. Preserve remote system meanings. [Remotes, Best practices / Gestures / Buttons](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices).

**State appearance.** Unfocused cards recede; focused cards use system emphasis; pressed feedback is immediate; “Last opened” persists as focus moves. Unavailable content is labeled and not activatable. If a focused object disappears during directional browsing, move focus to a nearby one-step surviving target rather than leaving focus invisible. This live-removal rule is separate from the saved-return fallback. [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

## Contract 2 — Apple Vision Pro / visionOS

**Presentation.** A single movable standard window in Shared Space contains a responsive scrollable gallery and its detail route. Start with four columns where comfortable; reduce columns when window size or text enlargement requires it. The system places the initial window; retain dynamic scaling and space anchoring rather than head locking. Details replace the gallery content in the same window. No volume or Full Space is needed for the evidenced browse/read task; if true 3D inspection is later supplied, specify that separately. Do not take over system recentering or immersion controls. [Designing for visionOS, Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [Spatial layout, Scale / Best practices](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Scale).

| State/input | Required transition and feedback |
|---|---|
| Gallery entry | Show the saved viewport, or the beginning on first entry. Do not fabricate a gaze target or TV-style focus. |
| Look at a card | System hover subtly emphasizes the containing artwork-and-title region. No route, selection, viewed flag, or app business logic changes. |
| Look + indirect finger-thumb tap | Activate the standard card action, save return context, commit its ID, and open detail. Hands may rest in the lap or at the sides within supported tracking conditions. |
| Standard indirect scroll gesture | Scroll the visible gallery or detail container from rest; show content movement. No custom gesture or raised-arm requirement. |
| Detail entry | Show title, image, text and an always available labeled “Back to Gallery” control. Reading and controls stay on a coherent window plane. |
| Activate “Back to Gallery” | Restore the saved viewport and selected object marker. Do not force the person's gaze or synthesize hover. |
| Connected keyboard/controller navigation | Use actual platform component focus, distinct from gaze hover; activation opens detail. Restore that input mode's focus to the returned card. |
| Supported assistive activation | Invoke the same card and Back actions and preserve the same return context. System Dwell Control may deliberately activate a control; app-created gaze dwell opening is forbidden. |

Use standard hover responses with stable artwork and target bounds. Treat each image and title as one target, not competing targets. Start regular controls at the local guide's visionOS default of 60 × 60 pt; retain at least 16 pt gaps and at least 60 pt center spacing between regular controls. Reflow rather than shrinking into crowded targets. No numeric universal field-of-view angle or fixed window distance is assumed. Sustained reading normally belongs at least 1 m away per the Eyes guide; use system placement/scaling and validate actual comfort rather than enforcing an unmeasured distance. [Eyes, Making items easy to see / Custom hover effects](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see), [Spatial layout, Best practices](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Best-practices).

Direct touch can supplement brief nearby interactions, but every essential action must work indirectly from rest. No required reach, two-hand pose, hand tracking permission, walking, or repeated head turns. Keep palm/wrist system gestures available. Provide standard actionable controls usable through VoiceOver, Switch Control and head/hand Pointer Control; do not require speech or gaze precision. Actual availability and behavior must be verified in the chosen SDK and device configuration. [Gestures, visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS), [Accessibility, visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS).

## Cross-platform accessibility decisions

Each card has one actionable semantic element named by the object's title, with an opening-details action; meaningful imagery has a content description without duplicating the title unnecessarily. Detail exposes a heading, image description, reading content, and a named Back action. The last-opened state is distinguishable without color. No essential information depends on sound. All 20 objects and the return action must remain available through assistive navigation.

Use platform text styles and preserve content/actions with at least 200% text enlargement through reflow and scrolling. TV controls start from the local guide's 66 × 66 pt default rather than its smaller minimum. Avoid decorative peripheral motion; Reduce Motion must retain location and state cues while reducing animated scaling, depth and transitions. Contrast, actual bounds and enlarged layouts require measurement of the implementation. [Accessibility, Vision / Mobility / Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

## Acceptance checks and current status

**Passed — specification inspection only:** Both contracts preserve all 20 object identities and detail/return routes; activation is distinct from targeting; TV has a complete directional route; TV return explicitly restores focus and viewport; Vision Pro has a resting indirect path and no app gaze-driven state changes. This confirms written requirements, not runtime behavior.

**Failed — supplied concept, as described in interface.md:** Looking automatically opens detail; gaze is equated with remote/keyboard focus; TV requires pinpoint cursor motion; returning loses focus; all Vision Pro actions require raised arms. The replacement contracts address each described issue. These are brief-level findings, not observed device failures.

**Not executed — implementation acceptance scenarios:**

| Check | Pass condition |
|---|---|
| TV traversal | From first entry reach and activate every one of the 20 cards using only Siri Remote; reverse direction and exit every region; focus enlargement never clips important content. |
| TV targeting versus activation | Navigate across several cards and rest/move the remote; detail opens only on deliberate Select. The last-opened marker survives focus changes. |
| TV return | Open object 18 after scrolling, return by physical Back and separately by visible Back; object 18 is visible and focused with the prior viewport restored. Root Back reaches Home. |
| Data changes | Remove the return object while detail is open; return follows the documented surviving-neighbor fallback. Remove all objects; a usable empty gallery appears. Remove a currently focused TV card during directional use; focus remains visible nearby. |
| Vision hover privacy | Look across all cards without activation; no route or stored state changes. Review implementation to ensure there is no pre-tap gaze tracking or app dwell timer. |
| Vision activation and return | With resting hands, scroll to object 18, activate it, read details and activate Back; the original viewport and marker return without forced gaze/hover. |
| Vision alternatives | Repeat browse/open/return using connected input and supported VoiceOver, Switch Control and Pointer Control paths; all actions remain reachable, named and activatable. Verify system Dwell Control independently. |
| Layout and comfort | Measure target gaps/bounds, text reflow and contrast; inspect TV across-room legibility and Vision Pro hover separation, reading depth and stationary use across seated/standing postures. No repeated reach or broad turns needed. |
| Preferences and failure | Repeat at enlarged text, Reduce Motion and Increase Contrast; content and return survive. Simulate failed detail loading; Retry and Back remain operable. |

## Evidence still missing

No source implementation, screenshots, object assets, semantic tree, saved-state implementation, or measured target/contrast geometry was supplied. It remains unknown whether “objects” are 2D or genuinely spatial, how long details are, and how real titles affect layout. The four-column layouts and marker wording are provisional product choices.

No SDK compilation, simulator, GUI, television, Siri Remote, worn Vision Pro, eye/hand tracking, comfort, or accessibility execution occurred. Required next evidence is an implemented prototype plus supported SDK validation, actual TV/remote traversal and viewing-distance checks, and worn Vision Pro testing across postures and supported assistive methods. These checks must establish native focus restoration, hover responsiveness, alternative-input order, tracking from rest and physical comfort. Local snapshot guidance does not establish current API availability. No source conflict was identified in the loaded guides; this is not a review of the entire corpus.
