# Documentation and Durable Context

Review documentation, comments, help text, examples, changelogs, and
model-facing guidance for durable reader value. Use the `documentation-comments`
skill's standard: prose should orient a future maintainer or user to runtime
behavior, architecture, an invariant, a compatibility promise, a security
boundary, or another contract that survives the current change.

Flag text that mainly recounts the current conversation, recently changed
implementation details, review history, temporary rollout state, or other
ephemeral context. A reader who encounters the code after this implementation
session is forgotten should still learn something the code cannot say itself.

Keep model-facing instructions distinct from human documentation. Tool
descriptions and schema descriptions should guide the model; comments should
explain the architectural context a human maintainer needs. Do not delete
durable compatibility, security, serialization, or operational context merely
because it arose during this change.
