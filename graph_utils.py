import csv
import os

import networkx as nx


DEFAULT_EDGES = [
    # Fast but bottleneck-heavy corridor
    (0, 1, 1.0),
    (1, 2, 1.0),
    (2, 3, 1.0),
    (3, 9, 1.0),
    # Balanced corridor
    (0, 4, 1.3),
    (4, 5, 1.3),
    (5, 6, 1.3),
    (6, 9, 1.3),
    # Safe detour corridor
    (0, 7, 1.8),
    (7, 8, 1.8),
    (8, 9, 1.8),
    # Cross-links that make nodes 2 and 3 structurally critical
    (2, 4, 0.9),
    (2, 5, 0.9),
    (3, 5, 0.9),
    (3, 6, 0.9),
    (1, 4, 1.2),
    (6, 8, 1.1),
]


def create_graph(edges=None):
    G = nx.Graph()

    for u, v, w in edges or DEFAULT_EDGES:
        G.add_edge(u, v, weight=w)

    return G


def apply_edge_updates(G, edge_updates):
    G_dynamic = G.copy()

    for (u, v), new_weight in edge_updates.items():
        if G_dynamic.has_edge(u, v):
            G_dynamic[u][v]["weight"] = new_weight

    return G_dynamic


def create_dynamic_graph_sequence(base_graph, updates_per_snapshot):
    dynamic_graphs = []
    for edge_updates in updates_per_snapshot:
        dynamic_graphs.append(apply_edge_updates(base_graph, edge_updates))
    return dynamic_graphs


def load_graph_from_csv(csv_path):
    if not csv_path:
        return None, "No custom CSV provided. Using the built-in benchmark graph."

    if not os.path.exists(csv_path):
        return None, (
            f"Custom graph file '{csv_path}' was not found. "
            "Using the built-in benchmark graph instead."
        )

    edges = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for line_number, row in enumerate(reader, start=1):
                if not row or all(not cell.strip() for cell in row):
                    continue

                row = [cell.strip() for cell in row]
                if line_number == 1 and [cell.lower() for cell in row] == [
                    "source",
                    "target",
                    "weight",
                ]:
                    continue

                if len(row) != 3:
                    return None, (
                        f"Custom graph file '{csv_path}' is invalid at line {line_number}. "
                        "Each row must be: source,target,weight. "
                        "Using the built-in benchmark graph instead."
                    )

                try:
                    source = int(row[0])
                    target = int(row[1])
                    weight = float(row[2])
                except ValueError:
                    return None, (
                        f"Custom graph file '{csv_path}' has non-numeric values at line {line_number}. "
                        "Using the built-in benchmark graph instead."
                    )

                if weight <= 0:
                    return None, (
                        f"Custom graph file '{csv_path}' has a non-positive weight at line {line_number}. "
                        "Using the built-in benchmark graph instead."
                    )

                edges.append((source, target, weight))
    except OSError as exc:
        return None, (
            f"Could not read custom graph file '{csv_path}' ({exc}). "
            "Using the built-in benchmark graph instead."
        )

    if not edges:
        return None, (
            f"Custom graph file '{csv_path}' is empty. "
            "Using the built-in benchmark graph instead."
        )

    return create_graph(edges), f"Loaded custom graph from '{csv_path}'."
