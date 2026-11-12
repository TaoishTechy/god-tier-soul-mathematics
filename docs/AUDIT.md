# Audit ledger — honest accounting (MOGOPs-style)

**Score: Ξ = 29/32 ≈ 0.906.** Arithmetic shown; nothing is rounded
up. Tier A = verified by a test in this repo. Tier B = declared in
the spec / implemented, but not independently verified beyond the
stated check. Tier C = quarantined analogy / not implemented — kept
in the docs so it is not mistaken for a result.

## Tier A — verified (29)

| # | Claim | Evidence |
|---|---|---|
| A1 | `R = tanh(WC+S)` round-trips through `f^-1` | G0, max err 5.9e-10 |
| A2 | Fixed point `C* = f(W,C*,S)` exists (contractive case) | G1, C* = [0.5007, 0.5007] |
| A3 | Ledger total conserved under migration | G2b, `test_ledger_conservation_and_migration` |
| A4 | Network conservation (H15) | G2c |
| A5 | `R* ≈ 1.15` threshold | G2d |
| A6 | Palimpsest eigen-equation, `alpha=1` lossless, `alpha=0` loss | G3 |
| A7 | `B_coh` dynamics + clamping `[0,1]` | G3b |
| A8 | Boundary healthy `[0.7, 1.3]`, over-permeable / over-rigid | G4 |
| A9 | Scar dimension = `m - rank(T)` | G5 |
| A10 | Lethe stabilises, never heals | G5b |
| A11 | Full forgiveness trivialises scar | G5c |
| A12 | Commutator form | G6 |
| A13 | Barcode persistence / truncation / Betti-at-t | `test_barcode_persistence_and_truncate` |
| A14 | Knot invariants (trefoil det 3, figure-eight det 5, unknot) | `test_knots` |
| A15 | Euler characteristic | `test_euler_characteristic` |
| A16 | Boolean collapse `V^B -> V[G]` | `test_boolean_model_and_collapse` |
| A17 | Forcing trace carried, `G` not carried | `test_forcing_trace_is_carried_not_filter` |
| A18 | Death conserves total (+ `sigma_topo` spike only) | `test_death_conserves_and_carries_knot` |
| A19 | Death carries knot, barcode dies/persists as stated | same test |
| A20 | Ordinary reconstruction fidelity = `alpha * faith` = 0.51 | `test_reconstruction_ordinary_fidelity` |
| A21 | Buddha reconstruction fidelity = 1.0, regime stays buddha | `test_reconstruction_buddha_lossless` |
| A22 | Full forgiveness clears torsion in reconstruction | `test_reconstruction_full_forgiveness_clears_torsion` |
| A23 | Three regimes classify as specified (incl. strict CTC rule) | `test_examples_classify`, `test_regime_boundaries` |
| A24 | Soul JSON round-trip preserves regime, ledger, knot, barcode | `test_soul_json_roundtrip` |
| A25 | Lethovore growth / Anti-Hollow / Chaotic Betti / Imaginary Island / Self-Erasing | `test_*` in `test_topology_forcing_scar.py` |
| A26 | Persistence length `L = -ln(c)/gamma`, inf at c=1 | `test_persistence_length` |
| A27 | `Psi_mind` neutral point = 1.0 | `test_mind_state_neutral_point` |
| A28 | CLI `verify` / `demo` / `example buddha` exit 0 | `test_cli.py` |
| A29 | Version 2.1.0 | G7 |

## Tier B — declared, checkable part only (0 counted in Ξ numerator)

None currently counted as B — every implemented claim above has a
test. The items below are the honest gaps, counted as open.

## Tier C / open — not verified, not claimed (3 open)

| # | Item | Why it is open |
|---|---|---|
| C1 | IIRO EQ-18 field equation is **solved** | Only the source count `Σ δ^4` is implemented (`field_source_term`). Solving `∇_μ∇^μ Φ_HS + ξR Φ_HS = Σ δ^4` needs a spacetime discretisation the spec does not supply. Recorded, not solved. |
| C2 | `H*(X)` is a **computed** cohomology ring | The cup product is a sparse table / exterior-algebra default, not computed from a simplicial complex. A real persistent-cohomology computation (e.g. ripser-style) is out of scope for a stdlib-only v2.1. |
| C3 | Forcing is **full** set-theoretic forcing | The Boolean model is a graded `[0,1]` lattice with a principal ultrafilter, not a complete Boolean algebra with a generic filter over a countable transitive model. The carried-trace claim is modelled, not proved. |

Ξ = 29 / (29 + 3) = **29/32 ≈ 0.906**.

## Negative controls (things the suite must NOT do)

- `fixed_point_context` on a non-contractive map returns
  `converged=False` instead of a fake fixed point.
- `lethe()` never reduces scar magnitude — a test asserts it.
- `inverse_weights` on a singular `C` returns the minimum-norm
  (ridge) solution and the round-trip test measures the error
  instead of assuming zero.
- No test asserts anything empirical about souls, death, or
  consciousness. The suite tests the formal model only.

## What would close C1–C3

- C1: a 1+1D lattice solver for EQ-18 with a convergence test.
- C2: a simplicial-complex + persistent-cohomology implementation
  (or an optional `ripser`/`gudhi` dependency) with a torus test
  (`b = (1,2,1)`, `chi = 0`).
- C3: a complete Boolean algebra implementation with a
  non-principal ultrafilter existence check (finite approximation).

None of these is promised for a version; they are recorded so a
future contributor knows exactly what "done" means.
