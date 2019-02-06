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
