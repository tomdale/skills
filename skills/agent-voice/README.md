# agent-voice and voicecheck

The agent-voice skill describes the writing standard. `scripts/voicecheck` checks prose against it and reports candidates for a reader to judge. The script needs Python 3.9 or later and uses only the standard library.

Run `scripts/voicecheck draft.md` from this skill directory, pipe text to `scripts/voicecheck -`, or invoke `voicecheck` when the command is on PATH. Use `--json` for machine-readable output and `--selftest` to exercise the decision model against the fixtures.

The phrase pass reads Markdown paragraphs, skips fenced code, and selects sentences with case-insensitive patterns. For each selected sentence, the model sees the target and bounded context from its heading, list introduction, previous paragraph, and current paragraph. When the model pass runs, voicecheck sends these excerpts to AI Gateway.

Every request includes a safety identifier, the token the gateway gives the provider to attribute a call to one end user. The default hashes the local account and hostname into `voicecheck-<hex>`; set `VOICECHECK_SAFETY_IDENTIFIER` to use one identity across machines.

The default model is `openai/gpt-6-luna-decisions`. It returns a problem probability and a problem family. The threshold defaults to 0.5. Findings are ranked by probability and a phrase-reliability heuristic from an earlier audit. The displayed confidence is the model's probability, not a calibrated correctness rate. There is no separate reasoning-model pass.

Treat a model result as a prompt to inspect the sentence. The decision call can flag factual bounds or intentional design choices despite the allowances in its instructions. When the model fails or omits a score, the command reports the unscored sentence as a phrase candidate with confidence 0.0. Without `AI_GATEWAY_API_KEY`, the command uses the phrase pass and prints a warning to stderr. `--no-model` requests that pass explicitly.

The default model pass scores at most 24 phrase candidates. `--max-candidates N` changes that limit; additional candidates use the phrase pass. Requests contain at most 24 sentences each. `--exhaustive` scores every sentence and ignores the candidate limit. With `--no-model --exhaustive`, every sentence is reported as a candidate.

The text report prints at most 10 findings by default. `--top N` changes that limit and `--all` removes it. `--quiet` suppresses the report; warnings still go to stderr. Exit codes are 0 for no reported findings, 1 for findings, and 2 when input cannot be read or a self-test lacks a key. Lines refer to the start of the Markdown block containing the sentence. The command concatenates multiple input files. The text report prints the first file's path.

The development corpus holds 809 single sentences from 12 public repositories, labeled against the current SKILL.md without model scores in view. Each row records its repository as the stratum and its document kind: README, design doc, SKILL.md, AGENTS.md, prompt, or other. A passive is clean when its actor is the reader or is named in the sentence, and a contrast is clean when it names a real alternative. The sample is random within each document kind, so its violation rate does not estimate how often agents break the standard. `evals/run.py` sweeps thresholds against that corpus and accepts `--corpus PATH` for another JSONL dataset. It downloads each row's pinned source file once, into `~/.cache/voicecheck/corpus-sources`, and scores the sentences with the context voicecheck builds from that file; `--stored-context` uses the context saved in each row.

Run `python3 -m unittest -v test_voicecheck` from `scripts/` for deterministic tests. Run `./voicecheck --selftest` with `AI_GATEWAY_API_KEY` to check model recall against `evals/fixtures.jsonl`. The self-test reports false alarms but its exit code checks recall of the labeled violations.
