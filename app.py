from flask import Flask, request, render_template
import networkx as nx
import matplotlib.pyplot as plt

from coloring import cbip, colors_used, first_fit, random_k_colorable

app = Flask(__name__)

ALGORITHMS = {"first-fit": first_fit, "cbip": cbip}


def draw_graph(graph, node_colors=None):
    plt.clf()
    G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    if node_colors is not None:
        colors = [node_colors.get(node, 0) for node in G.nodes()]
        nx.draw(G, pos, node_color=colors, with_labels=True)
    else:
        nx.draw(G, pos, with_labels=True)
    plt.savefig('static/my_plot.png')


@app.route('/', methods=['GET', 'POST'])
def graph_coloring():
    if request.method == 'POST':
        chromatic_number = int(request.form['chromatic-number'])
        num_vertices = int(request.form['number-of-vertices'])
        num_instances = int(request.form['number-of-instances'])
        coloring_method = request.form['coloring-method']
        algorithm = ALGORITHMS[coloring_method]

        # CBIP is defined for bipartite graphs, so its graphs are always 2-colorable.
        if coloring_method == 'cbip':
            chromatic_number = 2

        total_ratio = 0.0
        for _ in range(num_instances):
            graph = random_k_colorable(num_vertices, chromatic_number)
            coloring = algorithm(graph)
            total_ratio += colors_used(coloring) / chromatic_number

        average_value = total_ratio / num_instances

        draw_graph(graph, coloring)
        return render_template('index.html', data=average_value, image="done", method=coloring_method)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
