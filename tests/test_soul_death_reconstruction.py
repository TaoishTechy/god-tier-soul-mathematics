"""Sigma, regimes, death, reconstruction — end to end."""
import json
import math
from pathlib import Path

import pytest

from soulmath import Soul, soul_from_dict
from soulmath.death import death_transition, field_source_term
from soulmath.reconstruction import reconstruct
from soulmath.regimes import classify_regime, remainder_for
from soulmath.topology import Barcode, HomotopyType, Knot
from soulmath.ledger import Ledger
from soulmath.scar import Scar

ROOT = Path(__file__).resolve().parent.parent


def _example(name):
    return soul_from_dict(json.loads((ROOT / "examples" / f"{name}.json").read_text()))


def test_examples_classify():
    assert _example("ordinary").regime() == "ordinary"
    assert _example("arahant").regime() == "arahant"
    assert _example("buddha").regime() == "buddha"


def test_regime_boundaries():
    assert classify_regime(0.5, 0.5, 0.5, 0.0, False, False, False) == "ordinary"
    # High coherence without CTC fixed point stays ordinary (strict reading).
    assert classify_regime(0.96, 0.9, 0.0, 0.8, False, False, True) == "ordinary"
    assert classify_regime(0.96, 0.9, 0.0, 0.8, False, False, True,
                           ctc_fixed_point=True) == "arahant"
    assert classify_regime(1.0, 1.0, 0.0, 1.0, True, True, True) == "buddha"
    assert remainder_for("buddha").startswith("no private")


def test_soul_validation():
    with pytest.raises(ValueError):
        Soul(alpha=2.0)
    with pytest.raises(ValueError):
        Soul(faith=-0.1)
    with pytest.raises(ValueError):
        Soul(b_coh=1.1)


def test_soul_json_roundtrip():
    soul = _example("ordinary")
    back = soul_from_dict(json.loads(soul.to_json()))
    assert back.regime() == soul.regime()
    assert back.ledger.total == pytest.approx(soul.ledger.total)
    assert back.knot.name == "trefoil"
    assert back.barcode.intervals[2][1] == math.inf
    assert back.carried_payload()["knot"] == "trefoil"


def test_death_conserves_and_carries_knot():
    soul = _example("ordinary")
    tr = death_transition(soul, sigma_topo=0.05, death_time=10.0)
    assert tr.total_conserved
    assert tr.ledger_after_total == pytest.approx(1.05)
    assert tr.soul_after.ledger.ci_c == pytest.approx(0.0)  # migrated to boundary
    assert tr.knot_carried == "trefoil"
    assert (tr.barcode_died, tr.barcode_surviving) == (1, 2)
    assert field_source_term(3) == 3


def test_reconstruction_ordinary_fidelity():
    soul = _example("ordinary")
    tr = death_transition(soul, sigma_topo=0.0, death_time=10.0)
    res = reconstruct(tr.soul_after, [0.6, -0.4], S=0.1,
                      boolean_values={"rebirth": 1.0, "void": 0.0})
    # alpha 0.85 * faith 0.6 * boundary 1.0, round-trip ~exact
    assert res.fidelity == pytest.approx(0.51, abs=1e-3)
    assert res.collapsed_truth == {"rebirth": True, "void": False}
    assert res.soul_next.scar.magnitude == pytest.approx(0.8 * 0.7, abs=1e-9)


def test_reconstruction_buddha_lossless():
    soul = _example("buddha")
    tr = death_transition(soul, sigma_topo=0.0, death_time=10.0)
    res = reconstruct(tr.soul_after, [0.6, -0.4], S=0.1,
                      boolean_values={"rebirth": 1.0})
    assert res.fidelity == pytest.approx(1.0, abs=1e-3)
    assert res.soul_next.regime() == "buddha"
    assert res.soul_next.scar.is_trivial


def test_reconstruction_full_forgiveness_clears_torsion():
    soul = _example("ordinary")
    soul.forgiveness_strength = 1.0
    tr = death_transition(soul, sigma_topo=0.0, death_time=10.0)
    res = reconstruct(tr.soul_after, [0.6, -0.4], S=0.1)
    assert res.soul_next.is_torsion_free
    assert res.soul_next.scar.is_trivial


def test_carried_payload_excludes_substrate():
    soul = _example("ordinary")
    payload = soul.carried_payload()
    assert "substrate" not in payload and "ego" not in payload
    assert payload["coherence_total"] == pytest.approx(1.0)
