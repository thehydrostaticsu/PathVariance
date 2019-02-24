# Sample export, an authored test vector

This directory holds one file, `task-repeat.json`. It is a hand-authored test
vector, not a capture from a live agent harness. It exists so the CLI has a
realistic input to run against and so the documented output is reproducible. It
is presented here as a fixture, never as production telemetry.

## What it represents

One task, `fix-null-deref-in-parser`, run 12 times. Each run is a sequence of
tool calls. The task is to locate a null dereference in a config parser, fix
