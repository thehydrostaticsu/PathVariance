import unittest

from pathvariance.distribution import build_distribution
from pathvariance.stability import Verdict, assess


def _dist(a, b=0, c=0):
    sigs = [("a",)] * a + [("b",)] * b + [("c",)] * c
    return build_distribution(sigs)


class TestStability(unittest.TestCase):
    def test_under_min_refuses(self):
        result = assess(_dist(2, 1), min_runs=5)
        self.assertIs(result.verdict, Verdict.UNDER_MIN)
        self.assertIsNone(result.modal_share)
        self.assertFalse(result.is_reportable)
        self.assertIn("below the minimum", result.reason)

    def test_stable_above_threshold(self):
        result = assess(_dist(10), min_runs=5, threshold=0.90)
        self.assertIs(result.verdict, Verdict.STABLE)
        self.assertEqual(result.exit_code, 0)

    def test_unstable_below_threshold(self):
        result = assess(_dist(8, 2, 2), min_runs=5, threshold=0.90)
        self.assertIs(result.verdict, Verdict.UNSTABLE)
        self.assertEqual(result.exit_code, 1)

    def test_exactly_at_threshold_is_stable(self):
        # 9 of 10 is 0.9, at the threshold, which counts as stable.
        result = assess(_dist(9, 1), min_runs=5, threshold=0.90)
        self.assertIs(result.verdict, Verdict.STABLE)

    def test_under_min_exit_code_is_one(self):
        result = assess(_dist(3), min_runs=5)
