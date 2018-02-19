import unittest

from pathvariance.canon import (
    CanonOptions,
    canonicalise,
    label_paths,
    signature_id,
)
from pathvariance.runs import Run, Step


def _run(tools, args=None):
    steps = []
    for i, t in enumerate(tools):
        a = (args or {}).get(i, {})
        steps.append(Step(tool=t, args=a))
    return Run(run_id="r", steps=tuple(steps))


class TestCanon(unittest.TestCase):
    def test_tool_only_by_default(self):
        run = _run(["grep", "read"], {0: {"p": "x"}})
        self.assertEqual(canonicalise(run), ("grep", "read"))

    def test_argument_sensitive_distinguishes(self):
        opts = CanonOptions(argument_sensitive=True)
        r1 = _run(["grep"], {0: {"p": "a"}})
        r2 = _run(["grep"], {0: {"p": "b"}})
        self.assertNotEqual(canonicalise(r1, opts), canonicalise(r2, opts))

    def test_argument_insensitive_collapses(self):
        r1 = _run(["grep"], {0: {"p": "a"}})
        r2 = _run(["grep"], {0: {"p": "b"}})
        self.assertEqual(canonicalise(r1), canonicalise(r2))

    def test_collapse_repeats(self):
        opts = CanonOptions(collapse_repeats=True)
        run = _run(["read", "read", "read", "edit"])
        self.assertEqual(canonicalise(run, opts), ("read", "edit"))
