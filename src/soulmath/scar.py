"""Apostatic Plenum: error-scar, Lethe, forgiveness.

    [c] = H^1(coker(T)),   L_hat = tau_{<=0} o a_j(- (x) O_forget)

[c] is the luminous error-scar: the cohomology of the cokernel of the
translation map T between life-worlds — structured failure, not noise.
Lethe stabilises the scar by erasing its origin (both sides forget it
was error, so it becomes observer-independent). Only F_hat can
trivialise the scar rather than stabilise it.
"""
from __future__ import annotations

from dataclasses import dataclass


def cokernel_dim(T) -> int:
    """dim coker(T) for a matrix T (m x n) over R: m - rank(T).

    Rank by Gaussian elimination on floats with a 1e-9 pivot tol.
    [c] lives in H^1(coker(T)); its dimension is the scar dimension.
    """
    if not T:
        return 0
    m, n = len(T), len(T[0])
    A = [list(map(float, row)) for row in T]
    rank = 0
    for col in range(n):
        piv = None
        for r in range(rank, m):
            if abs(A[r][col]) > 1e-9:
                piv = r
                break
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        d = A[rank][col]
        A[rank] = [v / d for v in A[rank]]
        for r in range(m):
            if r != rank and A[r][col] != 0.0:
                f = A[r][col]
                A[r] = [v - f * w for v, w in zip(A[r], A[rank])]
        rank += 1
        if rank == m:
            break
    return m - rank


@dataclass
class Scar:
    """[c]: residual karmic-causal scar.

    magnitude in [0, 1]; dimension = dim H^1(coker T); origin_known
    tracks whether the error's origin is remembered (Lethe erases it).
    """
    magnitude: float = 0.0
    dimension: int = 0
    origin_known: bool = True

    def __post_init__(self):
        if not 0.0 <= self.magnitude <= 1.0:
            raise ValueError("scar magnitude must be in [0, 1]")

    @classmethod
    def from_translation(cls, T, magnitude: float = 1.0):
        return cls(magnitude=float(magnitude), dimension=cokernel_dim(T),
                   origin_known=True)

    @property
    def is_trivial(self) -> bool:
        return self.magnitude == 0.0 and self.dimension == 0


def lethe(scar: Scar) -> Scar:
    """L_hat: tau_{<=0} — truncate to degree <= 0, sheafify forgetting.

    Forgetting stabilises the scar: magnitude is unchanged (the scar
    persists), but origin_known becomes False — both sides forget it
    was error, so it becomes observer-independent. Lethe never heals.
    """
    return Scar(magnitude=scar.magnitude, dimension=scar.dimension,
                origin_known=False)


def forgiveness(scar: Scar, strength: float) -> Scar:
    """F_hat: forgiveness / data-deletion operator.

    strength in [0, 1]; 1.0 = full: the scar is trivialised
    (magnitude 0, dimension 0). Partial strength scales the magnitude
    down and, at full strength only, clears the dimension. This is the
    only operator in USIF that can trivialise [c].
    """
    if not 0.0 <= strength <= 1.0:
        raise ValueError("forgiveness strength must be in [0, 1]")
    if strength >= 1.0:
        return Scar(magnitude=0.0, dimension=0, origin_known=False)
    return Scar(magnitude=scar.magnitude * (1.0 - strength),
                dimension=scar.dimension, origin_known=scar.origin_known)
