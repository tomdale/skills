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


class CandidateTests(unittest.TestCase):
    def test_tics_are_candidates_in_any_case(self):
        cases = {
            "The interface CARRIES a label.": "carry",
            "A plugin names an icon.": "name verb",
            "The component owns deletion.": "component ownership",
            "The core stays on loopback.": "state phrasing",
            "The cookies remain isolated.": "state phrasing",
            "The daemon retains its key.": "state phrasing",
            "The page says so.": "says so",
            "The selectors are validated.": "passive voice",
            "The runner accepts a source, not a destination.": "X, not Y",
            "Observed: version 1.": "evidence framing",
            "The release is gated on approval.": "gating word",
            "The rule holds: eight tests pass.": "verdict verb",
            "Status: first draft.": "draft byline",
            "The list uses Alpha · Beta.": "mid-dot chain",
            "Those excerpts leave the machine through AI Gateway.": "data motion",
            "Your keys never travel off the device.": "data motion",
        }
        for sentence, expected in cases.items():
            with self.subTest(sentence=sentence):
                found, examined = vc.candidates(sentence)
                self.assertEqual(examined, 1)
                self.assertIn(expected, found[0]["matched"])

    def test_accepted_wording_is_not_a_word_specific_candidate(self):
        for sentence in (
            "The panel surfaces errors.",
            "The SDK exposes its controls.",
            "The only plugin-owned route is a navPanel.",
            "Name the file README.md.",
            "Deletion is deliberately left to the CLI after stopping agents.",
        ):
            with self.subTest(sentence=sentence):
                self.assertEqual(vc.candidates(sentence)[0], [])

    def test_bold_fragment_and_list_context(self):
        text = "# Settings\n\nThe program handles:\n\n- The interface carries a label.\n\n**Details.**\n"
        found, examined = vc.candidates(text)
        self.assertEqual(examined, 4)
        self.assertEqual(found[0]["line"], 5)
        self.assertIn("Heading: Settings", found[0]["context"])
        self.assertIn("List introduction: The program handles:", found[0]["context"])
        self.assertIn("bold fragment", found[1]["matched"])

    def test_emphasis_lead_in_only_applies_to_the_opening_sentence(self):
        found, _ = vc.candidates("**Result**: The panel carries a label. The page says so.")
        self.assertIn("emphasis lead-in", found[0]["matched"])
        self.assertNotIn("emphasis lead-in", found[1]["matched"])

    def test_context_is_bounded_and_contains_nearby_text(self):
        text = "A" * 5000 + ". The page says so. " + "B" * 5000
        found, _ = vc.candidates(text)
        self.assertEqual(len(found), 1)
        self.assertLessEqual(len(found[0]["context"]), 2100)
        self.assertIn("The page says so.", found[0]["context"])

    def test_physical_carry_is_candidate_for_model_to_decide(self):
        found, _ = vc.candidates("A courier carries a parcel.")
        self.assertIn("carry", found[0]["matched"])


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

    def test_custom_corpus_needs_no_matched_metadata(self):
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

    def test_empty_corpus_fails_cleanly(self):
        with tempfile.NamedTemporaryFile() as f, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.evaluator.main(["--corpus", f.name]), 2)


class GatewayTests(unittest.TestCase):
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

    def run_cli(self, text, args, ask):
        out = io.StringIO()
        err = io.StringIO()
        with mock.patch.dict(os.environ, {"AI_GATEWAY_API_KEY": "test-key"}), \
             mock.patch.object(vc, "ask", side_effect=ask), \
             mock.patch.object(vc.sys, "stdin", io.StringIO(text)), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = vc.main(["voicecheck", "--json", "--all", *args])
        return result, json.loads(out.getvalue()), err.getvalue()

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

    def test_failed_request_does_not_report_clean(self):
        result, output, err = self.run_cli(
            "The interface carries a label.", [], urllib.error.URLError("offline")
        )
        self.assertEqual(result, 1)
        self.assertEqual(len(output["findings"]), 1)
        self.assertEqual(output["findings"][0]["confidence"], 0)
        self.assertIn("model pass failed", err)

    def test_missing_answer_falls_back_for_that_candidate(self):
        answers = {"g0": {"probabilities": {"problem": 0.1}}}
        result, output, err = self.run_cli(
            "The interface carries a label.\n\nThe page says so.", [], [(answers, 0.0)]
        )
        self.assertEqual(result, 1)
        self.assertEqual([f["sentence"] for f in output["findings"]], ["The page says so."])
        self.assertIn("omitted candidate scores", err)

    def test_invalid_probability_falls_back_for_that_candidate(self):
        answers = {"g0": {"probabilities": {"problem": False}}}
        result, output, err = self.run_cli("The page says so.", [], [(answers, 0.0)])
        self.assertEqual(result, 1)
        self.assertEqual(output["findings"][0]["confidence"], 0)
        self.assertIn("omitted candidate scores", err)

    def test_failed_exhaustive_pass_reports_unscored_sentences(self):
        result, output, _ = self.run_cli(
            "The compiler wrote the output.", ["--exhaustive"], urllib.error.URLError("offline")
        )
        self.assertEqual(result, 1)
        self.assertEqual(output["findings"][0]["matched"], ["no phrase"])


if __name__ == "__main__":
    unittest.main()
