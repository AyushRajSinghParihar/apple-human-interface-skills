# Revised control specification

Patched `interface.md` in place, replacing the original single paragraph with a platform/input matrix, complete action mappings, touch geometry and cancellation rules, controller detection and glyph resolution, remapping, pause/recovery states, and Apple TV focus routes.

## Decisions

- iPhone has a complete touch route plus optional physical controllers. Independent movement and weapon aim/fire use two virtual sticks; the second controls weapon direction rather than camera motion.
- Apple TV gameplay requires a compatible dual-stick controller, with store disclosure and graceful absence handling. Siri Remote remains sufficient for menus and recovery. This applies the locally documented tvOS exception rather than pretending a remote supplies two independent sticks. See [Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Physical-controllers).
- Prompts use effective bindings and active hardware glyphs, paired with action names. Conventional menu semantics remain separate from customizable gameplay bindings.
- Input loss freezes the match and clears held actions. Reconnection requires explicit Resume and neutral input. iPhone can switch to touch; Apple TV can reconnect or leave safely.
- Touch controls use conservative 44 pt button targets, larger stick regions and safe-area constraints. The local games article has a smaller table minimum alongside 44 pt prose; the patch explicitly resolves that tension. The 120 pt regions, 12 pt separation, dead zones and recovery state machine are project decisions requiring validation, not Apple mandates. See [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Look-stunning-on-every-display).
- Remapping and optional aiming assistance offer different motor accommodations; no accessibility conformance is inferred. See [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

## Worked before/after

Before: a player starts with a symbol-labeled controller, sees “A” everywhere, then disconnects it while moving and firing. The match continues to a loss; on iPhone there is no touch fallback.

After: setup assigns that controller's detected profile. Prompts show the effective input glyph beside its action. At disconnection, simulation, health, timers and score freeze and held movement/fire clear. On iPhone the player chooses Use touch controls, sees Move and Aim / Fire, then selects Resume; no stale fire is replayed. On Apple TV the Siri Remote reaches connection instructions and Retry. A compatible replacement is assigned, prompts refresh, axes return to neutral, and the player explicitly resumes the frozen match.

## Acceptance checks and status

**Passed — static specification review:** Both platform input routes cover move, aim/fire, pause, menu activation and return. The revised text explicitly covers missing/incompatible controllers, multiple-device assignment, profile-specific prompts, invalid remaps, reserved system inputs, touch cancellation, orientation changes and disconnect recovery. These are document-level passes only.

**Failed:** No failure was established in the revised document review. The original brief explicitly described absent touch/remapping, incorrect universal labels and disconnect losses; the revision supplies replacement contracts. Their runtime correction is unverified.

**Not executed — implementation acceptance gates:**

| Scenario | Required observable result |
|---|---|
| Fresh iPhone install without controller | Enter practice, move and independently aim/fire, pause and return using touch only |
| Simultaneous touch, crossing regions and cancellation | Each touch retains its assigned stick; release/cancel stops the corresponding action |
| Portrait/landscape, safe areas and enlarged labels | Controls remain separate and reachable; rotation pauses without losing match state; labels remain readable |
| Two controller profiles with different glyphs | Tutorials, menus and remapping show the active profile's effective binding; no universal A label |
| Two connected controllers | Unassigned input cannot hijack play or mix prompt identities |
| Remap, conflict, cancel and restore | Valid Apply persists per profile; conflicts explain rejection; Cancel preserves working bindings |
| Disconnect while moving/firing | No later simulation tick uses held input after loss detection; frozen health/score/timers remain unchanged; no disconnect loss |
| Reconnect with held stick/button | No automatic resume or stale action; Resume requires neutral input |
| iPhone touch fallback / TV controller absence | Touch resumes the same match; TV blocks play but Remote reaches every recovery action |
| Siri Remote and controller menu traversal | Every available action is reachable with visible focus; selection is deliberate; Back and Home follow the state contract |
| Comfort and across-room reading | Touch regions are comfortable on supported iPhones; TV text and focus states are readable at viewing distance |
| Assistive input and assistance mode | Setup/recovery expose meaningful actions and states; assistance permits movement-only play; no essential status relies solely on color/sound |

## Evidence limits and audit route

Only local text was inspected and edited. No web browsing, SDK validation, build, GUI, device/controller trial, contrast measurement, assistive-technology execution or App Store submission was performed. Official links identify the sources named by the installed snapshot; they were not opened or independently checked for current changes. Hardware behavior, physical comfort, haptics, focus-engine execution and accessibility support remain unproven. The supplied brief identifies no engine, controller inventory or networking model; local single-player pausing is an explicit assumption.

Installed root read: `.agents/skills/apple-hig/SKILL.md`. Routes were resolved from that package and consumed one file per shell command: Getting started family → iOS, tvOS and Designing for games topic procedures → their references; Inputs family → Game controls, Remotes, Focus and selection procedures → their references; Gestures procedure → reference; Foundations family → Accessibility procedure → reference. Relevant game/controller/platform rows of `references/topic-index.md` were searched before finalizing the route. Each source guide was read after its owning family and topic procedure. No sibling installation or network source was used.
