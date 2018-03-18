import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from pathvariance.cli import main

SAMPLE = str(Path(__file__).resolve().parent.parent / "samples" / "task-repeat.json")


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_version(self):
        code, out, _ = _run(["version"])
        self.assertEqual(code, 0)
        self.assertIn("pathvariance", out)

    def test_paths_counts(self):
        code, out, _ = _run(["paths", SAMPLE])
        self.assertEqual(code, 0)
        self.assertIn("distinct paths: 3", out)
        self.assertIn("66.7%", out)

    def test_entropy_value(self):
        code, out, _ = _run(["entropy", SAMPLE])
        self.assertEqual(code, 0)
        self.assertIn("1.252 bits", out)

    def test_diverge_index(self):
        code, out, _ = _run(["diverge", SAMPLE])
        self.assertEqual(code, 0)
        self.assertIn("first divergence index: 2", out)

    def test_report_exits_one_when_unstable(self):
        code, out, _ = _run(["report", SAMPLE])
        self.assertEqual(code, 1)
        self.assertIn("UNSTABLE", out)

    def test_report_stable_lower_threshold(self):
        code, out, _ = _run(["report", SAMPLE, "--threshold", "0.5"])
