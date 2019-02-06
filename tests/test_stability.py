import unittest

from pathvariance.distribution import build_distribution
from pathvariance.stability import Verdict, assess


def _dist(a, b=0, c=0):
    sigs = [("a",)] * a + [("b",)] * b + [("c",)] * c
    return build_distribution(sigs)
