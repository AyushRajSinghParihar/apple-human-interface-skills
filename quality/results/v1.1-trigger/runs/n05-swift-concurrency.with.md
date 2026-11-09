Both `async let` and `TaskGroup` run **child tasks concurrently within a scope**. The main difference is whether you know the number of tasks ahead of time.

| | `async let` | `TaskGroup` |
|---|---|---|
| Best for | A fixed set of concurrent operations | A dynamic number of operations |
| Result types | Each binding can have a different type | All children return the same type |
| Results | Await named bindings | Iterate results as tasks finish |
| Syntax | Simple declarations | Explicitly add and manage tasks |

**Use `async let` for a few known operations:**

```swift
async let user = fetchUser()
async let posts = fetchPosts()

let (loadedUser, loadedPosts) = try await (user, posts)
```

Both operations start without waiting for the other. You await their results when you need them. Here, `fetchUser()` and `fetchPosts()` can return different types.

**Use a task group when the work depends on a collection or runtime decisions:**

```swift
let images = try await withThrowingTaskGroup(of: Image.self) { group in
    for url in urls {
        group.addTask {
            try await downloadImage(from: url)
        }
    }

    var results: [Image] = []
    for try await image in group {
        results.append(image)
    }
    return results
}
```

The group yields results in **completion order**, so `images` may not match the order of `urls`. To preserve input order, return each image alongside its original index.

Both use **structured concurrency**: child tasks cannot outlive their scope, and cancellation propagates from parent to children. Cancellation is cooperative, so the child’s work must respond to it.

Choose `async let` when you can name the operations individually; choose `TaskGroup` when you need to create or process tasks dynamically.