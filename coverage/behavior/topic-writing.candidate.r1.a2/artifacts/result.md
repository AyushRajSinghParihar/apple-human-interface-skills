# Copy revision result

Edited `interface.md` in place from a one-line brief into exact replacement strings, contextual placement, action outcomes, a permission contract, checkout states, and acceptance requirements. All six supplied copy occurrences are addressed, including separate cancellation and payment labels.

## Decisions and support

- Replace vague operations with specific verbs and errors with neutral remedies; distinguish sign-in expiry from paid parking expiry. This applies [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). Exact parking vocabulary and assumed causes are product decisions, explicitly marked in the specification.
- Replace identical OK labels with **Cancel** and **Pay {total}**. Separate review from charging and specify pending outcomes. Clear verb phrases, roles, and iOS activity indication follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). Full-price disclosure and duplicate-payment handling are proposed product safeguards, not quoted HIG requirements.
- Name location and nearby parking in the purpose sentence; request access at the moment of use and prefer one-time access. This applies [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) and [Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button). Location is an assumption because the original resource is unspecified.
- Keep ordinary corrections and recovery in context; define meaningful actions and cancellation if an existing expiry alert remains, following [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts). No alert implementation was supplied.

## Worked before/after

Before: cancellation and payment both say **OK**, concealing which commits a charge.

After, for an illustrative total of $6.50: review displays vehicle, location, duration, end time, and total with **Cancel** and **Pay $6.50**. Cancel returns to setup with selections retained and no submission. Pay submits the reviewed amount and shows **Processing Payment…**. Only confirmed payment and activation show **Parking Started**. Unknown outcomes show **Checking Payment** with a status check instead of another charge. The price is an example, not supplied product data.

## Acceptance checks

Passed by static inspection of the revised specification:

- All original copy occurrences have contextual replacements and defined outcomes.
- Review and payment are distinct; the payment label contains a defined full-total token.
- Permission names resource and purpose and defines scope and denial behavior.
- Validation gives a nonblaming remedy for a specified cause without invented format restrictions.
- Expiry names sign-in and offers recovery without implying paid parking ended.
- Cancellation retains selections; pending and unresolved payments have distinct transitions.

Failed: no static specification checks identified as failing. This does not establish app behavior.

Not executed: actual handlers, payment/authentication services, permission prompts, denial handling, duplicate-charge prevention, native alert/default-key cancellation, SDK compilation, device rendering, currency expansion, localization, larger-text layout, hit regions, VoiceOver names/order/announcements, or other accessibility execution. The specification requires implementation checks; this report does not claim they passed.

## Evidence limits and audit

The only supplied product evidence was the original one-line `interface.md`. No code, screenshots, service rules, protected-resource category, registration rules, or expiry semantics were supplied. Checkout, location, empty-registration, and authentication meanings are explicit proposed assumptions requiring confirmation before release. Storage, transfers, retention, and privacy disclosures remain unknown. No Apple Pay support is claimed.

Read the installed root `.agents/skills/apple-hig/SKILL.md`, searched `references/topic-index.md`, then read the Foundations, Menus and actions, and Presentation family procedures. Read their Writing, Privacy, Buttons, and Alerts topic procedures before their respective supporting guides. Paths were resolved within the installed `.agents/skills/apple-hig/` package. Each instruction/source read used a separate command reading one file.

Official links identify supporting articles from local guidance; they were not opened. Work used only local files and the installed snapshot dated 2026-10-25. No web browsing, device, SDK, GUI, or accessibility execution occurred. Local guides are application guidance derived from Apple sources; their presence does not establish independent source review or current SDK behavior.
