import math
import unittest

from pathvariance.distribution import build_distribution, shannon_entropy_bits


class TestEntropy(unittest.TestCase):
    def test_single_category_zero(self):
        self.assertEqual(shannon_entropy_bits([10]), 0.0)

    def test_uniform_two_is_one_bit(self):
        self.assertAlmostEqual(shannon_entropy_bits([5, 5]), 1.0)

    def test_uniform_four_is_two_bits(self):
        self.assertAlmostEqual(shannon_entropy_bits([1, 1, 1, 1]), 2.0)

    def test_empty_zero(self):
        self.assertEqual(shannon_entropy_bits([]), 0.0)

    def test_no_negative_zero(self):
        self.assertEqual(shannon_entropy_bits([7]), 0.0)


class TestDistribution(unittest.TestCase):
    def setUp(self):
        # 8 of A, 2 of B, 2 of C, matching the sample fixture shape.
        self.sigs = (
            [("a",)] * 8 + [("b",)] * 2 + [("c",)] * 2
        )
