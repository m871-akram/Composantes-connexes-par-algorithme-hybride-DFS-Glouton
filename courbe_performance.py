#!/usr/bin/env python3
"""
Compare les temps d'exécution du DFS classique et du DFS hybride.

Cherche tous les fichiers exemple_*.pts, lance les deux algos sur chacun,
mesure le temps, et trace la courbe (temps en fonction du nombre de points).
"""

import glob
import os
import time
from typing import Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt

from connectes import print_components_sizes
from dfs_connectes import compute_component_sizes_dfs, load_instance


def measure_performance(
    filename: str,
    algo: Callable,
    algo_name: str,
    k: Optional[int] = None,
) -> Tuple[float, List[int], List]:
    """Lance un algo sur un fichier et renvoie (temps_ms, tailles, points)."""
    distance, points = load_instance(filename)
    if not points:
        print(f"[]  # {filename} (0 points)")
        return float("inf"), [], points

    start = time.perf_counter()
    sizes = algo(distance, points) if k is None else algo(distance, points, k)
    elapsed_ms = (time.perf_counter() - start) * 1000

    print(f"# {algo_name} — {filename} ({len(points)} points): {elapsed_ms:.2f} ms")
    return elapsed_ms, sizes, points


def main() -> None:
    """Détecte les fichiers exemple, mesure les deux algos et trace la courbe."""
    repo_dir = os.path.dirname(__file__)
    files = sorted(glob.glob(os.path.join(repo_dir, "exemple_*.pts")))

    if not files:
        print("No exemple_*.pts files found in the project directory.")
        return

    algorithms = [
        ("Classic DFS", compute_component_sizes_dfs, None),
        ("Hybrid Greedy-DFS (k=8)", print_components_sizes, 8),
    ]

    print("Benchmarking Classic DFS vs. Hybrid Greedy-DFS (k=8)\n")

    performance_data: Dict[str, List[float]] = {name: [] for name, _, _ in algorithms}
    point_counts: List[int] = []

    for filepath in files:
        print(f"--- {os.path.basename(filepath)} ---")
        point_counts.append(0)

        for algo_name, algo, k in algorithms:
            elapsed, sizes, points = measure_performance(filepath, algo, algo_name, k)
            if not points:
                continue

            performance_data[algo_name].append(elapsed)
            if point_counts[-1] == 0:
                point_counts[-1] = len(points)

        print()

    # tracé de la courbe
    plt.figure(figsize=(10, 6))
    for algo_name, times in performance_data.items():
        plt.plot(point_counts[: len(times)], times, marker="o", label=algo_name)

    plt.xlabel("Number of points")
    plt.ylabel("Execution time (ms)")
    plt.title("Classic DFS vs. Hybrid Greedy-DFS (k=8) — Performance Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
