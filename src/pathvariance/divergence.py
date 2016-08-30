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


@dataclass(frozen=True)
class StepAgreement:
    """Agreement at one step index."""

    index: int
    modal_token: str
    agreeing: int
    considered: int

    @property
    def rate(self) -> float:
        return self.agreeing / self.considered if self.considered else 0.0


@dataclass(frozen=True)
class DivergenceReport:
    """Where and how runs leave the modal path."""

    modal_signature: tuple[str, ...]
    first_divergence_index: int | None
    per_step: tuple[StepAgreement, ...]

    @property
    def diverges(self) -> bool:
        return self.first_divergence_index is not None


def _token_at(signature: tuple[str, ...], index: int) -> str | None:
    return signature[index] if index < len(signature) else None


def analyse_divergence(
    signatures: list[tuple[str, ...]], modal: tuple[str, ...]
) -> DivergenceReport:
    """Compute first divergence index and per-step agreement.

    ``signatures`` is every run's signature. ``modal`` is the modal path to
    compare against. Per-step agreement is measured for each index in the modal
    path.
    """
