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
