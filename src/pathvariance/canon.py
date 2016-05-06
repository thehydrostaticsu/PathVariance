"""Canonicalise a run into a path signature.

A path signature is the ordered sequence of tool calls, rendered as a tuple of
strings, that identifies the route the agent took. Two runs share a path when
their signatures are equal.

The single control that matters here is argument sensitivity. With it off, a
step is identified by its tool name alone, so ``grep(pattern="a")`` and
``grep(pattern="b")`` collapse to the same path. With it on, the argument
signature is folded in, so those two become different paths. The choice is the
user's, because whether an argument difference is a genuine route difference is
a judgement about the task, not something the tool can decide.

A ``PathSignature`` is deliberately a tuple of strings rather than a hash. The
readable form is what a report prints, and the tuple compares and comes out of
a dictionary deterministically, so identical input gives byte-identical output.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from pathvariance.runs import Run, Step


@dataclass(frozen=True)
class CanonOptions:
    """How to canonicalise. Defaults match the conservative reading."""

    argument_sensitive: bool = False
    # When set, a tool's calls are collapsed to one step no matter how many
    # times it repeats in a row. This models "used grep" rather than "used grep
    # three times". Off by default, because repetition is often signal.
    collapse_repeats: bool = False


def _step_token(step: Step, options: CanonOptions) -> str:
    if not options.argument_sensitive:
        return step.tool
    return f"{step.tool}({step.arg_signature()})"


def canonicalise(run: Run, options: CanonOptions | None = None) -> tuple[str, ...]:
    """Return the ordered path signature for one run."""
    opts = options or CanonOptions()
    tokens: list[str] = []
    for step in run.steps:
        token = _step_token(step, opts)
        if opts.collapse_repeats and tokens and tokens[-1] == token:
            continue
        tokens.append(token)
    return tuple(tokens)


def signature_id(signature: tuple[str, ...]) -> str:
    """A short stable identifier for a signature, for compact labelling.

    This is a truncated SHA-256 over the joined tokens. It is not used for any
    security purpose, only to give each distinct path a stable short handle
    such as ``p1a2b3c4`` in reports and assets.
    """
    joined = "\x1f".join(signature)
    digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return "p" + digest[:8]


def label_paths(signatures: list[tuple[str, ...]]) -> dict[tuple[str, ...], str]:
    """Assign ordinal labels A, B, C ... to signatures by first appearance.

    Ordering follows first appearance in the given list so labels are stable
    against the run order in the export, which keeps report output diffable.
    """
    labels: dict[tuple[str, ...], str] = {}
