import unittest

from pathvariance.divergence import analyse_divergence


class TestDivergence(unittest.TestCase):
    def test_no_divergence_when_all_match(self):
        modal = ("a", "b", "c")
        sigs = [modal, modal, modal]
        rep = analyse_divergence(sigs, modal)
        self.assertIsNone(rep.first_divergence_index)
        self.assertFalse(rep.diverges)

    def test_divergence_at_index(self):
        modal = ("a", "b", "c")
        sigs = [modal, ("a", "b", "x"), ("a", "b", "c")]
        rep = analyse_divergence(sigs, modal)
        self.assertEqual(rep.first_divergence_index, 2)

    def test_shorter_run_diverges(self):
        modal = ("a", "b", "c")
        sigs = [modal, ("a", "b")]
        rep = analyse_divergence(sigs, modal)
        self.assertEqual(rep.first_divergence_index, 2)

    def test_longer_run_diverges_past_modal_end(self):
        modal = ("a", "b")
        sigs = [modal, ("a", "b", "c")]
        rep = analyse_divergence(sigs, modal)
        self.assertEqual(rep.first_divergence_index, 2)

    def test_per_step_agreement_rates(self):
        modal = ("a", "b", "c")
