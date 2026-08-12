---
name: review-agent-changes
description: Audit a batch of agent-generated changes through parallel, context-sensitive review lenses. Use before shipping agent-produced implementation work to find behavioral, validation, readability, safety, and repository-convention issues.
---

# Review Agent Changes

Audit a completed batch of agent-generated changes before shipping. This is a
quality gate for the current implementation, not a GitHub PR review and not a
review of another author's work. Review the diff against its base, identify
material issues, and either fix them after approval or report a clean result.

Do not use this skill to draft or post GitHub review feedback; use `pr-feedback`
for that. Do not modify files during the audit unless the user explicitly asks
for fixes.

## Preparation

1. Identify the base revision and review target. Prefer the branch merge base or
   repository default branch; state the comparison in the result.
2. Read applicable repository guidance before reviewing: `AGENTS.md`,
   `CLAUDE.md`, contribution guides, package-local instructions, and relevant
   design-system or CLI-UX references.
3. Read the complete diff and enough nearby unchanged code to understand local
   patterns and real consumers. Inspect tests, configuration, package metadata,
   release notes, and generated-file rules when the diff touches them.
4. Select the core and specialist lenses below. Do not select a lens merely
   because it exists; each selected lens must have a meaningful target in the
   diff.

## Lenses

Use all core lenses for substantive implementation changes. Add specialist
lenses only when the diff has a meaningful target. Read the selected lens file
before reviewing or delegating it.

| Lens | Use when | Reference |
| --- | --- | --- |
| Behavior and regression risk | Any substantive behavior change | [lenses/behavior.md](lenses/behavior.md) |
| Readability and house style | Any substantive implementation change | [lenses/readability.md](lenses/readability.md) |
| Prose and writing style | READMEs, docs, comments, help text, changelogs, examples, or model-facing prose | [lenses/writing-style.md](lenses/writing-style.md) |
| Tests and validation | Tests or validation claims are affected | [lenses/tests.md](lenses/tests.md) |
| Change scope | Any shippable change; checks diff coherence, delivery completeness, churn, and abandoned work | [lenses/change-scope.md](lenses/change-scope.md) |
| Documentation and durable context | Documentation, comments, help text, examples, changelogs, or model-facing guidance | [lenses/documentation.md](lenses/documentation.md) |
| Compatibility and cruft | Compatibility branches, fallbacks, aliases, adapters, normalization, or legacy shapes | [lenses/compatibility.md](lenses/compatibility.md) |
| CLI UX and machine output | Commands, prompts, confirmations, help, `--json`, agents, stdout/stderr, output managers | [lenses/cli-ux.md](lenses/cli-ux.md) |
| Data safety | Archive, delete, remove, revoke, purge, migration, retention, or restore guardrails | [lenses/data-safety.md](lenses/data-safety.md) |
| Dependency boundaries | Cross-layer imports, utilities, adapters, packages, shared modules | [lenses/dependency-boundaries.md](lenses/dependency-boundaries.md) |
| API contracts and compatibility | Public handlers, clients, schemas, SDKs, serialized data, pagination, idempotency | [lenses/api-contracts.md](lenses/api-contracts.md) |
| Concurrency and idempotency | Async mutations, retries, queues, jobs, locks, shared state | [lenses/concurrency.md](lenses/concurrency.md) |
| Security and secrets | Auth, authorization, tokens, redirects, input, network, permissions | [lenses/security.md](lenses/security.md) |
| Data policy | Retention, archival, deletion, export, restoration, privacy, deliberate lifecycle transitions | [lenses/data-policy.md](lenses/data-policy.md) |
| Observability | Telemetry, logs, metrics, tracing, alerts, error context | [lenses/observability.md](lenses/observability.md) |
| Accessibility and interaction design | UI components, forms, keyboard flows, focus, screen-reader behavior, motion | [lenses/accessibility.md](lenses/accessibility.md) |
| Performance and resource use | Queries, loops, pagination, payloads, caching, hot paths | [lenses/performance.md](lenses/performance.md) |
| Configuration and rollout safety | Feature flags, environment variables, defaults, migrations, rollout | [lenses/configuration.md](lenses/configuration.md) |

For a documentation-only change, select documentation and change focus, plus
any directly relevant lens; do not mechanically run concurrency or performance.
A clean lens is a valid result.

## Parallel Dispatch

When subagents are available, dispatch independent selected lenses in parallel.
Usually dispatch three to six reviewers.

Delegate lenses that share surface area to the same reviewer rather than
spreading them across subagents that would each re-read the same code and file
look-alike findings. Natural bundles: `behavior` with `concurrency`;
`compatibility` with `api-contracts`; `data-safety` with `data-policy` and
`security`; `accessibility` with `cli-ux`; `documentation` with
`writing-style`, which review the same prose. Merge or chain
lenses that need the same deep context, and do not ask multiple reviewers to
rediscover the same generic behavior.

Give every reviewer:

- the base revision, head revision, and relevant paths;
- the applicable repository guidance;
- its selected lens file and explicit scope;
- a read-only instruction: do not edit files;
- a requirement to report only evidence-backed findings with priority, path and
  line, impact, and smallest remedy;
- a requirement to report no finding when the lens is clean.

If parallel subagents are unavailable, review lenses sequentially: behavior,
safety specialists, tests, readability, documentation, then change scope.

## Synthesis

1. Deduplicate overlapping findings and preserve the clearest evidence.
2. Reject speculative findings, generic best-practice claims without local
   precedent, and findings contradicted by an intentional requirement.
3. Classify remaining findings:
   - **High:** likely correctness, safety, contract, or architectural-boundary
     harm that should block shipping.
   - **Medium:** material maintainability, UX, validation, or convention issue
     with a clear narrow fix.
   - **Low:** bounded improvement that is useful but should not delay shipping.
4. List clean lenses explicitly so the user knows what was examined.
5. Separate required fixes from optional follow-ups. Do not silently expand the
   scope into broad refactoring.

## Output

Start with the base/head comparison and selected lenses. List findings by
priority. Each finding includes priority and `path:line`, a concise title,
concrete evidence and relevant repository precedent, impact on this
implementation, and the smallest recommended remedy.

End with clean lenses, validation already observed and still recommended, and
optional follow-ups. Say plainly when the audit is clean rather than inventing
nits.
