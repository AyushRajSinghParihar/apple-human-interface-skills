# Game Center: artwork and interface examples

Source: [Apple HIG — Game Center](https://developer.apple.com/design/human-interface-guidelines/game-center), independently inspected in the 2026-10-25 snapshot. These are original descriptions; no Apple artwork is included.

## Artwork crop conflict

The source's challenge and multiplayer-activity diagrams label their cropped region **1465 × 1080 pt**. The adjacent specification tables instead give **1465 × 767 pt**, or **2930 × 1534 px at @2x**. Both use a full image canvas of **1920 × 1080 pt**, or **3840 × 2160 px at @2x**.

The article guide retains the table values. The diagram discrepancy remains unresolved; neither source value should be silently presented as unanimous guidance. Keep essential artwork inside the smaller shared region as a conservative design precaution, and verify the current Apple production templates and implementation requirements before exporting final artwork.

## System presentation

The main-menu example keeps the Game Center access point in a corner away from the title and start action. Its overlay exposes friends, progress, achievements, challenges and multiplayer without replacing the game's own identity.

Achievement cards combine circular artwork, a short title and a short description, while locked and completed groups remain distinct. The image-mask diagrams differ across platforms: ordinary achievement artwork fills its circular mask, while the television mask occupies a smaller central area inside its canvas.

Challenge and multiplayer cards place system-owned titles, player counts and a legibility gradient over the supplied artwork. Compose the art so the important subject survives those overlays and platform crops; do not bake the card title or description into the image itself.
