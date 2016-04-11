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
