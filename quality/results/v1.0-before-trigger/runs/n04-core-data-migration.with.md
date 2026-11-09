Use a **lightweight migration**: add the attribute in a new model version, mark it non-optional, and set its default **in the Core Data model**. Core Data can infer this migration without a custom mapping model. [Apple’s migration guidance](https://developer.apple.com/documentation/coredata/migrating-your-data-model-automatically)

1. Select your `.xcdatamodeld` file in Xcode and choose **Editor → Add Model Version**. Base it on the existing version.
2. In the new version, add the attribute—for example, `isArchived`, type **Boolean**.
3. In the Data Model inspector, uncheck **Optional** and set **Default Value** to `NO`.
4. Select the `.xcdatamodeld` container and set **Current Model Version** to the new version. Keep the old version bundled so Core Data can recognize existing stores.
5. Enable automatic migration before loading the store:

```swift
let container = NSPersistentContainer(name: "MyModel")

for description in container.persistentStoreDescriptions {
    description.shouldMigrateStoreAutomatically = true
    description.shouldInferMappingModelAutomatically = true
}

container.loadPersistentStores { _, error in
    if let error {
        // Handle or report the failure; preserve the existing store.
        print("Failed to load persistent store: \(error)")
    }
}
```

Existing objects receive `false` for `isArchived` during migration; newly inserted objects also get that model default. A value assigned only in Swift or `awakeFromInsert()` does **not** supply the migration default.

Test using a store created by the previous app version: open it with the updated app, confirm existing records remain intact, and check the new attribute’s value. A fresh installation alone won’t test migration.