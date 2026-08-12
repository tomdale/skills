# Compatibility and Cruft

Trace every compatibility shim, fallback, alias, adapter, normalization branch,
or legacy input/output shape to a current production consumer or documented
external contract. The existence of a test is not proof of a real consumer.

Agent-generated changes often retain compatibility with an API, helper,
parameter, or data shape introduced earlier in the same working session. If the
supposed older shape has never shipped, been pushed, or merged into the review
base, it has no compatibility obligation. Remove that shim and tests that only
encode it.

Preserve compatibility only for real released callers, in-flight work that can
resume against the change, durable serialized data, or explicitly documented
external contracts. Apply the `cruft` skill's consumer-triage rules when this
lens finds a candidate.

Pair with `api-contracts` in one reviewer: this lens decides whether a shim has
a real consumer; `api-contracts` applies to released surface and durable data.
