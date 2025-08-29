# Chinese Poker (Pusoy) — Python Implementation

## 1. Introduction
This repository provides a complete Python implementation of **Chinese Poker (Pusoy)**. 
It includes an interactive command-line client, a modular game engine, and measurement utilities for evaluating strategy efficiency and runtime performance.

The project is structured as a package of Python modules with clear separation of concerns:
- **Game engine** — card and deck primitives, player management, hand analysis, arrangement algorithms, and scoring.
- **Client interface** — terminal-based game runner with interactive controls.
- **Measurement tools** — standalone scripts to benchmark runtime, memory, and comparative win rates across heuristics.

---

## 2. Repository Contents

### Core Game Files
- **`card.py`**  
  Defines the `Card` class and suit/value mappings. Provides utilities for card codes, labels, ASCII symbols, and randomization.

- **`deck.py`**  
  Implements the `Deck` class, representing a standard 52-card deck. Supports shuffling (with optional seeds), sorting by value or ID, and dump utilities for debugging.

- **`player.py`**  
  Contains the `Player` class, representing human or bot players. Includes card management, arranged hand storage, scoring fields, and string-format helpers for displaying hands.  
  Also defines `PLAYER_TYPE`, mapping seats (0: human, 1–3: bots).

- **`poker_stat.py`**  
  Provides pre-computed combinatorial statistics, odds, and probabilities of poker hands (both 5-card and 3-card). Used for ranking, analysis, and display of hand types.

- **`poker.py`**  
  The main game engine.  
  Responsibilities:
  - Manages the deck and players
  - Shuffles and distributes 13-card hands
  - Provides arrangement algorithms:
    - `find_best_poker_play` (greedy strategy)
    - `find_balanced_poker_play` (defensive strategy)
  - Validates Chinese Poker ordering (back ≥ middle ≥ front)
  - Implements hand analysis (`analyze_hand`) and evaluation helpers (`has_flush`, `has_straight`, etc.)
  - Calculates scores by comparing each row across players

- **`pusoy.py`**  
  The interactive command-line game client.  
  Features:
  - Welcome banner and rules explanation
  - Menu options for Human vs Human, Human vs Bots, or Quit
  - Human arrangement by swapping positions (1–13)
  - Bot arrangement using greedy or balanced strategies
  - Validation of arrangements and score computation
  - Final display of hand types, results, and winner

### Measurement Files

- **`measurement.py` (simplified)**
  - Benchmarks **heuristic bot arrangements only** across **five fixed configs**:
    1) All Greedy
    2) All Balanced
    3) 2 Greedy / 2 Balanced
    4) 1 Greedy / 3 Balanced
    5) 3 Greedy / 1 Balanced
  - Measures per-config: **overall/per-seat runtime** (avg, p95, max), **peak memory** (via `tracemalloc`), and counters:
    - `greedy_invalid_total` (only invalid orderings)
    - `balanced_ooo_total` (out-of-order allowed, counted)
  - Runs **all five configs in one invocation**; supports `--seed` for reproducibility.

- **`advanced_measurement.py`**
  - **Score-comparison harness** for large runs over these lineups:
    - `all_greedy`, `all_balanced`, `b2g2`, `b3g1`, `b1g3`
  - Prints **win counts / win rates** and **mean scores** per strategy (Greedy, Balanced) for each lineup.
  - Optional `--plots-out` saves **histograms of score distributions** per lineup × strategy.
  - **Extra mode** `--balanced-stats`: counts **Balanced search candidates** across N deals × 4 seats:
    - **Valid hands** (candidates found)
    - **Pruned hands** (valid − 1)
    - Prints totals and per-hand averages.

---

## Reports

- **Advanced Measurement Report.pdf** — Comparative strategy results (win rates, mean scores, histograms) and **Balanced exploration stats**.
- **Intermediate Report.pdf** — Runtime/memory profiling of bot arrangements using `measurement.py` (current focus: the five fixed configurations).

---

---

## 3. How to Run

### 3.1 Interactive Game
From Jupyter notebook, run pusoy.ipynb.

On launch, select:
1. Human vs Human  
2. Human vs Bots  
3. Quit  

**Arrangement phase (for Human players):**
- Input two numbers (1–13) to swap positions  
- Press Enter with no input to submit  
- Enter `A` to auto-arrange using the engine  
- Enter `h` to display hand-rank probabilities (from `poker_stat.py`)  

The program validates order constraints and prints results with per-hand comparisons and cumulative scores.

### 3.2 Programmatic Use
```python
from poker import Poker
from player import PLAYER_TYPE

game = Poker()
game.shuffle_deck(seed=1234)
game.distribute_cards()
game.distribute_hands()

# Arrange
game.auto_arrange_for_player(PLAYER_TYPE['You'], 'greedy')
for pid in range(1,4):
    game.auto_arrange_for_player(pid, 'balanced' if pid==3 else 'greedy')

# Score
game.update_player_scores()
for p in game.players:
    print(p.name, p.hand_score, p.score)
```
----

## 4. Implementation Notes
- Arrangement must satisfy **Chinese Poker ordering rules** (back ≥ middle ≥ front).  
- The **balanced heuristic** can deliberately produce out-of-order hands; measurement tools log these cases.  
- Some evaluation methods (e.g., `has_one_pair`, `has_high_card`) have TODOs for kicker handling.  
- Jokers are included in `Card`, though not standard in Pusoy.  

---

## 5. Requirements
- Python 3.9+  
- Standard library (no external dependencies required for core engine)  
- `matplotlib` for histogram generation in measurement scripts  

---

## 6. References
- Combinatorial counts and odds derived from `poker_stat.py`.  
- Measurement results are detailed in **Intermediate Report.pdf** and **Advanced Measurement Report.pdf**.  
