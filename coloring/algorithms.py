"""Online coloring algorithms.

Vertices arrive in increasing order (0, 1, 2, ...). When a vertex arrives the algorithm sees only
its edges to vertices that arrived earlier, and must fix its color immediately. Colors are the
positive integers 1, 2, 3, ...
"""

from collections import deque

from coloring.graphs import Graph

Coloring = dict[int, int]


def smallest_missing(used: set[int]) -> int:
    """The smallest positive integer not in `used`."""
    color = 1
    while color in used:
        color += 1
    return color


def first_fit(graph: Graph) -> Coloring:
    """Give each arriving vertex the smallest color not used by an earlier neighbour."""
    coloring: Coloring = {}
    for v in sorted(graph):
        coloring[v] = smallest_missing({coloring[u] for u in graph[v] if u in coloring})
    return coloring


def cbip(graph: Graph) -> Coloring:
    """Coloring Based on Interval Partitioning, for bipartite graphs.

    When v arrives, take the connected component containing v in the graph revealed so far and
    split it into its two sides. v gets the smallest color not used on the side opposite v.
    CBIP uses O(log n) colors on bipartite graphs, where First-Fit can be forced to use n/2.

    Raises ValueError if a revealed component has an odd cycle, since then it has no two sides.
    """
    coloring: Coloring = {}
    for v in sorted(graph):
        side = _two_sides(graph, v, revealed=coloring.keys() | {v})
        opposite = {u for u, s in side.items() if s == 1}
        coloring[v] = smallest_missing({coloring[u] for u in opposite})
    return coloring


def _two_sides(graph: Graph, start: int, revealed) -> dict[int, int]:
    """BFS from `start` through revealed vertices; map each reached vertex to side 0 or 1."""
    side = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for w in graph[u]:
            if w not in revealed:
                continue
            if w not in side:
                side[w] = 1 - side[u]
                queue.append(w)
            elif side[w] == side[u]:
                raise ValueError(f"the component containing vertex {start} is not bipartite")
    return side


def is_proper(graph: Graph, coloring: Coloring) -> bool:
    """True if every vertex is colored and no edge joins two vertices of the same color."""
    return graph.keys() == coloring.keys() and all(
        coloring[u] != coloring[v] for u in graph for v in graph[u]
    )


def colors_used(coloring: Coloring) -> int:
    return len(set(coloring.values()))
