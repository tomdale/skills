#!/usr/bin/env bash
# Node.js workspace provisioning for a raw Vercel Sandbox. Run INSIDE the sandbox
# after uploading this script and (optionally) a source archive.
# Required env: NODE_VERSION (e.g. 25.9.0), NPM_VERSION (e.g. 11.21.1).
# Optional env: WORKDIR (default /vercel/work), SOURCE_ARCHIVE (tar.gz extracted
# into $WORKDIR/source), INSTALL_DEPS (default 1: npm ci from the committed lockfile).
set -euo pipefail
NODE_VERSION=${NODE_VERSION:?set NODE_VERSION, e.g. 25.9.0}
NPM_VERSION=${NPM_VERSION:?set NPM_VERSION, e.g. 11.21.1}
WORKDIR=${WORKDIR:-/vercel/work}
INSTALL_DEPS=${INSTALL_DEPS:-1}
mkdir -p "$WORKDIR"/{logs,artifacts,tools}
exec > >(tee -a "$WORKDIR/logs/provision.log") 2>&1

case "$(uname -m)" in
  x86_64) NODE_TRIPLE=x64 ;;
  aarch64) NODE_TRIPLE=arm64 ;;
  *) echo "unsupported arch $(uname -m)" >&2; exit 1 ;;
esac

cd "$WORKDIR/tools"
curl -fsSLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$NODE_TRIPLE.tar.xz"
curl -fsSLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt"
grep " node-v$NODE_VERSION-linux-$NODE_TRIPLE.tar.xz$" SHASUMS256.txt | sha256sum -c -
tar -xf "node-v$NODE_VERSION-linux-$NODE_TRIPLE.tar.xz"
export PATH="$WORKDIR/tools/node-v$NODE_VERSION-linux-$NODE_TRIPLE/bin:$PATH"
npm install -g "npm@$NPM_VERSION"
node -v
npm -v

if [ -n "${SOURCE_ARCHIVE:-}" ]; then
  mkdir -p "$WORKDIR/source"
  tar -xzf "$SOURCE_ARCHIVE" -C "$WORKDIR/source"
fi

CHROME_PATH=""
if [ "$INSTALL_DEPS" = 1 ] && [ -f "$WORKDIR/source/package.json" ]; then
  cd "$WORKDIR/source"
  NPM_CONFIG_MIN_RELEASE_AGE=0 npm ci
  PW_VERSION=$(node -p "try { require('playwright-core/package.json').version } catch { '' }")
  if [ -n "$PW_VERSION" ]; then
    npx --yes "playwright@$PW_VERSION" install --with-deps chromium
    CHROME_PATH=$(node -p "require('playwright-core').chromium.executablePath()")
    "$CHROME_PATH" --version
  fi
fi

{
  printf 'export PATH=%q/bin:$PATH\n' "$WORKDIR/tools/node-v$NODE_VERSION-linux-$NODE_TRIPLE"
  if [ -n "$CHROME_PATH" ]; then printf 'export CHROME_PATH=%q\n' "$CHROME_PATH"; fi
} > "$WORKDIR/env.sh"
echo "provisioned: node $(node -v), npm $(npm -v); env file $WORKDIR/env.sh"
