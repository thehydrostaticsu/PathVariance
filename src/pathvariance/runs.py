"""Parse the repeated-run export.

The export is one task run many times. Each run is a sequence of tool calls,
where a tool call has a tool name and, optionally, arguments. The parser is
strict about structure and permissive about extra fields it does not use, so a
richer export from some agent harness still loads.

Accepted top level shapes, all JSON:

1. An object with a ``task`` string and a ``runs`` list. This is the canonical
   shape produced by ``samples/task-repeat.json``.

    {
      "task": "find-and-fix-null-deref",
      "runs": [
        {"run_id": "r01", "steps": [{"tool": "grep", "args": {...}}, ...]},
        ...
      ]
    }

2. A bare list of runs, when the task label is supplied out of band.

Each step must carry a ``tool`` string. Arguments are optional and may live
under ``args`` or ``arguments``; either is accepted and normalised to ``args``.
An ``ok`` boolean and a ``result`` field are read if present and preserved on
the step, because a caller may want to confirm that outcome parity held while
path parity did not.

Parsing never touches the network and never runs a subprocess. It only reads a
file or a string.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ParseError(ValueError):
    """Raised when the export does not match an accepted shape."""


@dataclass(frozen=True)
class Step:
    """One tool call within a run."""

    tool: str
    args: dict[str, Any] = field(default_factory=dict)
    ok: bool | None = None

    def arg_signature(self) -> str:
        """A stable string of the arguments, key sorted, for hashing.

        Values are rendered with ``json.dumps`` so nested structures compare
        deterministically. Missing arguments render as an empty object.
        """
        return json.dumps(self.args, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class Run:
    """One complete attempt at the task, an ordered list of steps."""

    run_id: str
    steps: tuple[Step, ...]
    outcome: bool | None = None

    def tools(self) -> tuple[str, ...]:
        return tuple(step.tool for step in self.steps)


@dataclass(frozen=True)
class Export:
    """The full repeated-run export for a single task."""

    task: str
    runs: tuple[Run, ...]

