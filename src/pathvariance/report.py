"""Assemble analysis into line-oriented, deterministic report text.

Every function here returns a list of lines. The CLI joins them with newlines.
Keeping output line-oriented means two runs of the tool diff cleanly in git,
which is the point of the whole exercise: reproducibility you can see.

No wall-clock time, no randomness, no locale-dependent formatting appears in
any line. Shares are formatted with a fixed one-decimal percent and entropy
with three decimals.
"""

from __future__ import annotations

