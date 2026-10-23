"""Random graphs with a known upper bound on the chromatic number.

A graph is a dict mapping each vertex to the set of its neighbours. Vertices are the integers
0..n-1, and that is also the order in which they arrive for the online algorithms.
"""

import random

Graph = dict[int, set[int]]


def random_k_colorable(n: int, k: int, p: float | None = None, rng: random.Random | None = None) -> Graph:
    """Return a random graph on n vertices that can be colored with k colors.

    Vertex i belongs to class i mod k. Every pair of vertices from different classes is joined
    with probability p, and vertices in the same class are never joined, so the k classes are a
    proper k-coloring. When p is None a fresh p is drawn uniformly from [0, 1) for each graph, as
    in the original experiments.
    """
    if n < 0 or k < 1:
        raise ValueError("need n >= 0 and k >= 1")
    rng = rng or random.Random()
    if p is None:
        p = rng.random()

    graph: Graph = {v: set() for v in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if u % k != v % k and rng.random() < p:
                graph[u].add(v)
                graph[v].add(u)
    return graph


def edge_count(graph: Graph) -> int:
    return sum(len(neighbours) for neighbours in graph.values()) // 2
