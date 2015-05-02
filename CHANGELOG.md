# Changelog

All notable changes to PathVariance are documented here. The format follows
Keep a Changelog, and the project uses semantic versioning.

## [Unreleased]

### Changed

- Normalised entropy wording is under review for the next patch.

## [1.0.2] - 2026-06-23

### Fixed

- Ties in modal share resolve to the lexicographically smallest path id, so
  two runs over the same export are identical.

## [1.0.1] - 2025-10-07

### Fixed

- Normalised entropy divides by the entropy of the observed path count, not
  the theoretical maximum, so a two path export can reach 1.0.

## [1.0.0] - 2024-09-24

### Added

- Stable CLI contract for paths, entropy, diverge, report, and version, exit
  codes 0/1/2.
- Tests pin the divergence arithmetic across the bundled export.

## [0.9.0] - 2023-07-18

### Added

- Full report mode: distribution, entropy, and divergence in one run.

## [0.8.0] - 2022-11-08

### Added

- Argument sensitivity as a control on the canonicaliser.

## [0.7.0] - 2021-03-30

### Added

- A 12 run sample export and the README walkthrough captured from it.

## [0.6.0] - 2020-09-22

### Added

- Test suite covering runs, canon, and the CLI.

## [0.5.0] - 2019-06-11

### Added

- Report renderer with line oriented, deterministic output.
- CLI entry point with subcommands.

## [0.4.0] - 2018-10-09

### Added

- First divergence index and per step agreement against the modal path.
