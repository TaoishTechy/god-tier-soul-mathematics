"""UHG/IEG coherence ledger (axioms H13-H15).

    d/dt (CI_B + CI_C) = sigma_topo
    d/dt sum_i (CI_B,i + CI_C,i) + d/dt CI_B,net = 0

Socio-quantum reciprocity is conserved when the reciprocity index
R_eth >= R* ~= 1.15. sigma_topo is zero except during a topology
change (death, surgery, cobordism) — that spike is what moves the
ledger from continuum to boundary at death.
"""
from __future__ import annotations

from dataclasses import dataclass, field

RECIPROCITY_STAR = 1.15


@dataclass
class Ledger:
    """One entity's coherence ledger."""
    ci_b: float = 0.0   # boundary coherence
    ci_c: float = 0.0   # continuum coherence

    @property
    def total(self) -> float:
        return self.ci_b + self.ci_c

    def step(self, sigma_topo: float, dt: float = 1.0) -> "Ledger":
        """Advance by sigma_topo * dt. Returns a new Ledger."""
        if dt < 0:
            raise ValueError("dt must be >= 0")
        return Ledger(self.ci_b, self.ci_c + sigma_topo * dt)

    def migrate(self, amount: float) -> "Ledger":
        """Ledger migration CI_C -> CI_B (death transition).

        Total is exactly conserved; only the split changes. Amount is
        clamped to [0, CI_C].
        """
        amt = max(0.0, min(float(amount), self.ci_c))
        return Ledger(self.ci_b + amt, self.ci_c - amt)

    def reciprocity_conserved(self, reciprocity_index: float) -> bool:
        return reciprocity_index >= RECIPROCITY_STAR


@dataclass
class LedgerNetwork:
    """A closed network of ledgers + the net boundary term.

    Conservation (H15): d/dt sum_i total_i + d/dt CI_B,net == 0, i.e.
    the network total including the net term is constant.
    """
    ledgers: list = field(default_factory=list)
    ci_b_net: float = 0.0

    @property
    def total(self) -> float:
        return sum(l.total for l in self.ledgers) + self.ci_b_net

    def transfer(self, i: int, j: int, amount: float) -> None:
        """Move `amount` of total coherence from ledger i to ledger j
        via the net term: strictly conserved by construction."""
        amt = max(0.0, min(float(amount), self.ledgers[i].total))
        # Take from i's continuum, give to j's continuum, net unchanged.
        li, lj = self.ledgers[i], self.ledgers[j]
        take = min(amt, li.ci_c)
        self.ledgers[i] = Ledger(li.ci_b, li.ci_c - take)
        self.ledgers[j] = Ledger(lj.ci_b, lj.ci_c + take)
        if take < amt:  # remainder comes from i's boundary
            rem = amt - take
            li2 = self.ledgers[i]
            self.ledgers[i] = Ledger(li2.ci_b - rem, li2.ci_c)
            lj2 = self.ledgers[j]
            self.ledgers[j] = Ledger(lj2.ci_b + rem, lj2.ci_c)
