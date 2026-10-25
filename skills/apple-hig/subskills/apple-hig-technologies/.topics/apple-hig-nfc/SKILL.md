---
name: apple-hig-nfc
description: Use when designing or reviewing physical-object NFC scanning, scan-sheet instructions, repeated scans, background-read entry, or foreground fallback.
---

# Explain the object and the result of holding nearby

Read [NFC](../../references/nfc.md). Inspect the physical object, read result, supported hardware, scan session, and requested design/review/adaptation. Preserve the existing stack. The guide concerns supported iOS hardware, with no additional iPadOS rule; verify actual device/API support rather than assuming every iPad can read tags. Other platforms are excluded.

Choose in-app reading for a deliberate one-or-many-object workflow. Present the system scanning sheet with short complete sentence-case instructions naming the real object and saying scan or hold near. Avoid tag/Core NFC/near-field communication jargon and do not imply physical contact is required. Update the instruction after an initial scan when the next object/action changes.

Use background reading only as an additional entrypoint on compatible devices. A lit display can detect suitable objects and show a notification opening the matching app/context, but scanning is unavailable in the source's restricted states, including active NFC sessions, Wallet/Apple Pay, camera use, Airplane Mode, or the post-restart locked state. Keep a complete in-app route for devices or moments without background support. Define the destination/action from the read data without claiming background reading always occurs.

**Worked transformation:** Before, a library app says “Touch NFC tag,” waits for background detection on all devices, and opens a generic home screen. Decision: the person needs a clear nearby-object action and reliable fallback. After, “Hold iPhone near the book label” starts the foreground sheet, subsequent text guides the next book when appropriate, and a supported background notification opens the scanned book's details.

Deliver scan instructions, first/subsequent result states, invocation destination, and fallback flow or implementation. Fail if copy implies contact, the task depends solely on background reading, or scanned context is lost. Real tag compatibility, radio conditions, sheet behavior, and background-state restrictions require hardware tests; simulated data verifies only app routing.

Use [App Clips](../apple-hig-app-clips/SKILL.md) for Clip Code invocation and [ID Verifier](../apple-hig-id-verifier/SKILL.md) for mobile-ID verification rather than ordinary object scanning.
