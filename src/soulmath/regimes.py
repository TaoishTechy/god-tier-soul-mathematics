"""Three regimes (USIF v2.0 §6 / v2.1 §6).

Ordinary:      B_coh < 0.95, F_hat partial
Arahant:       B_coh >= 0.95, CTC fixed point dS/dphi = 0, F_hat largely active
Buddha:        B_coh = 1, alpha = 1, F_hat full, S_sin = 0, knot unknotted

Sa-upadisesa vs anupadisesa is exactly residual scar/torsion present
vs fully trivialised.
"""
from __future__ import annotations

REGIMES = ("ordinary", "arahant", "buddha")


def classify_regime(b_coh: float, alpha: float, s_sin: float,
                    forgiveness_strength: float, knot_unknotted: bool,
                    scar_trivial: bool, torsion_free_flag: bool,
                    ctc_fixed_point: bool = False) -> str:
    """Classify a soul's regime from its calibration numbers."""
    if (b_coh == 1.0 and alpha == 1.0 and s_sin == 0.0
            and forgiveness_strength >= 1.0 and knot_unknotted
            and scar_trivial and torsion_free_flag):
        return "buddha"
    if b_coh >= 0.95 and forgiveness_strength >= 0.5 and ctc_fixed_point:
        return "arahant"
    # High coherence without the CTC fixed point is still ordinary in
    # the strict reading; the threshold alone does not promote it.
    return "ordinary"


def remainder_for(regime: str) -> str:
    return {
        "ordinary": "full complex + Tor + scar",
        "arahant": "purified pattern, reduced Tor/scar",
        "buddha": "no private residual packet (anupadisesa)",
    }[regime]
