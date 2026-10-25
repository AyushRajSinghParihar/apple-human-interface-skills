---
name: apple-hig-wallet
description: Use when designing or reviewing Wallet passes, field/semantic-tag hierarchy, add/view/update lifecycle, order tracking, or contextual Wallet identity verification.
---

# Put the useful credential or order state into the right Wallet model

Read [Wallet](../../references/wallet.md). Inspect whether the task concerns a pass, order, or identity request; identify platform/device, existing data/assets, and design/review/adaptation scope. Preserve the PassKit/order integration and verify current API/service availability. A pass appearing on Watch does not imply every Wallet verification flow works there.

For passes, choose the style by actual purpose and put essential information in fields/semantic tags, not embedded artwork or device-vulnerable layouts. Keep collapsed headers meaningful and fronts uncluttered; back/supplemental detail serves less frequent needs. Use the guide's image specifications and system barcode APIs, preserving essential content through phone/Watch crop differences. Poster/semantic styles need tags plus appropriate older-system fallback fields.

Offer system addition after the relevant purchase/registration, retain Add for absent/removed passes and View in Wallet for existing ones, and stop repeated suggestions after refusal. Keep expiry/relevance/voiding and changing details accurate. Deletion needs permission; interruptive updates are for time-critical changes, not marketing.

For orders, supply data promptly even while pending and maintain actual shipping/pickup fulfillments, final confirmed price, management/support links, and useful receipt data. Use detailed delivery states only with supporting carrier data; avoid duplicate notifications. For identity, request minimum necessary attributes in transaction context with retention intent/duration, supported system controls, and another method when unavailable. In-person reading belongs to ID Verifier.

**Worked transformation:** Before, a concert pass puts the seat number only in a background image, repeats Add prompts after refusal, and sends promotional “changed” alerts. Decision: the credential must remain readable across devices and updates must serve the event. After, seat/time live in appropriate fields/tags, existing passes open through View in Wallet, declined suggestions stop, and alerts are reserved for a meaningful time-critical event change.

Deliver the chosen model's field/lifecycle/update contract and corrected artifact. Fail if essential information vanishes on Watch, order status exceeds known evidence, or identity requests exceed the task. File/schema checks do not prove Wallet rendering, pass delivery, carrier updates, or encrypted identity handling; identify supported-runtime checks.

Use [Apple Pay](../apple-hig-apple-pay/SKILL.md) for payment and [ID Verifier](../apple-hig-id-verifier/SKILL.md) for in-person mobile-ID reading.
