



from flask import Flask, request, render_template
import networkx as nx
import random
import matplotlib.pyplot as plt

app = Flask(__name__)

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


def random_graph_generator(n, k):
        # Step 1: partition the vertices into k disjoint subsets
        value = random.random()
        p = value

        subsets = [[] for _ in range(k)]
        for i in range(n):
            subsets[i % k].append(i)

        # Step 2: generate edges between vertices in different subsets
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if i in subsets[j % k] or j in subsets[i % k]:
                    # vertices belong to the same subset, do nothing
                    continue
                elif random.random() < p:
                    # generate edge with probability p
                    edges.add((i, j))

        # Construct the graph as a dictionary of adjacency lists
        graph = {i: [] for i in range(n)}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        return graph


def bipartite_is(graph):
    i_set = set()
    i_set2 = set()
    visited = set()

    # LAST VERTEX ADD TO INDEPENDENT VERTEX 1
    st_v = len(list(graph.nodes())) - 1
    i_set.add(st_v)
    visited.add(st_v)

    # PERFORM BFS
    qu = [st_v]
    while qu:
        ver = qu.pop(0)
        for neighbor in graph[ver]:
            if neighbor not in visited:
                # add neighbor to the opposite independent set
                if ver in i_set:
                    i_set2.add(neighbor)
                else:
                    i_set.add(neighbor)
                visited.add(neighbor)
                qu.append(neighbor)

    # return the two independent sets
    return list(i_set), list(i_set2)



def CBIP(G):

  find_minimum_integer = lambda lst: next(i for i in range(1, len(lst) + 2) if i not in set(lst))
  G = nx.Graph(G)
  n = len(G.nodes())
  if n<1:
    return []
  #Color the first vertice 1 as our base case.
  color_list = [1]
  for i in range(1,n):
    other_part_colors = []
    other_part = bipartite_is(G.subgraph(range(i + 1)))[1]
    for j in other_part:
      other_part_colors.append(color_list[j])
    color = find_minimum_integer(other_part_colors)
    color_list.append(color)
  return color_list

def firstfit(graph):
    """
    Implementation of First-Fit algorithm for graph coloring that minimizes the number of colors used.

    Parameters:
    graph (dict): A dictionary representing the graph.

    Returns:
    A dictionary representing the color assignments for each vertex.
    """
    # Initialize an empty dictionary to store the color assignments for each vertex.
    colors = {}

    # Loop through each vertex in the graph.
    for vertex in graph:
        # Create a set of colors that have already been assigned to the vertex's neighbors.
        used_colors = set(colors.get(neighbor) for neighbor in graph[vertex] if neighbor in colors)

        # Initialize a set of available colors.
        available_colors = set(range(len(graph))) - used_colors

        # If there are available colors, assign the first one in the set.
        if available_colors:
            colors[vertex] = min(available_colors)
        else:
            # If there are no available colors, assign a new color to the vertex.
            colors[vertex] = len(graph)

    return colors


@app.route('/', methods=['GET', 'POST'])
def graph_coloring():
    if request.method == 'POST':
        chromatic_number = int(request.form['chromatic-number'])
        num_vertices = int(request.form['number-of-vertices'])
        num_instances = int(request.form['number-of-instances'])
        coloring_method = request.form['coloring-method']
        total_average = 0.0

        for _ in range(num_instances):
            graph = random_graph_generator(num_vertices, chromatic_number)

            if coloring_method == 'cbip':
                coloring = CBIP(graph)
                unique_values = set(coloring)
            else:
                coloring = firstfit(graph)
                unique_values = set(coloring.values())

            total_average += len(unique_values) / chromatic_number

        average_value = total_average / num_instances

        if coloring_method == 'cbip':
            colormap = {index: num for index, num in enumerate(coloring)}
        else:
            colormap = coloring

        node_colors = {node: colormap.get(node, 0) for node in graph.keys()}
        draw_graph(graph, node_colors)
        return render_template('index.html', data=average_value, image="done", method=coloring_method)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
