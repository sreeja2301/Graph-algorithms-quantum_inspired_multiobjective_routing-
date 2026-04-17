# Quantum-Walk-Inspired Routing Model

A quantum-walk-inspired classical routing framework that integrates weighted graph topology with centrality-based structural risk assessment.

## Overview

This project proposes a multi-objective routing model on weighted graphs. The walker evolves over the vertex Hilbert space under a Hamiltonian that combines weighted adjacency and a centrality-based potential term. The resulting time-averaged node occupation probabilities define a structural-risk score, which is integrated with normalized path distance through a bounded trade-off parameter `alpha ∈ [0,1]`.
#### 5. How to Run (Generic)
Step 1: Clone the repository
```git clone <your-repo-url>```
```cd <project-folder>```

Step 2: Create and activate virtual environment
Windows (CMD)
```python -m venv .venv```
```.venv\Scripts\activate```
Windows (PowerShell)
```python -m venv .venv```
```.venv\Scripts\Activate.ps1```
macOS/Linux (bash/zsh)
```python3 -m venv .venv```
```source .venv/bin/activate```
Step 3: Install dependencies
```pip install -r requirements.txt```
Step 4: Run the project
```python main.py```

## Mathematical Foundations

### 1. Quantum State and Hilbert Space

- **Graph**: `G = (V, E, w)`
- **Hilbert space**: `H = span{|v⟩ : v ∈ V}`
- **State vector**: `|ψ(t)⟩ = Σ_{v ∈ V} ψ_v(t) |v⟩`

### 2. Hamiltonian Formulation

The evolution is governed by:

```
H_α = -γA_w + α·diag(C_norm)
```

Where:
- `A_w` is the weighted adjacency-derived coupling matrix
- `γ > 0` controls walk diffusion
- `C_norm(v) ∈ [0, 1]` is the normalized node centrality
- `α ∈ [0, 1]` is the trade-off parameter

### 3. Quantum Walk Evolution

The state evolves as:

```
|ψ(t)⟩ = exp(-i H_α t) |s⟩
```

starting from source node `|s⟩`.

Node occupation probabilities are:

```
p_t(v) = |⟨v|ψ(t)⟩|²
```

The model uses time-averaged probabilities:

```
q(v) = (1 / T) Σ_{t ∈ T_grid} p_t(v)
```

as a structural congestion or exposure score.

### 4. Multi-Objective Path Cost

**Normalized edge distance**:
```
d̂(u, v) = w(u, v) / max_{e ∈ E} w(e)
```

**Structural risk on edge (u, v)**:
```
r(u, v) = (q(u) + q(v)) / 2
```

**Path objective** for path `P = (v_0 = s, v_1, ..., v_k = t)`:
```
J_α(P) = Σ_{i=0}^{k-1} [(1 - α)·d̂(v_i, v_{i+1}) + α·r(v_i, v_{i+1})]
```

**Optimal route**:
```
P*(α) = arg min_P J_α(P)
```

### 5. Amplitude Model

Edge-level amplitude preservation:

```
A(u, v) = exp(-(β / 2) J_α(u, v))
```

Where `β > 0` is a sensitivity parameter. Larger `β` increases discrimination between good and bad edges.

Path amplitude proxy:

```
A(P) = ∏_{e ∈ P} A(e)
```

### 6. Trade-off Parameter Interpretation

The `alpha` parameter provides a convex trade-off:

- `α = 0`: Pure distance minimization
- `α = 1`: Pure structural-risk minimization  
- `0 < α < 1`: Convex trade-off between both objectives

## Key Features

- **Formal Quantum Model**: Explicit Hilbert space and Hamiltonian formulation
- **Multi-Objective Optimization**: Balanced trade-off between distance and structural risk
- **Centrality Integration**: Incorporates node importance through normalized centrality
- **Dynamic Graph Support**: Handles time-varying graphs with snapshot-based recomputation
- **Interpretable Scores**: Time-averaged occupation probabilities as structural exposure metrics

## Implementation Details

### Dynamics

For dynamic graph sequences `G^(1), G^(2), ..., G^(T)`, the model recomputes at each snapshot τ:

1. `C_norm^(τ)` - Normalized centrality
2. `H_α^(τ)` - Hamiltonian
3. `q^(τ)(v)` - Time-averaged occupation probabilities
4. `J_α^(τ)(P)` - Path objective
5. `P*^(τ)` - Optimal route

### Complexity Analysis

**Per-snapshot complexity**:
- Centrality computation: depends on chosen routine
- Hamiltonian eigendecomposition: `O(|V|³)`
- Dijkstra shortest path on modified costs: `O(|E| log |V|)`

### Important Note

This is a **quantum-walk-inspired classical routing framework**. The current implementation:
- ✓ Imports quantum walk concepts into routing design
- ✓ Provides interpretable amplitude and occupation-probability based heuristics
- ✓ Offers principled multi-objective trade-off optimization

This is **not**:
- A fault-tolerant quantum algorithm
- Claiming proven quantum complexity advantage
- A substitute for classical shortest-path algorithms

## Project Structure

```
centrality.py          - Node centrality computation
config.py              - Configuration parameters
graph_utils.py         - Graph construction and manipulation utilities
main.py                - Main routing pipeline
quantum_model.py       - Quantum walk evolution and Hamiltonian
routing.py             - Route optimization and path finding
visualization.py       - Visualization utilities
weight_modifier.py     - Edge weight adjustment based on quantum scores
sample_graph.csv       - Example graph data
requirements.txt       - Python dependencies
```

## Usage

1. Configure parameters in `config.py` (gamma, alpha, beta, etc.)
2. Load or generate a graph using `graph_utils.py`
3. Run the routing pipeline via `main.py`
4. Visualize results using `visualization.py`

## Literature Context

**Research Streams**:
1. Classical shortest-path and centrality-aware routing
2. Multi-objective routing and weighted trade-off optimization
3. Quantum walk formulations on graphs
4. Dynamic or time-varying graph routing

**Research Gap**:
This work addresses the intersection of these areas by:
- Formalizing a quantum-walk-inspired occupancy model within routing
- Explicitly bounding the trade-off parameter `α` with clear interpretation
- Integrating structural exposure (from quantum occupation) with path distance
- Supporting dynamic graph evolution with quantum-aware re-routing

## References

- Quantum walks on graphs literature
- Classical network routing optimization
- Multi-objective path planning
- Centrality-based network analysis

---

**Version**: 1.0  
**Description**: Quantum-Walk-Inspired Multi-Objective Routing on Weighted Graphs
