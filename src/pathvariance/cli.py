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
