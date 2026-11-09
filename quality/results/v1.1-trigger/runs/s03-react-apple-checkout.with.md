Based on your description, I’d prioritize these three fixes:

1. **High: Errors rely on color alone.** Red borders don’t explain the problem and can be missed by people with color vision differences. Add specific inline messages such as “Enter a valid email address.” Keep the border as a secondary cue. This follows Apple’s [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Writing](https://developer.apple.com/design/human-interface-guidelines/writing) guidance.

2. **High: Field labels disappear during entry.** Placeholder-only labels make checkout fields harder to identify once filled. Add persistent visible labels such as “Email address”; reserve placeholders for optional examples. Grey isn’t inherently a defect—contrast needs measurement. See [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields).

3. **Medium: “Submit” hides the outcome.** Use “Place Order” if it commits the purchase, “Pay [total]” if it takes payment, or “Review Order” if another review step follows. Apple recommends clear, action-specific [button labels](https://developer.apple.com/design/human-interface-guidelines/buttons).

For React, implement these with semantic HTML: `<label htmlFor>`, matching input IDs, `aria-invalid` for invalid fields, and `aria-describedby` linking each field to its error message. Those are web implementation recommendations applying the HIG principles.

**Verification:** The described design has these issues; contrast, keyboard behavior, and screen-reader announcements remain untested without the page or code.