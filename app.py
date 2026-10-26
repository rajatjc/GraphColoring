import base64
import io
import random

import matplotlib

matplotlib.use("Agg")  # render to PNG in memory; there is no display on a server

import matplotlib.pyplot as plt
import networkx as nx
from flask import Flask, render_template, request

from coloring.algorithms import colors_used
from coloring.experiment import run_trials

app = Flask(__name__)

# What each choice in the "Algorithm" menu runs.
METHODS = {"first-fit": ["first-fit"], "cbip": ["cbip"], "compare": ["first-fit", "cbip"]}

# Bounds on the form inputs, so one request can't tie up the server.
LIMITS = {"k": (1, 10), "n": (1, 500), "instances": (1, 500)}
MAX_WORK = 100_000  # n * instances, per algorithm
MAX_DRAWN_VERTICES = 150  # bigger graphs are unreadable as a picture


def draw_graph(graph, coloring, layout):
    """Return a PNG of the graph, colored by `coloring`, as a base64 string."""
    G = nx.Graph()
    G.add_nodes_from(graph)
    G.add_edges_from((u, v) for u in graph for v in graph[u] if u < v)

    small = len(graph) <= 60
    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw(G, layout, ax=ax, with_labels=small, node_color=[coloring[v] for v in G.nodes()],
            cmap=plt.cm.tab10, vmin=1, vmax=10, node_size=220 if small else 50,
            edge_color="#7a8590", width=1.2, font_color="white", font_size=7)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", transparent=True)
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode()


def parse_form(form):
    """Validate the form. Returns (values, errors)."""
    values, errors = {}, []
    for key, field, label in [("k", "chromatic-number", "Chromatic number"),
                              ("n", "number-of-vertices", "Number of vertices"),
                              ("instances", "number-of-instances", "Number of instances")]:
        low, high = LIMITS[key]
        try:
            values[key] = int(form.get(field, ""))
        except ValueError:
            errors.append(f"{label} must be a whole number.")
            continue
        if not low <= values[key] <= high:
            errors.append(f"{label} must be between {low} and {high}.")

    values["method"] = form.get("coloring-method", "")
    if values["method"] not in METHODS:
        errors.append("Choose First Fit, CBIP or Compare.")

    seed = form.get("seed", "").strip()
    try:
        values["seed"] = int(seed) if seed else None
    except ValueError:
        errors.append("Seed must be a whole number, or left empty.")

    if not errors and values["n"] * values["instances"] > MAX_WORK:
        errors.append(f"Vertices × instances must be at most {MAX_WORK:,}.")
    return values, errors


@app.route("/", methods=["GET", "POST"])
def graph_coloring():
    if request.method == "GET":
        return render_template("index.html", form={})

    values, errors = parse_form(request.form)
    if errors:
        return render_template("index.html", form=request.form, errors=errors), 400

    algorithms = METHODS[values["method"]]
    # CBIP is defined for bipartite graphs, so any run that includes it uses k = 2.
    k = 2 if "cbip" in algorithms else values["k"]
    trials = run_trials(algorithms, values["n"], k, values["instances"], random.Random(values["seed"]))

    drawings = []
    if values["n"] <= MAX_DRAWN_VERTICES:
        # Same positions in every drawing, spread out enough that nodes don't overlap.
        G = nx.Graph(trials.last_graph)
        layout = nx.spring_layout(G, seed=1, k=2.5 / max(len(G), 1) ** 0.5, iterations=100)
        for result in trials.results:
            coloring = trials.last_colorings[result.algorithm]
            drawings.append((result.label, colors_used(coloring), draw_graph(trials.last_graph, coloring, layout)))

    return render_template("index.html", form=request.form, trials=trials, drawings=drawings,
                           k_forced=k != values["k"])


if __name__ == "__main__":
    app.run()
