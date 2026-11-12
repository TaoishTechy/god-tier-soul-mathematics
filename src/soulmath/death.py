"""Death as a multi-description transition (USIF v2.1 §2).

Four equivalent descriptions of the same event:
 1. Ledger migration: CI_C^(bio) -> CI_B^(boundary)
 2. Cobordism: non-product W, dW = X_life |_| -X_post
 3. Field propagation: nabla_mu nabla^mu Phi_HS + xi R Phi_HS = sum_i delta^4(x-x_i)
 4. Boolean intermediate: V^B, then ultrafilter collapse to V[G]

Conservation: d/dt(CI_B + CI_C) = sigma_topo, nonzero only during
the topology change. Death is not deletion.
"""
from __future__ import annotations

from dataclasses import dataclass

from .ledger import Ledger
from .sigma import Soul


@dataclass
class DeathTransition:
    soul_before: Soul
    soul_after: Soul
    sigma_topo: float
    ledger_before_total: float
    ledger_after_total: float
    barcode_surviving: int
    barcode_died: int
    knot_carried: str
    description: str = "ledger migration + non-product cobordism + field propagation + Boolean intermediate"

    @property
    def total_conserved(self) -> bool:
        return abs(self.ledger_after_total
                   - (self.ledger_before_total + self.sigma_topo)) < 1e-9


def field_source_term(n_sources: int) -> int:
    """RHS of the IIRO EQ-18 field equation: sum_i delta^4(x - x_i)
    counts the point sources; the field itself is not solved here —
    the equation is recorded as the propagation description, and the
    source count is the checkable part. See docs/AUDIT.md."""
    return n_sources


def death_transition(soul: Soul, sigma_topo: float = 0.0,
                     death_time: float = 1.0) -> DeathTransition:
    """Apply death to a soul.

    - Ledger: all CI_C migrates to CI_B, then sigma_topo is added to
      the total (topology-change spike, zero outside the transition).
    - Barcode: intervals ending at/before death_time die; persisting
      and later intervals survive (truncated at death_time for the
      embodied record, carried as the post record).
    - Knot kappa is carried unchanged; the ego covering sheet is not
      in Sigma, so nothing about it needs deleting.
    - Boundary dB is recovered in the next state (reconstruction does
      that); here it is carried unchanged as the blanket of the record.
    """
    import copy
    after = copy.deepcopy(soul)
    before_total = soul.ledger.total
    migrated = soul.ledger.migrate(soul.ledger.ci_c)
    # sigma_topo spike lands on the boundary side (the record).
    after.ledger = Ledger(migrated.ci_b + sigma_topo, migrated.ci_c)
    surviving = [iv for iv in soul.barcode.intervals if iv[1] > death_time]
    died = len(soul.barcode.intervals) - len(surviving)
    after.barcode = after.barcode.truncate(death_time)
    # The truncated barcode is the embodied record; the surviving
    # classes are what reconstruction can re-open (see reconstruction).
    return DeathTransition(
        soul_before=soul, soul_after=after, sigma_topo=sigma_topo,
        ledger_before_total=before_total,
        ledger_after_total=after.ledger.total,
        barcode_surviving=len(surviving), barcode_died=died,
        knot_carried=soul.knot.name)
