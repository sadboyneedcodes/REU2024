"""
tait_graph
==========
A SageMath package for computing the Tait graph of a knot or link diagram
from its PD-code, together with related invariants and visualizations.

Modules
-------
core
    :func:`~tait_graph.core.tait_graph` — build the black and white
    checkerboard graphs.
    :func:`~tait_graph.core.white_graph` — convenience accessor for the
    white graph.
    :func:`~tait_graph.core.r1_crossings` — detect R1 (kink) crossings.

weights
    :func:`~tait_graph.weights.compute_weight` — signed weight of a
    Tait-graph edge.
    :func:`~tait_graph.weights.type_weight` — Type I / Type II weighting
    (Chase's scheme).

laplacian
    :func:`~tait_graph.laplacian.weighted_laplacian` — weighted Laplacian
    matrix.
    :func:`~tait_graph.laplacian.reduced_weighted_laplacian` — reduced
    (cofactor) Laplacian.
    :func:`~tait_graph.laplacian.knot_determinant` — knot determinant from
    the Tait graph.

directed
    :func:`~tait_graph.directed.directed_tait_graph` — Silver–Williams
    directed Tait graph from pre-built data.
    :func:`~tait_graph.directed.directed_tait_graph_from_knot` — convenience
    wrapper that accepts a knot object directly.

visualization
    :func:`~tait_graph.visualization.color_and_plot_graph` — plot a Tait
    graph with blue/red edge coloring.
    :func:`~tait_graph.visualization.plot_both_graphs` — plot both
    checkerboard graphs side by side.

Quick start
-----------
In a SageMath session::

    sage: from tait_graph import tait_graph, knot_determinant, color_and_plot_graph
    sage: from sage.knots.knot import Knots
    sage: K = Knots().from_table(3, 1)          # trefoil
    sage: black, white = tait_graph(K)
    sage: knot_determinant(black)
    3
    sage: color_and_plot_graph(black)
"""

from .core import tait_graph, white_graph, r1_crossings
from .weights import compute_weight, type_weight, common_elements
from .laplacian import (
    weighted_laplacian,
    reduced_weighted_laplacian,
    knot_determinant,
    signature_from_laplacian,
)
from .directed import directed_tait_graph, directed_tait_graph_from_knot
from .visualization import color_and_plot_graph, plot_both_graphs

__all__ = [
    # core
    "tait_graph",
    "white_graph",
    "r1_crossings",
    # weights
    "compute_weight",
    "type_weight",
    "common_elements",
    # laplacian
    "weighted_laplacian",
    "reduced_weighted_laplacian",
    "knot_determinant",
    "signature_from_laplacian",
    # directed
    "directed_tait_graph",
    "directed_tait_graph_from_knot",
    # visualization
    "color_and_plot_graph",
    "plot_both_graphs",
]
