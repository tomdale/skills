# Behavior and Regression Risk

Follow changed values, state, and control flow into real production callers.
Check input validation, error classification, retries, state transitions,
partial failures, boundary conditions, and backward-compatible behavior. Tests
are evidence; they do not prove untested callers or failure modes are safe.

Report only behavior risks traceable to the diff and a real consumer or
contract. Recommend the smallest fix that preserves the intended change.
