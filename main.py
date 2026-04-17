from centrality import compute_centrality, normalize_centrality
import config
from graph_utils import create_dynamic_graph_sequence, create_graph, load_graph_from_csv
import networkx as nx
from quantum_model import average_quantum_probabilities, clamp_alpha
from routing import classical_path, path_metrics, quantum_inspired_path
from visualization import draw_graph, plot_alpha_vs_cost
from weight_modifier import modify_weights


def print_quantum_definition():
    print("\n=== Formal Model Definition ===")
    print("Hilbert space: H = span{|v> : v in V}")
    print("State: |psi(t)> = sum_v psi_v(t) |v>")
    print("Evolution: |psi(t)> = exp(-i H_alpha t) |source>")
    print("Hamiltonian: H_alpha = -gamma A_w + alpha * diag(C_norm)")
    print("Routing objective: J_alpha(P) = sum_e [(1-alpha)d_hat(e) + alpha r(e)]")
    print("Alpha range: alpha in [0, 1]")


def resolve_graph():
    custom_graph, message = load_graph_from_csv(config.CUSTOM_GRAPH_CSV)
    print(f"\n[GRAPH INPUT] {message}")

    if custom_graph is None:
        graph = create_graph()
    else:
        graph = custom_graph

    if config.SOURCE not in graph.nodes or config.TARGET not in graph.nodes:
        print(
            "[GRAPH INPUT] The chosen SOURCE/TARGET nodes are not present in the custom graph. "
            "Using the built-in benchmark graph instead."
        )
        graph = create_graph()

    return graph


def run_static_experiment(G, source, target):
    centrality = compute_centrality(G)
    centrality_norm = normalize_centrality(centrality)

    print("\nCentrality:", centrality)
    print("\nNormalized Centrality:", centrality_norm)

    print_quantum_definition()

    classical_route, classical_cost = classical_path(G, source, target)
    print("\n=== Classical Routing ===")
    print(f"Path: {classical_route}")
    print(f"Raw distance: {classical_cost:.4f}")

    alpha_costs = []
    default_route = None
    default_graph = None
    sweep_results = []

    print("\n=== Quantum-Walk-Inspired Routing ===")
    for alpha in config.ALPHA_SWEEP:
        alpha = clamp_alpha(alpha)
        node_probabilities = average_quantum_probabilities(
            G,
            centrality_norm,
            source=source,
            alpha=alpha,
            time_grid=config.TIME_GRID,
            beta=config.BETA,
            gamma=config.GAMMA,
        )
        G_mod = modify_weights(
            G,
            centrality_norm,
            alpha=alpha,
            beta=config.BETA,
            quantum_probabilities=node_probabilities,
        )
        route, objective_cost = quantum_inspired_path(G_mod, source, target)
        metrics = path_metrics(G_mod, route)
        alpha_costs.append(objective_cost)

        print(f"\n--- Alpha = {alpha:.2f} ---")
        print(f"Path: {route}")
        print(f"Objective cost: {objective_cost:.4f}")
        print(f"Raw distance: {metrics['raw_distance']:.4f}")
        print(f"Normalized distance: {metrics['normalized_distance']:.4f}")
        print(f"Structural risk: {metrics['structural_risk']:.4f}")
        print(f"Path amplitude: {metrics['path_amplitude']:.6f}")

        sweep_results.append(
            {
                "alpha": alpha,
                "route": route,
                "graph": G_mod,
                "objective_cost": objective_cost,
            }
        )

        if abs(alpha - config.ALPHA) < 1e-12:
            default_route = route
            default_graph = G_mod

    return classical_route, default_route, default_graph, alpha_costs, sweep_results


def choose_visualization_result(classical_route, default_route, default_graph, sweep_results):
    if default_route is not None and default_route != classical_route:
        return config.ALPHA, default_route, default_graph

    for result in reversed(sweep_results):
        if result["route"] != classical_route:
            return result["alpha"], result["route"], result["graph"]

    return config.ALPHA, default_route, default_graph


def run_dynamic_experiment(base_graph, source, target):
    print("\n=== Dynamic Graph Extension ===")
    dynamic_graphs = create_dynamic_graph_sequence(
        base_graph,
        config.DYNAMIC_EDGE_UPDATES,
    )

    for snapshot_id, graph_snapshot in enumerate(dynamic_graphs, start=1):
        centrality = compute_centrality(graph_snapshot)
        centrality_norm = normalize_centrality(centrality)
        node_probabilities = average_quantum_probabilities(
            graph_snapshot,
            centrality_norm,
            source=source,
            alpha=config.ALPHA,
            time_grid=config.TIME_GRID,
            beta=config.BETA,
            gamma=config.GAMMA,
        )
        G_mod = modify_weights(
            graph_snapshot,
            centrality_norm,
            alpha=config.ALPHA,
            beta=config.BETA,
            quantum_probabilities=node_probabilities,
        )
        route, objective_cost = quantum_inspired_path(G_mod, source, target)
        metrics = path_metrics(G_mod, route)

        print(f"\nSnapshot {snapshot_id}")
        print(f"Route: {route}")
        print(f"Objective cost: {objective_cost:.4f}")
        print(f"Raw distance: {metrics['raw_distance']:.4f}")
        print(f"Structural risk: {metrics['structural_risk']:.4f}")


def main():
    G = resolve_graph()
    classical_route, default_route, default_graph, alpha_costs, sweep_results = run_static_experiment(
        G,
        config.SOURCE,
        config.TARGET,
    )
    run_dynamic_experiment(G, config.SOURCE, config.TARGET)
    shared_pos = nx.spring_layout(G, seed=42)
    visualization_alpha, visualization_route, visualization_graph = choose_visualization_result(
        classical_route,
        default_route,
        default_graph,
        sweep_results,
    )

    print("\n[NOTE] Close each plot window to continue.")
    draw_graph(G, classical_route, "Classical Shortest Path", pos=shared_pos)

    if visualization_route is not None and visualization_graph is not None:
        print(
            f"[VISUALIZATION] Showing quantum-inspired path using alpha={visualization_alpha:.2f} "
            "so the route difference is visible."
        )
        draw_graph(
            visualization_graph,
            visualization_route,
            f"Quantum-Walk-Inspired Path (alpha={visualization_alpha:.2f})",
            pos=shared_pos,
        )

    plot_alpha_vs_cost(config.ALPHA_SWEEP, alpha_costs)


if __name__ == "__main__":
    main()
