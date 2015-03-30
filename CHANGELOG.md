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
