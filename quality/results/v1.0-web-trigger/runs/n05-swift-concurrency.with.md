**Use `async let` for a fixed set of independent operations; use a `TaskGroup` for a dynamic set or when you need to process results as they finish.** Both create child tasks within Swift’s structured concurrency model. [Swift concurrency guide](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html)

| | `async let` | `TaskGroup` |
|---|---|---|
| Number of tasks | Known where you write the code | Can be determined at runtime |
| Result types | Each binding can have a different type | All children share one result type |
| Getting results | Await named bindings | Iterate results in completion order |
| Control | Simple, scope-based lifetime | Add tasks dynamically and cancel the group |

With `async let`, operations start without immediately waiting for each one:

```swift
async let user = fetchUser()       // Returns User
async let posts = fetchPosts()     // Returns [Post]

// Both operations are already underway.
let dashboard = try await Dashboard(user: user, posts: posts)
```

This is useful when loading a screen requires a few known pieces of data.

With a task group, you can create one task per item:

```swift
let images = try await withThrowingTaskGroup(of: Image.self) { group in
    for id in imageIDs {
        group.addTask {
            try await fetchImage(id: id)
        }
    }

    var results: [Image] = []
    for try await image in group {
        results.append(image)
    }
    return results
}
```

Here, `images` follows **completion order**, which can differ from `imageIDs`. To preserve input order, return an index alongside each image and reorder the results. [TaskGroup documentation](https://docs.swift.org/latest/documentation/swift/taskgroup/)

Both approaches keep children within their scope: **the scope cannot finish until every child finishes**, even after cancellation. Cancellation is cooperative, so children must respond to it. Neither approach guarantees execution on separate threads. [TaskGroup documentation](https://docs.swift.org/latest/documentation/swift/taskgroup/)