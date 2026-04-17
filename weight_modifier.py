import math

from quantum_model import clamp_alpha


def compute_amplitude(objective_cost, beta):
    return math.exp(-0.5 * beta * objective_cost)


def modify_weights(G, centrality_norm, alpha, beta, quantum_probabilities=None):
    alpha = clamp_alpha(alpha)
    G_mod = G.copy()

    max_weight = max(data["weight"] for _, _, data in G_mod.edges(data=True))

    for u, v, data in G_mod.edges(data=True):
        original_weight = data["weight"]
        distance_norm = original_weight / max_weight if max_weight else 0.0

        if quantum_probabilities is None:
            structural_risk = 0.5 * (centrality_norm[u] + centrality_norm[v])
        else:
            structural_risk = 0.5 * (
                quantum_probabilities[u] + quantum_probabilities[v]
            )

        objective_cost = ((1.0 - alpha) * distance_norm) + (alpha * structural_risk)
        amplitude = compute_amplitude(objective_cost, beta)

        data["distance_norm"] = distance_norm
        data["structural_risk"] = structural_risk
        data["objective_cost"] = objective_cost
        data["modified_weight"] = objective_cost
        data["transition_amplitude"] = amplitude

    return G_mod
