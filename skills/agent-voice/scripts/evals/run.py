#!/usr/bin/env python3
"""Score voicecheck against public Markdown paragraphs.

The development corpus holds single sentences sampled from public Markdown
documents and labeled against the current SKILL.md. The sample is random within
each document kind, so precision and recall do not estimate natural prevalence.
The phrase pass selects candidates and the decision call scores them at or above
the threshold.

Each row's source URL pins a file at a commit. The evaluator downloads that file
once into ~/.cache/voicecheck/corpus-sources and sends the model the sentences
and context voicecheck itself would build from it. Rows without a loadable
source use the context stored in the row.

    ./run.py                   # sweep thresholds, report the best
    ./run.py --threshold 0.5
    ./run.py --json
    ./run.py --stored-context  # use each row's stored context instead
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import sys
import time
from importlib.machinery import SourceFileLoader

HERE = os.path.dirname(os.path.realpath(__file__))
TOOL = os.path.join(os.path.dirname(HERE), "voicecheck")
vc = SourceFileLoader("voicecheck_tool", TOOL).load_module()

SWEEP = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7)
CHUNK = 20


RAW = re.compile(r"https://github\.com/([^/]+)/([^/]+)/blob/([0-9a-f]{7,40})/([^#]+)")


def cache_dir() -> str:
    base = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
    return os.path.join(base, "voicecheck", "corpus-sources")


def fetch_source(source: str) -> str | None:
    """The document a row came from, at the commit its URL pins, or None.

    A pinned file never changes, so a cached copy is reused without checking.
    """
    match = RAW.match(source or "")
    if not match:
        return None
    owner, repo, sha, quoted = match.groups()
    path = urllib.parse.unquote(quoted)
    cached = os.path.join(cache_dir(), owner, repo, sha, path)
    if os.path.exists(cached):
        with open(cached, encoding="utf-8") as f:
            return f.read()
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{urllib.parse.quote(path)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            text = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError):
        return None
    os.makedirs(os.path.dirname(cached), exist_ok=True)
    with open(cached, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", vc.plain(text)).strip().lower()


def tool_units(row, documents):
    """The sentences voicecheck would score for this row, with the context it would send.

    A row can hold more than one sentence; voicecheck scores each separately, so
    each becomes a unit and the row takes the highest score. A row whose source
    cannot be loaded, or whose text is not found in it, falls back to its stored
    context, and the second value reports which happened.
    """
    text = documents.get(row.get("source", "").split("#")[0])
    if text is not None:
        wanted = _norm(row["sentence"])
        units = [
            {"sentence": sentence, "context": context, "matched": _matches(sentence, block, first)}
            for _, sentence, block, context, first in vc.contextual_units(text)
            if _norm(sentence) and _norm(sentence) in wanted and wanted[:60] in _norm(block)
        ]
        if units:
            return units, True
    return [{"sentence": row["sentence"], "context": row.get("context", ""), "matched": _matches(row["sentence"], row["sentence"], True)}], False


def _matches(sentence, block, first):
    found, _ = vc.candidates(sentence)
    hits = list(found[0]["matched"]) if found else []
    if first:
        for name, _, pattern in vc.PATTERNS:
            if name in ("bold fragment", "emphasis lead-in") and re.search(pattern, block, re.IGNORECASE) and name not in hits:
                hits.append(name)
    return hits


def score_corpus(rows, key, stored_context=False):
    documents = {}
    if not stored_context:
        for source in {r.get("source", "").split("#")[0] for r in rows}:
            text = fetch_source(source)
            if text is not None:
                documents[source] = text
    expanded = [tool_units(row, documents) for row in rows]
    items = [unit for units, _ in expanded for unit in units]
    scores = []
    for start in range(0, len(items), CHUNK):
        chunk = items[start : start + CHUNK]
        answers, _ = vc.ask(
            [{"offset": i, "line": i + 1, "sentence": u["sentence"], "matched": ["corpus"], "context": u["context"]} for i, u in enumerate(chunk)],
            vc.DEFAULT_MODEL, key, timeout=90,
        )
        for index in range(len(chunk)):
            answer = answers.get(f"g{index}") or {}
            scores.append(((answer.get("probabilities") or {}).get("problem", 0.0), (answers.get(f"f{index}") or {}).get("choice") or "none"))
    scored = []
    position = 0
    for row, (units, from_source) in zip(rows, expanded):
        unit_scores = scores[position : position + len(units)]
        position += len(units)
        # The row counts as reported when any of its sentences would be: a phrase
        # match selected it and its decision score crosses the threshold.
        reported = [s for u, s in zip(units, unit_scores) if u["matched"]]
        best = max(reported or unit_scores, key=lambda s: s[0])
        scored.append({
            **row,
            "candidate": bool(reported),
            "matched": sorted({m for u in units for m in u["matched"]}),
            "score": best[0],
            "family": best[1],
            "fromSource": from_source,
        })
    return scored


def confusion(scored, threshold):
    tp = fp = fn = tn = 0
    wrong = []
    for row in scored:
        predicted = bool(row["candidate"]) and row["score"] >= threshold
        actual = bool(row["label"])
        if predicted and actual:
            tp += 1
        elif predicted:
            fp += 1
            wrong.append(("false positive", row))
        elif actual:
            fn += 1
            wrong.append(("miss", row))
        else:
            tn += 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "threshold": threshold,
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision, "recall": recall, "f1": f1,
        "accuracy": (tp + tn) / len(scored) if scored else 0.0,
    }, wrong


def main(argv):
    as_json = "--json" in argv
    threshold = None
    if "--threshold" in argv:
        threshold = float(argv[argv.index("--threshold") + 1])
    path = os.path.join(HERE, "corpus.jsonl")
    stored_context = "--stored-context" in argv
    if "--corpus" in argv:
        path = argv[argv.index("--corpus") + 1]
    try:
        with open(path, encoding="utf-8") as corpus:
            rows = [json.loads(line) for line in corpus if line.strip()]
    except (OSError, ValueError) as error:
        print(f"run.py: cannot read corpus ({error})", file=sys.stderr)
        return 2
    if not rows:
        print("run.py: corpus must contain at least one row", file=sys.stderr)
        return 2
    strata = sorted({r.get("stratum", "all") for r in rows})
    key = os.environ.get("AI_GATEWAY_API_KEY", "").strip()
    if not key:
        print("run.py: needs AI_GATEWAY_API_KEY", file=sys.stderr)
        return 2

    started = time.monotonic()
    scored = score_corpus(rows, key, stored_context)
    elapsed = int((time.monotonic() - started) * 1000)

    results = [confusion(scored, t)[0] for t in ([threshold] if threshold is not None else SWEEP)]
    best = max(results, key=lambda r: (r["f1"], r["precision"]))["threshold"]
    positives = [r for r in scored if r["label"]]
    negatives = [r for r in scored if not r["label"]]
    candidate_recall = sum(1 for r in positives if r["candidate"]) / len(positives) if positives else 0
    mean_pos = sum(r["score"] for r in positives) / len(positives) if positives else 0
    mean_neg = sum(r["score"] for r in negatives) / len(negatives) if negatives else 0

    if as_json:
        print(json.dumps({
            "sweep": results,
            "best": best,
            "sentences": len(scored),
            "positives": len(positives),
            "negatives": len(negatives),
            "prefilterRecall": round(candidate_recall, 3),
            "meanScorePositives": round(mean_pos, 3),
            "meanScoreNegatives": round(mean_neg, 3),
            "elapsedMs": elapsed,
            "model": vc.DEFAULT_MODEL,
            "rowsFromSource": sum(1 for r in scored if r["fromSource"]),
        }, indent=2))
        return 0

    rebuilt = sum(1 for r in scored if r["fromSource"])
    print(f"context: {rebuilt} of {len(scored)} rows rebuilt from their pinned source, {len(scored) - rebuilt} use stored context")
    print(f"{len(scored)} sentences: {len(positives)} violations ({len(positives)/len(scored):.1%}), {len(negatives)} clean")
    for stratum in strata:
        group = [r for r in scored if r.get("stratum", "all") == stratum]
        if not group:
            continue
        hits = sum(1 for r in group if r["label"])
        reached = sum(1 for r in group if r["candidate"])
        print(f"  {stratum:9} {len(group):3} sentences, {hits:2} violations ({hits/len(group):.1%}), "
              f"{reached:2} reach the decision call ({reached/len(group):.0%})")
    print(f"phrase pass reaches {candidate_recall:.0%} of the violations; decision mean score "
          f"{mean_pos:.2f} on violations and {mean_neg:.2f} on clean ({elapsed} ms)\n")
    print("A first pass wants recall, so read the curve at a low threshold and")
    print("check that the shortlist stays trustworthy as you go down it.\n")
    print(f"{'thr':>5} {'prec':>6} {'rec':>6} {'F1':>6} {'acc':>6}   tp fp fn tn")
    for result in results:
        mark = " <-" if result["threshold"] == best else ""
        print(f"{result['threshold']:5.2f} {result['precision']:6.2f} {result['recall']:6.2f} "
              f"{result['f1']:6.2f} {result['accuracy']:6.2f}  {result['tp']:3} {result['fp']:2} "
              f"{result['fn']:2} {result['tn']:2}{mark}")

    print(f"\nat the shipped threshold {vc.DEFAULT_THRESHOLD}, per stratum:")
    for stratum in strata:
        group = [r for r in scored if r.get("stratum", "all") == stratum]
        result, _ = confusion(group, vc.DEFAULT_THRESHOLD)
        print(f"  {stratum:9} tp {result['tp']:2} fp {result['fp']:2} fn {result['fn']:2} "
              f"| precision {result['precision']:.2f} recall {result['recall']:.2f}")

    ranked = sorted((r for r in scored if r["candidate"] and r["score"] >= vc.DEFAULT_THRESHOLD), key=lambda r: -(r["score"] * max(
        (vc.PRIORS.get(name, 0.5) for name in (r.get("matched") or ["none"])), default=0.5)))
    total_positives = sum(1 for r in scored if r["label"])
    print(f"\nshortlist at {vc.DEFAULT_THRESHOLD}, ranked by score x phrase reliability:")
    for k in (5, 8, 12, 16):
        if k > len(ranked):
            break
        top = ranked[:k]
        hits = sum(1 for r in top if r["label"])
        print(f"  top {k:2}: {hits:2} of {total_positives} violations, precision {hits / k:.2f}")

    chosen = [r for r in results if r["threshold"] == (threshold if threshold is not None else best)][0]
    _, wrong = confusion(scored, chosen["threshold"])
    if wrong:
        print(f"\nmistakes at {chosen['threshold']:.2f}:")
        for kind, row in wrong:
            print(f"  {kind:14} score={row['score']:.2f} match={row['candidate']}  {row['sentence'][:120]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
