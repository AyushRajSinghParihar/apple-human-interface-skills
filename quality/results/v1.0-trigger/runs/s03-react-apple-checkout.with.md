Based on your description, all three choices need revision. Apple’s guidance can inform your React web app while you retain standard HTML controls.

| Finding | Why it matters | Recommended correction |
|---|---|---|
| Placeholder text serves as the label | It disappears during entry, making fields harder to identify and review. | Add persistent visible labels, such as **Email address**, associated through `<label htmlFor>`. Use placeholders only for optional examples. See [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields). |
| Primary button says **Submit** | It doesn’t explain whether the next step reviews the order or commits the purchase. | Name the actual outcome: **Review Order** for another review step, or **Place Order** when it commits the purchase. See [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). |
| Errors appear only as red borders | Color alone can be missed, and a border gives no explanation or remedy. | Keep the border as reinforcement and add nearby text, such as “Enter an email address in the format name@example.com.” See [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [Writing](https://developer.apple.com/design/human-interface-guidelines/writing). |

For the web implementation, connect each error with `aria-describedby`, set `aria-invalid="true"` on invalid fields, and ensure newly displayed errors are discoverable through focus management or an appropriate announcement.

These three design checks fail based on the described behavior. Contrast, keyboard navigation, and screen-reader behavior remain untested; grey text alone doesn’t establish a contrast failure.