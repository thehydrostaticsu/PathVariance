"""Command line interface for pathvariance.

Subcommands:

    paths     print the path distribution table
    entropy   print modal share and Shannon entropy
    diverge   print the first divergence index and per-step agreement
    report    print the full combined report
    version   print the version and exit

Exit codes:

    0   analysis ran and the task is stable (for report), or the query
        succeeded (for paths, entropy, diverge)
    1   the task is below the declared stability threshold, or below the
        minimum run count so no verdict could be issued
    2   usage or input error

The stability-driven subcommands (report) exit 1 when the verdict is not
STABLE, so the tool is usable as a gate in continuous integration.
"""

from __future__ import annotations

import argparse
import sys

from pathvariance import __version__
from pathvariance.canon import CanonOptions
from pathvariance.distribution import build_distribution
from pathvariance.divergence import analyse_divergence
from pathvariance.report import (
    diverge_lines,
    entropy_lines,
    full_report,
    paths_lines,
    signatures_for,
)
from pathvariance.runs import ParseError, load_export
from pathvariance.stability import (
    DEFAULT_MIN_RUNS,
    DEFAULT_THRESHOLD,
    Verdict,
    assess,
)

USAGE_ERROR = 2


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("export", help="path to the repeated-run export JSON")
    parser.add_argument(
        "--task",
        default=None,
        help="task label, when the export is a bare list of runs",
    )
    parser.add_argument(
        "--args-sensitive",
        action="store_true",
        help="treat differing arguments as different paths",
    )
    parser.add_argument(
        "--collapse-repeats",
        action="store_true",
        help="collapse an immediately repeated tool call to one step",
    )


def _add_gate(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--min-runs",
        type=int,
        default=DEFAULT_MIN_RUNS,
        help=f"minimum run count gate (default {DEFAULT_MIN_RUNS})",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"stable modal share threshold (default {DEFAULT_THRESHOLD})",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pathvariance",
        description="Measure whether an agent takes the same tool path twice.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_paths = sub.add_parser("paths", help="print the path distribution table")
    _add_common(p_paths)

    p_entropy = sub.add_parser("entropy", help="print modal share and entropy")
    _add_common(p_entropy)
    _add_gate(p_entropy)

    p_diverge = sub.add_parser("diverge", help="print divergence analysis")
    _add_common(p_diverge)

    p_report = sub.add_parser("report", help="print the full report")
    _add_common(p_report)
    _add_gate(p_report)

    sub.add_parser("version", help="print the version and exit")
    return parser


def _options(args: argparse.Namespace) -> CanonOptions:
    return CanonOptions(
        argument_sensitive=args.args_sensitive,
        collapse_repeats=args.collapse_repeats,
    )


def _emit(lines: list[str]) -> None:
    sys.stdout.write("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        _emit([f"pathvariance {__version__}"])
        return 0

    try:
        export = load_export(args.export, task=args.task)
    except ParseError as exc:
        sys.stderr.write(f"error: {exc}\n")
