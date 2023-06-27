from dataclasses import dataclass
from heap import MaxHeap


@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

    def __eq__(self, other) -> bool:
        """
        Magic method that allows the equality comparison between two Beehive
        objects. Two Mountain objects are equal when they both yield the same
        amount of emeralds

        Arguments:
            -other: Beehive Object

        Complexity: O(CompB)
        where CompB is the complexity of comparing the Beehives
        """
        return (min(self.capacity, self.volume) * self.nutrient_factor) == \
            (min(other.capacity, other.volume) * other.nutrient_factor)

    def __lt__(self, other) -> bool:
        """
        Magic method that allows the "less than" comparison (<) between two
        Beehive objects. A Beehive object is less than another Beehive object
        when it yields a lower amount of emeralds.

        Arguments:
            -other: Beehive Object

        Complexity: O(CompB)
        where CompB is the complexity of comparing the Beehives
        """
        return (min(self.capacity, self.volume) * self.nutrient_factor) < \
            (min(other.capacity, other.volume) * other.nutrient_factor)

    def __le__(self, other) -> bool:
        """
        Magic method that allows the "less than or equal to" comparison (<=) between
        two Beehive objects. Utilises the "lower than" magic method (__lt__) to
        check if a Beehive object is lower than or equal to another.

        Arguments:
            -other: Beehive Object

        Complexity: O(CompB)
        where CompB is the complexity of comparing the Beehives
        """
        return self < other or self == other

    def __gt__(self, other) -> bool:
        """
        Magic method that allows the "greater than" comparison (>) between two
        Beehive objects. A Beehive object is greaer than another Beehive object
        when it yields a larger amount of emeralds.

        Arguments:
            -other: Beehive Object

        Complexity: O(CompB)
        where CompB is the complexity of comparing the Beehives
        """
        return (min(self.capacity, self.volume) * self.nutrient_factor) > \
            (min(other.capacity, other.volume) * other.nutrient_factor)

    def __ge__(self, other) -> bool:
        """
        Magic method that allows the "greater than or equal to" comparison (>=)
        between two Beehive objects. Utilises the "greater than" magic method
        (__gt__) to check if a Beehive object is greater than or equal to another.

        Arguments:
            -other: Beehive Object

        Complexity: O(CompB)
        where CompB is the complexity of comparing the Beehives
        """
        return self > other or self == other


class BeehiveSelector:

    def __init__(self, max_beehives: int):
        """
        Initialisation for a BeehiveSelector object.

        Arguments:
            -max_beehives: The maximum number of beehives.

        Complexity: O(max_beehives)
        where max_beehives is the maximum number of beehives
        """
        self.heap: MaxHeap = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]):
        """
        Sets all beehives into the BeehiveSelector object with the Beehives given from hive_list.

        Arguments:
            -hive_list: List of Beehive objects

        Complexity: O(M)
        where M is the number of beehives in hive_list
        """
        self.heap.heapify_with_overwrite(hive_list)  # O(M)

    def add_beehive(self, hive: Beehive):
        """
        Adds a single Beehive object into the BeehiveSelector Object

        Arguments:
            -hive: Beehive object

        Complexity: O(logN)
        where N is the number of Beehives currently in the BeehiveSelector object
        """
        self.heap.add(hive)  # O(logN)

    def harvest_best_beehive(self) -> int:
        """
        Harvests the best beehive that yields the greatest amount of emeralds

        Complexity: O(logN)
        where N is the number of Beehives currently in the BeehiveSelector object
        """
        best_beehive: Beehive = self.heap.get_max()  # O(logN)
        emeralds: int = min(best_beehive.capacity, best_beehive.volume) * best_beehive.nutrient_factor
        best_beehive.volume -= min(best_beehive.capacity, best_beehive.volume)
        self.add_beehive(best_beehive)  # O(logN)

        return emeralds

        # Harvests the best Beehive that yields the greatest amount of emeralds with the "get_max()" method from
        # MaxHeap and the amount of emeralds is calculated. The best Beehive is now harvested and its volume is
        # reduced based on the minimum of its capacity and volume. Finally, the best Beehive is added back into the
        # MaxHeap, and returns the amount of emeralds gained.
