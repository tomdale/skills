# Concurrency and Idempotency

Review asynchronous mutations, retries, queues, jobs, locks, and shared state
for time-of-check/time-of-use gaps, duplicate mutation, stale writes, ordering
assumptions, cancellation leaks, and retry safety.

Each concurrent or repeated path needs an explicit safe outcome. Prefer
idempotent mutation contracts and fresh verification at the mutation boundary
when stale evidence could cause harm. Report only a concurrency gap traceable to
the changed code and a real mutation, retry, or shared-state path.
