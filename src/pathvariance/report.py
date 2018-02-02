"""Assemble analysis into line-oriented, deterministic report text.

Every function here returns a list of lines. The CLI joins them with newlines.
Keeping output line-oriented means two runs of the tool diff cleanly in git,
which is the point of the whole exercise: reproducibility you can see.

No wall-clock time, no randomness, no locale-dependent formatting appears in
any line. Shares are formatted with a fixed one-decimal percent and entropy
with three decimals.
"""

from __future__ import annotations

from pathvariance.canon import CanonOptions, canonicalise
from pathvariance.distribution import Distribution, build_distribution
from pathvariance.divergence import DivergenceReport, analyse_divergence
from pathvariance.runs import Export
from pathvariance.stability import StabilityResult, assess


def signatures_for(export: Export, options: CanonOptions) -> list[tuple[str, ...]]:
    return [canonicalise(run, options) for run in export.runs]


def _sig_text(signature: tuple[str, ...]) -> str:
    return " -> ".join(signature) if signature else "(empty)"


def paths_lines(export: Export, dist: Distribution) -> list[str]:
    lines = [
        f"task: {export.task}",
        f"runs: {dist.total_runs}",
        f"distinct paths: {dist.distinct}",
        "",
        "label  id         count  share   path",
    ]
    for stat in dist.paths:
        lines.append(
            f"{stat.label:<5}  {stat.sig_id}  {stat.count:>5}  "
            f"{stat.share:>5.1%}  {_sig_text(stat.signature)}"
        )
    return lines


def entropy_lines(export: Export, dist: Distribution) -> list[str]:
    return [
        f"task: {export.task}",
        f"runs: {dist.total_runs}",
        f"distinct paths: {dist.distinct}",
        f"modal path: {dist.modal.label} ({dist.modal.sig_id})",
        f"modal share: {dist.modal.share:.1%}",
        f"shannon entropy: {dist.entropy_bits:.3f} bits",
        f"normalised entropy: {dist.normalised_entropy:.3f}",
    ]


def diverge_lines(
    export: Export, dist: Distribution, div: DivergenceReport
) -> list[str]:
    if div.first_divergence_index is None:
        first = "none (every run matched the modal path)"
    else:
        first = str(div.first_divergence_index)
    lines = [
        f"task: {export.task}",
        f"runs: {dist.total_runs}",
        f"modal path: {dist.modal.label} ({dist.modal.sig_id})",
        f"first divergence index: {first}",
        "",
        "step  agree  of     rate   modal token",
    ]
    for step in div.per_step:
        lines.append(
            f"{step.index:>4}  {step.agreeing:>5}  {step.considered:>5}  "
            f"{step.rate:>5.1%}  {step.modal_token}"
        )
