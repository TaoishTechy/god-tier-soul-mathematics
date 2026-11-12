"""UHIF relational signature.

    R = tanh(W C + S),            W' = (arctanh(R) - S) C^+
    f^-1(f(W, C, S)) ~= W,        C* = f(W, C*, S)  (fixed point)

W: weight matrix (m x n), C: context vector (n), S: scalar shift (or
per-output vector). R is the low-rank holographic relational signature /
intent. The inverse is exact up to the nullspace of C — that degeneracy
is a feature of the spec, not a bug: identity preservation is the
condition R(f^-1(R)) == R.
"""
from __future__ import annotations

import math

from .linalg import arctanh_clipped, matvec, pinv


def relational_signature(W, C, S=0.0):
    """R = tanh(W C + S). Returns a list of floats in (-1, 1)."""
    z = matvec(W, C)
    if isinstance(S, (list, tuple)):
        z = [zi + si for zi, si in zip(z, S)]
    else:
        z = [zi + float(S) for zi in z]
    return [math.tanh(zi) for zi in z]


def inverse_weights(R, C, S=0.0):
    """W' = (arctanh(R) - S) C^+  — one row per output, rank-1 in C.

    C^+ is the pseudoinverse of C viewed as a column vector, i.e.
    C^+ = C^T / ||C||^2. Returns W' with W' C == arctanh(R) - S
    (up to the ridge in pinv, < 1e-6 relative error in tests).
    """
    y = [arctanh_clipped(r) - (float(S) if not isinstance(S, (list, tuple)) else float(s))
         for r, s in zip(R, S if isinstance(S, (list, tuple)) else [S] * len(R))]
    # C as column matrix (n x 1); pinv gives (1 x n) row.
    C_col = [[c] for c in C]
    C_plus = pinv(C_col)  # [[c1/||C||^2, ...]]
    row = C_plus[0]
    return [[yi * rj for rj in row] for yi in y]


def fixed_point_context(W, S=0.0, C0=None, tol=1e-10, max_iter=10000):
    """Iterate C <- tanh(W C + S) until convergence.

    Returns (C*, iterations, converged). The map is a contraction when
    the spectral radius of W is < 1 in the induced norm; otherwise it
    may oscillate — the caller gets `converged=False` and the last
    iterate, never a silent lie. Awareness condition in the spec is
    exactly C* = f(W, C*, S).
    """
    n = len(W[0]) if W else 0
    C = list(C0) if C0 is not None else [0.0] * n
    for i in range(1, max_iter + 1):
        nxt = relational_signature(W, C, S)
        # tanh output lives in (-1,1); fixed point is in that range.
        # Pad/truncate to n if W is not square.
        nxt = (nxt + [0.0] * n)[:n]
        err = max((abs(a - b) for a, b in zip(nxt, C)), default=0.0)
        C = nxt
        if err < tol:
            return C, i, True
    return C, max_iter, False
