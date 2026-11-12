# Contributing

1. Every new equation gets a row in `docs/EQUATIONS.md` (equation →
   module → function → test) **before** prose about it.
2. Every claim gets a tier in `docs/AUDIT.md`. A claim without a test
   is Tier C, not Tier A — do not promote it.
3. Stdlib only for the library. Optional dependencies belong behind
   an import guard with a clear error, never in the core path.
4. Run `PYTHONPATH=src python -m pytest tests/ -q` and
   `PYTHONPATH=src python -m soulmath.cli verify` before opening a PR.
5. The caveat in the README is load-bearing: this is a formal model
   of speculative frameworks, not an empirical claim. Keep it that way.
