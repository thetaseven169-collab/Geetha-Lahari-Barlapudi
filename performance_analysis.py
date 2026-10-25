"""Empirical performance tests

Writes results/benchmark_results.csv and if matplotlib is installed,
results/selection_runtime.png. Matplotlib is optional, the CSV is always created.
Benchmarks contain the same information to be sorted and check selection answers against the sorting.
"""
from __future__ import annotations

import csv
import random
import statistics
import time
from pathlib import Path
from typing import Callable, Dict, List, Sequence

from part1_selection_algorithms import deterministic_select, randomized_select


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"


def _time_call(function: Callable[[], object], repeats: int) -> float:
    """Return median elapsed seconds over repeats."""
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def _make_data(size: int, distribution: str, seed: int) -> List[int]:
    generator = random.Random(seed)
    if distribution == "random":
        return [generator.randrange(0, max(10, size * 3)) for _ in range(size)]
    if distribution == "sorted":
        return list(range(size))
    if distribution == "reverse-sorted":
        return list(range(size, 0, -1))
    if distribution == "duplicates":
        return [generator.randrange(0, 10) for _ in range(size)]
    raise ValueError(f"Unknown distribution: {distribution}")


def run_benchmarks(
    sizes: Sequence[int] = (100, 500, 1000, 3000),
    distributions: Sequence[str] = ("random", "sorted", "reverse-sorted", "duplicates"),
    repeats: int = 3,
) -> List[Dict[str, object]]:
    """Run both selection algorithms and return rows ready for CSV output."""
    if repeats < 1:
        raise ValueError("repeats must be at least 1.")
    if any(size < 1 for size in sizes):
        raise ValueError("All input sizes must be positive.")

    rows: List[Dict[str, object]] = []
    for size in sizes:
        for distribution_index, distribution in enumerate(distributions):
            data = _make_data(size, distribution, seed=2026 + size + distribution_index)
            k = (size + 1) // 2  # lower median for even sizes; median rank for odd sizes
            expected = sorted(data)[k - 1]

            algorithms = (
                ("deterministic_median_of_medians",
                 lambda data=data, k=k: deterministic_select(data, k)),
                ("randomized_quickselect",
                 lambda data=data, k=k: randomized_select(data, k, random.Random(2026))),
            )
            for algorithm_name, call in algorithms:
                result = call()
                if result != expected:
                    raise AssertionError(
                        f"{algorithm_name} returned {result}; expected {expected}."
                    )
                elapsed = _time_call(call, repeats)
                rows.append({
                    "algorithm": algorithm_name,
                    "input_size": size,
                    "distribution": distribution,
                    "k": k,
                    "median_runtime_seconds": f"{elapsed:.10f}",
                    "repeats": repeats,
                    "result_verified": True,
                })
                print(
                    f"{algorithm_name:34s} n={size:5d} "
                    f"distribution={distribution:14s} median_time={elapsed:.6f}s"
                )
    return rows


def save_csv(rows: Sequence[Dict[str, object]], path: Path) -> None:
    """Write benchmark rows to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "algorithm", "input_size", "distribution", "k",
        "median_runtime_seconds", "repeats", "result_verified",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_plot(rows: Sequence[Dict[str, object]], path: Path) -> bool:
    """Create a runtime plot if matplotlib is available; otherwise return False."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Plot skipped: matplotlib is not installed. CSV results were saved.")
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    distributions = sorted({str(row["distribution"]) for row in rows})
    algorithms = sorted({str(row["algorithm"]) for row in rows})

    for distribution in distributions:
        plt.figure()
        for algorithm in algorithms:
            selected = [
                row for row in rows
                if row["distribution"] == distribution and row["algorithm"] == algorithm
            ]
            selected.sort(key=lambda row: int(row["input_size"]))
            x_values = [int(row["input_size"]) for row in selected]
            y_values = [float(row["median_runtime_seconds"]) for row in selected]
            plt.plot(x_values, y_values, marker="o", label=algorithm)
        plt.xlabel("Input size (n)")
        plt.ylabel("Median runtime (seconds)")
        plt.title(f"Selection algorithm runtime: {distribution}")
        plt.legend()
        plt.tight_layout()
        distribution_path = path.with_name(f"selection_runtime_{distribution}.png")
        plt.savefig(distribution_path, dpi=150)
        plt.close()

    return True


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = run_benchmarks()
    csv_path = RESULTS_DIR / "benchmark_results.csv"
    save_csv(rows, csv_path)
    save_plot(rows, RESULTS_DIR / "selection_runtime.png")
    print(f"\nCSV results saved to: {csv_path}")
    print("Benchmarking complete.")


if __name__ == "__main__":
    main()
