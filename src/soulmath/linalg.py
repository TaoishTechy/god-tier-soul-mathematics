"""Small pure-Python linear algebra (stdlib only).

Kept deliberately dependency-free so the suite runs anywhere CPython
runs. Matrices are lists of lists of floats; vectors are lists of floats.
Only the operations USIF actually needs are provided.
"""
from __future__ import annotations

import math


def matvec(A, x):
    return [sum(a * xi for a, xi in zip(row, x)) for row in A]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def _solve(A, b):
    """Gauss-Jordan with partial pivoting. Raises ValueError if singular."""
    n = len(A)
    M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("singular matrix")
        M[col], M[piv] = M[piv], M[col]
        d = M[col][col]
        M[col] = [v / d for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [v - f * w for v, w in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def pinv(A, ridge=1e-9):
    """Moore-Penrose pseudoinverse via (A^T A + ridge I)^-1 A^T.

    Exact on full-column-rank inputs (ridge -> 0 limit); the tiny ridge
    only regularises the nullspace of C, where USIF explicitly allows
    degeneracy: identity is preserved iff R(f^-1(R)) == R on that
    nullspace, so any nullspace component is a legitimate gauge choice.
    """
    At = transpose(A)
    AtA = matmul(At, A)
    n = len(AtA)
    for i in range(n):
        AtA[i][i] += ridge
    # Invert AtA column by column.
    inv_cols = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        inv_cols.append(_solve(AtA, e))
    inv = transpose(inv_cols)  # inv[i][j] = (AtA^-1)[i][j]
    return matmul(inv, At)


def arctanh_clipped(x, eps=1e-9):
    x = max(-1.0 + eps, min(1.0 - eps, x))
    return 0.5 * math.log((1.0 + x) / (1.0 - x))
