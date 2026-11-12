"""Correlation Continuum: non-commutative correlation algebra.

    [O_i, O_j] = i hbar Omega_ij + lambda C_ijk O_k

Core data is a stable pattern in this algebra; persistence lengths
determine survival of entanglement history. hbar is set to 1 in
natural units unless the caller passes another value — the algebra
is formal, so the unit choice is documented, not hidden.
"""
from __future__ import annotations

import math


def commutator(omega_ij: float, lam: float, c_ijk, o_k, hbar: float = 1.0) -> complex:
    """[O_i, O_j] for one (i, j) pair: i*hbar*Omega + lambda * sum_k C_ijk O_k."""
    return 1j * hbar * omega_ij + lam * sum(c * o for c, o in zip(c_ijk, o_k))


def persistence_length(correlation: float, decay_rate: float) -> float:
    """Length over which entanglement history survives: L = -ln(c)/gamma.

    correlation in (0, 1]; decay_rate > 0. Returns inf for correlation
    1 (perfect persistence) — the lossless-history limit.
    """
    if not 0.0 < correlation <= 1.0:
        raise ValueError("correlation must be in (0, 1]")
    if decay_rate <= 0:
        raise ValueError("decay_rate must be > 0")
    if correlation == 1.0:
        return math.inf
    return -math.log(correlation) / decay_rate
