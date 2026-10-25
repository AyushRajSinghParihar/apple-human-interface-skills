---
name: apple-hig-digit-entry-views
description: Use when creating, reviewing, or adapting tvOS fullscreen numeric sequence entry such as a PIN.
---

# Explain and protect numeric entry

Read [the digit-entry guide](../../references/digit-entry-views.md). This procedure is application advice for the tvOS-specific component, not a universal OTP-field specification.

Inspect sequence purpose/length, sensitivity, prompt, validation, platform/input, and create/review/adapt request. Distinguish a numeric sequence from a numeric quantity: leading zeroes and exact length may matter. Do not infer security from a screenshot showing obscured characters; inspect secure-entry configuration when available.

Use the fullscreen numeric-entry presentation for the intended TV task, with a clear title and prompt explaining why digits are needed. Mask sensitive sequences using secure fields. Specify completion, correction, cancellation, and an understandable rejected-entry path without exposing the secret. These lifecycle choices are application advice; the source does not define an authentication protocol or retry policy. For other platforms choose a supported secure-entry approach instead of claiming this component's availability.

Implement the entry/validation boundary or deliver prompt, field, sequence, and result-state specifications; review specific exposure or input-loss defects. Keep authorization and actual authentication outside a cosmetic redesign unless included in scope.

**Worked transformation:** Before: a TV parental PIN screen asks only `Number`, displays the full PIN, and converts `0042` into `42`. Decision: purpose, secrecy, and sequence identity are all lost. After: explain the parental approval task, mask secure entry, and preserve the exact four-digit sequence through validation.

Deliver the artifact and entry/correct/reject/cancel contract. Verify leading zeroes, correction, completion length, rejected input, and cancellation. Fail for sensitive exposure, altered sequence, unexplained purpose, or an exit that commits incomplete input. Native remote/keyboard and authentication behavior need separate execution evidence.

Load [virtual-keyboards](../apple-hig-virtual-keyboards/SKILL.md) for TV input variants or [privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for handling sensitive information.
