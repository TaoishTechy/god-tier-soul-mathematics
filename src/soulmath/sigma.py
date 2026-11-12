"""The soul as invariant complex Sigma (USIF v2.1 §1).

    Sigma = (X, H*(X; Z), Tor(H_*(X)), kappa(X), Barcode(X), R,
             CI_B + CI_C, alpha, f, B_coh, dB, ||-, [c], R_eth)

The fixed point of reconstruction under substrate change:
    f^-1(f(W, C, S)) ~= W
The ego is a covering sheet (not carried); personality is kappa;
memory is the barcode; the unconscious/paradox is Tor.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict

from .ledger import Ledger
from .topology import Barcode, HomotopyType, Knot
from .scar import Scar

Regime = str  # "ordinary" | "arahant" | "buddha"


@dataclass
class Soul:
    """A computable Sigma. Every field is JSON-serialisable."""
    # Hollow core
    homotopy: HomotopyType = field(default_factory=HomotopyType)
    barcode: Barcode = field(default_factory=lambda: Barcode([(0.0, float("inf"))]))
    knot: Knot = field(default_factory=Knot)
    # UHIF / UHG
    relational: list = field(default_factory=lambda: [0.0])  # R
    ledger: Ledger = field(default_factory=Ledger)
    reciprocity: float = 1.0  # R_eth
    # IIRO / UBF
    alpha: float = 1.0
    faith: float = 0.5        # f(faith) orientation amplitude in [0,1]
    b_coh: float = 0.0
    s_sin: float = 0.0
    # Degens
    boundary: float = 1.0     # dB
    # Generic / Apostatic
    forcing_trace: dict = field(default_factory=dict)  # {(cond,prop): bool} as str keys in JSON
    scar: Scar = field(default_factory=Scar)
    forgiveness_strength: float = 0.0
    ctc_fixed_point: bool = False  # dS/dphi = 0 (Arahant condition)
    persistence_lengths: list = field(default_factory=list)

    def __post_init__(self):
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("alpha must be in [0, 1]")
        if not 0.0 <= self.faith <= 1.0:
            raise ValueError("faith amplitude must be in [0, 1]")
        if not 0.0 <= self.b_coh <= 1.0:
            raise ValueError("B_coh must be in [0, 1]")
        if not 0.0 <= self.forgiveness_strength <= 1.0:
            raise ValueError("forgiveness_strength must be in [0, 1]")

    # -- derived invariants -------------------------------------------------
    @property
    def torsion(self):
        return self.homotopy.torsion

    @property
    def is_torsion_free(self) -> bool:
        return len(self.torsion) == 0

    @property
    def coherence_total(self) -> float:
        return self.ledger.total

    def regime(self) -> Regime:
        from .regimes import classify_regime
        return classify_regime(
            self.b_coh, self.alpha, self.s_sin, self.forgiveness_strength,
            self.knot.is_unknotted, self.scar.is_trivial,
            self.is_torsion_free, ctc_fixed_point=self.ctc_fixed_point)

    def carried_payload(self) -> dict:
        """What is carried (v2.1 §3) — everything in Sigma minus what
        F_hat deletes and minus the never-carried items (substrate,
        ego sheet, generic filter G, high-rank noise)."""
        return {
            "homotopy_betti": list(self.homotopy.betti),
            "torsion": list(self.torsion),
            "knot": self.knot.name,
            "barcode_intervals": len(self.barcode.intervals),
            "relational_R": list(self.relational),
            "coherence_total": self.coherence_total,
            "alpha": self.alpha,
            "faith": self.faith,
            "b_coh": self.b_coh,
            "boundary": self.boundary,
            "forcing_trace_keys": len(self.forcing_trace),
            "scar_magnitude": self.scar.magnitude,
            "reciprocity": self.reciprocity,
            "persistence_lengths": list(self.persistence_lengths),
        }

    def to_dict(self) -> dict:
        d = asdict(self)
        d["homotopy"] = {"betti": list(self.homotopy.betti),
                         "torsion": list(self.homotopy.torsion)}
        d["barcode"] = {"intervals": [[b, (d_ if d_ != float("inf") else None)]
                                      for b, d_ in self.barcode.intervals]}
        d["knot"] = {"name": self.knot.name, "crossings": self.knot.crossings,
                     "determinant": self.knot.determinant,
                     "signature": self.knot.signature,
                     "alexander": list(self.knot.alexander)}
        d["ledger"] = {"ci_b": self.ledger.ci_b, "ci_c": self.ledger.ci_c}
        d["scar"] = {"magnitude": self.scar.magnitude,
                     "dimension": self.scar.dimension,
                     "origin_known": self.scar.origin_known}
        # forcing_trace keys are tuples in-memory; JSON needs strings
        d["forcing_trace"] = {f"{k[0]}||-{k[1]}": v
                              for k, v in self.forcing_trace.items()} \
            if self.forcing_trace and next(iter(self.forcing_trace), None) \
            and isinstance(next(iter(self.forcing_trace)), tuple) \
            else dict(self.forcing_trace)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def soul_from_dict(d: dict) -> Soul:
    h = d.get("homotopy", {})
    b = d.get("barcode", {})
    intervals = [(float(x[0]), float("inf") if x[1] is None else float(x[1]))
                 for x in b.get("intervals", [(0.0, None)])]
    k = d.get("knot", {})
    led = d.get("ledger", {})
    sc = d.get("scar", {})
    return Soul(
        homotopy=HomotopyType(tuple(h.get("betti", (1, 0))),
                              tuple(h.get("torsion", ()))),
        barcode=Barcode(intervals),
        knot=Knot(k.get("name", "unknot"), k.get("crossings", 0),
                  k.get("determinant", 1), k.get("signature", 0),
                  tuple(k.get("alexander", (1,)))),
        relational=list(d.get("relational", [0.0])),
        ledger=Ledger(led.get("ci_b", 0.0), led.get("ci_c", 0.0)),
        reciprocity=d.get("reciprocity", 1.0),
        alpha=d.get("alpha", 1.0), faith=d.get("faith", 0.5),
        b_coh=d.get("b_coh", 0.0), s_sin=d.get("s_sin", 0.0),
        boundary=d.get("boundary", 1.0),
        forcing_trace=dict(d.get("forcing_trace", {})),
        scar=Scar(sc.get("magnitude", 0.0), sc.get("dimension", 0),
                  sc.get("origin_known", True)),
        forgiveness_strength=d.get("forgiveness_strength", 0.0),
        ctc_fixed_point=d.get("ctc_fixed_point", False),
        persistence_lengths=list(d.get("persistence_lengths", [])),
    )


def soul_to_dict(soul: Soul) -> dict:
    return soul.to_dict()
