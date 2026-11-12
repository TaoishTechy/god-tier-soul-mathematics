"""Doctor / verify gates — the MOGOPs-style honest check.

`verify()` runs every checkable identity in USIF v2.1 and returns a
list of (name, passed, detail). Nothing here claims an empirical
result: each gate is either a mathematical identity of the model or
an explicit NOT-RUN / NOT-IMPLEMENTED admission (see docs/AUDIT.md).
"""
from __future__ import annotations

import math

from . import __version__
from .boundary import HEALTHY_LO, HEALTHY_HI, markov_boundary
from .correlation import commutator
from .ledger import Ledger, LedgerNetwork, RECIPROCITY_STAR
from .palimpsest import coherence_step, palimpsest_apply
from .relational import fixed_point_context, inverse_weights, relational_signature
from .scar import Scar, cokernel_dim, forgiveness, lethe


def verify():
    checks = []

    def gate(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    # G0: R = tanh(WC+S) round-trips through f^-1
    W = [[0.5, -0.2], [0.1, 0.8]]
    C = [0.6, -0.4]
    R = relational_signature(W, C, 0.1)
    Wp = inverse_weights(R, C, 0.1)
    R2 = relational_signature(Wp, C, 0.1)
    gate("G0 relational round-trip", max(abs(a - b) for a, b in zip(R, R2)) < 1e-6,
         f"max err {max(abs(a - b) for a, b in zip(R, R2)):.2e}")
    # G1: fixed point C* = f(W, C*, S) — nonzero S so C* is nontrivial
    Cs, _, conv = fixed_point_context([[0.2, 0.1], [0.1, 0.2]], 0.4, [0.3, -0.2])
    gate("G1 fixed-point awareness", conv and abs(Cs[0]) > 0.1, f"C*={Cs}")
    # G2: ledger conservation
    led = Ledger(0.3, 0.7)
    gate("G2 ledger total", abs(led.total - 1.0) < 1e-12, f"total={led.total}")
    mig = led.migrate(0.7)
    gate("G2b migration conserves", abs(mig.total - 1.0) < 1e-12 and mig.ci_c == 0.0,
         f"after={mig}")
    net = LedgerNetwork([Ledger(0.5, 0.5), Ledger(0.2, 0.3)], 0.1)
    t0 = net.total
    net.transfer(0, 1, 0.4)
    gate("G2c network conservation", abs(net.total - t0) < 1e-12, f"{t0} -> {net.total}")
    gate("G2d reciprocity star", RECIPROCITY_STAR == 1.15, f"R*={RECIPROCITY_STAR}")
    # G3: palimpsest alpha=1 lossless, alpha=0 total loss
    _, a1 = palimpsest_apply([1.0, 2.0], 1.0)
    s0, _ = palimpsest_apply([1.0, 2.0], 0.0)
    gate("G3 palimpsest eigen", a1 == 1.0 and s0 == [0.0, 0.0], "")
    gate("G3b B_coh dynamics", coherence_step(0.5, [0.3], [0.1]) == 0.7, "")
    # G4: boundary healthy range
    gate("G4 boundary healthy", HEALTHY_LO == 0.7 and HEALTHY_HI == 1.3
         and 0.7 <= markov_boundary(0.7, 1.0) <= 1.3, "")
    # G5: scar / lethe / forgiveness
    scar = Scar.from_translation([[1, 0], [0, 0]], 0.8)
    gate("G5 scar dim", scar.dimension == cokernel_dim([[1, 0], [0, 0]]) == 1, f"dim={scar.dimension}")
    gate("G5b lethe stabilises not heals",
         lethe(scar).magnitude == 0.8 and not lethe(scar).origin_known, "")
    gate("G5c forgiveness full trivialises", forgiveness(scar, 1.0).is_trivial, "")
    # G6: commutator is purely the stated form
    c = commutator(0.5, 0.2, [1.0], [2.0])
    gate("G6 commutator", abs(c - (0.5j + 0.4)) < 1e-12, f"[O,O]={c}")
    # G7: version
    gate("G7 version", __version__ == "2.1.0", __version__)
    return checks


def main():
    ok = True
    for name, passed, detail in verify():
        print(f"{'PASS' if passed else 'FAIL'}  {name}  {detail}")
        ok = ok and passed
    print("ALL GATES PASS" if ok else "GATES FAILED")
    return 0 if ok else 1
