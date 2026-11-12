"""Hollow / Generic / Apostatic: topology, forcing, scar, operators."""
import math
import pytest

from soulmath.topology import HomotopyType, Barcode, Knot, torsion_free
from soulmath.forcing import BooleanModel, Ultrafilter, forcing_trace
from soulmath.scar import Scar, cokernel_dim, lethe, forgiveness
from soulmath.operators import (
    lethovore, anti_hollow, chaotic_betti, chaotic_betti_ceiling,
    imaginary_island, self_erasing,
)


def test_euler_characteristic():
    assert HomotopyType((1, 2, 0)).euler_characteristic == -1
    assert HomotopyType((1, 0)).euler_characteristic == 1
    assert HomotopyType((1, 0), (2,)).is_torsion_free is False
    assert torsion_free([]) and not torsion_free([2])


def test_cup_product_default():
    h = HomotopyType()
    assert h.cup_product(0, 1) == 1
    assert h.cup_product(1, 1) == 0  # exterior algebra


def test_barcode_persistence_and_truncate():
    bc = Barcode([(0.0, 5.0), (1.0, 12.0), (2.0, math.inf)])
    assert bc.total_persistence == pytest.approx(16.0)
    assert bc.n_persisting == 1
    assert bc.betti_at(3.0) == 3
    assert bc.betti_at(6.0) == 2
    tr = bc.truncate(10.0)
    assert tr.intervals == [(0.0, 5.0), (1.0, 10.0), (2.0, 10.0)]
    with pytest.raises(ValueError):
        Barcode([(5.0, 1.0)])


def test_knots():
    assert Knot().is_unknotted
    assert not Knot.trefoil().is_unknotted
    assert Knot.trefoil().determinant == 3
    assert Knot.figure_eight().determinant == 5


def test_boolean_model_and_collapse():
    m = BooleanModel({"rebirth": 1.0, "void": 0.0, "maybe": 0.5})
    assert m.forces("rebirth") and not m.forces("maybe")
    U = Ultrafilter.from_true_values(m)
    assert U.collapse(m) == {"rebirth": True, "void": False, "maybe": False}
    with pytest.raises(ValueError):
        BooleanModel({"x": 2.0})


def test_forcing_trace_is_carried_not_filter():
    m = BooleanModel({"p": 1.0, "q": 0.0})
    tr = forcing_trace(m, ["p"])
    # p -> p is forced; p -> q is not.
    assert tr[("p", "p")] is True
    assert tr[("p", "q")] is False


def test_cokernel_dim():
    assert cokernel_dim([[1, 0], [0, 0]]) == 1
    assert cokernel_dim([[1, 0], [0, 1]]) == 0
    assert cokernel_dim([[0, 0], [0, 0]]) == 2


def test_scar_lethe_forgiveness():
    scar = Scar.from_translation([[1, 0], [0, 0]], 0.8)
    assert scar.dimension == 1 and scar.magnitude == 0.8
    l = lethe(scar)
    assert l.magnitude == 0.8 and l.origin_known is False  # stabilises, never heals
    assert forgiveness(scar, 0.5).magnitude == pytest.approx(0.4)
    assert forgiveness(scar, 1.0).is_trivial
    assert not Scar().is_trivial is False  # magnitude 0 + dim 0 is trivial
    with pytest.raises(ValueError):
        Scar(magnitude=2.0)
    with pytest.raises(ValueError):
        forgiveness(scar, -0.1)


def test_lethovore():
    r, consumed = lethovore(1.0, 2)
    assert r == pytest.approx(1.2) and consumed is True
    assert lethovore(1.0, 0)[1] is False


def test_anti_hollow():
    assert anti_hollow(True) == 1
    assert anti_hollow(False) == 0


def test_chaotic_betti():
    assert chaotic_betti(0.5) == pytest.approx(0.125)
    assert chaotic_betti_ceiling() == pytest.approx(0.41)


def test_imaginary_island():
    # <Phi|Psi> = 1, A|Psi> = [1j], <Phi| = [1]  -> A_w = 1j, clock = 1
    a_w, clock = imaginary_island([1 + 0j], [1j], [1 + 0j], 1 + 0j)
    assert a_w == pytest.approx(1j) and clock == pytest.approx(1.0)
    with pytest.raises(ValueError):
        imaginary_island([1j], [1j], [1j], 0j)


def test_self_erasing():
    assert self_erasing(2, bulk=False) is True   # survives single refutation
    assert self_erasing(2, bulk=True) is False   # not bulk refutation
    assert self_erasing(1) is False
