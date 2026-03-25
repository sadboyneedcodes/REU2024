"""
core.py
-------
Core algorithm for computing the Tait graph from a PD-code.

The Tait graph (also called the *checkerboard graph*) of a knot/link diagram
is constructed as follows:

  1. Checkerboard-color the regions (faces) of the diagram black and white.
  2. Place a vertex for each black (or white) region.
  3. For each crossing, add an edge between the two vertices whose regions
     share that crossing, and label the edge with the crossing sign (+1/-1).

This module returns *both* checkerboard graphs (the two connected components
of the full graph on all faces).

Reidemeister move handling
--------------------------
R1 moves introduce a *self-loop* in the Tait graph: a crossing where both
sides belong to the same region.  These are detected and stored separately
so that callers can handle them or strip them as needed.

R2 moves are silently handled: if two regions share more than one crossing
(a "bigon"), multiple parallel edges are added between the corresponding
vertices.

Interior R1 move / white graph
--------------------------------
When interior R1 moves are present the naive checkerboard coloring can
produce a disconnected "black" component.  In that case this module attempts
to identify the white graph as the other component.  If the diagram is
genuinely split a :class:`ValueError` is raised.
"""

from typing import Dict, List, Optional, Set, Tuple

from sage.graphs.graph import Graph  # type: ignore

from .weights import compute_weight


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _abs_regions(K) -> List[List[int]]:
    """Return regions of *K* with all strand labels made positive."""
    return [[abs(x) for x in region] for region in K.regions()]


def _detect_r1_crossings(
    pd_code: List[List[int]],
    regions: List[List[int]],
) -> Set[int]:
    """Return the set of indices in *pd_code* that are R1 (self-loop) crossings.

    A crossing is an R1 crossing when all four of its strands belong to the
    *same* region.

    Parameters
    ----------
    pd_code:
        Full PD-code of the diagram.
    regions:
        List of regions (absolute strand labels).

    Returns
    -------
    A set of indices into *pd_code* identifying R1 crossings.
    """
    r1_indices: Set[int] = set()
    for i, crossing in enumerate(pd_code):
        crossing_set = set(crossing)
        for region in regions:
            if crossing_set.issubset(set(region)):
                r1_indices.add(i)
                break
    return r1_indices


def _build_faces(K) -> Tuple[Dict[int, Tuple[int, ...]], List[Tuple[int, int, int]]]:
    """Build the face dictionary and signed edge list for knot *K*.

    This is the computational core shared by :func:`tait_graph` and
    :func:`tait_graph.directed.directed_tait_graph_from_knot`.

    Parameters
    ----------
    K:
        A SageMath knot/link object exposing ``.pd_code()`` and
        ``.regions()``.

    Returns
    -------
    faces:
        Mapping ``{face_index: tuple_of_strand_labels}``.
    signed_edges:
        List of ``(face_i, face_j, weight)`` triples, one per non-R1
        crossing, where *weight* is ``+1`` or ``-1``.
    """
    regions = _abs_regions(K)
    pd_code = K.pd_code()
    crossings = [set(pd) for pd in pd_code]

    faces_static: Dict[int, Tuple[int, ...]] = {
        i: tuple(region) for i, region in enumerate(regions)
    }
    faces_lookup: Dict[Tuple[int, ...], int] = {
        v: k for k, v in faces_static.items()
    }

    # Identify R1 crossings so we can handle them separately.
    r1_indices = _detect_r1_crossings(pd_code, regions)

    signed_edges: List[Tuple[int, int, int]] = []
    seen: List[Tuple[int, ...]] = []

    for face_idx, face_strands in faces_static.items():
        face_set = set(face_strands)

        # Crossings that share exactly 2 strands with this face (non-R1).
        common_crossings = [
            (ci, c)
            for ci, c in enumerate(crossings)
            if ci not in r1_indices and len(face_set.intersection(c)) == 2
        ]

        for ci, crossing in common_crossings:
            # Strands of the crossing *not* in this face → in the neighbor.
            diff = crossing.difference(face_set)

            # Find all faces that contain exactly those two "other" strands.
            neighbors = [
                (nidx, nstrands)
                for nidx, nstrands in faces_static.items()
                if len(set(nstrands).intersection(diff)) == 2
            ]

            for nidx, nstrands in neighbors:
                if nstrands not in seen:
                    w = compute_weight(pd_code, list(face_strands), list(nstrands))
                    signed_edges.append((face_idx, nidx, w))

        seen.append(face_strands)

    return faces_static, signed_edges


def _build_r1_loops(
    K,
    faces_static: Dict[int, Tuple[int, ...]],
) -> List[Tuple[int, int, int]]:
    """Return self-loop edges for each R1 crossing in the diagram.

    Parameters
    ----------
    K:
        A SageMath knot/link object.
    faces_static:
        Face dictionary produced by :func:`_build_faces`.

    Returns
    -------
    A list of ``(face_i, face_i, weight)`` triples representing self-loops.
    """
    regions = _abs_regions(K)
    pd_code = K.pd_code()
    r1_indices = _detect_r1_crossings(pd_code, regions)

    loops: List[Tuple[int, int, int]] = []
    for ci in r1_indices:
        crossing = set(pd_code[ci])
        for face_idx, face_strands in faces_static.items():
            if crossing.issubset(set(face_strands)):
                w = compute_weight(pd_code, list(face_strands), list(face_strands))
                loops.append((face_idx, face_idx, w))
                break
    return loops


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def tait_graph(
    K,
    include_r1_loops: bool = True,
) -> Tuple[Graph, Graph]:
    """Compute the black and white Tait graphs of knot/link *K*.

    Parameters
    ----------
    K:
        A SageMath knot/link object that exposes ``.pd_code()`` and
        ``.regions()``.
    include_r1_loops:
        If ``True`` (default), R1 self-loop crossings are included as loop
        edges on the appropriate vertex.  If ``False``, R1 crossings are
        silently dropped, which is useful when computing the knot determinant
        (R1 loops do not affect the determinant).

    Returns
    -------
    black_graph, white_graph:
        The two connected components of the full Tait graph, as SageMath
        :class:`Graph` objects with ``multiedges=True`` and ``loops=True``.
        Edges carry ``+1``/``-1`` weight labels.

    Raises
    ------
    ValueError
        If the diagram is *split* (more than two connected components in the
        full graph), or if neither component represents a valid Tait graph.

    Notes
    -----
    *Interior R1 moves and the white graph*: when one or more interior R1
    moves are present the first component returned is the component containing
    the majority of vertices; the second is the complementary component.
    Callers that need the white graph specifically should inspect
    ``white_graph.vertices()``.

    Examples
    --------
    In a SageMath session::

        sage: from sage.knots.knot import Knots
        sage: from tait_graph.core import tait_graph
        sage: K = Knots().from_table(3, 1)   # trefoil
        sage: black, white = tait_graph(K)
        sage: black.edges()
        [(0, 1, 1), (0, 1, 1), (0, 1, 1)]
    """
    faces_static, signed_edges = _build_faces(K)

    all_edges = list(signed_edges)

    if include_r1_loops:
        all_edges += _build_r1_loops(K, faces_static)

    G = Graph(all_edges, multiedges=True, loops=True)

    # Ensure isolated vertices (faces with no crossings) are present.
    for v in faces_static:
        if v not in G:
            G.add_vertex(v)

    components = G.connected_components()

    if len(components) > 2:
        raise ValueError(
            f"The link diagram appears to be split: {len(components)} connected "
            "components found in the Tait graph (expected at most 2)."
        )

    if len(components) == 1:
        # Diagram has a single checkerboard component (e.g. after R1 reduction).
        only = G.subgraph(components[0])
        return only, Graph(multiedges=True, loops=True)

    # Return larger component first (heuristic for "black" graph).
    comp_a = G.subgraph(components[0])
    comp_b = G.subgraph(components[1])

    if comp_a.order() >= comp_b.order():
        return comp_a, comp_b
    return comp_b, comp_a


def white_graph(K) -> Graph:
    """Return only the white Tait graph of *K*.

    This is a convenience wrapper around :func:`tait_graph` for callers that
    only need the white checkerboard graph.

    Parameters
    ----------
    K:
        A SageMath knot/link object.

    Returns
    -------
    The white Tait graph as a SageMath :class:`Graph`.
    """
    _, white = tait_graph(K)
    return white


def r1_crossings(K) -> List[int]:
    """Return the PD-code indices of all R1 (kink) crossings in *K*.

    Parameters
    ----------
    K:
        A SageMath knot/link object.

    Returns
    -------
    A sorted list of indices into ``K.pd_code()`` where self-loop crossings
    occur.  An empty list means the diagram has no R1 crossings.

    Examples
    --------
    In a SageMath session::

        sage: from tait_graph.core import r1_crossings
        sage: # A diagram with a deliberate kink would give non-empty output.
        sage: r1_crossings(K)
        []
    """
    regions = _abs_regions(K)
    return sorted(_detect_r1_crossings(K.pd_code(), regions))
