---
name: apple-hig-homekit
description: Use when designing or reviewing smart-home setup, accessory naming, rooms/scenes/automations, multiple homes, external configuration changes, or Apple Home integration.
---

# Preserve the shared home's authoritative configuration

Read [HomeKit](../../references/homekit.md). Inspect accessory functions, existing Home configuration, setup/account flow, external updates, and requested design/review/adaptation. Preserve the existing stack and check actual API availability for the target platform rather than inferring it from this overview.

Map the UI to the home model: separate home roots, rooms, optional zones, physical accessories, controllable functions, actions, scenes, and automations. Use consumer function/attribute names such as light/brightness instead of services/characteristics jargon. Keep location details findable and do not ask people to recreate configurations already established in Apple Home.

Start pairing/naming/network/room/category setup through the system flow. Basic functionality must work before optional cloud accounts or extra proprietary features. Suggest understandable names, validate the source's supported character/boundary rules, and avoid duplicating room names in function names. Teach Siri with the person's actual configured names; reserve Shortcuts for unique functionality HomeKit cannot already perform.

Reflect external Home changes automatically. Obtain permission or explicit intent before writing changes and never silently overwrite the database. If conflict choice is needed, show both alternatives clearly. For camera accessories, keep the image clear of unrelated overlays and expose microphone controls only with bidirectional audio support. Preserve official setup/compatibility artwork and consumer terminology.

**Before → decision → after:** A light app demands a cloud account before pairing, calls every device “Brand X Service,” and restores its cached room name over changes made in Apple Home. Decision: shared home configuration leads. After, system setup works first, functions use meaningful names/room assignments, optional cloud features follow, and external room changes update the app rather than being overwritten.

Deliver a model/setup/synchronization contract or corrected implementation. Fail if a second home merges into the first, setup is gated by optional identity, Siri names are ambiguous, or external settings are silently lost. Actual pairing, permission, device-state, and multi-app synchronization require supported hardware/runtime tests.

Use [Siri](../apple-hig-siri/SKILL.md) for unique shortcut interactions and [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for Home-data purpose strings.
