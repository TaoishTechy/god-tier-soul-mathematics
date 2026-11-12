# Equation index — USIF v2.1

Every equation in the spec, where it lives in code, and which test
covers it. "Modelled" means a computable miniature with the limits
stated in `AUDIT.md`; "recorded" means the equation is stated and its
checkable part is tested, but it is not solved.

| # | Equation | Module / function | Test |
|---|---|---|---|
| 1 | `Sigma = (X, H*(X), Tor, kappa, Barcode, R, CI_B+CI_C, alpha, f, B_coh, dB, \|\|-, [c], R)` | `sigma.Soul` | `test_soul_json_roundtrip`, `test_carried_payload_excludes_substrate` |
| 2 | `R = tanh(WC + S)` | `relational.relational_signature` | `test_relational_signature_is_tanh` |
| 3 | `W' = (arctanh(R) - S) C^+` | `relational.inverse_weights` | `test_inverse_weights_roundtrip`, `test_inverse_weights_recovers_projection` |
| 4 | `f^-1(f(W,C,S)) ≈ W` (round-trip `R(f^-1(R)) = R`) | `relational.*` + `verify.G0` | `test_inverse_weights_roundtrip` |
| 5 | `C* = f(W, C*, S)` | `relational.fixed_point_context` | `test_fixed_point_converges_and_satisfies`, G1 |
| 6 | `d/dt(CI_B + CI_C) = sigma_topo` | `ledger.Ledger.step` | `test_ledger_conservation_and_migration`, G2 |
| 7 | `d/dt sum_i(CI_B,i + CI_C,i) + d/dt CI_B,net = 0` | `ledger.LedgerNetwork` | `test_ledger_network_conservation`, G2c |
| 8 | Reciprocity conserved iff `R >= R* ≈ 1.15` | `ledger.RECIPROCITY_STAR`, `Ledger.reciprocity_conserved` | `test_reciprocity_star`, G2d |
| 9 | `P_hat \|teaching> = alpha \|teaching>`, `alpha in [0,1]` | `palimpsest.palimpsest_apply` | `test_palimpsest_eigen`, G3 |
| 10 | `dB_coh/dt = sum L_i - sum D_i` | `palimpsest.coherence_step` | `test_coherence_budget`, G3b |
| 11 | Buddha: `B_coh=1, S_sin=0, F_hat\|karma> = 0` | `palimpsest.buddha_eigenstate`, `is_buddha` | `test_buddha_eigenstate` |
| 12 | `[O_i, O_j] = i hbar Omega_ij + lambda C_ijk O_k` | `correlation.commutator` | `test_commutator_form`, G6 |
| 13 | Persistence length `L = -ln(c)/gamma` | `correlation.persistence_length` | `test_persistence_length` |
| 14 | `dB = dP(internal)/dP(external)`, healthy `[0.7, 1.3]` | `boundary.markov_boundary`, `boundary_status` | `test_boundary_healthy_range`, G4 |
| 15 | `Psi_mind(t) = F(pi(P), dB(B), gamma(T)) + xi(t)` | `boundary.mind_state` (F = product, documented default) | `test_mind_state_neutral_point` |
| 16 | `chi = sum_k (-1)^k b_k` | `topology.HomotopyType.euler_characteristic` | `test_euler_characteristic` |
| 17 | Cup product on `H*(X)` | `topology.HomotopyType.cup_product` (sparse table) | `test_cup_product_default` |
| 18 | Barcode persistence `d - b`, truncation at `t` | `topology.Barcode` | `test_barcode_persistence_and_truncate` |
| 19 | Knot `kappa`, unknotted iff crossings 0 + det 1 | `topology.Knot` | `test_knots` |
| 20 | `V^B -> V[G]` via ultrafilter `U` | `forcing.BooleanModel`, `Ultrafilter.collapse` | `test_boolean_model_and_collapse` |
| 21 | Forcing trace `||-` (carried, `G` not carried) | `forcing.forcing_trace` | `test_forcing_trace_is_carried_not_filter` |
| 22 | `[c] = H^1(coker(T))`, `dim coker = m - rank(T)` | `scar.Scar.from_translation`, `cokernel_dim` | `test_cokernel_dim`, G5 |
| 23 | `L_hat = tau_{<=0} ∘ a_j(- ⊗ O_forget)` | `scar.lethe` (stabilises, never heals) | `test_scar_lethe_forgiveness`, G5b |
| 24 | `F_hat` trivialises `[c]` at full strength | `scar.forgiveness` | `test_scar_lethe_forgiveness`, G5c |
| 25 | `Psi_next = U ∘ P_hat(alpha) ∘ F_hat ∘ f^-1(...)` | `reconstruction.reconstruct` | `test_reconstruction_ordinary_fidelity`, `test_reconstruction_buddha_lossless` |
| 26 | Death: `CI_C^(bio) -> CI_B^(boundary)` | `death.death_transition` | `test_death_conserves_and_carries_knot` |
| 27 | Field eq: `∇_μ∇^μ Φ_HS + ξR Φ_HS = Σ δ^4(x-x_i)` | `death.field_source_term` (source count only — recorded, not solved) | `test_death_conserves_and_carries_knot` |
| 28 | Lethovore `F(R) = hocolim(R <- coker(T_R) -> D^2)` | `operators.lethovore` | `test_lethovore` |
| 29 | Anti-Hollow `AH(U)=1 iff U dense open` | `operators.anti_hollow` | `test_anti_hollow` |
| 30 | Chaotic Betti `f(b) = b ∪ (b ∪ b)`, `chi_max ≈ 0.41` | `operators.chaotic_betti` | `test_chaotic_betti` |
| 31 | Imaginary Island `A_w = <Φ\|A\|Ψ>/<Φ\|Ψ>`, `Im(A_w)` Larmor clock | `operators.imaginary_island` | `test_imaginary_island` |
| 32 | Self-Erasing `m.[c_phi]=0 ∧ [c_phi]≠0` | `operators.self_erasing` | `test_self_erasing` |

Fidelity model (documented, not in the source spec — the spec says
`f` "gates reconstruction probability" without a formula):
`fidelity = alpha * faith * boundary_factor * (1 - roundtrip_err)`,
with `boundary_factor = 1` inside `[0.7, 1.3]`, linear penalty
outside. See `reconstruction.py`.
