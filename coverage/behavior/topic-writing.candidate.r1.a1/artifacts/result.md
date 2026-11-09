# Copy revision result

Patched `interface.md` in place with exact replacement strings, trigger conditions, action outcomes, payment states, assumptions, and acceptance checks.

## Decisions and source support

- **Review Parking**, **Cancel**, and **Pay {total}** distinguish review, abandonment, and purchase. Short action-specific labels and semantic roles follow [Buttons — Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons). The selected flow is a product design assumption.
- Field-specific correction replaces blame; sign-in recovery replaces technical jargon. Routine correction stays inline and retains input. These choices follow [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).
- The permission explanation names location and nearby-zone lookup. Request timing and purpose wording follow [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). The data-purpose/access matrix is: location → nearby-zone lookup → minimum task-scoped access; manual zone entry → no location permission. No background access is specified. Transfer and retention are unknown, so no storage promises are made.
- In-button waiting feedback follows [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). Retained selections and payment reconciliation are product decisions that keep copy accurate, not claims of specific Apple requirements.

## Worked before/after

Before: **You entered bad data** identifies neither the field nor a remedy; **Execute operation** hides the next step; both payment and cancellation say **OK**.

After: a verified unknown zone shows **Zone not found. Check the number on the parking sign and try again.** beside **Zone Number**, preserving the value. After correction, **Review Parking** opens details and total. For an illustrative $4.50 total, **Pay $4.50** submits that purchase; **Cancel** returns to setup without payment. The amount is an example, not a fixed price. A lookup outage instead receives **Couldn’t check the zone. Try again.**

## Acceptance results

Passed by static inspection of the revised specification:

- All six original problems have explicit replacements and triggering contexts.
- Actions identify distinct outcomes; the proposed flow contains no generic OK button.
- Permission copy states data and benefit, with manual entry after denial.
- Correction and expiry messages offer remedies without blame or unexplained codes.
- Review, cancellation, pending, confirmed, declined, and uncertain payment outcomes are distinguished. Sign-in never silently retries payment.
- Terminology and capitalization are consistent; runtime values are identified.

Failed static checks: none found. This does not establish passing app behavior.

Not executed: iPhone rendering, enlarged text and localization fit, VoiceOver semantics/order, button geometry and activation, system permission prompts and denial, SDK compilation, backend lookup, sign-in recovery, transaction reconciliation, or parking activation. The execution checks in `interface.md` are requirements, not completed tests.

## Evidence limits and audit

Explicitly read the installed apple-hig root `SKILL.md`, searched its topic index, read the Foundations and Menus and actions family files, then read the Writing, Privacy, and Buttons topic procedures before their corresponding local source guides. Each file was read in a separate shell command. Paths were resolved within `.agents/skills/apple-hig/`. Official links above identify source articles; no web browsing was performed.

The supplied interface was one paragraph, without screens, implementation, permission category, field identity, or code definition. The chosen flow, location permission, zone error, and authentication expiry are explicit assumptions requiring product verification. In particular, 0x17 must be mapped to its verified cause before release. Payment-provider and data-handling details remain unknown. Local guidance is a dated, derived snapshot; no current online verification, device, GUI, SDK, accessibility execution, or security certification is claimed.
