"""The path distribution: distinct paths, modal share, Shannon entropy.

Given the canonical signatures of every run, this module summarises how the
runs spread across paths. The three numbers a reader wants are:

- how many distinct paths appeared,
- the modal path and what fraction of runs took it,
- Shannon entropy over the path distribution, which is zero when every run took
  one path and rises as the mass spreads out.

Entropy is reported in bits (log base 2). Normalised entropy divides by
``log2(k)`` where ``k`` is the number of distinct paths, giving a 0 to 1 scale
that is comparable across tasks with different path counts. When ``k`` is 1 the
normalised value is defined as 0, because there is no spread to measure.

Ties for the modal path are broken by the ordinal label, so the result does not
depend on run order in the export.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from pathvariance.canon import label_paths, signature_id


@dataclass(frozen=True)
class PathStat:
    """One distinct path and how often it occurred."""

    label: str
    sig_id: str
    signature: tuple[str, ...]
    count: int
    share: float


@dataclass(frozen=True)
class Distribution:
    """The full path distribution for a set of runs."""

    total_runs: int
    paths: tuple[PathStat, ...]
    entropy_bits: float
    normalised_entropy: float

    @property
    def distinct(self) -> int:
        return len(self.paths)

    @property
    def modal(self) -> PathStat:
        return self.paths[0]


def shannon_entropy_bits(counts: list[int]) -> float:
    """Shannon entropy in bits for a list of category counts."""
    total = sum(counts)
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts:
        if count <= 0:
            continue
        p = count / total
        entropy -= p * math.log2(p)
    # A single populated category yields exactly 0.0; guard tiny negatives from
    # floating point so the sign is never surprising.
    return abs(entropy)


def build_distribution(signatures: list[tuple[str, ...]]) -> Distribution:
    """Summarise the distribution of the given per-run signatures."""
    total = len(signatures)
    labels = label_paths(signatures)
