# Extension API Reference

> Source: `docs/extensions.md` (v0.79.x)

## `pi.*` Methods (ExtensionAPI)

### Registration

```typescript
pi.on(event: string, handler: Function): void
// Subscribe to lifecycle events (see extension-events.md)

pi.registerTool(definition: ToolDefinition): void
// Register a custom LLM-callable tool. Can be called after startup; tools go live immediately.

pi.registerCommand(name: string, options: {
  description?: string;
  getArgumentCompletions?: (prefix: string) => AutocompleteItem[] | null;
  handler: (args: string, ctx: ExtensionCommandContext) => Promise<void>;
}): void

pi.registerShortcut(shortcut: string, options: {
  description?: string;
  handler: (ctx: ExtensionContext) => Promise<void>;
}): void

pi.registerFlag(name: string, options: {
  description?: string;
  type: "boolean" | "string";
  default?: unknown;
}): void

pi.registerProvider(name: string, config: ProviderConfig): void
// Register or override a model provider. Queued during factory; immediate after startup.
// config: { name?, baseUrl, apiKey, api, headers?, authHeader?, models?, oauth?, streamSimple? }

pi.unregisterProvider(name: string): void

pi.registerMessageRenderer(customType: string, renderer: MessageRenderer): void
// Custom TUI renderer for messages created with pi.sendMessage() (participate in LLM context)

pi.registerEntryRenderer(customType: string, renderer: EntryRenderer): void
// Custom TUI renderer for entries created with pi.appendEntry() (not in LLM context)
```

### Messaging

```typescript
pi.sendMessage(message: {
  customType: string;
  content: string;
  display?: boolean;
  details?: unknown;
}, options?: {
  triggerTurn?: boolean;  // trigger LLM response if idle
  deliverAs?: "steer" | "followUp" | "nextTurn";
}): void

pi.sendUserMessage(content: string | ContentPart[], options?: {
  deliverAs?: "steer" | "followUp";  // required when streaming
}): void
// Sends as if typed by user. Always triggers a turn.

pi.appendEntry(customType: string, data?: unknown): void
// Persist extension data to session (not in LLM context). Pair with registerEntryRenderer().
```

### Tools

```typescript
pi.getActiveTools(): string[]
pi.getAllTools(): Array<{
  name: string; description: string; parameters: unknown;
  promptGuidelines?: string[];
  sourceInfo: { path: string; source: string; scope: string; origin: string };
}>
pi.setActiveTools(names: string[]): void
// Dynamic tool loading: additive changes use deferred loading on supported models (Anthropic 4.5+, OpenAI gpt-5.4+)
```

### Session & State

```typescript
pi.setSessionName(name: string): void
pi.getSessionName(): string | undefined
pi.setLabel(entryId: string, label: string | undefined): void
pi.getCommands(): Array<{
  name: string; description?: string; source: string;
  sourceInfo: { path: string; source: string; scope: string; origin: string; baseDir?: string };
}>
```

### Model

```typescript
pi.setModel(model: Model): Promise<boolean>  // false if no API key
pi.getThinkingLevel(): ThinkingLevel
pi.setThinkingLevel(level: ThinkingLevel): void
// ThinkingLevel: "off" | "minimal" | "low" | "medium" | "high" | "xhigh" | "max"
```

### Utilities

```typescript
pi.exec(command: string, args: string[], options?: { signal?: AbortSignal; timeout?: number }):
  Promise<{ stdout: string; stderr: string; code: number; killed: boolean }>

pi.getFlag(name: string): unknown

pi.events: EventEmitter  // inter-extension event bus
// pi.events.on("my:event", handler)
// pi.events.emit("my:event", data)
```

---

## `ctx.*` (ExtensionContext)

Available in all event handlers.

```typescript
ctx.ui          // UI methods (see below)
ctx.mode        // "tui" | "rpc" | "json" | "print"
ctx.hasUI       // true in tui and rpc modes
ctx.cwd         // current working directory (string)
ctx.signal      // AbortSignal | undefined (active during tool/turn events)
ctx.model       // current Model | undefined
ctx.modelRegistry  // ModelRegistry
ctx.sessionManager // read-only session access

ctx.isIdle(): boolean
ctx.abort(): Promise<void>
ctx.hasPendingMessages(): boolean
ctx.compact(options?: {
  customInstructions?: string;
  onComplete?: (result: CompactionResult) => void;
  onError?: (error: Error) => void;
}): void
ctx.getContextUsage(): { tokens: number; maxTokens: number } | undefined
ctx.getSystemPrompt(): string
ctx.isProjectTrusted(): boolean
ctx.shutdown(): void  // graceful shutdown; deferred in interactive/rpc until idle
```

### `ctx.ui.*`

```typescript
ctx.ui.notify(message: string, level: "info" | "warning" | "error"): void
ctx.ui.confirm(title: string, message: string, opts?: { timeout?: number; signal?: AbortSignal }): Promise<boolean>
ctx.ui.select(title: string, items: string[], opts?: { timeout?: number; signal?: AbortSignal }): Promise<string | undefined>
ctx.ui.input(title: string, placeholder?: string, opts?: { timeout?: number; signal?: AbortSignal }): Promise<string | undefined>
ctx.ui.editor(title: string, prefill?: string): Promise<string | undefined>

ctx.ui.setStatus(key: string, text: string | undefined): void   // footer status; clear with undefined
ctx.ui.setWidget(key: string, content: string[] | ((tui, theme) => Component) | undefined,
  opts?: { placement?: "aboveEditor" | "belowEditor" }): void
ctx.ui.setFooter(fn: ((tui, theme) => FooterComponent) | undefined): void
ctx.ui.setTitle(title: string): void
ctx.ui.setEditorText(text: string): void
ctx.ui.getEditorText(): string
ctx.ui.pasteToEditor(content: string): void
ctx.ui.setToolsExpanded(expanded: boolean): void
ctx.ui.getToolsExpanded(): boolean

ctx.ui.setWorkingMessage(message?: string): void     // streaming loader text; undefined = restore default
ctx.ui.setWorkingVisible(visible: boolean): void      // hide/show loader row
ctx.ui.setWorkingIndicator(opts?: { frames: string[]; intervalMs?: number }): void  // spinner frames

ctx.ui.setEditorComponent(factory: ((tui, theme, keybindings) => Component) | undefined): void
ctx.ui.getEditorComponent(): ((tui, theme, keybindings) => Component) | undefined

ctx.ui.addAutocompleteProvider(provider: (current: AutocompleteProvider) => AutocompleteProvider): void
// Stack custom completion logic; delegate to `current` for default behavior

ctx.ui.getAllThemes(): Array<{ name: string; path: string | undefined }>
ctx.ui.getTheme(name: string): Theme | undefined
ctx.ui.setTheme(nameOrTheme: string | Theme): { success: boolean; error?: string }
ctx.ui.theme  // current Theme object; theme.fg(color, text), theme.bg(color, text), theme.bold(text)

ctx.ui.custom<T>(
  factory: (tui, theme, keybindings, done: (value: T) => void) => Component,
  opts?: {
    overlay?: boolean;
    overlayOptions?: { anchor?: string; width?: string | number; margin?: number };
    onHandle?: (handle: OverlayHandle) => void;
  }
): Promise<T>
// Temporarily replaces (or overlays) the editor with a custom TUI component.
// TUI mode only. Check ctx.mode === "tui" before calling.
```

---

## `ctx.*` (ExtensionCommandContext)

Everything in `ExtensionContext`, plus session control. **Only available in command handlers** (to avoid deadlocks in event handlers).

```typescript
ctx.getSystemPromptOptions(): SystemPromptOptions
// { customPrompt, selectedTools, toolSnippets, promptGuidelines, appendSystemPrompt, cwd, contextFiles, skills }

ctx.waitForIdle(): Promise<void>

ctx.newSession(options?: {
  parentSession?: string;
  setup?: (sm: SessionManager) => void | Promise<void>;
  withSession?: (ctx: ReplacedSessionContext) => Promise<void>;
}): Promise<{ cancelled: boolean }>

ctx.fork(entryId: string, options?: {
  position?: "before" | "at";
  withSession?: (ctx: ReplacedSessionContext) => Promise<void>;
}): Promise<{ cancelled: boolean }>

ctx.navigateTree(targetId: string, options?: {
  summarize?: boolean;
  customInstructions?: string;
  replaceInstructions?: boolean;
  label?: string;
}): Promise<{ editorText?: string; cancelled: boolean }>

ctx.switchSession(sessionPath: string, options?: {
  withSession?: (ctx: ReplacedSessionContext) => Promise<void>;
}): Promise<{ cancelled: boolean }>

ctx.reload(): Promise<void>
// Avoid: code after await ctx.reload() still runs from pre-reload version. Treat as terminal.
```

### `ReplacedSessionContext` (in `withSession`)

Extends `ExtensionCommandContext` with:
```typescript
ctx.sendMessage(message, options?): void
ctx.sendUserMessage(content, options?): Promise<void>
```

**⚠ Warning:** `withSession` runs after old session is torn down and new session has started. Do NOT use captured old `pi` or old command `ctx`. Use only the fresh `ctx` passed to `withSession`.

---

## `ctx.sessionManager` (read-only)

```typescript
ctx.sessionManager.getEntries(): SessionEntry[]
ctx.sessionManager.getBranch(): SessionEntry[]   // active branch
ctx.sessionManager.buildContextEntries(): SessionEntry[]  // with compaction applied
ctx.sessionManager.getLeafId(): string
ctx.sessionManager.getSessionFile(): string | undefined
ctx.sessionManager.getSessionId(): string
ctx.sessionManager.getLabel(entryId: string): string | undefined

// Static (import SessionManager):
SessionManager.list(cwd: string): Promise<SessionInfo[]>
SessionManager.listAll(cwd: string): Promise<SessionInfo[]>
```

---

## `CONFIG_DIR_NAME`

```typescript
import { CONFIG_DIR_NAME } from "@earendil-works/pi-coding-agent";
// Always use this instead of hardcoding ".pi" — rebranded distributions may differ.
const projectConfig = join(ctx.cwd, CONFIG_DIR_NAME, "my-extension.json");
```

---

## Tool Rendering Helpers

```typescript
import { keyHint, keyText, rawKeyHint } from "@earendil-works/pi-coding-agent";
// Use in renderCall / renderResult:
keyHint("app.tools.expand", "to expand")  // → "(ctrl+o to expand)"
keyText("app.tools.expand")               // → "ctrl+o"
```

Keybinding namespaces: `app.*` (coding-agent), `tui.*` (shared TUI). See `docs/keybindings.md`.
