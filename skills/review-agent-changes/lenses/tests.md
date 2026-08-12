# Tests and Validation

Check that tests assert user-visible or contract-level behavior, including
negative and failure paths. Identify mocks that can hide incorrect integration,
and validation claims unsupported by commands that actually ran.

Treat tests as suspect when they only prove that a recently removed API, option,
or behavior remains absent. A negative test is valuable only when absence is a
durable contract, safety invariant, compatibility promise, or security boundary.

Prefer outcomes over implementation details. Do not preserve tests that only
assert private helper calls, internal control flow, incidental request shapes,
or exact prompt phrasing unless that detail is an intentional, versioned
contract. For prompts, test the model-visible behavior or durable policy
requirement rather than wording chosen during the current implementation.

Recommend the narrowest missing test or higher-level verification that exposes
the risk. Update or delete implementation-detail tests that only memorialize an
abandoned implementation.
