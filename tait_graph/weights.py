"""
weights.py
----------
Helpers for determining the signed weight (+1 or -1) of each edge in the
Tait graph, based on the crossing orientation encoded in the PD-code.

A PD-code entry [a, b, c, d] represents a crossing where:
  - a is the incoming under-strand
  - b is the outgoing strand to the left of the over-strand
  - c is the outgoing under-strand
  - d is the incoming strand from the right of the over-strand

Sign convention (following the standard knot-theory orientation):
  - If the first element of the corner pair occupies index 0 or 2 in the
    crossing list, the over-strand passes left-to-right  → positive crossing (+1).
  - If it occupies index 1 or 3, the over-strand passes right-to-left     → negative crossing (-1).
"""

from typing import List, Tuple, Optional


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def find_pd_code(
    pd_code: List[List[int]],
    region: List[int],
    neighboring_region: List[int],
) -> Optional[List[int]]:
    """Return the PD-code entry shared by *region* and *neighboring_region*.

    A crossing is "shared" when the union of the two regions covers all four
    strands of that crossing (i.e. the intersection has exactly 4 elements).

    Parameters
    ----------
    pd_code:
        Full PD-code of the knot/link diagram.  Each entry is a list of four
        integers labelling the strands around one crossing.
    region:
        Strand labels forming one checkerboard region.
    neighboring_region:
        Strand labels forming the adjacent checkerboard region.

    Returns
    -------
    The matching PD-code entry, or ``None`` if no unique match is found.

    Notes
    -----
    TODO: When two regions share more than one crossing (R2-move configurations),
    this function returns the *first* match.  A future revision should accept
    an optional hint (e.g. a specific crossing index) to disambiguate.
    """
    combined: set = set(region).union(set(neighboring_region))
    for pd in pd_code:
        if len(combined.intersection(set(pd))) == 4:
            return pd
    return None


def matches_cyclic_order(corner: List[int], crossing: List[int]) -> bool:
    """Check whether *corner* appears as a consecutive pair in *crossing*.

    Parameters
    ----------
    corner:
        A two-element list ``[a, b]`` representing the 'incoming' and 'next'
        strand around a region at a particular crossing.
    crossing:
        A four-element PD-code entry representing the cyclic order of strands
        around a crossing.

    Returns
    -------
    ``True`` if ``corner[0]`` is immediately followed (mod 4) by ``corner[1]``
    in *crossing*, ``False`` otherwise.
    """
    n = len(crossing)
    for i in range(n):
        if crossing[i] == corner[0] and crossing[(i + 1) % n] == corner[1]:
            return True
    return False


# ---------------------------------------------------------------------------
# Main weight computation
# ---------------------------------------------------------------------------

def compute_weight(
    pd_code: List[List[int]],
    region: List[int],
    neighboring_region: List[int],
) -> int:
    """Compute the signed weight of the Tait-graph edge between two regions.

    Parameters
    ----------
    pd_code:
        Full PD-code of the knot/link diagram.
    region:
        Strand labels of one checkerboard face (as a plain list, not a set,
        so that cyclic ordering is preserved).
    neighboring_region:
        Strand labels of the adjacent checkerboard face.

    Returns
    -------
    ``+1`` for a positive crossing, ``-1`` for a negative crossing.

    Raises
    ------
    ValueError
        If no shared crossing can be found between the two regions, or if the
        corner strand cannot be located in the crossing entry.
    """
    # Cyclic pairs encode the 'corners' seen while walking counter-clockwise
    # around *region*, turning left at each crossing.
    cyclic_pairs: List[List[int]] = [
        [region[i], region[(i + 1) % len(region)]]
        for i in range(len(region))
    ]

    crossing = find_pd_code(pd_code, region, neighboring_region)
    if crossing is None:
        raise ValueError(
            f"No shared crossing found between region {region} "
            f"and neighboring region {neighboring_region}."
        )

    # Corners: cyclic pairs whose both elements appear in this crossing.
    corner_candidates = [
        c for c in cyclic_pairs if len(set(c).intersection(set(crossing))) == 2
    ]

    if len(corner_candidates) > 1:
        # Disambiguate by checking cyclic order within the crossing list.
        matched = [c for c in corner_candidates if matches_cyclic_order(c, crossing)]
        corner = matched[0] if matched else corner_candidates[0]
    elif corner_candidates:
        corner = corner_candidates[0]
    else:
        raise ValueError(
            f"Could not identify a corner for region {region} "
            f"at crossing {crossing}."
        )

    index_of_crossing = crossing.index(corner[0])
    # Indices 0 and 2 correspond to the under-strand → positive crossing.
    return 1 if index_of_crossing in (0, 2) else -1


# ---------------------------------------------------------------------------
# Chase's Type I / Type II weighting scheme
# ---------------------------------------------------------------------------

def type_weight(edge_tuple: Tuple, knot_type: str) -> int:
    """Return the signed weight for Type I / Type II crossings (Chase's scheme).

    Parameters
    ----------
    edge_tuple:
        A graph-edge tuple whose third element (index 2) carries the crossing
        label used to determine parity.
    knot_type:
        Either ``'TypeI'`` or ``'TypeII'``.

    Returns
    -------
    ``+1`` or ``-1`` according to the parity of the crossing label and the
    knot type.

    Raises
    ------
    ValueError
        If *knot_type* is not ``'TypeI'`` or ``'TypeII'``.
    """
    if knot_type not in ("TypeI", "TypeII"):
        raise ValueError(f"knot_type must be 'TypeI' or 'TypeII', got {knot_type!r}.")

    parity = int(edge_tuple[2]) % 2
    if knot_type == "TypeI":
        return 1 if parity == 1 else -1
    else:
        return -1 if parity == 1 else 1


def common_elements(lst: List[int], s: set) -> int:
    """Return the number of elements shared between *lst* and set *s*.

    Parameters
    ----------
    lst:
        A list of integers (typically a region or crossing entry).
    s:
        A set of integers to intersect with.

    Returns
    -------
    The cardinality of the intersection.
    """
    return len(set(lst).intersection(s))
