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

    def test_distinct_count(self):
        dist = build_distribution(self.sigs)
        self.assertEqual(dist.distinct, 3)

    def test_total_runs(self):
        dist = build_distribution(self.sigs)
        self.assertEqual(dist.total_runs, 12)

    def test_modal_is_a(self):
        dist = build_distribution(self.sigs)
        self.assertEqual(dist.modal.signature, ("a",))
        self.assertEqual(dist.modal.count, 8)
        self.assertAlmostEqual(dist.modal.share, 8 / 12)

    def test_entropy_matches_hand_computation(self):
        dist = build_distribution(self.sigs)
        expected = -(
            (8 / 12) * math.log2(8 / 12)
            + 2 * (2 / 12) * math.log2(2 / 12)
        )
        self.assertAlmostEqual(dist.entropy_bits, expected)

    def test_normalised_between_zero_and_one(self):
        dist = build_distribution(self.sigs)
        self.assertGreater(dist.normalised_entropy, 0.0)
        self.assertLessEqual(dist.normalised_entropy, 1.0)

    def test_single_path_normalised_zero(self):
