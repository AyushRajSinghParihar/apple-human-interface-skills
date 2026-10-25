# Haptic visual and audio examples

Source: [Apple HIG playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics).

## Read the illustrations as predefined feedback

The moving playhead crosses diagrams of pulse timing and relative strength while
the clips provide an audible illustration. These examples explain predefined
system patterns; they are not audio assets to copy into an app. Select the system
feedback type for its documented meaning, and evaluate tactile results on the
intended device. An image or decoded recording does not reproduce how a haptic
feels in the hand.

## iPhone patterns

Success shows two pulses with a stronger second pulse; warning shows a stronger
first pulse followed by a weaker second pulse. Error uses four pulses with a
changing strength profile. Keep those outcomes semantically distinct instead of
reusing the same feedback for both success and failure.

The light, medium, and heavy impact examples are individual pulses with increasing
strength. The rigid example is visually narrow and abrupt; the soft example has a
broader envelope. Choose the impact character that matches the physical metaphor
of the accompanying animation, rather than treating every impact as a heavier
version of the same event. Selection is a separate brief pulse associated with
changing a control's values.

## Apple Watch patterns

The watch demonstrations pair tactile envelopes with distinct audible motifs.
Click is isolated and brief. Start presents one initial tactile event, while Stop
presents two separated events. Up and Down each show a short sequence whose audio
and relative envelope help distinguish opposite threshold crossings. Success has
a multi-event motif; Failure and Retry show longer sequences that require their
documented semantic distinction even when their diagrams look similar.
Notification combines short events with a more extended tapering event to attract
attention.

Use Notification for noteworthy events, Up or Down for important threshold
crossings, Success for completion, Failure for an unsuccessful action, Retry when
another attempt is possible, Start and Stop for user-controlled activities, and
Click for discrete progress increments. Preserve these meanings throughout the
experience. Frequent overlapping Click feedback can make increments harder to
understand.
