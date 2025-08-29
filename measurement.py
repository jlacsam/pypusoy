#!/usr/bin/env python3
"""
measurement.py (simplified)

Benchmark utilities for heuristic bot arrangements only.

Compares five configurations across N games:
1) All Greedy
2) All Balanced
3) 2 Greedy, 2 Balanced
4) 1 Greedy, 3 Balanced
5) 3 Greedy, 1 Balanced

Measures per-game phase times and peak tracemalloc memory,
then summarizes by config. For validity:
- Greedy: count only INVALID orderings.
- Balanced: count out-of-order (OOO) arrangements (allowed).

Usage:
  python measurement.py --games 20 [--seed 123]
"""

from __future__ import annotations

import argparse
import statistics
import time
import tracemalloc
from typing import Any, Callable, Dict, List, Optional, Tuple

# Local game modules (must be in the same project)
from player import PLAYER_TYPE
from poker import Poker


def human_bytes(n: int) -> str:
    step = 1024.0
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    x = float(n)
    while x >= step and i < len(units) - 1:
        x /= step
        i += 1
    return f"{x:.2f} {units[i]}" if i else f"{int(x)} {units[i]}"


def measure(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Tuple[float, int, int, Any]:
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - t0
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed, current, peak, result


def _p95_or_max(xs: List[float]) -> float:
    if not xs:
        return 0.0
    if len(xs) < 20:
        return max(xs)
    return statistics.quantiles(xs, n=20)[18]


def _assignments() -> Dict[str, Dict[int, str]]:
    """
    Return the five requested configurations.
    Players are pids 0..3. We assign deterministically:

    - All Greedy:     all 'greedy'
    - All Balanced:   all 'balanced'
    - 2G,2B:          p0,p1 greedy; p2,p3 balanced
    - 1G,3B:          p0 greedy;    p1,p2,p3 balanced
    - 3G,1B:          p0,p1,p2 greedy; p3 balanced
    """
    return {
        "all_greedy":   {0: "greedy", 1: "greedy", 2: "greedy", 3: "greedy"},
        "all_balanced": {0: "balanced", 1: "balanced", 2: "balanced", 3: "balanced"},
        "2g_2b":        {0: "greedy", 1: "greedy", 2: "balanced", 3: "balanced"},
        "1g_3b":        {0: "greedy", 1: "balanced", 2: "balanced", 3: "balanced"},
        "3g_1b":        {0: "greedy", 1: "greedy", 2: "greedy", 3: "balanced"},
    }


def deal_and_arrange_once(assign_map: Dict[int, str], seed: Optional[int] = None) -> Dict[str, float]:
    """
    Run one full deal with explicit per-player algos, validate, and record metrics.
    Returns per-phase timings/peaks, overall summary, counters, used seed.
    """
    poker = Poker()

    shuffle_seed = int(time.time()) if seed is None else int(seed)
    poker.shuffle_deck(shuffle_seed)
    poker.distribute_cards()
    poker.distribute_hands()

    results: Dict[str, float] = {}
    greedy_invalids = 0
    balanced_ooo = 0

    overall_start = time.perf_counter()
    max_peaks: List[int] = []

    # Arrange players 0..3 per assignment
    for pid in range(4):
        algo = assign_map.get(pid, "greedy")
        e_b, _, p_b, _ = measure(poker.auto_arrange_for_player, pid, algo)
        player = poker.players[pid]
        # Basic shape check
        assert len(player.arranged_cards) == 13, f"Player {pid} arranged cards != 13"

        order_ok = Poker.is_valid_hand(player.arranged_cards)
        if algo == "balanced":
            if not order_ok:
                balanced_ooo += 1
        else:  # greedy
            if not order_ok:
                greedy_invalids += 1

        results[f"p{pid}_time_s"] = e_b
        results[f"p{pid}_peak"] = float(p_b)
        max_peaks.append(p_b)

    # Scoring phase
    e_sc, _, p_sc, _ = measure(poker.update_player_scores)
    for pl in poker.players:
        for row in pl.raw_scores:
            for r in row:
                assert r in (-1, 0, 1), "Score diff must be -1/0/1"

    results["scoring_time_s"] = e_sc
    results["scoring_peak"] = float(p_sc)
    max_peaks.append(p_sc)

    # Overall time and peak
    results["overall_time_s"] = time.perf_counter() - overall_start
    results["overall_peak"] = float(max(max_peaks) if max_peaks else 0)

    # Counters + seed
    results["greedy_invalids"] = float(greedy_invalids)
    results["balanced_ooo"] = float(balanced_ooo)
    results["seed"] = float(shuffle_seed)
    return results


def run_config_suite(games: int, assign_map: Dict[int, str], base_seed: Optional[int] = None) -> Dict[str, float]:
    times_overall: List[float] = []
    peaks_overall: List[float] = []
    p_times = {pid: [] for pid in range(4)}
    p_peaks = {pid: [] for pid in range(4)}
    times_sc: List[float] = []
    peaks_sc: List[float] = []
    greedy_invalids_total = 0
    balanced_ooo_total = 0

    for i in range(games):
        seed_i = None if base_seed is None else (base_seed + i)
        res = deal_and_arrange_once(assign_map, seed=seed_i)

        times_overall.append(res["overall_time_s"])
        peaks_overall.append(res["overall_peak"])
        for pid in range(4):
            p_times[pid].append(res[f"p{pid}_time_s"])
            p_peaks[pid].append(res[f"p{pid}_peak"])
        times_sc.append(res["scoring_time_s"])
        peaks_sc.append(res["scoring_peak"])

        greedy_invalids_total += int(res.get("greedy_invalids", 0))
        balanced_ooo_total += int(res.get("balanced_ooo", 0))

    def _avg(xs: List[float]) -> float:
        return statistics.mean(xs) if xs else 0.0

    out: Dict[str, float] = {
        "overall_time_avg_s": _avg(times_overall),
        "overall_time_p95_s": _p95_or_max(times_overall),
        "overall_time_max_s": max(times_overall) if times_overall else 0.0,
        "overall_peak_avg": _avg(peaks_overall),
        "overall_peak_max": max(peaks_overall) if peaks_overall else 0.0,
        "scoring_time_avg_s": _avg(times_sc),
        "scoring_peak_avg": _avg(peaks_sc),
        "scoring_peak_max": max(peaks_sc) if peaks_sc else 0.0,
        "greedy_invalid_total": float(greedy_invalids_total),
        "balanced_ooo_total": float(balanced_ooo_total),
    }
    for pid in range(4):
        out[f"p{pid}_time_avg_s"] = _avg(p_times[pid])
        out[f"p{pid}_peak_avg"] = _avg(p_peaks[pid])
        out[f"p{pid}_peak_max"] = max(p_peaks[pid]) if p_peaks[pid] else 0.0
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark bots across five greedy/balanced configurations."
    )
    parser.add_argument(
        "--games", type=int, default=5, help="Number of randomized deals per configuration."
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Base seed for reproducible shuffles (seed+i per game)."
    )
    args = parser.parse_args()

    configs = _assignments()

    for name, amap in configs.items():
        print(f"--- {name} ---")
        rb = run_config_suite(args.games, amap, base_seed=args.seed)
        print(
            "OVERALL time avg: {:.6f}s | p95: {:.6f}s | max: {:.6f}s".format(
                rb["overall_time_avg_s"], rb["overall_time_p95_s"], rb["overall_time_max_s"]
            )
        )
        print(
            "OVERALL peak avg: {} | max: {}".format(
                human_bytes(int(rb["overall_peak_avg"])), human_bytes(int(rb["overall_peak_max"]))
            )
        )
        for pid in range(4):
            print(
                f"P{pid} time avg:  {rb[f'p{pid}_time_avg_s']:.6f}s | "
                f"peak avg: {human_bytes(int(rb[f'p{pid}_peak_avg']))} | "
                f"peak max: {human_bytes(int(rb[f'p{pid}_peak_max']))}"
            )
        print(
            "Scoring time avg: {:.6f}s | peak avg: {} | peak max: {}".format(
                rb["scoring_time_avg_s"],
                human_bytes(int(rb["scoring_peak_avg"])),
                human_bytes(int(rb["scoring_peak_max"])),
            )
        )
        print(
            "Greedy invalids (total): {} | Balanced out-of-order (total): {}".format(
                int(rb.get("greedy_invalid_total", 0)),
                int(rb.get("balanced_ooo_total", 0)),
            )
        )
        print()


if __name__ == "__main__":
    main()
