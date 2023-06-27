from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree, TreeNode

T = TypeVar("T")
I = TypeVar("I")


class Percentiles(Generic[T]):

    def __init__(self):
        """
        Initialises Percentiles

        Complexity: O(1)
        """
        self.points = BinarySearchTree()

    def add_point(self, item: I) -> None:
        """
        Adds an item to the Percentiles object.

        Arguments:
            -item: Item Type

        Best Complexity: O(CompK) inserts the item at the root.
        Worst Complexity: O(CompK * D) inserting at the bottom of the tree
        where D is the depth of the tree, and CompK is the complexity of comparing the keys
        """
        self.points[item] = None

    def remove_point(self, item: I) -> None:
        """
        Removes an item to the Percentiles object.

        Arguments:
            -item: Item Type

        Best Complexity: O(CompK) when deleting item at root that has only one or no child
        Worst Complexity: O(CompK * D) when deleting item at leaf
        where D is the depth of the tree, and CompK is the complexity of comparing the keys
        """
        del self.points[item]

    def ratio(self, x: float, y: float) -> list[I]:
        """
        Computes a list of keys that satisfy a specific criterion based on the provided percentages.

        Arguments:
            x: The percentage of items that the selected item should be larger than.
            y: The percentage of items that the selected item should be smaller than.

        Complexity: O(_ratio_aux)
        where _ratio_aux is the complexity of the _ratio_aux() method of the Percentiles class
        """
        total_points: int = len(self.points)
        front_index: int = ceil(x / 100 * total_points)
        rear_index: int = total_points - ceil(y / 100 * total_points)

        return self._ratio_aux(self.points.root, front_index + 1, rear_index)

        # Calculate the front index and rear index based on the given percentages and call the helper function
        # _ratio_aux() to retrieve the range of keys.

    def _ratio_aux(self, current: TreeNode, front_index: int, rear_index: int, range_items: list[I] = None) -> list[I]:
        """
        Recursively retrieves the range of items falling within the range of given indices.

        Arguments:
            current: Root node of a current TreeNode
            front_index: Starting position of the range.
            rear_index: Ending position of the range.
            range_items: List of items falling within the range.

        Complexity: O(n)
        where n is the number of nodes in the BinarySearchTree
        """
        if range_items is None:
            range_items = []

        # For the first iteration of the recursion, range_keys is created to record the keys falling within the range
        # that were traversed.

        if current is None:
            return range_items

        # The base case is when current is None, indicating that the tree has been traversed to the end

        left_size = current.left.subtree_size if current.left else 0

        # Calculate the number of nodes in the left subtree, considering that if there is no left subtree, it will be
        # an error when accessing current.left.subtree_size.

        if front_index <= left_size + 1 <= rear_index:
            range_items.append(current.key)

        range_items = self._ratio_aux(current.left, front_index, rear_index, range_items)
        range_items = self._ratio_aux(current.right, front_index - left_size - 1, rear_index - left_size - 1, range_items)

        # The value of front and rear index is adjusted by deducting the left size and root (which is 1),
        # and the method is recursively called on the right subtree with the adjusted value of k.

        # Uses pre-order traversal, visiting the current node before its children. If the position of the current
        # node is within the range, append its key to the output list.

        return range_items


if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))
