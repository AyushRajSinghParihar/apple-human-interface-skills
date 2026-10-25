---
name: apple-hig-app-clips
description: Use when designing or reviewing an App Clip finite task, invocation context, full-app continuation, card, notifications, or physical App Clip Code placement.
---

# Finish the invoked task without requiring installation

Read [App Clips](../../references/app-clips.md). Inspect the finite task/demo, invocation URL/context, startup dependencies, identity/payment needs, and requested design/review/adaptation. Preserve the existing native implementation approach where appropriate; a web-only experience should use a website link. The guide supports iOS/iPadOS and excludes the other platforms.

Define the complete smallest task, then remove unrelated tabs, settings, ads, and installation gates. Launch into the invoked business/location/content context with required assets available and a short flow. Prefer guest use, suitable Apple Pay checkout, or minimal Sign in with Apple when identity is indispensable. Do not rely on background operations or durable local Clip storage; the system may remove all local data. When the full app replaces the Clip, preserve the focused destination and avoid repeat login or extra steps.

Promote installation only after completion or a natural demo pause, using appropriate system overlay behavior. Request extended notifications only for a genuine longer task; ordinary limited notifications must respond to task action, never promotion. For multiple businesses/locations, verify launch context and preserve separate recent contexts with business branding leading provider branding.

If cards/codes are in scope, choose task-explaining opaque card art and correct action/length limits from the guide. Use generated codes unchanged, selecting reachable NFC or distant/digital scan-only placement. Check size, clear space, distance, surface rigidity, print calibration, and invocation URL/version against the guide's production tables; never redraw the code or print it directly on crumpling material.

**Before → decision → after:** A bike-rental Clip scans to a generic provider home, asks for installation, and loses the active rental when local data clears. Decision: invocation should finish the chosen rental without installation or fragile persistence. After, the code opens that station's rental flow, guest payment completes it, required rental recovery is handled securely beyond temporary storage, and installation is offered after success.

Deliver the invocation-to-completion flow and any card/code production specification. Fail if installation is necessary, a code opens the wrong location, promotion interrupts completion, or data loss makes recovery impossible. Actual scan/print/startup/notification tests must be reported separately from design inspection.

Use [Apple Pay](../apple-hig-apple-pay/SKILL.md) or [Sign in with Apple](../apple-hig-sign-in-with-apple/SKILL.md) for chosen checkout/identity, and [NFC](../apple-hig-nfc/SKILL.md) for tag interaction.
