"""Max Heap implemented using an array"""
from __future__ import annotations

__author__ = "Brendon Taylor, modified by Jackson Goerner"
__docformat__ = 'reStructuredText'

from typing import Generic
from referential_array import ArrayR, T


class MaxHeap(Generic[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        """
        Initialises MaxHeap

        Complexity: O(max_size)
        where max_size is the maximum number of nodes in the MaxHeap
        """
        self.length: int = 0
        self.the_array: ArrayR[T] = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        """
        Returns the number of nodes in the tree.

        Complexity: O(1)
        """
        return self.length

    def is_full(self) -> bool:
        """
        Returns whether the heap is full

        Complexity: O(1)
        """
        return self.length + 1 == len(self.the_array)

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length

        Arguments:
            -k: Index of rising element

        Best Complexity: O(CompT) when node item is the minimum
        Worst Complexity: O(logN*CompT) when node item is the maximum
        where N is the number of nodes in the heap, and CompT is the complexity of comparing the items
        """
        item: T = self.the_array[k]

        while k > 1 and item > self.the_array[k // 2]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2

        self.the_array[k] = item

    def add(self, element: T) -> None:
        """
        Swaps elements while rising

        Arguments:
            -element: Adding element

        Complexity: O(rise)
        where rise is the complexity of the rise() method of the MaxHeap class
        """
        if self.is_full():
            raise IndexError

        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with the greatest value.
        :pre: 1 <= k <= self.length // 2

        Arguments:
            -k: Index of element

        Complexity: O(CompT)
        where CompT is the complexity of comparing the items
        """

        if 2 * k == self.length or self.the_array[2 * k] > self.the_array[2 * k + 1]:
            return 2 * k

        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """
        Make the element at index k sink to the correct position.
        :pre: 1 <= k <= self.length

        Arguments:
            -k: Index of sinking element

        Best Complexity: O(CompT) when node item is the maximum
        Worst Complexity: O(logN*CompT) when node item is the minimum
        where N is the number of nodes in the heap, and CompT is the complexity of comparing the items
        """
        item = self.the_array[k]

        while 2 * k <= self.length:
            max_child = self.largest_child(k)

            if self.the_array[max_child] <= item:
                break

            self.the_array[k] = self.the_array[max_child]
            k = max_child

        self.the_array[k] = item

    def get_max(self) -> T:
        """
        Remove (and return) the maximum element from the heap.

        Complexity: O(sink)
        where sink is the complexity of the sink() method of the MaxHeap class
        """
        if self.length == 0:
            raise IndexError

        max_elt = self.the_array[1]
        self.length -= 1

        if self.length > 0:
            self.the_array[1] = self.the_array[self.length + 1]
            self.sink(1)

        return max_elt

    def heapify_with_overwrite(self, overwriting_elements: list[T]):
        """
        Replaces the existing elements in the MaxHeap object with the provided list of overwriting elements.

        Arguments:
            -overwriting_elements: List of elements to overwrite the current nodes in the MaxHeap

        Complexity: O(n)
        Where n is the number of elements in the overwriting_elements list
        """
        self.length = 0

        for index in range(len(overwriting_elements)):
            if self.is_full():
                raise IndexError

            self.length += 1
            self.the_array[index + 1] = overwriting_elements[index]

        for inner_node in range(self.length // 2, 0, -1):
            self.sink(inner_node)


if __name__ == '__main__':
    items = [int(x) for x in input('Enter a list of numbers: ').strip().split()]
    heap = MaxHeap(len(items))

    for item in items:
        heap.add(item)

    while len(heap) > 0:
        print(heap.get_max())
