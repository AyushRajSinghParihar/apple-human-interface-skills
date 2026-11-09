**Treat the single line as the default layout, and let it reflow as text grows.** Apple’s [Dynamic Type guidance](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type) specifically recommends stacking inline timestamps when space becomes cramped.

For your cell:

- Use semantic fonts and enable automatic updates on **both** labels.
- Allow the title to wrap and the cell to grow.
- At accessibility sizes, move the timestamp below the title. Reflow earlier if narrow widths or long localized text require it.
- Scale a meaningful icon with the text; avoid a fixed image frame that clips it.

```swift
titleLabel.font = .preferredFont(forTextStyle: .body)
timestampLabel.font = .preferredFont(forTextStyle: .caption1)

for label in [titleLabel, timestampLabel] {
    label.adjustsFontForContentSizeCategory = true
    label.numberOfLines = 0
}

iconView.preferredSymbolConfiguration =
    UIImage.SymbolConfiguration(textStyle: .body)
iconView.adjustsImageSizeForAccessibilityContentSizeCategory = true

tableView.rowHeight = UITableView.automaticDimension
tableView.estimatedRowHeight = 60
```

A practical arrangement is an outer horizontal stack containing the icon and an inner stack containing the labels. Switch the inner stack’s layout:

```swift
private func updateTextLayout() {
    let expanded = traitCollection
        .preferredContentSizeCategory
        .isAccessibilityCategory

    textStack.axis = expanded ? .vertical : .horizontal
    textStack.alignment = expanded ? .leading : .firstBaseline
    textStack.spacing = expanded ? 4 : 8
}
```

Call this during setup and when the content-size-category trait changes, using trait observation on iOS 17+ or `traitCollectionDidChange(_:)` on older versions. Constrain the outer stack to all four `contentView.layoutMarginsGuide` edges, and avoid fixed cell or label heights.

In the horizontal layout, give the timestamp higher horizontal compression resistance so the title wraps first. Don’t use `adjustsFontSizeToFitWidth` to counteract the user’s chosen text size.

Verify every Dynamic Type size, especially the largest accessibility size, with long titles, localized timestamps, narrow widths, and Bold Text. The essential check is that both pieces of information remain readable without clipping.