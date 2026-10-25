# Right to left

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/right-to-left) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Use standard framework layout so RTL languages such as Arabic and Hebrew adapt naturally. Fine-tune direction, localized numbers/currency/math, and custom assets where system behavior is insufficient.

<a id="Text-alignment"></a>
## Text alignment
Mirror short labels and one/two-line blocks with the interface. Align paragraphs of three or more lines according to the paragraph’s own language, which can differ from the surrounding UI. Keep all items in a list consistently aligned, including entries in a different script.

<a id="Numbers-and-characters"></a>
## Numbers and characters
Choose numeral systems according to locale; Arabic can use Western or Eastern forms while Hebrew uses Western Arabic numerals. Specialist math/number apps need locale-specific research. Preserve the digit order within a number, phone number, or card number. Reverse the positions of ordered/progress sequences when the control flips, without reflecting individual digit glyphs.

<a id="Controls"></a>
## Controls
Mirror progress bars, sliders, ratings, and their endpoint labels; mirror Back/Next/Previous when they represent reading-order navigation. Do not mirror a control meaning a literal physical direction or pointing toward a specific onscreen location. Arabic/Hebrew labels beside uppercase Latin text may need approximately 2 pt additional size for optical balance.

<a id="Images"></a>
## Images
Keep photographs, illustrations, and ordinary artwork unchanged; flipping can alter meaning or violate rights. Create a localized version for strongly directional art if necessary. Reverse positions of ordered image collections when their chronological/alphabetic/preference order carries meaning.

<a id="Interface-icons"></a>
## Interface icons
Prefer SF Symbols’ RTL and localized variants. Mirror symbols for reading direction, forward/backward movement, and abstract text alignment. Localize actual text characters used for writing concepts; replace letters with another metaphor when the concept is unrelated to writing. Preserve logos and universal signs such as checkmarks. Usually preserve real-world objects, clocks, and handed tools unless they specifically indicate direction. Evaluate complex custom glyphs component by component: a negation slash can retain orientation, a badge depicting actual UI may need mirroring, and another badge may need repositioning for balanced meaning. Preserve a tool’s handedness even when its surrounding base mirrors.

<a id="Platform-considerations"></a>
## Platform considerations
No additional platform-specific rules are given.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/right-to-left) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.
