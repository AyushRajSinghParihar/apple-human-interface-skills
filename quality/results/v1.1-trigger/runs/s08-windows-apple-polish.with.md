Your onboarding puts too much distance between opening the app and doing something useful. Apple-like polish here means faster access, clear choices, and learning in context.

1. **High priority: shorten the five-page introduction.** It delays sign-in and asks people to remember features before using them. Apple’s [onboarding guidance](https://developer.apple.com/design/human-interface-guidelines/onboarding) favors brief, optional learning through safe interaction. I’d replace the sequence with one concise welcome screen, then teach features during the first relevant task. Five pages isn’t a prohibited number; the concern is unnecessary delay.

2. **High priority: make skipping obvious.** A hidden corner button makes an optional tour feel compulsory. Place a clearly labeled **Skip intro** action alongside the tour’s navigation, with readable contrast and visible keyboard focus. It can have secondary emphasis while remaining easy to find. Apple recommends skippable tutorials and [clear button hierarchy](https://developer.apple.com/design/human-interface-guidelines/buttons).

3. **Verify skip persistence and later access.** Skipping or completing the introduction should prevent it from appearing on subsequent launches. Provide **Help → Take a tour** so people can return voluntarily. Both follow Apple’s onboarding guidance; your description doesn’t establish whether they already work.

My suggested flow is:

**Welcome with one clear benefit → Sign in → First useful task with contextual tips**

If an account isn’t essential for that first task, consider letting people try it before sign-in.

For Windows, keep the normal resizable window, Windows caption controls, system typography, and native keyboard behavior. Apply Apple’s clarity while preserving [Windows conventions](https://learn.microsoft.com/en-us/windows/apps/design/basics/titlebar-design).

This is a flow review based on your description. Keyboard access, Narrator behavior, text scaling, and skip persistence still need verification.