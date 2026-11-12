"""CLI + verify gates smoke tests."""
import os
import subprocess
import sys
from pathlib import Path

from soulmath.verify import verify

ROOT = Path(__file__).resolve().parent.parent


def test_verify_all_gates_pass():
    checks = verify()
    assert len(checks) >= 10
    assert all(passed for _, passed, _ in checks), checks


def _run(*args):
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    return subprocess.run([sys.executable, *args], capture_output=True,
                          text=True, cwd=ROOT, env=env)


def test_cli_verify_and_demo():
    for args in (["-m", "soulmath.cli", "verify"],
                 ["-m", "soulmath.cli", "demo"],
                 ["-m", "soulmath.cli", "example", "buddha"]):
        r = _run(*args)
        assert r.returncode == 0, r.stderr
    r = _run("-m", "soulmath.cli", "example", "buddha")
    assert "buddha" in r.stdout
    assert "fidelity=1.000" in r.stdout
