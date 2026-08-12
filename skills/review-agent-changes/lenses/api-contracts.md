# API Contracts and Compatibility

Review public request, response, client, schema, SDK, and serialized-data
changes against real callers and documented contracts. Check validation,
defaults, pagination, error shapes, idempotency, and compatibility promises.

Do not preserve internal flexibility merely because it was present in an
unmerged implementation. Preserve public contracts and durable stored data; ask
for evidence before treating an internal shape as externally supported.

Pair with `compatibility` in one reviewer: limit compatibility judgment here to
released surface and durable data; shim triage belongs there. Report only a
contract risk with a real caller.
