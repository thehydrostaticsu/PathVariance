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
