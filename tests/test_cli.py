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

