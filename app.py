import base64
import io
import random

import matplotlib

matplotlib.use("Agg")  # render to PNG in memory; there is no display on a server

import matplotlib.pyplot as plt
import networkx as nx
from flask import Flask, render_template, request

from coloring import cbip, colors_used, first_fit, random_k_colorable

app = Flask(__name__)

ALGORITHMS = {"first-fit": first_fit, "cbip": cbip}

# Bounds on the form inputs, so one request can't tie up the server.
LIMITS = {"k": (1, 10), "n": (1, 500), "instances": (1, 500)}
MAX_WORK = 100_000  # n * instances
MAX_DRAWN_VERTICES = 150  # bigger graphs are unreadable as a picture


def draw_graph(graph, coloring):
    """Return a PNG of the graph, colored by `coloring`, as a base64 string."""
    G = nx.Graph()
    G.add_nodes_from(graph)
    G.add_edges_from((u, v) for u in graph for v in graph[u] if u < v)

    fig, ax = plt.subplots(figsize=(7, 7))
    nx.draw(G, nx.spring_layout(G, seed=1), ax=ax, with_labels=len(graph) <= 60,
            node_color=[coloring[v] for v in G.nodes()], cmap=plt.cm.tab10, vmin=1, vmax=10,
            node_size=300 if len(graph) <= 60 else 60, edge_color="#999999", font_color="white")
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
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
    if values["method"] not in ALGORITHMS:
        errors.append("Choose First Fit or CBIP.")
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

    # CBIP is defined for bipartite graphs, so its graphs are always 2-colorable.
    k = 2 if values["method"] == "cbip" else values["k"]
    algorithm = ALGORITHMS[values["method"]]
    rng = random.Random()

    ratios = []
    for _ in range(values["instances"]):
        graph = random_k_colorable(values["n"], k, rng=rng)
        coloring = algorithm(graph)
        ratios.append(colors_used(coloring) / k)

    image = draw_graph(graph, coloring) if values["n"] <= MAX_DRAWN_VERTICES else None
    return render_template("index.html", form=request.form, method=values["method"], k=k,
                           data=sum(ratios) / len(ratios), image=image, last_colors=colors_used(coloring))


if __name__ == "__main__":
    app.run()
