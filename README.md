# PathVariance

*Measure whether an agent solves the same task the same way twice.*

PathVariance reads a repeated-run export: one task, the same agent, many runs.
It canonicalises each run into a path signature, then reports how the runs
spread across paths, where they first diverge, and whether the sample is large
enough to say anything at all.

It is offline and deterministic. The same export always produces the same
report, byte for byte.

## The export

A repeated-run export is one JSON document: the task, and a list of runs where
each run is the ordered sequence of tool calls the agent made. A tool call has
a name and, optionally, arguments. The parser is strict about structure and
permissive about extra fields, so a richer export from a real harness still
loads.

## Commands

| Command | What it prints |
|---|---|
| `paths` | the path distribution table: label, id, count, share, route |
| `entropy` | distinct paths, modal share, Shannon entropy, normalised entropy |
| `diverge` | first divergence index and per-step agreement against the modal path |
| `report` | the full report: all of the above, in order |
| `version` | the version string |

Exit codes: `0` a verdict was issued, `1` the run count is below the minimum,
`2` usage or parse error.

## A real run

`python -m pathvariance paths samples/task-repeat.json`:

```
task: fix-null-deref-in-parser
runs: 12
distinct paths: 3

label  id         count  share   path
A      pe17777e0      8  66.7%  grep -> read -> edit -> test -> done
B      pfddfbe1f      2  16.7%  grep -> read -> read -> edit -> test -> done
C      p6b61031c      2  16.7%  grep -> read -> test -> edit -> test -> done
```

`python -m pathvariance entropy samples/task-repeat.json`:

```
task: fix-null-deref-in-parser
runs: 12
distinct paths: 3
modal path: A (pe17777e0)
modal share: 66.7%
shannon entropy: 1.252 bits
normalised entropy: 0.790
```

`python -m pathvariance diverge samples/task-repeat.json`:

```
task: fix-null-deref-in-parser
runs: 12
modal path: A (pe17777e0)
first divergence index: 2

step  agree  of     rate   modal token
   0     12     12  100.0%  grep
   1     12     12  100.0%  read
   2      8     12   66.7%  edit
   3      8     12   66.7%  test
   4      8     12   66.7%  done
```

Every run agrees on the opening moves and the disagreement starts at step 2:
the modal path edits the file, while two runs read again first and two others
test before editing. That is the debugging lead the tool exists to produce.

## Path signatures

A signature is the ordered sequence of tool calls, canonicalised into a stable
id. The one control that matters is **argument sensitivity**: with it off, two
runs that call the same tools in the same order but with different arguments
share a path; with it on, they do not. Pick per question. "Did the agent take
the same route" wants it off; "did it make the same decisions" wants it on.

## The stability gate

Three runs cannot describe a distribution. One path taking two of three runs
looks like 67 percent stability, and the confidence interval around that is so
wide the number misleads more than it informs. Below the minimum run count the
tool refuses to issue entropy or a verdict and says why, instead of printing a
figure that reads as authoritative.

## Repository layout

```
pathvariance/
  src/pathvariance/
    runs.py          strict repeated-run export parsing
    canon.py         path signatures, argument sensitivity
    distribution.py  distinct paths, modal share, Shannon entropy
    divergence.py    first divergence index, per-step agreement
    stability.py     minimum-run-count gate and verdict
    report.py        line-oriented deterministic rendering
    cli.py           subcommands and exit codes
  samples/           a 12-run export to try
  tests/             suite per module and for the CLI
  scripts/verify.py  the eight check quality gate
```

## Why entropy and not a single score

A single "stability score" hides the shape. Entropy says how spread the runs
are; the distribution table shows which routes exist; divergence says where
they part. Read together they tell a maintainer whether to fix the prompt, the
tool descriptions, or nothing at all.

## What it does not do

- It does not run the agent. It reads exports the harness already produces.
- It does not compare across tasks. One export is one task by design.
- It does not guess. Below the minimum run count, it says so.

## License

MIT. See `LICENSE`.

<!-- draft note 455 -->
