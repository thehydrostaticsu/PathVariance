"""Stability verdict with an explicit minimum-run-count gate.

Three runs cannot describe a distribution. With so few samples, one path taking
two of three runs looks like 67 percent stability, but the confidence interval
around that is so wide that the number misleads more than it informs. So this
module refuses to issue entropy or a verdict below a minimum run count and says
why, rather than printing a figure that reads as authoritative.

The verdict compares the modal share against a declared threshold. At or above
the threshold the task is STABLE. Below it the task is UNSTABLE. When the run
count is below the gate the verdict is UNDER_MIN and no share or entropy is
asserted. The default gate is 5 and the default threshold is 0.90, both chosen
to be conservative and both overridable from the CLI.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pathvariance.distribution import Distribution

DEFAULT_MIN_RUNS = 5
DEFAULT_THRESHOLD = 0.90


class Verdict(str, Enum):
    STABLE = "STABLE"
    UNSTABLE = "UNSTABLE"
    UNDER_MIN = "UNDER_MIN"


@dataclass(frozen=True)
class StabilityResult:
    """The verdict and the reasoning behind it."""

    verdict: Verdict
    total_runs: int
