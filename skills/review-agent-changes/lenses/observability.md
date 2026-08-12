# Observability

Review telemetry, logs, metrics, traces, alerts, and error context at the
operation boundary. Events should identify meaningful outcomes and failures
without secrets, high-cardinality values, or duplicate noise.

Check that new dangerous, asynchronous, or user-visible operations provide the
context operators need to diagnose them, while respecting existing telemetry and
output conventions. Do not add telemetry solely because a code path changed.
Report only a missing-operability gap for a changed operation, supported by the
changed code and its operational context.
