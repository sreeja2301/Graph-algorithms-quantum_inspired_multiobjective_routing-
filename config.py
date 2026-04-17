ALPHA = 0.75
ALPHA_SWEEP = [0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]

SOURCE = 0
TARGET = 9

# Optional custom graph CSV.
# Leave as None to use the built-in benchmark graph.
# CSV format: source,target,weight
CUSTOM_GRAPH_CSV = None



# Quantum-walk-inspired model parameters
BETA = 3.0
GAMMA = 1.0
TIME_GRID = [0.5, 1.0, 1.5, 2.0, 3.0]

# Example time-varying edge updates for dynamic routing experiments.
# Each snapshot updates selected edge weights relative to the base graph.
DYNAMIC_EDGE_UPDATES = [
    {(2, 3): 2.0, (3, 9): 2.2},
    {(4, 5): 1.0, (5, 6): 1.0},
    {(7, 8): 1.2, (8, 9): 1.2, (2, 5): 1.4},
]
