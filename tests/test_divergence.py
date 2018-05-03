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
        sigs = [modal, modal, ("a", "x", "c")]
        rep = analyse_divergence(sigs, modal)
        self.assertAlmostEqual(rep.per_step[0].rate, 1.0)
        self.assertAlmostEqual(rep.per_step[1].rate, 2 / 3)
        self.assertAlmostEqual(rep.per_step[2].rate, 1.0)

    def test_ended_run_not_counted_in_rate(self):
        modal = ("a", "b", "c")
        sigs = [modal, ("a", "b")]
        rep = analyse_divergence(sigs, modal)
        # At index 2 only one run reached the step, and it agreed.
        self.assertEqual(rep.per_step[2].considered, 1)
        self.assertEqual(rep.per_step[2].agreeing, 1)

