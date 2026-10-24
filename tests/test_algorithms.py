import math
import random

import pytest

from coloring import cbip, colors_used, first_fit, is_proper, random_k_colorable
from coloring.algorithms import smallest_missing
from coloring.graphs import edge_count


def from_edges(n, edges):
    graph = {v: set() for v in range(n)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


def crown(pairs):
    """K(m,m) minus a perfect matching, arriving a0, b0, a1, b1, ...

    a_i (vertex 2i) is joined to every b_j (vertex 2j+1) except b_i. This order is the classic
    trap for First-Fit: a_i and b_i both get color i+1, so it needs `pairs` colors for a
    2-colorable graph.
    """
    return from_edges(2 * pairs, [(2 * i, 2 * j + 1) for i in range(pairs) for j in range(pairs) if i != j])


def test_smallest_missing():
    assert smallest_missing(set()) == 1
    assert smallest_missing({1, 2, 4}) == 3
    assert smallest_missing({2, 3}) == 1


@pytest.mark.parametrize("algorithm", [first_fit, cbip])
def test_empty_and_edgeless_graphs(algorithm):
    assert algorithm({}) == {}
    assert algorithm({0: set(), 1: set(), 2: set()}) == {0: 1, 1: 1, 2: 1}


@pytest.mark.parametrize("algorithm", [first_fit, cbip])
def test_path_uses_two_colors(algorithm):
    path = from_edges(6, [(i, i + 1) for i in range(5)])
    coloring = algorithm(path)
    assert is_proper(path, coloring)
    assert colors_used(coloring) == 2


def test_first_fit_falls_into_the_crown_trap():
    for pairs in (2, 5, 10, 20):
        coloring = first_fit(crown(pairs))
        assert is_proper(crown(pairs), coloring)
        assert colors_used(coloring) == pairs


def test_cbip_stays_logarithmic_on_the_crown():
    for pairs in (5, 10, 20, 40):
        n = 2 * pairs
        coloring = cbip(crown(pairs))
        assert is_proper(crown(pairs), coloring)
        assert colors_used(coloring) <= 2 * math.log2(n)


def test_cbip_only_looks_at_the_revealed_graph():
    # 0 and 1 are joined only through vertex 2, which arrives last. When 1 arrives, its component
    # is just {1}, so it reuses color 1 even though 0 and 1 end up on the same side.
    graph = from_edges(3, [(0, 2), (1, 2)])
    assert cbip(graph) == {0: 1, 1: 1, 2: 2}


def test_cbip_rejects_odd_cycles():
    triangle = from_edges(3, [(0, 1), (1, 2), (0, 2)])
    with pytest.raises(ValueError, match="not bipartite"):
        cbip(triangle)


@pytest.mark.parametrize("k", [1, 2, 3, 5])
def test_random_graphs_are_k_colorable_and_colored_properly(k):
    rng = random.Random(k)
    for _ in range(50):
        graph = random_k_colorable(rng.randint(0, 40), k, rng=rng)
        assert is_proper(graph, {v: v % k for v in graph})  # the planted classes
        assert is_proper(graph, first_fit(graph))
        if k <= 2:
            assert is_proper(graph, cbip(graph))


def test_generator_edge_probability_extremes():
    assert edge_count(random_k_colorable(30, 3, p=0)) == 0
    # p=1 gives the complete 3-partite graph with classes of 10: 3 * 10 * 10 edges
    assert edge_count(random_k_colorable(30, 3, p=1)) == 300


def test_generator_is_reproducible_with_a_seed():
    assert random_k_colorable(25, 3, rng=random.Random(42)) == random_k_colorable(25, 3, rng=random.Random(42))


def test_generator_rejects_bad_arguments():
    with pytest.raises(ValueError):
        random_k_colorable(10, 0)
    with pytest.raises(ValueError):
        random_k_colorable(-1, 2)


def test_is_proper_catches_conflicts_and_missing_vertices():
    graph = from_edges(3, [(0, 1)])
    assert not is_proper(graph, {0: 1, 1: 1, 2: 1})
    assert not is_proper(graph, {0: 1, 1: 2})
