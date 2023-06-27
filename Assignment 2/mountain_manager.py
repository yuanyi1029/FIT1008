from mountain import Mountain
from double_key_table import DoubleKeyTable
from algorithms.mergesort import mergesort


class MountainManager:

    def __init__(self) -> None:
        """
        Initialisation for MountainManager object.

        Complexity: O(DoubleKeyTable.__init__())
        """
        self.mountains: DoubleKeyTable = DoubleKeyTable()

        # Initialise self.mountains as a DoubleKeyTable to store a Mountain object's difficulty level as a top-level
        # key and the Mountain's name as a bottom-level key

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Adds a single Mountain object into the MountainManager object.

        Arguments:
            -mountain: Mountain Object

        Complexity: O(DoubleKeyTable.__setitem__())
        """
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain

        # Utilises the __setitem__ from the DoubleKeyTable to add a Mountain object where key1 = Mountain object's
        # difficulty level, key2 = Mountain name and value = Mountain object

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Removes a single Mountain object from the MountainManager object.

        Arguments:
            -mountain: Mountain Object

        Complexity: O(DoubleKeyTable.__delitem__())
        """
        del self.mountains[str(mountain.difficulty_level), mountain.name]

        # Utilises the __delitem__ from the DoubleKeyTable to delete a Mountain object by passing in the Mountain
        # object's difficulty level and name as keys. If the Mountain does not exist, a KeyError is raised

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Replaces an existing Mountain object from the MountainManager object
        with a new Mountain object.

        Arguments:
            -old: existing Mountain Object
            -new: new Mountain Object

        Complexity: O(remove_mountain + add_mountain)

        where remove_mountain is the complexity of the remove_mountain() method of the MountainManager class,
        add_mountain is the complexity of the add_mountain() method of the MountainManager class.
        """
        self.remove_mountain(old)
        self.add_mountain(new)

        # Removes an existing mountain with self.remove_mountain(old) and inserts a new mountain into the
        # DoubleKeyTable with self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Returns a list of Mountain objects grouped together by a certain
        difficulty level based on the input parameter

        Arguments:
            -diff: a Mountain object's difficulty level

        Complexity: O(DoubleKeyTable.values())
        """
        return self.mountains.values(str(diff))

        # Passes in a difficulty level into self.mountains.values() to get a list of values (Mountain objects) of
        # that certain key

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Returns a list of lists of Mountain objects grouped together by 
        their difficulty level.

        Best Complexity: O(DoubleKeyTable.keys()+nlog(n)+mountains_with_difficulty) when all the Mountain objects
        have the same difficulty level.
        Worst Complexity: O(n*mountains_with_difficulty) when each Mountain object has a different difficulty level.

        where n is the number of Mountains in self.mountains, and mountains_with_difficulty is the complexity of the
        mountains_with_difficulty method of the MountainManager class.
        """
        output: list[list[Mountain]] = []

        sorted_difficulty: list[int] = mergesort(self.mountains.keys())  # O(DoubleKeyTable.keys()+nlog(n))

        for difficulty in sorted_difficulty:  # O(n)
            output.append(self.mountains_with_difficulty(difficulty))  # O(mountains_with_difficulty)

        return output

        # Sorts through a list of top-level keys (Mountain object's difficulty level) in ascending order,
        # get each list of Mountain objects grouped by difficulty level and append them to output
