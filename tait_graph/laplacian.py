"""
laplacian.py
------------
Weighted Laplacian matrix utilities for Tait graphs.

The *weighted Laplacian* of a signed graph G = (V, E, w) is the matrix L
where:
  - L[i, i]  = -sum of weights of all edges incident to vertex i
  - L[i, j]  = sum of weights of all edges between i and j  (i ≠ j)

(Note the sign convention: diagonal entries are *negative* sums, matching
the knot-theory literature where the determinant of a knot equals
|det(reduced_L)|.)

The *reduced* Laplacian (also called the *deletion* matrix) is obtained by
deleting one row and the corresponding column; its determinant gives the
weighted spanning-tree count, which equals the knot determinant for the Tait
graph of an alternating knot diagram.
"""

from typing import Optional
from sage.matrix.constructor import Matrix  # type: ignore
from sage.rings.rational_field import QQ  # type: ignore
from sage.graphs.graph import Graph  # type: ignore


# ---------------------------------------------------------------------------
# Laplacian construction
# ---------------------------------------------------------------------------

def weighted_laplacian(G: Graph) -> Matrix:
    """Compute the weighted Laplacian matrix of *G*.

    Parameters
    ----------
    G:
        A SageMath :class:`Graph` whose edges carry integer or rational
        weights as their labels.  Multi-edges and loops are supported.

    Returns
    -------
    An *n × n* matrix over ℚ (``QQ``) where *n* = ``G.order()``.  Vertices
    are indexed in the order returned by ``G.vertices()``.

    Examples
    --------
    In a SageMath session::

        sage: from tait_graph.laplacian import weighted_laplacian
        sage: G = Graph([(0, 1, 1), (1, 2, -1), (0, 2, 1)], weighted=True)
        sage: weighted_laplacian(G)
        [-2  1  1]
        [ 1  0 -1]
        [ 1 -1  0]
    """
    vert_list = G.vertices()
    vert_index: dict = {v: i for i, v in enumerate(vert_list)}
    n = G.order()
    M = Matrix(QQ, n, n)

    for u, v, w in G.edges():
        i, j = vert_index[u], vert_index[v]
        if i == j:
            # Self-loop: contributes to diagonal only.
            # Convention: loops count twice in the degree (as in the matrix-
            # tree theorem for weighted graphs).
            M[i, i] -= 2 * w
        else:
            M[i, j] += w
            M[j, i] += w
            M[i, i] -= w
            M[j, j] -= w

    return M


def reduced_weighted_laplacian(M: Matrix, i: int = 0) -> Matrix:
    """Return the reduced Laplacian obtained by deleting row and column *i*.

    Parameters
    ----------
    M:
        A weighted Laplacian matrix, typically produced by
        :func:`weighted_laplacian`.
    i:
        Index of the row/column to delete (default: ``0``, i.e. the first
        vertex).

    Returns
    -------
    An *(n-1) × (n-1)* matrix over the same ring as *M*.

    Notes
    -----
    The determinant of the reduced Laplacian equals the *weighted spanning-
    tree count* of the graph (Matrix-Tree Theorem).  For the Tait graph of an
    alternating knot this equals the *knot determinant*.
    """
    return M.delete_rows([i]).delete_columns([i])


# ---------------------------------------------------------------------------
# Convenience: determinant-based knot invariants
# ---------------------------------------------------------------------------

def knot_determinant(G: Graph, vertex_index: int = 0) -> int:
    """Compute the determinant of the knot from its Tait graph *G*.

    Parameters
    ----------
    G:
        The Tait graph (one of the two checkerboard graphs) of an alternating
        knot diagram.
    vertex_index:
        Which vertex to delete when forming the reduced Laplacian
        (default: ``0``).  The result is independent of this choice for
        connected graphs.

    Returns
    -------
    The absolute value of the determinant of the reduced weighted Laplacian,
    as an integer.
    """
    L = weighted_laplacian(G)
    R = reduced_weighted_laplacian(L, vertex_index)
    return abs(int(R.determinant()))


def signature_from_laplacian(G: Graph) -> Optional[int]:
    """Estimate the knot signature from the Laplacian of the Tait graph.

    This is an *experimental* helper.  For alternating knots the signature
    equals the number of negative eigenvalues of the reduced Laplacian minus
    the number of positive eigenvalues (with sign convention matching
    Trotter/Gordon–Litherland).

    Parameters
    ----------
    G:
        The Tait graph of an alternating knot diagram.

    Returns
    -------
    The signature as an integer, or ``None`` if the computation fails (e.g.
    for non-integer eigenvalues over ℚ).

    Notes
    -----
    This function is provided for experimentation.  For non-alternating knots
    the Tait graph approach does not directly give the signature.
    """
    try:
        L = weighted_laplacian(G)
        R = reduced_weighted_laplacian(L)
        eigenvalues = R.eigenvalues()
        pos = sum(1 for e in eigenvalues if e > 0)
        neg = sum(1 for e in eigenvalues if e < 0)
        return neg - pos
    except Exception:
        return None
