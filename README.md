# Comparative Analysis of Online Graph Coloring Problem

## Table of Contents

- [Problem Description](#problem-description)
- [Installation](#installation)
- [Usage](#usage)
- [Implementation](#implementation)
- [Algorithms](#algorithms)
- [Graph Generation](#graph-generation)
- [Results](#results)
- [Conclusion](#conclusion)
- [References](#references)

## Problem Description

This project focuses on the Online Graph Coloring Problem, a well-known problem in graph theory. The objective is to assign colors to vertices as they arrive online while minimizing the number of colors used and ensuring adjacent vertices have different colors. Two algorithms, First-Fit and CBIP, are studied for coloring online graphs.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/online-graph-coloring.git
   ```

2. Navigate to the project directory:

   ```bash
   cd online-graph-coloring
   ```

3. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Enter the desired parameters in the UI:
   - Chromatic number (k)
   - Number of vertices (n)
   - Number of instances (N)
   - Choose an algorithm: "First Fit" or "CBIP"
3. Click the "Check" button to generate graphs and analyze results.
4. View the generated graph, coloring method used, and average competitive ratio.

## Implementation
      

### Backend (Python Flask)

- **Graph Generation:** Implemented a function to generate k-colorable online graphs based on user input using the Flask framework.
- **Coloring Algorithm:** Implemented First-Fit and CBIP algorithms as separate functions to color online graphs.
- **Routing:** Set up Flask routes to handle API requests for graph generation and running the coloring algorithms.

### Frontend (HTML, CSS, JavaScript)

- **User Interface:** Designed an interactive UI with input options for chromatic number (k), number of vertices (n), and instances (N).
- **Visualization:** Utilized D3.js to visualize the online graph generation process, algorithm results, competitive ratio, and statistics.
- **API Calls:** Implemented JavaScript functions to make asynchronous calls to Flask APIs for processing and displaying results.

## Algorithms

### Greedy Algorithms

Greedy algorithms make locally optimal choices at each step with the hope of reaching a global optimum solution. Two algorithms are studied:

1. **First-Fit Graph Coloring Algorithm:** Assigns the first available color not used by neighboring vertices.
2. **CBIP Greedy Graph Coloring Algorithm:** Assigns colors using bipartite partitioning.

## Graph Generation

Graphs are generated to be k-colorable, allowing efficient testing of k-coloring algorithms. The vertices are partitioned into subsets, and edges are added with a probability p to create a random graph.

## Results

### First-Fit Greedy Graph Coloring Algorithm

- **N=100:** Comparisons of competitive ratios for various k and n values are presented.
- **N=1000:** Competitive ratios for k=2,3,4 are compared, demonstrating the algorithm's behavior.

### CBIP Greedy Graph Coloring Algorithm

- **N=100:** Competitive ratios for k=2 are analyzed across varying n values.
- **Time Complexity:** CBIP's exponential time complexity for higher k values is discussed.

## Conclusion

This study empirically explores the average competitive ratios of First-Fit and CBIP algorithms. Insights are drawn on their performance, limitations, and computational practicality.


## References

A list of references is provided for the algorithms and concepts used in the project.

[1] Li, Y., Narayan, V.V., Pankratov, D. (2022). Online Coloring and a New Type of Adversary for Online Graph Problems. Algorithmica 84(4), 1232-1251.

[2] Erdős, P., R’enyi, A. (1959). On random graphs I. Publicationes Mathematicae, 6, 290-297.

[3] Kierstead, H., Smith, D., Trotter, W. (2015). First-fit coloring on interval graphs has performance ratio at least 5. European Journal of Combinatorics, 51.
