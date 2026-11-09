---
description: Design a household-visible pickup widget and a private delivery Live Activity.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Design a pickup summary widget and a delivery tracker for our iPhone logistics app, including stale and offline states. Some surfaces are shared with the household.

- Surfaces: iPhone Home Screen and Lock Screen, the shared Apple HomeView Modular face, and a watch glance where it makes sense. For the watch, compare a watch-face complication with a delivery Live Activity in the Smart Stack.
- Data: parcel for Sam at 14 Willow Road, gate code 9182. The last server update was 35 minutes ago.
- The current proposal refreshes the widget every second and puts the full address and gate code on the shared face.
- A delivery lasts about 80 minutes.
- The inline Lock Screen accessory draws Accept, Cancel and Details as three separate tap targets.

Give me the design, the decisions, acceptance checks, and what evidence is still missing.
