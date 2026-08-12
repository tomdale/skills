# Dependency Boundaries

Check that foundational modules do not depend on higher-level command, UI, or
application code without an established boundary. Trace cross-layer imports,
adapters, package dependencies, and shared utilities to the lowest suitable
layer.

Flag a boundary only when it creates an architectural inversion, circular-risk,
or confusing ownership. Prefer the smallest move or shared abstraction that
matches existing dependency direction; do not reorganize modules for aesthetics
alone.
