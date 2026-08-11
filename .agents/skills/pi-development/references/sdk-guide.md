# SDK Integration Guide

> Source: `docs/sdk.md` + `examples/sdk/` (v0.79.x)  
> Install: `npm install @earendil-works/pi-coding-agent`

## Quick Start

```typescript
import { AuthStorage, createAgentSession, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";

const auth = AuthStorage.create();                             // reads ~/.pi/agent/auth.json
const { session } = await createAgentSession({
  authStorage: auth,
  modelRegistry: ModelRegistry.create(auth),                  // built-in + custom models
  sessionManager: SessionManager.inMemory(),                  // no persistence
});

session.subscribe((event) => {
  if (event.type === "message_update" && event.assistantMessageEvent.type === "text_delta")
    process.stdout.write(event.assistantMessageEvent.delta);
  if (event.type === "tool_execution_start") console.error(`[tool] ${event.toolName}`);
});

await session.prompt("What files are here?");
session.dispose();
```

## createAgentSession() Options

```typescript
const { session, extensionsResult, modelFallbackMessage } = await createAgentSession({
  // Directory context
  cwd: process.cwd(),            // for resource discovery and tool path resolution
  agentDir: "~/.pi/agent",       // global config dir (expands ~)

  // Model
  model: getModel("anthropic", "claude-opus-4-5"),  // or: modelRegistry.find(provider, id)
  thinkingLevel: "medium",       // "off"|"minimal"|"low"|"medium"|"high"|"xhigh"|"max"
  scopedModels: [{ model, thinkingLevel }],  // for Ctrl+P cycling in interactive mode

  // Auth
  authStorage: AuthStorage.create(),
  modelRegistry: ModelRegistry.create(authStorage),

  // Tools
  tools: ["read", "bash", "grep"],  // allowlist; defaults: read, bash, edit, write
  excludeTools: ["bash"],            // disable specific tools; applied after allowlist
  noTools: "builtin",               // "all" | "builtin" (keeps extension tools)
  customTools: [myTool],            // pass defineTool() results

  // Resources
  resourceLoader: myLoader,         // DefaultResourceLoader or custom ResourceLoader

  // Sessions
  sessionManager: SessionManager.create(cwd),

  // Settings
  settingsManager: SettingsManager.inMemory({ compaction: { enabled: false } }),
});
```

If no model is provided: tries to restore from session → uses settings default → first available.

## AgentSession API

```typescript
session.prompt(text: string, options?: {
  expandPromptTemplates?: boolean;
  images?: ImageContent[];
  streamingBehavior?: "steer" | "followUp";
  source?: InputSource;
  preflightResult?: (success: boolean) => void;
}): Promise<void>

session.steer(text: string): Promise<void>    // queue during streaming (after current tool batch)
session.followUp(text: string): Promise<void> // queue until agent fully done

session.subscribe(listener: (event: AgentSessionEvent) => void): () => void  // returns unsubscribe
session.abort(): Promise<void>
session.dispose(): void

session.navigateTree(targetId: string, options?: { summarize?, customInstructions?, label? }): Promise<{ editorText?, cancelled }>
session.compact(customInstructions?: string): Promise<CompactionResult>

// State
session.sessionFile: string | undefined
session.sessionId: string
session.model: Model | undefined
session.thinkingLevel: ThinkingLevel
session.messages: AgentMessage[]
session.isStreaming: boolean
session.agent: Agent  // low-level access; session.agent.state.messages, .tools, .model
```

## AgentSessionEvent Types

```typescript
// Streaming
{ type: "message_update"; message; assistantMessageEvent: { type: "text_delta"; delta: string }
  | { type: "thinking_delta"; delta: string } | ... }

// Tool execution
{ type: "tool_execution_start"; toolCallId; toolName; args }
{ type: "tool_execution_update"; toolCallId; toolName; partialResult }
{ type: "tool_execution_end"; toolCallId; toolName; result; isError }

// Lifecycle
{ type: "message_start" | "message_end"; message }
{ type: "agent_start" | "agent_end"; messages? }
{ type: "turn_start"; turnIndex; timestamp }
{ type: "turn_end"; turnIndex; message; toolResults }

// Session ops
{ type: "queue_update"; steering: string[]; followUp: string[] }
{ type: "compaction_start" | "compaction_end" }
{ type: "auto_retry_start" | "auto_retry_end" }
```

## DefaultResourceLoader

```typescript
import { DefaultResourceLoader } from "@earendil-works/pi-coding-agent";

const loader = new DefaultResourceLoader({
  cwd,
  agentDir: getAgentDir(),       // ~/.pi/agent
  settingsManager,

  // Override system prompt
  systemPromptOverride: () => "You are a minimal assistant.",

  // Inject additional extension paths or inline factories
  additionalExtensionPaths: ["/path/to/my-extension.ts"],
  extensionFactories: [
    (pi) => { pi.on("agent_start", () => console.log("starting")); },
    { name: "my-ext", factory: (pi) => { /* ... */ } },  // named for display
  ],

  // Override skills, prompts, context files
  skillsOverride: (current) => ({
    skills: [...current.skills, { name: "custom", description: "...", filePath: "/path/SKILL.md",
      baseDir: "/path", source: "custom" }],
    diagnostics: current.diagnostics,
  }),
  promptsOverride: (current) => ({
    prompts: [...current.prompts, { name: "deploy", description: "Deploy",
      source: "(custom)", content: "# Deploy\n..." }],
    diagnostics: current.diagnostics,
  }),
  agentsFilesOverride: (current) => ({
    agentsFiles: [...current.agentsFiles,
      { path: "/virtual/AGENTS.md", content: "# Guidelines\n- Be concise" }],
  }),

  // Shared event bus for inter-extension communication from outside
  eventBus,
});
await loader.reload();  // must call before use

const extensions = loader.getExtensions();
const skills = loader.getSkills();
const prompts = loader.getPrompts();
const contextFiles = loader.getAgentsFiles().agentsFiles;
```

**Event bus:**
```typescript
import { createEventBus } from "@earendil-works/pi-coding-agent";
const eventBus = createEventBus();
const loader = new DefaultResourceLoader({ eventBus });
eventBus.on("my-ext:status", (data) => console.log(data));
```

## Auth and Models

```typescript
// API key resolution order: setRuntimeApiKey → auth.json → env vars → fallback resolver
const auth = AuthStorage.create();                     // ~/.pi/agent/auth.json
const auth = AuthStorage.create("/custom/auth.json");  // custom path
auth.setRuntimeApiKey("anthropic", "sk-ant-...");      // override for this process (not persisted)

const registry = ModelRegistry.create(auth);           // uses ~/.pi/agent/models.json for custom models
const registry = ModelRegistry.create(auth, "/custom/models.json");
const registry = ModelRegistry.inMemory(auth);         // built-in models only

// Find models
import { getModel } from "@earendil-works/pi-ai";
const model = getModel("anthropic", "claude-opus-4-5");  // doesn't check API key
const model = registry.find("anthropic", "claude-opus-4-5");  // includes custom models
const available = await registry.getAvailable();        // only models with valid API keys

// CLI-style model parsing
import { resolveCliModel, resolveModelScopeWithDiagnostics } from "@earendil-works/pi-coding-agent";
const { model, error, warning } = resolveCliModel({ cliModel: "anthropic/claude-opus-4-5:high", registry });
const { scopedModels, diagnostics } = await resolveModelScopeWithDiagnostics(["claude-*:high", "gpt-5"], registry);
```

## Session Management

```typescript
import { SessionManager } from "@earendil-works/pi-coding-agent";

SessionManager.inMemory()                    // no persistence; optional cwd
SessionManager.create(cwd)                   // new session in cwd's sessions dir
SessionManager.continueRecent(cwd)           // most recent session for cwd
SessionManager.open("/path/to/session.jsonl") // specific file

// Listing
await SessionManager.list(cwd)               // sessions for this cwd
await SessionManager.listAll(cwd)            // all sessions

// Tree API (on instance)
sm.getEntries()          // all entries (excludes header)
sm.getBranch()           // active branch entries
sm.buildContextEntries() // with compaction applied
sm.getTree()             // full tree structure
sm.getLeafEntry()        // current leaf
sm.getEntry(id)          // by ID
sm.getChildren(id)       // direct children
sm.getLabel(id)          // label string or undefined
sm.branch(entryId)       // navigate to earlier entry
sm.branchWithSummary(id, summary)
sm.createBranchedSession(leafId)  // extract path to new file
```

## Session Replacement (newSession / switchSession / fork)

For workflows that need session switching, use `createAgentSessionRuntime()`:

```typescript
import {
  type CreateAgentSessionRuntimeFactory,
  createAgentSessionFromServices, createAgentSessionRuntime, createAgentSessionServices,
  getAgentDir, SessionManager,
} from "@earendil-works/pi-coding-agent";

const createRuntime: CreateAgentSessionRuntimeFactory = async ({ cwd, sessionManager, sessionStartEvent }) => {
  const services = await createAgentSessionServices({ cwd });
  return {
    ...(await createAgentSessionFromServices({ services, sessionManager, sessionStartEvent })),
    services, diagnostics: services.diagnostics,
  };
};

const runtime = await createAgentSessionRuntime(createRuntime, {
  cwd: process.cwd(), agentDir: getAgentDir(),
  sessionManager: SessionManager.create(process.cwd()),
});

// runtime.session changes after replacement; re-subscribe after each replacement
let { session } = runtime;
let unsub = session.subscribe(handleEvent);

await runtime.newSession();           // creates new session
await runtime.switchSession(path);    // opens existing session
await runtime.fork("entry-id");       // fork before entry
await runtime.fork("entry-id", { position: "at" });  // clone through entry
await runtime.importFromJsonl(path);  // import session

unsub(); session = runtime.session; unsub = session.subscribe(handleEvent);  // re-subscribe
```

## SettingsManager

```typescript
import { SettingsManager } from "@earendil-works/pi-coding-agent";

SettingsManager.create()                         // load from files (global + project merge)
SettingsManager.create(cwd, agentDir)            // custom paths
SettingsManager.inMemory({ compaction: {...} })  // no I/O (testing)

const sm = SettingsManager.create();
sm.applyOverrides({ compaction: { enabled: false }, retry: { maxRetries: 5 } });
await sm.flush();   // flush pending writes (before process exit or in tests)
sm.drainErrors();   // get and clear any I/O errors
```

## Run Modes (SDK)

```typescript
import { InteractiveMode, runPrintMode, runRpcMode } from "@earendil-works/pi-coding-agent";

// Full TUI interactive mode
const mode = new InteractiveMode(runtime, {
  initialMessage: "Hello", initialImages: [], initialMessages: [],
  migratedProviders: [], modelFallbackMessage: undefined,
});
await mode.run();

// Print mode: send prompts, output to stdout, exit
await runPrintMode(runtime, {
  mode: "text",  // or "json"
  initialMessage: "Hello", initialImages: [],
  messages: ["Follow up"],
});

// RPC mode: JSON-RPC protocol on stdin/stdout
await runRpcMode(runtime);
```

See `docs/rpc.md` for the RPC protocol.

## Tool Collections

```typescript
import { createCodingTools, createReadOnlyTools } from "@earendil-works/pi-coding-agent";
// createCodingTools(cwd) → [read, bash, edit, write]  (default set)
// createReadOnlyTools(cwd) → [read, grep, find, ls]
```

## Exports Reference

Key types: `CreateAgentSessionOptions`, `CreateAgentSessionResult`, `AgentSession`, `AgentSessionEvent`, `ExtensionFactory`, `InlineExtension`, `ExtensionAPI`, `ToolDefinition`, `Skill`, `PromptTemplate`, `Tool`, `Model`, `ThinkingLevel`.

Key constants: `CONFIG_DIR_NAME`, `getAgentDir()`, `getPackageDir()`, `getReadmePath()`, `getDocsPath()`, `getExamplesPath()`.
