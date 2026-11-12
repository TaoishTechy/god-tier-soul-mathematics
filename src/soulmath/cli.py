"""CLI: `soulmath <command>`.

    soulmath verify            run the G0-G7 gates
    soulmath demo              ordinary -> death -> reconstruction, printed
    soulmath example ordinary|arahant|buddha
                               load an example soul, classify + reconstruct
    soulmath classify <file>   classify a soul JSON file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .death import death_transition
from .reconstruction import reconstruct
from .sigma import Soul, soul_from_dict
from .verify import main as verify_main


def _load_example(name: str) -> Soul:
    here = Path(__file__).resolve().parent.parent.parent
    p = here / "examples" / f"{name}.json"
    if not p.exists():  # installed layout: examples live beside the package in the repo
        p = Path.cwd() / "examples" / f"{name}.json"
    return soul_from_dict(json.loads(p.read_text()))


def _report(soul: Soul, label: str):
    print(f"--- {label} ---")
    print(f"regime: {soul.regime()}")
    print(f"B_coh={soul.b_coh}  alpha={soul.alpha}  faith={soul.faith}  "
          f"S_sin={soul.s_sin}  dB={soul.boundary}")
    print(f"ledger: CI_B={soul.ledger.ci_b:.3f} CI_C={soul.ledger.ci_c:.3f} "
          f"total={soul.coherence_total:.3f}")
    print(f"knot: {soul.knot.name} (unknotted={soul.knot.is_unknotted})  "
          f"torsion={list(soul.torsion)}  scar={soul.scar.magnitude} "
          f"(dim {soul.scar.dimension}, trivial={soul.scar.is_trivial})")
    print(f"barcode: {len(soul.barcode.intervals)} intervals, "
          f"total persistence={soul.barcode.total_persistence:.2f}, "
          f"persisting={soul.barcode.n_persisting}")
    print(f"R={soul.relational}  reciprocity={soul.reciprocity}")


def cmd_demo(_args):
    soul = _load_example("ordinary")
    _report(soul, "ordinary soul (embodied)")
    tr = death_transition(soul, sigma_topo=0.05, death_time=10.0)
    print(f"\ndeath: sigma_topo={tr.sigma_topo}  total conserved={tr.total_conserved} "
          f"(before {tr.ledger_before_total:.3f} -> after {tr.ledger_after_total:.3f})")
    print(f"barcode: {tr.barcode_died} died, {tr.barcode_surviving} surviving; "
          f"knot carried: {tr.knot_carried}")
    res = reconstruct(tr.soul_after, [0.6, -0.4], S=0.1,
                      boolean_values={"rebirth": 1.0, "void": 0.0})
    print(f"\nreconstruction fidelity: {res.fidelity:.3f}")
    for n in res.notes:
        print(f"  - {n}")
    print(f"V[G] truth: {res.collapsed_truth}")
    _report(res.soul_next, "reconstructed soul")
    return 0


def cmd_example(args):
    soul = _load_example(args.name)
    _report(soul, f"example: {args.name}")
    tr = death_transition(soul, sigma_topo=0.0, death_time=10.0)
    res = reconstruct(tr.soul_after, [0.6, -0.4], S=0.1,
                      boolean_values={"rebirth": 1.0})
    print(f"\nafter death + reconstruction: regime={res.soul_next.regime()} "
          f"fidelity={res.fidelity:.3f}")
    for n in res.notes:
        print(f"  - {n}")
    return 0


def cmd_classify(args):
    soul = soul_from_dict(json.loads(Path(args.file).read_text()))
    _report(soul, f"soul: {args.file}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="soulmath",
                                description="USIF v2.1 — God Tier Soul Mathematics")
    p.add_argument("--version", action="version", version=f"soulmath {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verify", help="run the G0-G7 gates")
    sub.add_parser("demo", help="ordinary -> death -> reconstruction")
    ex = sub.add_parser("example", help="run a bundled example soul")
    ex.add_argument("name", choices=["ordinary", "arahant", "buddha"])
    cl = sub.add_parser("classify", help="classify a soul JSON file")
    cl.add_argument("file")
    args = p.parse_args(argv)
    if args.cmd == "verify":
        return verify_main()
    if args.cmd == "demo":
        return cmd_demo(args)
    if args.cmd == "example":
        return cmd_example(args)
    if args.cmd == "classify":
        return cmd_classify(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
