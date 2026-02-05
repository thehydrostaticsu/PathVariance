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

    def test_no_collapse_by_default(self):
        run = _run(["read", "read"])
        self.assertEqual(canonicalise(run), ("read", "read"))

    def test_signature_id_stable_and_prefixed(self):
        sig = ("grep", "read")
        self.assertTrue(signature_id(sig).startswith("p"))
        self.assertEqual(signature_id(sig), signature_id(sig))

    def test_signature_id_differs(self):
        self.assertNotEqual(signature_id(("a",)), signature_id(("b",)))

    def test_labels_by_first_appearance(self):
        sigs = [("a",), ("b",), ("a",), ("c",)]
        labels = label_paths(sigs)
        self.assertEqual(labels[("a",)], "A")
        self.assertEqual(labels[("b",)], "B")
        self.assertEqual(labels[("c",)], "C")

    def test_label_wraps_past_z(self):
        sigs = [(str(i),) for i in range(28)]
        labels = label_paths(sigs)
        self.assertEqual(labels[("25",)], "Z")
        self.assertEqual(labels[("26",)], "AA")
        self.assertEqual(labels[("27",)], "AB")


if __name__ == "__main__":
    unittest.main()
