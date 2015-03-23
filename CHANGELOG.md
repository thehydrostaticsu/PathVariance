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
