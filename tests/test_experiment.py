import random

import pytest

from coloring import is_proper
from coloring.experiment import run_trials


def test_each_algorithm_gets_one_ratio_per_graph():
    trials = run_trials(["first-fit", "cbip"], n=30, k=2, instances=25, rng=random.Random(0))
    assert [r.algorithm for r in trials.results] == ["first-fit", "cbip"]
    for result in trials.results:
        assert len(result.ratios) == 25
        assert result.best <= result.average <= result.worst
        assert all(r >= 0.5 for r in result.ratios)  # a nonempty graph needs at least 1 of the k=2 colors


def test_last_graph_and_colorings_match():
    trials = run_trials(["first-fit", "cbip"], n=20, k=2, instances=3, rng=random.Random(1))
    for coloring in trials.last_colorings.values():
        assert is_proper(trials.last_graph, coloring)


def test_same_seed_same_results():
    a = run_trials(["first-fit"], n=40, k=3, instances=10, rng=random.Random(5))
    b = run_trials(["first-fit"], n=40, k=3, instances=10, rng=random.Random(5))
    assert a.results[0].ratios == b.results[0].ratios


def test_cbip_requires_k_2():
    with pytest.raises(ValueError, match="k must be 2"):
        run_trials(["cbip"], n=10, k=3, instances=1)
