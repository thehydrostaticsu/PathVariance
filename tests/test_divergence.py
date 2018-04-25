import unittest

from pathvariance.divergence import analyse_divergence


class TestDivergence(unittest.TestCase):
    def test_no_divergence_when_all_match(self):
        modal = ("a", "b", "c")
        sigs = [modal, modal, modal]
        rep = analyse_divergence(sigs, modal)
        self.assertIsNone(rep.first_divergence_index)
        self.assertFalse(rep.diverges)
