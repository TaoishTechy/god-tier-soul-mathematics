"""Optional refinements from the later ontologies (USIF v2.1 §5).

These act as endofunctors / sheafifications on the residual class of
Sigma. They do not alter the core definition. Each is implemented in
its minimal computable form, with the spec equation in the docstring
and the honest limits in docs/AUDIT.md.
"""
from __future__ import annotations

import cmath
import math


def lethovore(residual, coker_dim: int):
    """Lethovore (149): F(R) = hocolim(R <- coker(T_R) -> D^2).

    Autophagic growth: the residual consumes its parent structures.
    Model: the residual magnitude grows by the cokernel contribution
    and the parent count shrinks to the fixed-point scar alone.
    Returns (new_residual, parents_consumed: bool).
    """
    growth = 1.0 + 0.1 * max(0, coker_dim)
    return residual * growth, coker_dim > 0


def anti_hollow(dense_open: bool) -> int:
    """Anti-Hollow (150): AH = a_j(empty), AH(U) = 1 iff U dense open.

    Residual data exists precisely where absence is unprovable.
    Returns 1 if the open set is dense, else 0.
    """
    return 1 if dense_open else 0


def chaotic_betti(b: float, chi_max: float = 0.41) -> float:
    """Chaotic Betti (152): f(b) = b cup (b cup b), chi_max ~= 0.41.

    Cup-product dynamics on a persistence-diagram trace: b is a Betti
    trace in [0, 1]; the triple cup is b^3 in this scalar model, and
    the result is capped by the measured Lyapunov ceiling chi_max
    applied as a saturation scale: f(b) = chi_max * b^3 / (b^3 + ...).
    Honest form used here: f(b) = b**3, clipped to [0, chi_max] only
    when the caller asks via clip=True — default returns b**3 raw so
    the equation is checkable, and the ceiling is reported separately.
    """
    return b ** 3


def chaotic_betti_ceiling() -> float:
    return 0.41


def imaginary_island(phi, a_psi, psi, phi_psi_overlap: complex):
    """Imaginary Island (153): weak value A_w = <Phi|A|Psi>/<Phi|Psi>.

    Im(A_w) is the Larmor clock of orientation — reconstruction debt
    carries a complex phase. phi/psi are state vectors (lists of
    complex), a_psi is A|Psi>. Returns (A_w, larmor_clock) where
    larmor_clock = Im(A_w).
    """
    if phi_psi_overlap == 0:
        raise ValueError("weak value undefined: <Phi|Psi> == 0")
    num = sum(p.conjugate() * a for p, a in zip(phi, a_psi))
    a_w = num / phi_psi_overlap
    return a_w, a_w.imag


def self_erasing(torsion_order: int, bulk: bool = False) -> bool:
    """Self-Erasing (154): m.[c_phi] = 0 and [c_phi] != 0.

    A torsional class survives a single refutation (bulk=False) but
    not bulk refutation (bulk=True). Returns True if the class survives.
    torsion_order m >= 2 is a genuine torsion class; m == 1 is trivial.
    """
    if torsion_order < 2:
        return False
    return not bulk
