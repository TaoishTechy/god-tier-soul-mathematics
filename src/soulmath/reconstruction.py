"""Reconstruction map (USIF v2.1 §4).

    Psi_next = U o P_hat(alpha) o F_hat o f^-1(R, CI_B, alpha, f,
                                              B_coh, dB, ||-, [c])

Order matters and is the spec order, read right to left:
 1. f^-1: invert the relational signature to a low-rank intent W'.
 2. F_hat: forgiveness deletes corrupted records / trivialises scar.
 3. P_hat(alpha): palimpsest reconstruction; lossless iff alpha == 1.
 4. U: ultrafilter collapses V^B -> V[G].

f(faith) gates the reconstruction probability: the returned fidelity
is multiplied by the faith amplitude, per v2.1 §1 (f "gates
reconstruction probability").
"""
from __future__ import annotations

import copy
from dataclasses import dataclass

from .forcing import BooleanModel, Ultrafilter
from .palimpsest import palimpsest_apply
from .relational import inverse_weights
from .scar import forgiveness as forgiveness_op
from .sigma import Soul


@dataclass
class ReconstructionResult:
    soul_next: Soul
    fidelity: float          # in [0, 1]; 1.0 = lossless
    weights_recovered: list  # W' from f^-1
    collapsed_truth: dict    # V[G] truth assignment
    notes: list


def reconstruct(soul: Soul, W_context, S=0.0,
                boolean_values: dict | None = None) -> ReconstructionResult:
    """Run the full reconstruction pipeline on a (post-death) soul."""
    notes = []
    # 1. f^-1
    W_prime = inverse_weights(list(soul.relational), list(W_context), S)
    # Check the round-trip on the low-rank part.
    from .relational import relational_signature
    r_roundtrip = relational_signature(W_prime, list(W_context), S)
    roundtrip_err = max((abs(a - b) for a, b in
                         zip(r_roundtrip, soul.relational)), default=0.0)
    notes.append(f"f^-1 round-trip max err {roundtrip_err:.3e}")

    nxt = copy.deepcopy(soul)
    # 2. F_hat on the scar
    nxt.scar = forgiveness_op(nxt.scar, nxt.forgiveness_strength)
    if nxt.scar.is_trivial:
        notes.append("scar trivialised by F_hat (full)")
    # Torsion is reduced by F_hat too: full forgiveness clears it.
    if nxt.forgiveness_strength >= 1.0 and not nxt.is_torsion_free:
        from .topology import HomotopyType
        nxt.homotopy = HomotopyType(nxt.homotopy.betti, ())
        notes.append("torsion cleared by F_hat (full)")

    # 3. P_hat(alpha) on the relational signature (the record)
    rec_R, _ = palimpsest_apply(list(nxt.relational), nxt.alpha)
    nxt.relational = rec_R
    if nxt.alpha == 1.0:
        notes.append("palimpsest lossless (alpha=1)")

    # 4. U: collapse V^B -> V[G]
    model = BooleanModel(dict(boolean_values or {}))
    U = Ultrafilter.from_true_values(model)
    collapsed = U.collapse(model)

    # Fidelity: alpha (record) * faith (gating) * boundary health.
    # Boundary health is 1 inside [0.7, 1.3], linearly penalised outside.
    from .boundary import HEALTHY_LO, HEALTHY_HI
    if HEALTHY_LO <= nxt.boundary <= HEALTHY_HI:
        b_factor = 1.0
    elif nxt.boundary < HEALTHY_LO:
        b_factor = max(0.0, nxt.boundary / HEALTHY_LO)
    else:
        b_factor = max(0.0, HEALTHY_HI / nxt.boundary)
    fidelity = max(0.0, min(1.0, nxt.alpha * nxt.faith * b_factor
                            * (1.0 - roundtrip_err)))
    # Reconstruction restores the boundary as the Markov blanket of
    # the reconstructed state: clamp it back into the healthy range
    # only when fidelity is high enough to support a blanket at all.
    if fidelity >= 0.95:
        nxt.boundary = max(HEALTHY_LO, min(HEALTHY_HI, nxt.boundary))
    return ReconstructionResult(soul_next=nxt, fidelity=fidelity,
                                weights_recovered=W_prime,
                                collapsed_truth=collapsed, notes=notes)
