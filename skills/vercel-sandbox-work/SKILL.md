---
name: vercel-sandbox-work
description: Provision and drive raw Vercel Sandbox Linux machines for isolated, reproducible work — benchmarks, test suites, native builds, browser automation — with the local agent orchestrating remotely through the @vercel/sandbox SDK. Use when asked to run tests or benchmarks on a clean Linux machine, provision a benchmark sandbox, prepare baseline-vs-optimized comparisons, or keep heavy experiments off the local machine.
---

# Vercel sandbox isolated work

A raw Vercel Sandbox is a disposable Linux machine the local agent drives command-by-command over the @vercel/sandbox SDK. It gives benchmarks and test runs a clean, pinned environment that touches no local state and dies on timeout, while orchestration stays in the local thread.

## Choose the provisioning path

Drive a raw SDK sandbox (this skill) whenever the local thread runs every command — the usual case for benchmarks and tests. Provision a BB machine instead (`bb machine create --provider vercel-sandbox`) only when the machine itself must host a BB thread; its enrollment bootstrap must reach the BB server, and a sandbox cannot resolve a private Tailscale DNS name, so enrollment fails whenever the BB server URL is a tailnet hostname. Use the raw SDK path; BB server access settings are live configuration shared by every BB thread, so do not change them to enroll one sandbox.

## Prerequisites and credentials

- `vc` CLI logged in (`vc whoami`). All authentication flows through the existing login; never start a separate one.
- Before allocating, confirm the account is ready and read capacity with two read-only commands: `bb vercel-sandbox account inspect --json` (teamId, projectId, login/OIDC readiness) and `bb vercel-sandbox launch options --json` (image `vercel/sandbox/universal:latest`, allowed vCPU sizes, timeout limits; memory is 2048 MiB per vCPU). The helper reads teamId/projectId from account inspect or from `VERCEL_TEAM_ID`/`VERCEL_PROJECT_ID` env vars.
- @vercel/sandbox SDK: run `npm install @vercel/sandbox` in a scratch directory and invoke the helper by absolute path from there, or set `VERCEL_SANDBOX_SDK` to the SDK's `dist/index.js`. The helper also falls back to the SDK copy inside the BB vercel-sandbox plugin checkout.

Token hygiene: the helper refreshes a project token per invocation via `vc api <endpoint> --method POST --raw` with endpoint `/v1/projects/<projectId>/token?source=vercel-oidc-refresh&teamId=<teamId>`; the token exists only in process memory and is redacted from error output. Keep anything built on top the same: tokens never appear in logs, reports, archives, or command arguments.

Known-broken listing paths (observed with vc 58.3.0, SDK 3.5.1): `vc sandbox list` segfaults under Node 22–25, and the Homebrew `sandbox` CLI authenticates separately (403). List with the helper's `list` action or `vc api '/v1/sandboxes?project=<projectId>' --scope <team> --raw`.

## The transport helper

`scripts/sandbox.mjs` (in this skill's directory) wraps the SDK. Set `HELPER` to its absolute path when invoking from elsewhere:

```sh
HELPER=<skill-dir>/scripts/sandbox.mjs
node "$HELPER" create NAME --vcpus 8 --timeout-minutes 90
node "$HELPER" exec NAME 'bash command'   # streams output; exits with the remote exit code
node "$HELPER" upload NAME /local/path /remote/path
node "$HELPER" download NAME /remote/path /local/path
node "$HELPER" info NAME                  # sessionId, status, expiresAt, vcpus, region
node "$HELPER" list
node "$HELPER" stop NAME
```

`Sandbox.get` uses `resume:false`, so an expired session errors instead of silently resurrecting. `info` reports `expiresAt = createdAt + timeout`: check it before long work, and size `--timeout-minutes` up front to cover install, runs, and artifact retrieval. Give local `exec` calls a generous timeout — a remote install routinely outruns a 90-second local cap, and remote work keeps going after the local call dies, so re-check state instead of assuming failure.

## Provisioning inside the sandbox

The sandbox user is `ubuntu` (uid 1000), not root, so browsers launch with no extra flags and product code needs no root-specific changes.

Layout convention: one workdir per purpose — `/vercel/<slug>/{logs,artifacts,tools,source}`, `/vercel/work` for a single workspace — with `exec > >(tee -a logs/provision.log) 2>&1` so setup failures stay on record.

`scripts/provision-node.sh` provisions a Node.js workspace. Upload it plus a source archive, then run it inside the sandbox:

```sh
node "$HELPER" upload NAME "$(dirname "$HELPER")/provision-node.sh" /vercel/work/provision-node.sh
node "$HELPER" upload NAME /path/to/source.tar.gz /vercel/work/source.tar.gz
node "$HELPER" exec NAME \
  'NODE_VERSION=25.9.0 NPM_VERSION=11.21.1 SOURCE_ARCHIVE=/vercel/work/source.tar.gz bash /vercel/work/provision-node.sh'
```

It pins a Node/npm pair matching the local machine (downloaded from nodejs.org, verified against SHASUMS256.txt), extracts the source archive, runs `NPM_CONFIG_MIN_RELEASE_AGE=0 npm ci` from the committed lockfile, and installs Playwright's Chromium with system deps when the lockfile contains playwright-core. It writes `env.sh` in the workdir; start every remote command by sourcing it (`source /vercel/work/env.sh` with the default `WORKDIR`) so nothing silently falls back to image defaults and browser tests cannot silently skip for a missing executable.

Beyond the template:

- Match the local runtime exactly — same Node and npm versions on both sides — and record `node -v`/`npm -v` in the verification log; benchmarks compare machines only when runtimes match.
- A green install of a native module proves nothing. Verify by requiring it and doing real work: better-sqlite3 → `new Database(':memory:').prepare('select 1').get()`.
- Browser: install the Chromium matching the lockfile's playwright-core (`npx --yes playwright@<core-version> install --with-deps chromium`), then sanity-launch headless once and print the browser version.

## Source snapshots and fair baselines

- Snapshot exact commits, never moving branches: `git archive --format=tar.gz --output=<file> <commit>`. For uncommitted work, tar the files from `git ls-files --cached --others --exclude-standard` minus deletions, excluding `.git`, `node_modules`, `dist`, and benchmark outputs.
- sha256 every archive locally and again after upload; record commits and hashes in a manifest JSON so the remote workspace is provably the intended source.
- For baseline-vs-optimized benchmarks, build both workspaces in one sandbox: same lockfile (compare sha256), same runtime, same install steps — only source differs.
- The sandbox is disposable verification: never push, deploy, or integrate from it, and never upload credentials inside archives. Transfer results out with `download` before expiry; anything left behind dies with the session.

## Verify before reporting ready

Run one verification command that captures `node -v; npm -v; id; lscpu; free -m; uname -a` — plus `"$CHROME_PATH" --version` and a headless launch when the workspace uses a browser, and a real native-module operation when the workspace has one — `tee` it to a remote log, and `download` it. Report the handoff explicitly: sandbox name, session ID, expiry, workspace paths, snapshot commits/hashes, runtime versions, env.sh path, and the exact local commands to run work and retrieve artifacts. Stop the sandbox with `stop NAME` when the work is done.
