# Sample export, an authored test vector

This directory holds one file, `task-repeat.json`. It is a hand-authored test
vector, not a capture from a live agent harness. It exists so the CLI has a
realistic input to run against and so the documented output is reproducible. It
is presented here as a fixture, never as production telemetry.

## What it represents

One task, `fix-null-deref-in-parser`, run 12 times. Each run is a sequence of
tool calls. The task is to locate a null dereference in a config parser, fix
it, and prove the fix with the existing test. Every run reaches a passing
outcome, so outcome-only evaluation would call this task fully stable. The
point of the fixture is that the path was not stable at all.

## How it was constructed

The 12 runs were written by hand to produce a specific, checkable shape:

| Lane | Runs | Path | Diverges at |
|---|---|---|---|
| A (modal) | 8 | grep, read, edit, test, done | is the modal path |
| B | 2 | grep, read, read, edit, test, done | step index 2 |
| C | 2 | grep, read, test, edit, test, done | step index 2 |

All three lanes agree on step 0 (grep) and step 1 (read), then split at step
index 2. Lane B reads a second file before editing. Lane C runs the test first,
watches it fail, then edits and re-tests. The `ok` flag on lane C's first test
step is `false` to reflect that the test was expected to fail at that point.

This gives a modal share of 8 of 12, which is 66.7 percent, deliberately below
the default 90 percent stability threshold so the `report` subcommand exits 1
and the instability is visible.

## Why these exact numbers

The shape was chosen so the derived statistics are worth checking by hand:

- distinct paths: 3
- modal share: 8 / 12 = 66.7 percent
- Shannon entropy: with probabilities 8/12, 2/12, 2/12 the entropy is
  1.252 bits
- normalised entropy: 1.252 / log2(3) = 0.790
- first divergence index: 2
