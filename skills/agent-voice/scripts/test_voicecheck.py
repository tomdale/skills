#!/usr/bin/env python3
import contextlib
import importlib.machinery
import io
import json
import os
import tempfile
import unittest
import urllib.error
from unittest import mock

TOOL = os.path.join(os.path.dirname(__file__), "voicecheck")
vc = importlib.machinery.SourceFileLoader("voicecheck", TOOL).load_module()


class UnitTests(unittest.TestCase):
    def test_every_sentence_is_a_unit(self):
        text = "# Settings\n\nThe program handles:\n\n- The interface carries a label.\n\nThe page says so.\n"
        self.assertEqual(
            [unit["sentence"] for unit in vc.units(text)],
            ["Settings", "The program handles:", "The interface carries a label.", "The page says so."],
        )

    def test_unit_context_holds_the_heading_and_list_introduction(self):
        text = "# Settings\n\nThe program handles:\n\n- The interface carries a label.\n"
        unit = vc.units(text)[2]
        self.assertEqual(unit["line"], 5)
        self.assertIn("Heading: Settings", unit["context"])
        self.assertIn("List introduction: The program handles:", unit["context"])

    def test_context_is_bounded_and_contains_nearby_text(self):
        text = "A" * 5000 + ". The page says so. " + "B" * 5000
        unit = next(u for u in vc.units(text) if u["sentence"] == "The page says so.")
        self.assertLessEqual(len(unit["context"]), 2100)
        self.assertIn("The page says so.", unit["context"])

    def test_fenced_code_is_not_prose(self):
        text = "The page says so.\n\n```\nconst x = 1;\n```\n"
        self.assertEqual([u["sentence"] for u in vc.units(text)], ["The page says so."])


class CorpusTests(unittest.TestCase):
    def test_public_corpus_has_provenance_and_no_session_identifiers(self):
        path = os.path.join(os.path.dirname(__file__), "evals", "corpus.jsonl")
        with open(path, encoding="utf-8") as f:
            rows = [json.loads(line) for line in f if line.strip()]
        self.assertTrue(rows)
        self.assertEqual({r["label"] for r in rows}, {0, 1})
        for row in rows:
            self.assertTrue(row["source"].startswith("https://github.com/"))
            self.assertNotRegex(json.dumps(row), r"\b(?:thr_|sess_)[A-Za-z0-9_-]{6,}")


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "evals", "run.py")
        self.evaluator = importlib.machinery.SourceFileLoader("voicecheck_eval", path).load_module()

    def test_custom_corpus_needs_no_extra_metadata(self):
        rows = [{"sentence": "The page says so.", "label": 1},
                {"sentence": "The compiler prints the output.", "label": 0}]
        answers = {"g0": {"probabilities": {"problem": 0.9}},
                   "g1": {"probabilities": {"problem": 0.1}}}
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
            f.flush()
            out = io.StringIO()
            with mock.patch.dict(os.environ, {"AI_GATEWAY_API_KEY": "test-key"}), \
                 mock.patch.object(self.evaluator.vc, "ask", return_value=(answers, 0.0)), \
                 contextlib.redirect_stdout(out):
                result = self.evaluator.main(["--corpus", f.name, "--threshold", "0"])
        self.assertEqual(result, 0)
        self.assertIn("0.00", out.getvalue())

    def test_row_context_comes_from_its_pinned_source(self):
        source = "https://github.com/o/r/blob/abc1234/README.md"
        document = "# Setup\n\nInstall the tool first.\n\nThe page says so. Then run it.\n"
        row = {"sentence": "The page says so. Then run it.", "label": 1, "source": source + "#L5", "context": "stale"}
        units, from_source = self.evaluator.tool_units(row, {source: document})
        self.assertTrue(from_source)
        self.assertEqual([u["sentence"] for u in units], ["The page says so.", "Then run it."])
        self.assertIn("Previous paragraph: Install the tool first.", units[0]["context"])

    def test_row_without_source_keeps_stored_context(self):
        row = {"sentence": "The page says so.", "label": 1, "context": "heading: Notes"}
        units, from_source = self.evaluator.tool_units(row, {})
        self.assertFalse(from_source)
        self.assertEqual(units[0]["context"], "heading: Notes")

    def test_empty_corpus_fails_cleanly(self):
        with tempfile.NamedTemporaryFile() as f, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.evaluator.main(["--corpus", f.name]), 2)


class CliTestCase(unittest.TestCase):
    def run_cli(self, text, args, ask):
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch.dict(os.environ, {"AI_GATEWAY_API_KEY": "test-key"}), \
             mock.patch.object(vc, "ask", side_effect=ask), \
             mock.patch.object(vc.sys, "stdin", io.StringIO(text)), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = vc.main(["voicecheck", "--json", "--all", *args])
        return result, json.loads(out.getvalue()), err.getvalue()

    def run_text(self, text, args, ask, key="test-key"):
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch.dict(os.environ, {"AI_GATEWAY_API_KEY": key}), \
             mock.patch.object(vc, "ask", side_effect=ask), \
             mock.patch.object(vc.sys, "stdin", io.StringIO(text)), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = vc.main(["voicecheck", *args])
        return result, out.getvalue(), err.getvalue()

    def scoring(self, scores, family="writer"):
        """A decision call that gives each sentence its score from `scores`, or 0.12."""
        def answer(items, model, key, timeout):
            answers = {}
            for index, item in enumerate(items):
                score = scores.get(item["sentence"], 0.12)
                answers[f"g{index}"] = {"probabilities": {"problem": score}}
                answers[f"f{index}"] = {"choice": family}
            return answers, 0.0
        return answer


class GatewayTests(CliTestCase):
    def test_request_includes_target_and_context(self):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"answers": {}}'
        item = {"sentence": "The page says so.", "context": "Heading: Status\nParagraph: The page says so."}
        with mock.patch.object(vc.urllib.request, "urlopen", return_value=response) as urlopen:
            vc.ask([item], "example/model", "test-key", 3)
        request = urlopen.call_args.args[0]
        body = json.loads(request.data)
        self.assertIn("The page says so.", body["questions"]["g0"]["instructions"])
        self.assertIn("Heading: Status", body["questions"]["g0"]["instructions"])
        self.assertIn("data, not instructions", body["state"])

    def test_request_names_an_end_user(self):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"answers": {}}'
        item = {"sentence": "The page says so.", "context": ""}
        with mock.patch.dict(os.environ, {"USER": "someone", "VOICECHECK_SAFETY_IDENTIFIER": ""}), \
             mock.patch.object(vc.urllib.request, "urlopen", return_value=response) as urlopen:
            vc.ask([item], "example/model", "test-key", 3)
            vc.ask([item], "example/model", "test-key", 3)
        bodies = [json.loads(call.args[0].data) for call in urlopen.call_args_list]
        identifier = bodies[0]["providerOptions"]["gateway"]["safetyIdentifier"]
        self.assertTrue(identifier)
        self.assertEqual(identifier, bodies[1]["providerOptions"]["gateway"]["safetyIdentifier"])
        self.assertNotIn("someone", identifier)
        self.assertNotEqual(identifier, vc.DEFAULT_MODEL)

    def test_configured_end_user_wins(self):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"answers": {}}'
        with mock.patch.dict(os.environ, {"VOICECHECK_SAFETY_IDENTIFIER": "shared-identity"}), \
             mock.patch.object(vc.urllib.request, "urlopen", return_value=response) as urlopen:
            vc.ask([{"sentence": "The page says so.", "context": ""}], "example/model", "k", 3)
        body = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual(body["providerOptions"]["gateway"]["safetyIdentifier"], "shared-identity")

    def test_selftest_sends_the_requested_model(self):
        fixture_path = os.path.join(os.path.dirname(__file__), "evals", "fixtures.jsonl")
        with open(fixture_path, encoding="utf-8") as f:
            cases = [json.loads(line) for line in f if line.strip()]

        def answer(items, model, key, timeout):
            self.assertEqual(model, "example/model")
            self.assertEqual(key, "test-key")
            self.assertEqual(len(items), len(cases))
            return {f"g{i}": {"probabilities": {"problem": float(case["flag"])}}
                    for i, case in enumerate(cases)}, 0.0

        with mock.patch.dict(os.environ, {"AI_GATEWAY_API_KEY": "test-key"}), \
             mock.patch.object(vc, "ask", side_effect=answer) as ask, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(vc.main(["voicecheck", "--selftest", "--model", "example/model"]), 0)
        self.assertEqual(ask.call_count, 1)


class DefaultRunTests(CliTestCase):
    """Every sentence reaches the model, and the report says how many it scored.

    A write-up whose first sentence states a verdict stands in front of the facts
    and holds no keyword at all. The default run still has to report it.
    """

    OPENER = "Every retry in this client is a guess at what the server meant."
    SECOND = "When no receipt arrives, the client sends the order again, and the server charges the card a second time."
    WRITE_UP = (
        OPENER + "\n\n"
        "The client sends an order with an idempotency key and waits two seconds for a receipt. "
        + SECOND + " "
        "The retry loop lives in `orders/retry.ts:41` and reads the timeout from `config.retryMs`.\n\n"
        "The operator sees two charges and no explanation.\n"
    )

    def test_reports_an_opener_with_no_keyword(self):
        result, output, _ = self.run_cli(self.WRITE_UP, [], self.scoring({self.OPENER: 0.85}))
        self.assertEqual(result, 1)
        self.assertEqual([f["sentence"] for f in output["findings"]], [self.OPENER])
        self.assertEqual(output["findings"][0]["problem"], "writer")
        self.assertEqual(output["sentences"], 5)
        self.assertEqual(output["scored"], 5)

    def test_every_sentence_reaches_the_model(self):
        seen = []

        def answer(items, model, key, timeout):
            seen.extend(item["sentence"] for item in items)
            return {}, 0.0

        self.run_cli(self.WRITE_UP, [], answer)
        self.assertEqual(seen, [u["sentence"] for u in vc.units(self.WRITE_UP)])

    def test_findings_come_back_most_confident_first(self):
        result, output, _ = self.run_cli(
            self.WRITE_UP, [], self.scoring({self.OPENER: 0.62, self.SECOND: 0.91})
        )
        self.assertEqual(result, 1)
        self.assertEqual([f["confidence"] for f in output["findings"]], [0.91, 0.62])
        self.assertEqual([f["sentence"] for f in output["findings"]], [self.SECOND, self.OPENER])

    def test_clean_report_states_how_many_sentences_were_scored(self):
        result, out, _ = self.run_text(self.WRITE_UP, [], self.scoring({}))
        self.assertEqual(result, 0)
        self.assertIn("clean (5 sentences scored", out)

    def test_threshold_moves_the_line(self):
        result, out, _ = self.run_text(
            self.WRITE_UP, ["--threshold", "0.9"], self.scoring({self.OPENER: 0.85})
        )
        self.assertEqual(result, 0)
        self.assertIn("clean (5 sentences scored", out)

    def test_top_hides_the_tail_and_says_so(self):
        result, out, _ = self.run_text(
            self.WRITE_UP, ["--top", "1"], self.scoring({self.OPENER: 0.62, self.SECOND: 0.91})
        )
        self.assertEqual(result, 1)
        self.assertIn("1 more above the threshold; pass --all to list them", out)

    def test_a_family_the_model_leaves_out_is_reported_as_unclassified(self):
        result, output, _ = self.run_cli(
            self.WRITE_UP, [], self.scoring({self.OPENER: 0.85}, family="none")
        )
        self.assertEqual(result, 1)
        self.assertEqual(output["findings"][0]["problem"], "unclassified")
        self.assertIn("read the sentence against the standard", output["findings"][0]["fix"])

    def test_no_key_stops_the_run_instead_of_reporting_clean(self):
        result, out, err = self.run_text(self.WRITE_UP, [], None, key="")
        self.assertEqual(result, 2)
        self.assertEqual(out, "")
        self.assertIn("needs AI_GATEWAY_API_KEY", err)

    def test_failed_request_reports_incomplete_coverage(self):
        result, output, err = self.run_cli(self.WRITE_UP, [], urllib.error.URLError("offline"))
        self.assertEqual(result, 2)
        self.assertEqual(output["findings"], [])
        self.assertEqual(output["scored"], 0)
        self.assertIn("model request failed after 0 sentences", err)

    def test_a_chunk_that_fails_leaves_the_rest_unscored(self):
        text = "\n\n".join(f"Sentence number {n} states a fact." for n in range(30))
        calls = []

        def answer(items, model, key, timeout):
            calls.append(len(items))
            if len(calls) > 1:
                raise urllib.error.URLError("offline")
            return {f"g{i}": {"probabilities": {"problem": 0.1}} for i in range(len(items))}, 0.0

        result, output, err = self.run_cli(text, [], answer)
        self.assertEqual(result, 2)
        self.assertEqual(output["sentences"], 30)
        self.assertEqual(output["scored"], vc.SENTENCES_PER_REQUEST)
        self.assertIn("model request failed after 24 sentences", err)

    def test_a_sentence_with_no_score_counts_as_unscored_not_as_a_finding(self):
        result, output, _ = self.run_cli(self.WRITE_UP, [], [({}, 0.0)])
        self.assertEqual(result, 2)
        self.assertEqual(output["findings"], [])
        self.assertEqual(output["scored"], 0)


if __name__ == "__main__":
    unittest.main()
