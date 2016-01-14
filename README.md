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
