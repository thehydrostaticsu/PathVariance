"""First divergence index and per-step agreement against the modal path.

Once the modal path is known, two further questions matter for debugging:

- At which step do runs first stray from the modal path? A late divergence
  means the agent agrees on the opening moves and only differs near the end. An
  early divergence means it disagrees about how to even start.
- How much do runs agree at each step? The per-step agreement rate is the
  fraction of runs whose token at that index equals the modal token, computed
  only over runs that are long enough to have a token there.

The first divergence index is the smallest step index at which at least one run
disagrees with the modal path, counting a run that has ended as a disagreement
once the modal path still has tokens. It is ``None`` when every run matches the
modal path exactly, which is the fully stable case.
"""

from __future__ import annotations

from dataclasses import dataclass
