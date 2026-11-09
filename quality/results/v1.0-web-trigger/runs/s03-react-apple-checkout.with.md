Based on your description, all three choices need revision. Apple’s principles apply to your React web app; you can keep standard HTML controls.

| Finding | Why it matters | Recommended correction |
|---|---|---|
| Placeholder text serves as the label | It disappears during entry, making fields harder to identify and review. | Add persistent visible labels such as **Email address**, linked with `<label htmlFor>`. Reserve placeholders for optional examples. Grey alone doesn’t establish a contrast failure; measure the actual colors. [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) |
| Primary button says **Submit** | It doesn’t explain the checkout consequence. | Use **Place Order** if it commits the purchase, **Pay $49.00** if it charges that amount, or **Review Order** if another step follows. Match the actual behavior. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) |
| Errors appear only as red borders | Color alone can be missed and gives no correction instructions. | Add persistent inline text beside each affected field, such as **Enter an email address in the format name@example.com**. Keep red as a supplementary cue. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Writing](https://developer.apple.com/design/human-interface-guidelines/writing) |

For the web implementation, associate errors using `aria-describedby`, set `aria-invalid` when appropriate, and guide focus to the first invalid field after failed submission. These are implementation recommendations for applying the principles in React.

The description establishes these three design issues. Contrast, keyboard navigation, and screen-reader error announcements remain untested without the rendered page or code.