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
