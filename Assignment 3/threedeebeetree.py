from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field
from referential_array import ArrayR

I = TypeVar('I')
Point = Tuple[int, int, int]


@dataclass
class BeeNode:
    """
    BeeNode class represent ThreeDeeBeeTree nodes.
    """

    key: Point
    item: I
    subtree_size: int = 1
    children: ArrayR[BeeNode] = field(default_factory=lambda: ArrayR(8))

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        """
        Get the children in the BeeNode

        Arguments:
            -point: Tuples representing the coordinates x, y, z

        Complexity: O(1)
        """
        index: int = self.get_child_index(point)
        return self.children[index]

    def get_child_index(self, point: Point) -> int:
        """
        Get the children index in the BeeNode

        Arguments:
            -point: Tuples representing the coordinates x, y, z

        Octant Indices:
            - Index 0: nnn (negative x, negative y, negative z)
            - Index 1: pnn (positive x, negative y, negative z)
            - Index 2: npn (negative x, positive y, negative z)
            - Index 3: ppn (positive x, positive y, negative z)
            - Index 4: nnp (negative x, negative y, positive z)
            - Index 5: pnp (positive x, negative y, positive z)
            - Index 6: npp (negative x, positive y, positive z)
            - Index 7: ppp (positive x, positive y, positive z)

        Octant Representation:
            - n represents less than the corresponding coordinate value
            - p represents greater than or equal to the corresponding coordinate value

        Complexity: O(1)
        """
        x: int
        y: int
        z: int
        x, y, z = point

        self_x: int
        self_y: int
        self_z: int
        self_x, self_y, self_z = self.key

        index: int = 0

        if x >= self_x:
            index += 1

        if y >= self_y:
            index += 2

        if z >= self_z:
            index += 4

        return index


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
        Initialises an empty 3DBT

        Complexity: O(1)
        """
        self.root: BeeNode | None = None
        self.length: int = 0

    def is_empty(self) -> bool:
        """
        Checks to see if the 3DBT is empty

        Complexity: O(1)
        """
        return len(self) == 0

    def __len__(self) -> int:
        """
        Returns the number of nodes in the tree

        Complexity: O(1)
        """
        return self.length

    def __contains__(self, key: Point) -> bool:
        """
        Checks to see if the key is in the 3DBT

        O(get_tree_node_by_key)
        where get_tree_node_by_key is the complexity of the get_tree_node_by_key() method of the ThreeDeeBeeTree class
        """
        try:
            self.get_tree_node_by_key(key)
            return True

        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
        Attempts to get an item in the tree, it uses the Key to attempt to find it

        Arguments:
            -key: Tuples representing the coordinates x, y, z

        Complexity: O(get_tree_node_by_key)
        where get_tree_node_by_key is the complexity of the get_tree_node_by_key() method of the ThreeDeeBeeTree class
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        """
        Get the BeeNode in the ThreeDeeBeeTree

        Arguments:
            -key: Tuples representing the coordinates x, y, z

        Complexity: O(get_tree_node_by_key_aux)
        where get_tree_node_by_key_aux is the complexity of the get_tree_node_by_key_aux() method of the
        ThreeDeeBeeTree class
        """
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: BeeNode, key: Point) -> BeeNode:
        """
        Auxiliary function of get_tree_node_by_key() method of the ThreeDeeBeeTree class

        :raises KeyError: key is not found in the ThreeDeeBeeTree

        Arguments:
            -current: BeeNode object
            -key: Tuples representing the coordinates x, y, z

        Best Complexity: O(CompK) when key is at the root
        Worst Complexity: O(CompK * D) when key is at the leaf
        where D is the depth of the tree, and CompK is the complexity of comparing the keys
        """
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))

        if key == current.key:
            return current

        index: int = current.get_child_index(key)

        return self.get_tree_node_by_key_aux(current.children[index], key)

        # Recursively traverses the child nodes of the ThreeDeeBeeTree starting from the current node with its child
        # index, comparing the provided key with the keys of the nodes. If a match is found, the corresponding
        # BeeNode object is returned. This process continues until a match is found or None is encountered,
        # indicating that the key is not present in the tree, which will raise a KeyError.

    def __setitem__(self, key: Point, item: I) -> None:
        """
        Set a (key, item) pair in the ThreeDeeBeeTree

        Arguments:
            -key: Tuples representing the coordinates x, y, z
            -item: Item Type

        Complexity: O(insert_aux)
        where insert_aux is the complexity of the insert_aux() method of the ThreeDeeBeeTree class
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
        Attempts to insert an item into the tree, it uses the Key to insert it

        Arguments:
            -current: BeeNode object
            -key: Point Type
            -item: Item Type

        Best Complexity: O(1) when inserting root
        Worst Complexity: O(D) when inserting leaf
        where D is the depth of the ThreeDeeBeeTree
        """
        if current is None:
            current = BeeNode(key, item=item)
            self.length += 1

        else:
            index: int = current.get_child_index(key)
            current.children[index] = self.insert_aux(current.children[index], key, item)  # O(D)
            current.subtree_size += 1

        return current

        # Attempts to insert the key item pair into the ThreeDeeBeeTree by recursively traversing the tree based on
        # the provided key. If the current node is None, indicating an empty spot in the ThreeDeeBeeTree,
        # a new BeeNode is created with the given key and item, and the length of the tree is incremented. Otherwise,
        # the function determines the appropriate child node index based on the key and recursively calls itself on
        # that child node. After each recursive call, the subtree size of the current node is updated accordingly.

    @staticmethod
    def is_leaf(current: BeeNode) -> bool:
        """
        Simple check whether the node is a leaf.

        Best Complexity: O(1) when current BeeNode has children at the first octant
        Worst Complexity: O(len(current.children)) when current BeeNode is a leaf
        """
        for index in range(len(current.children)):  # O(len(current.children))
            if current.children[index] is not None:
                return False

        return True

        # Iterates over the children of the current node and checks if any of them are not None. If at least one
        # child is not None, it means that the node is not a leaf, and False is returned. Otherwise, if all children
        # are None, it means that the node is a leaf, and True is returned.


if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size)  # 2
