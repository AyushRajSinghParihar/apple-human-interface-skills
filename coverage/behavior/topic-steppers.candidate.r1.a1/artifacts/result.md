# Revised iPhone ticket-cart interaction specification

## Decisions

The quantity control edits a draft cart line; it never purchases, charges, or reserves tickets. Use a paired minus/plus stepper with an unmistakable adjacent value, consistent with [Steppers — Best practices](https://developer.apple.com/design/human-interface-guidelines/steppers#Best-practices). Bounds, checkout separation, and inventory recovery below are product decisions, not claims that Apple prescribes ticket-commerce rules.

- Domain: whole tickets, step 1, minimum 0, maximum M supplied by authoritative availability and any per-order limit (use the smaller). No negative, fractional, overflowing, or wrapping quantities. Zero means no tickets selected; retain the line so the person can increase it again.
- Show the ticket/event name, `Quantity: 2 tickets`, and `Maximum available for this order: 6` beside the control. Keep the actual value visible after every change. At zero show `No tickets selected`; at M show `Maximum reached`. At M = 0 show `Sold out`.
- Minus subtracts one; plus adds one. Disable minus at zero and plus at M. Keep both visible and expose their disabled state. One activation changes one ticket; holding does not repeat or accelerate. Rapid taps are serialized against the latest draft state.
- Availability unknown: show `Checking availability`, disable both segments and checkout, and preserve any prior draft quantity as unvalidated. Failure shows persistent `Availability unavailable` with a `Retry` action; never invent M or assume unlimited stock.
- Quantity changes immediately update the draft value and displayed subtotal together. They cause no payment request. Show the subtotal from the same quantity and pricing revision; if pricing is unavailable, show that status and block checkout rather than showing an old total as current.
- `Continue to checkout` is the prominent cart action, enabled only for a positive, validated quantity and current price. It opens review/payment; it does not itself charge. Return/default activation must not invoke a purchase from this screen. Final purchase belongs to a separately labeled payment action after review. Detailed payment design is outside this specification.

Assumption: this is a small ticket range, provisionally at most 10 per order; that number is an explicit design assumption, not an inventory fact. Confirm the real range before implementation. If materially larger ranges are permitted, extend this specification with direct numeric entry and its validation before release; repeated tapping across a large range is unsuitable per the stepper guidance.

## Presentation and access contract

Use the existing framework's suitable standard control if available, otherwise implement the same contract without requiring an Apple SDK. Keep familiar minus/plus symbols; a 16 pt glyph may remain if legible. Give each segment a distinct, nonoverlapping activation region of at least 44 × 44 pt and clear separation from the value and checkout. Provide visible pressed feedback and perceivable disabled styling. These choices follow [Buttons — Best practices and Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

The accessibility guide lists a 44 × 44 pt iOS default and a smaller 28 × 28 pt minimum; this design chooses 44 × 44 pt or larger, following the button guidance rather than treating the smaller figure as a target. The brief supplies glyph size only; existing hit regions are unknown.

Expose minus as a button named `Decrease tickets for [ticket name]`, plus as `Increase tickets for [ticket name]`; expose enabled/disabled states and the associated quantity and range as readable information. Do not use `Button` as the accessible name or depend on glyph recognition. After activation, make the updated quantity available to assistive input without moving focus to checkout. Reading order must keep the ticket identity, quantity, limit, and controls associated; avoid duplicate interactive representations of the same stepper.

Keep essential text and actions usable at at least 200% text enlargement: allow labels/status to wrap and place controls on another row when needed. Never communicate boundaries or failures by color or sound alone. Names, states, enlargement, and alternative input requirements follow [Accessibility — Vision, Mobility, and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Exact layout, contrast, focus behavior, and assistive announcements require implementation verification.

## State and transition contract

```text
state = {quantity, maximum?, availabilityRevision?, priceRevision?, status}
status = checking | ready | unavailable

on adjust(delta):                 // delta is exactly -1 or +1
    atomically:
        if status != ready: return
        candidate = quantity + delta  // checked integer arithmetic
        if overflow or candidate < 0 or candidate > maximum: return
        quantity = candidate
        render quantity, bound states, and matching subtotal together
    // no purchase/payment/reservation side effect

on authoritativeAvailability(M, revision):
    require M is a nonnegative integer and revision is newer
    atomically:
        maximum = M
        if quantity > M:
            old = quantity
            quantity = M
            show persistent "Availability changed: quantity reduced from old to M."
        status = ready
        render quantity, maximum, matching subtotal, and enabled states
    // expose correction as readable status; never auto-purchase

on refreshFailure:
    status = unavailable
    preserve draft; mark it unvalidated; block adjustment and checkout

on continueToCheckout:
    if status != ready or quantity == 0 or price is not current: return
    submit immutable draft snapshot for server validation, not payment
    prevent duplicate submission while validation is pending
    show activity indication inside the activating button
    if valid: open review with that validated snapshot
    if inventory/price changed: return to cart with revised facts and
        persistent explanation; require another explicit Continue
    if network failure: retain draft, show error, reenable retry when possible
```

The server must also reject out-of-range quantities and revalidate stock before final purchase; client bounds cannot guarantee inventory. Ignore stale availability responses. Checkout validation must use the submitted snapshot and reject a mismatched revision rather than silently buying a different amount. Pending button feedback follows [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS); inventory/version policies are application decisions.

## Worked before/after

**Before, as reported in interface.md:** minus can make quantity negative; tapping adjustment immediately purchases another ticket. Quantity and maximum are absent, and both accessibility names say `Button`. Only 16 pt glyph dimensions are supplied.

**After, illustrative data:** M = 3, draft quantity = 1. Display `Quantity: 1 ticket` and `Maximum available for this order: 3`. Minus changes it to 0 and disables minus; another minus does nothing. Three plus activations produce 1, 2, 3, then disable plus; another plus does nothing. All these actions make zero purchases. Accessible names distinguish increase from decrease and identify the ticket.

`Continue to checkout` from 3 validates and opens review. If availability instead falls to 2, show `Availability changed: quantity reduced from 3 to 2`, update the subtotal, and require another Continue. No ticket is purchased by the correction or validation. If availability falls to zero, show sold out and disable checkout.

## Acceptance checks and evidence status

**Passed — document inspection only:** read the supplied interface.md and installed root, relevant family routes, topic procedures, and source guides. This specification defines the affected value, unit, increment, bounds, display binding, commit boundary, control names, target requirements, and recovery behavior. The worked trace is internally consistent with 0 ≤ quantity ≤ M; it is a manual specification walkthrough, not executed logic.

**Failed — current behavior reported by the brief:** negative quantities, purchase on adjustment, missing quantity/maximum display, and generic accessibility names conflict with the revised contract. No failure is established for hit-region geometry merely from 16 pt glyphs.

**Not executed — required implementation acceptance:**

| Check | Expected result |
| --- | --- |
| Start at 0; activate minus, including stale/programmatic input | Remains 0; no side effects; minus disabled |
| Start at M; activate plus; repeat rapidly | Remains M; no wrap or overflow; plus disabled |
| Exercise M = 0 and M = 1 | Sold-out and single-ticket bounds work; no negative values |
| Alternate plus/minus and rapid taps | Correct line changes by exactly 1 per accepted activation; display, subtotal, and stored value agree |
| Instrument all adjustment paths, including assistive activation | Zero purchase, payment, or reservation requests |
| Refresh unknown/failed inventory, stale responses, and a falling maximum | Controls gate appropriately; stale responses ignored; corrections explained and never silently purchased |
| Continue repeatedly during pending validation; simulate failure or changed inventory/price | One active validation; visible wait/error; preserved draft; review only for matching validated snapshot |
| Measure actual layout and press behavior on iPhone | Each target ≥44 × 44 pt, no overlapping hit regions, clear separation, visible press feedback |
| Enlarge text to ≥200%; inspect light/dark and Increase Contrast | Quantity, limit, statuses, and all actions remain readable and reachable; measure actual contrast |
| VoiceOver, Voice Control, Switch Control, Full Keyboard Access, AssistiveTouch | Distinct names, value/range and disabled states available; logical navigation, stable focus, complete adjustment-to-checkout path |
| Test actual supported maximum | Every permitted value is practical to reach; revisit the control if the small-range assumption fails |

## Evidence limits

Only interface.md and local installed guidance were used; official links identify the local guides' sources and were not opened. The references identify a 2026-10-25 snapshot/retrieval date; this is not an independent freshness or source-review claim. Routes read: Selection and input → Steppers; Menus and actions → Buttons; Foundations → Accessibility, with the complete topic index searched before finalizing.

No implementation, screenshot, SDK, running app, device, GUI, accessibility tooling, contrast measurement, or runtime test was supplied or exercised. Actual target geometry, rendering, pricing, inventory API behavior, real maximum, and payment flow remain unverified. This artifact is a proposed interaction contract, not evidence that the existing cart now behaves this way.
