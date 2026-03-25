"""
visualization.py
----------------
Plotting utilities for Tait graphs.

Positive edges (+1) are drawn in blue; negative edges (-1) are drawn in red.
This matches the standard checkerboard-coloring convention used in the
knot-theory literature.
"""

from typing import Optional
from sage.graphs.graph import Graph  # type: ignore


def color_and_plot_graph(
    G: Graph,
    figsize: int = 6,
    positive_color: str = "blue",
    negative_color: str = "red",
    vertex_size: int = 200,
    vertex_labels: bool = True,
) -> None:
    """Display the Tait graph with signed-edge coloring.

    Edges with weight ``+1`` are drawn in *positive_color* (default blue) and
    edges with weight ``-1`` are drawn in *negative_color* (default red).

    Parameters
    ----------
    G:
        A SageMath :class:`Graph` whose edge labels are ``+1`` or ``-1``.
    figsize:
        Side length (in inches) of the square plot window (default ``6``).
    positive_color:
        Color used for positive (``+1``) edges (default ``'blue'``).
    negative_color:
        Color used for negative (``-1``) edges (default ``'red'``).
    vertex_size:
        Size of the vertex markers in the plot (default ``200``).
    vertex_labels:
        Whether to display vertex labels (default ``True``).

    Returns
    -------
    ``None``; the plot is displayed via SageMath's ``.show()`` mechanism.

    Examples
    --------
    In a SageMath session::

        sage: from sage.knots.knot import Knots
        sage: from tait_graph.core import tait_graph
        sage: from tait_graph.visualization import color_and_plot_graph
        sage: K = Knots().from_table(3, 1)   # trefoil
        sage: black, white = tait_graph(K)
        sage: color_and_plot_graph(black)
    """
    positive_edges = [e for e in G.edge_iterator() if e[2] == 1]
    negative_edges = [e for e in G.edge_iterator() if e[2] == -1]

    G.plot(
        edge_color=positive_color,
        edge_colors={negative_color: negative_edges},
        vertex_size=vertex_size,
        vertex_labels=vertex_labels,
        figsize=figsize,
    ).show()


def plot_both_graphs(
    black_graph: Graph,
    white_graph: Graph,
    figsize: int = 6,
) -> None:
    """Display the black and white Tait graphs side by side.

    Parameters
    ----------
    black_graph:
        The first connected component returned by :func:`tait_graph.core.tait_graph`.
    white_graph:
        The second connected component returned by :func:`tait_graph.core.tait_graph`.
    figsize:
        Side length (in inches) of each individual square plot (default ``6``).

    Returns
    -------
    ``None``; both plots are displayed sequentially.
    """
    print("Black Tait graph:")
    color_and_plot_graph(black_graph, figsize=figsize)
    print("White Tait graph:")
    color_and_plot_graph(white_graph, figsize=figsize)
