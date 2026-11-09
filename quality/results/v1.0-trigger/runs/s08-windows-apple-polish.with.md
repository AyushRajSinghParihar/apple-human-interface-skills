The main issue is delayed access to value: five intro pages ask people to learn the app before using it, and the hidden Skip makes an optional tour feel mandatory.

Apple’s [onboarding guidance](https://developer.apple.com/design/human-interface-guidelines/onboarding) favors brief, optional learning, safe interaction, and contextual tips. Apply those principles while keeping familiar Windows controls and window behavior.

| Finding | Recommended correction |
|---|---|
| Five pages before sign-in delay both new and returning users. | Replace them with a brief welcome screen offering a direct path to sign-in. Teach features during the first useful task. |
| Skip is hidden in a corner. | Put a clearly labeled **Skip tour** beside the tour’s navigation controls, visible on every page. It can have secondary emphasis without being hard to find. |
| Full-screen presentation gives introductory content excessive weight. | Use the normal, resizable app window. This is a Windows design recommendation, rather than an Apple requirement. |

My suggested flow is: **Welcome → Sign in, if required → First useful task with optional contextual tips.** Offer the longer tour through Help, remember completion or skipping across launches, and avoid showing it again to returning users.

For buttons, use native Windows styling with clear labels and a distinct primary action, consistent with Apple’s [button principles](https://developer.apple.com/design/human-interface-guidelines/buttons).

Based on your description, the flow needs revision. Skip persistence, keyboard access, focus visibility, and screen-reader behavior remain unverified.