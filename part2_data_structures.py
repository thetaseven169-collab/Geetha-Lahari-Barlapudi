"""Elementary data structures

Includes:
- ArrayList: small dynamic-array abstraction which is backed by a Python list.
A 2-D rectangular collection with insertion, deletion and access is called Matrix.
- ArrayStack: implementation of the stack using an array (list in Python).
- ArrayQueue: Circular buffer queue that is based on a Python list.
SinglyLinkedList: Linked nodes can be inserted, deleted and traversed.

For arrays, matrices, and linked-list methods of positioning, indices are zero based.
"""
from __future__ import annotations

from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class ArrayList(Generic[T]):
    """Dynamic array wrapper with basic insertion, deletion, and access."""

    def __init__(self, values: Optional[Iterable[T]] = None) -> None:
        self._items: List[T] = list(values) if values is not None else []

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"ArrayList({self._items!r})"

    def access(self, index: int) -> T:
        """Return the item at a zero-based index."""
        return self._items[index]

    def insert(self, index: int, value: T) -> None:
        """Insert value before index; index may equal len(self)."""
        if not 0 <= index <= len(self._items):
            raise IndexError("Insertion index out of range.")
        self._items.insert(index, value)

    def delete(self, index: int) -> T:
        """Delete and return the item at index."""
        if not 0 <= index < len(self._items):
            raise IndexError("Deletion index out of range.")
        return self._items.pop(index)

    def to_list(self) -> List[T]:
        """Return a shallow copy of the stored values.""" 
        return self._items.copy()


class Matrix(Generic[T]):
    """Rectangular matrix supporting element access, row insertion/deletion."""

    def __init__(self, rows: Iterable[Iterable[T]]) -> None:
        self._rows: List[List[T]] = [list(row) for row in rows]
        if self._rows:
            width = len(self._rows[0])
            if any(len(row) != width for row in self._rows):
                raise ValueError("All matrix rows must have the same length.")

    @property
    def shape(self) -> tuple[int, int]:
        """Return (number_of_rows, number_of_columns)."""
        return (len(self._rows), len(self._rows[0]) if self._rows else 0)

    def access(self, row: int, column: int) -> T:
        return self._rows[row][column]

    def set(self, row: int, column: int, value: T) -> None:
        self._rows[row][column] = value

    def insert_row(self, index: int, row: Iterable[T]) -> None:
        new_row = list(row)
        columns = self.shape[1]
        if self._rows and len(new_row) != columns:
            raise ValueError("Inserted row must match the matrix column count.")
        if not 0 <= index <= len(self._rows):
            raise IndexError("Row insertion index out of range.")
        if not self._rows and index != 0:
            raise IndexError("Only index 0 is valid for an empty matrix.")
        self._rows.insert(index, new_row)

    def delete_row(self, index: int) -> List[T]:
        if not 0 <= index < len(self._rows):
            raise IndexError("Row deletion index out of range.")
        return self._rows.pop(index)

    def to_list(self) -> List[List[T]]:
        return [row.copy() for row in self._rows]

    def __repr__(self) -> str:
        return f"Matrix({self._rows!r})"


class ArrayStack(Generic[T]):
    """Last-in, first-out stack implemented with a Python list."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, value: T) -> None:
        self._items.append(value)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class ArrayQueue(Generic[T]):
    """First-in, first-out queue using a dynamically resized circular buffer."""

    def __init__(self, initial_capacity: int = 8) -> None:
        if not isinstance(initial_capacity, int) or isinstance(initial_capacity, bool):
            raise TypeError("initial_capacity must be an integer.")
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be at least 1.")
        self._items: List[Optional[T]] = [None] * initial_capacity
        self._head = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _resize(self, capacity: int) -> None:
        new_items: List[Optional[T]] = [None] * capacity
        for offset in range(self._size):
            new_items[offset] = self._items[(self._head + offset) % len(self._items)]
        self._items = new_items
        self._head = 0

    def enqueue(self, value: T) -> None:
        if self._size == len(self._items):
            self._resize(len(self._items) * 2)
        tail = (self._head + self._size) % len(self._items)
        self._items[tail] = value
        self._size += 1

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        value = self._items[self._head]
        self._items[self._head] = None
        self._head = (self._head + 1) % len(self._items)
        self._size -= 1
        if len(self._items) > 8 and self._size <= len(self._items) // 4:
            self._resize(max(8, len(self._items) // 2))
        return value  # type: ignore[return-value]

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue.")
        return self._items[self._head]  # type: ignore[return-value]


class _Node(Generic[T]):
    """Internal node for SinglyLinkedList."""

    __slots__ = ("value", "next")

    def __init__(self, value: T, next_node: Optional["_Node[T]"] = None) -> None:
        self.value = value
        self.next = next_node


class SinglyLinkedList(Generic[T]):
    """Singly linked list supporting insertion, deletion, search, and traversal."""

    def __init__(self, values: Optional[Iterable[T]] = None) -> None:
        self.head: Optional[_Node[T]] = None
        self._size = 0
        if values is not None:
            for value in values:
                self.append(value)

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def prepend(self, value: T) -> None:
        self.head = _Node(value, self.head)
        self._size += 1

    def append(self, value: T) -> None:
        node = _Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        if not 0 <= index <= self._size:
            raise IndexError("Insertion index out of range.")
        if index == 0:
            self.prepend(value)
            return
        previous = self._node_at(index - 1)
        previous.next = _Node(value, previous.next)
        self._size += 1

    def delete(self, index: int) -> T:
        if not 0 <= index < self._size:
            raise IndexError("Deletion index out of range.")
        if index == 0:
            assert self.head is not None
            removed = self.head
            self.head = removed.next
        else:
            previous = self._node_at(index - 1)
            assert previous.next is not None
            removed = previous.next
            previous.next = removed.next
        self._size -= 1
        return removed.value

    def _node_at(self, index: int) -> _Node[T]:
        if not 0 <= index < self._size:
            raise IndexError("Index out of range.")
        current = self.head
        for _ in range(index):
            assert current is not None
            current = current.next
        assert current is not None
        return current

    def access(self, index: int) -> T:
        return self._node_at(index).value

    def find(self, value: T) -> int:
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def traverse(self) -> List[T]:
        result: List[T] = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __iter__(self) -> Iterator[T]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"SinglyLinkedList({self.traverse()!r})"


if __name__ == "__main__":
    array = ArrayList([10, 20, 30])
    array.insert(1, 15)
    print("Array:", array.to_list(), "deleted:", array.delete(2))

    matrix = Matrix([[1, 2], [3, 4]])
    matrix.set(0, 1, 99)
    matrix.insert_row(2, [5, 6])
    print("Matrix:", matrix.to_list(), "shape:", matrix.shape)

    stack = ArrayStack[int]()
    stack.push(10)
    stack.push(20)
    print("Stack pop:", stack.pop())

    queue = ArrayQueue[int]()
    queue.enqueue(10)
    queue.enqueue(20)
    print("Queue dequeue:", queue.dequeue())

    linked = SinglyLinkedList([1, 2, 3])
    linked.insert(1, 99)
    print("Linked list:", linked.traverse(), "deleted:", linked.delete(2))
