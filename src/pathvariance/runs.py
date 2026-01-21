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

    def __len__(self) -> int:
        return len(self.runs)


def _coerce_step(raw: Any, run_id: str, index: int) -> Step:
    if not isinstance(raw, dict):
        raise ParseError(
            f"run {run_id!r} step {index}: expected an object, got "
            f"{type(raw).__name__}"
        )
    tool = raw.get("tool")
    if not isinstance(tool, str) or not tool:
        raise ParseError(
            f"run {run_id!r} step {index}: missing a non-empty 'tool' string"
        )
    args = raw.get("args", raw.get("arguments", {}))
    if args is None:
        args = {}
    if not isinstance(args, dict):
        raise ParseError(
            f"run {run_id!r} step {index}: 'args' must be an object"
        )
    ok = raw.get("ok")
    if ok is not None and not isinstance(ok, bool):
        raise ParseError(
            f"run {run_id!r} step {index}: 'ok' must be a boolean when present"
        )
    return Step(tool=tool, args=args, ok=ok)


def _coerce_run(raw: Any, index: int) -> Run:
    if not isinstance(raw, dict):
        raise ParseError(f"run {index}: expected an object")
    run_id = raw.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        run_id = f"run{index:03d}"
    steps_raw = raw.get("steps")
    if not isinstance(steps_raw, list):
        raise ParseError(f"run {run_id!r}: 'steps' must be a list")
    steps = tuple(
        _coerce_step(step, run_id, i) for i, step in enumerate(steps_raw)
    )
    outcome = raw.get("outcome")
    if outcome is not None and not isinstance(outcome, bool):
        raise ParseError(f"run {run_id!r}: 'outcome' must be a boolean")
    return Run(run_id=run_id, steps=steps, outcome=outcome)


def parse_export(data: Any, task: str | None = None) -> Export:
    """Turn already decoded JSON into an ``Export``.

    ``task`` overrides or supplies the task label. When the data is a bare list
    of runs, ``task`` is required unless it defaults to the string ``task``.
    """
    if isinstance(data, dict) and "runs" in data:
        label = task or data.get("task")
        if not isinstance(label, str) or not label:
            raise ParseError("export is missing a non-empty 'task' string")
        runs_raw = data.get("runs")
    elif isinstance(data, list):
        label = task or "task"
        runs_raw = data
    else:
        raise ParseError(
            "export must be an object with 'runs' or a bare list of runs"
        )
    if not isinstance(runs_raw, list) or not runs_raw:
        raise ParseError("export has no runs")
    runs = tuple(_coerce_run(run, i) for i, run in enumerate(runs_raw))
    return Export(task=label, runs=runs)


def load_export(source: str | Path, task: str | None = None) -> Export:
    """Load and parse an export from a file path or a JSON string."""
    text: str
    path = Path(source)
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = str(source)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ParseError(f"export is not valid JSON: {exc}") from exc
    return parse_export(data, task=task)
