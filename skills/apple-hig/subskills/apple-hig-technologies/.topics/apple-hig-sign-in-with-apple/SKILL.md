---
name: apple-hig-sign-in-with-apple
description: Use when designing or reviewing Sign in with Apple timing, existing-account linking, private relay email, required versus optional data, or authentication button treatment.
---

# Authenticate without recreating unnecessary account work

Read [Sign in with Apple](../../references/sign-in-with-apple.md). Inspect why an account is needed, existing customers, other sign-in methods, extra fields, and requested design/review/adaptation. Preserve the existing authentication stack. Use current API/security documentation for implementation details beyond this design guide.

Defer sign-in until its value is clear. If a separate service account is necessary, explain that account before offering methods. Provide existing-account linking rather than making a duplicate identity; commerce should allow guest purchase and optional registration afterward without reasking already supplied Apple Pay fields. After success, welcome the person into useful work and identify the method in account settings.

Separate required fields from optional beneficial information. Never demand a new password for this method. Respect the chosen relay address without requesting the underlying address, and show usable relay/support identifiers. Ask optional information after useful engagement and allow decline without blocking features/account use.

Prefer system-provided buttons, using one suitable approved title consistently and prominence at least equal to other methods without scrolling. Select a contrasting supported style and corner treatment; Watch has its own shorter title/dark-gray behavior. If a custom permitted design is explicitly required, use supplied padded logo artwork and the guide's exact size/proportion/title/color constraints instead of redrawing Apple identity.

**Before → decision → after:** A reading app hides the Apple option below other methods, requests a new password, and rejects relay email for a “real address.” Decision: this method already authenticates and the relay is the person's choice. After, an equally prominent system button opens the supported flow, no extra password is required, relay identity works for support, and optional profile fields follow the first useful reading task.

Deliver a corrected entry/linking/data/button flow or implementation. Fail if relay users cannot proceed, unnecessary credentials are required, existing accounts cannot link coherently, or the option is visually disadvantaged. Static UI review cannot verify token validation, account linking security, or actual biometric/relay behavior; report those runtime checks separately.

Use [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for data purpose and [Apple Pay](../apple-hig-apple-pay/SKILL.md) for guest commerce continuity.
