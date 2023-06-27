from __future__ import annotations
from mountain import Mountain
from algorithms.binary_search import binary_search
from algorithms.mergesort import mergesort


class MountainOrganiser:
    def __init__(self) -> None:
        """
        Initialisation for MountainOrganiser object.

        Complexity: O(1)
        """
        self.mountains: list[Mountain] = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Returns the current index position of a Mountain object based on its
        length increasing. In cases where the length is the same, a Mountain
        is ordered by name lexicographically increasing.

        :raises KeyError: when mountain has not been added yet

        Arguments:
            -mountain: Mountain Object

        Best Complexity: O(1) when mountain is located at the middle index of self.mountains
        Worst Complexity: O(log(n)) when mountain is located at the first or last index of self.mountains
        where n is the number of Mountains in self.mountains
        """
        return binary_search(self.mountains, mountain)

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Goes through a list of Mountain objects and insert them to self.mountains
        based on their length increasing. In cases where the length is the same, 
        a Mountain is inserted by name lexicographically increasing.

        Arguments:
            -mountains: list of Mountain Objects
            
        Complexity: O(m*log(m)+n)

        where m is the length of self.mountains, and n is the concatenation of lists.
        """
        self.mountains += mountains  # O(n)
        self.mountains = mergesort(self.mountains)  # O(m*log(m))
