# Performance and Resource Use

Review queries, pagination, loops, buffering, payloads, caching, and hot paths
for unbounded work or changed cost at the expected scale. Trace the changed path
far enough to identify multiplicative calls, repeated fetches, materialized
large collections, and missing limits.

Use workload evidence and local performance conventions. Do not report a
hypothetical micro-optimization without a plausible affected path or scale.
