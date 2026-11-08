#!/usr/bin/env python3
"""Check UI source files and screenshots for slop with a fast model.

Usage: slop-check.py [--review] [--model ID] [--jobs N] PATH [PATH ...]

PATH may be a file or directory. Directories are walked for UI source
(HTML, CSS, JSX/TSX, Vue, Svelte, JS/TS, Markdown) and screenshots (PNG,
JPEG, WebP), skipping node_modules, dist, build, out, coverage, vendor and
dot-directories. Files are batched and each batch goes to one `pi -p` run
with SKILL.md and references/checker.md as the system prompt and no tools.

--review   report patterns the existing product already uses (exception 2 off)
--model    model ID (default $SLOP_CHECK_MODEL or vercel-ai-gateway/openai/gpt-6-luna-fast)
--jobs     concurrent model runs (default 8)

Prints `path:line | tell | quote | fix` per hit and `path | clean` per clean
file, then a count. Exits 1 when any hit was reported, 0 when every file is
clean, 2 on usage errors or when a model run failed.
"""

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "SKILL.md")
CHECKER = os.path.join(HERE, "..", "references", "checker.md")
SOURCE = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".jsx", ".tsx", ".mdx",
          ".vue", ".svelte", ".js", ".mjs", ".ts", ".md", ".markdown"}
IMAGES = {".png", ".jpg", ".jpeg", ".webp"}
SKIP_DIRS = {"node_modules", "dist", "build", "out", "coverage", "vendor"}
BATCH_CHARS = 40000
BATCH_IMAGES = 4


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
                for n in sorted(names):
                    ext = os.path.splitext(n)[1].lower()
                    if (ext in SOURCE or ext in IMAGES) and not n.endswith((".min.js", ".d.ts")):
                        files.append(os.path.join(root, n))
        elif os.path.isfile(p):
            ext = os.path.splitext(p)[1].lower()
            if ext in SOURCE or ext in IMAGES:
                files.append(p)
            else:
                print("%s: not checked (unsupported file type)" % p, file=sys.stderr)
        else:
            print("%s: no such file or directory" % p, file=sys.stderr)
    return files


def numbered(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    body = "\n".join("%d\t%s" % (i, l) for i, l in enumerate(lines, 1))
    return "=== %s ===\n%s\n" % (path, body)


def batches(files):
    """Yield (text_blocks, images). Files larger than one batch go alone."""
    texts, size = [], 0
    for f in files:
        if os.path.splitext(f)[1].lower() in IMAGES:
            continue
        block = numbered(f)
        if texts and size + len(block) > BATCH_CHARS:
            yield texts, []
            texts, size = [], 0
        texts.append(block)
        size += len(block)
    if texts:
        yield texts, []
    imgs = [f for f in files if os.path.splitext(f)[1].lower() in IMAGES]
    for i in range(0, len(imgs), BATCH_IMAGES):
        yield [], imgs[i:i + BATCH_IMAGES]


def run(batch, model, review):
    texts, imgs = batch
    mode = "review" if review else "edit"
    header = "Run: %s. Check every file below.\n" % mode
    if imgs:
        header += "Screenshots: %s\n" % ", ".join(imgs)
    cmd = ["pi", "-p", "--no-session", "-nt", "-ne", "-ns", "-nc", "-np", "--no-mcp",
           "--no-themes", "--model", model,
           "--append-system-prompt", SKILL, "--append-system-prompt", CHECKER]
    cmd += ["@" + os.path.abspath(i) for i in imgs]
    cmd += [header + "\n".join(texts)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except (OSError, subprocess.TimeoutExpired) as err:
        return None, "pi failed: %s" % err
    if out.returncode != 0:
        return None, out.stderr.strip()[-500:]
    return out.stdout, None


def main():
    ap = argparse.ArgumentParser(add_help=True, usage=__doc__.split("\n\n")[1])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--review", action="store_true")
    ap.add_argument("--model", default=os.environ.get("SLOP_CHECK_MODEL", "vercel-ai-gateway/openai/gpt-6-luna-fast"))
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    if not args.paths:
        print(__doc__.strip())
        return 2
    files = collect(args.paths)
    if not files:
        print("no supported files found", file=sys.stderr)
        return 2
    work = list(batches(files))
    hits = failed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for out, err in pool.map(lambda b: run(b, args.model, args.review), work):
            if err is not None:
                failed += 1
                print("model run failed: %s" % err, file=sys.stderr)
                continue
            for line in out.splitlines():
                line = line.strip().strip("`")
                if not line or "|" not in line:
                    continue
                print(line)
                if not line.endswith("| clean"):
                    hits += 1
    print("\n%d files in %d batches, %d hits%s" % (
        len(files), len(work), hits, ", %d batches failed" % failed if failed else ""))
    if failed:
        return 2
    return 1 if hits else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(1)
