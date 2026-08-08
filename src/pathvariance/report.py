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
    return lines


def stability_lines(stability: StabilityResult) -> list[str]:
    lines = [
        f"verdict: {stability.verdict.value}",
        f"runs: {stability.total_runs}",
        f"minimum runs: {stability.min_runs}",
        f"threshold: {stability.threshold:.0%}",
    ]
    if stability.modal_share is not None:
        lines.append(f"modal share: {stability.modal_share:.1%}")
    lines.append(f"reason: {stability.reason}")
    return lines


def full_report(
    export: Export,
    options: CanonOptions,
    min_runs: int,
    threshold: float,
) -> tuple[list[str], StabilityResult]:
    """The combined report used by the ``report`` subcommand.

    Returns the report lines and the stability result so the CLI can set its
    exit code from the same assessment the report describes.
    """
    signatures = signatures_for(export, options)
    dist = build_distribution(signatures)
    stability = assess(dist, min_runs=min_runs, threshold=threshold)

    lines: list[str] = []
    lines.append("== pathvariance report ==")
    lines.append(f"task: {export.task}")
    lines.append(
        "argument sensitivity: "
        + ("on" if options.argument_sensitive else "off")
    )
    lines.append("")
    lines.extend(stability_lines(stability))

    if not stability.is_reportable:
        # Honesty gate: refuse to print the distribution or entropy below the
        # minimum run count. State why and stop.
        lines.append("")
        lines.append(
            "distribution and entropy withheld: run count is below the "
            "minimum gate"
        )
        return lines, stability

    lines.append("")
    lines.append("-- distribution --")
    lines.extend(paths_lines(export, dist))
    lines.append("")
    lines.append("-- entropy --")
    lines.extend(entropy_lines(export, dist))
    lines.append("")
    lines.append("-- divergence --")
    div = analyse_divergence(signatures, dist.modal.signature)
    lines.extend(diverge_lines(export, dist, div))
    return lines, stability
