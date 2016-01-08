# PathVariance

*Measure whether an agent solves the same task the same way twice.*

PathVariance reads a repeated-run export: one task, the same agent, many runs.
It canonicalises each run into a path signature, then reports how the runs
spread across paths, where they first diverge, and whether the sample is large
enough to say anything at all.

It is offline and deterministic. The same export always produces the same
report, byte for byte.

