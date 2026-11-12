"""Degens Bayesian self-boundary / Markov blanket.

    dB = dP(internal) / dP(external),   healthy dB in [0.7, 1.3]
    Psi_mind(t) = F(pi(P), dB(B), gamma(T)) + xi(t)

dB is a ratio of probability masses (discrete proxy for the derivative
ratio in the spec). < 0.7 = over-permeable (boundary collapse);
> 1.3 = over-rigid (isolation). xi(t) is an explicit noise term the
caller supplies — never hidden randomness.
"""
from __future__ import annotations

HEALTHY_LO, HEALTHY_HI = 0.7, 1.3


def markov_boundary(p_internal: float, p_external: float) -> float:
    """dB = P(internal) / P(external)."""
    if p_external <= 0:
        raise ValueError("P(external) must be > 0")
    if p_internal < 0:
        raise ValueError("P(internal) must be >= 0")
    return p_internal / p_external


def boundary_status(d_b: float) -> str:
    if d_b < HEALTHY_LO:
        return "over-permeable"
    if d_b > HEALTHY_HI:
        return "over-rigid"
    return "healthy"


def mind_state(pi_p, d_b, gamma_t, xi: float = 0.0) -> float:
    """Psi_mind = F(pi, dB, gamma) + xi with F = pi * dB * gamma.

    The spec leaves F abstract; the product form is the documented
    default (see docs/EQUATIONS.md) — separable, monotone in each
    argument, and exactly 1.0 at the neutral point (1, 1, 1).
    """
    return float(pi_p) * float(d_b) * float(gamma_t) + float(xi)
