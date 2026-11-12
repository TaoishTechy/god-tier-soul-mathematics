"""IIRO/UBF palimpsest + coherence budget.

    P_hat |teaching> = alpha |teaching>,   alpha in [0, 1]
    dB_coh/dt = sum_i L_i - sum_i D_i
    Buddha calibration: B_coh = 1, S_sin = 0, F_hat |karma> = 0

alpha = 1 is lossless (zero-decay) record. alpha < 1 attenuates the
record each reconstruction; alpha = 0 is total loss.
"""
from __future__ import annotations


def palimpsest_apply(state, alpha: float):
    """P_hat(alpha) acting on a state vector: scales by alpha.

    Eigen-equation: P_hat |psi> = alpha |psi>. Returns the scaled state
    and the eigenvalue used (clamped to [0, 1]).
    """
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be in [0, 1]")
    return [alpha * x for x in state], alpha


def coherence_step(b_coh: float, gains, drains, dt: float = 1.0) -> float:
    """One Euler step of dB_coh/dt = sum L_i - sum D_i, clamped [0, 1]."""
    if dt < 0:
        raise ValueError("dt must be >= 0")
    return max(0.0, min(1.0, b_coh + (sum(gains) - sum(drains)) * dt))


def buddha_eigenstate():
    """The calibration eigenstate: B_coh=1, alpha=1, S_sin=0."""
    return {"b_coh": 1.0, "alpha": 1.0, "s_sin": 0.0, "forgiven": True}


def is_buddha(b_coh: float, alpha: float, s_sin: float) -> bool:
    return b_coh == 1.0 and alpha == 1.0 and s_sin == 0.0
