"""The path distribution: distinct paths, modal share, Shannon entropy.

Given the canonical signatures of every run, this module summarises how the
runs spread across paths. The three numbers a reader wants are:

- how many distinct paths appeared,
- the modal path and what fraction of runs took it,
- Shannon entropy over the path distribution, which is zero when every run took
  one path and rises as the mass spreads out.

