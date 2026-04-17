import networkx as nx


def classical_path(G, source, target):
    path = nx.shortest_path(G, source, target, weight="weight")
    cost = nx.shortest_path_length(G, source, target, weight="weight")
    return path, cost


def quantum_inspired_path(G, source, target):
    path = nx.shortest_path(G, source, target, weight="objective_cost")
    cost = nx.shortest_path_length(G, source, target, weight="objective_cost")
    return path, cost


def path_metrics(G, path):
    raw_distance = 0.0
    normalized_distance = 0.0
    structural_risk = 0.0
    path_amplitude = 1.0

    for u, v in zip(path, path[1:]):
        edge = G[u][v]
        raw_distance += edge["weight"]
        normalized_distance += edge.get("distance_norm", 0.0)
        structural_risk += edge.get("structural_risk", 0.0)
        path_amplitude *= edge.get("transition_amplitude", 1.0)

    return {
        "raw_distance": raw_distance,
        "normalized_distance": normalized_distance,
        "structural_risk": structural_risk,
        "path_amplitude": path_amplitude,
    }
