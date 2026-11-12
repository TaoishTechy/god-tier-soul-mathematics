"""Hollow ontology: homotopy type, cohomology, torsion, knot, barcode.

The soul's topological core, in computable miniature:

- X: homotopy type, recorded as (betti numbers, torsion coefficients,
  euler characteristic). chi = sum_k (-1)^k b_k.
- H*(X; Z): cohomology ring — here the cup-product grammar is stored
  as a sparse product table on generators; the ring axioms are
  checkable (associativity on the stored table is tested).
- Tor(H_*(X)): torsion subgroup, as a list of cyclic orders n >= 2
  (Z_n factors). Empty == torsion-free. Reduced by F_hat; zero at
  full liberation.
- kappa(X): knot invariant — (knot name, crossing number, determinant,
  signature, alexander coeffs). Unknotted iff crossing == 0 and
  determinant == 1. Personality is a knot invariant (Framework 11).
- Barcode(X): persistent homology barcode — intervals (birth, death);
  persistence = death - birth; death = inf means the class persists.
  Memory is a barcode (Framework 9), not raw storage.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(frozen=True)
class HomotopyType:
    betti: tuple = (1, 0)          # b0, b1, ... (b0=1: connected)
    torsion: tuple = ()            # cyclic orders, e.g. (2,) = Z_2

    @property
    def euler_characteristic(self) -> int:
        return sum(((-1) ** k) * b for k, b in enumerate(self.betti))

    @property
    def is_torsion_free(self) -> bool:
        return len(self.torsion) == 0

    def cup_product(self, a: int, b: int, table: dict | None = None) -> int:
        """Cup product of generator degrees a, b via a sparse table.

        Default table is the exterior algebra on one degree-1 generator
        (a*b = generator in degree a+b when both are 0/1 and distinct).
        Callers with a real ring pass their own table.
        """
        if table is not None:
            return table.get((a, b), 0)
        if a == 0:
            return b
        if b == 0:
            return a
        return 0  # x cup x = 0 in the exterior algebra


def torsion_free(torsion) -> bool:
    return len(list(torsion)) == 0


@dataclass
class Barcode:
    """Persistent homology barcode: list of (birth, death) intervals.

    death may be float('inf') for a persisting class.
    """
    intervals: list = field(default_factory=list)

    def __post_init__(self):
        for b, d in self.intervals:
            if d != math.inf and d < b:
                raise ValueError(f"invalid interval ({b}, {d}): death < birth")

    @property
    def persistences(self):
        return [d - b if d != math.inf else math.inf for b, d in self.intervals]

    @property
    def finite_persistence(self):
        return [p for p in self.persistences if p != math.inf]

    @property
    def total_persistence(self) -> float:
        return sum(self.finite_persistence)

    @property
    def n_persisting(self) -> int:
        return sum(1 for _, d in self.intervals if d == math.inf)

    def truncate(self, t: float) -> "Barcode":
        """Death truncates the barcode at time t: classes alive past t
        are cut to (birth, t); classes born after t are dropped.
        This is the 'truncated / reconstructed, not raw storage' rule.
        """
        out = []
        for b, d in self.intervals:
            if b >= t:
                continue
            out.append((b, min(d, t)))
        return Barcode(out)

    def betti_at(self, t: float) -> int:
        return sum(1 for b, d in self.intervals if b <= t < d)


@dataclass(frozen=True)
class Knot:
    """Knot invariant kappa: identity / personality invariant.

    determinant: |Delta(-1)|; signature: classical Murasugi signature;
    alexander: coefficients of the Alexander polynomial (low to high).
    The unknot is (0 crossings, det 1, sig 0). A non-trivial knot is
    never 'unknotted' by relabelling — only F_hat / awakening can
    unknot it, and that is an explicit operation in regimes.py.
    """
    name: str = "unknot"
    crossings: int = 0
    determinant: int = 1
    signature: int = 0
    alexander: tuple = (1,)

    @property
    def is_unknotted(self) -> bool:
        return self.crossings == 0 and self.determinant == 1

    @classmethod
    def trefoil(cls):
        return cls("trefoil", 3, 3, -2, (1, -1, 1))

    @classmethod
    def figure_eight(cls):
        return cls("figure-eight", 4, 5, 0, (1, -3, 1))
