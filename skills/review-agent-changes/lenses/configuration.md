# Configuration and Rollout Safety

Review feature flags, environment variables, defaults, migrations, and rollout
paths for safe defaults, clear invalid-configuration failures, and behavior for
existing users. Trace configuration through loading, validation, and consumers
rather than reviewing declarations in isolation.

Check that migration and rollback paths preserve required compatibility, but do
not preserve compatibility for unshipped intermediate shapes. Flag only
concrete unsafe defaults, ambiguous transitions, or unsupported rollout states,
traceable to the changed configuration and a real deployment or user-visible
behavior.
