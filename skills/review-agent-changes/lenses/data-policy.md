# Data Policy (Lifecycle and Privacy)

Review data creation, retention, archival, deletion, export, restoration, and
personal-data handling as one lifecycle. Check that transitions are deliberate,
recoverable where promised, and consistent with retention and privacy
contracts.

Distinguish a real retention or restoration guarantee from temporary
implementation state. Flag irreversible behavior, missing cleanup, or exposed
personal data only when supported by the changed contract or consumer flow.

Pair with `data-safety` in one reviewer: destructive flow mechanics
(confirmation, dry-run, recovery) belong there; scope this lens to the data
lifecycle policy — retention, export, restore, privacy, and deliberate
transitions.
