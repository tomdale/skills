---
name: pi-development
description: "Develop for the Pi coding agent harness (v0.79.x): skills, extensions, custom tools, packages, prompt templates, SDK, TUI, and config. Use when building, debugging, or extending Pi behavior, implementing custom tools or events, or integrating Pi programmatically via SDK."
---

# Pi Development

> **v0.79.x** — Docs: `~/.local/share/proto/tools/npm__earendil-works-pi-coding-agent/0.79.1/lib/node_modules/@earendil-works/pi-coding-agent/docs/` | Examples: `...examples/` | https://pi.dev

## Architecture

Pi core + Extensions (TypeScript, full system access) + Skills (SKILL.md, on-demand) + Prompts (.md, /name) + Themes (.json) + Packages (npm/git bundles). Default tools: `read`, `bash`, `edit`, `write`; also `grep`, `find`, `ls`.

## Skills

Skills are `SKILL.md` directories providing agent-readable instructions loaded on-demand.

**Locations** (global → project → package → settings → CLI):

| Scope | Path |
|-------|------|
| Global | `~/.pi/agent/skills/`, `~/.agents/skills/` |
| Project | `.pi/skills/`, `.agents/skills/` (cwd→git root; trust required) |
| Package/CLI | `skills/` in package, `skills` in settings.json, `--skill <path>` |

Dirs containing `SKILL.md` found recursively everywhere; root `.md` files only in `~/.pi/agent/skills/` and `.pi/skills/`.

**Frontmatter** (in `SKILL.md`):

```yaml
---
name: my-skill           # required; 1-64 chars; a-z0-9 hyphens; unique
description: "..."       # required (≤1024 chars); specificity drives auto-loading
license: MIT             # optional
compatibility: "..."     # optional (≤500 chars)
allowed-tools: bash read # optional; space-delimited pre-approved tools
disable-model-invocation: false  # true → hidden from prompt; /skill:name only
---
```

Missing `description` → skill not loaded. Name collision → first found wins (warning).

**Invocation:** Agent auto-loads when description matches; explicit `/skill:name` or `/skill:name <args>` (args appended as `User: <args>`); `enableSkillCommands: true/false` in settings.

## Extensions

Extensions are TypeScript modules with full system access: tools, events, UI, commands, providers.

**Locations:**

| Scope | Path |
|-------|------|
| Global | `~/.pi/agent/extensions/*.ts` or `*/index.ts` |
| Project | `.pi/extensions/*.ts` or `*/index.ts` (trust required) |
| Settings/CLI | `extensions` array, `packages` list, `-e ./path.ts` or `-e npm:pkg` |

Auto-discovered locations support `/reload`; CLI `-e` paths do not.

**Factory pattern** — export default `function (pi: ExtensionAPI)` (or `async function`). Call `pi.on(event, handler)`, `pi.registerTool({...})`, `pi.registerCommand(name, {handler})` inside. TypeScript via [jiti](https://github.com/unjs/jiti) — no compilation needed. See `...examples/extensions/hello.ts` for a minimal example.

- **Async factories:** Pi awaits before startup — for remote model fetch, `registerProvider` init
- **Background resources:** Start in `session_start`, clean up in `session_shutdown` (never in factory)
- **npm deps:** Add `package.json` next to extension, run `npm install`; imports resolve automatically

**Key Events** (see [`references/extension-events.md`](references/extension-events.md) for full signatures):

| Event | Purpose / Return |
|-------|-----------------|
| `project_trust` | Custom trust before project resources load → `{ trusted: "yes"/"no"/"undecided" }` |
| `session_start` | Init state; `reason`: startup/new/resume/fork/reload |
| `resources_discover` | Contribute extra skill/prompt/theme paths → `{ skillPaths, promptPaths, themePaths }` |
| `before_agent_start` | Inject messages, modify system prompt → `{ message?, systemPrompt? }` |
| `input` | Transform/intercept user input → `{ action: "continue"/"transform"/"handled" }` |
| `context` | Modify messages before each LLM call → `{ messages }` |
| `tool_call` | Gate tool execution; mutate `event.input` → `{ block: true, reason? }` |
| `tool_result` | Modify tool results (chained) → `{ content?, details?, isError? }` |
| `session_shutdown` | Cleanup; `reason`: quit/reload/new/resume/fork |
| `agent_settled` | Final idle after all retries/follow-ups |

**Key `pi.*` methods:** `registerTool` · `registerCommand` · `registerShortcut` · `registerFlag` · `registerProvider` / `unregisterProvider` · `registerMessageRenderer` · `registerEntryRenderer` · `sendMessage` · `sendUserMessage` · `appendEntry` · `setSessionName` · `getActiveTools` / `setActiveTools` / `getAllTools` · `exec` · `setModel` · `setThinkingLevel` · `events`

**Key `ctx.*`:** `ui.*` · `sessionManager` · `mode` · `cwd` · `signal` · `compact()` · `isIdle()` · `isProjectTrusted()` · `getContextUsage()` · `getSystemPrompt()` · `shutdown()`

See [`references/extension-api.md`](references/extension-api.md) for full signatures. Commands get additional `ExtensionCommandContext` with `waitForIdle`, `newSession`, `fork`, `switchSession`, `reload`.

## Custom Tools

See [`references/tool-patterns.md`](references/tool-patterns.md) for TypeBox schemas, `StringEnum`, truncation utilities, `withFileMutationQueue`, `renderCall`/`renderResult`, built-in overrides, remote execution, dynamic loading.

**Critical rules:**
- **`StringEnum`** from `@earendil-works/pi-ai` for string enums — `Type.Union/Literal` fails on Google Gemini/Vertex
- **Error signaling:** Throw to set `isError: true`; returning a value never sets the flag
- **Output truncation:** 50KB/2000 lines max; use `truncateHead`/`truncateTail` from the package; always inform the LLM when truncated
- **File mutations:** Wrap in `withFileMutationQueue(absolutePath, fn)` for parallel-safe read-modify-write
- **`prepareArguments(args)`:** Optional hook before schema validation for backward-compat shims

## Packages

```bash
pi install npm:@scope/pkg[@version]        # pinned versions skipped by update
pi install git:github.com/user/repo[@ref]  # -l = project-local (.pi/npm or .pi/git)
pi remove npm:@scope/pkg   |   pi list   |   pi config  # enable/disable resources
pi update --all            # update pi + packages (skips pinned git refs)
pi update --extensions     # packages only
```

**`package.json`:** `"keywords": ["pi-package"]` + `"pi": { "extensions": [...], "skills": [...], "prompts": [...], "themes": [...] }`. Runtime deps → `dependencies`. Bundled pi-packages → `bundledDependencies`. Peer (do NOT bundle): `@earendil-works/pi-coding-agent`, `typebox`, `@earendil-works/pi-tui`, `@earendil-works/pi-ai`.

## Prompt Templates

Frontmatter: `description` (optional; first line used if absent), `argument-hint` (shown in autocomplete). Body uses `$1`/`$2`/`$@`, defaults `${1:-default}`, slices `${@:N}`. Filename → `/command-name`. Locations: `~/.pi/agent/prompts/`, `.pi/prompts/`, packages; non-recursive.

## Config / Settings

Files: `~/.pi/agent/settings.json` (global) and `.pi/settings.json` (project; trust required; overrides global). Key settings: `defaultProvider`, `defaultModel`, `defaultThinkingLevel`, `theme`, `compaction.*` (enabled/reserveTokens/keepRecentTokens), `retry.*`, `enabledModels`, `packages`, `extensions`, `skills`, `enableSkillCommands`, `npmCommand`, `shellCommandPrefix`, `defaultProjectTrust` (`"ask"`/`"always"`/`"never"`), `sessionDir`.

Env vars: `PI_CODING_AGENT_DIR`, `PI_OFFLINE`, `PI_SKIP_VERSION_CHECK`, `PI_TELEMETRY`, `PI_CACHE_RETENTION`; provider keys `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.

Non-interactive modes (`-p`, `--mode json`, `--mode rpc`) use `defaultProjectTrust`; pass `-a`/`--approve` to trust one run.

## SDK

```typescript
import { AuthStorage, createAgentSession, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";
const auth = AuthStorage.create();
const { session } = await createAgentSession({ authStorage: auth,
  modelRegistry: ModelRegistry.create(auth), sessionManager: SessionManager.inMemory() });
session.subscribe((e) => { if (e.type === "message_update" && e.assistantMessageEvent.type === "text_delta")
  process.stdout.write(e.assistantMessageEvent.delta); });
await session.prompt("List files here");
```

Key exports: `createAgentSession` · `createAgentSessionRuntime` · `DefaultResourceLoader` · `defineTool` · `SessionManager` · `SettingsManager` · `AuthStorage` · `ModelRegistry` · `InteractiveMode` · `runPrintMode` · `runRpcMode`.

See [`references/sdk-guide.md`](references/sdk-guide.md) for ResourceLoader, custom models/tools/extensions, session management, and run modes.

## TUI / UI

`ctx.ui` methods in extension handlers (`custom()` requires TUI mode; use `ctx.hasUI` to guard dialogs):

| Method | Description |
|--------|-------------|
| `notify(msg, level)` | Non-blocking toast (`"info"/"warning"/"error"`) |
| `confirm(title, msg, opts?)` | Confirm dialog; `{ timeout: ms }` or `{ signal }` for auto-dismiss |
| `select(title, items, opts?)` | Selection list |
| `input(title, placeholder?)` / `editor(title, prefill?)` | Text / multi-line input |
| `setStatus(key, text?)` | Footer status; clear with `undefined` |
| `setWidget(key, content, opts?)` | Widget above/below editor; `{ placement: "belowEditor" }` |
| `setFooter(fn?)` | Replace built-in footer entirely |
| `setEditorText(text)` | Pre-fill editor |
| `custom(fn, opts?)` | Full custom TUI component (TUI mode only); `{ overlay: true }` for modal |

TUI components implement `Component { render(width): string[]; handleInput?(data): void; invalidate(): void }`. Available in `@earendil-works/pi-tui`: `Text`, `Box`, `Container`, `SelectList`, `Input`.

## Limitations & Gotchas

- **No sandbox:** Extensions run with full user permissions; no built-in isolation
- **Project trust:** `.pi/` resources require trust interactively; configure `defaultProjectTrust` for CI
- **No MCP/sub-agents built-in:** Build extensions or install packages; spawn `pi` via tmux for sub-agents
- **Portability:** Import `CONFIG_DIR_NAME` from `@earendil-works/pi-coding-agent` instead of hardcoding `.pi`
- **Google Gemini:** `StringEnum` required; `Type.Union(Type.Literal(...))` fails
- **Reload:** Can't call `ctx.reload()` from tools; use a command + `pi.sendUserMessage("/cmd", { deliverAs: "followUp" })`
- **Session replacement:** After `newSession()`/`fork()`, use only the fresh `ctx` in `withSession`; old references go stale
- **Pinned git packages:** `pi update --all` skips pinned git refs; use `pi install git:host/user/repo@new-ref` to move

## References

| File | Contents |
|------|----------|
| [`references/extension-events.md`](references/extension-events.md) | All events with full signatures, lifecycle diagram, return types |
| [`references/extension-api.md`](references/extension-api.md) | All `pi.*` and `ctx.*` / `ExtensionCommandContext` method signatures |
| [`references/tool-patterns.md`](references/tool-patterns.md) | TypeBox, `StringEnum`, truncation, rendering, overrides, dynamic loading |
| [`references/sdk-guide.md`](references/sdk-guide.md) | SDK integration, `DefaultResourceLoader`, run modes, session management |
