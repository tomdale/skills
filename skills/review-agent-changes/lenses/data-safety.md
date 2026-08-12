# Data Safety

Review archive, delete, remove, revoke, purge, migration, retention, and restore
flows for evidence gates, confirmation timing, non-interactive behavior,
dry-run and recovery paths, idempotency, and fail-open versus fail-closed
choices. Match the guardrail to the operation's irreversible risk.

Check that warnings describe an action only when it will occur, confirmations
precede mutations, retries remain actionable, and a bypass is visibly deliberate
rather than an accidental side effect of a convenience flag.

Pair with `data-policy` and `security` in one reviewer: report only a guardrail
gap exposing an irreversible or data-loss risk; retention and privacy policy
belong to `data-policy`.
