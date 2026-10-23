"""Online graph coloring: a k-colorable graph generator and the First-Fit and CBIP algorithms."""

from coloring.algorithms import cbip, colors_used, first_fit, is_proper
from coloring.graphs import random_k_colorable

__all__ = ["cbip", "colors_used", "first_fit", "is_proper", "random_k_colorable"]
