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
