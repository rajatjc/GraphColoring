"""Run the coloring algorithms on many random graphs and summarise their competitive ratios.

The competitive ratio of one run is colors used / k. k is the number of planted classes, which is
an upper bound on the true chromatic number, so this is a lower bound on the true ratio.
"""

import random
from dataclasses import dataclass, field
from statistics import mean

from coloring.algorithms import cbip, colors_used, first_fit
from coloring.graphs import Graph, random_k_colorable

ALGORITHMS = {"first-fit": first_fit, "cbip": cbip}
LABELS = {"first-fit": "First-Fit", "cbip": "CBIP"}


@dataclass
class Result:
    algorithm: str
    ratios: list[float] = field(default_factory=list)

    @property
    def label(self) -> str:
        return LABELS[self.algorithm]

    @property
    def average(self) -> float:
        return mean(self.ratios)

    @property
    def best(self) -> float:
        return min(self.ratios)

    @property
    def worst(self) -> float:
        return max(self.ratios)


@dataclass
class Trials:
    n: int
    k: int
    results: list[Result]
    last_graph: Graph
    last_colorings: dict[str, dict[int, int]]


def run_trials(algorithms: list[str], n: int, k: int, instances: int, rng: random.Random | None = None) -> Trials:
    """Color `instances` random k-colorable graphs on n vertices with each algorithm.

    Every algorithm sees the same graphs, so their ratios can be compared run by run.
    """
    if "cbip" in algorithms and k != 2:
        raise ValueError("CBIP needs bipartite graphs, so k must be 2")
    rng = rng or random.Random()
    results = {name: Result(name) for name in algorithms}
    graph, colorings = {}, {}
    for _ in range(instances):
        graph = random_k_colorable(n, k, rng=rng)
        colorings = {name: ALGORITHMS[name](graph) for name in algorithms}
        for name, coloring in colorings.items():
            results[name].ratios.append(colors_used(coloring) / k)
    return Trials(n, k, list(results.values()), graph, colorings)
