#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
advanced_measurement.py

Score-comparison harness for Chinese Poker (Pusoy).

Lineups tested:
- all_greedy
- all_balanced
- b2g2   (2 Balanced, 2 Greedy)
- b3g1   (3 Balanced, 1 Greedy)
- b1g3   (1 Balanced, 3 Greedy)

For each N in --games, simulate all lineups, print mean scores and win rates,
and save histograms of score distributions (per strategy × lineup).

Extra mode:
--balanced-stats  → counts Balanced search candidates:
  - Valid hands  = number of candidate plays found
  - Pruned hands = candidates not chosen as final (len-1)
across N deals × 4 seats. Prints totals and per-hand averages.

Usage:
  # Score comparisons + histograms
  python advanced_measurement.py --games 20,50,100,1000,10000 --seed 4242 --plots-out plots

  # Balanced candidate counts only (valid/pruned)
  python advanced_measurement.py --games 1000 --seed 4242 --balanced-stats
"""

import argparse
import os
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from poker import Poker  # project engine

# Try to import hand-type bounds; fall back if not exposed.
try:
    from poker import ROYAL_FLUSH, HIGH_CARD  # type: ignore
except Exception:
    ROYAL_FLUSH, HIGH_CARD = 10, 1  # adjust if your enum differs


# --------------------------
# Helpers
# --------------------------

def parse_int_list(csv_ints: str) -> List[int]:
    return [int(x.strip()) for x in csv_ints.split(",") if x.strip()]


def lineup_assign(lineup: str) -> Dict[int, str]:
    """Return seat->strategy mapping for fixed lineups."""
    if lineup == "all_greedy":
        return {s: "greedy" for s in range(4)}
    if lineup == "all_balanced":
        return {s: "balanced" for s in range(4)}
    if lineup == "b2g2":
        return {0: "balanced", 1: "balanced", 2: "greedy", 3: "greedy"}
    if lineup == "b3g1":
        return {0: "balanced", 1: "balanced", 2: "balanced", 3: "greedy"}
    if lineup == "b1g3":
        return {0: "balanced", 1: "greedy", 2: "greedy", 3: "greedy"}
    raise ValueError(f"Unknown lineup: {lineup}")


def winner_seats_from_scores(scores: Dict[int, int]) -> List[int]:
    """Return seat indices of winners (ties possible)."""
    if not scores:
        return []
    max_score = max(scores.values())
    return [s for s, v in scores.items() if v == max_score]


# --------------------------
# Balanced exploration stats
# --------------------------

def _balanced_candidate_counts_for_hand(hand: list) -> Tuple[int, int]:
    """
    Reproduce the Balanced exploration loop (defensive search) just enough
    to count:
      - valid hands: number of candidate plays collected
      - pruned hands: candidates not chosen as final (len-1)
    """
    poker_plays = []
    current_best = HIGH_CARD
    i = ROYAL_FLUSH

    while i > HIGH_CARD:
        cards = hand.copy()
        arranged_cards = []

        # Greedy search for best >= i (engine mutates arranged_cards)
        best_hand = Poker.find_best_poker_play(cards, arranged_cards, i)

        # Only consider valid 13-card orderings
        if not Poker.is_valid_hand(arranged_cards):
            i = best_hand - 1
            continue

        if best_hand > HIGH_CARD and best_hand != current_best:
            poker_plays.append({'best_hand': best_hand, 'hand': arranged_cards})
            current_best = best_hand
            i = best_hand - 1
        else:
            break

    valid_count = len(poker_plays)
    pruned_count = max(valid_count - 1, 0)
    return valid_count, pruned_count


def run_balanced_stats(n_games: int, seed_base: int) -> None:
    """
    Count Balanced candidates across deals × seats.
    Prints totals and per-hand averages.
    """
    total_valid, total_pruned, total_hands = 0, 0, 0

    for game_idx in range(n_games):
        game_seed = seed_base + game_idx
        poker = Poker()
        poker.shuffle_deck(game_seed)
        poker.distribute_cards()
        poker.distribute_hands()

        for seat in range(4):
            hand = poker.players[seat].cards
            valid, pruned = _balanced_candidate_counts_for_hand(hand)
            total_valid += valid
            total_pruned += pruned
            total_hands += 1

    avg_valid = (total_valid / total_hands) if total_hands else 0.0
    avg_pruned = (total_pruned / total_hands) if total_hands else 0.0

    print("\n=== Balanced Exploration Stats ===")
    print(f"Deals: {n_games} | Hands evaluated: {total_hands}")
    print(f"Valid hands (total): {total_valid}")
    print(f"Pruned hands (total): {total_pruned}")
    print(f"Valid per hand (avg): {avg_valid:.3f}")
    print(f"Pruned per hand (avg): {avg_pruned:.3f}")


# --------------------------
# Score-comparison experiment
# --------------------------

def run_experiment(n_games: int, seed_base: int, lineup: str, plots_out: str):
    score_by_strategy: Dict[str, List[int]] = defaultdict(list)
    win_counts: Counter = Counter()

    for game_idx in range(n_games):
        game_seed = seed_base + game_idx
        poker = Poker()
        poker.shuffle_deck(game_seed)
        poker.distribute_cards()
        poker.distribute_hands()

        strat_map = lineup_assign(lineup)
        for seat, strat in strat_map.items():
            poker.auto_arrange_for_player(seat, strat)

        poker.update_player_scores()

        scores = {pid: pl.score for pid, pl in enumerate(poker.players)}
        winners = winner_seats_from_scores(scores)

        for seat, score in scores.items():
            score_by_strategy[strat_map[seat]].append(score)

        for seat in winners:
            win_counts[strat_map[seat]] += 1

    # Mean scores
    means = {k: (sum(v) / len(v)) if v else 0.0 for k, v in score_by_strategy.items()}

    # Win rates
    total_wins = sum(win_counts.values()) or 1
    win_rates = {k: win_counts[k] / total_wins for k in win_counts}

    # Plots
    if plots_out:
        os.makedirs(plots_out, exist_ok=True)
        try:
            import matplotlib.pyplot as plt
            for strat, vals in score_by_strategy.items():
                if not vals:
                    continue
                plt.figure()
                plt.hist(vals, bins=30)
                plt.title(f"{lineup} – {strat} scores (N={n_games})")
                plt.xlabel("Score")
                plt.ylabel("Frequency")
                plt.tight_layout()
                fname = f"{lineup}_{strat}_n{n_games}.png"
                plt.savefig(os.path.join(plots_out, fname))
                plt.close()
        except Exception as exc:
            print(f"[WARN] plotting failed: {exc}")

    return means, win_counts, win_rates


# --------------------------
# CLI
# --------------------------

def main():
    ap = argparse.ArgumentParser(description="Score comparisons for bot lineups.")
    ap.add_argument("--games", type=str, default="20",
                    help="Comma-separated list, e.g., 20,50,100,1000,10000")
    ap.add_argument("--seed", type=int, default=4242,
                    help="Base seed; each game uses seed+i.")
    ap.add_argument("--plots-out", type=str, default=None,
                    help="If set, saves histograms into this directory.")
    ap.add_argument("--balanced-stats", action="store_true",
                    help="Run Balanced exploration stats (valid/pruned counts only).")
    args = ap.parse_args()

    # Balanced stats mode (counts only)
    if args.balanced_stats:
        for n in parse_int_list(args.games):
            print(f"\n=== Balanced Stats: N={n} ===")
            run_balanced_stats(n, args.seed)
        return

    # Score-comparison mode
    n_list = parse_int_list(args.games)
    lineups = ["all_greedy", "all_balanced", "b2g2", "b3g1", "b1g3"]

    for n in n_list:
        print(f"\n=== N={n} games ===")
        for lineup in lineups:
            means, wins, win_rates = run_experiment(n, args.seed, lineup, args.plots_out)
            print(f"\nLineup: {lineup}")
            print(" Mean scores:", {k: round(v, 2) for k, v in means.items()})
            print(" Win counts:", dict(wins))
            print(" Win rates:", {k: f"{v:.1%}" for k, v in win_rates.items()})


if __name__ == "__main__":
    main()
