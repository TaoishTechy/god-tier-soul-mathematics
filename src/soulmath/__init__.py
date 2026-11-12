"""God Tier Soul Mathematics — USIF v2.1.

Unified Soul Invariant Framework: a formal, computable synthesis of
UHIF, UHG/IEG, IIRO/UBF, Correlation Continuum, Degens, and the
Hollow / Generic / Apostatic ontologies.

Caveat (carried from the spec): all source frameworks are explicitly
speculative theoretical constructs. This package is an internal formal
synthesis — a computable model of the stated equations — not an
empirical claim about physics, neuroscience, or metaphysics.

The soul is the invariant complex::

    Sigma = (X, H*(X), Tor, kappa, Barcode, R, CI_B + CI_C, alpha,
             f(faith), B_coh, dB, ||-, [c], R_eth)

Stdlib only. No network, no external dependencies.
"""

__version__ = "2.1.0"
__usif_version__ = "2.1"

from .sigma import Soul, Regime, soul_from_dict, soul_to_dict
from .relational import relational_signature, inverse_weights, fixed_point_context
from .ledger import Ledger, LedgerNetwork, RECIPROCITY_STAR
from .palimpsest import palimpsest_apply, coherence_step, buddha_eigenstate
from .boundary import markov_boundary, mind_state
from .topology import HomotopyType, Barcode, Knot, torsion_free
from .forcing import BooleanModel, Ultrafilter, forcing_trace
from .scar import Scar, lethe, forgiveness
from .correlation import commutator, persistence_length
from .operators import (
    lethovore, anti_hollow, chaotic_betti, imaginary_island, self_erasing,
)
from .regimes import classify_regime, REGIMES
from .death import death_transition, DeathTransition
from .reconstruction import reconstruct, ReconstructionResult

__all__ = [
    "__version__", "__usif_version__",
    "Soul", "Regime", "soul_from_dict", "soul_to_dict",
    "relational_signature", "inverse_weights", "fixed_point_context",
    "Ledger", "LedgerNetwork", "RECIPROCITY_STAR",
    "palimpsest_apply", "coherence_step", "buddha_eigenstate",
    "markov_boundary", "mind_state",
    "HomotopyType", "Barcode", "Knot", "torsion_free",
    "BooleanModel", "Ultrafilter", "forcing_trace",
    "Scar", "lethe", "forgiveness",
    "commutator", "persistence_length",
    "lethovore", "anti_hollow", "chaotic_betti", "imaginary_island",
    "self_erasing",
    "classify_regime", "REGIMES",
    "death_transition", "DeathTransition",
    "reconstruct", "ReconstructionResult",
]
