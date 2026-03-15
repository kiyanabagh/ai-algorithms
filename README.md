# AI Algorithms

Three assignments from CSCE 5210 (Fundamentals of AI) at the University of North Texas,
implementing core AI search algorithms across graph search, local search, and adversarial
game search.

---

## Assignment 1: Route Finding (Python)

Implements a unified graph search that runs either Uniform Cost Search or A* depending
on whether a heuristic file is provided.

**File:** `assignment1-route-finding/find_route.py`

**How it works:**
- Reads a weighted undirected graph from a text file
- Uses a min-heap (priority queue) with a closed set to avoid re-expanding nodes
- Without a heuristic: priority = path cost (UCS)
- With a heuristic: priority = path cost + h(n) (A*)
- Outputs nodes popped, expanded, generated, total distance, and the full route

**Run:**
```bash
# Uninformed (UCS)
python3 find_route.py input1.txt Bremen Kassel

# Informed (A*)
python3 find_route.py input1.txt Bremen Kassel h_kassel.txt
```

---

## Assignment 2: Local Search — 8-Queens (C++)

Four independent C++ programs solving the 8-queens problem using different local
search strategies. Each reads one or more initial board states from a file and reports
final fitness, nodes explored, goal state, and time taken.

Fitness is defined as the number of non-attacking queen pairs (max = 28).

**Files:** `assignment2-local-search/`

| File | Algorithm |
|---|---|
| `hill_climb.cpp` | Steepest-ascent hill climbing |
| `sim_anneal.cpp` | Simulated annealing with exponential cooling |
| `local_beam.cpp` | Local beam search across k states simultaneously |
| `genetic.cpp` | Genetic algorithm with fitness-proportionate selection, single-point crossover, and mutation |

**Compile and run:**
```bash
g++ -o hill_climb hill_climb.cpp && ./hill_climb input1.txt
g++ -o sim_anneal sim_anneal.cpp && ./sim_anneal input1.txt
g++ -o local_beam local_beam.cpp && ./local_beam input1.txt
g++ -o genetic genetic.cpp && ./genetic input1.txt
```

**Input format:** one board state per line, 8 space-separated integers (column-indexed row positions).

---

## Assignment 3: Game Search — Tic-Tac-Toe (Python)

Implements minimax and alpha-beta pruning agents for tic-tac-toe, with node expansion
tracking and an interactive play mode.

**Files:** `assignment3-game-search/`

| File | Contents |
|---|---|
| `tictactoe.py` | Immutable game state, actions, result, terminal test, utility |
| `minimax_agents.py` | Minimax decision, three MIN opponent policies (optimal, random, 40/60 partial) |
| `alphabeta_agents.py` | Vanilla alpha-beta and move-ordered alpha-beta with best-first heuristic |
| `terminal_test.py` | Terminal state tests |
| `print_board.py` | Board display utilities |

**Move ordering heuristic (alpha-beta):** winning move > blocking opponent win > center > corners > edges.
This reduces node expansions measurably compared to vanilla alpha-beta.

**Run:**
```bash
python3 minimax_agents.py    # simulates 50 games vs 3 opponent types, then interactive menu
python3 alphabeta_agents.py  # compares vanilla vs move-ordered, then interactive menu
```

---

## Requirements

- Python 3.8+
- C++11 or later (`g++`)
