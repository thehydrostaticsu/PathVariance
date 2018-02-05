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
