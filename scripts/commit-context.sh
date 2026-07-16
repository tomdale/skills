#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: commit-context.sh [repo-path]

Print compact repository context for commit workflows:
- repository and branch state
- applicable instruction files
- staged, unstaged, and untracked paths with diff stats
- recent commit subjects
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

repo_path="${1:-$PWD}"
if [[ ! -d "$repo_path" ]]; then
  echo "error: repo path does not exist: $repo_path" >&2
  exit 1
fi

cd "$repo_path"
if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "error: not a git repository: $repo_path" >&2
  exit 1
fi

repo_root="$(git rev-parse --show-toplevel)"
branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || printf 'DETACHED')"
upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || printf 'none')"
remote="$(git remote | head -n1 || true)"

resolve_base() {
  local candidate=""
  if [[ -n "$remote" ]]; then
    candidate="$(git symbolic-ref --quiet --short "refs/remotes/$remote/HEAD" 2>/dev/null || true)"
    candidate="${candidate#"$remote/"}"
  fi
  if [[ -z "$candidate" ]] && git show-ref --verify --quiet refs/heads/main; then candidate="main"; fi
  if [[ -z "$candidate" ]] && git show-ref --verify --quiet refs/heads/master; then candidate="master"; fi
  printf '%s' "$candidate"
}

base="$(resolve_base)"
base_ref=""
if [[ -n "$base" && -n "$remote" ]] && git show-ref --verify --quiet "refs/remotes/$remote/$base"; then
  base_ref="$remote/$base"
elif [[ -n "$base" ]] && git show-ref --verify --quiet "refs/heads/$base"; then
  base_ref="$base"
fi

echo "repo_root=$repo_root"
echo "branch=$branch"
echo "upstream=$upstream"
echo "base=${base_ref:-unknown}"
if [[ -n "$base_ref" ]]; then
  counts="$(git rev-list --left-right --count "$base_ref...HEAD" 2>/dev/null || true)"
  echo "ahead_behind=${counts:-unknown}"
fi

echo
echo '== applicable instruction files =='
path="$PWD"
while [[ "$path" == "$repo_root" || "$path" == "$repo_root"/* ]]; do
  for name in AGENTS.md CLAUDE.md; do
    [[ -f "$path/$name" ]] && printf '%s\n' "$path/$name"
  done
  [[ "$path" == "$repo_root" ]] && break
  path="$(dirname "$path")"
done

echo
echo '== status =='
git status --short --branch

echo
echo '== staged paths =='
git diff --cached --name-status
echo
echo '== staged stats =='
git diff --cached --stat
echo
echo '== unstaged paths =='
git diff --name-status
echo
echo '== unstaged stats =='
git diff --stat
echo
echo '== untracked paths =='
git ls-files --others --exclude-standard
echo
echo '== recent commits =='
git log --oneline --decorate -10
