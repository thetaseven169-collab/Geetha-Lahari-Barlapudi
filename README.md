# Algorithms and Data Structures Assignment

This repository contains Python implementations developed for an
Algorithms and Data Structures assignment. The work is organised into
two main parts:

1.  **Selection algorithms** for finding the *k*-th smallest element
    without sorting the entire input.
2.  **Elementary data structures** implemented using Python classes.

A separate benchmarking script measures the selection algorithms across
multiple input sizes and data distributions. Benchmark results are
written to CSV, and runtime charts are generated when Matplotlib is
installed.

## Repository Contents

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  File or folder                                                                                                                                                                      Description
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------
  `part1_selection_algorithms.py`                                                                                                                                                     Implements deterministic selection
                                                                                                                                                                                      using the Median of Medians method
                                                                                                                                                                                      and randomized selection using
                                                                                                                                                                                      three-way Quickselect.

  `part2_data_structures.py`                                                                                                                                                          Implements `ArrayList`, `Matrix`,
                                                                                                                                                                                      `ArrayStack`, `ArrayQueue`, and
                                                                                                                                                                                      `SinglyLinkedList`.

  `performance_analysis.py`                                                                                                                                                           Benchmarks both selection
                                                                                                                                                                                      algorithms, verifies their answers
                                                                                                                                                                                      against sorting, and exports
                                                                                                                                                                                      performance results.

  `results.zip`                                                                                                                                                                       Archive of result files included in
                                                                                                                                                                                      the repository.

  `University of the Cumberlands Fall’26 Term 1 Algorithms and Data Structures Assignment 6 Medians and Order Statistics & Elementary Data Structures Geetha Lahari Barlapudi.docx`   Assignment document included in the
                                                                                                                                                                                      repository.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Requirements

-   Python 3.9 or later is recommended.
-   No third-party package is required to run the core implementations
    or generate the benchmark CSV file.
-   `matplotlib` is optional. It is required only for generating runtime
    charts.

Install Matplotlib if charts are required:

``` bash
python -m pip install matplotlib
```

## Getting Started

Clone the repository:

``` bash
git clone https://github.com/thetaseven169-collab/Geetha-Lahari-Barlapudi.git
cd Geetha-Lahari-Barlapudi
```

Run the selection algorithm demonstration:

``` bash
python part1_selection_algorithms.py
```

Run the data structures demonstration:

``` bash
python part2_data_structures.py
```

Run the performance benchmarks:

``` bash
python performance_analysis.py
```

## Part 1: Selection Algorithms

The module `part1_selection_algorithms.py` provides two public
functions.

### 1. Deterministic Selection --- Median of Medians

``` python
from part1_selection_algorithms import deterministic_select

values = [7, 2, 9, 2, 5, 1, 8]
rank = 4

result = deterministic_select(values, rank)
print(result)
```

The Median of Medians method selects a pivot by dividing values into
groups of up to five, finding each group's median, and recursively
selecting a pivot from those medians. The input is partitioned into
values lower than, equal to, and higher than the pivot. The relevant
partition is processed until the requested rank is found.

-   **Worst-case time complexity:** O(n)
-   **Additional space:** O(n) in this implementation, due to copied and
    partitioned lists.

### 2. Randomized Selection --- Three-Way Quickselect

``` python
from part1_selection_algorithms import randomized_select

values = [7, 2, 9, 2, 5, 1, 8]
rank = 4

result = randomized_select(values, rank)
print(result)
```

Randomized Quickselect chooses a pivot at random and uses a three-way
(Dutch-national-flag) partition. The partition separates values smaller
than, equal to, and greater than the pivot. This approach also handles
duplicate values efficiently.

-   **Expected time complexity:** O(n)
-   **Worst-case time complexity:** O(n²)
-   **Additional space:** O(n) for the working copy; partitioning is
    performed iteratively.

### Rank and Input Behaviour

Both public selection functions use a **1-based rank**:

-   `k = 1` returns the smallest value.
-   `k = len(values)` returns the largest value.
-   Duplicate values are supported.
-   The supplied input sequence is not modified; a working copy is used.
-   An empty input or an out-of-range rank raises `ValueError`.
-   A non-integer rank, including a Boolean value, raises `TypeError`.

For reproducible randomized selection, an optional `random.Random`
instance can be supplied through the `rng` parameter:

``` python
import random
from part1_selection_algorithms import randomized_select

values = [12, 4, 7, 4, 19, 2]
result = randomized_select(values, 3, rng=random.Random(2026))
print(result)
```

## Part 2: Elementary Data Structures

The module `part2_data_structures.py` contains five data structure
implementations.

### `ArrayList`

A dynamic-array wrapper backed by a Python list.

Supported operations: - `access(index)` --- retrieve an element by
zero-based index. - `insert(index, value)` --- insert an element at a
specified position. - `delete(index)` --- remove and return an
element. - `to_list()` --- return a shallow copy of the stored
elements. - `len(array_list)` and iteration are supported.

### `Matrix`

A two-dimensional rectangular collection.

Supported operations: - `shape` --- obtain the number of rows and
columns. - `access(row, column)` --- retrieve an element. -
`set(row, column, value)` --- update an element. -
`insert_row(index, row)` --- insert a row. - `delete_row(index)` ---
remove and return a row. - `to_list()` --- return a copy of the matrix
data.

All rows must have the same number of columns. An invalid row width
raises `ValueError`.

### `ArrayStack`

A list-backed **last-in, first-out (LIFO)** stack.

Supported operations: - `push(value)` --- add an item to the top. -
`pop()` --- remove and return the top item. - `peek()` --- inspect the
top item without removing it. - `is_empty()` --- check whether the stack
is empty. - `len(stack)` --- obtain the number of stored items.

Attempting to call `pop()` or `peek()` on an empty stack raises
`IndexError`.

### `ArrayQueue`

A **first-in, first-out (FIFO)** queue implemented with a dynamically
resized circular buffer.

Supported operations: - `enqueue(value)` --- add an item to the rear. -
`dequeue()` --- remove and return the front item. - `peek()` --- inspect
the front item without removing it. - `is_empty()` and `len(queue)` ---
inspect the queue state.

The default initial capacity is 8. The buffer is expanded when full and
may be reduced when usage becomes sufficiently low, while maintaining a
minimum capacity of 8. An empty queue cannot be dequeued or peeked;
those operations raise `IndexError`.

### `SinglyLinkedList`

A singly linked list built from internal nodes.

Supported operations: - `prepend(value)` --- insert at the beginning. -
`append(value)` --- insert at the end. - `insert(index, value)` ---
insert at a zero-based position. - `delete(index)` --- remove and return
the value at an index. - `access(index)` --- retrieve a value by
index. - `find(value)` --- return the first matching index, or `-1` if
not found. - `traverse()` --- return the elements as a Python list. -
Iteration, `is_empty()`, and `len(linked_list)` are supported.

Invalid insertion or access positions raise `IndexError`.

## Part 3: Performance Analysis

The script `performance_analysis.py` imports the two selection functions
from `part1_selection_algorithms.py` and benchmarks them.

### Default Benchmark Configuration

  -----------------------------------------------------------------------
  Setting                             Default
  ----------------------------------- -----------------------------------
  Input sizes                         100, 500, 1,000, and 3,000

  Data distributions                  Random, sorted, reverse-sorted, and
                                      duplicate-heavy

  Repetitions per algorithm and case  3

  Selected rank                       Lower-median rank:
                                      `(size + 1) // 2`

  Timing statistic                    Median elapsed time
  -----------------------------------------------------------------------

For each test case, the expected selected value is calculated using
Python's `sorted()` function. Both algorithms are checked against this
expected value before timing results are recorded. A failed comparison
raises an `AssertionError`.

The benchmark data is generated with fixed seeds to make the test inputs
reproducible.

### Generated Files

After `performance_analysis.py` is executed, a `results/` directory is
created containing:

-   `benchmark_results.csv` --- benchmark records with algorithm name,
    input size, distribution, rank, median runtime, repetition count,
    and result-verification status.
-   `selection_runtime_random.png` --- runtime comparison for random
    inputs, when Matplotlib is available.
-   `selection_runtime_sorted.png` --- runtime comparison for sorted
    inputs, when Matplotlib is available.
-   `selection_runtime_reverse-sorted.png` --- runtime comparison for
    reverse-sorted inputs, when Matplotlib is available.
-   `selection_runtime_duplicates.png` --- runtime comparison for
    duplicate-heavy inputs, when Matplotlib is available.

The CSV file is generated even when Matplotlib is not installed. If
Matplotlib is unavailable, chart generation is skipped and a message is
printed.

## Complexity Overview

The following table summarises the principal expected or guaranteed
costs. Actual costs can depend on input size and operation position.

  -----------------------------------------------------------------------
  Component / operation               Time complexity
  ----------------------------------- -----------------------------------
  Deterministic selection             O(n) worst case

  Randomized Quickselect              O(n) expected; O(n²) worst case

  `ArrayList` access                  O(1)

  `ArrayList` insertion/deletion      O(n) in the general case

  `Matrix` element access/update      O(1)

  `Matrix` row insertion/deletion     O(r + c) in this list-based
                                      implementation, where r is the
                                      number of rows and c is the row
                                      width

  `ArrayStack` push/pop/peek          O(1) amortized for push; O(1) for
                                      pop and peek

  `ArrayQueue` enqueue/dequeue/peek   O(1) amortized for enqueue; O(1)
                                      for dequeue and peek

  `SinglyLinkedList` prepend          O(1)

  `SinglyLinkedList` append           O(n), because the tail is not
                                      stored

  `SinglyLinkedList` access/search    O(n)

  `SinglyLinkedList`                  O(n)
  insertion/deletion by index         
  -----------------------------------------------------------------------

## Notes and Limitations

-   Selection ranks are 1-based, while array, matrix, and linked-list
    positions are zero-based.
-   The selection algorithms accept mutually orderable values.
-   The data structure classes are educational implementations and are
    not intended to replace specialised production libraries.
-   The benchmark measures selection operations only; the reference
    sorting operation is used to verify correctness, not included in the
    reported selection runtime.
-   Benchmark timings vary with hardware, Python version, system load,
    and runtime environment. Results should be interpreted comparatively
    rather than as universal performance guarantees.
-   The assignment document and `results.zip` are included as repository
    assets; the scripts generate benchmark outputs in the `results/`
    directory when executed.

## Author

**Geetha Lahari Barlapudi**

## Repository

[Geetha-Lahari-Barlapudi ---
GitHub](https://github.com/thetaseven169-collab/Geetha-Lahari-Barlapudi)
