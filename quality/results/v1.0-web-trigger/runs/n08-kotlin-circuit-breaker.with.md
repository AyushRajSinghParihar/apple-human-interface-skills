Add a circuit breaker **around outbound calls to a failing dependency**. If your own backend is exhausting its CPU, threads, or database pool, you’ll also need concurrency limits and capacity fixes—a breaker alone won’t resolve that.

[Resilience4j](https://resilience4j.readme.io/docs/circuitbreaker) supports Kotlin: it tracks failures, opens to reject calls quickly, and later allows a few recovery probes.

For a coroutine-based backend:

```kotlin
// build.gradle.kts — use the same JVM-compatible version for both
implementation("io.github.resilience4j:resilience4j-circuitbreaker:$resilience4jVersion")
implementation("io.github.resilience4j:resilience4j-kotlin:$resilience4jVersion")
```

Create one shared breaker per dependency, rather than one per request:

```kotlin
import io.github.resilience4j.circuitbreaker.CircuitBreaker
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig
import io.github.resilience4j.kotlin.circuitbreaker.executeSuspendFunction
import java.time.Duration

class InventoryGateway(private val client: InventoryClient) {
    private val breaker = CircuitBreaker.of(
        "inventory",
        CircuitBreakerConfig.custom()
            .slidingWindowSize(50)
            .minimumNumberOfCalls(20)
            .failureRateThreshold(50f)
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            .slowCallRateThreshold(50f)
            .waitDurationInOpenState(Duration.ofSeconds(10))
            .permittedNumberOfCallsInHalfOpenState(3)
            .build()
    )

    suspend fun fetchStock(productId: String): Stock =
        breaker.executeSuspendFunction {
            client.fetchStock(productId)
        }
}
```

The coroutine extension supports suspending calls directly. Ensure your HTTP client **throws for relevant downstream 5xx responses**; a returned error response won’t automatically count as an exception. Configure expected business errors, such as “product not found,” to be ignored by the breaker. [Kotlin integration](https://resilience4j.readme.io/docs/getting-started-4)

For production:

- Map `CallNotPermittedException` to **503 Service Unavailable**, or return a legitimate cached fallback.
- Set HTTP connection and request timeouts. The slow-call threshold records slowness; it doesn’t cancel requests.
- Add a **bulkhead/concurrency limit** to prevent too many simultaneous calls. A circuit breaker doesn’t limit concurrency while closed. [Breaker behavior](https://resilience4j.readme.io/docs/circuitbreaker)
- Avoid adding automatic retries initially; they can amplify overload.
- Load-test failure and recovery, watching latency, rejected calls, pool usage, and breaker transitions.

Are you using Spring Boot, Ktor, or another framework—and do the 500 logs point to a downstream service or local resource exhaustion?