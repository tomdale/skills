#!/usr/bin/env node
// Remote control for raw Vercel Sandbox instances through the @vercel/sandbox SDK.
// Authentication uses the local `vc` CLI login: a project token is refreshed per
// invocation and exists only in process memory, never in logs or arguments.
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { isAbsolute, resolve } from 'node:path';

function resolveSdkPath() {
  const candidates = [
    process.env.VERCEL_SANDBOX_SDK,
    'node_modules/@vercel/sandbox/dist/index.js',
    `${process.env.HOME}/Code/Repos/bb-vercel-sandbox/main/bb-plugin-vercel-sandbox/node_modules/@vercel/sandbox/dist/index.js`,
  ];
  for (const candidate of candidates) {
    if (!candidate) continue;
    const path = isAbsolute(candidate) ? candidate : resolve(process.cwd(), candidate);
    if (existsSync(path)) return path;
  }
  console.error(
    'No @vercel/sandbox SDK found. Run `npm install @vercel/sandbox` in a directory and invoke this script from there, or set VERCEL_SANDBOX_SDK to the SDK dist/index.js path.'
  );
  process.exit(2);
}

function parseArgs(argv) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        flags[key] = argv[++i];
      } else {
        flags[key] = true;
      }
    } else {
      positional.push(argv[i]);
    }
  }
  return { flags, positional };
}

function resolveAccount() {
  const teamId = process.env.VERCEL_TEAM_ID;
  const projectId = process.env.VERCEL_PROJECT_ID;
  if (teamId && projectId) return { teamId, projectId };
  try {
    const inspect = JSON.parse(
      execFileSync('bb', ['vercel-sandbox', 'account', 'inspect', '--json'], { encoding: 'utf8' })
    );
    return { teamId: teamId ?? inspect.teamId, projectId: projectId ?? inspect.projectId };
  } catch {
    console.error(
      'Set VERCEL_TEAM_ID and VERCEL_PROJECT_ID, or make `bb vercel-sandbox account inspect --json` resolve them.'
    );
    process.exit(2);
  }
}

function freshToken(account) {
  const endpoint = `/v1/projects/${account.projectId}/token?source=vercel-oidc-refresh&teamId=${account.teamId}`;
  const { token } = JSON.parse(
    execFileSync('vc', ['api', endpoint, '--method', 'POST', '--raw'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    })
  );
  return token;
}

const usage = `usage: sandbox.mjs <action> [args]
  create NAME [--vcpus N] [--timeout-minutes N] [--image IMAGE]
  exec NAME 'bash command'        streams output; exits with the remote exit code
  upload NAME /local/path /remote/path
  download NAME /remote/path /local/path
  info NAME                      sessionId, status, expiresAt, vcpus, region
  list                           up to 20 sandboxes in the account
  stop NAME`;

const { Sandbox } = await import(resolveSdkPath());
const [action, name, ...rest] = process.argv.slice(2);
const { flags, positional } = parseArgs(rest);
let token;

try {
  const account = resolveAccount();
  token = freshToken(account);
  const credentials = { token, ...account };

  if (action === 'list') {
    console.log(JSON.stringify(await Sandbox.list({ ...credentials, limit: 20 })));
  } else if (action === 'create') {
    if (!name) throw new Error(usage);
    const sandbox = await Sandbox.create({
      ...credentials,
      name,
      image: flags.image ?? 'vercel/sandbox/universal:latest',
      persistent: false,
      resources: { vcpus: Number(flags.vcpus ?? 8) },
      timeout: Number(flags['timeout-minutes'] ?? 90) * 60 * 1000,
    });
    console.log(JSON.stringify({ name: sandbox.name, sessionId: sandbox.currentSession().sessionId }));
  } else if (action === 'exec' || action === 'upload' || action === 'download' || action === 'info' || action === 'stop') {
    if (!name) throw new Error(usage);
    // resume:false: an expired session errors instead of silently resurrecting.
    const sandbox = await Sandbox.get({ ...credentials, name, resume: false });
    if (action === 'exec') {
      if (!positional[0]) throw new Error(usage);
      const result = await sandbox.runCommand({
        cmd: 'bash',
        args: ['-lc', positional[0]],
        stdout: process.stdout,
        stderr: process.stderr,
      });
      process.exitCode = result.exitCode;
    } else if (action === 'upload') {
      const [localPath, remotePath] = positional;
      if (!localPath || !remotePath) throw new Error(usage);
      await sandbox.writeFiles([{ path: remotePath, content: readFileSync(localPath) }]);
      console.log(JSON.stringify({ uploaded: remotePath }));
    } else if (action === 'download') {
      const [remotePath, localPath] = positional;
      if (!remotePath || !localPath) throw new Error(usage);
      const buffer = await sandbox.readFileToBuffer({ path: remotePath });
      if (!buffer) throw new Error(`missing remote file: ${remotePath}`);
      writeFileSync(localPath, buffer);
      console.log(JSON.stringify({ downloaded: localPath }));
    } else if (action === 'info') {
      const session = sandbox.currentSession();
      console.log(
        JSON.stringify({
          name: sandbox.name,
          sessionId: session.sessionId,
          status: session.status,
          createdAt: session.createdAt,
          expiresAt: new Date(session.createdAt.getTime() + session.timeout).toISOString(),
          vcpus: session.vcpus,
          memory: session.memory,
          region: session.region,
        })
      );
    } else {
      await sandbox.stop();
      console.log(JSON.stringify({ name, stopRequested: true }));
    }
  } else {
    throw new Error(usage);
  }
} catch (error) {
  console.error('Sandbox operation failed:', error.name ?? '', error.statusCode ?? '', String(error.message).replaceAll(token, '[redacted]'));
  process.exitCode = 1;
}
