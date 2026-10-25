"""Selection algorithms

Public functions use 1-based k (the smallest element is k=1):
- deterministic_select(values, k): Median of Medians, worst-case O(n) time.
- randomized_select(values, k, rng=None): randomized three-way Quickselect,
  expected O(n) time.

Input sequence is not changed, duplication of values is okay.
"""
from __future__ import annotations

import random
from typing import MutableSequence, Optional, Sequence, TypeVar

T = TypeVar("T")


def _validate_k(values: Sequence[T], k: int) -> None:
    """Raise a clear exception when k is not a valid 1-based rank."""
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer.")
    if not values:
        raise ValueError("Cannot select from an empty sequence.")
    if not 1 <= k <= len(values):
        raise ValueError(f"k must be between 1 and {len(values)} inclusive.")


def _median_of_medians(values: MutableSequence[T]) -> T:
    """Return a deterministic pivot using groups of at most five."""
    if len(values) <= 5:
        return sorted(values)[len(values) // 2]

    medians = []
    for start in range(0, len(values), 5):
        group = sorted(values[start:start + 5])
        medians.append(group[len(group) // 2])

    return _median_of_medians(medians)


def deterministic_select(values: Sequence[T], k: int) -> T:
    """Return the k-th smallest value using Median of Medians.

    Args:
        values: Non-empty sequence of mutually orderable values.
        k: 1-based rank (1 means the minimum).

    Returns:
        The value at rank k in sorted order.

    Raises:
        TypeError: If k is not an integer.
        ValueError: If values is empty or k is out of range.
    """
    _validate_k(values, k)
    work = list(values)
    target = k - 1

    while True:
        if len(work) <= 5:
            return sorted(work)[target]

        pivot = _median_of_medians(work)
        lows = [item for item in work if item < pivot]
        equals = [item for item in work if item == pivot]
        highs = [item for item in work if item > pivot]

        if target < len(lows):
            work = lows
        elif target < len(lows) + len(equals):
            return pivot
        else:
            target -= len(lows) + len(equals)
            work = highs


def randomized_select(
    values: Sequence[T],
    k: int,
    rng: Optional[random.Random] = None,
) -> T:
    """Return the k-th smallest value using randomized Quickselect.

    A three-way partition handles duplicate values efficiently. The optional
    random.Random instance makes tests reproducible without changing the
    module-level random generator.
    """
    _validate_k(values, k)
    work = list(values)
    target = k - 1
    generator = rng if rng is not None else random.Random()

    left = 0
    right = len(work) - 1

    while left <= right:
        pivot = work[generator.randint(left, right)]
        lower = left
        current = left
        upper = right

        # Dutch-national-flag partition:
        # [left, lower) < pivot; [lower, current) == pivot;
        # (upper, right] > pivot.
        while current <= upper:
            if work[current] < pivot:
                work[lower], work[current] = work[current], work[lower]
                lower += 1
                current += 1
            elif work[current] > pivot:
                work[current], work[upper] = work[upper], work[current]
                upper -= 1
            else:
                current += 1

        if target < lower:
            right = lower - 1
        elif target <= upper:
            return pivot
        else:
            left = upper + 1

    # This point is unreachable after validation, but keeps the function
    # defensive if its implementation is changed later.
    raise RuntimeError("Selection failed unexpectedly.")


if __name__ == "__main__":
    sample = [7, 2, 9, 2, 5, 1, 8]
    rank = 4
    print(f"Input: {sample}")
    print(f"{rank}-th smallest (deterministic): {deterministic_select(sample, rank)}")
    print(f"{rank}-th smallest (randomized): {randomized_select(sample, rank)}")
