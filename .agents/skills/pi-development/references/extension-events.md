# Extension Events Reference

> Source: `docs/extensions.md` (v0.79.x) — full lifecycle diagram in that file.

## Lifecycle Overview (condensed)

```
startup → project_trust → session_start → resources_discover
user prompt → input → before_agent_start → agent_start
  turn loop: turn_start → context → before_provider_headers →
             before_provider_request → [LLM] → after_provider_response →
             tool_execution_start → tool_call → tool_execution_update →
             tool_result → tool_execution_end → turn_end
→ agent_end → agent_settled
/new|/resume → session_before_switch → session_shutdown → session_start
/fork|/clone → session_before_fork → session_shutdown → session_start(reason:"fork")
exit → session_shutdown
```

## Event Signatures and Return Types

### `project_trust`
Fires before project resources load. Only user/global and CLI `-e` extensions participate.
```typescript
pi.on("project_trust", async (event, ctx) => {
  // event.cwd: string
  // ctx: limited (cwd, mode, hasUI, select/confirm/input/notify only)
  return { trusted: "yes" | "no" | "undecided", remember?: boolean };
  // First yes/no wins. "undecided" passes to next handler or built-in flow.
});
```

### `session_start`
```typescript
pi.on("session_start", async (event, ctx) => {
  // event.reason: "startup" | "reload" | "new" | "resume" | "fork"
  // event.previousSessionFile?: string  (present for new/resume/fork)
});
```

### `resources_discover`
Contribute additional skill, prompt, theme paths.
```typescript
pi.on("resources_discover", async (event, _ctx) => {
  // event.cwd: string
  // event.reason: "startup" | "reload"
  return { skillPaths?: string[], promptPaths?: string[], themePaths?: string[] };
});
```

### `session_info_changed`
```typescript
pi.on("session_info_changed", async (event, ctx) => {
  // event.name?: string  (undefined if cleared)
});
```

### `session_before_switch`
```typescript
pi.on("session_before_switch", async (event, ctx) => {
  // event.reason: "new" | "resume"
  // event.targetSessionFile?: string  (only for "resume")
  return { cancel: true };  // or return nothing to allow
});
```

### `session_before_fork`
```typescript
pi.on("session_before_fork", async (event, ctx) => {
  // event.entryId: string
  // event.position: "before" | "at"
  return { cancel: true };
});
```

### `session_before_compact` / `session_compact`
```typescript
pi.on("session_before_compact", async (event, ctx) => {
  // event.reason: "manual" | "threshold" | "overflow"
  // event.willRetry: boolean
  // event.preparation: { firstKeptEntryId, tokensBefore }
  // event.branchEntries, event.customInstructions, event.signal
  return { cancel: true };
  // OR provide custom summary:
  return { compaction: { summary: "...", firstKeptEntryId: "...", tokensBefore: 0 } };
});
pi.on("session_compact", async (event, ctx) => {
  // event.compactionEntry, event.fromExtension, event.reason, event.willRetry
});
```

### `session_before_tree` / `session_tree`
```typescript
pi.on("session_before_tree", async (event, ctx) => {
  // event.preparation, event.signal
  return { cancel: true };
  // OR: return { summary: { summary: "...", details: {} } };
});
pi.on("session_tree", async (event, ctx) => {
  // event.newLeafId, event.oldLeafId, event.summaryEntry, event.fromExtension
});
```

### `session_shutdown`
```typescript
pi.on("session_shutdown", async (event, ctx) => {
  // event.reason: "quit" | "reload" | "new" | "resume" | "fork"
  // event.targetSessionFile?: string
});
```

### `before_agent_start`
```typescript
pi.on("before_agent_start", async (event, ctx) => {
  // event.prompt: string
  // event.images: ImageContent[]
  // event.systemPrompt: string  (chained; includes prior handler changes)
  // event.systemPromptOptions: { customPrompt, selectedTools, toolSnippets,
  //   promptGuidelines, appendSystemPrompt, cwd, contextFiles, skills }
  return {
    message?: { customType: string; content: string; display?: boolean; details?: unknown },
    systemPrompt?: string,  // replaces for this turn (chained)
  };
});
```

### `input`
Fires after extension commands checked, before skill/template expansion.
```typescript
pi.on("input", async (event, ctx) => {
  // event.text: string
  // event.images: ImageContent[]
  // event.source: "interactive" | "rpc" | "extension"
  // event.streamingBehavior: "steer" | "followUp" | undefined
  return { action: "continue" };       // pass through (default)
  return { action: "transform", text: "..." };  // rewrite, then continue
  return { action: "handled" };        // skip agent (first wins)
});
```

### `context`
```typescript
pi.on("context", async (event, ctx) => {
  // event.messages: deep copy (safe to modify)
  return { messages: event.messages.filter(...) };
});
```

### `before_provider_headers`
```typescript
pi.on("before_provider_headers", (event, ctx) => {
  // event.headers: Record<string, string | null>  (mutate in place)
  event.headers["x-custom"] = "value";
  event.headers["x-remove"] = null;  // delete header
});
```

### `before_provider_request`
```typescript
pi.on("before_provider_request", (event, ctx) => {
  // event.payload: provider-specific body
  // return undefined to keep, or return modified payload to replace
  console.log(JSON.stringify(event.payload, null, 2));
});
```

### `after_provider_response`
```typescript
pi.on("after_provider_response", (event, ctx) => {
  // event.status: number  (HTTP status)
  // event.headers: Record<string, string>
});
```

### `tool_execution_start` / `tool_execution_update` / `tool_execution_end`
```typescript
pi.on("tool_execution_start", async (event, ctx) => {
  // event.toolCallId, event.toolName, event.args
});
pi.on("tool_execution_update", async (event, ctx) => {
  // event.toolCallId, event.toolName, event.args, event.partialResult
});
pi.on("tool_execution_end", async (event, ctx) => {
  // event.toolCallId, event.toolName, event.result, event.isError
});
```

### `tool_call`  ← **Can block. `event.input` is mutable.**
```typescript
import { isToolCallEventType } from "@earendil-works/pi-coding-agent";
pi.on("tool_call", async (event, ctx) => {
  // event.toolName, event.toolCallId, event.input (mutable)
  if (isToolCallEventType("bash", event)) {
    // event.input is typed as { command: string; timeout?: number }
    event.input.command = `source ~/.profile\n${event.input.command}`;
    if (event.input.command.includes("rm -rf"))
      return { block: true, reason: "Blocked" };
  }
});
```

### `tool_result`  ← **Can modify. Handlers chain.**
```typescript
import { isBashToolResult } from "@earendil-works/pi-coding-agent";
pi.on("tool_result", async (event, ctx) => {
  // event.toolName, event.toolCallId, event.input, event.content, event.details, event.isError
  // ctx.signal for abort-aware work
  return { content: [...], details: {...}, isError: false };  // partial patch OK
});
```

### `agent_start` / `agent_end` / `agent_settled`
```typescript
pi.on("agent_start", async (_event, ctx) => {});
pi.on("agent_end", async (event, ctx) => { /* event.messages */ });
pi.on("agent_settled", async (_event, ctx) => {
  // ctx.isIdle() is true here unless another extension started a new run
});
```

### `turn_start` / `turn_end`
```typescript
pi.on("turn_start", async (event, ctx) => { /* event.turnIndex, event.timestamp */ });
pi.on("turn_end", async (event, ctx) => { /* event.turnIndex, event.message, event.toolResults */ });
```

### `message_start` / `message_update` / `message_end`
```typescript
pi.on("message_start", async (event, ctx) => { /* event.message */ });
pi.on("message_update", async (event, ctx) => { /* event.message, event.assistantMessageEvent */ });
pi.on("message_end", async (event, ctx) => {
  if (event.message.role !== "assistant") return;
  return { message: { ...event.message } };  // replacement must keep same role
});
```

### `model_select`
```typescript
pi.on("model_select", async (event, ctx) => {
  // event.model, event.previousModel?, event.source: "set"|"cycle"|"restore"
});
```

### `thinking_level_select`
```typescript
pi.on("thinking_level_select", async (event, ctx) => {
  // event.level, event.previousLevel  (return values ignored)
});
```

### `user_bash`
```typescript
import { createLocalBashOperations } from "@earendil-works/pi-coding-agent";
pi.on("user_bash", (event, ctx) => {
  // event.command, event.excludeFromContext, event.cwd
  return { operations: customBashOps };
  // OR: return { result: { output, exitCode, cancelled, truncated } };
});
```
