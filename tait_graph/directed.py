"""
directed.py
-----------
Implementation of the directed Tait graph following the Silver–Williams
construction described in:

    Silver, D. S. & Williams, S. G.
    "Crowell's derived group and twisted polynomials."
    Journal of Knot Theory and Its Ramifications, 2006.

In the directed Tait graph each undirected edge of the ordinary Tait graph is
replaced by a *directed* edge.  The direction is determined by the orientation
of the knot diagram and the sign of the corresponding crossing.

Orientation convention
----------------------
We use the standard PD-code orientation:
  - Each crossing [a, b, c, d] is traversed so that the *over-strand* goes
    from ``d`` → ``b``, and the *under-strand* goes from ``a`` → ``c``.
  - A crossing is *positive* if the over-strand passes from left to right when
    facing in the direction of the under-strand (right-hand rule), and
    *negative* otherwise.

Directed-edge rule (Silver–Williams)
--------------------------------------
  - For a **positive** crossing the directed edge points from the region to the
    *left* of the over-strand to the region to its *right*.
  - For a **negative** crossing the direction is reversed.

In terms of the PD-code entry ``[a, b, c, d]`` and the two regions
``R_left`` (containing strands ``b`` and ``c``) and ``R_right`` (containing
strands ``a`` and ``d``):
  - positive crossing  →  directed edge  R_left  → R_right
  - negative crossing  →  directed edge  R_right → R_left
"""

from typing import List, Tuple, Dict, Optional
from sage.graphs.digraph import DiGraph  # type: ignore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _regions_for_crossing(
    crossing: List[int],
    faces: Dict[int, Tuple[int, ...]],
) -> Tuple[Optional[int], Optional[int]]:
    """Identify the two faces that share *crossing*.

    The left face contains ``crossing[1]`` and ``crossing[2]`` (b, c),
    the right face contains ``crossing[0]`` and ``crossing[3]`` (a, d).

    Parameters
    ----------
    crossing:
        A four-element PD-code entry ``[a, b, c, d]``.
    faces:
        Mapping ``{face_index: tuple_of_strand_labels}`` for all faces of the
        diagram.

    Returns
    -------
    ``(left_face_index, right_face_index)`` where *left* is the face
    containing ``{b, c}`` and *right* is the face containing ``{a, d}``.
    Either value may be ``None`` if no matching face is found (this can occur
    for boundary faces of split diagrams).
    """
    a, b, c, d = crossing
    left_face: Optional[int] = None
    right_face: Optional[int] = None

    for idx, strands in faces.items():
        strand_set = set(strands)
        if b in strand_set and c in strand_set:
            left_face = idx
        if a in strand_set and d in strand_set:
            right_face = idx
        if left_face is not None and right_face is not None:
            break

    return left_face, right_face


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def directed_tait_graph(
    pd_code: List[List[int]],
    faces: Dict[int, Tuple[int, ...]],
    signed_edges: List[Tuple[int, int, int]],
) -> DiGraph:
    """Build the Silver–Williams directed Tait graph.

    Parameters
    ----------
    pd_code:
        Full PD-code of the knot/link diagram.  Each entry is a list
        ``[a, b, c, d]`` of four strand labels.
    faces:
        Mapping ``{face_index: tuple_of_strand_labels}`` produced by
        :func:`tait_graph.core.tait_graph`.
    signed_edges:
        List of ``(u, v, weight)`` triples from the undirected Tait graph,
        as returned by :func:`tait_graph.core.tait_graph`.  The ``weight``
        is ``+1`` (positive crossing) or ``-1`` (negative crossing).

    Returns
    -------
    A SageMath :class:`DiGraph` whose edges carry the same ``+1``/``-1``
    weights as the undirected graph, but with directions assigned according
    to the Silver–Williams rule.

    Notes
    -----
    Multi-edges and loops are enabled so that the directed graph faithfully
    mirrors the undirected Tait graph even in the presence of R1 or R2
    configurations.
    """
    directed_edges: List[Tuple[int, int, int]] = []

    for crossing in pd_code:
        left_idx, right_idx = _regions_for_crossing(crossing, faces)

        if left_idx is None or right_idx is None:
            # Boundary or split-diagram face — skip.
            continue

        # Find the weight of the corresponding undirected edge.
        weight: Optional[int] = None
        for u, v, w in signed_edges:
            edge_faces = {u, v}
            if edge_faces == {left_idx, right_idx}:
                weight = w
                break

        if weight is None:
            # No matching undirected edge (can happen for isolated crossings).
            continue

        # Silver–Williams direction rule.
        if weight == 1:
            # Positive crossing: left → right.
            directed_edges.append((left_idx, right_idx, weight))
        else:
            # Negative crossing: right → left.
            directed_edges.append((right_idx, left_idx, weight))

    return DiGraph(directed_edges, multiedges=True, loops=True)


def directed_tait_graph_from_knot(K) -> DiGraph:
    """Convenience wrapper: build the directed Tait graph directly from a knot.

    This function calls :func:`tait_graph.core.tait_graph` internally and
    passes its output to :func:`directed_tait_graph`.

    Parameters
    ----------
    K:
        A SageMath knot/link object that exposes ``.pd_code()`` and
        ``.regions()``.

    Returns
    -------
    The directed Tait graph as a SageMath :class:`DiGraph`.
    """
    # Import here to avoid circular imports.
    from tait_graph.core import tait_graph as _tait_graph, _build_faces

    faces, signed_edges = _build_faces(K)
    return directed_tait_graph(K.pd_code(), faces, signed_edges)
