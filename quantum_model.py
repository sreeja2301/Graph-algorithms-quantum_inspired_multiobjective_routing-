import math

import numpy as np


def clamp_alpha(alpha):
    return max(0.0, min(1.0, alpha))


def basis_state(size, index):
    state = np.zeros(size, dtype=complex)
    state[index] = 1.0 + 0.0j
    return state


def build_hamiltonian(G, centrality_norm, alpha, beta=3.0, gamma=1.0):
    alpha = clamp_alpha(alpha)
    nodes = sorted(G.nodes())
    node_index = {node: idx for idx, node in enumerate(nodes)}
    size = len(nodes)
    adjacency = np.zeros((size, size), dtype=float)

    max_weight = max(data["weight"] for _, _, data in G.edges(data=True))
    for u, v, data in G.edges(data=True):
        i = node_index[u]
        j = node_index[v]
        weight_norm = data["weight"] / max_weight if max_weight else 0.0
        coupling = math.exp(-beta * weight_norm)
        adjacency[i, j] = coupling
        adjacency[j, i] = coupling

    potential = np.diag([centrality_norm[node] for node in nodes])
    hamiltonian = (-gamma * adjacency) + (alpha * potential)
    return hamiltonian, nodes, node_index


def evolve_state(hamiltonian, source_index, time_value):
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    initial_state = basis_state(hamiltonian.shape[0], source_index)
    spectral_weights = eigenvectors.conj().T @ initial_state
    phases = np.exp(-1j * eigenvalues * time_value)
    evolved_state = eigenvectors @ (phases * spectral_weights)
    return evolved_state


def average_quantum_probabilities(
    G,
    centrality_norm,
    source,
    alpha,
    time_grid,
    beta=3.0,
    gamma=1.0,
):
    hamiltonian, nodes, node_index = build_hamiltonian(
        G,
        centrality_norm,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
    )
    source_index = node_index[source]
    average_prob = np.zeros(len(nodes), dtype=float)

    for time_value in time_grid:
        psi_t = evolve_state(hamiltonian, source_index, time_value)
        average_prob += np.abs(psi_t) ** 2

    average_prob /= len(time_grid)
    return {node: float(average_prob[node_index[node]]) for node in nodes}
