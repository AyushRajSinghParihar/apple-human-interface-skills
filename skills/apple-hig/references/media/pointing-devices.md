# Pointing device visual examples

Source: [Apple HIG pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices).

## Distinct pointer effects

In Photos, the pointer becomes a rounded highlighted background around a tab's
symbol and title, moving between tab targets. In Calendar's confirmation, the
button background darkens while the circular pointer remains visible. These are
different relationships: Highlight integrates the pointer with the target;
Hover changes the target without replacing the pointer's ordinary shape.

In the Dock, an app icon lifts and enlarges as the pointer disappears beneath it,
then settles back when the pointer moves away. Leave room for the lifted element
and preserve a coherent transition into and out of its shape.

The Clock example illustrates magnetism as the highlighted capsule remains tied
to nearby tab targets while moving between them. Favor the system's targeting
behavior for the effects that support it, instead of making every element pull
on the pointer. In text-entry areas, the pointer changes to an I-beam and returns
to a circle between fields; keep that familiar distinction.

## Trackpad interaction in space

The visionOS Safari sequence pairs hand movement on a physical trackpad with
pointer targeting and page scrolling in a spatial window. Pointer input remains
useful even when the keyboard and trackpad sit outside the immediate field of
view. Support standard pointing and scrolling alongside spatial inputs; people
need not reach toward the window for these operations.
