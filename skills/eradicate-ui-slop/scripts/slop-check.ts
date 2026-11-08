#!/usr/bin/env node
/**
 * Check UI source files and screenshots for slop with a fast model.
 *
 * Usage: slop-check.ts [--review] [--model ID] [--jobs N] PATH [PATH ...]
 *
 * PATH may be a file or directory. Directories are walked for UI source
 * (HTML, CSS, JSX/TSX, Vue, Svelte, JS/TS, Markdown) and screenshots (PNG,
 * JPEG, WebP), skipping node_modules, dist, build, out, coverage, vendor and
 * dot-directories. Files are batched and each batch goes to one `pi -p` run
 * with SKILL.md and references/checker.md as the system prompt and no tools.
 *
 * --review   report patterns the existing product already uses (exception 2 off)
 * --model    model ID (default $SLOP_CHECK_MODEL or vercel-ai-gateway/openai/gpt-6-luna-fast)
 * --jobs     concurrent model runs (default 8)
 *
 * Prints `path:line | rule | quote | fix` per hit and `path | clean` per clean
 * file, then a count. Exits 1 when any hit was reported, 0 when every file is
 * clean, 2 on usage errors or when a model run failed.
 */

import { spawn } from "node:child_process";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { parseArgs } from "node:util";

const HERE = dirname(import.meta.filename);
const SKILL = join(HERE, "..", "SKILL.md");
const CHECKER = join(HERE, "..", "references", "checker.md");
const SOURCE = new Set([".html", ".htm", ".css", ".scss", ".sass", ".less", ".jsx", ".tsx", ".mdx",
  ".vue", ".svelte", ".js", ".mjs", ".ts", ".md", ".markdown"]);
const IMAGES = new Set([".png", ".jpg", ".jpeg", ".webp"]);
const SKIP_DIRS = new Set(["node_modules", "dist", "build", "out", "coverage", "vendor"]);
const BATCH_CHARS = 40000;
const BATCH_IMAGES = 4;
const TIMEOUT_MS = 600_000;
const DEFAULT_MODEL = "vercel-ai-gateway/openai/gpt-6-luna-fast";

type Batch = { texts: string[]; images: string[] };
type RunResult = { out: string; err: null } | { out: null; err: string };

/** The doc comment above, without comment markers; it is the help text. */
function docText(): string {
  const src = readFileSync(import.meta.filename, "utf8");
  const body = /\/\*\*\n([\s\S]*?)\n \*\//.exec(src)![1];
  return body.split("\n").map((l) => l.replace(/^ \*( |$)/, "")).join("\n");
}

/** Lowercased extension; a dotfile such as `.css` has none. */
function ext(p: string): string {
  const name = basename(p);
  const i = name.lastIndexOf(".");
  if (i <= 0 || /^\.+$/.test(name.slice(0, i + 1))) return "";
  return name.slice(i).toLowerCase();
}

function isDir(p: string): boolean {
  return statSync(p, { throwIfNoEntry: false })?.isDirectory() ?? false;
}

function isFile(p: string): boolean {
  return statSync(p, { throwIfNoEntry: false })?.isFile() ?? false;
}

/** Joins without normalising, so reported paths keep the caller's spelling. */
function joinPath(root: string, name: string): string {
  return root.endsWith("/") ? root + name : root + "/" + name;
}

/** Top-down walk in sorted order, files before subdirectories; symlinked directories are not entered. */
function walk(root: string, files: string[]): void {
  let entries;
  try {
    entries = readdirSync(root, { withFileTypes: true });
  } catch {
    return;
  }
  const dirs: string[] = [];
  const linkedDirs = new Set<string>();
  const names: string[] = [];
  for (const e of entries) {
    if (e.isDirectory()) dirs.push(e.name);
    else if (e.isSymbolicLink() && isDir(joinPath(root, e.name))) {
      dirs.push(e.name);
      linkedDirs.add(e.name);
    } else names.push(e.name);
  }
  for (const n of names.sort()) {
    const x = ext(n);
    if ((SOURCE.has(x) || IMAGES.has(x)) && !n.endsWith(".min.js") && !n.endsWith(".d.ts")) {
      files.push(joinPath(root, n));
    }
  }
  for (const d of dirs.filter((d) => !SKIP_DIRS.has(d) && !d.startsWith(".")).sort()) {
    if (!linkedDirs.has(d)) walk(joinPath(root, d), files);
  }
}

function collect(paths: string[]): string[] {
  const files: string[] = [];
  for (const p of paths) {
    if (isDir(p)) {
      walk(p, files);
    } else if (isFile(p)) {
      const x = ext(p);
      if (SOURCE.has(x) || IMAGES.has(x)) files.push(p);
      else console.error(`${p}: not checked (unsupported file type)`);
    } else {
      console.error(`${p}: no such file or directory`);
    }
  }
  return files;
}

function numbered(path: string): string {
  const lines = readFileSync(path, "utf8").split(/\r?\n/);
  if (lines.at(-1) === "") lines.pop();
  const body = lines.map((l, i) => `${i + 1}\t${l}`).join("\n");
  return `=== ${path} ===\n${body}\n`;
}

/** Text batches first, then image batches. Files larger than one batch go alone. */
function batches(files: string[]): Batch[] {
  const out: Batch[] = [];
  let texts: string[] = [];
  let size = 0;
  for (const f of files) {
    if (IMAGES.has(ext(f))) continue;
    const block = numbered(f);
    if (texts.length && size + block.length > BATCH_CHARS) {
      out.push({ texts, images: [] });
      texts = [];
      size = 0;
    }
    texts.push(block);
    size += block.length;
  }
  if (texts.length) out.push({ texts, images: [] });
  const imgs = files.filter((f) => IMAGES.has(ext(f)));
  for (let i = 0; i < imgs.length; i += BATCH_IMAGES) {
    out.push({ texts: [], images: imgs.slice(i, i + BATCH_IMAGES) });
  }
  return out;
}

function run(batch: Batch, model: string, review: boolean): Promise<RunResult> {
  const mode = review ? "review" : "edit";
  let header = `Run: ${mode}. Check every file below.\n`;
  if (batch.images.length) header += `Screenshots: ${batch.images.join(", ")}\n`;
  const args = ["-p", "--no-session", "-nt", "-ne", "-ns", "-nc", "-np", "--no-mcp",
    "--no-themes", "--model", model,
    "--append-system-prompt", SKILL, "--append-system-prompt", CHECKER,
    ...batch.images.map((i) => "@" + resolve(i)),
    header + batch.texts.join("\n")];
  return new Promise((done) => {
    const child = spawn("pi", args, { stdio: ["inherit", "pipe", "pipe"], timeout: TIMEOUT_MS });
    const stdout: Buffer[] = [];
    const stderr: Buffer[] = [];
    let timedOut = false;
    let spawnError: Error | null = null;
    child.stdout.on("data", (b: Buffer) => stdout.push(b));
    child.stderr.on("data", (b: Buffer) => stderr.push(b));
    child.on("error", (e) => {
      spawnError = e;
    });
    child.on("exit", (_code, signal) => {
      if (signal === "SIGTERM" && child.killed) timedOut = true;
    });
    child.on("close", (code) => {
      if (spawnError) return done({ out: null, err: `pi failed: ${spawnError.message}` });
      if (timedOut) return done({ out: null, err: `pi failed: timed out after ${TIMEOUT_MS / 1000} seconds` });
      if (code !== 0) {
        const tail = Buffer.concat(stderr).toString("utf8").trim().slice(-500);
        return done({ out: null, err: tail });
      }
      done({ out: Buffer.concat(stdout).toString("utf8"), err: null });
    });
  });
}

function usageError(msg: string): number {
  console.error(`${msg}\n\n${docText().trim()}`);
  return 2;
}

async function main(): Promise<number> {
  let values, positionals;
  try {
    ({ values, positionals } = parseArgs({
      allowPositionals: true,
      options: {
        review: { type: "boolean" },
        model: { type: "string" },
        jobs: { type: "string" },
        help: { type: "boolean", short: "h" },
      },
    }));
  } catch (e) {
    return usageError((e as Error).message);
  }
  if (values.help || !positionals.length) {
    console.log(docText().trim());
    return 2;
  }
  const model = values.model ?? process.env.SLOP_CHECK_MODEL ?? DEFAULT_MODEL;
  let jobs = 8;
  if (values.jobs !== undefined) {
    jobs = Number(values.jobs);
    if (!Number.isInteger(jobs) || jobs < 1) return usageError(`--jobs must be a positive integer, got '${values.jobs}'`);
  }
  const files = collect(positionals);
  if (!files.length) {
    console.error("no supported files found");
    return 2;
  }
  const work = batches(files);

  // Run at most `jobs` batches at once; report results in batch order.
  const results: Promise<RunResult>[] = new Array(work.length);
  const resolvers: ((r: RunResult) => void)[] = [];
  for (let i = 0; i < work.length; i++) results[i] = new Promise((r) => (resolvers[i] = r));
  let next = 0;
  const worker = async () => {
    while (next < work.length) {
      const i = next++;
      resolvers[i](await run(work[i], model, values.review ?? false));
    }
  };
  for (let w = 0; w < Math.min(jobs, work.length); w++) void worker();

  let hits = 0;
  let failed = 0;
  for (const p of results) {
    const r = await p;
    if (r.err !== null) {
      failed++;
      console.error(`model run failed: ${r.err}`);
      continue;
    }
    for (const raw of r.out.split("\n")) {
      const line = raw.trim().replace(/^`+|`+$/g, "");
      if (!line || !line.includes("|")) continue;
      console.log(line);
      if (!line.endsWith("| clean")) hits++;
    }
  }
  console.log(`\n${files.length} files in ${work.length} batches, ${hits} hits${failed ? `, ${failed} batches failed` : ""}`);
  if (failed) return 2;
  return hits ? 1 : 0;
}

process.stdout.on("error", (e: Error & { code?: string }) => {
  if (e.code === "EPIPE") process.exit(1);
  throw e;
});
process.exitCode = await main();
