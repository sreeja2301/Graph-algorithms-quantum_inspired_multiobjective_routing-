import networkx as nx

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


def draw_graph(G, path=None, title="Graph", pos=None):
    if plt is None:
        print(f"[VISUALIZATION SKIPPED] matplotlib is not installed. Could not render: {title}")
        return

    if pos is None:
        pos = nx.spring_layout(G, seed=42)

    edge_labels = nx.get_edge_attributes(G, "weight")

    nx.draw(G, pos, with_labels=True, node_color="lightblue")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=3)

    plt.title(title)
    plt.show()


def plot_alpha_vs_cost(alphas, costs):
    if plt is None:
        print("[VISUALIZATION SKIPPED] matplotlib is not installed. Could not render alpha-cost plot.")
        return

    plt.figure()
    plt.plot(alphas, costs, marker="o")
    plt.xlabel("Alpha")
    plt.ylabel("Objective Cost")
    plt.title("Trade-off Between Alpha and Objective Cost")
    plt.grid(True, alpha=0.3)
    plt.show()
