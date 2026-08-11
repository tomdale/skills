# Custom Tool Patterns Reference

> Source: `docs/extensions.md` + `examples/extensions/` (v0.79.x)

## Tool Definition Structure

```typescript
import { Type } from "typebox";
import { StringEnum } from "@earendil-works/pi-ai";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

pi.registerTool({
  name: "my_tool",           // snake_case
  label: "My Tool",          // display label in TUI
  description: "...",        // shown to LLM in system prompt

  // Optional: one-line entry in "Available tools" section of system prompt
  promptSnippet: "List or add items in the project todo list",

  // Optional: bullets appended to "Guidelines" section (only when tool is active)
  // MUST name the tool explicitly — avoid "Use this tool when..." (LLM can't tell which)
  promptGuidelines: ["Use my_tool when the user asks for a task list."],

  parameters: Type.Object({
    action: StringEnum(["list", "add"] as const),  // ← NOT Type.Union/Literal (Google breaks)
    text: Type.Optional(Type.String()),
  }),

  // Optional: backward-compat shim. Runs before schema validation.
  prepareArguments(args) {
    if (!args || typeof args !== "object") return args;
    const input = args as { oldField?: string; action?: string };
    if (input.oldField && !input.action) return { ...input, action: input.oldField };
    return args;
  },

  async execute(toolCallId, params, signal, onUpdate, ctx) {
    // signal: AbortSignal | undefined
    // onUpdate: stream partial results
    onUpdate?.({ content: [{ type: "text", text: "Working..." }], details: { progress: 50 } });

    if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

    return {
      content: [{ type: "text", text: "Done" }],   // sent to LLM
      details: { result: "..." },                    // for rendering & state reconstruction
      terminate: true,  // hint: skip auto follow-up LLM call (only if ALL tools in batch terminate)
    };
  },

  renderCall(args, theme, context) { /* returns Component */ },
  renderResult(result, { expanded, isPartial }, theme, context) { /* returns Component */ },
  renderShell: "self",  // take full control of framing; omit for default Box wrapper
});
```

**Throwing errors:** `throw new Error("message")` → `isError: true` on the result. Returning a value never sets the error flag.

## StringEnum (Google Gemini/Vertex compatibility)

```typescript
import { StringEnum } from "@earendil-works/pi-ai";

// ✅ Works with all providers including Google:
parameters: Type.Object({ action: StringEnum(["list", "add"] as const) })

// ❌ Fails on Google Gemini/Vertex:
parameters: Type.Object({ action: Type.Union([Type.Literal("list"), Type.Literal("add")]) })
```

## Output Truncation

**Always truncate tool output.** Large outputs cause context overflow and compaction failures.

```typescript
import {
  truncateHead,      // keep first N lines/bytes (file reads, search results)
  truncateTail,      // keep last N lines/bytes (logs, command output)
  truncateLine,      // truncate a single line with ellipsis
  formatSize,
  DEFAULT_MAX_BYTES, // 50KB
  DEFAULT_MAX_LINES, // 2000
} from "@earendil-works/pi-coding-agent";

const output = await runSomething();
const truncation = truncateHead(output, { maxLines: DEFAULT_MAX_LINES, maxBytes: DEFAULT_MAX_BYTES });

let result = truncation.content;
if (truncation.truncated) {
  // Write full output to temp file and tell LLM where to find it
  result += `\n\n[Truncated: ${truncation.outputLines}/${truncation.totalLines} lines shown.`;
  result += ` Full output saved to /tmp/full-output.txt]`;
}
return { content: [{ type: "text", text: result }] };
```

## withFileMutationQueue (parallel safety)

When a tool mutates files and may run in parallel with other tools (default in multi-tool turns):

```typescript
import { withFileMutationQueue } from "@earendil-works/pi-coding-agent";
import { resolve } from "node:path";

async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
  const absolutePath = resolve(ctx.cwd, params.path);
  return withFileMutationQueue(absolutePath, async () => {
    // read-modify-write atomically within the per-file queue
    const current = await readFile(absolutePath, "utf8");
    const next = transform(current, params);
    await writeFile(absolutePath, next, "utf8");
    return { content: [{ type: "text", text: `Updated ${params.path}` }], details: {} };
  });
}
```

Pass the real target path (resolve to absolute first). For existing files, `realpath()` is used so symlink aliases share one queue.

## Overriding Built-in Tools

Register a tool with the same name as a built-in (`read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`). TUI shows a warning.

```typescript
// Override bash with logging:
pi.registerTool({
  name: "bash",
  // your custom execute...
  // renderCall/renderResult: inherit from built-in if omitted
  // promptSnippet/promptGuidelines: NOT inherited, define explicitly if needed
});
```

**Your result shape must match the built-in exactly** (same `details` type). Built-in source links:
- `github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/tools/`
- Types: `ReadToolDetails`, `BashToolDetails`, `GrepToolDetails`, `FindToolDetails`, `LsToolDetails`

Use `--no-builtin-tools` to start without any built-in tools (keep extension tools).

## Remote Execution (SSH, containers)

```typescript
import { createReadTool, createBashTool } from "@earendil-works/pi-coding-agent";
import { createLocalBashOperations } from "@earendil-works/pi-coding-agent";

// Create tool with custom operations object
const remoteTool = createReadTool(cwd, {
  operations: {
    readFile: (path) => sshExec(`cat ${path}`),
    access: (path) => sshExec(`test -r ${path}`).then(() => {}),
  }
});

// Bash spawn hook
const bashTool = createBashTool(cwd, {
  spawnHook: ({ command, cwd, env }) => ({
    command: `source ~/.profile\n${command}`,
    cwd: `/mnt/sandbox${cwd}`,
    env: { ...env, CI: "1" },
  }),
});
```

See `examples/extensions/ssh.ts` for a complete SSH example.

Operations interfaces: `ReadOperations`, `WriteOperations`, `EditOperations`, `BashOperations`, `LsOperations`, `GrepOperations`, `FindOperations`.

## Custom Rendering

Tools can provide `renderCall` and `renderResult`. Both receive `(args, theme, context)` where:
- `context`: `{ args, state, lastComponent, invalidate(), toolCallId, cwd, executionStarted, argsComplete, isPartial, expanded, showImages, isError }`
- `context.state`: shared cross-slot state (use for data that must survive call→result)
- `context.lastComponent`: previously returned component for this slot

```typescript
import { Text, Box } from "@earendil-works/pi-tui";

renderCall(args, theme, context) {
  const text = (context.lastComponent as Text | undefined) ?? new Text("", 0, 0);
  text.setText(theme.fg("toolTitle", theme.bold("my_tool ")) + theme.fg("dim", args.action));
  return text;  // reuse and mutate the same Text instance
},

renderResult(result, { expanded, isPartial }, theme, context) {
  if (isPartial) return new Text(theme.fg("warning", "Working..."), 0, 0);
  let text = theme.fg("success", "✓ Done");
  if (expanded && result.details?.items) {
    for (const item of result.details.items) text += "\n  " + theme.fg("dim", item);
  }
  return new Text(text, 0, 0);
},
```

- Default `Box` handles padding; use `Text` with `(0, 0)` padding
- Return empty `Container` for intentionally empty slots (not `undefined`)
- `renderShell: "self"` for full frame control (large previews, stable bg)
- On fallback: `renderCall` shows tool name; `renderResult` shows raw `content` text

## Dynamic Tool Loading

Register tools but keep them inactive initially; a "loader" tool activates them on demand.

```typescript
pi.registerTool({ name: "lazy_tool", ... });  // register all tools

pi.on("session_start", () => {
  // Remove lazy tools from initial active set
  const initial = pi.getActiveTools().filter(n => n !== "lazy_tool");
  pi.setActiveTools([...initial, "search_tools"]);  // keep loader active
});

// In search_tools execute():
const toAdd = findMatchingTools(params.query);
pi.setActiveTools([...new Set([...pi.getActiveTools(), ...toAdd])]);  // ADDITIVE only
```

**Additive requirement:** `setActiveTools()` must be additive for deferred loading to work. Non-additive changes fall back to sending the full tool list on the next request.

**Native deferred loading support:**
- Anthropic: Sonnet/Opus/Fable v4.5+ (not Haiku) — uses `defer_loading`/`tool_reference`
- OpenAI: `gpt-5.4`+ — uses `tool_search_call`/`tool_search_output`

## State Management (session branching support)

Store state in tool result `details` for correct behavior across branches:

```typescript
let items: string[] = [];

pi.on("session_start", async (_event, ctx) => {
  items = [];
  for (const entry of ctx.sessionManager.getBranch()) {
    if (entry.type === "message" && entry.message.role === "toolResult"
        && entry.message.toolName === "my_tool") {
      items = entry.message.details?.items ?? [];
    }
  }
});

pi.registerTool({
  name: "my_tool",
  async execute(_id, params) {
    items.push(params.newItem);
    return { content: [{ type: "text", text: "Added" }], details: { items: [...items] } };
  },
});
```

## defineTool (standalone SDK use)

```typescript
import { defineTool } from "@earendil-works/pi-coding-agent";
const myTool = defineTool({ name: "greet", label: "Greet", description: "...",
  parameters: Type.Object({ name: Type.String() }),
  execute: async (_id, params) => ({ content: [{ type: "text", text: `Hi ${params.name}` }], details: {} }),
});
// Use in createAgentSession({ customTools: [myTool] })
```

## Leading `@` in Path Arguments

Some models prepend `@` to path arguments. Built-in tools strip it. If your custom tool accepts paths, do the same:

```typescript
const path = params.path.startsWith("@") ? params.path.slice(1) : params.path;
```

## Multiple Tools with Shared State

```typescript
export default function (pi: ExtensionAPI) {
  let connection: DbConnection | null = null;

  pi.registerTool({ name: "db_connect", async execute(_id, params) {
    connection = await createConnection(params.url);
    return { content: [{ type: "text", text: "Connected" }], details: {} };
  }});
  pi.registerTool({ name: "db_query", async execute(_id, params) {
    if (!connection) throw new Error("Not connected");
    const rows = await connection.query(params.sql);
    return { content: [{ type: "text", text: JSON.stringify(rows) }], details: { rows } };
  }});

  pi.on("session_shutdown", async () => { connection?.close(); connection = null; });
}
```
