""" Implementation of a node in linked lists and binary search trees. """

from __future__ import annotations
from typing import TypeVar, Generic
from dataclasses import dataclass

I = TypeVar('I')
K = TypeVar('K')

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'


@dataclass
class TreeNode(Generic[K, I]):
    """
    Node class represent BST nodes.
    """

    key: K
    item: I = None
    left: TreeNode | None = None
    right: TreeNode | None = None
    # This value should be maintained by yourself in bst.py
    subtree_size: int = 1

    def set_subtree_size(self, subtree_size: int) -> None:
        self.subtree_size = subtree_size

    def __str__(self):
        """
        Returns the string representation of a node

        Complexity: O(N) where N is the size of the item
        """
        key = str(self.key) if type(self.key) != str else "'{0}'".format(self.key)
        item = str(self.item) if type(self.item) != str else "'{0}'".format(self.item)
        return '({0}, {1}, [{2}])'.format(key, item, self.subtree_size)
