from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Mountain:
    name: str
    difficulty_level: int
    length: int

    def __eq__(self, other: Mountain) -> bool:
        """
        Magic method that allows the equality comparison between two Mountain
        objects. Two Mountain objects are equal when they both have the same 
        length and exact same name.

        Arguments:
            -other: Mountain Object

        Complexity: O(comp)
        """
        return self.length == other.length and self.name == other.name

    def __lt__(self, other: Mountain) -> bool:
        """
        Magic method that allows the "less than" comparison (<) between two
        Mountain objects. A Mountain object is less than another Mountain object
        when it has a lower length. If both Mountains are the same length, the
        mountain with a lower lexicographical name will be considered less than
        the mountain with a higher lexicographical name.

        Arguments:
            -other: Mountain Object

        Complexity: O(comp)
        """
        return (self.length, self.name) < (other.length, other.name)

    def __le__(self, other: Mountain) -> bool:
        """
        Magic method that allows the "less than or equal to" comparison (<=) between 
        two Mountain objects. Utilises the "lower than" magic method (__lt__) to 
        check if a Mountain object is lower than or equal to another.

        Arguments:
            -other: Mountain Object

        Complexity: O(comp)
        """
        return self < other or self == other

    def __gt__(self, other: Mountain) -> bool:
        """
        Magic method that allows the "greater than" comparison (>) between two
        Mountain objects. A Mountain object is greater than another Mountain object
        when it has a higher length. If both Mountains are the same length, the
        mountain with a higher lexicographical name will be considered greater than
        the mountain with a lower lexicographical name.

        Arguments:
            -other: Mountain Object

        Complexity: O(comp)
        """
        return (self.length, self.name) > (other.length, other.name)

    def __ge__(self, other: Mountain) -> bool:
        """
        Magic method that allows the "greater than or equal to" comparison (>=) 
        between two Mountain objects. Utilises the "greater than" magic method 
        (__gt__) to check if a Mountain object is lower than or equal to another.

        Arguments:
            -other: Mountain Object

        Complexity: O(comp)
        """
        return self > other or self == other
