---
name: portable-harness-development
description: Design, author, package, test, and maintain skills or extensions that work across Codex CLI, Claude Code CLI, Pi, and other agent harnesses. Use when making agent capabilities portable, mapping harness features, defining adapters, or reviewing cross-environment compatibility.
metadata:
  internal: true
---

# Portable Harness Development

Treat portability as a layered design problem, not as a claim that every harness has identical behavior. Maintain one harness-neutral capability description and small native adapters for loading, tools, lifecycle, packaging, and UX.

## Start with a capability contract

Define:

1. **Trigger** — when the capability applies and how a user invokes it.
2. **Inputs/outputs** — files, arguments, structured results, and failure states.
3. **Workflow** — ordered actions and verification independent of tool names.
4. **Required capabilities** — read/write, shell, network, MCP, subagents, hooks, UI, persistence.
5. **Safety invariants** — permissions, confirmation, secrets, idempotence, and rollback.
6. **Fallback** — what to do when an optional capability is absent.

Put this contract in a concise `SKILL.md`; move long explanations, schemas, and examples to `references/`.

## Native packaging map

| Concept | Codex CLI | Claude Code CLI | Pi |
|---|---|---|---|
| On-demand knowledge | `SKILL.md` in `.codex/skills`, `.agents/skills`, or user roots | `skills/<name>/SKILL.md` in plugin or supported skill locations | `SKILL.md` in `.pi/skills`, global, packages, or configured paths |
| Explicit command | `$SkillName` / mention | `/skill-name`; legacy `commands/*.md` | `/skill:name` when skill commands enabled |
| Package | plugin manifest / marketplace | `.claude-plugin/plugin.json`, marketplace | npm/git package with `pi` resource metadata |
| Native executable extension | hooks, MCP, plugin resources | hooks, agents, MCP, plugin resources | TypeScript extensions and custom tools |
| Lifecycle interception | hooks | hooks | extension events (`input`, `context`, `tool_call`, etc.) |
| Tool integration | built-ins, MCP, plugins | built-ins, MCP, plugins | `registerTool`, extensions, packages |
| UI | CLI/TUI features | CLI features | extension `ctx.ui` and TUI components |
| Isolation | sandbox and approval policy | permissions/settings; extension/MCP trust | extensions have full system access; project trust gates resources |

This matrix is a planning aid. Verify current names and schemas against each harness's first-party documentation.

## Authoring rules

- Use portable Markdown for the core; do not mention a harness-specific tool unless in an adapter or capability table.
- Phrase operations by intent (“read the target file”, “run the validator”) and map them to available tools.
- Make descriptions highly specific: each harness uses metadata for routing, but field limits and trigger behavior differ.
- Keep scripts deterministic, noninteractive where possible, bounded, and dependency-light.
- Never assume hooks, MCP, subagents, network, persistent state, or a TUI. Detect or declare them.
- Separate model guidance from deterministic automation. Put policy checks in scripts/hooks where available, and provide an explicit manual step otherwise.
- Make all paths, arguments, output formats, and error handling explicit.
- Use least privilege. Review every hook, MCP server, package dependency, and extension before loading.

## Adapter layout

```text
capability/
├── SKILL.md                 # universal contract and workflow
├── references/              # schemas and deep guidance
├── scripts/                 # portable deterministic helpers
├── adapters/
│   ├── codex/               # plugin/config/hooks/MCP mapping
│   ├── claude-code/         # plugin/marketplace/hooks/MCP mapping
│   └── pi/                  # package/extension/resource mapping
└── tests/
    ├── contract/            # harness-neutral behavior tests
    └── adapters/             # install/discovery/native smoke tests
```

Do not fork the workflow unnecessarily. An adapter may translate metadata, register a tool, expose a command, or add lifecycle enforcement, but the contract and acceptance criteria remain shared.

## Verification strategy

For each target harness:

1. Install/load in a clean temporary project using the native mechanism.
2. Verify discovery metadata and explicit invocation.
3. Run a happy-path task and a malformed-input task.
4. Exercise permission/trust-denied and missing-optional-capability paths.
5. Verify tool output, truncation, errors, cleanup, and repeatability.
6. Test packaging/uninstall and ensure no settings are silently overwritten.
7. Record the tested CLI/package version and source URLs.

Use static checks for frontmatter, manifests, paths, and references; use smoke tests for runtime behavior. A successful install is not evidence of portable semantics.

## Important gaps and design consequences

- **Skills are the common denominator**: all three can load Markdown guidance, but discovery roots, explicit syntax, metadata fields, and routing semantics differ.
- **Extensions are not common**: Pi has first-class TypeScript extensions and custom tools; Codex and Claude primarily compose plugins, hooks, MCP, agents, and skills. Keep Pi code optional and expose a script/MCP/manual fallback.
- **Lifecycle hooks differ**: Codex and Claude provide hook systems; Pi provides rich typed extension events. Put core invariants in the workflow and duplicate only enforcement adapters.
- **Security differs materially**: Codex has sandbox/approval controls; Claude relies on permissions and trust boundaries; Pi extensions run with full system access. Default to the most restrictive common behavior.
- **MCP is an adapter, not a guarantee**: Codex and Claude support MCP-oriented integration; Pi does not provide the same built-in MCP contract. Offer ordinary CLI/API fallback.
- **UI differs**: Pi exposes extension UI/TUI APIs; Codex and Claude do not offer an equivalent portable extension UI. Use text and structured files as the canonical interface.
- **State/session APIs differ**: Pi has SDK/session events; Codex and Claude have different CLI/session mechanisms. Persist portable state in explicit files with locking and migrations, not hidden session objects.

## Harness-specific testing

Run the common contract tests first, then exercise each native loader in a clean temporary project. Record the installed version, platform, package/plugin source, and exact command used.

### Codex CLI

1. Create a temporary project and place the skill under `.agents/skills/<name>/SKILL.md` or `.codex/skills/<name>/SKILL.md`.
2. Run `codex --version` and `codex --help`; confirm the current skill and plugin commands before relying on them.
3. Start an interactive session and verify the skill appears in the available skill context. Test explicit invocation with the current Codex syntax (for example `$skill-name` where supported) and a natural-language trigger.
4. Run a non-interactive smoke test with `codex exec` using a deterministic prompt. Capture stdout, stderr, exit status, and generated files; test `--json` if the integration consumes structured events. Place the skill in a discovered `.agents/skills/` or `.codex/skills/` root and invoke `codex exec` normally.
5. If packaged as a plugin, install it in the temporary Codex environment, verify `codex plugin list`, test discovery, then remove it and confirm the skill disappears.
6. Test the relevant approval policy and sandbox mode. A skill must not assume network, writes, or unrestricted shell access; verify its documented fallback when denied.

Use Codex's actual installed CLI and current official documentation for plugin and marketplace commands, because these commands are version-sensitive. Validate every suggested command with the installed subcommand's `--help` output before using it in a test or guide.

### Claude Code CLI

1. Create a clean temporary project and install or link the plugin from the checkout. Confirm the plugin is enabled using the current `/plugin` interface.
2. Verify the skill's frontmatter and test both model selection from a matching task and explicit `/skill-name` invocation when the skill exposes a user command.
3. Test argument handling, `argument-hint`, and `allowed-tools` restrictions. Confirm the skill behaves correctly when a requested tool is unavailable or denied.
4. Exercise every contributed native resource independently: commands or skills, agents, hooks, and MCP servers. For hooks, test success, failure, timeout, malformed input, and repeated execution.
5. Test in trusted and untrusted project contexts where applicable. Confirm project settings are not silently overwritten and that uninstalling the plugin removes its resources.
6. If the plugin uses MCP, verify authentication, transport, startup failure, tool errors, network boundaries, and secret redaction.

Use the installed Claude Code help/docs for the current plugin installation and diagnostic commands; do not hard-code undocumented CLI flags in portable instructions.

### Pi

1. Create a temporary project, ensure it is trusted as needed, and load the skill through `.pi/skills/`, a package, settings, or the CLI resource option. Run `pi --version` and confirm the current resource-loading options.
2. Test automatic skill selection and explicit `/skill:name` invocation with skill commands enabled. Verify argument substitution and behavior when the skill is not selected.
3. For extensions or packages, load the TypeScript extension with the supported project/global/package mechanism and confirm registration of tools, commands, shortcuts, providers, and message renderers.
4. Exercise lifecycle behavior across startup, new session, resume, fork, reload, shutdown, and idle/settled states. Test signal cancellation and cleanup of background resources.
5. Test custom tools with valid input, schema failures, thrown errors, large output/truncation, concurrent file mutation, and unavailable UI. Run both interactive TUI and non-interactive print/JSON/RPC modes when supported.
6. Verify project trust denial, missing optional dependencies, offline mode, and package uninstall/update behavior. Extensions have full system access, so include a permissions and dependency review.

Use Pi's installed versioned docs and examples for exact extension APIs and CLI flags. Do not treat an extension-only implementation as portable; provide a skill, script, or ordinary CLI fallback.

### Cross-harness acceptance matrix

For each harness, record:

| Check | Codex | Claude Code | Pi |
|---|---|---|---|
| Discovery in a clean project | pass/fail + version | pass/fail + version | pass/fail + version |
| Explicit invocation | syntax and result | syntax and result | syntax and result |
| Natural/model-triggered selection | result | result | result |
| Tool/permission denial fallback | result | result | result |
| Malformed input and error reporting | result | result | result |
| Large output/truncation behavior | result | result | result |
| Packaging and uninstall | result | result | result |
| Non-interactive execution | result | result if supported | print/JSON/RPC result |

A capability is portable only when the core acceptance criteria pass in every declared target, or the unsupported target has an explicit documented fallback.

## Release checklist

- Core `SKILL.md` has valid frontmatter for every target or generated native metadata.
- Trigger phrases and explicit invocation are documented per harness.
- Required capabilities and fallbacks are listed.
- No portable instruction depends on an unavailable tool name or lifecycle event.
- Native manifests are minimal, pinned where appropriate, and uninstallable.
- Security review covers scripts, hooks, MCP, network, dependencies, and permissions.
- CI validates structure and runs one smoke test per supported harness.
- README records supported versions, known gaps, and how adapters are generated.

## Sources and version caveat

This guide synthesizes the repo-local `codex-cli-development`, `claude-code-cli-development`, and `pi-development` guides and their first-party references. Codex and Claude Code APIs, marketplace formats, and Pi package/extension APIs evolve quickly; re-check official documentation and installed versions before release.
