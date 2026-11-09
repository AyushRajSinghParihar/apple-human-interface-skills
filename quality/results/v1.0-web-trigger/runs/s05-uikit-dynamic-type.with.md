Support the one-line layout where it fits, but **let it reflow as text grows**. At larger sizes, put the timestamp below the title and let the title wrap. Apple explicitly recommends stacking inline timestamps and growing containers for Dynamic Type. [HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type)

For a custom UIKit cell:

```swift
titleLabel.font = .preferredFont(forTextStyle: .body)
timestampLabel.font = .preferredFont(forTextStyle: .caption1)

for label in [titleLabel, timestampLabel] {
    label.adjustsFontForContentSizeCategory = true
    label.adjustsFontSizeToFitWidth = false
}
titleLabel.numberOfLines = 0
timestampLabel.numberOfLines = 0

tableView.rowHeight = UITableView.automaticDimension
tableView.estimatedRowHeight = 60
```

Use `UIFontMetrics` if you have custom fonts. Setting `adjustsFontForContentSizeCategory` alone doesn’t make an arbitrary fixed-size font scale. [UIKit: Scaling fonts automatically](https://developer.apple.com/documentation/uikit/scaling-fonts-automatically)

A practical layout is an outer horizontal stack containing the icon and an inner stack containing the title and timestamp:

- **When space permits:** inner stack is horizontal, with first-baseline alignment.
- **When space is tight:** inner stack becomes vertical, with leading alignment. Accessibility categories are a useful starting breakpoint; long titles and localized dates may need reflow earlier.
- **Icon:** scale a meaningful symbol with its associated text style; avoid fixed constraints that prevent growth.
- **Constraints:** pin the layout to `contentView.layoutMarginsGuide` on all four sides, providing an unbroken top-to-bottom constraint chain. Avoid fixed cell or label heights. [UIKit: Self-sizing cells](https://developer.apple.com/documentation/uikit/creating-self-sizing-table-view-cells)

For the category-based part of that layout:

```swift
func updateTextLayout() {
    let stacked =
        traitCollection.preferredContentSizeCategory.isAccessibilityCategory

    textStack.axis = stacked ? .vertical : .horizontal
    textStack.alignment = stacked ? .leading : .firstBaseline
}
```

Call this during setup and when the preferred content-size trait changes. Font updates happen automatically; your custom stack arrangement still needs updating.

**Don’t shrink text to preserve the single line.** Test every Dynamic Type size, especially the largest accessibility size, with long titles, localized timestamps, and narrow screens. No runtime validation was performed here.